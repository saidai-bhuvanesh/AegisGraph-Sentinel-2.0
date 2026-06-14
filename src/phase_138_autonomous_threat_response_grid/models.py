"""
Data models for Autonomous Threat Response Grid
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

@dataclass
class ThreatSignal:
    signal_id: str = ""
    source: str = ""
    threat_type: str = ""
    severity: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "signal_id": self.signal_id,
            "source": self.source,
            "threat_type": self.threat_type,
            "severity": self.severity,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ThreatSignal":
        return cls(
            signal_id=data.get("signal_id"),
            source=data.get("source"),
            threat_type=data.get("threat_type"),
            severity=data.get("severity"),
        )

@dataclass
class PlaybookAction:
    action_id: str = ""
    playbook_name: str = ""
    target_entity: str = ""
    status: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_id": self.action_id,
            "playbook_name": self.playbook_name,
            "target_entity": self.target_entity,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PlaybookAction":
        return cls(
            action_id=data.get("action_id"),
            playbook_name=data.get("playbook_name"),
            target_entity=data.get("target_entity"),
            status=data.get("status"),
        )

@dataclass
class GridOrchestrator:
    orchestrator_id: str = ""
    active_nodes: int = 0
    status: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "orchestrator_id": self.orchestrator_id,
            "active_nodes": self.active_nodes,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GridOrchestrator":
        return cls(
            orchestrator_id=data.get("orchestrator_id"),
            active_nodes=data.get("active_nodes"),
            status=data.get("status"),
        )

@dataclass
class RemediationResult:
    remediation_id: str = ""
    target_entity: str = ""
    action_taken: str = ""
    success: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "remediation_id": self.remediation_id,
            "target_entity": self.target_entity,
            "action_taken": self.action_taken,
            "success": self.success,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RemediationResult":
        return cls(
            remediation_id=data.get("remediation_id"),
            target_entity=data.get("target_entity"),
            action_taken=data.get("action_taken"),
            success=data.get("success"),
        )

