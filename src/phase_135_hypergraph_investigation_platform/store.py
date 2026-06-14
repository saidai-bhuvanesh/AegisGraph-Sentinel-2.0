"""
Thread-safe store for Hypergraph Investigation Platform
"""

import threading
from typing import Dict, List, Optional, Any
from .models import HyperEdge, HyperNode, InvestigationCluster, PatternMatch

class HypergraphInvestigationPlatformStore:
    def __init__(self):
        self.lock = threading.RLock()
        self._hyperedges: Dict[str, HyperEdge] = {}
        self._hypernodes: Dict[str, HyperNode] = {}
        self._investigationclusters: Dict[str, InvestigationCluster] = {}
        self._patternmatchs: Dict[str, PatternMatch] = {}

    def add_hyperedge(self, obj: HyperEdge) -> HyperEdge:
        with self.lock:
            self._hyperedges[obj.edge_id] = obj
            return obj

    def get_hyperedge(self, key: str) -> Optional[HyperEdge]:
        with self.lock:
            return self._hyperedges.get(key)

    def list_hyperedges(self) -> List[HyperEdge]:
        with self.lock:
            return list(self._hyperedges.values())

    def add_hypernode(self, obj: HyperNode) -> HyperNode:
        with self.lock:
            self._hypernodes[obj.node_id] = obj
            return obj

    def get_hypernode(self, key: str) -> Optional[HyperNode]:
        with self.lock:
            return self._hypernodes.get(key)

    def list_hypernodes(self) -> List[HyperNode]:
        with self.lock:
            return list(self._hypernodes.values())

    def add_investigationcluster(self, obj: InvestigationCluster) -> InvestigationCluster:
        with self.lock:
            self._investigationclusters[obj.cluster_id] = obj
            return obj

    def get_investigationcluster(self, key: str) -> Optional[InvestigationCluster]:
        with self.lock:
            return self._investigationclusters.get(key)

    def list_investigationclusters(self) -> List[InvestigationCluster]:
        with self.lock:
            return list(self._investigationclusters.values())

    def add_patternmatch(self, obj: PatternMatch) -> PatternMatch:
        with self.lock:
            self._patternmatchs[obj.match_id] = obj
            return obj

    def get_patternmatch(self, key: str) -> Optional[PatternMatch]:
        with self.lock:
            return self._patternmatchs.get(key)

    def list_patternmatchs(self) -> List[PatternMatch]:
        with self.lock:
            return list(self._patternmatchs.values())

_store_instance = None
def get_store() -> HypergraphInvestigationPlatformStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = HypergraphInvestigationPlatformStore()
    return _store_instance
