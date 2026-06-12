"""
Intelligence Marketplace Engine
Security intelligence data marketplace.
"""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

from .models import (
    MarketplaceListing,
    ListingType,
    ListingStatus,
    AccessType,
    Subscription,
    SubscriptionTier,
    Dataset,
    ThreatFeed,
)


class ListingManager:
    """Manager for marketplace listings."""
    
    def __init__(self):
        self.listings: Dict[str, MarketplaceListing] = {}
        self._initialize_default_listings()
    
    def _initialize_default_listings(self):
        """Initialize default listings."""
        listings = [
            MarketplaceListing(
                listing_id="list-001",
                name="Global Fraud Indicators",
                description="Real-time fraud indicators from multiple sources",
                listing_type=ListingType.THREAT_FEED,
                status=ListingStatus.PUBLISHED,
                publisher_id="system",
                tags=["fraud", "indicators", "real-time"],
                categories=["Fraud Detection", "Threat Intelligence"],
            ),
            MarketplaceListing(
                listing_id="list-002",
                name="AML Transaction Dataset",
                description="Synthetic AML transaction data for training",
                listing_type=ListingType.DATASET,
                status=ListingStatus.PUBLISHED,
                publisher_id="research-team",
                tags=["aml", "transactions", "training"],
                categories=["Anti-Money Laundering", "Research"],
            ),
        ]
        
        for listing in listings:
            self.listings[listing.listing_id] = listing
    
    def create_listing(
        self,
        name: str,
        description: str,
        listing_type: ListingType,
        publisher_id: str,
        price: float = 0.0,
        subscription_tier: SubscriptionTier = SubscriptionTier.FREE,
        tags: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
        access_type: AccessType = AccessType.PUBLIC,
    ) -> str:
        """Create a new listing."""
        listing_id = str(uuid4())
        
        listing = MarketplaceListing(
            listing_id=listing_id,
            name=name,
            description=description,
            listing_type=listing_type,
            publisher_id=publisher_id,
            price=price,
            subscription_tier=subscription_tier,
            tags=tags or [],
            categories=categories or [],
            access_type=access_type,
        )
        
        self.listings[listing_id] = listing
        return listing_id
    
    def get_listing(self, listing_id: str) -> Optional[MarketplaceListing]:
        """Get a listing by ID."""
        return self.listings.get(listing_id)
    
    def update_listing(
        self,
        listing_id: str,
        status: Optional[ListingStatus] = None,
        price: Optional[float] = None,
    ) -> bool:
        """Update a listing."""
        listing = self.listings.get(listing_id)
        if not listing:
            return False
        
        if status:
            listing.status = status
        if price is not None:
            listing.price = price
        
        listing.updated_at = datetime.now(timezone.utc)
        return True
    
    def search_listings(
        self,
        query: str,
        listing_type: Optional[ListingType] = None,
        tags: Optional[List[str]] = None,
    ) -> List[MarketplaceListing]:
        """Search listings."""
        results = []
        
        for listing in self.listings.values():
            if listing.status == ListingStatus.ARCHIVED:
                continue
            
            if listing_type and listing.listing_type != listing_type:
                continue
            
            if query.lower() in listing.name.lower() or query.lower() in listing.description.lower():
                results.append(listing)
                continue
            
            if tags:
                if any(tag in listing.tags for tag in tags):
                    results.append(listing)
        
        return results
    
    def get_listings_by_publisher(self, publisher_id: str) -> List[MarketplaceListing]:
        """Get listings by publisher."""
        return [l for l in self.listings.values() if l.publisher_id == publisher_id]


class SubscriptionManager:
    """Manager for subscriptions."""
    
    def __init__(self):
        self.subscriptions: Dict[str, Subscription] = {}
    
    def subscribe(
        self,
        listing_id: str,
        subscriber_id: str,
        tier: SubscriptionTier = SubscriptionTier.FREE,
    ) -> str:
        """Subscribe to a listing."""
        subscription_id = str(uuid4())
        
        subscription = Subscription(
            subscription_id=subscription_id,
            listing_id=listing_id,
            subscriber_id=subscriber_id,
            tier=tier,
        )
        
        self.subscriptions[subscription_id] = subscription
        return subscription_id
    
    def get_subscription(self, subscription_id: str) -> Optional[Subscription]:
        """Get a subscription."""
        return self.subscriptions.get(subscription_id)
    
    def get_subscriptions_by_subscriber(self, subscriber_id: str) -> List[Subscription]:
        """Get subscriptions for a subscriber."""
        return [s for s in self.subscriptions.values() if s.subscriber_id == subscriber_id]
    
    def get_subscriptions_by_listing(self, listing_id: str) -> List[Subscription]:
        """Get subscriptions for a listing."""
        return [s for s in self.subscriptions.values() if s.listing_id == listing_id]
    
    def cancel_subscription(self, subscription_id: str) -> bool:
        """Cancel a subscription."""
        subscription = self.subscriptions.get(subscription_id)
        if not subscription:
            return False
        
        subscription.status = "CANCELLED"
        return True


class DatasetRegistry:
    """Registry for datasets."""
    
    def __init__(self):
        self.datasets: Dict[str, Dataset] = {}
        self._initialize_default_datasets()
    
    def _initialize_default_datasets(self):
        """Initialize default datasets."""
        datasets = [
            Dataset(
                dataset_id="ds-001",
                listing_id="list-002",
                name="AML Training Data",
                size=50000,
                format="CSV",
                features=["amount", "frequency", "velocity"],
                labels=["suspicious", "normal"],
                quality_score=0.92,
            ),
        ]
        
        for ds in datasets:
            self.datasets[ds.dataset_id] = ds
    
    def register_dataset(
        self,
        listing_id: str,
        name: str,
        size: int,
        format: str,
        features: List[str],
        labels: List[str],
    ) -> str:
        """Register a dataset."""
        dataset_id = str(uuid4())
        
        dataset = Dataset(
            dataset_id=dataset_id,
            listing_id=listing_id,
            name=name,
            size=size,
            format=format,
            features=features,
            labels=labels,
        )
        
        self.datasets[dataset_id] = dataset
        return dataset_id
    
    def get_dataset(self, dataset_id: str) -> Optional[Dataset]:
        """Get a dataset."""
        return self.datasets.get(dataset_id)


class ThreatFeedExchange:
    """Exchange for threat feeds."""
    
    def __init__(self):
        self.feeds: Dict[str, ThreatFeed] = {}
        self._initialize_default_feeds()
    
    def _initialize_default_feeds(self):
        """Initialize default feeds."""
        feeds = [
            ThreatFeed(
                feed_id="feed-001",
                listing_id="list-001",
                name="Global Fraud Feed",
                feed_type="INDICATORS",
                indicators=[
                    {"type": "ip", "value": "192.168.1.1", "confidence": 0.9},
                    {"type": "domain", "value": "malicious.com", "confidence": 0.85},
                ],
                update_frequency="REAL-TIME",
            ),
        ]
        
        for feed in feeds:
            self.feeds[feed.feed_id] = feed
    
    def publish_feed(
        self,
        listing_id: str,
        name: str,
        feed_type: str,
        indicators: List[Dict[str, Any]],
    ) -> str:
        """Publish a threat feed."""
        feed_id = str(uuid4())
        
        feed = ThreatFeed(
            feed_id=feed_id,
            listing_id=listing_id,
            name=name,
            feed_type=feed_type,
            indicators=indicators,
        )
        
        self.feeds[feed_id] = feed
        return feed_id
    
    def get_feed(self, feed_id: str) -> Optional[ThreatFeed]:
        """Get a feed."""
        return self.feeds.get(feed_id)
    
    def get_feed_indicators(self, feed_id: str) -> List[Dict[str, Any]]:
        """Get feed indicators."""
        feed = self.feeds.get(feed_id)
        return feed.indicators if feed else []


class MarketplaceEngine:
    """Main marketplace engine."""
    
    def __init__(self):
        self.listing_manager = ListingManager()
        self.subscription_manager = SubscriptionManager()
        self.dataset_registry = DatasetRegistry()
        self.feed_exchange = ThreatFeedExchange()
    
    def publish_listing(
        self,
        name: str,
        description: str,
        listing_type: ListingType,
        publisher_id: str,
        tags: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
    ) -> str:
        """Publish a listing."""
        listing_id = self.listing_manager.create_listing(
            name=name,
            description=description,
            listing_type=listing_type,
            publisher_id=publisher_id,
            tags=tags,
            categories=categories,
        )
        
        self.listing_manager.update_listing(listing_id, ListingStatus.PUBLISHED)
        return listing_id
    
    def subscribe_to_listing(
        self,
        listing_id: str,
        subscriber_id: str,
        tier: SubscriptionTier = SubscriptionTier.FREE,
    ) -> str:
        """Subscribe to a listing."""
        subscription_id = self.subscription_manager.subscribe(
            listing_id=listing_id,
            subscriber_id=subscriber_id,
            tier=tier,
        )
        
        listing = self.listing_manager.get_listing(listing_id)
        if listing:
            listing.subscriber_count += 1
            listing.status = ListingStatus.SUBSCRIBED
        
        return subscription_id
    
    def get_dashboard(self, publisher_id: Optional[str] = None) -> Dict[str, Any]:
        """Get marketplace dashboard."""
        listings = list(self.listing_manager.listings.values())
        
        if publisher_id:
            listings = [l for l in listings if l.publisher_id == publisher_id]
        
        type_counts = {}
        for listing in listings:
            ltype = listing.listing_type.value
            type_counts[ltype] = type_counts.get(ltype, 0) + 1
        
        return {
            "total_listings": len(listings),
            "by_type": type_counts,
            "total_subscribers": sum(l.subscriber_count for l in listings),
            "avg_rating": sum(l.rating for l in listings) / max(1, len(listings)),
        }


def get_marketplace_engine() -> MarketplaceEngine:
    """Get the global marketplace engine instance."""
    global _marketplace_engine
    if _marketplace_engine is None:
        _marketplace_engine = MarketplaceEngine()
    return _marketplace_engine


_marketplace_engine: Optional[MarketplaceEngine] = None