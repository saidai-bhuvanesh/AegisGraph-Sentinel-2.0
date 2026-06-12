"""Hyper-Scale Correlation Engine Models"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List
from uuid import uuid4

class CorrelationType(Enum):
    TEMPORAL = "TEMPORAL"
    SPATIAL = "SPATIAL"
    BEHAVIORAL = "BEHAVIORAL"

@dataclass
class CorrelationEvent:
    event_id: str
    correlation_type: CorrelationType
    score: float
    related_events: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {"event_id": self.event_id, "type": self.correlation_type.value, "score": self.score, "related_events": self.related_events}