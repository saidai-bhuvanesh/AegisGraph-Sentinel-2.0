"""
FastAPI request/response schemas for Enterprise Trust Graph
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class TrustEdgeSchema(BaseModel):
    edge_id: Optional[str] = None
    source_entity: Optional[str] = None
    target_entity: Optional[str] = None
    trust_score: Optional[float] = None
    last_evaluation: Optional[str] = None

class TrustEntitySchema(BaseModel):
    entity_id: Optional[str] = None
    entity_type: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None
    base_trust: Optional[float] = None

class DeviceFingerprintSchema(BaseModel):
    device_id: Optional[str] = None
    hardware_hash: Optional[str] = None
    is_trusted: Optional[bool] = None

class VendorRiskProfileSchema(BaseModel):
    vendor_id: Optional[str] = None
    risk_rating: Optional[str] = None
    criticality: Optional[str] = None

class ExecutionRequest(BaseModel):
    tenant_id: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    status: str
    phase: int
    result: Dict[str, Any]
