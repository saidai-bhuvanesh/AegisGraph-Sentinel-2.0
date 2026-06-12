"""Trust & Reputation Network Models"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict
from uuid import uuid4

class TrustLevel(Enum):
    VERY_LOW = "VERY_LOW"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"

@dataclass
class TrustEntity:
    entity_id: str
    name: str
    trust_score: float = 0.5
    trust_level: TrustLevel = TrustLevel.MEDIUM
    
    def to_dict(self) -> Dict[str, Any]:
        return {"entity_id": self.entity_id, "name": self.name,
                "trust_score": self.trust_score, "trust_level": self.trust_level.value}

@dataclass
class ReputationRecord:
    record_id: str
    entity_id: str
    score: float
    factors: list = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {"record_id": self.record_id, "entity_id": self.entity_id,
                "score": self.score, "factors": self.factors}