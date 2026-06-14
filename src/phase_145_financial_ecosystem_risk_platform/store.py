"""
Thread-safe store for Financial Ecosystem Risk Platform
"""

import threading
from typing import Dict, List, Optional, Any
from .models import EcosystemNode, InterbankTx, SystemicAnomaly, RiskExposureReport

class FinancialEcosystemRiskPlatformStore:
    def __init__(self):
        self.lock = threading.RLock()
        self._ecosystemnodes: Dict[str, EcosystemNode] = {}
        self._interbanktxs: Dict[str, InterbankTx] = {}
        self._systemicanomalys: Dict[str, SystemicAnomaly] = {}
        self._riskexposurereports: Dict[str, RiskExposureReport] = {}

    def add_ecosystemnode(self, obj: EcosystemNode) -> EcosystemNode:
        with self.lock:
            self._ecosystemnodes[obj.node_id] = obj
            return obj

    def get_ecosystemnode(self, key: str) -> Optional[EcosystemNode]:
        with self.lock:
            return self._ecosystemnodes.get(key)

    def list_ecosystemnodes(self) -> List[EcosystemNode]:
        with self.lock:
            return list(self._ecosystemnodes.values())

    def add_interbanktx(self, obj: InterbankTx) -> InterbankTx:
        with self.lock:
            self._interbanktxs[obj.tx_id] = obj
            return obj

    def get_interbanktx(self, key: str) -> Optional[InterbankTx]:
        with self.lock:
            return self._interbanktxs.get(key)

    def list_interbanktxs(self) -> List[InterbankTx]:
        with self.lock:
            return list(self._interbanktxs.values())

    def add_systemicanomaly(self, obj: SystemicAnomaly) -> SystemicAnomaly:
        with self.lock:
            self._systemicanomalys[obj.anomaly_id] = obj
            return obj

    def get_systemicanomaly(self, key: str) -> Optional[SystemicAnomaly]:
        with self.lock:
            return self._systemicanomalys.get(key)

    def list_systemicanomalys(self) -> List[SystemicAnomaly]:
        with self.lock:
            return list(self._systemicanomalys.values())

    def add_riskexposurereport(self, obj: RiskExposureReport) -> RiskExposureReport:
        with self.lock:
            self._riskexposurereports[obj.report_id] = obj
            return obj

    def get_riskexposurereport(self, key: str) -> Optional[RiskExposureReport]:
        with self.lock:
            return self._riskexposurereports.get(key)

    def list_riskexposurereports(self) -> List[RiskExposureReport]:
        with self.lock:
            return list(self._riskexposurereports.values())

_store_instance = None
def get_store() -> FinancialEcosystemRiskPlatformStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = FinancialEcosystemRiskPlatformStore()
    return _store_instance
