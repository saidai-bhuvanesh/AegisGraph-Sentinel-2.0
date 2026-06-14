"""
FastAPI request/response schemas for Enterprise Intelligence Fabric 2.0
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class IntelligenceHubSchema(BaseModel):
    hub_id: Optional[str] = None
    name: Optional[str] = None
    connected_domains: Optional[List[str]] = None
    uptime: Optional[float] = None

class DomainBridgeSchema(BaseModel):
    bridge_id: Optional[str] = None
    source_domain: Optional[str] = None
    dest_domain: Optional[str] = None
    sync_rate: Optional[float] = None

class FabricSignalSchema(BaseModel):
    signal_id: Optional[str] = None
    domain: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None

class UnifiedContextSchema(BaseModel):
    context_id: Optional[str] = None
    entity_id: Optional[str] = None
    combined_score: Optional[float] = None

class ExecutionRequest(BaseModel):
    tenant_id: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    status: str
    phase: int
    result: Dict[str, Any]
