# src/api/routes/innovation_routes.py
"""Innovation API router – thin wrapper delegating to the innovation service.

Provides minimal `/status` and `/metrics` endpoints. Future work will expose
model health, experiment dashboards, etc.
"""

from __future__ import annotations

from fastapi import APIRouter
from ..services.innovation_service import get_status, get_metrics

router = APIRouter()

@router.get("/status", tags=["Innovation"], summary="Innovation subsystem status")
async def innovation_status():
    """Return a simple status payload for the innovation components."""
    return get_status()

@router.get("/metrics", tags=["Innovation"], summary="Innovation subsystem metrics")
async def innovation_metrics():
    """Return placeholder metrics for the innovation subsystem.

    In a production system this would expose model latency, error rates, etc.
    """
    return get_metrics()
