# tests/services/test_scoring_service.py
"""Unit tests for the ScoringService implementation.

These tests verify the simple heuristic used in the stub – the score is
`len(transaction) * 10` and is clamped to the range 0‑100.
"""

from src.api.services.scoring_service import ScoringService


def test_compute_score_basic():
    service = ScoringService()
    tx = {"field1": 1, "field2": 2, "field3": 3}
    # 3 fields -> 30.0
    assert service.compute_score(tx) == 30.0


def test_compute_score_clamped_max():
    service = ScoringService()
    # 11 fields would give 110, should be capped at 100
    tx = {f"k{i}": i for i in range(11)}
    assert service.compute_score(tx) == 100.0


def test_compute_score_clamped_min():
    service = ScoringService()
    tx = {}
    # empty dict yields 0
    assert service.compute_score(tx) == 0.0


def test_compute_score_non_dict_input():
    service = ScoringService()
    # Passing a non‑dict should raise a TypeError because len() is not defined
    try:
        service.compute_score([1, 2, 3])
    except Exception as exc:
        assert isinstance(exc, TypeError)
