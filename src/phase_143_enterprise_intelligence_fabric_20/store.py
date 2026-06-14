"""
Thread-safe store for Enterprise Intelligence Fabric 2.0
"""

import threading
from typing import Dict, List, Optional, Any
from .models import IntelligenceHub, DomainBridge, FabricSignal, UnifiedContext

class EnterpriseIntelligenceFabric20Store:
    def __init__(self):
        self.lock = threading.RLock()
        self._intelligencehubs: Dict[str, IntelligenceHub] = {}
        self._domainbridges: Dict[str, DomainBridge] = {}
        self._fabricsignals: Dict[str, FabricSignal] = {}
        self._unifiedcontexts: Dict[str, UnifiedContext] = {}

    def add_intelligencehub(self, obj: IntelligenceHub) -> IntelligenceHub:
        with self.lock:
            self._intelligencehubs[obj.hub_id] = obj
            return obj

    def get_intelligencehub(self, key: str) -> Optional[IntelligenceHub]:
        with self.lock:
            return self._intelligencehubs.get(key)

    def list_intelligencehubs(self) -> List[IntelligenceHub]:
        with self.lock:
            return list(self._intelligencehubs.values())

    def add_domainbridge(self, obj: DomainBridge) -> DomainBridge:
        with self.lock:
            self._domainbridges[obj.bridge_id] = obj
            return obj

    def get_domainbridge(self, key: str) -> Optional[DomainBridge]:
        with self.lock:
            return self._domainbridges.get(key)

    def list_domainbridges(self) -> List[DomainBridge]:
        with self.lock:
            return list(self._domainbridges.values())

    def add_fabricsignal(self, obj: FabricSignal) -> FabricSignal:
        with self.lock:
            self._fabricsignals[obj.signal_id] = obj
            return obj

    def get_fabricsignal(self, key: str) -> Optional[FabricSignal]:
        with self.lock:
            return self._fabricsignals.get(key)

    def list_fabricsignals(self) -> List[FabricSignal]:
        with self.lock:
            return list(self._fabricsignals.values())

    def add_unifiedcontext(self, obj: UnifiedContext) -> UnifiedContext:
        with self.lock:
            self._unifiedcontexts[obj.context_id] = obj
            return obj

    def get_unifiedcontext(self, key: str) -> Optional[UnifiedContext]:
        with self.lock:
            return self._unifiedcontexts.get(key)

    def list_unifiedcontexts(self) -> List[UnifiedContext]:
        with self.lock:
            return list(self._unifiedcontexts.values())

_store_instance = None
def get_store() -> EnterpriseIntelligenceFabric20Store:
    global _store_instance
    if _store_instance is None:
        _store_instance = EnterpriseIntelligenceFabric20Store()
    return _store_instance
