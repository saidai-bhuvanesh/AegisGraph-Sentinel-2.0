"""
Intelligence Federation Engine
Cross-industry intelligence sharing.
"""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

from .models import (
    FederationMember,
    IndustryType,
    FederationRole,
    SharedIndicator,
)


class FederationRegistry:
    """Registry for federation members."""
    
    def __init__(self):
        self.members: Dict[str, FederationMember] = {}
        self._initialize_default_members()
    
    def _initialize_default_members(self):
        """Initialize default members."""
        members = [
            FederationMember(
                member_id="mem-001",
                organization="Global Bank A",
                industry=IndustryType.FINANCIAL,
                role=FederationRole.BOTH,
            ),
            FederationMember(
                member_id="mem-002",
                organization="Major Healthcare Inc",
                industry=IndustryType.HEALTHCARE,
                role=FederationRole.CONSUMER,
            ),
        ]
        for m in members:
            self.members[m.member_id] = m
    
    def register_member(
        self,
        organization: str,
        industry: IndustryType,
        role: FederationRole,
    ) -> str:
        """Register a new member."""
        member_id = str(uuid4())
        member = FederationMember(
            member_id=member_id,
            organization=organization,
            industry=industry,
            role=role,
        )
        self.members[member_id] = member
        return member_id
    
    def get_member(self, member_id: str) -> Optional[FederationMember]:
        """Get a member."""
        return self.members.get(member_id)
    
    def get_members_by_industry(self, industry: IndustryType) -> List[FederationMember]:
        """Get members by industry."""
        return [m for m in self.members.values() if m.industry == industry]


class IntelligenceExchange:
    """Exchange for sharing intelligence."""
    
    def __init__(self):
        self.indicators: Dict[str, SharedIndicator] = {}
    
    def share_indicator(
        self,
        indicator_type: str,
        value: str,
        source_industry: IndustryType,
        confidence: float,
    ) -> str:
        """Share an indicator."""
        indicator_id = str(uuid4())
        indicator = SharedIndicator(
            indicator_id=indicator_id,
            type=indicator_type,
            value=value,
            source_industry=source_industry,
            confidence=confidence,
        )
        self.indicators[indicator_id] = indicator
        return indicator_id
    
    def get_indicator(self, indicator_id: str) -> Optional[SharedIndicator]:
        """Get an indicator."""
        return self.indicators.get(indicator_id)
    
    def search_indicators(
        self,
        indicator_type: Optional[str] = None,
        source_industry: Optional[IndustryType] = None,
    ) -> List[SharedIndicator]:
        """Search indicators."""
        results = list(self.indicators.values())
        
        if indicator_type:
            results = [i for i in results if i.type == indicator_type]
        
        if source_industry:
            results = [i for i in results if i.source_industry == source_industry]
        
        return results


class CrossIndustryCorrelation:
    """Cross-industry correlation engine."""
    
    def __init__(self):
        self.correlations: Dict[str, List[str]] = {}
    
    def correlate(
        self,
        indicator_id1: str,
        indicator_id2: str,
        correlation_score: float,
    ) -> str:
        """Correlate two indicators."""
        correlation_id = str(uuid4())
        self.correlations[correlation_id] = [indicator_id1, indicator_id2]
        return correlation_id
    
    def get_correlations(self, indicator_id: str) -> List[str]:
        """Get correlations for an indicator."""
        return [
            cid for cid, ids in self.correlations.items()
            if indicator_id in ids
        ]


class FederationEngine:
    """Main federation engine."""
    
    def __init__(self):
        self.registry = FederationRegistry()
        self.exchange = IntelligenceExchange()
        self.correlation = CrossIndustryCorrelation()
    
    def join_federation(
        self,
        organization: str,
        industry: IndustryType,
        role: FederationRole,
    ) -> str:
        """Join the federation."""
        return self.registry.register_member(organization, industry, role)
    
    def publish_indicator(
        self,
        member_id: str,
        indicator_type: str,
        value: str,
        confidence: float,
    ) -> str:
        """Publish an indicator."""
        member = self.registry.get_member(member_id)
        if not member:
            raise ValueError("Member not found")
        
        return self.exchange.share_indicator(
            indicator_type=indicator_type,
            value=value,
            source_industry=member.industry,
            confidence=confidence,
        )
    
    def get_federation_stats(self) -> Dict[str, Any]:
        """Get federation statistics."""
        members = list(self.registry.members.values())
        
        industry_counts = {}
        for m in members:
            ind = m.industry.value
            industry_counts[ind] = industry_counts.get(ind, 0) + 1
        
        return {
            "total_members": len(members),
            "by_industry": industry_counts,
            "total_indicators": len(self.exchange.indicators),
            "avg_trust_score": sum(m.trust_score for m in members) / max(1, len(members)),
        }


def get_federation_engine() -> FederationEngine:
    """Get the global federation engine."""
    global _federation_engine
    if _federation_engine is None:
        _federation_engine = FederationEngine()
    return _federation_engine


_federation_engine: Optional[FederationEngine] = None