"""
Thread-safe store for Cross-Border Fraud Intelligence Platform
"""

import threading
from typing import Dict, List, Optional, Any
from .models import CrossBorderTx, TransnationalMuleRing, JurisdictionalReport, IntelExchangeLog

class CrossBorderFraudIntelligencePlatformStore:
    def __init__(self):
        self.lock = threading.RLock()
        self._crossbordertxs: Dict[str, CrossBorderTx] = {}
        self._transnationalmulerings: Dict[str, TransnationalMuleRing] = {}
        self._jurisdictionalreports: Dict[str, JurisdictionalReport] = {}
        self._intelexchangelogs: Dict[str, IntelExchangeLog] = {}

    def add_crossbordertx(self, obj: CrossBorderTx) -> CrossBorderTx:
        with self.lock:
            self._crossbordertxs[obj.tx_id] = obj
            return obj

    def get_crossbordertx(self, key: str) -> Optional[CrossBorderTx]:
        with self.lock:
            return self._crossbordertxs.get(key)

    def list_crossbordertxs(self) -> List[CrossBorderTx]:
        with self.lock:
            return list(self._crossbordertxs.values())

    def add_transnationalmulering(self, obj: TransnationalMuleRing) -> TransnationalMuleRing:
        with self.lock:
            self._transnationalmulerings[obj.ring_id] = obj
            return obj

    def get_transnationalmulering(self, key: str) -> Optional[TransnationalMuleRing]:
        with self.lock:
            return self._transnationalmulerings.get(key)

    def list_transnationalmulerings(self) -> List[TransnationalMuleRing]:
        with self.lock:
            return list(self._transnationalmulerings.values())

    def add_jurisdictionalreport(self, obj: JurisdictionalReport) -> JurisdictionalReport:
        with self.lock:
            self._jurisdictionalreports[obj.report_id] = obj
            return obj

    def get_jurisdictionalreport(self, key: str) -> Optional[JurisdictionalReport]:
        with self.lock:
            return self._jurisdictionalreports.get(key)

    def list_jurisdictionalreports(self) -> List[JurisdictionalReport]:
        with self.lock:
            return list(self._jurisdictionalreports.values())

    def add_intelexchangelog(self, obj: IntelExchangeLog) -> IntelExchangeLog:
        with self.lock:
            self._intelexchangelogs[obj.log_id] = obj
            return obj

    def get_intelexchangelog(self, key: str) -> Optional[IntelExchangeLog]:
        with self.lock:
            return self._intelexchangelogs.get(key)

    def list_intelexchangelogs(self) -> List[IntelExchangeLog]:
        with self.lock:
            return list(self._intelexchangelogs.values())

_store_instance = None
def get_store() -> CrossBorderFraudIntelligencePlatformStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = CrossBorderFraudIntelligencePlatformStore()
    return _store_instance
