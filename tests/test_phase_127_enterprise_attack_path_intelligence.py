"""
Comprehensive testing module for Enterprise Attack Path Intelligence Platform
"""

import pytest
from src.phase_127_enterprise_attack_path_intelligence.models import AttackPath, LateralMovement, AssetExposure, BreachScenario
from src.phase_127_enterprise_attack_path_intelligence.store import get_store
from src.phase_127_enterprise_attack_path_intelligence.service import get_service
from src.phase_127_enterprise_attack_path_intelligence.analytics import EnterpriseAttackPathIntelligencePlatformAnalytics

def test_models_to_dict():
    obj = AttackPath()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = AttackPath.from_dict(d)
    assert obj2.path_id == obj.path_id

    obj = LateralMovement()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = LateralMovement.from_dict(d)
    assert obj2.movement_id == obj.movement_id

    obj = AssetExposure()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = AssetExposure.from_dict(d)
    assert obj2.exposure_id == obj.exposure_id

    obj = BreachScenario()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = BreachScenario.from_dict(d)
    assert obj2.scenario_id == obj.scenario_id

def test_store_operations():
    store = get_store()
    obj = AttackPath()
    store.add_attackpath(obj)
    assert store.get_attackpath(obj.path_id) is not None
    assert len(store.list_attackpaths()) >= 1

    obj = LateralMovement()
    store.add_lateralmovement(obj)
    assert store.get_lateralmovement(obj.movement_id) is not None
    assert len(store.list_lateralmovements()) >= 1

    obj = AssetExposure()
    store.add_assetexposure(obj)
    assert store.get_assetexposure(obj.exposure_id) is not None
    assert len(store.list_assetexposures()) >= 1

    obj = BreachScenario()
    store.add_breachscenario(obj)
    assert store.get_breachscenario(obj.scenario_id) is not None
    assert len(store.list_breachscenarios()) >= 1

def test_service_methods():
    srv = get_service()
    assert srv.analyze_attack_path(source_node="test", target_node="test") is not None
    assert srv.detect_lateral_movement(source_host="test", dest_host="test") is not None
    assert srv.assess_exposure(asset_id="test") is not None
    assert srv.simulate_breach(entry_point="test", target_asset="test") is not None
    assert srv.execute("tenant-123")["status"] == "success"

def test_analytics():
    calc = EnterpriseAttackPathIntelligencePlatformAnalytics()
    assert calc.calculate_kpis()["efficiency_rating"] == 98.4
    assert calc.generate_dashboard_metrics()["system_health"] == 100.0
