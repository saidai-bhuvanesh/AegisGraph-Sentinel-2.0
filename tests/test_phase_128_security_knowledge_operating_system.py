"""
Comprehensive testing module for Security Knowledge Operating System
"""

import pytest
from src.phase_128_security_knowledge_operating_system.models import KnowledgeArticle, InvestigationKnowledge, ThreatIntelEntry, FraudPattern
from src.phase_128_security_knowledge_operating_system.store import get_store
from src.phase_128_security_knowledge_operating_system.service import get_service
from src.phase_128_security_knowledge_operating_system.analytics import SecurityKnowledgeOperatingSystemAnalytics

def test_models_to_dict():
    obj = KnowledgeArticle()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = KnowledgeArticle.from_dict(d)
    assert obj2.article_id == obj.article_id

    obj = InvestigationKnowledge()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = InvestigationKnowledge.from_dict(d)
    assert obj2.knowledge_id == obj.knowledge_id

    obj = ThreatIntelEntry()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = ThreatIntelEntry.from_dict(d)
    assert obj2.intel_id == obj.intel_id

    obj = FraudPattern()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = FraudPattern.from_dict(d)
    assert obj2.pattern_id == obj.pattern_id

def test_store_operations():
    store = get_store()
    obj = KnowledgeArticle()
    store.add_knowledgearticle(obj)
    assert store.get_knowledgearticle(obj.article_id) is not None
    assert len(store.list_knowledgearticles()) >= 1

    obj = InvestigationKnowledge()
    store.add_investigationknowledge(obj)
    assert store.get_investigationknowledge(obj.knowledge_id) is not None
    assert len(store.list_investigationknowledges()) >= 1

    obj = ThreatIntelEntry()
    store.add_threatintelentry(obj)
    assert store.get_threatintelentry(obj.intel_id) is not None
    assert len(store.list_threatintelentrys()) >= 1

    obj = FraudPattern()
    store.add_fraudpattern(obj)
    assert store.get_fraudpattern(obj.pattern_id) is not None
    assert len(store.list_fraudpatterns()) >= 1

def test_service_methods():
    srv = get_service()
    assert srv.create_article(title="test", content="test", category="test") is not None
    assert srv.search_knowledge(query="test") is not None
    assert srv.link_investigation(case_id="test", knowledge_id="test") is not None
    assert srv.register_fraud_pattern(name="test", rules=[]) is not None
    assert srv.execute("tenant-123")["status"] == "success"

def test_analytics():
    calc = SecurityKnowledgeOperatingSystemAnalytics()
    assert calc.calculate_kpis()["efficiency_rating"] == 98.4
    assert calc.generate_dashboard_metrics()["system_health"] == 100.0
