"""Thread-safe in-memory store for AI Copilot insights and feedback.

Uses bounded LRU cache dictionaries for generated insights.
"""

from __future__ import annotations

import threading
from collections import OrderedDict
from typing import Dict, List, Optional

from .models import (
    InvestigationSummary,
    RiskExplanation,
    AIRecommendation,
    AnalystFeedback,
)


class _LRUDict(OrderedDict):
    """Bounded LRU dictionary — same pattern as case_store."""

    def __init__(self, maxsize: int = 10_000):
        self.maxsize = maxsize
        super().__init__()

    def __setitem__(self, key, value):
        if key in self:
            self.move_to_end(key)
        super().__setitem__(key, value)
        if len(self) > self.maxsize:
            self.popitem(last=False)

    def __getitem__(self, key):
        value = super().__getitem__(key)
        self.move_to_end(key)
        return value


class CopilotStore:
    """Singleton in-memory store for all copilot entities."""

    def __init__(self):
        self._lock = threading.RLock()
        self._summaries: _LRUDict = _LRUDict(maxsize=10_000)
        self._explanations: _LRUDict = _LRUDict(maxsize=10_000)
        self._recommendations: _LRUDict = _LRUDict(maxsize=10_000)
        self._feedback: Dict[str, List[AnalystFeedback]] = {}  # case_id → list of feedback

    # ------------------------------------------------------------------
    # Summaries
    # ------------------------------------------------------------------
    def save_summary(self, summary: InvestigationSummary) -> None:
        with self._lock:
            self._summaries[summary.case_id] = summary

    def get_summary(self, case_id: str) -> Optional[InvestigationSummary]:
        with self._lock:
            return self._summaries.get(case_id)

    # ------------------------------------------------------------------
    # Explanations
    # ------------------------------------------------------------------
    def save_explanation(self, explanation: RiskExplanation) -> None:
        with self._lock:
            self._explanations[explanation.case_id] = explanation

    def get_explanation(self, case_id: str) -> Optional[RiskExplanation]:
        with self._lock:
            return self._explanations.get(case_id)

    # ------------------------------------------------------------------
    # Recommendations
    # ------------------------------------------------------------------
    def save_recommendation(self, recommendation: AIRecommendation) -> None:
        with self._lock:
            self._recommendations[recommendation.case_id] = recommendation

    def get_recommendation(self, case_id: str) -> Optional[AIRecommendation]:
        with self._lock:
            return self._recommendations.get(case_id)

    # ------------------------------------------------------------------
    # Feedback
    # ------------------------------------------------------------------
    def add_feedback(
        self, case_id: str, analyst_id: str, score: int, text: Optional[str] = None
    ) -> AnalystFeedback:
        with self._lock:
            feedback = AnalystFeedback(
                case_id=case_id,
                analyst_id=analyst_id,
                usefulness_score=score,
                feedback_text=text,
            )
            if case_id not in self._feedback:
                self._feedback[case_id] = []
            self._feedback[case_id].append(feedback)
            return feedback

    def get_feedback(self, case_id: str) -> List[AnalystFeedback]:
        with self._lock:
            return list(self._feedback.get(case_id, []))


# Singleton access
_copilot_store_instance: Optional[CopilotStore] = None
_copilot_store_lock = threading.Lock()


def get_copilot_store() -> CopilotStore:
    global _copilot_store_instance
    if _copilot_store_instance is None:
        with _copilot_store_lock:
            if _copilot_store_instance is None:
                _copilot_store_instance = CopilotStore()
    return _copilot_store_instance
