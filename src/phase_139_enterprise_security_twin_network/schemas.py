"""
FastAPI request/response schemas for Enterprise Security Twin Network
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class DigitalTwinSchema(BaseModel):
    twin_id: Optional[str] = None
    name: Optional[str] = None
    target_tenant: Optional[str] = None
    status: Optional[str] = None

class EntityStateSchema(BaseModel):
    state_id: Optional[str] = None
    twin_id: Optional[str] = None
    entity_id: Optional[str] = None
    variables: Optional[Dict[str, Any]] = None

class SynchronizationJobSchema(BaseModel):
    job_id: Optional[str] = None
    twin_id: Optional[str] = None
    last_sync: Optional[str] = None
    status: Optional[str] = None

class RiskForecastSchema(BaseModel):
    forecast_id: Optional[str] = None
    twin_id: Optional[str] = None
    simulated_incidents: Optional[int] = None
    projected_loss: Optional[float] = None

class ExecutionRequest(BaseModel):
    tenant_id: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    status: str
    phase: int
    result: Dict[str, Any]
