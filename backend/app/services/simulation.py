"""
Living Simulation Engine – the core of RealityOS.

MVP implementation uses deterministic + lightly stochastic models so that
the system is fully runnable today. Real production versions will replace
the internal models with learned cross-organization patterns while keeping
the same external interface (confidence scores, provenance, progressive fidelity).
"""

from __future__ import annotations

import random
from datetime import datetime
from typing import Any

from app.models.domain import (
    Organization,
    SimulationState,
    SimulationStatus,
    DataSource,
)


class SimulationEngine:
    """
    Maintains and advances the living simulation for an organization.

    Design invariants:
    - Fidelity starts low and rises as more high-quality data sources are connected
      and as prediction → outcome feedback is received.
    - Every state change records provenance.
    - The engine never claims certainty; confidence is always explicit.
    """

    def __init__(self):
        # In-memory store for MVP. Replace with proper persistence layer later.
        self._simulations: dict[str, SimulationState] = {}
        self._organizations: dict[str, Organization] = {}
        self._data_sources: dict[str, list[DataSource]] = {}

    def create_organization(self, name: str, industry: str | None = None) -> Organization:
        org = Organization(name=name, industry=industry)
        self._organizations[org.id] = org

        # Bootstrap an empty simulation
        sim = SimulationState(
            organization_id=org.id,
            status=SimulationStatus.INITIALIZING,
            fidelity_score=0.05,
            entity_counts={},
            key_metrics={},
        )
        self._simulations[org.id] = sim
        self._data_sources[org.id] = []
        return org

    def get_organization(self, org_id: str) -> Organization | None:
        return self._organizations.get(org_id)

    def get_simulation(self, org_id: str) -> SimulationState | None:
        return self._simulations.get(org_id)

    def list_data_sources(self, org_id: str) -> list[DataSource]:
        return self._data_sources.get(org_id, [])

    def add_data_source(self, org_id: str, source: DataSource) -> DataSource:
        if org_id not in self._organizations:
            raise ValueError(f"Organization {org_id} not found")

        sources = self._data_sources.setdefault(org_id, [])
        sources.append(source)

        # Progressive fidelity increase
        sim = self._simulations[org_id]
        base_boost = 0.12 if source.health_score > 0.7 else 0.06
        sim.fidelity_score = min(0.95, sim.fidelity_score + base_boost)
        sim.status = SimulationStatus.LIVE if sim.fidelity_score > 0.25 else SimulationStatus.INITIALIZING
        sim.updated_at = datetime.utcnow()

        # Naive entity count growth for demonstration
        if source.type.value == "crm":
            sim.entity_counts["customers"] = sim.entity_counts.get("customers", 0) + random.randint(200, 2000)
            sim.entity_counts["opportunities"] = sim.entity_counts.get("opportunities", 0) + random.randint(50, 400)
        elif source.type.value == "accounting":
            sim.entity_counts["invoices"] = sim.entity_counts.get("invoices", 0) + random.randint(100, 1500)
            sim.key_metrics["monthly_revenue"] = round(random.uniform(80_000, 1_200_000), 2)
        elif source.type.value == "support":
            sim.entity_counts["tickets"] = sim.entity_counts.get("tickets", 0) + random.randint(300, 5000)

        return source

    def advance_simulation(self, org_id: str) -> SimulationState:
        """
        Called periodically (or by an agent) to keep the simulation living.
        In production this would ingest new events and recalibrate models.
        """
        sim = self._simulations.get(org_id)
        if not sim:
            raise ValueError(f"No simulation for organization {org_id}")

        # Simple drift + noise to keep the world feeling alive
        for key in list(sim.key_metrics.keys()):
            current = sim.key_metrics[key]
            drift = random.uniform(-0.03, 0.04)
            sim.key_metrics[key] = round(current * (1 + drift), 2)

        sim.updated_at = datetime.utcnow()
        return sim

    def estimate_scenario_impact(
        self,
        org_id: str,
        question: str,
        parameters: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Core prediction primitive used by the ScenarioService.

        Returns a structured result containing:
        - predicted outcomes
        - confidence
        - key drivers
        - provenance
        """
        sim = self._simulations.get(org_id)
        if not sim:
            raise ValueError(f"No simulation for organization {org_id}")

        fidelity = sim.fidelity_score
        base_confidence = min(0.92, 0.35 + fidelity * 0.6)

        # Extremely simplified impact models for MVP.
        # Real system will use learned causal / simulation models.
        outcomes: dict[str, Any] = {}
        drivers: list[str] = []
        actions: list[str] = []

        q = question.lower()

        if "price" in q or "pricing" in q:
            pct = float(parameters.get("percent_change", 5.0))
            # Rough elasticity assumption
            demand_impact = -0.6 * (pct / 10.0)
            revenue_impact = pct / 100.0 + demand_impact
            outcomes["revenue_change_pct"] = round(revenue_impact * 100, 1)
            outcomes["customer_churn_delta_pct"] = round(abs(demand_impact) * 40, 1)
            drivers = ["historical price elasticity", "current competitive intensity", "customer segment mix"]
            actions = [
                "Segment price changes by customer value tier",
                "Monitor early churn signals for 30 days",
                "Prepare targeted retention offers for price-sensitive cohorts",
            ]
            confidence = base_confidence * 0.9

        elif "hire" in q or "hiring" in q or "headcount" in q:
            count = int(parameters.get("count", 10))
            cost_per = float(parameters.get("fully_loaded_cost", 120000))
            outcomes["annual_cost_increase"] = count * cost_per
            outcomes["productivity_lag_months"] = 3.5
            outcomes["expected_revenue_uplift_pct"] = round(min(18.0, count * 0.7), 1)
            drivers = ["current utilization", "ramp time by role", "manager span of control"]
            actions = [
                "Stagger start dates to protect manager capacity",
                "Define 90-day success metrics before offers",
            ]
            confidence = base_confidence * 0.85

        elif "supplier" in q or "supply" in q:
            outcomes["revenue_at_risk_pct"] = round(random.uniform(4.0, 22.0), 1)
            outcomes["time_to_recover_weeks"] = round(random.uniform(3.0, 14.0), 1)
            drivers = ["supplier concentration", "inventory buffer days", "alternative supplier readiness"]
            actions = [
                "Activate secondary supplier qualification",
                "Increase safety stock on critical SKUs",
                "Communicate proactively with top customers",
            ]
            confidence = base_confidence * 0.8

        else:
            # Generic fallback
            outcomes["expected_impact"] = "moderate"
            outcomes["direction"] = random.choice(["positive", "negative", "mixed"])
            drivers = ["limited historical analogues", "current simulation fidelity"]
            actions = ["Gather more specific parameters", "Connect additional high-value data sources"]
            confidence = base_confidence * 0.55

        return {
            "outcomes": outcomes,
            "confidence": round(min(0.95, confidence), 3),
            "key_drivers": drivers,
            "recommended_actions": actions,
            "provenance": {
                "simulation_id": sim.id,
                "fidelity_score": sim.fidelity_score,
                "data_sources_used": [s.type.value for s in self._data_sources.get(org_id, [])],
                "model_version": "mvp-heuristic-0.1",
            },
        }
