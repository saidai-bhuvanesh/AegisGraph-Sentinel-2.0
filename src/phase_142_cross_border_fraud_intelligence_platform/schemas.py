"""
FastAPI request/response schemas for Cross-Border Fraud Intelligence Platform
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class CrossBorderTxSchema(BaseModel):
    tx_id: Optional[str] = None
    source_country: Optional[str] = None
    dest_country: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None

class TransnationalMuleRingSchema(BaseModel):
    ring_id: Optional[str] = None
    main_nodes: Optional[List[str]] = None
    countries_involved: Optional[List[str]] = None
    score: Optional[float] = None

class JurisdictionalReportSchema(BaseModel):
    report_id: Optional[str] = None
    jurisdiction: Optional[str] = None
    cases_flagged: Optional[int] = None

class IntelExchangeLogSchema(BaseModel):
    log_id: Optional[str] = None
    partner_jurisdiction: Optional[str] = None
    shared_records: Optional[int] = None

class ExecutionRequest(BaseModel):
    tenant_id: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    status: str
    phase: int
    result: Dict[str, Any]
