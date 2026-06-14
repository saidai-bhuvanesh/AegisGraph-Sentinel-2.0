"""
FastAPI request/response schemas for Autonomous Security Economy Platform
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class EconomicMetricSchema(BaseModel):
    metric_id: Optional[str] = None
    name: Optional[str] = None
    unit: Optional[str] = None
    value: Optional[float] = None

class CostAnalysisSchema(BaseModel):
    analysis_id: Optional[str] = None
    incident_type: Optional[str] = None
    cost_direct: Optional[float] = None
    cost_indirect: Optional[float] = None

class RoiForecastSchema(BaseModel):
    forecast_id: Optional[str] = None
    investment_name: Optional[str] = None
    projected_roi: Optional[float] = None

class LossPreventionAuditSchema(BaseModel):
    audit_id: Optional[str] = None
    period: Optional[str] = None
    savings_verified: Optional[float] = None

class ExecutionRequest(BaseModel):
    tenant_id: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    status: str
    phase: int
    result: Dict[str, Any]
