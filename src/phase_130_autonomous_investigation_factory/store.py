"""
Thread-safe store for Autonomous Investigation Factory
"""

import threading
from typing import Dict, List, Optional, Any
from .models import Investigation, Evidence, EntityCorrelation, CaseReport

class AutonomousInvestigationFactoryStore:
    def __init__(self):
        self.lock = threading.RLock()
        self._investigations: Dict[str, Investigation] = {}
        self._evidences: Dict[str, Evidence] = {}
        self._entitycorrelations: Dict[str, EntityCorrelation] = {}
        self._casereports: Dict[str, CaseReport] = {}

    def add_investigation(self, obj: Investigation) -> Investigation:
        with self.lock:
            self._investigations[obj.investigation_id] = obj
            return obj

    def get_investigation(self, key: str) -> Optional[Investigation]:
        with self.lock:
            return self._investigations.get(key)

    def list_investigations(self) -> List[Investigation]:
        with self.lock:
            return list(self._investigations.values())

    def add_evidence(self, obj: Evidence) -> Evidence:
        with self.lock:
            self._evidences[obj.evidence_id] = obj
            return obj

    def get_evidence(self, key: str) -> Optional[Evidence]:
        with self.lock:
            return self._evidences.get(key)

    def list_evidences(self) -> List[Evidence]:
        with self.lock:
            return list(self._evidences.values())

    def add_entitycorrelation(self, obj: EntityCorrelation) -> EntityCorrelation:
        with self.lock:
            self._entitycorrelations[obj.correlation_id] = obj
            return obj

    def get_entitycorrelation(self, key: str) -> Optional[EntityCorrelation]:
        with self.lock:
            return self._entitycorrelations.get(key)

    def list_entitycorrelations(self) -> List[EntityCorrelation]:
        with self.lock:
            return list(self._entitycorrelations.values())

    def add_casereport(self, obj: CaseReport) -> CaseReport:
        with self.lock:
            self._casereports[obj.report_id] = obj
            return obj

    def get_casereport(self, key: str) -> Optional[CaseReport]:
        with self.lock:
            return self._casereports.get(key)

    def list_casereports(self) -> List[CaseReport]:
        with self.lock:
            return list(self._casereports.values())

_store_instance = None
def get_store() -> AutonomousInvestigationFactoryStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = AutonomousInvestigationFactoryStore()
    return _store_instance
