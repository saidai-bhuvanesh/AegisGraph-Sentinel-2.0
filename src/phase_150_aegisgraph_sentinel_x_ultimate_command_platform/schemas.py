"""
FastAPI request/response schemas for AegisGraph Sentinel X Ultimate Command Platform
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class PlatformStatusSchema(BaseModel):
    platform_id: Optional[str] = None
    status: Optional[str] = None
    active_phases: Optional[int] = None
    uptime: Optional[float] = None

class EcosystemConfigSchema(BaseModel):
    config_id: Optional[str] = None
    unification_enabled: Optional[bool] = None
    auto_remediation: Optional[bool] = None

class UltimateReportSchema(BaseModel):
    report_id: Optional[str] = None
    compiled_at: Optional[str] = None
    summary: Optional[str] = None
    risk_posture: Optional[float] = None

class OrchestratorEventSchema(BaseModel):
    event_id: Optional[str] = None
    origin_phase: Optional[int] = None
    event_type: Optional[str] = None
    status: Optional[str] = None

class ExecutionRequest(BaseModel):
    tenant_id: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    status: str
    phase: int
    result: Dict[str, Any]
