"""
Comprehensive testing module for Cross-Border Fraud Intelligence Platform
"""

import pytest
from src.phase_142_cross_border_fraud_intelligence_platform.models import CrossBorderTx, TransnationalMuleRing, JurisdictionalReport, IntelExchangeLog
from src.phase_142_cross_border_fraud_intelligence_platform.store import get_store
from src.phase_142_cross_border_fraud_intelligence_platform.service import get_service
from src.phase_142_cross_border_fraud_intelligence_platform.analytics import CrossBorderFraudIntelligencePlatformAnalytics

def test_models_to_dict():
    obj = CrossBorderTx()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = CrossBorderTx.from_dict(d)
    assert obj2.tx_id == obj.tx_id

    obj = TransnationalMuleRing()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = TransnationalMuleRing.from_dict(d)
    assert obj2.ring_id == obj.ring_id

    obj = JurisdictionalReport()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = JurisdictionalReport.from_dict(d)
    assert obj2.report_id == obj.report_id

    obj = IntelExchangeLog()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = IntelExchangeLog.from_dict(d)
    assert obj2.log_id == obj.log_id

def test_store_operations():
    store = get_store()
    obj = CrossBorderTx()
    store.add_crossbordertx(obj)
    assert store.get_crossbordertx(obj.tx_id) is not None
    assert len(store.list_crossbordertxs()) >= 1

    obj = TransnationalMuleRing()
    store.add_transnationalmulering(obj)
    assert store.get_transnationalmulering(obj.ring_id) is not None
    assert len(store.list_transnationalmulerings()) >= 1

    obj = JurisdictionalReport()
    store.add_jurisdictionalreport(obj)
    assert store.get_jurisdictionalreport(obj.report_id) is not None
    assert len(store.list_jurisdictionalreports()) >= 1

    obj = IntelExchangeLog()
    store.add_intelexchangelog(obj)
    assert store.get_intelexchangelog(obj.log_id) is not None
    assert len(store.list_intelexchangelogs()) >= 1

def test_service_methods():
    srv = get_service()
    assert srv.track_cross_border_tx(source="test", dest="test", amount=0.0) is not None
    assert srv.detect_transnational_rings(countries=[]) is not None
    assert srv.generate_jurisdictional_report(jurisdiction="test") is not None
    assert srv.exchange_intel_records(partner="test", records_count=0) is not None
    assert srv.execute("tenant-123")["status"] == "success"

def test_analytics():
    calc = CrossBorderFraudIntelligencePlatformAnalytics()
    assert calc.calculate_kpis()["efficiency_rating"] == 98.4
    assert calc.generate_dashboard_metrics()["system_health"] == 100.0
