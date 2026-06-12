"""Trust & Reputation Network Engine"""
from typing import Any, Dict
from uuid import uuid4
from .models import TrustEntity, TrustLevel, ReputationRecord

class TrustEngine:
    def __init__(self):
        self.entities: Dict[str, TrustEntity] = {}
        self.reputation: Dict[str, ReputationRecord] = {}
    
    def add_entity(self, name: str, initial_score: float = 0.5) -> str:
        entity_id = str(uuid4())
        level = TrustLevel.MEDIUM
        if initial_score >= 0.8: level = TrustLevel.VERY_HIGH
        elif initial_score >= 0.6: level = TrustLevel.HIGH
        elif initial_score < 0.4: level = TrustLevel.LOW
        elif initial_score < 0.2: level = TrustLevel.VERY_LOW
        
        entity = TrustEntity(entity_id=entity_id, name=name, trust_score=initial_score, trust_level=level)
        self.entities[entity_id] = entity
        return entity_id
    
    def get_entity(self, entity_id: str) -> TrustEntity:
        return self.entities.get(entity_id)
    
    def add_reputation(self, entity_id: str, score: float, factors: list) -> str:
        record_id = str(uuid4())
        record = ReputationRecord(record_id=record_id, entity_id=entity_id, score=score, factors=factors)
        self.reputation[record_id] = record
        return record_id
    
    def get_stats(self) -> Dict[str, Any]:
        return {"total_entities": len(self.entities), "total_records": len(self.reputation)}

def get_trust_engine() -> TrustEngine:
    global _trust_engine
    if _trust_engine is None:
        _trust_engine = TrustEngine()
    return _trust_engine

_trust_engine = None