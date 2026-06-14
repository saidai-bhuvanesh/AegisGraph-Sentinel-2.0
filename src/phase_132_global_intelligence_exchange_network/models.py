"""
Data models for Global Intelligence Exchange Network
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

@dataclass
class ExchangeNode:
    node_id: str = ""
    org_name: str = ""
    endpoint: str = ""
    trust_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "org_name": self.org_name,
            "endpoint": self.endpoint,
            "trust_score": self.trust_score,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExchangeNode":
        return cls(
            node_id=data.get("node_id"),
            org_name=data.get("org_name"),
            endpoint=data.get("endpoint"),
            trust_score=data.get("trust_score"),
        )

@dataclass
class IntelligencePayload:
    payload_id: str = ""
    sender_node: str = ""
    data_type: str = ""
    content: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "payload_id": self.payload_id,
            "sender_node": self.sender_node,
            "data_type": self.data_type,
            "content": self.content,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IntelligencePayload":
        return cls(
            payload_id=data.get("payload_id"),
            sender_node=data.get("sender_node"),
            data_type=data.get("data_type"),
            content=data.get("content"),
        )

@dataclass
class SharingPolicy:
    policy_id: str = ""
    classification_level: str = ""
    allowed_recipients: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "classification_level": self.classification_level,
            "allowed_recipients": self.allowed_recipients,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SharingPolicy":
        return cls(
            policy_id=data.get("policy_id"),
            classification_level=data.get("classification_level"),
            allowed_recipients=data.get("allowed_recipients"),
        )

@dataclass
class ExchangeAudit:
    audit_id: str = ""
    timestamp: str = ""
    action: str = ""
    status: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "timestamp": self.timestamp,
            "action": self.action,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExchangeAudit":
        return cls(
            audit_id=data.get("audit_id"),
            timestamp=data.get("timestamp"),
            action=data.get("action"),
            status=data.get("status"),
        )

