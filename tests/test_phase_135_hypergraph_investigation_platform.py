"""
Comprehensive testing module for Hypergraph Investigation Platform
"""

import pytest
from src.phase_135_hypergraph_investigation_platform.models import HyperEdge, HyperNode, InvestigationCluster, PatternMatch
from src.phase_135_hypergraph_investigation_platform.store import get_store
from src.phase_135_hypergraph_investigation_platform.service import get_service
from src.phase_135_hypergraph_investigation_platform.analytics import HypergraphInvestigationPlatformAnalytics

def test_models_to_dict():
    obj = HyperEdge()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = HyperEdge.from_dict(d)
    assert obj2.edge_id == obj.edge_id

    obj = HyperNode()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = HyperNode.from_dict(d)
    assert obj2.node_id == obj.node_id

    obj = InvestigationCluster()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = InvestigationCluster.from_dict(d)
    assert obj2.cluster_id == obj.cluster_id

    obj = PatternMatch()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = PatternMatch.from_dict(d)
    assert obj2.match_id == obj.match_id

def test_store_operations():
    store = get_store()
    obj = HyperEdge()
    store.add_hyperedge(obj)
    assert store.get_hyperedge(obj.edge_id) is not None
    assert len(store.list_hyperedges()) >= 1

    obj = HyperNode()
    store.add_hypernode(obj)
    assert store.get_hypernode(obj.node_id) is not None
    assert len(store.list_hypernodes()) >= 1

    obj = InvestigationCluster()
    store.add_investigationcluster(obj)
    assert store.get_investigationcluster(obj.cluster_id) is not None
    assert len(store.list_investigationclusters()) >= 1

    obj = PatternMatch()
    store.add_patternmatch(obj)
    assert store.get_patternmatch(obj.match_id) is not None
    assert len(store.list_patternmatchs()) >= 1

def test_service_methods():
    srv = get_service()
    assert srv.create_hyperedge(entities=[], rel_type="test") is not None
    assert srv.find_fraud_rings(min_entities=0) is not None
    assert srv.query_hypernode(node_id="test") is not None
    assert srv.detect_advanced_patterns(pattern_name="test") is not None
    assert srv.execute("tenant-123")["status"] == "success"

def test_analytics():
    calc = HypergraphInvestigationPlatformAnalytics()
    assert calc.calculate_kpis()["efficiency_rating"] == 98.4
    assert calc.generate_dashboard_metrics()["system_health"] == 100.0
