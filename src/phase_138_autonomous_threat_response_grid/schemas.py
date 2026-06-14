"""
FastAPI request/response schemas for Autonomous Threat Response Grid
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class ThreatSignalSchema(BaseModel):
    signal_id: Optional[str] = None
    source: Optional[str] = None
    threat_type: Optional[str] = None
    severity: Optional[str] = None

class PlaybookActionSchema(BaseModel):
    action_id: Optional[str] = None
    playbook_name: Optional[str] = None
    target_entity: Optional[str] = None
    status: Optional[str] = None

class GridOrchestratorSchema(BaseModel):
    orchestrator_id: Optional[str] = None
    active_nodes: Optional[int] = None
    status: Optional[str] = None

class RemediationResultSchema(BaseModel):
    remediation_id: Optional[str] = None
    target_entity: Optional[str] = None
    action_taken: Optional[str] = None
    success: Optional[bool] = None

class ExecutionRequest(BaseModel):
    tenant_id: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    status: str
    phase: int
    result: Dict[str, Any]
