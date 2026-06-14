"""
FastAPI request/response schemas for Global AML Intelligence Platform
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class SanctionsListSchema(BaseModel):
    list_id: Optional[str] = None
    name: Optional[str] = None
    entities_count: Optional[int] = None
    last_update: Optional[str] = None

class AmlAlertSchema(BaseModel):
    alert_id: Optional[str] = None
    account_id: Optional[str] = None
    alert_type: Optional[str] = None
    score: Optional[float] = None

class SanctionsMatchSchema(BaseModel):
    match_id: Optional[str] = None
    entity_name: Optional[str] = None
    list_name: Optional[str] = None
    confidence: Optional[float] = None

class AmlCaseSchema(BaseModel):
    case_id: Optional[str] = None
    account_id: Optional[str] = None
    stage: Optional[str] = None
    assigned_to: Optional[str] = None

class ExecutionRequest(BaseModel):
    tenant_id: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    status: str
    phase: int
    result: Dict[str, Any]
