# src/api/di.py
"""Dependency‑Injection registration for AegisGraph Sentinel 2.0.

This module centralises the creation of service instances and registers them
with the global ``container`` defined in ``src.core.dependency_container``.
It is invoked during the FastAPI ``lifespan`` start‑up.
"""

from __future__ import annotations

from src.core.dependency_container import container
from src.api.services.scoring_service import ScoringService
from src.api.services.fraud_service import FraudService


def register_services() -> None:
    """Create and register service singletons.

    The services are simple and stateless, so a single shared instance works
    for the entire process.  Future extensions can replace them with factories
    or scoped lifetimes as needed.
    """
    # Register ScoringService first – FraudService depends on it.
    if not container.has("scoring_service"):
        container.register("scoring_service", ScoringService())

    if not container.has("fraud_service"):
        scoring = container.get("scoring_service")
        container.register("fraud_service", FraudService(scoring))

    if not container.has("websocket_manager"):
        from src.api.websocket_manager import WebSocketManager
        container.register("websocket_manager", WebSocketManager())

    # Additional services (e.g., blockchain, innovation) can be added here.
