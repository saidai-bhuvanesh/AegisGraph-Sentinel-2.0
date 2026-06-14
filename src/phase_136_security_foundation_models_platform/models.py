"""
Data models for Security Foundation Models Platform
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

@dataclass
class FoundationModel:
    model_id: str = ""
    name: str = ""
    version: str = ""
    task_type: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "name": self.name,
            "version": self.version,
            "task_type": self.task_type,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FoundationModel":
        return cls(
            model_id=data.get("model_id"),
            name=data.get("name"),
            version=data.get("version"),
            task_type=data.get("task_type"),
        )

@dataclass
class ModelTrainingJob:
    job_id: str = ""
    model_id: str = ""
    dataset_path: str = ""
    status: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "model_id": self.model_id,
            "dataset_path": self.dataset_path,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ModelTrainingJob":
        return cls(
            job_id=data.get("job_id"),
            model_id=data.get("model_id"),
            dataset_path=data.get("dataset_path"),
            status=data.get("status"),
        )

@dataclass
class EvaluationReport:
    report_id: str = ""
    model_id: str = ""
    precision: float = 0.0
    recall: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "model_id": self.model_id,
            "precision": self.precision,
            "recall": self.recall,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EvaluationReport":
        return cls(
            report_id=data.get("report_id"),
            model_id=data.get("model_id"),
            precision=data.get("precision"),
            recall=data.get("recall"),
        )

@dataclass
class DeploymentConfig:
    config_id: str = ""
    replicas: int = 0
    endpoint: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "config_id": self.config_id,
            "replicas": self.replicas,
            "endpoint": self.endpoint,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeploymentConfig":
        return cls(
            config_id=data.get("config_id"),
            replicas=data.get("replicas"),
            endpoint=data.get("endpoint"),
        )

