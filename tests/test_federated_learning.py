"""Tests for Federated Learning Module"""
import pytest
from src.federated_learning import FederatedLearningEngine, NodeRole

class TestFederatedLearningEngine:
    def setup_method(self):
        self.engine = FederatedLearningEngine()
    
    def test_register_node(self):
        node_id = self.engine.register_node("Test Node", NodeRole.PARTICIPANT)
        assert node_id is not None
    
    def test_submit_update(self):
        node_id = self.engine.register_node("Test", NodeRole.AGGREGATOR)
        update_id = self.engine.submit_update(node_id, {"w1": 0.5})
        assert update_id is not None
    
    def test_get_stats(self):
        stats = self.engine.get_stats()
        assert "total_nodes" in stats

if __name__ == "__main__":
    pytest.main([__file__, "-v"])