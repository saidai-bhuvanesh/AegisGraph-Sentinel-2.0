"""
Comprehensive testing module for Global Intelligence Mesh 2.0
"""

import pytest
from src.phase_148_global_intelligence_mesh_20.models import MeshNode, MeshTelemetry, SyncPolicy, DefenseState
from src.phase_148_global_intelligence_mesh_20.store import get_store
from src.phase_148_global_intelligence_mesh_20.service import get_service
from src.phase_148_global_intelligence_mesh_20.analytics import GlobalIntelligenceMesh20Analytics

def test_models_to_dict():
    obj = MeshNode()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = MeshNode.from_dict(d)
    assert obj2.node_id == obj.node_id

    obj = MeshTelemetry()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = MeshTelemetry.from_dict(d)
    assert obj2.telemetry_id == obj.telemetry_id

    obj = SyncPolicy()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = SyncPolicy.from_dict(d)
    assert obj2.policy_id == obj.policy_id

    obj = DefenseState()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = DefenseState.from_dict(d)
    assert obj2.state_id == obj.state_id

def test_store_operations():
    store = get_store()
    obj = MeshNode()
    store.add_meshnode(obj)
    assert store.get_meshnode(obj.node_id) is not None
    assert len(store.list_meshnodes()) >= 1

    obj = MeshTelemetry()
    store.add_meshtelemetry(obj)
    assert store.get_meshtelemetry(obj.telemetry_id) is not None
    assert len(store.list_meshtelemetrys()) >= 1

    obj = SyncPolicy()
    store.add_syncpolicy(obj)
    assert store.get_syncpolicy(obj.policy_id) is not None
    assert len(store.list_syncpolicys()) >= 1

    obj = DefenseState()
    store.add_defensestate(obj)
    assert store.get_defensestate(obj.state_id) is not None
    assert len(store.list_defensestates()) >= 1

def test_service_methods():
    srv = get_service()
    assert srv.register_mesh_node(region="test", peers=[]) is not None
    assert srv.synchronize_mesh(node_id="test") is not None
    assert srv.configure_sync_policy(interval=0) is not None
    assert srv.get_mesh_defense_state() is not None
    assert srv.execute("tenant-123")["status"] == "success"

def test_analytics():
    calc = GlobalIntelligenceMesh20Analytics()
    assert calc.calculate_kpis()["efficiency_rating"] == 98.4
    assert calc.generate_dashboard_metrics()["system_health"] == 100.0
