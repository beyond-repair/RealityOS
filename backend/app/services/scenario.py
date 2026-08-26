"""
Scenario evaluation service.

Turns natural-language ‘What happens if…?’ questions into structured,
confidence-scored Predictions against the living simulation.
"""

from __future__ import annotations

from app.models.domain import Scenario, Prediction
from app.services.simulation import SimulationEngine


class ScenarioService:
    def __init__(self, engine: SimulationEngine):
        self.engine = engine
        self._scenarios: dict[str, Scenario] = {}
        self._predictions: dict[str, Prediction] = {}

    def ask(
        self,
        organization_id: str,
        question: str,
        parameters: dict | None = None,
        created_by: str | None = None,
    ) -> Prediction:
        parameters = parameters or {}

        scenario = Scenario(
            organization_id=organization_id,
            question=question,
            parameters=parameters,
            created_by=created_by,
        )
        self._scenarios[scenario.id] = scenario

        result = self.engine.estimate_scenario_impact(
            org_id=organization_id,
            question=question,
            parameters=parameters,
        )

        prediction = Prediction(
            scenario_id=scenario.id,
            organization_id=organization_id,
            summary=self._build_summary(question, result),
            outcomes=result["outcomes"],
            confidence=result["confidence"],
            key_drivers=result["key_drivers"],
            recommended_actions=result["recommended_actions"],
            provenance=result["provenance"],
        )
        self._predictions[prediction.id] = prediction
        return prediction

    def get_prediction(self, prediction_id: str) -> Prediction | None:
        return self._predictions.get(prediction_id)

    def list_predictions(self, organization_id: str) -> list[Prediction]:
        return [p for p in self._predictions.values() if p.organization_id == organization_id]

    @staticmethod
    def _build_summary(question: str, result: dict) -> str:
        conf = result["confidence"]
        conf_label = "high" if conf >= 0.75 else "moderate" if conf >= 0.5 else "low"
        return (
            f"Scenario evaluated with {conf_label} confidence ({conf:.0%}). "
            f"Key outcomes and recommended actions are available in structured form."
        )
