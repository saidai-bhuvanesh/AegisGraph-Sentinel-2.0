# src/api/services/health_service.py
"""Health service – provides health information for the API.

In a production system this would aggregate runtime, database, and external
service health checks. For now we return a static healthy payload.
"""

from __future__ import annotations

from typing import Dict, Any


def get_basic_health() -> Dict[str, Any]:
    """Return a minimal health payload.

    Returns a dictionary with a simple "status" field. More detailed health can
    be added later without changing the router contract.
    """
    return {"status": "healthy"}


def get_detailed_health() -> Dict[str, Any]:
    """Return a more detailed health payload.

    This stub includes version information and a placeholder uptime.
    """
    return {
        "status": "healthy",
        "version": "2.0.0",
        "uptime_seconds": 0,
        "timestamp": "2026-01-01T00:00:00Z",
    }
