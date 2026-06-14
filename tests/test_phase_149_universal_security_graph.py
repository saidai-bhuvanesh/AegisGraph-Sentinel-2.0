"""
Comprehensive testing module for Universal Security Graph
"""

import pytest
from src.phase_149_universal_security_graph.models import UnifiedNode, UnifiedEdge, USGGraph, CrossDomainCorrelation
from src.phase_149_universal_security_graph.store import get_store
from src.phase_149_universal_security_graph.service import get_service
from src.phase_149_universal_security_graph.analytics import UniversalSecurityGraphAnalytics

def test_models_to_dict():
    obj = UnifiedNode()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = UnifiedNode.from_dict(d)
    assert obj2.node_id == obj.node_id

    obj = UnifiedEdge()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = UnifiedEdge.from_dict(d)
    assert obj2.edge_id == obj.edge_id

    obj = USGGraph()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = USGGraph.from_dict(d)
    assert obj2.graph_id == obj.graph_id

    obj = CrossDomainCorrelation()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = CrossDomainCorrelation.from_dict(d)
    assert obj2.correlation_id == obj.correlation_id

def test_store_operations():
    store = get_store()
    obj = UnifiedNode()
    store.add_unifiednode(obj)
    assert store.get_unifiednode(obj.node_id) is not None
    assert len(store.list_unifiednodes()) >= 1

    obj = UnifiedEdge()
    store.add_unifiededge(obj)
    assert store.get_unifiededge(obj.edge_id) is not None
    assert len(store.list_unifiededges()) >= 1

    obj = USGGraph()
    store.add_usggraph(obj)
    assert store.get_usggraph(obj.graph_id) is not None
    assert len(store.list_usggraphs()) >= 1

    obj = CrossDomainCorrelation()
    store.add_crossdomaincorrelation(obj)
    assert store.get_crossdomaincorrelation(obj.correlation_id) is not None
    assert len(store.list_crossdomaincorrelations()) >= 1

def test_service_methods():
    srv = get_service()
    assert srv.add_unified_node(domain="test", label="test", weight=0.0) is not None
    assert srv.add_unified_edge(source="test", target="test", edge_type="test") is not None
    assert srv.correlate_domains(source="test", target="test") is not None
    assert srv.get_usg_status() is not None
    assert srv.execute("tenant-123")["status"] == "success"

def test_analytics():
    calc = UniversalSecurityGraphAnalytics()
    assert calc.calculate_kpis()["efficiency_rating"] == 98.4
    assert calc.generate_dashboard_metrics()["system_health"] == 100.0
