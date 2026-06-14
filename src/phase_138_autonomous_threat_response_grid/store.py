"""
Thread-safe store for Autonomous Threat Response Grid
"""

import threading
from typing import Dict, List, Optional, Any
from .models import ThreatSignal, PlaybookAction, GridOrchestrator, RemediationResult

class AutonomousThreatResponseGridStore:
    def __init__(self):
        self.lock = threading.RLock()
        self._threatsignals: Dict[str, ThreatSignal] = {}
        self._playbookactions: Dict[str, PlaybookAction] = {}
        self._gridorchestrators: Dict[str, GridOrchestrator] = {}
        self._remediationresults: Dict[str, RemediationResult] = {}

    def add_threatsignal(self, obj: ThreatSignal) -> ThreatSignal:
        with self.lock:
            self._threatsignals[obj.signal_id] = obj
            return obj

    def get_threatsignal(self, key: str) -> Optional[ThreatSignal]:
        with self.lock:
            return self._threatsignals.get(key)

    def list_threatsignals(self) -> List[ThreatSignal]:
        with self.lock:
            return list(self._threatsignals.values())

    def add_playbookaction(self, obj: PlaybookAction) -> PlaybookAction:
        with self.lock:
            self._playbookactions[obj.action_id] = obj
            return obj

    def get_playbookaction(self, key: str) -> Optional[PlaybookAction]:
        with self.lock:
            return self._playbookactions.get(key)

    def list_playbookactions(self) -> List[PlaybookAction]:
        with self.lock:
            return list(self._playbookactions.values())

    def add_gridorchestrator(self, obj: GridOrchestrator) -> GridOrchestrator:
        with self.lock:
            self._gridorchestrators[obj.orchestrator_id] = obj
            return obj

    def get_gridorchestrator(self, key: str) -> Optional[GridOrchestrator]:
        with self.lock:
            return self._gridorchestrators.get(key)

    def list_gridorchestrators(self) -> List[GridOrchestrator]:
        with self.lock:
            return list(self._gridorchestrators.values())

    def add_remediationresult(self, obj: RemediationResult) -> RemediationResult:
        with self.lock:
            self._remediationresults[obj.remediation_id] = obj
            return obj

    def get_remediationresult(self, key: str) -> Optional[RemediationResult]:
        with self.lock:
            return self._remediationresults.get(key)

    def list_remediationresults(self) -> List[RemediationResult]:
        with self.lock:
            return list(self._remediationresults.values())

_store_instance = None
def get_store() -> AutonomousThreatResponseGridStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = AutonomousThreatResponseGridStore()
    return _store_instance
