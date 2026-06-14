"""
Comprehensive testing module for Global Security Command Network
"""

import pytest
from src.phase_141_global_security_command_network.models import CommandNetworkNode, CoordinatedCampaign, TacticalDirective, CommandTelemetry
from src.phase_141_global_security_command_network.store import get_store
from src.phase_141_global_security_command_network.service import get_service
from src.phase_141_global_security_command_network.analytics import GlobalSecurityCommandNetworkAnalytics

def test_models_to_dict():
    obj = CommandNetworkNode()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = CommandNetworkNode.from_dict(d)
    assert obj2.node_id == obj.node_id

    obj = CoordinatedCampaign()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = CoordinatedCampaign.from_dict(d)
    assert obj2.campaign_id == obj.campaign_id

    obj = TacticalDirective()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = TacticalDirective.from_dict(d)
    assert obj2.directive_id == obj.directive_id

    obj = CommandTelemetry()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = CommandTelemetry.from_dict(d)
    assert obj2.telemetry_id == obj.telemetry_id

def test_store_operations():
    store = get_store()
    obj = CommandNetworkNode()
    store.add_commandnetworknode(obj)
    assert store.get_commandnetworknode(obj.node_id) is not None
    assert len(store.list_commandnetworknodes()) >= 1

    obj = CoordinatedCampaign()
    store.add_coordinatedcampaign(obj)
    assert store.get_coordinatedcampaign(obj.campaign_id) is not None
    assert len(store.list_coordinatedcampaigns()) >= 1

    obj = TacticalDirective()
    store.add_tacticaldirective(obj)
    assert store.get_tacticaldirective(obj.directive_id) is not None
    assert len(store.list_tacticaldirectives()) >= 1

    obj = CommandTelemetry()
    store.add_commandtelemetry(obj)
    assert store.get_commandtelemetry(obj.telemetry_id) is not None
    assert len(store.list_commandtelemetrys()) >= 1

def test_service_methods():
    srv = get_service()
    assert srv.register_command_node(region="test", sector="test") is not None
    assert srv.coordinate_defense(campaign_desc="test", targets=[]) is not None
    assert srv.issue_directive(campaign_id="test", instructions="test") is not None
    assert srv.send_telemetry(node_id="test", kpis={}, float]="test") is not None
    assert srv.execute("tenant-123")["status"] == "success"

def test_analytics():
    calc = GlobalSecurityCommandNetworkAnalytics()
    assert calc.calculate_kpis()["efficiency_rating"] == 98.4
    assert calc.generate_dashboard_metrics()["system_health"] == 100.0
