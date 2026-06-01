# src/api/services/scoring_service.py
"""Scoring service – encapsulates all business‑logic for computing risk scores.

In a production system this would interface with the graph neural network,
pre‑trained models, rule‑based components, etc. For now we provide a minimal
implementation that can be expanded later.
"""

from __future__ import annotations

from typing import Any, Dict


class ScoringService:
    """Calculate a risk score for a transaction.

    The public ``compute_score`` method receives a transaction payload (as a
    ``dict``) and returns a numeric score between 0 and 100.  The implementation
    is deliberately simple – it sums placeholder feature values – but the
    signature is stable for future AI integration.
    """

    def __init__(self) -> None:
        # Placeholder for model loading – in the real product this would load a
        # GNN model, embeddings, or rule sets.
        self._model: Any = None
        self._load_model()

    def _load_model(self) -> None:
        """Load the underlying scoring model.

        In the MVP we just set a dummy object; replace with actual model loading
        (e.g., torch.load, TensorFlow, etc.) when the AI component is ready.
        """
        self._model = "dummy-model"

    def compute_score(self, transaction: Dict[str, Any]) -> float:
        """Return a risk score for *transaction*.

        Args:
            transaction: Parsed transaction payload.
        Returns:
            A float between 0 and 100 where higher means more risky.
        """
        if not isinstance(transaction, dict):
            raise TypeError("transaction must be a dict")
        # Simple heuristic – count number of keys as a proxy for complexity.
        base_score = len(transaction) * 10.0
        # Clamp to 0‑100 range.
        return max(0.0, min(100.0, base_score))
