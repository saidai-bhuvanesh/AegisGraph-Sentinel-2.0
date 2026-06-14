"""
FastAPI request/response schemas for Global Intelligence Exchange Network
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class ExchangeNodeSchema(BaseModel):
    node_id: Optional[str] = None
    org_name: Optional[str] = None
    endpoint: Optional[str] = None
    trust_score: Optional[float] = None

class IntelligencePayloadSchema(BaseModel):
    payload_id: Optional[str] = None
    sender_node: Optional[str] = None
    data_type: Optional[str] = None
    content: Optional[str] = None

class SharingPolicySchema(BaseModel):
    policy_id: Optional[str] = None
    classification_level: Optional[str] = None
    allowed_recipients: Optional[List[str]] = None

class ExchangeAuditSchema(BaseModel):
    audit_id: Optional[str] = None
    timestamp: Optional[str] = None
    action: Optional[str] = None
    status: Optional[str] = None

class ExecutionRequest(BaseModel):
    tenant_id: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    status: str
    phase: int
    result: Dict[str, Any]
