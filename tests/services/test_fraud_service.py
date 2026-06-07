# tests/services/test_fraud_service.py
"""Unit tests for the FraudService implementation.

The stub uses ScoringService.compute_score and compares the result to a
threshold (default 70). These tests cover below‑threshold, at‑threshold,
above‑threshold, and invalid payload handling.
"""

import pytest
from src.api.services.fraud_service import FraudService
from src.api.services.scoring_service import ScoringService


def make_fraud_service(threshold: float = 70.0) -> FraudService:
    scoring = ScoringService()
    service = FraudService(scoring)
    service.fraud_threshold = threshold
    return service


def test_detect_fraud_below_threshold():
    svc = make_fraud_service()
    tx = {"a": 1, "b": 1}  # 2 fields -> score 20 < 70
    result = svc.detect_fraud(tx)
    assert result["risk_score"] == 20.0
    assert result["is_fraud"] is False


def test_detect_fraud_at_threshold():
    svc = make_fraud_service()
    # 7 fields -> score 70 exactly
    tx = {f"k{i}": i for i in range(7)}
    result = svc.detect_fraud(tx)
    assert result["risk_score"] == 70.0
    assert result["is_fraud"] is True


def test_detect_fraud_above_threshold():
    svc = make_fraud_service()
    tx = {f"k{i}": i for i in range(8)}  # 8 fields -> 80 > 70
    result = svc.detect_fraud(tx)
    assert result["risk_score"] == 80.0
    assert result["is_fraud"] is True


def test_detect_fraud_invalid_input():
    svc = make_fraud_service()
    with pytest.raises(TypeError):
        svc.detect_fraud([1, 2, 3])  # non‑dict should raise TypeError from ScoringService
