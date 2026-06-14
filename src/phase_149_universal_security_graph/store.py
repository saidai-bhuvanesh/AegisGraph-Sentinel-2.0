"""
Thread-safe store for Universal Security Graph
"""

import threading
from typing import Dict, List, Optional, Any
from .models import UnifiedNode, UnifiedEdge, USGGraph, CrossDomainCorrelation

class UniversalSecurityGraphStore:
    def __init__(self):
        self.lock = threading.RLock()
        self._unifiednodes: Dict[str, UnifiedNode] = {}
        self._unifiededges: Dict[str, UnifiedEdge] = {}
        self._usggraphs: Dict[str, USGGraph] = {}
        self._crossdomaincorrelations: Dict[str, CrossDomainCorrelation] = {}

    def add_unifiednode(self, obj: UnifiedNode) -> UnifiedNode:
        with self.lock:
            self._unifiednodes[obj.node_id] = obj
            return obj

    def get_unifiednode(self, key: str) -> Optional[UnifiedNode]:
        with self.lock:
            return self._unifiednodes.get(key)

    def list_unifiednodes(self) -> List[UnifiedNode]:
        with self.lock:
            return list(self._unifiednodes.values())

    def add_unifiededge(self, obj: UnifiedEdge) -> UnifiedEdge:
        with self.lock:
            self._unifiededges[obj.edge_id] = obj
            return obj

    def get_unifiededge(self, key: str) -> Optional[UnifiedEdge]:
        with self.lock:
            return self._unifiededges.get(key)

    def list_unifiededges(self) -> List[UnifiedEdge]:
        with self.lock:
            return list(self._unifiededges.values())

    def add_usggraph(self, obj: USGGraph) -> USGGraph:
        with self.lock:
            self._usggraphs[obj.graph_id] = obj
            return obj

    def get_usggraph(self, key: str) -> Optional[USGGraph]:
        with self.lock:
            return self._usggraphs.get(key)

    def list_usggraphs(self) -> List[USGGraph]:
        with self.lock:
            return list(self._usggraphs.values())

    def add_crossdomaincorrelation(self, obj: CrossDomainCorrelation) -> CrossDomainCorrelation:
        with self.lock:
            self._crossdomaincorrelations[obj.correlation_id] = obj
            return obj

    def get_crossdomaincorrelation(self, key: str) -> Optional[CrossDomainCorrelation]:
        with self.lock:
            return self._crossdomaincorrelations.get(key)

    def list_crossdomaincorrelations(self) -> List[CrossDomainCorrelation]:
        with self.lock:
            return list(self._crossdomaincorrelations.values())

_store_instance = None
def get_store() -> UniversalSecurityGraphStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = UniversalSecurityGraphStore()
    return _store_instance
