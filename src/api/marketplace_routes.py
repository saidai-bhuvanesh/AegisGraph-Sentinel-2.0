"""
Intelligence Marketplace API Routes
"""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Header, Query
from pydantic import BaseModel

from src.intelligence_marketplace import (
    MarketplaceEngine,
    get_marketplace_engine,
    ListingType,
    ListingStatus,
    SubscriptionTier,
)


router = APIRouter(prefix="/api/v1/marketplace", tags=["marketplace"])


class PublishListingRequest(BaseModel):
    """Request to publish a listing."""
    name: str
    description: str
    listing_type: str
    publisher_id: str
    tags: List[str] = []
    categories: List[str] = []


class SubscribeRequest(BaseModel):
    """Request to subscribe."""
    listing_id: str
    subscriber_id: str
    tier: str = "FREE"


def verify_api_key(x_api_key: str = Header(None)) -> str:
    """Verify API key."""
    if x_api_key != "SUPER_ADMIN":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "module": "intelligence_marketplace",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.post("/publish")
async def publish_listing(
    request: PublishListingRequest,
    api_key: str = Header(None),
):
    """Publish a marketplace listing."""
    verify_api_key(api_key)
    engine = get_marketplace_engine()
    
    try:
        listing_type = ListingType(request.listing_type)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid listing type")
    
    listing_id = engine.publish_listing(
        name=request.name,
        description=request.description,
        listing_type=listing_type,
        publisher_id=request.publisher_id,
        tags=request.tags,
        categories=request.categories,
    )
    
    return {
        "listing_id": listing_id,
        "status": "published",
    }


@router.get("/listings")
async def list_listings(
    listing_type: Optional[str] = None,
    query: Optional[str] = None,
    api_key: str = Header(None),
):
    """List marketplace listings."""
    verify_api_key(api_key)
    engine = get_marketplace_engine()
    
    if query:
        ltype = None
        if listing_type:
            try:
                ltype = ListingType(listing_type)
            except ValueError:
                pass
        
        listings = engine.listing_manager.search_listings(query, ltype)
    else:
        listings = list(engine.listing_manager.listings.values())
        if listing_type:
            try:
                ltype = ListingType(listing_type)
                listings = [l for l in listings if l.listing_type == ltype]
            except ValueError:
                pass
    
    return {
        "count": len(listings),
        "listings": [l.to_dict() for l in listings],
    }


@router.get("/listings/{listing_id}")
async def get_listing(
    listing_id: str,
    api_key: str = Header(None),
):
    """Get a listing."""
    verify_api_key(api_key)
    engine = get_marketplace_engine()
    
    listing = engine.listing_manager.get_listing(listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    return {"listing": listing.to_dict()}


@router.post("/subscribe")
async def subscribe(
    request: SubscribeRequest,
    api_key: str = Header(None),
):
    """Subscribe to a listing."""
    verify_api_key(api_key)
    engine = get_marketplace_engine()
    
    try:
        tier = SubscriptionTier(request.tier)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid tier")
    
    subscription_id = engine.subscribe_to_listing(
        listing_id=request.listing_id,
        subscriber_id=request.subscriber_id,
        tier=tier,
    )
    
    return {
        "subscription_id": subscription_id,
        "status": "active",
    }


@router.get("/subscriptions")
async def list_subscriptions(
    subscriber_id: Optional[str] = None,
    api_key: str = Header(None),
):
    """List subscriptions."""
    verify_api_key(api_key)
    engine = get_marketplace_engine()
    
    if subscriber_id:
        subs = engine.subscription_manager.get_subscriptions_by_subscriber(subscriber_id)
    else:
        subs = list(engine.subscription_manager.subscriptions.values())
    
    return {
        "count": len(subs),
        "subscriptions": [s.to_dict() for s in subs],
    }


@router.delete("/subscriptions/{subscription_id}")
async def cancel_subscription(
    subscription_id: str,
    api_key: str = Header(None),
):
    """Cancel a subscription."""
    verify_api_key(api_key)
    engine = get_marketplace_engine()
    
    success = engine.subscription_manager.cancel_subscription(subscription_id)
    if not success:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    return {"status": "cancelled"}


@router.get("/feeds")
async def list_feeds(api_key: str = Header(None)):
    """List threat feeds."""
    verify_api_key(api_key)
    engine = get_marketplace_engine()
    
    feeds = list(engine.feed_exchange.feeds.values())
    
    return {
        "count": len(feeds),
        "feeds": [f.to_dict() for f in feeds],
    }


@router.get("/datasets")
async def list_datasets(api_key: str = Header(None)):
    """List datasets."""
    verify_api_key(api_key)
    engine = get_marketplace_engine()
    
    datasets = list(engine.dataset_registry.datasets.values())
    
    return {
        "count": len(datasets),
        "datasets": [d.to_dict() for d in datasets],
    }


@router.get("/dashboard")
async def get_dashboard(
    publisher_id: Optional[str] = None,
    api_key: str = Header(None),
):
    """Get marketplace dashboard."""
    verify_api_key(api_key)
    engine = get_marketplace_engine()
    
    return engine.get_dashboard(publisher_id)