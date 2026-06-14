"""
Thread-safe store for Enterprise Attack Path Intelligence Platform
"""

import threading
from typing import Dict, List, Optional, Any
from .models import AttackPath, LateralMovement, AssetExposure, BreachScenario

class EnterpriseAttackPathIntelligencePlatformStore:
    def __init__(self):
        self.lock = threading.RLock()
        self._attackpaths: Dict[str, AttackPath] = {}
        self._lateralmovements: Dict[str, LateralMovement] = {}
        self._assetexposures: Dict[str, AssetExposure] = {}
        self._breachscenarios: Dict[str, BreachScenario] = {}

    def add_attackpath(self, obj: AttackPath) -> AttackPath:
        with self.lock:
            self._attackpaths[obj.path_id] = obj
            return obj

    def get_attackpath(self, key: str) -> Optional[AttackPath]:
        with self.lock:
            return self._attackpaths.get(key)

    def list_attackpaths(self) -> List[AttackPath]:
        with self.lock:
            return list(self._attackpaths.values())

    def add_lateralmovement(self, obj: LateralMovement) -> LateralMovement:
        with self.lock:
            self._lateralmovements[obj.movement_id] = obj
            return obj

    def get_lateralmovement(self, key: str) -> Optional[LateralMovement]:
        with self.lock:
            return self._lateralmovements.get(key)

    def list_lateralmovements(self) -> List[LateralMovement]:
        with self.lock:
            return list(self._lateralmovements.values())

    def add_assetexposure(self, obj: AssetExposure) -> AssetExposure:
        with self.lock:
            self._assetexposures[obj.exposure_id] = obj
            return obj

    def get_assetexposure(self, key: str) -> Optional[AssetExposure]:
        with self.lock:
            return self._assetexposures.get(key)

    def list_assetexposures(self) -> List[AssetExposure]:
        with self.lock:
            return list(self._assetexposures.values())

    def add_breachscenario(self, obj: BreachScenario) -> BreachScenario:
        with self.lock:
            self._breachscenarios[obj.scenario_id] = obj
            return obj

    def get_breachscenario(self, key: str) -> Optional[BreachScenario]:
        with self.lock:
            return self._breachscenarios.get(key)

    def list_breachscenarios(self) -> List[BreachScenario]:
        with self.lock:
            return list(self._breachscenarios.values())

_store_instance = None
def get_store() -> EnterpriseAttackPathIntelligencePlatformStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = EnterpriseAttackPathIntelligencePlatformStore()
    return _store_instance
