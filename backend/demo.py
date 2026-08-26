"""
RealityOS MVP Demo

Run from the backend/ directory after installing requirements:

    python demo.py
"""

from app.services.simulation import SimulationEngine
from app.services.scenario import ScenarioService
from app.models.domain import DataSource, DataSourceType


def main():
    engine = SimulationEngine()
    scenarios = ScenarioService(engine)

    print("=== RealityOS MVP Demo ===\n")

    # 1. Create organization
    org = engine.create_organization(name="Acme Industrial", industry="Manufacturing")
    print(f"Created organization: {org.name} ({org.id})")

    # 2. Connect progressive data sources
    crm = DataSource(
        organization_id=org.id,
        type=DataSourceType.CRM,
        name="Salesforce Production",
        health_score=0.88,
    )
    engine.add_data_source(org.id, crm)
    print("Connected CRM data source")

    accounting = DataSource(
        organization_id=org.id,
        type=DataSourceType.ACCOUNTING,
        name="NetSuite",
        health_score=0.91,
    )
    engine.add_data_source(org.id, accounting)
    print("Connected Accounting data source")

    sim = engine.get_simulation(org.id)
    print(f"\nSimulation fidelity: {sim.fidelity_score:.2f}")
    print(f"Status: {sim.status.value}")
    print(f"Entities: {sim.entity_counts}")
    print(f"Key metrics: {sim.key_metrics}")

    # 3. Ask scenarios
    print("\n--- Scenario 1: Pricing ---")
    pred1 = scenarios.ask(
        organization_id=org.id,
        question="What happens if we raise prices 7% across the board?",
        parameters={"percent_change": 7.0},
    )
    print(f"Confidence: {pred1.confidence:.0%}")
    print(f"Outcomes: {pred1.outcomes}")
    print(f"Key drivers: {pred1.key_drivers}")
    print(f"Recommended actions: {pred1.recommended_actions}")

    print("\n--- Scenario 2: Hiring ---")
    pred2 = scenarios.ask(
        organization_id=org.id,
        question="What happens if we hire 40 additional engineers?",
        parameters={"count": 40, "fully_loaded_cost": 165000},
    )
    print(f"Confidence: {pred2.confidence:.0%}")
    print(f"Outcomes: {pred2.outcomes}")
    print(f"Recommended actions: {pred2.recommended_actions}")

    print("\n--- Scenario 3: Supplier risk ---")
    pred3 = scenarios.ask(
        organization_id=org.id,
        question="What happens if our primary steel supplier fails for 6 weeks?",
    )
    print(f"Confidence: {pred3.confidence:.0%}")
    print(f"Outcomes: {pred3.outcomes}")
    print(f"Recommended actions: {pred3.recommended_actions}")

    print("\nDemo complete. Start the API with:")
    print("  uvicorn app.main:app --reload")
    print("Then open http://localhost:8000/docs")


if __name__ == "__main__":
    main()
