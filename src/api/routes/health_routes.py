# src/api/routes/health_routes.py
"""Health API router – thin wrapper delegating to the health service.

Provides a basic `/health` endpoint and a detailed `/health/details`
endpoint. All business logic lives in `src.api.services.health_service`.
"""

from __future__ import annotations

from fastapi import APIRouter, Request, HTTPException
from ..services.health_service import get_basic_health, get_detailed_health

router = APIRouter()

@router.get("/", tags=["Health"], summary="Basic health check")
async def health_check():
    """Return a minimal health payload.
    Used by load‑balancers and orchestration tools.
    """
    return get_basic_health()

@router.get("/details", tags=["Health"], summary="Detailed health information")
async def health_details():
    """Return a richer health payload with version, uptime, etc.
    In production this would include DB, cache, and external service checks.
    """
    return get_detailed_health()

@router.get("/liveness", tags=["Health"], summary="Liveness probe")
async def liveness_probe():
    """Liveness probe to check if the app process is running."""
    return {"status": "healthy"}

@router.get("/readiness", tags=["Health"], summary="Readiness probe")
async def readiness_probe(request: Request):
    """Readiness probe to check if the app is ready to serve traffic."""
    runtime = getattr(request.app.state, "runtime", None)
    if runtime is None or not getattr(runtime, "started", False):
        raise HTTPException(status_code=503, detail="Application is starting up")
    
    from src.core.dependency_container import container
    if not container.has("fraud_service") or not container.has("scoring_service"):
        raise HTTPException(status_code=503, detail="DI services not fully initialized")
        
    return {"status": "ready"}

@router.get("/startup", tags=["Health"], summary="Startup probe")
async def startup_probe(request: Request):
    """Startup probe to check if the app lifespan startup completed successfully."""
    runtime = getattr(request.app.state, "runtime", None)
    if runtime is None or not getattr(runtime, "started", False):
        raise HTTPException(status_code=503, detail="Application startup not completed")
    return {"status": "started"}
