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
