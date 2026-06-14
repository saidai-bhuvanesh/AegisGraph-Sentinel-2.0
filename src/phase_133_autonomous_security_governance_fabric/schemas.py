"""
FastAPI request/response schemas for Autonomous Security Governance Fabric
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class GovernancePolicySchema(BaseModel):
    policy_id: Optional[str] = None
    title: Optional[str] = None
    rules: Optional[List[str]] = None
    is_active: Optional[bool] = None

class ComplianceControlSchema(BaseModel):
    control_id: Optional[str] = None
    name: Optional[str] = None
    framework: Optional[str] = None
    status: Optional[str] = None

class AuditRecordSchema(BaseModel):
    audit_id: Optional[str] = None
    timestamp: Optional[str] = None
    evidence_path: Optional[str] = None
    verified_by: Optional[str] = None

class GovernanceWorkflowSchema(BaseModel):
    workflow_id: Optional[str] = None
    name: Optional[str] = None
    steps: Optional[List[str]] = None
    current_step: Optional[str] = None

class ExecutionRequest(BaseModel):
    tenant_id: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    status: str
    phase: int
    result: Dict[str, Any]
