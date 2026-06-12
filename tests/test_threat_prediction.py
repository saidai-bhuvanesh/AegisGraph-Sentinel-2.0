"""Tests for Threat Prediction Module"""
import pytest
from src.threat_prediction import ThreatPredictionEngine, PredictionType

class TestThreatPredictionEngine:
    def setup_method(self):
        self.engine = ThreatPredictionEngine()
    
    def test_predict(self):
        pred_id = self.engine.predict(PredictionType.ATTACK, "Test prediction")
        assert pred_id is not None
        assert self.engine.get_prediction(pred_id) is not None
    
    def test_get_stats(self):
        self.engine.predict(PredictionType.THREAT, "Test")
        stats = self.engine.get_stats()
        assert "total_predictions" in stats

if __name__ == "__main__":
    pytest.main([__file__, "-v"])