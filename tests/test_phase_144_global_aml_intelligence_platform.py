"""
Comprehensive testing module for Global AML Intelligence Platform
"""

import pytest
from src.phase_144_global_aml_intelligence_platform.models import SanctionsList, AmlAlert, SanctionsMatch, AmlCase
from src.phase_144_global_aml_intelligence_platform.store import get_store
from src.phase_144_global_aml_intelligence_platform.service import get_service
from src.phase_144_global_aml_intelligence_platform.analytics import GlobalAMLIntelligencePlatformAnalytics

def test_models_to_dict():
    obj = SanctionsList()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = SanctionsList.from_dict(d)
    assert obj2.list_id == obj.list_id

    obj = AmlAlert()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = AmlAlert.from_dict(d)
    assert obj2.alert_id == obj.alert_id

    obj = SanctionsMatch()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = SanctionsMatch.from_dict(d)
    assert obj2.match_id == obj.match_id

    obj = AmlCase()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = AmlCase.from_dict(d)
    assert obj2.case_id == obj.case_id

def test_store_operations():
    store = get_store()
    obj = SanctionsList()
    store.add_sanctionslist(obj)
    assert store.get_sanctionslist(obj.list_id) is not None
    assert len(store.list_sanctionslists()) >= 1

    obj = AmlAlert()
    store.add_amlalert(obj)
    assert store.get_amlalert(obj.alert_id) is not None
    assert len(store.list_amlalerts()) >= 1

    obj = SanctionsMatch()
    store.add_sanctionsmatch(obj)
    assert store.get_sanctionsmatch(obj.match_id) is not None
    assert len(store.list_sanctionsmatchs()) >= 1

    obj = AmlCase()
    store.add_amlcase(obj)
    assert store.get_amlcase(obj.case_id) is not None
    assert len(store.list_amlcases()) >= 1

def test_service_methods():
    srv = get_service()
    assert srv.screen_sanctions(entity_name="test") is not None
    assert srv.process_aml_alert(account_id="test", alert_type="test", score=0.0) is not None
    assert srv.create_aml_case(account_id="test", priority="test") is not None
    assert srv.update_sanctions_list(list_name="test", count=0) is not None
    assert srv.execute("tenant-123")["status"] == "success"

def test_analytics():
    calc = GlobalAMLIntelligencePlatformAnalytics()
    assert calc.calculate_kpis()["efficiency_rating"] == 98.4
    assert calc.generate_dashboard_metrics()["system_health"] == 100.0
