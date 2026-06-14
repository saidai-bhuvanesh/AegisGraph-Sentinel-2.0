"""
Comprehensive testing module for AegisGraph Sentinel X Ultimate Command Platform
"""

import pytest
from src.phase_150_aegisgraph_sentinel_x_ultimate_command_platform.models import PlatformStatus, EcosystemConfig, UltimateReport, OrchestratorEvent
from src.phase_150_aegisgraph_sentinel_x_ultimate_command_platform.store import get_store
from src.phase_150_aegisgraph_sentinel_x_ultimate_command_platform.service import get_service
from src.phase_150_aegisgraph_sentinel_x_ultimate_command_platform.analytics import AegisGraphSentinelXUltimateCommandPlatformAnalytics

def test_models_to_dict():
    obj = PlatformStatus()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = PlatformStatus.from_dict(d)
    assert obj2.platform_id == obj.platform_id

    obj = EcosystemConfig()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = EcosystemConfig.from_dict(d)
    assert obj2.config_id == obj.config_id

    obj = UltimateReport()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = UltimateReport.from_dict(d)
    assert obj2.report_id == obj.report_id

    obj = OrchestratorEvent()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = OrchestratorEvent.from_dict(d)
    assert obj2.event_id == obj.event_id

def test_store_operations():
    store = get_store()
    obj = PlatformStatus()
    store.add_platformstatus(obj)
    assert store.get_platformstatus(obj.platform_id) is not None
    assert len(store.list_platformstatuss()) >= 1

    obj = EcosystemConfig()
    store.add_ecosystemconfig(obj)
    assert store.get_ecosystemconfig(obj.config_id) is not None
    assert len(store.list_ecosystemconfigs()) >= 1

    obj = UltimateReport()
    store.add_ultimatereport(obj)
    assert store.get_ultimatereport(obj.report_id) is not None
    assert len(store.list_ultimatereports()) >= 1

    obj = OrchestratorEvent()
    store.add_orchestratorevent(obj)
    assert store.get_orchestratorevent(obj.event_id) is not None
    assert len(store.list_orchestratorevents()) >= 1

def test_service_methods():
    srv = get_service()
    assert srv.get_ultimate_status() is not None
    assert srv.configure_unification(enabled="test", auto_remed="test") is not None
    assert srv.generate_ultimate_report() is not None
    assert srv.dispatch_event(origin=0, event_type="test") is not None
    assert srv.execute("tenant-123")["status"] == "success"

def test_analytics():
    calc = AegisGraphSentinelXUltimateCommandPlatformAnalytics()
    assert calc.calculate_kpis()["efficiency_rating"] == 98.4
    assert calc.generate_dashboard_metrics()["system_health"] == 100.0
