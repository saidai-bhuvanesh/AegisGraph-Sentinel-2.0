"""
Data models for Security Decision Intelligence Network
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

@dataclass
class RecommendationEngine:
    engine_id: str = ""
    name: str = ""
    version: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "engine_id": self.engine_id,
            "name": self.name,
            "version": self.version,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RecommendationEngine":
        return cls(
            engine_id=data.get("engine_id"),
            name=data.get("name"),
            version=data.get("version"),
        )

@dataclass
class DecisionScenario:
    scenario_id: str = ""
    decision_name: str = ""
    alternatives: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "decision_name": self.decision_name,
            "alternatives": self.alternatives,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DecisionScenario":
        return cls(
            scenario_id=data.get("scenario_id"),
            decision_name=data.get("decision_name"),
            alternatives=data.get("alternatives"),
        )

@dataclass
class ImpactForecast:
    forecast_id: str = ""
    scenario_id: str = ""
    metrics_impacted: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "forecast_id": self.forecast_id,
            "scenario_id": self.scenario_id,
            "metrics_impacted": self.metrics_impacted,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ImpactForecast":
        return cls(
            forecast_id=data.get("forecast_id"),
            scenario_id=data.get("scenario_id"),
            metrics_impacted=data.get("metrics_impacted"),
        )

@dataclass
class DecisionAudit:
    audit_id: str = ""
    scenario_id: str = ""
    approved_alternative: str = ""
    approved_by: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "scenario_id": self.scenario_id,
            "approved_alternative": self.approved_alternative,
            "approved_by": self.approved_by,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DecisionAudit":
        return cls(
            audit_id=data.get("audit_id"),
            scenario_id=data.get("scenario_id"),
            approved_alternative=data.get("approved_alternative"),
            approved_by=data.get("approved_by"),
        )

