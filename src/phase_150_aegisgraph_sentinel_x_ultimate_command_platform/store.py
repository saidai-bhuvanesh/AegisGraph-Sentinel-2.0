"""
Thread-safe store for AegisGraph Sentinel X Ultimate Command Platform
"""

import threading
from typing import Dict, List, Optional, Any
from .models import PlatformStatus, EcosystemConfig, UltimateReport, OrchestratorEvent

class AegisGraphSentinelXUltimateCommandPlatformStore:
    def __init__(self):
        self.lock = threading.RLock()
        self._platformstatuss: Dict[str, PlatformStatus] = {}
        self._ecosystemconfigs: Dict[str, EcosystemConfig] = {}
        self._ultimatereports: Dict[str, UltimateReport] = {}
        self._orchestratorevents: Dict[str, OrchestratorEvent] = {}

    def add_platformstatus(self, obj: PlatformStatus) -> PlatformStatus:
        with self.lock:
            self._platformstatuss[obj.platform_id] = obj
            return obj

    def get_platformstatus(self, key: str) -> Optional[PlatformStatus]:
        with self.lock:
            return self._platformstatuss.get(key)

    def list_platformstatuss(self) -> List[PlatformStatus]:
        with self.lock:
            return list(self._platformstatuss.values())

    def add_ecosystemconfig(self, obj: EcosystemConfig) -> EcosystemConfig:
        with self.lock:
            self._ecosystemconfigs[obj.config_id] = obj
            return obj

    def get_ecosystemconfig(self, key: str) -> Optional[EcosystemConfig]:
        with self.lock:
            return self._ecosystemconfigs.get(key)

    def list_ecosystemconfigs(self) -> List[EcosystemConfig]:
        with self.lock:
            return list(self._ecosystemconfigs.values())

    def add_ultimatereport(self, obj: UltimateReport) -> UltimateReport:
        with self.lock:
            self._ultimatereports[obj.report_id] = obj
            return obj

    def get_ultimatereport(self, key: str) -> Optional[UltimateReport]:
        with self.lock:
            return self._ultimatereports.get(key)

    def list_ultimatereports(self) -> List[UltimateReport]:
        with self.lock:
            return list(self._ultimatereports.values())

    def add_orchestratorevent(self, obj: OrchestratorEvent) -> OrchestratorEvent:
        with self.lock:
            self._orchestratorevents[obj.event_id] = obj
            return obj

    def get_orchestratorevent(self, key: str) -> Optional[OrchestratorEvent]:
        with self.lock:
            return self._orchestratorevents.get(key)

    def list_orchestratorevents(self) -> List[OrchestratorEvent]:
        with self.lock:
            return list(self._orchestratorevents.values())

_store_instance = None
def get_store() -> AegisGraphSentinelXUltimateCommandPlatformStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = AegisGraphSentinelXUltimateCommandPlatformStore()
    return _store_instance
