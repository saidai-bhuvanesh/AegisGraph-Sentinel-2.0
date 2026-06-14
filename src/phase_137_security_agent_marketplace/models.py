"""
Data models for Security Agent Marketplace
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

@dataclass
class AgentBlueprint:
    blueprint_id: str = ""
    name: str = ""
    description: str = ""
    agent_type: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "blueprint_id": self.blueprint_id,
            "name": self.name,
            "description": self.description,
            "agent_type": self.agent_type,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentBlueprint":
        return cls(
            blueprint_id=data.get("blueprint_id"),
            name=data.get("name"),
            description=data.get("description"),
            agent_type=data.get("agent_type"),
        )

@dataclass
class MarketplaceListing:
    listing_id: str = ""
    blueprint_id: str = ""
    author: str = ""
    rating: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "listing_id": self.listing_id,
            "blueprint_id": self.blueprint_id,
            "author": self.author,
            "rating": self.rating,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MarketplaceListing":
        return cls(
            listing_id=data.get("listing_id"),
            blueprint_id=data.get("blueprint_id"),
            author=data.get("author"),
            rating=data.get("rating"),
        )

@dataclass
class DeploymentInstance:
    instance_id: str = ""
    blueprint_id: str = ""
    tenant_id: str = ""
    status: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "blueprint_id": self.blueprint_id,
            "tenant_id": self.tenant_id,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeploymentInstance":
        return cls(
            instance_id=data.get("instance_id"),
            blueprint_id=data.get("blueprint_id"),
            tenant_id=data.get("tenant_id"),
            status=data.get("status"),
        )

@dataclass
class AgentSubscription:
    subscription_id: str = ""
    tenant_id: str = ""
    billing_plan: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "subscription_id": self.subscription_id,
            "tenant_id": self.tenant_id,
            "billing_plan": self.billing_plan,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentSubscription":
        return cls(
            subscription_id=data.get("subscription_id"),
            tenant_id=data.get("tenant_id"),
            billing_plan=data.get("billing_plan"),
        )

