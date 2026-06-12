"""Federated Learning Engine"""
from typing import Any, Dict
from uuid import uuid4
from .models import FederatedNode, NodeRole, ModelUpdate

class FederatedLearningEngine:
    def __init__(self):
        self.nodes: Dict[str, FederatedNode] = {}
        self.updates: Dict[str, ModelUpdate] = {}
        self.current_round = 0
    
    def register_node(self, name: str, role: NodeRole) -> str:
        node_id = str(uuid4())
        node = FederatedNode(node_id=node_id, name=name, role=role)
        self.nodes[node_id] = node
        return node_id
    
    def submit_update(self, node_id: str, weights: dict) -> str:
        update_id = str(uuid4())
        update = ModelUpdate(update_id=update_id, node_id=node_id, round=self.current_round, weights=weights)
        self.updates[update_id] = update
        return update_id
    
    def aggregate_updates(self) -> dict:
        self.current_round += 1
        return {"round": self.current_round, "aggregated": True}
    
    def get_stats(self) -> Dict[str, Any]:
        return {"total_nodes": len(self.nodes), "total_updates": len(self.updates), "current_round": self.current_round}

def get_federated_engine() -> FederatedLearningEngine:
    global _federated_engine
    if _federated_engine is None:
        _federated_engine = FederatedLearningEngine()
    return _federated_engine

_federated_engine = None