"""
Thread-safe store for Security Decision Intelligence Network
"""

import threading
from typing import Dict, List, Optional, Any
from .models import RecommendationEngine, DecisionScenario, ImpactForecast, DecisionAudit

class SecurityDecisionIntelligenceNetworkStore:
    def __init__(self):
        self.lock = threading.RLock()
        self._recommendationengines: Dict[str, RecommendationEngine] = {}
        self._decisionscenarios: Dict[str, DecisionScenario] = {}
        self._impactforecasts: Dict[str, ImpactForecast] = {}
        self._decisionaudits: Dict[str, DecisionAudit] = {}

    def add_recommendationengine(self, obj: RecommendationEngine) -> RecommendationEngine:
        with self.lock:
            self._recommendationengines[obj.engine_id] = obj
            return obj

    def get_recommendationengine(self, key: str) -> Optional[RecommendationEngine]:
        with self.lock:
            return self._recommendationengines.get(key)

    def list_recommendationengines(self) -> List[RecommendationEngine]:
        with self.lock:
            return list(self._recommendationengines.values())

    def add_decisionscenario(self, obj: DecisionScenario) -> DecisionScenario:
        with self.lock:
            self._decisionscenarios[obj.scenario_id] = obj
            return obj

    def get_decisionscenario(self, key: str) -> Optional[DecisionScenario]:
        with self.lock:
            return self._decisionscenarios.get(key)

    def list_decisionscenarios(self) -> List[DecisionScenario]:
        with self.lock:
            return list(self._decisionscenarios.values())

    def add_impactforecast(self, obj: ImpactForecast) -> ImpactForecast:
        with self.lock:
            self._impactforecasts[obj.forecast_id] = obj
            return obj

    def get_impactforecast(self, key: str) -> Optional[ImpactForecast]:
        with self.lock:
            return self._impactforecasts.get(key)

    def list_impactforecasts(self) -> List[ImpactForecast]:
        with self.lock:
            return list(self._impactforecasts.values())

    def add_decisionaudit(self, obj: DecisionAudit) -> DecisionAudit:
        with self.lock:
            self._decisionaudits[obj.audit_id] = obj
            return obj

    def get_decisionaudit(self, key: str) -> Optional[DecisionAudit]:
        with self.lock:
            return self._decisionaudits.get(key)

    def list_decisionaudits(self) -> List[DecisionAudit]:
        with self.lock:
            return list(self._decisionaudits.values())

_store_instance = None
def get_store() -> SecurityDecisionIntelligenceNetworkStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = SecurityDecisionIntelligenceNetworkStore()
    return _store_instance
