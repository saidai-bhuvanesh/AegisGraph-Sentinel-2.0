"""
Data models for Global AML Intelligence Platform
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

@dataclass
class SanctionsList:
    list_id: str = ""
    name: str = ""
    entities_count: int = 0
    last_update: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "list_id": self.list_id,
            "name": self.name,
            "entities_count": self.entities_count,
            "last_update": self.last_update,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SanctionsList":
        return cls(
            list_id=data.get("list_id"),
            name=data.get("name"),
            entities_count=data.get("entities_count"),
            last_update=data.get("last_update"),
        )

@dataclass
class AmlAlert:
    alert_id: str = ""
    account_id: str = ""
    alert_type: str = ""
    score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "account_id": self.account_id,
            "alert_type": self.alert_type,
            "score": self.score,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AmlAlert":
        return cls(
            alert_id=data.get("alert_id"),
            account_id=data.get("account_id"),
            alert_type=data.get("alert_type"),
            score=data.get("score"),
        )

@dataclass
class SanctionsMatch:
    match_id: str = ""
    entity_name: str = ""
    list_name: str = ""
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "match_id": self.match_id,
            "entity_name": self.entity_name,
            "list_name": self.list_name,
            "confidence": self.confidence,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SanctionsMatch":
        return cls(
            match_id=data.get("match_id"),
            entity_name=data.get("entity_name"),
            list_name=data.get("list_name"),
            confidence=data.get("confidence"),
        )

@dataclass
class AmlCase:
    case_id: str = ""
    account_id: str = ""
    stage: str = ""
    assigned_to: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "case_id": self.case_id,
            "account_id": self.account_id,
            "stage": self.stage,
            "assigned_to": self.assigned_to,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AmlCase":
        return cls(
            case_id=data.get("case_id"),
            account_id=data.get("account_id"),
            stage=data.get("stage"),
            assigned_to=data.get("assigned_to"),
        )

