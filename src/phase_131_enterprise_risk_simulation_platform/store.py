"""
Thread-safe store for Enterprise Risk Simulation Platform
"""

import threading
from typing import Dict, List, Optional, Any
from .models import Simulation, SimulationResult, ThreatVector, ForecastModel

class EnterpriseRiskSimulationPlatformStore:
    def __init__(self):
        self.lock = threading.RLock()
        self._simulations: Dict[str, Simulation] = {}
        self._simulationresults: Dict[str, SimulationResult] = {}
        self._threatvectors: Dict[str, ThreatVector] = {}
        self._forecastmodels: Dict[str, ForecastModel] = {}

    def add_simulation(self, obj: Simulation) -> Simulation:
        with self.lock:
            self._simulations[obj.simulation_id] = obj
            return obj

    def get_simulation(self, key: str) -> Optional[Simulation]:
        with self.lock:
            return self._simulations.get(key)

    def list_simulations(self) -> List[Simulation]:
        with self.lock:
            return list(self._simulations.values())

    def add_simulationresult(self, obj: SimulationResult) -> SimulationResult:
        with self.lock:
            self._simulationresults[obj.result_id] = obj
            return obj

    def get_simulationresult(self, key: str) -> Optional[SimulationResult]:
        with self.lock:
            return self._simulationresults.get(key)

    def list_simulationresults(self) -> List[SimulationResult]:
        with self.lock:
            return list(self._simulationresults.values())

    def add_threatvector(self, obj: ThreatVector) -> ThreatVector:
        with self.lock:
            self._threatvectors[obj.vector_id] = obj
            return obj

    def get_threatvector(self, key: str) -> Optional[ThreatVector]:
        with self.lock:
            return self._threatvectors.get(key)

    def list_threatvectors(self) -> List[ThreatVector]:
        with self.lock:
            return list(self._threatvectors.values())

    def add_forecastmodel(self, obj: ForecastModel) -> ForecastModel:
        with self.lock:
            self._forecastmodels[obj.model_id] = obj
            return obj

    def get_forecastmodel(self, key: str) -> Optional[ForecastModel]:
        with self.lock:
            return self._forecastmodels.get(key)

    def list_forecastmodels(self) -> List[ForecastModel]:
        with self.lock:
            return list(self._forecastmodels.values())

_store_instance = None
def get_store() -> EnterpriseRiskSimulationPlatformStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = EnterpriseRiskSimulationPlatformStore()
    return _store_instance
