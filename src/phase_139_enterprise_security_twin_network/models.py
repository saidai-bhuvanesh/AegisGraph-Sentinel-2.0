"""
Data models for Enterprise Security Twin Network
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

@dataclass
class DigitalTwin:
    twin_id: str = ""
    name: str = ""
    target_tenant: str = ""
    status: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "twin_id": self.twin_id,
            "name": self.name,
            "target_tenant": self.target_tenant,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DigitalTwin":
        return cls(
            twin_id=data.get("twin_id"),
            name=data.get("name"),
            target_tenant=data.get("target_tenant"),
            status=data.get("status"),
        )

@dataclass
class EntityState:
    state_id: str = ""
    twin_id: str = ""
    entity_id: str = ""
    variables: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "state_id": self.state_id,
            "twin_id": self.twin_id,
            "entity_id": self.entity_id,
            "variables": self.variables,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EntityState":
        return cls(
            state_id=data.get("state_id"),
            twin_id=data.get("twin_id"),
            entity_id=data.get("entity_id"),
            variables=data.get("variables"),
        )

@dataclass
class SynchronizationJob:
    job_id: str = ""
    twin_id: str = ""
    last_sync: str = ""
    status: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "twin_id": self.twin_id,
            "last_sync": self.last_sync,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SynchronizationJob":
        return cls(
            job_id=data.get("job_id"),
            twin_id=data.get("twin_id"),
            last_sync=data.get("last_sync"),
            status=data.get("status"),
        )

@dataclass
class RiskForecast:
    forecast_id: str = ""
    twin_id: str = ""
    simulated_incidents: int = 0
    projected_loss: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "forecast_id": self.forecast_id,
            "twin_id": self.twin_id,
            "simulated_incidents": self.simulated_incidents,
            "projected_loss": self.projected_loss,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RiskForecast":
        return cls(
            forecast_id=data.get("forecast_id"),
            twin_id=data.get("twin_id"),
            simulated_incidents=data.get("simulated_incidents"),
            projected_loss=data.get("projected_loss"),
        )

