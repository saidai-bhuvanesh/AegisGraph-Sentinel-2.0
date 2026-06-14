"""
Data models for Hypergraph Investigation Platform
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

@dataclass
class HyperEdge:
    edge_id: str = ""
    entities: List[str] = field(default_factory=list)
    weight: float = 0.0
    relationship_type: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "edge_id": self.edge_id,
            "entities": self.entities,
            "weight": self.weight,
            "relationship_type": self.relationship_type,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HyperEdge":
        return cls(
            edge_id=data.get("edge_id"),
            entities=data.get("entities"),
            weight=data.get("weight"),
            relationship_type=data.get("relationship_type"),
        )

@dataclass
class HyperNode:
    node_id: str = ""
    label: str = ""
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "label": self.label,
            "attributes": self.attributes,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HyperNode":
        return cls(
            node_id=data.get("node_id"),
            label=data.get("label"),
            attributes=data.get("attributes"),
        )

@dataclass
class InvestigationCluster:
    cluster_id: str = ""
    edges: List[str] = field(default_factory=list)
    severity: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cluster_id": self.cluster_id,
            "edges": self.edges,
            "severity": self.severity,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InvestigationCluster":
        return cls(
            cluster_id=data.get("cluster_id"),
            edges=data.get("edges"),
            severity=data.get("severity"),
        )

@dataclass
class PatternMatch:
    match_id: str = ""
    pattern_name: str = ""
    matching_nodes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "match_id": self.match_id,
            "pattern_name": self.pattern_name,
            "matching_nodes": self.matching_nodes,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PatternMatch":
        return cls(
            match_id=data.get("match_id"),
            pattern_name=data.get("pattern_name"),
            matching_nodes=data.get("matching_nodes"),
        )

