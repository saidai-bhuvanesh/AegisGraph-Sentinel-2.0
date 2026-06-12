"""
Cross-Industry Intelligence Federation Models
Secure intelligence sharing between industries.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4


class IndustryType(Enum):
    """Industry types."""
    FINANCIAL = "FINANCIAL"
    HEALTHCARE = "HEALTHCARE"
    RETAIL = "RETAIL"
    ENERGY = "ENERGY"
    GOVERNMENT = "GOVERNMENT"
    TECHNOLOGY = "TECHNOLOGY"


class FederationRole(Enum):
    """Federation roles."""
    CONTRIBUTOR = "CONTRIBUTOR"
    CONSUMER = "CONSUMER"
    BOTH = "BOTH"


@dataclass
class FederationMember:
    """Federation member."""
    member_id: str
    organization: str
    industry: IndustryType
    role: FederationRole
    trust_score: float = 1.0
    joined_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "member_id": self.member_id,
            "organization": self.organization,
            "industry": self.industry.value,
            "role": self.role.value,
            "trust_score": self.trust_score,
            "joined_at": self.joined_at.isoformat(),
        }


@dataclass
class SharedIndicator:
    """Shared intelligence indicator."""
    indicator_id: str
    type: str
    value: str
    source_industry: IndustryType
    confidence: float
    shared_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "indicator_id": self.indicator_id,
            "type": self.type,
            "value": self.value,
            "source_industry": self.source_industry.value,
            "confidence": self.confidence,
            "shared_at": self.shared_at.isoformat(),
        }