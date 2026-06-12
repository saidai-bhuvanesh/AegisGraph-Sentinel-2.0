"""Threat Prediction Engine"""
from datetime import datetime, timezone, timedelta
from typing import Any, Dict
from uuid import uuid4
import random
from .models import ThreatPrediction, PredictionType

class ThreatPredictionEngine:
    def __init__(self):
        self.predictions: Dict[str, ThreatPrediction] = {}
    
    def predict(self, prediction_type: PredictionType, description: str) -> str:
        prediction_id = str(uuid4())
        confidence = random.uniform(0.6, 0.95)
        predicted_time = datetime.now(timezone.utc) + timedelta(days=random.randint(1, 30))
        pred = ThreatPrediction(prediction_id=prediction_id, prediction_type=prediction_type, confidence=confidence, predicted_time=predicted_time, description=description)
        self.predictions[prediction_id] = pred
        return prediction_id
    
    def get_prediction(self, prediction_id: str) -> ThreatPrediction:
        return self.predictions.get(prediction_id)
    
    def get_stats(self) -> Dict[str, Any]:
        return {"total_predictions": len(self.predictions), "avg_confidence": sum(p.confidence for p in self.predictions.values()) / max(1, len(self.predictions))}

def get_prediction_engine() -> ThreatPredictionEngine:
    global _prediction_engine
    if _prediction_engine is None:
        _prediction_engine = ThreatPredictionEngine()
    return _prediction_engine

_prediction_engine = None