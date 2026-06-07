# src/api/services/fraud_service.py
"""Fraud service – orchestrates fraud detection workflow.

It uses the ScoringService to compute a risk score and can be extended
with additional business rules, model ensembles, or external API calls.
"""

from __future__ import annotations

from typing import Dict, Any

from .scoring_service import ScoringService


class FraudService:
    """High‑level fraud detection service.

    The service is deliberately lightweight now; the public ``detect_fraud``
    method returns a dict with a ``risk_score`` and a ``is_fraud`` flag based on
    a simple threshold.  Future versions will incorporate graph‑neural‑network
    inference, explainability, and adaptive thresholds.
    """

    def __init__(self, scoring_service: ScoringService) -> None:
        self.scoring_service = scoring_service
        # Placeholder for additional rule engines, data sources, etc.
        self.fraud_threshold = 70.0

    def detect_fraud(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Run fraud detection on a *transaction* payload.

        Returns a dictionary containing the computed ``risk_score`` and a
        boolean ``is_fraud`` indicating whether the score exceeds the configured
        threshold.
        """
        score = self.scoring_service.compute_score(transaction)
        return {
            "risk_score": score,
            "is_fraud": score >= self.fraud_threshold,
        }
