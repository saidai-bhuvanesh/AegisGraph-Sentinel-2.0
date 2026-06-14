"""
FastAPI request/response schemas for Global Fraud Intelligence Observatory 2.0
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class FraudObservationSchema(BaseModel):
    observation_id: Optional[str] = None
    country: Optional[str] = None
    fraud_type: Optional[str] = None
    volume: Optional[int] = None
    timestamp: Optional[str] = None

class CampaignEvolutionSchema(BaseModel):
    campaign_id: Optional[str] = None
    name: Optional[str] = None
    first_seen: Optional[str] = None
    current_stage: Optional[str] = None
    mutation_rate: Optional[float] = None

class FraudTrendSchema(BaseModel):
    trend_id: Optional[str] = None
    category: Optional[str] = None
    growth_percentage: Optional[float] = None
    period: Optional[str] = None

class ScamEcosystemSchema(BaseModel):
    ecosystem_id: Optional[str] = None
    main_actor: Optional[str] = None
    infrastructure_ips: Optional[List[str]] = None
    payment_methods: Optional[List[str]] = None

class ExecutionRequest(BaseModel):
    tenant_id: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    status: str
    phase: int
    result: Dict[str, Any]
