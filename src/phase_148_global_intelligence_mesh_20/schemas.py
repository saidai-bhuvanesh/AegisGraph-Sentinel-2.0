"""
FastAPI request/response schemas for Global Intelligence Mesh 2.0
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class MeshNodeSchema(BaseModel):
    node_id: Optional[str] = None
    region: Optional[str] = None
    peers: Optional[List[str]] = None
    mesh_status: Optional[str] = None

class MeshTelemetrySchema(BaseModel):
    telemetry_id: Optional[str] = None
    node_id: Optional[str] = None
    bandwidth_used: Optional[float] = None
    latency_ms: Optional[float] = None

class SyncPolicySchema(BaseModel):
    policy_id: Optional[str] = None
    sync_interval: Optional[int] = None
    encryption_method: Optional[str] = None

class DefenseStateSchema(BaseModel):
    state_id: Optional[str] = None
    active_directives: Optional[int] = None
    remediation_success_rate: Optional[float] = None

class ExecutionRequest(BaseModel):
    tenant_id: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    status: str
    phase: int
    result: Dict[str, Any]
