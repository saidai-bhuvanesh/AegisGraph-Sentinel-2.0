"""Data models for AI Fraud Investigation Copilot.

All models are pure Python dataclasses to store AI-generated insights in memory.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional


def _utcnow() -> str:
    """Return current UTC time as ISO-8601 string."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class InvestigationSummary:
    """AI-generated summary of a fraud case."""
    case_id: str
    summary: str
    suspicious_activity: List[str] = field(default_factory=list)
    key_risk_factors: List[str] = field(default_factory=list)
    unusual_patterns: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=_utcnow)


@dataclass
class RiskExplanation:
    """AI explanation of the risk score and model/graph decisioning."""
    case_id: str
    risk_score: float
    breakdown_explanation: str
    graph_relationship_explanation: str
    mule_detection_reasoning: str
    htgnn_decisions_explanation: str
    created_at: str = field(default_factory=_utcnow)


@dataclass
class AIRecommendation:
    """AI-recommended next actions for the analyst."""
    case_id: str
    recommended_actions: List[str] = field(default_factory=list)
    reasoning: str = ""
    escalation_path: str = ""
    created_at: str = field(default_factory=_utcnow)


@dataclass
class AnalystFeedback:
    """Feedback from analysts on the quality of AI insights."""
    case_id: str
    analyst_id: str
    usefulness_score: int  # e.g., 1-5 scale
    feedback_text: Optional[str] = None
    feedback_id: str = field(default_factory=lambda: f"FDB_{uuid.uuid4().hex[:12].upper()}")
    created_at: str = field(default_factory=_utcnow)
