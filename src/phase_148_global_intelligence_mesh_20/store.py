"""
Thread-safe store for Global Intelligence Mesh 2.0
"""

import threading
from typing import Dict, List, Optional, Any
from .models import MeshNode, MeshTelemetry, SyncPolicy, DefenseState

class GlobalIntelligenceMesh20Store:
    def __init__(self):
        self.lock = threading.RLock()
        self._meshnodes: Dict[str, MeshNode] = {}
        self._meshtelemetrys: Dict[str, MeshTelemetry] = {}
        self._syncpolicys: Dict[str, SyncPolicy] = {}
        self._defensestates: Dict[str, DefenseState] = {}

    def add_meshnode(self, obj: MeshNode) -> MeshNode:
        with self.lock:
            self._meshnodes[obj.node_id] = obj
            return obj

    def get_meshnode(self, key: str) -> Optional[MeshNode]:
        with self.lock:
            return self._meshnodes.get(key)

    def list_meshnodes(self) -> List[MeshNode]:
        with self.lock:
            return list(self._meshnodes.values())

    def add_meshtelemetry(self, obj: MeshTelemetry) -> MeshTelemetry:
        with self.lock:
            self._meshtelemetrys[obj.telemetry_id] = obj
            return obj

    def get_meshtelemetry(self, key: str) -> Optional[MeshTelemetry]:
        with self.lock:
            return self._meshtelemetrys.get(key)

    def list_meshtelemetrys(self) -> List[MeshTelemetry]:
        with self.lock:
            return list(self._meshtelemetrys.values())

    def add_syncpolicy(self, obj: SyncPolicy) -> SyncPolicy:
        with self.lock:
            self._syncpolicys[obj.policy_id] = obj
            return obj

    def get_syncpolicy(self, key: str) -> Optional[SyncPolicy]:
        with self.lock:
            return self._syncpolicys.get(key)

    def list_syncpolicys(self) -> List[SyncPolicy]:
        with self.lock:
            return list(self._syncpolicys.values())

    def add_defensestate(self, obj: DefenseState) -> DefenseState:
        with self.lock:
            self._defensestates[obj.state_id] = obj
            return obj

    def get_defensestate(self, key: str) -> Optional[DefenseState]:
        with self.lock:
            return self._defensestates.get(key)

    def list_defensestates(self) -> List[DefenseState]:
        with self.lock:
            return list(self._defensestates.values())

_store_instance = None
def get_store() -> GlobalIntelligenceMesh20Store:
    global _store_instance
    if _store_instance is None:
        _store_instance = GlobalIntelligenceMesh20Store()
    return _store_instance
