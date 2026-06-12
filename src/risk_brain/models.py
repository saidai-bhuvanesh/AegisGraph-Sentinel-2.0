"""
Enterprise Risk Brain Models
AI-powered enterprise risk reasoning system.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4


class RiskCategory(Enum):
    """Risk categories."""
    CYBER = "CYBER"
    FRAUD = "FRAUD"
    COMPLIANCE = "COMPLIANCE"
    OPERATIONAL = "OPERATIONAL"
    REPUTATIONAL = "REPUTATIONAL"
    FINANCIAL = "FINANCIAL"


class RiskLevel(Enum):
    """Risk levels."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    MINIMAL = "MINIMAL"


class ForecastHorizon(Enum):
    """Forecast time horizons."""
    SHORT_TERM = "SHORT_TERM"
    MEDIUM_TERM = "MEDIUM_TERM"
    LONG_TERM = "LONG_TERM"


@dataclass
class RiskEntity:
    """A risk entity."""
    entity_id: str
    name: str
    risk_category: RiskCategory
    current_risk_score: float = 0.0
    risk_level: RiskLevel = RiskLevel.LOW
    factors: List[Dict[str, Any]] = field(default_factory=list)
    indicators: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "risk_category": self.risk_category.value,
            "current_risk_score": self.current_risk_score,
            "risk_level": self.risk_level.value,
            "factors": self.factors,
            "indicators": self.indicators,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class RiskForecast:
    """Risk forecast."""
    forecast_id: str
    entity_id: str
    horizon: ForecastHorizon
    predicted_score: float
    confidence: float
    factors: List[str]
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "forecast_id": self.forecast_id,
            "entity_id": self.entity_id,
            "horizon": self.horizon.value,
            "predicted_score": self.predicted_score,
            "confidence": self.confidence,
            "factors": self.factors,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class RiskRecommendation:
    """Risk recommendation."""
    recommendation_id: str
    entity_id: str
    recommendation: str
    priority: int = 0
    impact: float = 0.0
    implementation_effort: str = "MEDIUM"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "recommendation_id": self.recommendation_id,
            "entity_id": self.entity_id,
            "recommendation": self.recommendation,
            "priority": self.priority,
            "impact": self.impact,
            "implementation_effort": self.implementation_effort,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class RiskAnalysis:
    """Risk analysis result."""
    analysis_id: str
    entity_id: str
    risk_score: float
    risk_level: RiskLevel
    contributing_factors: List[Dict[str, Any]]
    mitigation_options: List[str]
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "analysis_id": self.analysis_id,
            "entity_id": self.entity_id,
            "risk_score": self.risk_score,
            "risk_level": self.risk_level.value,
            "contributing_factors": self.contributing_factors,
            "mitigation_options": self.mitigation_options,
            "created_at": self.created_at.isoformat(),
        }