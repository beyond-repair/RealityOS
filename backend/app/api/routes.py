"""
RealityOS HTTP API

All endpoints are designed so that autonomous agents can drive the system
with minimal or zero human interaction after initial organization creation.
"""

from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.models.domain import DataSource, DataSourceType, Organization, Prediction, SimulationState
from app.services.simulation import SimulationEngine
from app.services.scenario import ScenarioService

router = APIRouter()

# Shared singletons for MVP (replace with proper DI / DB later)
engine = SimulationEngine()
scenario_service = ScenarioService(engine)


class CreateOrganizationRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    industry: Optional[str] = None


class AddDataSourceRequest(BaseModel):
    type: DataSourceType
    name: str
    connector_config: dict[str, Any] = Field(default_factory=dict)
    health_score: float = Field(default=0.8, ge=0.0, le=1.0)


class AskScenarioRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=1000)
    parameters: dict[str, Any] = Field(default_factory=dict)
    created_by: Optional[str] = None


@router.post("/organizations", response_model=Organization, tags=["Organizations"])
def create_organization(req: CreateOrganizationRequest):
    """Create a new organization and bootstrap its living simulation."""
    org = engine.create_organization(name=req.name, industry=req.industry)
    return org


@router.get("/organizations/{org_id}", response_model=Organization, tags=["Organizations"])
def get_organization(org_id: str):
    org = engine.get_organization(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


@router.get("/organizations/{org_id}/simulation", response_model=SimulationState, tags=["Simulation"])
def get_simulation(org_id: str):
    sim = engine.get_simulation(org_id)
    if not sim:
        raise HTTPException(status_code=404, detail="Simulation not found")
    return sim


@router.post("/organizations/{org_id}/data-sources", response_model=DataSource, tags=["Data Sources"])
def add_data_source(org_id: str, req: AddDataSourceRequest):
    """Connect a new progressive data source. Increases simulation fidelity."""
    if not engine.get_organization(org_id):
        raise HTTPException(status_code=404, detail="Organization not found")

    source = DataSource(
        organization_id=org_id,
        type=req.type,
        name=req.name,
        connector_config=req.connector_config,
        health_score=req.health_score,
    )
    return engine.add_data_source(org_id, source)


@router.get("/organizations/{org_id}/data-sources", response_model=list[DataSource], tags=["Data Sources"])
def list_data_sources(org_id: str):
    if not engine.get_organization(org_id):
        raise HTTPException(status_code=404, detail="Organization not found")
    return engine.list_data_sources(org_id)


@router.post("/organizations/{org_id}/scenarios", response_model=Prediction, tags=["Scenarios"])
def ask_scenario(org_id: str, req: AskScenarioRequest):
    """
    Ask a ‘What happens if…?’ question against the living simulation.

    Returns a structured Prediction with confidence, drivers, actions, and provenance.
    """
    if not engine.get_organization(org_id):
        raise HTTPException(status_code=404, detail="Organization not found")

    prediction = scenario_service.ask(
        organization_id=org_id,
        question=req.question,
        parameters=req.parameters,
        created_by=req.created_by,
    )
    return prediction


@router.get("/organizations/{org_id}/predictions", response_model=list[Prediction], tags=["Scenarios"])
def list_predictions(org_id: str):
    if not engine.get_organization(org_id):
        raise HTTPException(status_code=404, detail="Organization not found")
    return scenario_service.list_predictions(org_id)


@router.post("/organizations/{org_id}/simulation/advance", response_model=SimulationState, tags=["Simulation"])
def advance_simulation(org_id: str):
    """Manually advance the living simulation (normally done by a background agent)."""
    try:
        return engine.advance_simulation(org_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
