"""Tests for Cyber Genome Module"""
import pytest
from src.cyber_genome import CyberGenomeEngine, GenomeType

class TestCyberGenomeEngine:
    def setup_method(self):
        self.engine = CyberGenomeEngine()
    
    def test_discover_genome(self):
        genome_id = self.engine.discover_genome("Test Malware", GenomeType.MALWARE, ["indicator1", "indicator2"])
        assert genome_id is not None
    
    def test_add_pattern(self):
        pattern_id = self.engine.add_pattern("Suspicious Behavior", "signature_pattern")
        assert pattern_id is not None
    
    def test_get_stats(self):
        stats = self.engine.get_stats()
        assert "total_genomes" in stats

if __name__ == "__main__":
    pytest.main([__file__, "-v"])