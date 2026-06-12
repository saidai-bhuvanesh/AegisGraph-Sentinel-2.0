"""Threat Observatory Engine"""
from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import uuid4

from .models import ThreatEvent, ThreatType, GlobalTrend

class ThreatObservatory:
    def __init__(self):
        self.events: Dict[str, ThreatEvent] = {}
        self.trends: Dict[str, GlobalTrend] = {}
    
    def add_event(self, threat_type: ThreatType, severity: float, location: str) -> str:
        event_id = str(uuid4())
        event = ThreatEvent(event_id=event_id, threat_type=threat_type, severity=severity, location=location)
        self.events[event_id] = event
        return event_id
    
    def get_event(self, event_id: str) -> ThreatEvent:
        return self.events.get(event_id)
    
    def add_trend(self, name: str, growth_rate: float, regions: List[str]) -> str:
        trend_id = str(uuid4())
        trend = GlobalTrend(trend_id=trend_id, name=name, growth_rate=growth_rate, affected_regions=regions)
        self.trends[trend_id] = trend
        return trend_id
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_events": len(self.events),
            "total_trends": len(self.trends),
            "by_type": {t.value: len([e for e in self.events.values() if e.threat_type == t]) for t in ThreatType}
        }

def get_observatory() -> ThreatObservatory:
    global _observatory
    if _observatory is None:
        _observatory = ThreatObservatory()
    return _observatory

_observatory = None