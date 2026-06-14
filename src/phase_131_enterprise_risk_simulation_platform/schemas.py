"""
FastAPI request/response schemas for Enterprise Risk Simulation Platform
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class SimulationSchema(BaseModel):
    simulation_id: Optional[str] = None
    name: Optional[str] = None
    threat_vector: Optional[str] = None
    status: Optional[str] = None
    duration: Optional[float] = None

class SimulationResultSchema(BaseModel):
    result_id: Optional[str] = None
    simulation_id: Optional[str] = None
    losses_prevented: Optional[float] = None
    breach_probability: Optional[float] = None

class ThreatVectorSchema(BaseModel):
    vector_id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    severity: Optional[str] = None

class ForecastModelSchema(BaseModel):
    model_id: Optional[str] = None
    name: Optional[str] = None
    accuracy: Optional[float] = None

class ExecutionRequest(BaseModel):
    tenant_id: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    status: str
    phase: int
    result: Dict[str, Any]
