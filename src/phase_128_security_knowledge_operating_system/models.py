"""
Data models for Security Knowledge Operating System
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

@dataclass
class KnowledgeArticle:
    article_id: str = ""
    title: str = ""
    content: str = ""
    category: str = ""
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "article_id": self.article_id,
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KnowledgeArticle":
        return cls(
            article_id=data.get("article_id"),
            title=data.get("title"),
            content=data.get("content"),
            category=data.get("category"),
            tags=data.get("tags"),
        )

@dataclass
class InvestigationKnowledge:
    knowledge_id: str = ""
    case_id: str = ""
    findings: str = ""
    entities: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "knowledge_id": self.knowledge_id,
            "case_id": self.case_id,
            "findings": self.findings,
            "entities": self.entities,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InvestigationKnowledge":
        return cls(
            knowledge_id=data.get("knowledge_id"),
            case_id=data.get("case_id"),
            findings=data.get("findings"),
            entities=data.get("entities"),
        )

@dataclass
class ThreatIntelEntry:
    intel_id: str = ""
    indicator: str = ""
    threat_type: str = ""
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "intel_id": self.intel_id,
            "indicator": self.indicator,
            "threat_type": self.threat_type,
            "confidence": self.confidence,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ThreatIntelEntry":
        return cls(
            intel_id=data.get("intel_id"),
            indicator=data.get("indicator"),
            threat_type=data.get("threat_type"),
            confidence=data.get("confidence"),
        )

@dataclass
class FraudPattern:
    pattern_id: str = ""
    name: str = ""
    rules: List[str] = field(default_factory=list)
    severity: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pattern_id": self.pattern_id,
            "name": self.name,
            "rules": self.rules,
            "severity": self.severity,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FraudPattern":
        return cls(
            pattern_id=data.get("pattern_id"),
            name=data.get("name"),
            rules=data.get("rules"),
            severity=data.get("severity"),
        )

