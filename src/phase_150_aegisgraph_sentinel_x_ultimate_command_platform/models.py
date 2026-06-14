"""
Data models for AegisGraph Sentinel X Ultimate Command Platform
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

@dataclass
class PlatformStatus:
    platform_id: str = ""
    status: str = ""
    active_phases: int = 0
    uptime: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "platform_id": self.platform_id,
            "status": self.status,
            "active_phases": self.active_phases,
            "uptime": self.uptime,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PlatformStatus":
        return cls(
            platform_id=data.get("platform_id"),
            status=data.get("status"),
            active_phases=data.get("active_phases"),
            uptime=data.get("uptime"),
        )

@dataclass
class EcosystemConfig:
    config_id: str = ""
    unification_enabled: bool = False
    auto_remediation: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "config_id": self.config_id,
            "unification_enabled": self.unification_enabled,
            "auto_remediation": self.auto_remediation,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EcosystemConfig":
        return cls(
            config_id=data.get("config_id"),
            unification_enabled=data.get("unification_enabled"),
            auto_remediation=data.get("auto_remediation"),
        )

@dataclass
class UltimateReport:
    report_id: str = ""
    compiled_at: str = ""
    summary: str = ""
    risk_posture: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "compiled_at": self.compiled_at,
            "summary": self.summary,
            "risk_posture": self.risk_posture,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UltimateReport":
        return cls(
            report_id=data.get("report_id"),
            compiled_at=data.get("compiled_at"),
            summary=data.get("summary"),
            risk_posture=data.get("risk_posture"),
        )

@dataclass
class OrchestratorEvent:
    event_id: str = ""
    origin_phase: int = 0
    event_type: str = ""
    status: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "origin_phase": self.origin_phase,
            "event_type": self.event_type,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OrchestratorEvent":
        return cls(
            event_id=data.get("event_id"),
            origin_phase=data.get("origin_phase"),
            event_type=data.get("event_type"),
            status=data.get("status"),
        )

