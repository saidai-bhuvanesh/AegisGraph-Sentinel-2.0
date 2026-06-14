"""
Thread-safe store for Global Security Command Network
"""

import threading
from typing import Dict, List, Optional, Any
from .models import CommandNetworkNode, CoordinatedCampaign, TacticalDirective, CommandTelemetry

class GlobalSecurityCommandNetworkStore:
    def __init__(self):
        self.lock = threading.RLock()
        self._commandnetworknodes: Dict[str, CommandNetworkNode] = {}
        self._coordinatedcampaigns: Dict[str, CoordinatedCampaign] = {}
        self._tacticaldirectives: Dict[str, TacticalDirective] = {}
        self._commandtelemetrys: Dict[str, CommandTelemetry] = {}

    def add_commandnetworknode(self, obj: CommandNetworkNode) -> CommandNetworkNode:
        with self.lock:
            self._commandnetworknodes[obj.node_id] = obj
            return obj

    def get_commandnetworknode(self, key: str) -> Optional[CommandNetworkNode]:
        with self.lock:
            return self._commandnetworknodes.get(key)

    def list_commandnetworknodes(self) -> List[CommandNetworkNode]:
        with self.lock:
            return list(self._commandnetworknodes.values())

    def add_coordinatedcampaign(self, obj: CoordinatedCampaign) -> CoordinatedCampaign:
        with self.lock:
            self._coordinatedcampaigns[obj.campaign_id] = obj
            return obj

    def get_coordinatedcampaign(self, key: str) -> Optional[CoordinatedCampaign]:
        with self.lock:
            return self._coordinatedcampaigns.get(key)

    def list_coordinatedcampaigns(self) -> List[CoordinatedCampaign]:
        with self.lock:
            return list(self._coordinatedcampaigns.values())

    def add_tacticaldirective(self, obj: TacticalDirective) -> TacticalDirective:
        with self.lock:
            self._tacticaldirectives[obj.directive_id] = obj
            return obj

    def get_tacticaldirective(self, key: str) -> Optional[TacticalDirective]:
        with self.lock:
            return self._tacticaldirectives.get(key)

    def list_tacticaldirectives(self) -> List[TacticalDirective]:
        with self.lock:
            return list(self._tacticaldirectives.values())

    def add_commandtelemetry(self, obj: CommandTelemetry) -> CommandTelemetry:
        with self.lock:
            self._commandtelemetrys[obj.telemetry_id] = obj
            return obj

    def get_commandtelemetry(self, key: str) -> Optional[CommandTelemetry]:
        with self.lock:
            return self._commandtelemetrys.get(key)

    def list_commandtelemetrys(self) -> List[CommandTelemetry]:
        with self.lock:
            return list(self._commandtelemetrys.values())

_store_instance = None
def get_store() -> GlobalSecurityCommandNetworkStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = GlobalSecurityCommandNetworkStore()
    return _store_instance
