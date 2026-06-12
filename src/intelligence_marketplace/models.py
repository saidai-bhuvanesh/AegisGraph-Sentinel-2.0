"""
Intelligence Marketplace Models
Security intelligence data marketplace.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4


class ListingType(Enum):
    """Types of marketplace listings."""
    THREAT_FEED = "THREAT_FEED"
    DATASET = "DATASET"
    MODEL = "MODEL"
    KNOWLEDGE = "KNOWLEDGE"
    INDICATOR_SET = "INDICATOR_SET"


class ListingStatus(Enum):
    """Listing status."""
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    SUBSCRIBED = "SUBSCRIBED"
    ARCHIVED = "ARCHIVED"


class SubscriptionTier(Enum):
    """Subscription tiers."""
    FREE = "FREE"
    STANDARD = "STANDARD"
    PREMIUM = "PREMIUM"
    ENTERPRISE = "ENTERPRISE"


class AccessType(Enum):
    """Access types."""
    PUBLIC = "PUBLIC"
    RESTRICTED = "RESTRICTED"
    SUBSCRIPTION_REQUIRED = "SUBSCRIPTION_REQUIRED"


@dataclass
class MarketplaceListing:
    """A marketplace listing."""
    listing_id: str
    name: str
    description: str
    listing_type: ListingType
    status: ListingStatus = ListingStatus.DRAFT
    access_type: AccessType = AccessType.PUBLIC
    publisher_id: str = ""
    price: float = 0.0
    subscription_tier: SubscriptionTier = SubscriptionTier.FREE
    tags: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    rating: float = 0.0
    subscriber_count: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "listing_id": self.listing_id,
            "name": self.name,
            "description": self.description,
            "listing_type": self.listing_type.value,
            "status": self.status.value,
            "access_type": self.access_type.value,
            "publisher_id": self.publisher_id,
            "price": self.price,
            "subscription_tier": self.subscription_tier.value,
            "tags": self.tags,
            "categories": self.categories,
            "rating": self.rating,
            "subscriber_count": self.subscriber_count,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class Subscription:
    """Intelligence subscription."""
    subscription_id: str
    listing_id: str
    subscriber_id: str
    tier: SubscriptionTier
    status: str = "ACTIVE"
    start_date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    end_date: Optional[datetime] = None
    auto_renew: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "subscription_id": self.subscription_id,
            "listing_id": self.listing_id,
            "subscriber_id": self.subscriber_id,
            "tier": self.tier.value,
            "status": self.status,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "auto_renew": self.auto_renew,
        }


@dataclass
class Dataset:
    """Marketplace dataset."""
    dataset_id: str
    listing_id: str
    name: str
    size: int
    format: str
    features: List[str]
    labels: List[str]
    quality_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "dataset_id": self.dataset_id,
            "listing_id": self.listing_id,
            "name": self.name,
            "size": self.size,
            "format": self.format,
            "features": self.features,
            "labels": self.labels,
            "quality_score": self.quality_score,
        }


@dataclass
class ThreatFeed:
    """Threat intelligence feed."""
    feed_id: str
    listing_id: str
    name: str
    feed_type: str
    indicators: List[Dict[str, Any]] = field(default_factory=list)
    update_frequency: str = "DAILY"
    last_updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "feed_id": self.feed_id,
            "listing_id": self.listing_id,
            "name": self.name,
            "feed_type": self.feed_type,
            "indicator_count": len(self.indicators),
            "update_frequency": self.update_frequency,
            "last_updated": self.last_updated.isoformat(),
        }