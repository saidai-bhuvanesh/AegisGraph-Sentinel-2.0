"""Tests for Trust Network Module"""
import pytest
from src.trust_network import TrustEngine, TrustLevel

class TestTrustEngine:
    def setup_method(self):
        self.engine = TrustEngine()
    
    def test_add_entity(self):
        entity_id = self.engine.add_entity("Test Entity", 0.8)
        assert entity_id is not None
        assert self.engine.get_entity(entity_id) is not None
    
    def test_add_reputation(self):
        entity_id = self.engine.add_entity("Rep Test", 0.7)
        record_id = self.engine.add_reputation(entity_id, 0.9, ["factor1"])
        assert record_id is not None
    
    def test_get_stats(self):
        stats = self.engine.get_stats()
        assert "total_entities" in stats

if __name__ == "__main__":
    pytest.main([__file__, "-v"])