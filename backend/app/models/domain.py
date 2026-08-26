"""
Core domain models for RealityOS.

Design principles encoded here:
- Every prediction carries confidence and provenance
- Simulations are living (continuously updated)
- Data sources are progressive (start shallow, deepen over time)
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class DataSourceType(str, Enum):
    CRM = "crm"
    ERP = "erp"
    ACCOUNTING = "accounting"
    SUPPORT = "support"
    COMMUNICATION = "communication"
    INVENTORY = "inventory"
    MARKET = "market"
    CUSTOM = "custom"


class SimulationStatus(str, Enum):
    INITIALIZING = "initializing"
    LIVE = "live"
    DEGRADED = "degraded"
    PAUSED = "paused"


class Organization(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    industry: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DataSource(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    organization_id: str
    type: DataSourceType
    name: str
    connector_config: dict[str, Any] = Field(default_factory=dict)
    last_synced_at: Optional[datetime] = None
    health_score: float = Field(default=0.0, ge=0.0, le=1.0)  # 0–1
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SimulationState(BaseModel):
    """Living representation of an organization at a point in time."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    organization_id: str
    status: SimulationStatus = SimulationStatus.INITIALIZING
    fidelity_score: float = Field(default=0.0, ge=0.0, le=1.0)  # overall model quality
    last_calibrated_at: Optional[datetime] = None
    entity_counts: dict[str, int] = Field(default_factory=dict)  # e.g. {"customers": 1240, "contracts": 87}
    key_metrics: dict[str, float] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Scenario(BaseModel):
    """A ‘What happens if…?’ question posed to the simulation."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    organization_id: str
    question: str
    parameters: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None  # user or agent id


class Prediction(BaseModel):
    """Result of evaluating a scenario against the living simulation."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    scenario_id: str
    organization_id: str
    summary: str
    outcomes: dict[str, Any] = Field(default_factory=dict)  # metric → predicted value / distribution
    confidence: float = Field(ge=0.0, le=1.0)
    key_drivers: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)
    provenance: dict[str, Any] = Field(default_factory=dict)  # which data sources & models contributed
    created_at: datetime = Field(default_factory=datetime.utcnow)
