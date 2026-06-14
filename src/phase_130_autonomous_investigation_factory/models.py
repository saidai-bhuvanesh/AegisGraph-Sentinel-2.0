"""
Data models for Autonomous Investigation Factory
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

@dataclass
class Investigation:
    investigation_id: str = ""
    target_entity: str = ""
    status: str = ""
    created_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "investigation_id": self.investigation_id,
            "target_entity": self.target_entity,
            "status": self.status,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Investigation":
        return cls(
            investigation_id=data.get("investigation_id"),
            target_entity=data.get("target_entity"),
            status=data.get("status"),
            created_at=data.get("created_at"),
        )

@dataclass
class Evidence:
    evidence_id: str = ""
    source: str = ""
    data_payload: Dict[str, Any] = field(default_factory=dict)
    integrity_hash: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "source": self.source,
            "data_payload": self.data_payload,
            "integrity_hash": self.integrity_hash,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Evidence":
        return cls(
            evidence_id=data.get("evidence_id"),
            source=data.get("source"),
            data_payload=data.get("data_payload"),
            integrity_hash=data.get("integrity_hash"),
        )

@dataclass
class EntityCorrelation:
    correlation_id: str = ""
    source_entity: str = ""
    target_entity: str = ""
    relationship_type: str = ""
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "correlation_id": self.correlation_id,
            "source_entity": self.source_entity,
            "target_entity": self.target_entity,
            "relationship_type": self.relationship_type,
            "confidence": self.confidence,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EntityCorrelation":
        return cls(
            correlation_id=data.get("correlation_id"),
            source_entity=data.get("source_entity"),
            target_entity=data.get("target_entity"),
            relationship_type=data.get("relationship_type"),
            confidence=data.get("confidence"),
        )

@dataclass
class CaseReport:
    report_id: str = ""
    title: str = ""
    narrative: str = ""
    generated_by: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "title": self.title,
            "narrative": self.narrative,
            "generated_by": self.generated_by,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CaseReport":
        return cls(
            report_id=data.get("report_id"),
            title=data.get("title"),
            narrative=data.get("narrative"),
            generated_by=data.get("generated_by"),
        )

