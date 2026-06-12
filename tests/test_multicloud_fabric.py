"""Tests for Multi-Cloud Fabric Module"""
import pytest
from src.multicloud_fabric import MultiCloudFabric, CloudProvider

class TestMultiCloudFabric:
    def setup_method(self):
        self.fabric = MultiCloudFabric()
    
    def test_add_connector(self):
        conn_id = self.fabric.add_connector(CloudProvider.AWS)
        assert conn_id is not None
        assert self.fabric.get_connector(conn_id) is not None
    
    def test_create_fabric(self):
        fabric_id = self.fabric.create_fabric("Test Fabric")
        assert fabric_id is not None
    
    def test_get_stats(self):
        stats = self.fabric.get_stats()
        assert "total_connectors" in stats

if __name__ == "__main__":
    pytest.main([__file__, "-v"])