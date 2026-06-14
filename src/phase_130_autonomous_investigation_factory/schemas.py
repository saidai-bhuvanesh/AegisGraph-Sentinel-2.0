"""
FastAPI request/response schemas for Autonomous Investigation Factory
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class InvestigationSchema(BaseModel):
    investigation_id: Optional[str] = None
    target_entity: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None

class EvidenceSchema(BaseModel):
    evidence_id: Optional[str] = None
    source: Optional[str] = None
    data_payload: Optional[Dict[str, Any]] = None
    integrity_hash: Optional[str] = None

class EntityCorrelationSchema(BaseModel):
    correlation_id: Optional[str] = None
    source_entity: Optional[str] = None
    target_entity: Optional[str] = None
    relationship_type: Optional[str] = None
    confidence: Optional[float] = None

class CaseReportSchema(BaseModel):
    report_id: Optional[str] = None
    title: Optional[str] = None
    narrative: Optional[str] = None
    generated_by: Optional[str] = None

class ExecutionRequest(BaseModel):
    tenant_id: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    status: str
    phase: int
    result: Dict[str, Any]
