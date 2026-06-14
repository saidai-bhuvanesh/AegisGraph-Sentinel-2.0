"""
Data models for Enterprise Trust Graph
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

@dataclass
class TrustEdge:
    edge_id: str = ""
    source_entity: str = ""
    target_entity: str = ""
    trust_score: float = 0.0
    last_evaluation: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "edge_id": self.edge_id,
            "source_entity": self.source_entity,
            "target_entity": self.target_entity,
            "trust_score": self.trust_score,
            "last_evaluation": self.last_evaluation,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TrustEdge":
        return cls(
            edge_id=data.get("edge_id"),
            source_entity=data.get("source_entity"),
            target_entity=data.get("target_entity"),
            trust_score=data.get("trust_score"),
            last_evaluation=data.get("last_evaluation"),
        )

@dataclass
class TrustEntity:
    entity_id: str = ""
    entity_type: str = ""
    attributes: Dict[str, Any] = field(default_factory=dict)
    base_trust: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "attributes": self.attributes,
            "base_trust": self.base_trust,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TrustEntity":
        return cls(
            entity_id=data.get("entity_id"),
            entity_type=data.get("entity_type"),
            attributes=data.get("attributes"),
            base_trust=data.get("base_trust"),
        )

@dataclass
class DeviceFingerprint:
    device_id: str = ""
    hardware_hash: str = ""
    is_trusted: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "device_id": self.device_id,
            "hardware_hash": self.hardware_hash,
            "is_trusted": self.is_trusted,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeviceFingerprint":
        return cls(
            device_id=data.get("device_id"),
            hardware_hash=data.get("hardware_hash"),
            is_trusted=data.get("is_trusted"),
        )

@dataclass
class VendorRiskProfile:
    vendor_id: str = ""
    risk_rating: str = ""
    criticality: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "vendor_id": self.vendor_id,
            "risk_rating": self.risk_rating,
            "criticality": self.criticality,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VendorRiskProfile":
        return cls(
            vendor_id=data.get("vendor_id"),
            risk_rating=data.get("risk_rating"),
            criticality=data.get("criticality"),
        )

