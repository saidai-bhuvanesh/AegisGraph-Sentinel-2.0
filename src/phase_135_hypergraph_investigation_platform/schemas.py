"""
FastAPI request/response schemas for Hypergraph Investigation Platform
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class HyperEdgeSchema(BaseModel):
    edge_id: Optional[str] = None
    entities: Optional[List[str]] = None
    weight: Optional[float] = None
    relationship_type: Optional[str] = None

class HyperNodeSchema(BaseModel):
    node_id: Optional[str] = None
    label: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None

class InvestigationClusterSchema(BaseModel):
    cluster_id: Optional[str] = None
    edges: Optional[List[str]] = None
    severity: Optional[str] = None

class PatternMatchSchema(BaseModel):
    match_id: Optional[str] = None
    pattern_name: Optional[str] = None
    matching_nodes: Optional[List[str]] = None

class ExecutionRequest(BaseModel):
    tenant_id: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    status: str
    phase: int
    result: Dict[str, Any]
