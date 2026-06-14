"""
FastAPI request/response schemas for Security Knowledge Operating System
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class KnowledgeArticleSchema(BaseModel):
    article_id: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None

class InvestigationKnowledgeSchema(BaseModel):
    knowledge_id: Optional[str] = None
    case_id: Optional[str] = None
    findings: Optional[str] = None
    entities: Optional[List[str]] = None

class ThreatIntelEntrySchema(BaseModel):
    intel_id: Optional[str] = None
    indicator: Optional[str] = None
    threat_type: Optional[str] = None
    confidence: Optional[float] = None

class FraudPatternSchema(BaseModel):
    pattern_id: Optional[str] = None
    name: Optional[str] = None
    rules: Optional[List[str]] = None
    severity: Optional[str] = None

class ExecutionRequest(BaseModel):
    tenant_id: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    status: str
    phase: int
    result: Dict[str, Any]
