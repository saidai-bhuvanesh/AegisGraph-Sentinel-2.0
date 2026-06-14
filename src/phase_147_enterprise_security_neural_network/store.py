"""
Thread-safe store for Enterprise Security Neural Network
"""

import threading
from typing import Dict, List, Optional, Any
from .models import NeuralLayer, NetworkConfig, PredictionOutput, TrainingMetrics

class EnterpriseSecurityNeuralNetworkStore:
    def __init__(self):
        self.lock = threading.RLock()
        self._neurallayers: Dict[str, NeuralLayer] = {}
        self._networkconfigs: Dict[str, NetworkConfig] = {}
        self._predictionoutputs: Dict[str, PredictionOutput] = {}
        self._trainingmetricss: Dict[str, TrainingMetrics] = {}

    def add_neurallayer(self, obj: NeuralLayer) -> NeuralLayer:
        with self.lock:
            self._neurallayers[obj.layer_id] = obj
            return obj

    def get_neurallayer(self, key: str) -> Optional[NeuralLayer]:
        with self.lock:
            return self._neurallayers.get(key)

    def list_neurallayers(self) -> List[NeuralLayer]:
        with self.lock:
            return list(self._neurallayers.values())

    def add_networkconfig(self, obj: NetworkConfig) -> NetworkConfig:
        with self.lock:
            self._networkconfigs[obj.config_id] = obj
            return obj

    def get_networkconfig(self, key: str) -> Optional[NetworkConfig]:
        with self.lock:
            return self._networkconfigs.get(key)

    def list_networkconfigs(self) -> List[NetworkConfig]:
        with self.lock:
            return list(self._networkconfigs.values())

    def add_predictionoutput(self, obj: PredictionOutput) -> PredictionOutput:
        with self.lock:
            self._predictionoutputs[obj.prediction_id] = obj
            return obj

    def get_predictionoutput(self, key: str) -> Optional[PredictionOutput]:
        with self.lock:
            return self._predictionoutputs.get(key)

    def list_predictionoutputs(self) -> List[PredictionOutput]:
        with self.lock:
            return list(self._predictionoutputs.values())

    def add_trainingmetrics(self, obj: TrainingMetrics) -> TrainingMetrics:
        with self.lock:
            self._trainingmetricss[obj.metrics_id] = obj
            return obj

    def get_trainingmetrics(self, key: str) -> Optional[TrainingMetrics]:
        with self.lock:
            return self._trainingmetricss.get(key)

    def list_trainingmetricss(self) -> List[TrainingMetrics]:
        with self.lock:
            return list(self._trainingmetricss.values())

_store_instance = None
def get_store() -> EnterpriseSecurityNeuralNetworkStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = EnterpriseSecurityNeuralNetworkStore()
    return _store_instance
