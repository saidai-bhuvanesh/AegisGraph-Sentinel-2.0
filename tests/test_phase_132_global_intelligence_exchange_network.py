"""
Comprehensive testing module for Global Intelligence Exchange Network
"""

import pytest
from src.phase_132_global_intelligence_exchange_network.models import ExchangeNode, IntelligencePayload, SharingPolicy, ExchangeAudit
from src.phase_132_global_intelligence_exchange_network.store import get_store
from src.phase_132_global_intelligence_exchange_network.service import get_service
from src.phase_132_global_intelligence_exchange_network.analytics import GlobalIntelligenceExchangeNetworkAnalytics

def test_models_to_dict():
    obj = ExchangeNode()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = ExchangeNode.from_dict(d)
    assert obj2.node_id == obj.node_id

    obj = IntelligencePayload()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = IntelligencePayload.from_dict(d)
    assert obj2.payload_id == obj.payload_id

    obj = SharingPolicy()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = SharingPolicy.from_dict(d)
    assert obj2.policy_id == obj.policy_id

    obj = ExchangeAudit()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = ExchangeAudit.from_dict(d)
    assert obj2.audit_id == obj.audit_id

def test_store_operations():
    store = get_store()
    obj = ExchangeNode()
    store.add_exchangenode(obj)
    assert store.get_exchangenode(obj.node_id) is not None
    assert len(store.list_exchangenodes()) >= 1

    obj = IntelligencePayload()
    store.add_intelligencepayload(obj)
    assert store.get_intelligencepayload(obj.payload_id) is not None
    assert len(store.list_intelligencepayloads()) >= 1

    obj = SharingPolicy()
    store.add_sharingpolicy(obj)
    assert store.get_sharingpolicy(obj.policy_id) is not None
    assert len(store.list_sharingpolicys()) >= 1

    obj = ExchangeAudit()
    store.add_exchangeaudit(obj)
    assert store.get_exchangeaudit(obj.audit_id) is not None
    assert len(store.list_exchangeaudits()) >= 1

def test_service_methods():
    srv = get_service()
    assert srv.register_node(org_name="test", endpoint="test") is not None
    assert srv.share_intelligence(sender="test", data_type="test", content="test") is not None
    assert srv.configure_policy(classification="test", allowed=[]) is not None
    assert srv.get_exchange_audits(node_id="test") is not None
    assert srv.execute("tenant-123")["status"] == "success"

def test_analytics():
    calc = GlobalIntelligenceExchangeNetworkAnalytics()
    assert calc.calculate_kpis()["efficiency_rating"] == 98.4
    assert calc.generate_dashboard_metrics()["system_health"] == 100.0
