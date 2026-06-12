"""Federated Learning Security Network Models"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict
from uuid import uuid4

class NodeRole(Enum):
    AGGREGATOR = "AGGREGATOR"
    PARTICIPANT = "PARTICIPANT"

@dataclass
class FederatedNode:
    node_id: str
    name: str
    role: NodeRole
    status: str = "ACTIVE"
    
    def to_dict(self) -> Dict[str, Any]:
        return {"node_id": self.node_id, "name": self.name, "role": self.role.value, "status": self.status}

@dataclass
class ModelUpdate:
    update_id: str
    node_id: str
    round: int
    weights: dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {"update_id": self.update_id, "node_id": self.node_id, "round": self.round, "weights": self.weights}