"""
Thread-safe store for Enterprise Security Twin Network
"""

import threading
from typing import Dict, List, Optional, Any
from .models import DigitalTwin, EntityState, SynchronizationJob, RiskForecast

class EnterpriseSecurityTwinNetworkStore:
    def __init__(self):
        self.lock = threading.RLock()
        self._digitaltwins: Dict[str, DigitalTwin] = {}
        self._entitystates: Dict[str, EntityState] = {}
        self._synchronizationjobs: Dict[str, SynchronizationJob] = {}
        self._riskforecasts: Dict[str, RiskForecast] = {}

    def add_digitaltwin(self, obj: DigitalTwin) -> DigitalTwin:
        with self.lock:
            self._digitaltwins[obj.twin_id] = obj
            return obj

    def get_digitaltwin(self, key: str) -> Optional[DigitalTwin]:
        with self.lock:
            return self._digitaltwins.get(key)

    def list_digitaltwins(self) -> List[DigitalTwin]:
        with self.lock:
            return list(self._digitaltwins.values())

    def add_entitystate(self, obj: EntityState) -> EntityState:
        with self.lock:
            self._entitystates[obj.state_id] = obj
            return obj

    def get_entitystate(self, key: str) -> Optional[EntityState]:
        with self.lock:
            return self._entitystates.get(key)

    def list_entitystates(self) -> List[EntityState]:
        with self.lock:
            return list(self._entitystates.values())

    def add_synchronizationjob(self, obj: SynchronizationJob) -> SynchronizationJob:
        with self.lock:
            self._synchronizationjobs[obj.job_id] = obj
            return obj

    def get_synchronizationjob(self, key: str) -> Optional[SynchronizationJob]:
        with self.lock:
            return self._synchronizationjobs.get(key)

    def list_synchronizationjobs(self) -> List[SynchronizationJob]:
        with self.lock:
            return list(self._synchronizationjobs.values())

    def add_riskforecast(self, obj: RiskForecast) -> RiskForecast:
        with self.lock:
            self._riskforecasts[obj.forecast_id] = obj
            return obj

    def get_riskforecast(self, key: str) -> Optional[RiskForecast]:
        with self.lock:
            return self._riskforecasts.get(key)

    def list_riskforecasts(self) -> List[RiskForecast]:
        with self.lock:
            return list(self._riskforecasts.values())

_store_instance = None
def get_store() -> EnterpriseSecurityTwinNetworkStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = EnterpriseSecurityTwinNetworkStore()
    return _store_instance
