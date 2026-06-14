"""
Data models for Enterprise Attack Path Intelligence Platform
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

@dataclass
class AttackPath:
    path_id: str = ""
    source_node: str = ""
    target_node: str = ""
    complexity: float = 0.0
    steps: List[str] = field(default_factory=list)
    is_active: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path_id": self.path_id,
            "source_node": self.source_node,
            "target_node": self.target_node,
            "complexity": self.complexity,
            "steps": self.steps,
            "is_active": self.is_active,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AttackPath":
        return cls(
            path_id=data.get("path_id"),
            source_node=data.get("source_node"),
            target_node=data.get("target_node"),
            complexity=data.get("complexity"),
            steps=data.get("steps"),
            is_active=data.get("is_active"),
        )

@dataclass
class LateralMovement:
    movement_id: str = ""
    source_host: str = ""
    dest_host: str = ""
    credential_used: str = ""
    probability: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "movement_id": self.movement_id,
            "source_host": self.source_host,
            "dest_host": self.dest_host,
            "credential_used": self.credential_used,
            "probability": self.probability,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LateralMovement":
        return cls(
            movement_id=data.get("movement_id"),
            source_host=data.get("source_host"),
            dest_host=data.get("dest_host"),
            credential_used=data.get("credential_used"),
            probability=data.get("probability"),
        )

@dataclass
class AssetExposure:
    exposure_id: str = ""
    asset_id: str = ""
    exposure_level: str = ""
    vulnerabilities: List[str] = field(default_factory=list)
    score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "exposure_id": self.exposure_id,
            "asset_id": self.asset_id,
            "exposure_level": self.exposure_level,
            "vulnerabilities": self.vulnerabilities,
            "score": self.score,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AssetExposure":
        return cls(
            exposure_id=data.get("exposure_id"),
            asset_id=data.get("asset_id"),
            exposure_level=data.get("exposure_level"),
            vulnerabilities=data.get("vulnerabilities"),
            score=data.get("score"),
        )

@dataclass
class BreachScenario:
    scenario_id: str = ""
    name: str = ""
    entry_point: str = ""
    target_asset: str = ""
    estimated_impact: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "name": self.name,
            "entry_point": self.entry_point,
            "target_asset": self.target_asset,
            "estimated_impact": self.estimated_impact,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BreachScenario":
        return cls(
            scenario_id=data.get("scenario_id"),
            name=data.get("name"),
            entry_point=data.get("entry_point"),
            target_asset=data.get("target_asset"),
            estimated_impact=data.get("estimated_impact"),
        )

