"""
Data models for Enterprise Intelligence Fabric 2.0
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

@dataclass
class IntelligenceHub:
    hub_id: str = ""
    name: str = ""
    connected_domains: List[str] = field(default_factory=list)
    uptime: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hub_id": self.hub_id,
            "name": self.name,
            "connected_domains": self.connected_domains,
            "uptime": self.uptime,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IntelligenceHub":
        return cls(
            hub_id=data.get("hub_id"),
            name=data.get("name"),
            connected_domains=data.get("connected_domains"),
            uptime=data.get("uptime"),
        )

@dataclass
class DomainBridge:
    bridge_id: str = ""
    source_domain: str = ""
    dest_domain: str = ""
    sync_rate: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bridge_id": self.bridge_id,
            "source_domain": self.source_domain,
            "dest_domain": self.dest_domain,
            "sync_rate": self.sync_rate,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DomainBridge":
        return cls(
            bridge_id=data.get("bridge_id"),
            source_domain=data.get("source_domain"),
            dest_domain=data.get("dest_domain"),
            sync_rate=data.get("sync_rate"),
        )

@dataclass
class FabricSignal:
    signal_id: str = ""
    domain: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "signal_id": self.signal_id,
            "domain": self.domain,
            "payload": self.payload,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FabricSignal":
        return cls(
            signal_id=data.get("signal_id"),
            domain=data.get("domain"),
            payload=data.get("payload"),
        )

@dataclass
class UnifiedContext:
    context_id: str = ""
    entity_id: str = ""
    combined_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "context_id": self.context_id,
            "entity_id": self.entity_id,
            "combined_score": self.combined_score,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UnifiedContext":
        return cls(
            context_id=data.get("context_id"),
            entity_id=data.get("entity_id"),
            combined_score=data.get("combined_score"),
        )

