"""
Comprehensive testing module for Global Fraud Intelligence Observatory 2.0
"""

import pytest
from src.phase_129_global_fraud_intelligence_observatory.models import FraudObservation, CampaignEvolution, FraudTrend, ScamEcosystem
from src.phase_129_global_fraud_intelligence_observatory.store import get_store
from src.phase_129_global_fraud_intelligence_observatory.service import get_service
from src.phase_129_global_fraud_intelligence_observatory.analytics import GlobalFraudIntelligenceObservatory20Analytics

def test_models_to_dict():
    obj = FraudObservation()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = FraudObservation.from_dict(d)
    assert obj2.observation_id == obj.observation_id

    obj = CampaignEvolution()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = CampaignEvolution.from_dict(d)
    assert obj2.campaign_id == obj.campaign_id

    obj = FraudTrend()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = FraudTrend.from_dict(d)
    assert obj2.trend_id == obj.trend_id

    obj = ScamEcosystem()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = ScamEcosystem.from_dict(d)
    assert obj2.ecosystem_id == obj.ecosystem_id

def test_store_operations():
    store = get_store()
    obj = FraudObservation()
    store.add_fraudobservation(obj)
    assert store.get_fraudobservation(obj.observation_id) is not None
    assert len(store.list_fraudobservations()) >= 1

    obj = CampaignEvolution()
    store.add_campaignevolution(obj)
    assert store.get_campaignevolution(obj.campaign_id) is not None
    assert len(store.list_campaignevolutions()) >= 1

    obj = FraudTrend()
    store.add_fraudtrend(obj)
    assert store.get_fraudtrend(obj.trend_id) is not None
    assert len(store.list_fraudtrends()) >= 1

    obj = ScamEcosystem()
    store.add_scamecosystem(obj)
    assert store.get_scamecosystem(obj.ecosystem_id) is not None
    assert len(store.list_scamecosystems()) >= 1

def test_service_methods():
    srv = get_service()
    assert srv.observe_fraud(country="test", fraud_type="test") is not None
    assert srv.track_campaign(campaign_id="test") is not None
    assert srv.analyze_trends(period="test") is not None
    assert srv.map_scam_ecosystem(ecosystem_id="test") is not None
    assert srv.execute("tenant-123")["status"] == "success"

def test_analytics():
    calc = GlobalFraudIntelligenceObservatory20Analytics()
    assert calc.calculate_kpis()["efficiency_rating"] == 98.4
    assert calc.generate_dashboard_metrics()["system_health"] == 100.0
