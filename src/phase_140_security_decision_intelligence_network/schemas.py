"""
FastAPI request/response schemas for Security Decision Intelligence Network
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class RecommendationEngineSchema(BaseModel):
    engine_id: Optional[str] = None
    name: Optional[str] = None
    version: Optional[str] = None

class DecisionScenarioSchema(BaseModel):
    scenario_id: Optional[str] = None
    decision_name: Optional[str] = None
    alternatives: Optional[List[str]] = None

class ImpactForecastSchema(BaseModel):
    forecast_id: Optional[str] = None
    scenario_id: Optional[str] = None
    metrics_impacted: Optional[Dict[str, float]] = None

class DecisionAuditSchema(BaseModel):
    audit_id: Optional[str] = None
    scenario_id: Optional[str] = None
    approved_alternative: Optional[str] = None
    approved_by: Optional[str] = None

class ExecutionRequest(BaseModel):
    tenant_id: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    status: str
    phase: int
    result: Dict[str, Any]
