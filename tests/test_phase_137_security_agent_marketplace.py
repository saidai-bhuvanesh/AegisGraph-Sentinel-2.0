"""
Comprehensive testing module for Security Agent Marketplace
"""

import pytest
from src.phase_137_security_agent_marketplace.models import AgentBlueprint, MarketplaceListing, DeploymentInstance, AgentSubscription
from src.phase_137_security_agent_marketplace.store import get_store
from src.phase_137_security_agent_marketplace.service import get_service
from src.phase_137_security_agent_marketplace.analytics import SecurityAgentMarketplaceAnalytics

def test_models_to_dict():
    obj = AgentBlueprint()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = AgentBlueprint.from_dict(d)
    assert obj2.blueprint_id == obj.blueprint_id

    obj = MarketplaceListing()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = MarketplaceListing.from_dict(d)
    assert obj2.listing_id == obj.listing_id

    obj = DeploymentInstance()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = DeploymentInstance.from_dict(d)
    assert obj2.instance_id == obj.instance_id

    obj = AgentSubscription()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = AgentSubscription.from_dict(d)
    assert obj2.subscription_id == obj.subscription_id

def test_store_operations():
    store = get_store()
    obj = AgentBlueprint()
    store.add_agentblueprint(obj)
    assert store.get_agentblueprint(obj.blueprint_id) is not None
    assert len(store.list_agentblueprints()) >= 1

    obj = MarketplaceListing()
    store.add_marketplacelisting(obj)
    assert store.get_marketplacelisting(obj.listing_id) is not None
    assert len(store.list_marketplacelistings()) >= 1

    obj = DeploymentInstance()
    store.add_deploymentinstance(obj)
    assert store.get_deploymentinstance(obj.instance_id) is not None
    assert len(store.list_deploymentinstances()) >= 1

    obj = AgentSubscription()
    store.add_agentsubscription(obj)
    assert store.get_agentsubscription(obj.subscription_id) is not None
    assert len(store.list_agentsubscriptions()) >= 1

def test_service_methods():
    srv = get_service()
    assert srv.list_blueprints() is not None
    assert srv.publish_blueprint(name="test", agent_type="test") is not None
    assert srv.deploy_agent(blueprint_id="test", tenant_id="test") is not None
    assert srv.get_agent_metrics(instance_id="test") is not None
    assert srv.execute("tenant-123")["status"] == "success"

def test_analytics():
    calc = SecurityAgentMarketplaceAnalytics()
    assert calc.calculate_kpis()["efficiency_rating"] == 98.4
    assert calc.generate_dashboard_metrics()["system_health"] == 100.0
