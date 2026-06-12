"""Threat Prediction Neural Network Hub Models"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict
from uuid import uuid4

class PredictionType(Enum):
    CAMPAIGN = "CAMPAIGN"
    ATTACK = "ATTACK"
    THREAT = "THREAT"

@dataclass
class ThreatPrediction:
    prediction_id: str
    prediction_type: PredictionType
    confidence: float
    predicted_time: datetime
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {"prediction_id": self.prediction_id, "type": self.prediction_type.value,
                "confidence": self.confidence, "time": self.predicted_time.isoformat(), "description": self.description}