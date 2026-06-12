"""MLOps Platform Models - AI Security Model Training"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

class ModelStatus(Enum):
    REGISTERED = "REGISTERED"
    TRAINING = "TRAINING"
    VALIDATED = "VALIDATED"
    DEPLOYED = "DEPLOYED"
    DEPRECATED = "DEPRECATED"

@dataclass
class ModelRegistry:
    model_id: str
    name: str
    version: str
    status: ModelStatus = ModelStatus.REGISTERED
    metrics: Dict[str, float] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id, "name": self.name, "version": self.version,
            "status": self.status.value, "metrics": self.metrics,
            "created_at": self.created_at.isoformat(),
        }

@dataclass
class TrainingRun:
    run_id: str
    model_id: str
    status: str = "PENDING"
    metrics: Dict[str, float] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id, "model_id": self.model_id, "status": self.status,
            "metrics": self.metrics, "created_at": self.created_at.isoformat(),
        }