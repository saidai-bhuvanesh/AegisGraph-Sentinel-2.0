"""
Data models for Global Fraud Intelligence Observatory 2.0
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

@dataclass
class FraudObservation:
    observation_id: str = ""
    country: str = ""
    fraud_type: str = ""
    volume: int = 0
    timestamp: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "observation_id": self.observation_id,
            "country": self.country,
            "fraud_type": self.fraud_type,
            "volume": self.volume,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FraudObservation":
        return cls(
            observation_id=data.get("observation_id"),
            country=data.get("country"),
            fraud_type=data.get("fraud_type"),
            volume=data.get("volume"),
            timestamp=data.get("timestamp"),
        )

@dataclass
class CampaignEvolution:
    campaign_id: str = ""
    name: str = ""
    first_seen: str = ""
    current_stage: str = ""
    mutation_rate: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "campaign_id": self.campaign_id,
            "name": self.name,
            "first_seen": self.first_seen,
            "current_stage": self.current_stage,
            "mutation_rate": self.mutation_rate,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CampaignEvolution":
        return cls(
            campaign_id=data.get("campaign_id"),
            name=data.get("name"),
            first_seen=data.get("first_seen"),
            current_stage=data.get("current_stage"),
            mutation_rate=data.get("mutation_rate"),
        )

@dataclass
class FraudTrend:
    trend_id: str = ""
    category: str = ""
    growth_percentage: float = 0.0
    period: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trend_id": self.trend_id,
            "category": self.category,
            "growth_percentage": self.growth_percentage,
            "period": self.period,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FraudTrend":
        return cls(
            trend_id=data.get("trend_id"),
            category=data.get("category"),
            growth_percentage=data.get("growth_percentage"),
            period=data.get("period"),
        )

@dataclass
class ScamEcosystem:
    ecosystem_id: str = ""
    main_actor: str = ""
    infrastructure_ips: List[str] = field(default_factory=list)
    payment_methods: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ecosystem_id": self.ecosystem_id,
            "main_actor": self.main_actor,
            "infrastructure_ips": self.infrastructure_ips,
            "payment_methods": self.payment_methods,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ScamEcosystem":
        return cls(
            ecosystem_id=data.get("ecosystem_id"),
            main_actor=data.get("main_actor"),
            infrastructure_ips=data.get("infrastructure_ips"),
            payment_methods=data.get("payment_methods"),
        )

