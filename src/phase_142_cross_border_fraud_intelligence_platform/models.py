"""
Data models for Cross-Border Fraud Intelligence Platform
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

@dataclass
class CrossBorderTx:
    tx_id: str = ""
    source_country: str = ""
    dest_country: str = ""
    amount: float = 0.0
    currency: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tx_id": self.tx_id,
            "source_country": self.source_country,
            "dest_country": self.dest_country,
            "amount": self.amount,
            "currency": self.currency,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CrossBorderTx":
        return cls(
            tx_id=data.get("tx_id"),
            source_country=data.get("source_country"),
            dest_country=data.get("dest_country"),
            amount=data.get("amount"),
            currency=data.get("currency"),
        )

@dataclass
class TransnationalMuleRing:
    ring_id: str = ""
    main_nodes: List[str] = field(default_factory=list)
    countries_involved: List[str] = field(default_factory=list)
    score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ring_id": self.ring_id,
            "main_nodes": self.main_nodes,
            "countries_involved": self.countries_involved,
            "score": self.score,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TransnationalMuleRing":
        return cls(
            ring_id=data.get("ring_id"),
            main_nodes=data.get("main_nodes"),
            countries_involved=data.get("countries_involved"),
            score=data.get("score"),
        )

@dataclass
class JurisdictionalReport:
    report_id: str = ""
    jurisdiction: str = ""
    cases_flagged: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "jurisdiction": self.jurisdiction,
            "cases_flagged": self.cases_flagged,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JurisdictionalReport":
        return cls(
            report_id=data.get("report_id"),
            jurisdiction=data.get("jurisdiction"),
            cases_flagged=data.get("cases_flagged"),
        )

@dataclass
class IntelExchangeLog:
    log_id: str = ""
    partner_jurisdiction: str = ""
    shared_records: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "log_id": self.log_id,
            "partner_jurisdiction": self.partner_jurisdiction,
            "shared_records": self.shared_records,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IntelExchangeLog":
        return cls(
            log_id=data.get("log_id"),
            partner_jurisdiction=data.get("partner_jurisdiction"),
            shared_records=data.get("shared_records"),
        )

