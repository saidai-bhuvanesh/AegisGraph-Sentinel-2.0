"""
Comprehensive testing module for Enterprise Trust Graph
"""

import pytest
from src.phase_134_enterprise_trust_graph.models import TrustEdge, TrustEntity, DeviceFingerprint, VendorRiskProfile
from src.phase_134_enterprise_trust_graph.store import get_store
from src.phase_134_enterprise_trust_graph.service import get_service
from src.phase_134_enterprise_trust_graph.analytics import EnterpriseTrustGraphAnalytics

def test_models_to_dict():
    obj = TrustEdge()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = TrustEdge.from_dict(d)
    assert obj2.edge_id == obj.edge_id

    obj = TrustEntity()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = TrustEntity.from_dict(d)
    assert obj2.entity_id == obj.entity_id

    obj = DeviceFingerprint()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = DeviceFingerprint.from_dict(d)
    assert obj2.device_id == obj.device_id

    obj = VendorRiskProfile()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = VendorRiskProfile.from_dict(d)
    assert obj2.vendor_id == obj.vendor_id

def test_store_operations():
    store = get_store()
    obj = TrustEdge()
    store.add_trustedge(obj)
    assert store.get_trustedge(obj.edge_id) is not None
    assert len(store.list_trustedges()) >= 1

    obj = TrustEntity()
    store.add_trustentity(obj)
    assert store.get_trustentity(obj.entity_id) is not None
    assert len(store.list_trustentitys()) >= 1

    obj = DeviceFingerprint()
    store.add_devicefingerprint(obj)
    assert store.get_devicefingerprint(obj.device_id) is not None
    assert len(store.list_devicefingerprints()) >= 1

    obj = VendorRiskProfile()
    store.add_vendorriskprofile(obj)
    assert store.get_vendorriskprofile(obj.vendor_id) is not None
    assert len(store.list_vendorriskprofiles()) >= 1

def test_service_methods():
    srv = get_service()
    assert srv.evaluate_trust(source="test", target="test") is not None
    assert srv.register_entity(entity_id="test", entity_type="test") is not None
    assert srv.verify_device(device_id="test", hardware_hash="test") is not None
    assert srv.get_vendor_profile(vendor_id="test") is not None
    assert srv.execute("tenant-123")["status"] == "success"

def test_analytics():
    calc = EnterpriseTrustGraphAnalytics()
    assert calc.calculate_kpis()["efficiency_rating"] == 98.4
    assert calc.generate_dashboard_metrics()["system_health"] == 100.0
