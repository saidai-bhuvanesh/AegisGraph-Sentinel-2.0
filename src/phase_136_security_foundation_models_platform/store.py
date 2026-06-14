"""
Thread-safe store for Security Foundation Models Platform
"""

import threading
from typing import Dict, List, Optional, Any
from .models import FoundationModel, ModelTrainingJob, EvaluationReport, DeploymentConfig

class SecurityFoundationModelsPlatformStore:
    def __init__(self):
        self.lock = threading.RLock()
        self._foundationmodels: Dict[str, FoundationModel] = {}
        self._modeltrainingjobs: Dict[str, ModelTrainingJob] = {}
        self._evaluationreports: Dict[str, EvaluationReport] = {}
        self._deploymentconfigs: Dict[str, DeploymentConfig] = {}

    def add_foundationmodel(self, obj: FoundationModel) -> FoundationModel:
        with self.lock:
            self._foundationmodels[obj.model_id] = obj
            return obj

    def get_foundationmodel(self, key: str) -> Optional[FoundationModel]:
        with self.lock:
            return self._foundationmodels.get(key)

    def list_foundationmodels(self) -> List[FoundationModel]:
        with self.lock:
            return list(self._foundationmodels.values())

    def add_modeltrainingjob(self, obj: ModelTrainingJob) -> ModelTrainingJob:
        with self.lock:
            self._modeltrainingjobs[obj.job_id] = obj
            return obj

    def get_modeltrainingjob(self, key: str) -> Optional[ModelTrainingJob]:
        with self.lock:
            return self._modeltrainingjobs.get(key)

    def list_modeltrainingjobs(self) -> List[ModelTrainingJob]:
        with self.lock:
            return list(self._modeltrainingjobs.values())

    def add_evaluationreport(self, obj: EvaluationReport) -> EvaluationReport:
        with self.lock:
            self._evaluationreports[obj.report_id] = obj
            return obj

    def get_evaluationreport(self, key: str) -> Optional[EvaluationReport]:
        with self.lock:
            return self._evaluationreports.get(key)

    def list_evaluationreports(self) -> List[EvaluationReport]:
        with self.lock:
            return list(self._evaluationreports.values())

    def add_deploymentconfig(self, obj: DeploymentConfig) -> DeploymentConfig:
        with self.lock:
            self._deploymentconfigs[obj.config_id] = obj
            return obj

    def get_deploymentconfig(self, key: str) -> Optional[DeploymentConfig]:
        with self.lock:
            return self._deploymentconfigs.get(key)

    def list_deploymentconfigs(self) -> List[DeploymentConfig]:
        with self.lock:
            return list(self._deploymentconfigs.values())

_store_instance = None
def get_store() -> SecurityFoundationModelsPlatformStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = SecurityFoundationModelsPlatformStore()
    return _store_instance
