"""
Thread-safe store for Global AML Intelligence Platform
"""

import threading
from typing import Dict, List, Optional, Any
from .models import SanctionsList, AmlAlert, SanctionsMatch, AmlCase

class GlobalAMLIntelligencePlatformStore:
    def __init__(self):
        self.lock = threading.RLock()
        self._sanctionslists: Dict[str, SanctionsList] = {}
        self._amlalerts: Dict[str, AmlAlert] = {}
        self._sanctionsmatchs: Dict[str, SanctionsMatch] = {}
        self._amlcases: Dict[str, AmlCase] = {}

    def add_sanctionslist(self, obj: SanctionsList) -> SanctionsList:
        with self.lock:
            self._sanctionslists[obj.list_id] = obj
            return obj

    def get_sanctionslist(self, key: str) -> Optional[SanctionsList]:
        with self.lock:
            return self._sanctionslists.get(key)

    def list_sanctionslists(self) -> List[SanctionsList]:
        with self.lock:
            return list(self._sanctionslists.values())

    def add_amlalert(self, obj: AmlAlert) -> AmlAlert:
        with self.lock:
            self._amlalerts[obj.alert_id] = obj
            return obj

    def get_amlalert(self, key: str) -> Optional[AmlAlert]:
        with self.lock:
            return self._amlalerts.get(key)

    def list_amlalerts(self) -> List[AmlAlert]:
        with self.lock:
            return list(self._amlalerts.values())

    def add_sanctionsmatch(self, obj: SanctionsMatch) -> SanctionsMatch:
        with self.lock:
            self._sanctionsmatchs[obj.match_id] = obj
            return obj

    def get_sanctionsmatch(self, key: str) -> Optional[SanctionsMatch]:
        with self.lock:
            return self._sanctionsmatchs.get(key)

    def list_sanctionsmatchs(self) -> List[SanctionsMatch]:
        with self.lock:
            return list(self._sanctionsmatchs.values())

    def add_amlcase(self, obj: AmlCase) -> AmlCase:
        with self.lock:
            self._amlcases[obj.case_id] = obj
            return obj

    def get_amlcase(self, key: str) -> Optional[AmlCase]:
        with self.lock:
            return self._amlcases.get(key)

    def list_amlcases(self) -> List[AmlCase]:
        with self.lock:
            return list(self._amlcases.values())

_store_instance = None
def get_store() -> GlobalAMLIntelligencePlatformStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = GlobalAMLIntelligencePlatformStore()
    return _store_instance
