"""
Data models for Autonomous Security Governance Fabric
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

@dataclass
class GovernancePolicy:
    policy_id: str = ""
    title: str = ""
    rules: List[str] = field(default_factory=list)
    is_active: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "title": self.title,
            "rules": self.rules,
            "is_active": self.is_active,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GovernancePolicy":
        return cls(
            policy_id=data.get("policy_id"),
            title=data.get("title"),
            rules=data.get("rules"),
            is_active=data.get("is_active"),
        )

@dataclass
class ComplianceControl:
    control_id: str = ""
    name: str = ""
    framework: str = ""
    status: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "control_id": self.control_id,
            "name": self.name,
            "framework": self.framework,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ComplianceControl":
        return cls(
            control_id=data.get("control_id"),
            name=data.get("name"),
            framework=data.get("framework"),
            status=data.get("status"),
        )

@dataclass
class AuditRecord:
    audit_id: str = ""
    timestamp: str = ""
    evidence_path: str = ""
    verified_by: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "timestamp": self.timestamp,
            "evidence_path": self.evidence_path,
            "verified_by": self.verified_by,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AuditRecord":
        return cls(
            audit_id=data.get("audit_id"),
            timestamp=data.get("timestamp"),
            evidence_path=data.get("evidence_path"),
            verified_by=data.get("verified_by"),
        )

@dataclass
class GovernanceWorkflow:
    workflow_id: str = ""
    name: str = ""
    steps: List[str] = field(default_factory=list)
    current_step: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "name": self.name,
            "steps": self.steps,
            "current_step": self.current_step,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GovernanceWorkflow":
        return cls(
            workflow_id=data.get("workflow_id"),
            name=data.get("name"),
            steps=data.get("steps"),
            current_step=data.get("current_step"),
        )

