"""
FastAPI request/response schemas for Enterprise Attack Path Intelligence Platform
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class AttackPathSchema(BaseModel):
    path_id: Optional[str] = None
    source_node: Optional[str] = None
    target_node: Optional[str] = None
    complexity: Optional[float] = None
    steps: Optional[List[str]] = None
    is_active: Optional[bool] = None

class LateralMovementSchema(BaseModel):
    movement_id: Optional[str] = None
    source_host: Optional[str] = None
    dest_host: Optional[str] = None
    credential_used: Optional[str] = None
    probability: Optional[float] = None

class AssetExposureSchema(BaseModel):
    exposure_id: Optional[str] = None
    asset_id: Optional[str] = None
    exposure_level: Optional[str] = None
    vulnerabilities: Optional[List[str]] = None
    score: Optional[float] = None

class BreachScenarioSchema(BaseModel):
    scenario_id: Optional[str] = None
    name: Optional[str] = None
    entry_point: Optional[str] = None
    target_asset: Optional[str] = None
    estimated_impact: Optional[float] = None

class ExecutionRequest(BaseModel):
    tenant_id: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    status: str
    phase: int
    result: Dict[str, Any]
