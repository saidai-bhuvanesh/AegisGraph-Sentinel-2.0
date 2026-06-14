"""
FastAPI request/response schemas for Enterprise Security Neural Network
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class NeuralLayerSchema(BaseModel):
    layer_id: Optional[str] = None
    name: Optional[str] = None
    layer_type: Optional[str] = None
    neurons: Optional[int] = None

class NetworkConfigSchema(BaseModel):
    config_id: Optional[str] = None
    learning_rate: Optional[float] = None
    batch_size: Optional[int] = None

class PredictionOutputSchema(BaseModel):
    prediction_id: Optional[str] = None
    entity_id: Optional[str] = None
    threat_score: Optional[float] = None
    confidence: Optional[float] = None

class TrainingMetricsSchema(BaseModel):
    metrics_id: Optional[str] = None
    loss: Optional[float] = None
    accuracy: Optional[float] = None

class ExecutionRequest(BaseModel):
    tenant_id: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    status: str
    phase: int
    result: Dict[str, Any]
