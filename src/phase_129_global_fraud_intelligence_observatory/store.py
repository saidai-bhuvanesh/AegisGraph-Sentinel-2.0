"""
Thread-safe store for Global Fraud Intelligence Observatory 2.0
"""

import threading
from typing import Dict, List, Optional, Any
from .models import FraudObservation, CampaignEvolution, FraudTrend, ScamEcosystem

class GlobalFraudIntelligenceObservatory20Store:
    def __init__(self):
        self.lock = threading.RLock()
        self._fraudobservations: Dict[str, FraudObservation] = {}
        self._campaignevolutions: Dict[str, CampaignEvolution] = {}
        self._fraudtrends: Dict[str, FraudTrend] = {}
        self._scamecosystems: Dict[str, ScamEcosystem] = {}

    def add_fraudobservation(self, obj: FraudObservation) -> FraudObservation:
        with self.lock:
            self._fraudobservations[obj.observation_id] = obj
            return obj

    def get_fraudobservation(self, key: str) -> Optional[FraudObservation]:
        with self.lock:
            return self._fraudobservations.get(key)

    def list_fraudobservations(self) -> List[FraudObservation]:
        with self.lock:
            return list(self._fraudobservations.values())

    def add_campaignevolution(self, obj: CampaignEvolution) -> CampaignEvolution:
        with self.lock:
            self._campaignevolutions[obj.campaign_id] = obj
            return obj

    def get_campaignevolution(self, key: str) -> Optional[CampaignEvolution]:
        with self.lock:
            return self._campaignevolutions.get(key)

    def list_campaignevolutions(self) -> List[CampaignEvolution]:
        with self.lock:
            return list(self._campaignevolutions.values())

    def add_fraudtrend(self, obj: FraudTrend) -> FraudTrend:
        with self.lock:
            self._fraudtrends[obj.trend_id] = obj
            return obj

    def get_fraudtrend(self, key: str) -> Optional[FraudTrend]:
        with self.lock:
            return self._fraudtrends.get(key)

    def list_fraudtrends(self) -> List[FraudTrend]:
        with self.lock:
            return list(self._fraudtrends.values())

    def add_scamecosystem(self, obj: ScamEcosystem) -> ScamEcosystem:
        with self.lock:
            self._scamecosystems[obj.ecosystem_id] = obj
            return obj

    def get_scamecosystem(self, key: str) -> Optional[ScamEcosystem]:
        with self.lock:
            return self._scamecosystems.get(key)

    def list_scamecosystems(self) -> List[ScamEcosystem]:
        with self.lock:
            return list(self._scamecosystems.values())

_store_instance = None
def get_store() -> GlobalFraudIntelligenceObservatory20Store:
    global _store_instance
    if _store_instance is None:
        _store_instance = GlobalFraudIntelligenceObservatory20Store()
    return _store_instance
