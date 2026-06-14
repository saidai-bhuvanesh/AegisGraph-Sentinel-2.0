"""
Thread-safe store for Global Intelligence Exchange Network
"""

import threading
from typing import Dict, List, Optional, Any
from .models import ExchangeNode, IntelligencePayload, SharingPolicy, ExchangeAudit

class GlobalIntelligenceExchangeNetworkStore:
    def __init__(self):
        self.lock = threading.RLock()
        self._exchangenodes: Dict[str, ExchangeNode] = {}
        self._intelligencepayloads: Dict[str, IntelligencePayload] = {}
        self._sharingpolicys: Dict[str, SharingPolicy] = {}
        self._exchangeaudits: Dict[str, ExchangeAudit] = {}

    def add_exchangenode(self, obj: ExchangeNode) -> ExchangeNode:
        with self.lock:
            self._exchangenodes[obj.node_id] = obj
            return obj

    def get_exchangenode(self, key: str) -> Optional[ExchangeNode]:
        with self.lock:
            return self._exchangenodes.get(key)

    def list_exchangenodes(self) -> List[ExchangeNode]:
        with self.lock:
            return list(self._exchangenodes.values())

    def add_intelligencepayload(self, obj: IntelligencePayload) -> IntelligencePayload:
        with self.lock:
            self._intelligencepayloads[obj.payload_id] = obj
            return obj

    def get_intelligencepayload(self, key: str) -> Optional[IntelligencePayload]:
        with self.lock:
            return self._intelligencepayloads.get(key)

    def list_intelligencepayloads(self) -> List[IntelligencePayload]:
        with self.lock:
            return list(self._intelligencepayloads.values())

    def add_sharingpolicy(self, obj: SharingPolicy) -> SharingPolicy:
        with self.lock:
            self._sharingpolicys[obj.policy_id] = obj
            return obj

    def get_sharingpolicy(self, key: str) -> Optional[SharingPolicy]:
        with self.lock:
            return self._sharingpolicys.get(key)

    def list_sharingpolicys(self) -> List[SharingPolicy]:
        with self.lock:
            return list(self._sharingpolicys.values())

    def add_exchangeaudit(self, obj: ExchangeAudit) -> ExchangeAudit:
        with self.lock:
            self._exchangeaudits[obj.audit_id] = obj
            return obj

    def get_exchangeaudit(self, key: str) -> Optional[ExchangeAudit]:
        with self.lock:
            return self._exchangeaudits.get(key)

    def list_exchangeaudits(self) -> List[ExchangeAudit]:
        with self.lock:
            return list(self._exchangeaudits.values())

_store_instance = None
def get_store() -> GlobalIntelligenceExchangeNetworkStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = GlobalIntelligenceExchangeNetworkStore()
    return _store_instance
