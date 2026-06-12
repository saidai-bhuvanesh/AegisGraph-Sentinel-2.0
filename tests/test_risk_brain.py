"""
Tests for Enterprise Risk Brain Module
"""
import pytest
from datetime import datetime, timezone

from src.risk_brain import (
    EnterpriseRiskBrain,
    get_risk_brain,
    RiskGraphEngine,
    RiskForecastEngine,
    RiskRecommendationEngine,
    RiskAnalytics,
    RiskEntity,
    RiskCategory,
    RiskLevel,
    ForecastHorizon,
)


class TestRiskGraphEngine:
    """Tests for RiskGraphEngine."""
    
    def setup_method(self):
        self.engine = RiskGraphEngine()
    
    def test_add_entity(self):
        """Test adding an entity."""
        entity_id = self.engine.add_entity(
            name="Test Entity",
            risk_category=RiskCategory.CYBER,
        )
        
        assert entity_id is not None
        assert self.engine.get_entity(entity_id) is not None
    
    def test_get_entity(self):
        """Test getting an entity."""
        entity_id = self.engine.add_entity(
            name="Get Test",
            risk_category=RiskCategory.FRAUD,
        )
        
        entity = self.engine.get_entity(entity_id)
        assert entity is not None
        assert entity.name == "Get Test"
    
    def test_update_risk_score(self):
        """Test updating risk score."""
        entity_id = self.engine.add_entity(
            name="Score Test",
            risk_category=RiskCategory.CYBER,
        )
        
        success = self.engine.update_risk_score(entity_id, 0.85)
        assert success is True
        
        entity = self.engine.get_entity(entity_id)
        assert entity.risk_level == RiskLevel.CRITICAL
    
    def test_add_relationship(self):
        """Test adding relationships."""
        id1 = self.engine.add_entity("Entity 1", RiskCategory.CYBER)
        id2 = self.engine.add_entity("Entity 2", RiskCategory.FRAUD)
        
        success = self.engine.add_relationship(id1, id2)
        assert success is True


class TestRiskForecastEngine:
    """Tests for RiskForecastEngine."""
    
    def setup_method(self):
        self.engine = RiskForecastEngine()
    
    def test_generate_forecast(self):
        """Test generating a forecast."""
        forecast_id = self.engine.generate_forecast(
            entity_id="test-entity",
            horizon=ForecastHorizon.MEDIUM_TERM,
            current_score=0.5,
        )
        
        assert forecast_id is not None
        assert self.engine.get_forecast(forecast_id) is not None
    
    def test_get_forecasts_by_entity(self):
        """Test getting forecasts by entity."""
        self.engine.generate_forecast("entity-1", ForecastHorizon.SHORT_TERM, 0.4)
        self.engine.generate_forecast("entity-1", ForecastHorizon.LONG_TERM, 0.6)
        
        forecasts = self.engine.get_forecasts_by_entity("entity-1")
        assert len(forecasts) >= 2


class TestRiskRecommendationEngine:
    """Tests for RiskRecommendationEngine."""
    
    def setup_method(self):
        self.engine = RiskRecommendationEngine()
    
    def test_generate_recommendation(self):
        """Test generating a recommendation."""
        rec_id = self.engine.generate_recommendation(
            entity_id="test-entity",
            risk_score=0.85,
            risk_level=RiskLevel.CRITICAL,
        )
        
        assert rec_id is not None
        assert self.engine.get_recommendation(rec_id) is not None
    
    def test_get_recommendations_by_entity(self):
        """Test getting recommendations by entity."""
        self.engine.generate_recommendation("entity-2", 0.3, RiskLevel.LOW)
        self.engine.generate_recommendation("entity-2", 0.7, RiskLevel.HIGH)
        
        recs = self.engine.get_recommendations_by_entity("entity-2")
        assert len(recs) >= 2


class TestRiskAnalytics:
    """Tests for RiskAnalytics."""
    
    def setup_method(self):
        self.graph = RiskGraphEngine()
        self.analytics = RiskAnalytics(self.graph)
    
    def test_analyze_risk(self):
        """Test risk analysis."""
        entity_id = self.graph.add_entity(
            "Test",
            RiskCategory.CYBER,
            factors=[{"name": "Test Factor", "weight": 0.5}],
        )
        self.graph.update_risk_score(entity_id, 0.6)
        
        analysis = self.analytics.analyze_risk(entity_id)
        
        assert analysis is not None
        assert analysis.risk_score > 0
    
    def test_get_risk_summary(self):
        """Test getting risk summary."""
        self.graph.add_entity("Entity 1", RiskCategory.CYBER)
        self.graph.add_entity("Entity 2", RiskCategory.FRAUD)
        
        summary = self.analytics.get_risk_summary()
        
        assert "total_entities" in summary
        assert summary["total_entities"] >= 2


class TestEnterpriseRiskBrain:
    """Tests for EnterpriseRiskBrain."""
    
    def setup_method(self):
        self.brain = EnterpriseRiskBrain()
    
    def test_assess_risk(self):
        """Test risk assessment."""
        result = self.brain.assess_risk(
            name="Test Assessment",
            risk_category=RiskCategory.CYBER,
            factors=[{"name": "Factor", "weight": 0.7}],
        )
        
        assert "entity_id" in result
        assert "risk_score" in result
        assert "risk_level" in result
    
    def test_get_executive_dashboard(self):
        """Test executive dashboard."""
        self.brain.assess_risk(
            name="Dashboard Test",
            risk_category=RiskCategory.FRAUD,
            factors=[{"name": "Test", "weight": 0.5}],
        )
        
        dashboard = self.brain.get_executive_dashboard()
        
        assert "risk_summary" in dashboard
        assert "critical_entities" in dashboard


class TestModels:
    """Tests for model classes."""
    
    def test_risk_entity_to_dict(self):
        """Test RiskEntity serialization."""
        entity = RiskEntity(
            entity_id="test-1",
            name="Test",
            risk_category=RiskCategory.CYBER,
            current_risk_score=0.5,
        )
        
        data = entity.to_dict()
        assert data["entity_id"] == "test-1"
        assert data["risk_category"] == "CYBER"
    
    def test_risk_category_values(self):
        """Test RiskCategory enum."""
        assert RiskCategory.CYBER.value == "CYBER"
        assert RiskCategory.FRAUD.value == "FRAUD"
    
    def test_risk_level_values(self):
        """Test RiskLevel enum."""
        assert RiskLevel.CRITICAL.value == "CRITICAL"
        assert RiskLevel.HIGH.value == "HIGH"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])