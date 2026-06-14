"""
Data models for Enterprise Risk Simulation Platform
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

@dataclass
class Simulation:
    simulation_id: str = ""
    name: str = ""
    threat_vector: str = ""
    status: str = ""
    duration: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "simulation_id": self.simulation_id,
            "name": self.name,
            "threat_vector": self.threat_vector,
            "status": self.status,
            "duration": self.duration,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Simulation":
        return cls(
            simulation_id=data.get("simulation_id"),
            name=data.get("name"),
            threat_vector=data.get("threat_vector"),
            status=data.get("status"),
            duration=data.get("duration"),
        )

@dataclass
class SimulationResult:
    result_id: str = ""
    simulation_id: str = ""
    losses_prevented: float = 0.0
    breach_probability: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "result_id": self.result_id,
            "simulation_id": self.simulation_id,
            "losses_prevented": self.losses_prevented,
            "breach_probability": self.breach_probability,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SimulationResult":
        return cls(
            result_id=data.get("result_id"),
            simulation_id=data.get("simulation_id"),
            losses_prevented=data.get("losses_prevented"),
            breach_probability=data.get("breach_probability"),
        )

@dataclass
class ThreatVector:
    vector_id: str = ""
    name: str = ""
    type: str = ""
    severity: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "vector_id": self.vector_id,
            "name": self.name,
            "type": self.type,
            "severity": self.severity,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ThreatVector":
        return cls(
            vector_id=data.get("vector_id"),
            name=data.get("name"),
            type=data.get("type"),
            severity=data.get("severity"),
        )

@dataclass
class ForecastModel:
    model_id: str = ""
    name: str = ""
    accuracy: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "name": self.name,
            "accuracy": self.accuracy,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ForecastModel":
        return cls(
            model_id=data.get("model_id"),
            name=data.get("name"),
            accuracy=data.get("accuracy"),
        )

