"""
Data models for Global Security Command Network
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

@dataclass
class CommandNetworkNode:
    node_id: str = ""
    region: str = ""
    org_sector: str = ""
    status: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "region": self.region,
            "org_sector": self.org_sector,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CommandNetworkNode":
        return cls(
            node_id=data.get("node_id"),
            region=data.get("region"),
            org_sector=data.get("org_sector"),
            status=data.get("status"),
        )

@dataclass
class CoordinatedCampaign:
    campaign_id: str = ""
    description: str = ""
    target_nodes: List[str] = field(default_factory=list)
    severity: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "campaign_id": self.campaign_id,
            "description": self.description,
            "target_nodes": self.target_nodes,
            "severity": self.severity,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CoordinatedCampaign":
        return cls(
            campaign_id=data.get("campaign_id"),
            description=data.get("description"),
            target_nodes=data.get("target_nodes"),
            severity=data.get("severity"),
        )

@dataclass
class TacticalDirective:
    directive_id: str = ""
    campaign_id: str = ""
    instructions: str = ""
    status: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "directive_id": self.directive_id,
            "campaign_id": self.campaign_id,
            "instructions": self.instructions,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TacticalDirective":
        return cls(
            directive_id=data.get("directive_id"),
            campaign_id=data.get("campaign_id"),
            instructions=data.get("instructions"),
            status=data.get("status"),
        )

@dataclass
class CommandTelemetry:
    telemetry_id: str = ""
    node_id: str = ""
    kpis: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "telemetry_id": self.telemetry_id,
            "node_id": self.node_id,
            "kpis": self.kpis,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CommandTelemetry":
        return cls(
            telemetry_id=data.get("telemetry_id"),
            node_id=data.get("node_id"),
            kpis=data.get("kpis"),
        )

