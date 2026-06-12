"""Cyber Genome Platform Models"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List
from uuid import uuid4

class GenomeType(Enum):
    MALWARE = "MALWARE"
    ATTACK_PATTERN = "ATTACK_PATTERN"
    BEHAVIOR_SIGNATURE = "BEHAVIOR_SIGNATURE"

@dataclass
class ThreatGenome:
    genome_id: str
    name: str
    genome_type: GenomeType
    dna_sequence: str = ""
    indicators: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {"genome_id": self.genome_id, "name": self.name,
                "genome_type": self.genome_type.value, "dna_sequence": self.dna_sequence,
                "indicators": self.indicators}

@dataclass
class BehaviorPattern:
    pattern_id: str
    name: str
    signature: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {"pattern_id": self.pattern_id, "name": self.name, "signature": self.signature}