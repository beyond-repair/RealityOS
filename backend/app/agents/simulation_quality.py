"""
Simulation Quality Agent (stub)

In the full autonomous system this agent runs on a schedule, monitors
fidelity scores, triggers additional data source deepening, and raises
alerts when prediction calibration drifts.
"""

from __future__ import annotations

from app.services.simulation import SimulationEngine


class SimulationQualityAgent:
    def __init__(self, engine: SimulationEngine):
        self.engine = engine

    def evaluate(self, org_id: str) -> dict:
        sim = self.engine.get_simulation(org_id)
        if not sim:
            return {"status": "error", "message": "Simulation not found"}

        recommendations = []
        if sim.fidelity_score < 0.4:
            recommendations.append("Connect at least one high-health CRM or accounting source")
        if sim.fidelity_score < 0.7:
            recommendations.append("Enable outcome feedback loop to improve calibration")
        if not recommendations:
            recommendations.append("Fidelity is healthy. Continue normal operation.")

        return {
            "organization_id": org_id,
            "current_fidelity": sim.fidelity_score,
            "status": sim.status.value,
            "recommendations": recommendations,
        }
