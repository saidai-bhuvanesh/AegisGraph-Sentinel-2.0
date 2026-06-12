"""Tests for Intelligence Federation Module"""
import pytest
from src.intelligence_federation import (
    FederationEngine, FederationRegistry, IntelligenceExchange,
    IndustryType, FederationRole
)

class TestFederationRegistry:
    def setup_method(self):
        self.registry = FederationRegistry()
    
    def test_initialization(self):
        assert len(self.registry.members) > 0
    
    def test_register_member(self):
        member_id = self.registry.register_member(
            "Test Org", IndustryType.FINANCIAL, FederationRole.BOTH
        )
        assert member_id is not None
        assert self.registry.get_member(member_id) is not None
    
    def test_get_members_by_industry(self):
        members = self.registry.get_members_by_industry(IndustryType.FINANCIAL)
        assert len(members) >= 1

class TestIntelligenceExchange:
    def setup_method(self):
        self.exchange = IntelligenceExchange()
    
    def test_share_indicator(self):
        indicator_id = self.exchange.share_indicator(
            "ip", "192.168.1.1", IndustryType.FINANCIAL, 0.9
        )
        assert indicator_id is not None
    
    def test_search_indicators(self):
        self.exchange.share_indicator("domain", "test.com", IndustryType.FINANCIAL, 0.8)
        results = self.exchange.search_indicators(indicator_type="domain")
        assert len(results) >= 1

class TestFederationEngine:
    def setup_method(self):
        self.engine = FederationEngine()
    
    def test_join_federation(self):
        member_id = self.engine.join_federation(
            "Test", IndustryType.HEALTHCARE, FederationRole.CONSUMER
        )
        assert member_id is not None
    
    def test_get_federation_stats(self):
        stats = self.engine.get_federation_stats()
        assert "total_members" in stats

if __name__ == "__main__":
    pytest.main([__file__, "-v"])