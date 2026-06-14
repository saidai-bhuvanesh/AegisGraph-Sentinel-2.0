"""
Data models for Global Intelligence Mesh 2.0
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

@dataclass
class MeshNode:
    node_id: str = ""
    region: str = ""
    peers: List[str] = field(default_factory=list)
    mesh_status: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "region": self.region,
            "peers": self.peers,
            "mesh_status": self.mesh_status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MeshNode":
        return cls(
            node_id=data.get("node_id"),
            region=data.get("region"),
            peers=data.get("peers"),
            mesh_status=data.get("mesh_status"),
        )

@dataclass
class MeshTelemetry:
    telemetry_id: str = ""
    node_id: str = ""
    bandwidth_used: float = 0.0
    latency_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "telemetry_id": self.telemetry_id,
            "node_id": self.node_id,
            "bandwidth_used": self.bandwidth_used,
            "latency_ms": self.latency_ms,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MeshTelemetry":
        return cls(
            telemetry_id=data.get("telemetry_id"),
            node_id=data.get("node_id"),
            bandwidth_used=data.get("bandwidth_used"),
            latency_ms=data.get("latency_ms"),
        )

@dataclass
class SyncPolicy:
    policy_id: str = ""
    sync_interval: int = 0
    encryption_method: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "sync_interval": self.sync_interval,
            "encryption_method": self.encryption_method,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SyncPolicy":
        return cls(
            policy_id=data.get("policy_id"),
            sync_interval=data.get("sync_interval"),
            encryption_method=data.get("encryption_method"),
        )

@dataclass
class DefenseState:
    state_id: str = ""
    active_directives: int = 0
    remediation_success_rate: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "state_id": self.state_id,
            "active_directives": self.active_directives,
            "remediation_success_rate": self.remediation_success_rate,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DefenseState":
        return cls(
            state_id=data.get("state_id"),
            active_directives=data.get("active_directives"),
            remediation_success_rate=data.get("remediation_success_rate"),
        )

