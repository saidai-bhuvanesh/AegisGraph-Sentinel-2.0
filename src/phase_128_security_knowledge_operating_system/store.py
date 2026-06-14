"""
Thread-safe store for Security Knowledge Operating System
"""

import threading
from typing import Dict, List, Optional, Any
from .models import KnowledgeArticle, InvestigationKnowledge, ThreatIntelEntry, FraudPattern

class SecurityKnowledgeOperatingSystemStore:
    def __init__(self):
        self.lock = threading.RLock()
        self._knowledgearticles: Dict[str, KnowledgeArticle] = {}
        self._investigationknowledges: Dict[str, InvestigationKnowledge] = {}
        self._threatintelentrys: Dict[str, ThreatIntelEntry] = {}
        self._fraudpatterns: Dict[str, FraudPattern] = {}

    def add_knowledgearticle(self, obj: KnowledgeArticle) -> KnowledgeArticle:
        with self.lock:
            self._knowledgearticles[obj.article_id] = obj
            return obj

    def get_knowledgearticle(self, key: str) -> Optional[KnowledgeArticle]:
        with self.lock:
            return self._knowledgearticles.get(key)

    def list_knowledgearticles(self) -> List[KnowledgeArticle]:
        with self.lock:
            return list(self._knowledgearticles.values())

    def add_investigationknowledge(self, obj: InvestigationKnowledge) -> InvestigationKnowledge:
        with self.lock:
            self._investigationknowledges[obj.knowledge_id] = obj
            return obj

    def get_investigationknowledge(self, key: str) -> Optional[InvestigationKnowledge]:
        with self.lock:
            return self._investigationknowledges.get(key)

    def list_investigationknowledges(self) -> List[InvestigationKnowledge]:
        with self.lock:
            return list(self._investigationknowledges.values())

    def add_threatintelentry(self, obj: ThreatIntelEntry) -> ThreatIntelEntry:
        with self.lock:
            self._threatintelentrys[obj.intel_id] = obj
            return obj

    def get_threatintelentry(self, key: str) -> Optional[ThreatIntelEntry]:
        with self.lock:
            return self._threatintelentrys.get(key)

    def list_threatintelentrys(self) -> List[ThreatIntelEntry]:
        with self.lock:
            return list(self._threatintelentrys.values())

    def add_fraudpattern(self, obj: FraudPattern) -> FraudPattern:
        with self.lock:
            self._fraudpatterns[obj.pattern_id] = obj
            return obj

    def get_fraudpattern(self, key: str) -> Optional[FraudPattern]:
        with self.lock:
            return self._fraudpatterns.get(key)

    def list_fraudpatterns(self) -> List[FraudPattern]:
        with self.lock:
            return list(self._fraudpatterns.values())

_store_instance = None
def get_store() -> SecurityKnowledgeOperatingSystemStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = SecurityKnowledgeOperatingSystemStore()
    return _store_instance
