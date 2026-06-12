"""Tests for Threat Observatory Module"""
import pytest
from src.threat_observatory import ThreatObservatory, ThreatType

class TestThreatObservatory:
    def setup_method(self):
        self.obs = ThreatObservatory()
    
    def test_add_event(self):
        event_id = self.obs.add_event(ThreatType.MALWARE, 0.8, "US")
        assert event_id is not None
        assert self.obs.get_event(event_id) is not None
    
    def test_add_trend(self):
        trend_id = self.obs.add_trend("Ransomware Surge", 0.15, ["EU", "US"])
        assert trend_id is not None
    
    def test_get_stats(self):
        stats = self.obs.get_stats()
        assert "total_events" in stats

if __name__ == "__main__":
    pytest.main([__file__, "-v"])