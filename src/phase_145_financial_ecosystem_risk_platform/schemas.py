"""
FastAPI request/response schemas for Financial Ecosystem Risk Platform
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class EcosystemNodeSchema(BaseModel):
    node_id: Optional[str] = None
    institution_name: Optional[str] = None
    type: Optional[str] = None
    risk_score: Optional[float] = None

class InterbankTxSchema(BaseModel):
    tx_id: Optional[str] = None
    from_node: Optional[str] = None
    to_node: Optional[str] = None
    amount: Optional[float] = None

class SystemicAnomalySchema(BaseModel):
    anomaly_id: Optional[str] = None
    nodes_involved: Optional[List[str]] = None
    risk_type: Optional[str] = None
    severity: Optional[str] = None

class RiskExposureReportSchema(BaseModel):
    report_id: Optional[str] = None
    forecast_period: Optional[str] = None
    potential_loss: Optional[float] = None

class ExecutionRequest(BaseModel):
    tenant_id: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    status: str
    phase: int
    result: Dict[str, Any]
