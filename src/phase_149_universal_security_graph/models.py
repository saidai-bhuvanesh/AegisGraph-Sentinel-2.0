"""
Data models for Universal Security Graph
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

@dataclass
class UnifiedNode:
    node_id: str = ""
    domain: str = ""
    label: str = ""
    risk_weight: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "domain": self.domain,
            "label": self.label,
            "risk_weight": self.risk_weight,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UnifiedNode":
        return cls(
            node_id=data.get("node_id"),
            domain=data.get("domain"),
            label=data.get("label"),
            risk_weight=data.get("risk_weight"),
        )

@dataclass
class UnifiedEdge:
    edge_id: str = ""
    source_id: str = ""
    target_id: str = ""
    edge_type: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "edge_id": self.edge_id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "edge_type": self.edge_type,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UnifiedEdge":
        return cls(
            edge_id=data.get("edge_id"),
            source_id=data.get("source_id"),
            target_id=data.get("target_id"),
            edge_type=data.get("edge_type"),
        )

@dataclass
class USGGraph:
    graph_id: str = ""
    nodes_count: int = 0
    edges_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "graph_id": self.graph_id,
            "nodes_count": self.nodes_count,
            "edges_count": self.edges_count,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "USGGraph":
        return cls(
            graph_id=data.get("graph_id"),
            nodes_count=data.get("nodes_count"),
            edges_count=data.get("edges_count"),
        )

@dataclass
class CrossDomainCorrelation:
    correlation_id: str = ""
    source_node: str = ""
    target_node: str = ""
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "correlation_id": self.correlation_id,
            "source_node": self.source_node,
            "target_node": self.target_node,
            "confidence": self.confidence,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CrossDomainCorrelation":
        return cls(
            correlation_id=data.get("correlation_id"),
            source_node=data.get("source_node"),
            target_node=data.get("target_node"),
            confidence=data.get("confidence"),
        )

