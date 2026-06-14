"""
FastAPI request/response schemas for Global Security Command Network
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class CommandNetworkNodeSchema(BaseModel):
    node_id: Optional[str] = None
    region: Optional[str] = None
    org_sector: Optional[str] = None
    status: Optional[str] = None

class CoordinatedCampaignSchema(BaseModel):
    campaign_id: Optional[str] = None
    description: Optional[str] = None
    target_nodes: Optional[List[str]] = None
    severity: Optional[str] = None

class TacticalDirectiveSchema(BaseModel):
    directive_id: Optional[str] = None
    campaign_id: Optional[str] = None
    instructions: Optional[str] = None
    status: Optional[str] = None

class CommandTelemetrySchema(BaseModel):
    telemetry_id: Optional[str] = None
    node_id: Optional[str] = None
    kpis: Optional[Dict[str, float]] = None

class ExecutionRequest(BaseModel):
    tenant_id: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    status: str
    phase: int
    result: Dict[str, Any]
