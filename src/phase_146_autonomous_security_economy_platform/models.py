"""
Data models for Autonomous Security Economy Platform
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

@dataclass
class EconomicMetric:
    metric_id: str = ""
    name: str = ""
    unit: str = ""
    value: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_id": self.metric_id,
            "name": self.name,
            "unit": self.unit,
            "value": self.value,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EconomicMetric":
        return cls(
            metric_id=data.get("metric_id"),
            name=data.get("name"),
            unit=data.get("unit"),
            value=data.get("value"),
        )

@dataclass
class CostAnalysis:
    analysis_id: str = ""
    incident_type: str = ""
    cost_direct: float = 0.0
    cost_indirect: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "analysis_id": self.analysis_id,
            "incident_type": self.incident_type,
            "cost_direct": self.cost_direct,
            "cost_indirect": self.cost_indirect,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CostAnalysis":
        return cls(
            analysis_id=data.get("analysis_id"),
            incident_type=data.get("incident_type"),
            cost_direct=data.get("cost_direct"),
            cost_indirect=data.get("cost_indirect"),
        )

@dataclass
class RoiForecast:
    forecast_id: str = ""
    investment_name: str = ""
    projected_roi: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "forecast_id": self.forecast_id,
            "investment_name": self.investment_name,
            "projected_roi": self.projected_roi,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RoiForecast":
        return cls(
            forecast_id=data.get("forecast_id"),
            investment_name=data.get("investment_name"),
            projected_roi=data.get("projected_roi"),
        )

@dataclass
class LossPreventionAudit:
    audit_id: str = ""
    period: str = ""
    savings_verified: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "period": self.period,
            "savings_verified": self.savings_verified,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LossPreventionAudit":
        return cls(
            audit_id=data.get("audit_id"),
            period=data.get("period"),
            savings_verified=data.get("savings_verified"),
        )

