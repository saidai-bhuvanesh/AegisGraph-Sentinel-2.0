"""
Thread-safe store for Autonomous Security Economy Platform
"""

import threading
from typing import Dict, List, Optional, Any
from .models import EconomicMetric, CostAnalysis, RoiForecast, LossPreventionAudit

class AutonomousSecurityEconomyPlatformStore:
    def __init__(self):
        self.lock = threading.RLock()
        self._economicmetrics: Dict[str, EconomicMetric] = {}
        self._costanalysiss: Dict[str, CostAnalysis] = {}
        self._roiforecasts: Dict[str, RoiForecast] = {}
        self._losspreventionaudits: Dict[str, LossPreventionAudit] = {}

    def add_economicmetric(self, obj: EconomicMetric) -> EconomicMetric:
        with self.lock:
            self._economicmetrics[obj.metric_id] = obj
            return obj

    def get_economicmetric(self, key: str) -> Optional[EconomicMetric]:
        with self.lock:
            return self._economicmetrics.get(key)

    def list_economicmetrics(self) -> List[EconomicMetric]:
        with self.lock:
            return list(self._economicmetrics.values())

    def add_costanalysis(self, obj: CostAnalysis) -> CostAnalysis:
        with self.lock:
            self._costanalysiss[obj.analysis_id] = obj
            return obj

    def get_costanalysis(self, key: str) -> Optional[CostAnalysis]:
        with self.lock:
            return self._costanalysiss.get(key)

    def list_costanalysiss(self) -> List[CostAnalysis]:
        with self.lock:
            return list(self._costanalysiss.values())

    def add_roiforecast(self, obj: RoiForecast) -> RoiForecast:
        with self.lock:
            self._roiforecasts[obj.forecast_id] = obj
            return obj

    def get_roiforecast(self, key: str) -> Optional[RoiForecast]:
        with self.lock:
            return self._roiforecasts.get(key)

    def list_roiforecasts(self) -> List[RoiForecast]:
        with self.lock:
            return list(self._roiforecasts.values())

    def add_losspreventionaudit(self, obj: LossPreventionAudit) -> LossPreventionAudit:
        with self.lock:
            self._losspreventionaudits[obj.audit_id] = obj
            return obj

    def get_losspreventionaudit(self, key: str) -> Optional[LossPreventionAudit]:
        with self.lock:
            return self._losspreventionaudits.get(key)

    def list_losspreventionaudits(self) -> List[LossPreventionAudit]:
        with self.lock:
            return list(self._losspreventionaudits.values())

_store_instance = None
def get_store() -> AutonomousSecurityEconomyPlatformStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = AutonomousSecurityEconomyPlatformStore()
    return _store_instance
