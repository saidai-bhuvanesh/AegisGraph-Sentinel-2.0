"""
FastAPI request/response schemas for Universal Security Graph
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class UnifiedNodeSchema(BaseModel):
    node_id: Optional[str] = None
    domain: Optional[str] = None
    label: Optional[str] = None
    risk_weight: Optional[float] = None

class UnifiedEdgeSchema(BaseModel):
    edge_id: Optional[str] = None
    source_id: Optional[str] = None
    target_id: Optional[str] = None
    edge_type: Optional[str] = None

class USGGraphSchema(BaseModel):
    graph_id: Optional[str] = None
    nodes_count: Optional[int] = None
    edges_count: Optional[int] = None

class CrossDomainCorrelationSchema(BaseModel):
    correlation_id: Optional[str] = None
    source_node: Optional[str] = None
    target_node: Optional[str] = None
    confidence: Optional[float] = None

class ExecutionRequest(BaseModel):
    tenant_id: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    status: str
    phase: int
    result: Dict[str, Any]
