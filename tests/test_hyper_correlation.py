"""Tests for Hyper Correlation Module"""
import pytest
from src.hyper_correlation import HyperCorrelationEngine, CorrelationType

class TestHyperCorrelationEngine:
    def setup_method(self):
        self.engine = HyperCorrelationEngine()
    
    def test_correlate(self):
        event_id = self.engine.correlate(CorrelationType.TEMPORAL, ["event1", "event2"])
        assert event_id is not None
        assert self.engine.get_event(event_id) is not None
    
    def test_get_stats(self):
        self.engine.correlate(CorrelationType.SPATIAL, [])
        stats = self.engine.get_stats()
        assert "total_correlations" in stats

if __name__ == "__main__":
    pytest.main([__file__, "-v"])