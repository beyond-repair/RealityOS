"""Claim-capped unit tests for the RealityOS MVP simulation engine.

These tests check local heuristics only. They do not validate calibration,
connectors, or operating-system behavior.
"""

import random

import pytest

from app.models.domain import DataSource, DataSourceType, SimulationStatus
from app.services.simulation import SimulationEngine


def test_create_organization_bootstraps_low_fidelity():
    engine = SimulationEngine()
    org = engine.create_organization("Acme", "software")
    sim = engine.get_simulation(org.id)
    assert org.name == "Acme"
    assert sim is not None
    assert sim.organization_id == org.id
    assert sim.fidelity_score == 0.05
    assert sim.status == SimulationStatus.INITIALIZING
    assert engine.list_data_sources(org.id) == []


def test_unknown_organization_is_rejected():
    engine = SimulationEngine()
    source = DataSource(
        organization_id="missing",
        type=DataSourceType.ERP,
        name="none",
        health_score=0.9,
    )
    with pytest.raises(ValueError, match="not found"):
        engine.add_data_source("missing", source)


def test_high_health_sources_raise_fidelity_to_cap_and_live():
    random.seed(1)
    engine = SimulationEngine()
    org = engine.create_organization("Acme")
    for index in range(20):
        engine.add_data_source(
            org.id,
            DataSource(
                organization_id=org.id,
                type=DataSourceType.CRM,
                name=f"crm-{index}",
                health_score=0.9,
            ),
        )
    sim = engine.get_simulation(org.id)
    assert sim.fidelity_score == 0.95
    assert sim.status == SimulationStatus.LIVE
    assert sim.entity_counts["customers"] > 0


def test_price_scenario_stays_heuristic():
    engine = SimulationEngine()
    org = engine.create_organization("Acme")
    result = engine.estimate_scenario_impact(
        org.id,
        "What if we change pricing?",
        {"percent_change": 10},
    )
    assert result["provenance"]["model_version"] == "mvp-heuristic-0.1"
    assert 0.0 <= result["confidence"] <= 0.95
    assert "revenue_change_pct" in result["outcomes"]
    assert result["provenance"]["fidelity_score"] == 0.05


def test_one_high_health_source_rounds_fidelity_and_stays_initializing():
    engine = SimulationEngine()
    org = engine.create_organization("Acme")
    engine.add_data_source(
        org.id,
        DataSource(
            organization_id=org.id,
            type=DataSourceType.CRM,
            name="crm",
            health_score=0.9,
        ),
    )
    sim = engine.get_simulation(org.id)
    assert sim.fidelity_score == 0.17
    assert sim.status == SimulationStatus.INITIALIZING
    assert sim.entity_counts["customers"] > 0


def test_two_high_health_sources_cross_live_threshold():
    engine = SimulationEngine()
    org = engine.create_organization("Acme")
    for name, source_type in (("crm", DataSourceType.CRM), ("books", DataSourceType.ACCOUNTING)):
        engine.add_data_source(
            org.id,
            DataSource(
                organization_id=org.id,
                type=source_type,
                name=name,
                health_score=0.9,
            ),
        )
    sim = engine.get_simulation(org.id)
    assert sim.fidelity_score == 0.29
    assert sim.status == SimulationStatus.LIVE
    assert "monthly_revenue" in sim.key_metrics


def test_low_health_source_adds_smaller_fidelity_step():
    engine = SimulationEngine()
    org = engine.create_organization("Acme")
    engine.add_data_source(
        org.id,
        DataSource(
            organization_id=org.id,
            type=DataSourceType.SUPPORT,
            name="desk",
            health_score=0.4,
        ),
    )
    sim = engine.get_simulation(org.id)
    assert sim.fidelity_score == 0.11
    assert sim.entity_counts["tickets"] > 0


def test_price_heuristic_is_the_documented_elasticity():
    engine = SimulationEngine()
    org = engine.create_organization("Acme")
    result = engine.estimate_scenario_impact(org.id, "change pricing", {"percent_change": 10})
    # demand_impact = -0.6 * (pct/10); revenue = pct/100 + demand_impact
    assert result["outcomes"]["revenue_change_pct"] == -50.0
    assert result["outcomes"]["customer_churn_delta_pct"] == 24.0
    assert result["confidence"] == 0.342
    assert result["provenance"]["model_version"] == "mvp-heuristic-0.1"


def test_hiring_heuristic_uses_count_and_loaded_cost():
    engine = SimulationEngine()
    org = engine.create_organization("Acme")
    result = engine.estimate_scenario_impact(
        org.id,
        "hire more engineers",
        {"count": 40, "fully_loaded_cost": 165000},
    )
    assert result["outcomes"]["annual_cost_increase"] == 6_600_000
    assert result["outcomes"]["productivity_lag_months"] == 3.5
    assert result["outcomes"]["expected_revenue_uplift_pct"] == 18.0
    assert result["confidence"] == 0.323


def test_supplier_heuristic_is_seeded_range():
    random.seed(0)
    engine = SimulationEngine()
    org = engine.create_organization("Acme")
    result = engine.estimate_scenario_impact(org.id, "primary supplier fails", {})
    assert result["outcomes"]["revenue_at_risk_pct"] == 19.2
    assert result["outcomes"]["time_to_recover_weeks"] == 11.3
    assert result["confidence"] == 0.304


def test_generic_question_stays_low_confidence():
    random.seed(1)
    engine = SimulationEngine()
    org = engine.create_organization("Acme")
    result = engine.estimate_scenario_impact(org.id, "open a new office", {})
    assert result["outcomes"]["expected_impact"] == "moderate"
    assert result["outcomes"]["direction"] in {"positive", "negative", "mixed"}
    assert result["confidence"] == 0.209


def test_missing_simulation_rejects_scenario_and_advance():
    engine = SimulationEngine()
    with pytest.raises(ValueError, match="No simulation"):
        engine.estimate_scenario_impact("missing", "pricing", {})
    with pytest.raises(ValueError, match="No simulation"):
        engine.advance_simulation("missing")


def test_advance_applies_one_seeded_drift_to_revenue():
    engine = SimulationEngine()
    org = engine.create_organization("Acme")
    engine.add_data_source(
        org.id,
        DataSource(
            organization_id=org.id,
            type=DataSourceType.ACCOUNTING,
            name="books",
            health_score=0.5,
        ),
    )
    before = engine.get_simulation(org.id).key_metrics["monthly_revenue"]
    random.seed(2)
    advanced = engine.advance_simulation(org.id)
    random.seed(2)
    drift = random.uniform(-0.03, 0.04)
    assert advanced.key_metrics["monthly_revenue"] == round(before * (1 + drift), 2)


def test_scenario_service_stores_prediction():
    from app.services.scenario import ScenarioService

    engine = SimulationEngine()
    org = engine.create_organization("Acme")
    service = ScenarioService(engine)
    prediction = service.ask(org.id, "What if we change pricing?", {"percent_change": 7})
    assert prediction.provenance["model_version"] == "mvp-heuristic-0.1"
    assert "confidence" in prediction.summary
    assert service.get_prediction(prediction.id) == prediction
    assert service.list_predictions(org.id) == [prediction]
    assert service.list_predictions("other") == []


def test_quality_agent_flags_low_fidelity_and_missing_org():
    from app.agents.simulation_quality import SimulationQualityAgent

    engine = SimulationEngine()
    org = engine.create_organization("Acme")
    agent = SimulationQualityAgent(engine)
    report = agent.evaluate(org.id)
    assert report["current_fidelity"] == 0.05
    assert report["status"] == "initializing"
    assert any("CRM" in item for item in report["recommendations"])
    missing = agent.evaluate("missing")
    assert missing["status"] == "error"


def test_http_api_documented_flow():
    from fastapi.testclient import TestClient

    from app.main import app

    client = TestClient(app)
    root = client.get("/")
    assert root.status_code == 200
    body = root.json()
    assert body["status"] == "ok"
    assert body["persistence"] == "in-memory"
    assert body["model_version"] == "mvp-heuristic-0.1"
    assert client.get("/health").json() == {"status": "ok"}

    created = client.post(
        "/v1/organizations",
        json={"name": "Acme Industrial", "industry": "Manufacturing"},
    )
    assert created.status_code == 200
    org_id = created.json()["id"]
    assert client.get(f"/v1/organizations/{org_id}").json()["name"] == "Acme Industrial"

    source = client.post(
        f"/v1/organizations/{org_id}/data-sources",
        json={"type": "crm", "name": "Salesforce Production", "health_score": 0.88},
    )
    assert source.status_code == 200
    assert source.json()["type"] == "crm"
    listed = client.get(f"/v1/organizations/{org_id}/data-sources")
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    sim = client.get(f"/v1/organizations/{org_id}/simulation")
    assert sim.status_code == 200
    assert sim.json()["fidelity_score"] == 0.17
    assert sim.json()["status"] == "initializing"

    asked = client.post(
        f"/v1/organizations/{org_id}/scenarios",
        json={"question": "What happens if we raise prices 7%?", "parameters": {"percent_change": 7}},
    )
    assert asked.status_code == 200
    prediction = asked.json()
    assert prediction["provenance"]["model_version"] == "mvp-heuristic-0.1"
    assert prediction["outcomes"]["revenue_change_pct"] == -35.0
    preds = client.get(f"/v1/organizations/{org_id}/predictions")
    assert preds.status_code == 200
    assert len(preds.json()) >= 1

    advanced = client.post(f"/v1/organizations/{org_id}/simulation/advance")
    assert advanced.status_code == 200
    assert advanced.json()["organization_id"] == org_id

    assert client.get("/v1/organizations/missing").status_code == 404
    assert client.post(
        "/v1/organizations/missing/scenarios",
        json={"question": "What happens if we raise prices?"},
    ).status_code == 404
    assert client.post("/v1/organizations", json={"name": ""}).status_code == 422
    assert client.get("/docs").status_code == 200
    assert client.get("/openapi.json").status_code == 200


def test_demo_script_prints_heuristic_banner(capsys):
    from demo import main

    main()
    out = capsys.readouterr().out
    assert "RealityOS MVP Demo" in out
    assert "mvp-heuristic-0.1" in out
    assert "Simulation fidelity: 0.29" in out
    assert "Demo complete" in out
