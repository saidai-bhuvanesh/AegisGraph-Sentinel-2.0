"""
FastAPI request/response schemas for Security Agent Marketplace
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class AgentBlueprintSchema(BaseModel):
    blueprint_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    agent_type: Optional[str] = None

class MarketplaceListingSchema(BaseModel):
    listing_id: Optional[str] = None
    blueprint_id: Optional[str] = None
    author: Optional[str] = None
    rating: Optional[float] = None

class DeploymentInstanceSchema(BaseModel):
    instance_id: Optional[str] = None
    blueprint_id: Optional[str] = None
    tenant_id: Optional[str] = None
    status: Optional[str] = None

class AgentSubscriptionSchema(BaseModel):
    subscription_id: Optional[str] = None
    tenant_id: Optional[str] = None
    billing_plan: Optional[str] = None

class ExecutionRequest(BaseModel):
    tenant_id: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    status: str
    phase: int
    result: Dict[str, Any]
