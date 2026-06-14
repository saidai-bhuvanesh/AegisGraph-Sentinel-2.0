"""
Comprehensive testing module for Autonomous Investigation Factory
"""

import pytest
from src.phase_130_autonomous_investigation_factory.models import Investigation, Evidence, EntityCorrelation, CaseReport
from src.phase_130_autonomous_investigation_factory.store import get_store
from src.phase_130_autonomous_investigation_factory.service import get_service
from src.phase_130_autonomous_investigation_factory.analytics import AutonomousInvestigationFactoryAnalytics

def test_models_to_dict():
    obj = Investigation()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = Investigation.from_dict(d)
    assert obj2.investigation_id == obj.investigation_id

    obj = Evidence()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = Evidence.from_dict(d)
    assert obj2.evidence_id == obj.evidence_id

    obj = EntityCorrelation()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = EntityCorrelation.from_dict(d)
    assert obj2.correlation_id == obj.correlation_id

    obj = CaseReport()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = CaseReport.from_dict(d)
    assert obj2.report_id == obj.report_id

def test_store_operations():
    store = get_store()
    obj = Investigation()
    store.add_investigation(obj)
    assert store.get_investigation(obj.investigation_id) is not None
    assert len(store.list_investigations()) >= 1

    obj = Evidence()
    store.add_evidence(obj)
    assert store.get_evidence(obj.evidence_id) is not None
    assert len(store.list_evidences()) >= 1

    obj = EntityCorrelation()
    store.add_entitycorrelation(obj)
    assert store.get_entitycorrelation(obj.correlation_id) is not None
    assert len(store.list_entitycorrelations()) >= 1

    obj = CaseReport()
    store.add_casereport(obj)
    assert store.get_casereport(obj.report_id) is not None
    assert len(store.list_casereports()) >= 1

def test_service_methods():
    srv = get_service()
    assert srv.create_investigation(target_entity="test") is not None
    assert srv.gather_evidence(investigation_id="test", source="test") is not None
    assert srv.correlate_entities(source="test", target="test") is not None
    assert srv.produce_report(investigation_id="test") is not None
    assert srv.execute("tenant-123")["status"] == "success"

def test_analytics():
    calc = AutonomousInvestigationFactoryAnalytics()
    assert calc.calculate_kpis()["efficiency_rating"] == 98.4
    assert calc.generate_dashboard_metrics()["system_health"] == 100.0
