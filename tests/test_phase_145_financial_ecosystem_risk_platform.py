"""
Comprehensive testing module for Financial Ecosystem Risk Platform
"""

import pytest
from src.phase_145_financial_ecosystem_risk_platform.models import EcosystemNode, InterbankTx, SystemicAnomaly, RiskExposureReport
from src.phase_145_financial_ecosystem_risk_platform.store import get_store
from src.phase_145_financial_ecosystem_risk_platform.service import get_service
from src.phase_145_financial_ecosystem_risk_platform.analytics import FinancialEcosystemRiskPlatformAnalytics

def test_models_to_dict():
    obj = EcosystemNode()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = EcosystemNode.from_dict(d)
    assert obj2.node_id == obj.node_id

    obj = InterbankTx()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = InterbankTx.from_dict(d)
    assert obj2.tx_id == obj.tx_id

    obj = SystemicAnomaly()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = SystemicAnomaly.from_dict(d)
    assert obj2.anomaly_id == obj.anomaly_id

    obj = RiskExposureReport()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = RiskExposureReport.from_dict(d)
    assert obj2.report_id == obj.report_id

def test_store_operations():
    store = get_store()
    obj = EcosystemNode()
    store.add_ecosystemnode(obj)
    assert store.get_ecosystemnode(obj.node_id) is not None
    assert len(store.list_ecosystemnodes()) >= 1

    obj = InterbankTx()
    store.add_interbanktx(obj)
    assert store.get_interbanktx(obj.tx_id) is not None
    assert len(store.list_interbanktxs()) >= 1

    obj = SystemicAnomaly()
    store.add_systemicanomaly(obj)
    assert store.get_systemicanomaly(obj.anomaly_id) is not None
    assert len(store.list_systemicanomalys()) >= 1

    obj = RiskExposureReport()
    store.add_riskexposurereport(obj)
    assert store.get_riskexposurereport(obj.report_id) is not None
    assert len(store.list_riskexposurereports()) >= 1

def test_service_methods():
    srv = get_service()
    assert srv.evaluate_ecosystem_node(institution="test") is not None
    assert srv.monitor_interbank_tx(from_node="test", to_node="test", amount=0.0) is not None
    assert srv.detect_systemic_anomaly(nodes=[], anomaly_type="test") is not None
    assert srv.generate_exposure_report(period="test") is not None
    assert srv.execute("tenant-123")["status"] == "success"

def test_analytics():
    calc = FinancialEcosystemRiskPlatformAnalytics()
    assert calc.calculate_kpis()["efficiency_rating"] == 98.4
    assert calc.generate_dashboard_metrics()["system_health"] == 100.0
