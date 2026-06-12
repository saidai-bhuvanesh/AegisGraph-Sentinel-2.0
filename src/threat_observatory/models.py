"""Threat Observatory Models - Global Fraud & Threat Visibility"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List
from uuid import uuid4

class ThreatType(Enum):
    MALWARE = "MALWARE"
    PHISHING = "PHISHING"
    RANSOMWARE = "RANSOMWARE"
    FRAUD = "FRAUD"
    DDoS = "DDoS"

@dataclass
class ThreatEvent:
    event_id: str
    threat_type: ThreatType
    severity: float
    location: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> Dict[str, Any]:
        return {"event_id": self.event_id, "threat_type": self.threat_type.value,
                "severity": self.severity, "location": self.location,
                "timestamp": self.timestamp.isoformat()}

@dataclass
class GlobalTrend:
    trend_id: str
    name: str
    growth_rate: float
    affected_regions: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {"trend_id": self.trend_id, "name": self.name,
                "growth_rate": self.growth_rate, "affected_regions": self.affected_regions}