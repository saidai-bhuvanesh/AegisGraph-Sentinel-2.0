"""
Thread-safe store for Enterprise Trust Graph
"""

import threading
from typing import Dict, List, Optional, Any
from .models import TrustEdge, TrustEntity, DeviceFingerprint, VendorRiskProfile

class EnterpriseTrustGraphStore:
    def __init__(self):
        self.lock = threading.RLock()
        self._trustedges: Dict[str, TrustEdge] = {}
        self._trustentitys: Dict[str, TrustEntity] = {}
        self._devicefingerprints: Dict[str, DeviceFingerprint] = {}
        self._vendorriskprofiles: Dict[str, VendorRiskProfile] = {}

    def add_trustedge(self, obj: TrustEdge) -> TrustEdge:
        with self.lock:
            self._trustedges[obj.edge_id] = obj
            return obj

    def get_trustedge(self, key: str) -> Optional[TrustEdge]:
        with self.lock:
            return self._trustedges.get(key)

    def list_trustedges(self) -> List[TrustEdge]:
        with self.lock:
            return list(self._trustedges.values())

    def add_trustentity(self, obj: TrustEntity) -> TrustEntity:
        with self.lock:
            self._trustentitys[obj.entity_id] = obj
            return obj

    def get_trustentity(self, key: str) -> Optional[TrustEntity]:
        with self.lock:
            return self._trustentitys.get(key)

    def list_trustentitys(self) -> List[TrustEntity]:
        with self.lock:
            return list(self._trustentitys.values())

    def add_devicefingerprint(self, obj: DeviceFingerprint) -> DeviceFingerprint:
        with self.lock:
            self._devicefingerprints[obj.device_id] = obj
            return obj

    def get_devicefingerprint(self, key: str) -> Optional[DeviceFingerprint]:
        with self.lock:
            return self._devicefingerprints.get(key)

    def list_devicefingerprints(self) -> List[DeviceFingerprint]:
        with self.lock:
            return list(self._devicefingerprints.values())

    def add_vendorriskprofile(self, obj: VendorRiskProfile) -> VendorRiskProfile:
        with self.lock:
            self._vendorriskprofiles[obj.vendor_id] = obj
            return obj

    def get_vendorriskprofile(self, key: str) -> Optional[VendorRiskProfile]:
        with self.lock:
            return self._vendorriskprofiles.get(key)

    def list_vendorriskprofiles(self) -> List[VendorRiskProfile]:
        with self.lock:
            return list(self._vendorriskprofiles.values())

_store_instance = None
def get_store() -> EnterpriseTrustGraphStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = EnterpriseTrustGraphStore()
    return _store_instance
