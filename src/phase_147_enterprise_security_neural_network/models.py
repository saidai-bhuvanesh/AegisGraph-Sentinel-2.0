"""
Data models for Enterprise Security Neural Network
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

@dataclass
class NeuralLayer:
    layer_id: str = ""
    name: str = ""
    layer_type: str = ""
    neurons: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "layer_id": self.layer_id,
            "name": self.name,
            "layer_type": self.layer_type,
            "neurons": self.neurons,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NeuralLayer":
        return cls(
            layer_id=data.get("layer_id"),
            name=data.get("name"),
            layer_type=data.get("layer_type"),
            neurons=data.get("neurons"),
        )

@dataclass
class NetworkConfig:
    config_id: str = ""
    learning_rate: float = 0.0
    batch_size: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "config_id": self.config_id,
            "learning_rate": self.learning_rate,
            "batch_size": self.batch_size,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NetworkConfig":
        return cls(
            config_id=data.get("config_id"),
            learning_rate=data.get("learning_rate"),
            batch_size=data.get("batch_size"),
        )

@dataclass
class PredictionOutput:
    prediction_id: str = ""
    entity_id: str = ""
    threat_score: float = 0.0
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "prediction_id": self.prediction_id,
            "entity_id": self.entity_id,
            "threat_score": self.threat_score,
            "confidence": self.confidence,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PredictionOutput":
        return cls(
            prediction_id=data.get("prediction_id"),
            entity_id=data.get("entity_id"),
            threat_score=data.get("threat_score"),
            confidence=data.get("confidence"),
        )

@dataclass
class TrainingMetrics:
    metrics_id: str = ""
    loss: float = 0.0
    accuracy: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metrics_id": self.metrics_id,
            "loss": self.loss,
            "accuracy": self.accuracy,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TrainingMetrics":
        return cls(
            metrics_id=data.get("metrics_id"),
            loss=data.get("loss"),
            accuracy=data.get("accuracy"),
        )

