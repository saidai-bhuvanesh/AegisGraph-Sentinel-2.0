"""
Data models for Financial Ecosystem Risk Platform
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

@dataclass
class EcosystemNode:
    node_id: str = ""
    institution_name: str = ""
    type: str = ""
    risk_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "institution_name": self.institution_name,
            "type": self.type,
            "risk_score": self.risk_score,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EcosystemNode":
        return cls(
            node_id=data.get("node_id"),
            institution_name=data.get("institution_name"),
            type=data.get("type"),
            risk_score=data.get("risk_score"),
        )

@dataclass
class InterbankTx:
    tx_id: str = ""
    from_node: str = ""
    to_node: str = ""
    amount: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tx_id": self.tx_id,
            "from_node": self.from_node,
            "to_node": self.to_node,
            "amount": self.amount,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InterbankTx":
        return cls(
            tx_id=data.get("tx_id"),
            from_node=data.get("from_node"),
            to_node=data.get("to_node"),
            amount=data.get("amount"),
        )

@dataclass
class SystemicAnomaly:
    anomaly_id: str = ""
    nodes_involved: List[str] = field(default_factory=list)
    risk_type: str = ""
    severity: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "anomaly_id": self.anomaly_id,
            "nodes_involved": self.nodes_involved,
            "risk_type": self.risk_type,
            "severity": self.severity,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SystemicAnomaly":
        return cls(
            anomaly_id=data.get("anomaly_id"),
            nodes_involved=data.get("nodes_involved"),
            risk_type=data.get("risk_type"),
            severity=data.get("severity"),
        )

@dataclass
class RiskExposureReport:
    report_id: str = ""
    forecast_period: str = ""
    potential_loss: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "forecast_period": self.forecast_period,
            "potential_loss": self.potential_loss,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RiskExposureReport":
        return cls(
            report_id=data.get("report_id"),
            forecast_period=data.get("forecast_period"),
            potential_loss=data.get("potential_loss"),
        )

