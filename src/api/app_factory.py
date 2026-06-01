# src/api/app_factory.py
"""Application factory for AegisGraph Sentinel 2.0.

Creates a FastAPI instance, registers middleware, lifecycle handlers, DI
services, and includes route routers.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

# Local imports (imported inside the function to avoid circular deps)

@asynccontextmanager
async def _lifespan(app: FastAPI):
    """Startup / shutdown logic (replaces @app.on_event)."""
    from .di import register_services
    from ..runtime import RuntimeState
    from ..observability import get_logger, get_audit_logger

    logger = get_logger("api_factory")
    audit_logger = get_audit_logger()

    logger.info("🚀 Application startup – initializing services")

    # Register DI services
    register_services()

    # Core runtime state
    import time
    state = RuntimeState()
    app.state.runtime = state
    app.state.start_time = time.time()

    # --- Initialize & Start Kafka Streaming Infrastructure ---
    import os
    from src.streaming.producer import KafkaProducerWrapper
    from src.streaming.consumer import KafkaConsumerWorker
    from src.core.dependency_container import container

    kafka_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "")
    
    producer = KafkaProducerWrapper(bootstrap_servers=kafka_servers)
    await producer.start()
    container.register("kafka_producer", producer, replace=True)
    
    consumer = KafkaConsumerWorker(
        bootstrap_servers=kafka_servers,
        group_id="aegis-sentinel-group",
        topic="aegis-transactions"
    )
    await consumer.start()
    container.register("kafka_consumer", consumer, replace=True)
    app.state.kafka_consumer = consumer
    # ---------------------------------------------------------

    # Start WebSocket stale connection cleanup task
    from src.api.routes.websocket_routes import websocket_cleanup_loop
    state.tasks.register_task(
        websocket_cleanup_loop(interval_seconds=30),
        name="websocket_stale_cleanup",
        owner="api"
    )

    state.started = True

    yield  # Application runs

    state.started = False

    # ---- Shutdown ----
    logger.info("🛑 Application shutdown – cleaning up")
    
    # Gracefully stop Kafka consumer and producer
    from src.core.dependency_container import container
    if container.has("kafka_consumer"):
        try:
            await container.get("kafka_consumer").stop()
        except Exception as exc:
            logger.error(f"Error stopping Kafka consumer worker: {exc}")
            
    if container.has("kafka_producer"):
        try:
            await container.get("kafka_producer").stop()
        except Exception as exc:
            logger.error(f"Error stopping Kafka producer: {exc}")

    # Gracefully cancel all registered background tasks
    if hasattr(state, "tasks") and state.tasks:
        try:
            await state.tasks.cancel_all_tasks(timeout_seconds=5.0)
        except Exception as exc:
            logger.error(f"Error cancelling background tasks: {exc}")

    # Close any DI-registered services that support close/disconnect
    import inspect
    from src.core.dependency_container import container
    for service_name in ["neo4j_provider", "redis_client", "kafka_producer", "kafka_consumer"]:
        if container.has(service_name):
            try:
                service = container.get(service_name)
                if hasattr(service, "close") and callable(service.close):
                    if inspect.iscoroutinefunction(service.close):
                        await service.close()
                    else:
                        service.close()
                elif hasattr(service, "disconnect") and callable(service.disconnect):
                    if inspect.iscoroutinefunction(service.disconnect):
                        await service.disconnect()
                    else:
                        service.disconnect()
            except Exception as exc:
                logger.error(f"Error closing service {service_name}: {exc}")


def create_app(settings: Optional[dict] = None) -> FastAPI:
    """Factory that returns a fully‑configured FastAPI instance."""
    # Settings can be passed; otherwise use default settings module
    from ..config.settings import get_settings

    settings = settings or get_settings()
    app = FastAPI(
        title="AegisGraph Sentinel 2.0 API",
        version="2.0.0",
        description="Real‑time fraud detection platform with graph AI, streaming, and explainable AI.",
        lifespan=_lifespan,
    )

    # CORS Middleware from settings
    if not isinstance(settings, dict):
        allowed_origins = settings.api.allowed_origins
        env = settings.runtime.environment.lower()
    else:
        allowed_origins = settings.get("api", {}).get("allowed_origins", [])
        env = settings.get("runtime", {}).get("environment", "development").lower()

    # CORS hardening in production
    is_prod = env in {"prod", "production"}
    if is_prod:
        if not allowed_origins or "*" in allowed_origins:
            raise RuntimeError(
                "CORS configuration error: ALLOWED_ORIGINS must be set to specific origins in production and cannot be empty or contain '*'"
            )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Optional rate‑limiting via SlowAPI
    try:
        from slowapi import Limiter, _rate_limit_exceeded_handler
        from slowapi.middleware import SlowAPIMiddleware
        from slowapi.util import get_remote_address
        from src.observability.middleware import RequestIDLoggingMiddleware

        # Add request‑id logging middleware
        app.add_middleware(RequestIDLoggingMiddleware)
        limiter = Limiter(key_func=get_remote_address)
        app.state.limiter = limiter
        app.add_exception_handler(
            getattr(limiter, "RateLimitExceeded", Exception),
            _rate_limit_exceeded_handler,
        )
        app.add_middleware(SlowAPIMiddleware)
    except Exception:  # pragma: no cover – SlowAPI optional
        pass

    # Register middleware & exception handlers
    from ..exceptions import register_exception_handlers, register_observability_middleware
    register_observability_middleware(app)
    register_exception_handlers(app)

    # Include routers (import lazily to avoid circular imports)
    from .routes.fraud_routes import router as fraud_router
    from .routes.blockchain_routes import router as blockchain_router
    from .routes.innovation_routes import router as innovation_router
    from .routes.health_routes import router as health_router
    from .routes.stream_routes import router as stream_router
    from .routes.websocket_routes import router as websocket_router

    app.include_router(fraud_router, prefix="/api/v1/fraud", tags=["Fraud"])
    app.include_router(blockchain_router, prefix="/api/v1/blockchain", tags=["Blockchain"])
    app.include_router(innovation_router, prefix="/api/v1/innovation", tags=["Innovation"])
    app.include_router(health_router, prefix="/api/v1/health", tags=["Health"])
    app.include_router(stream_router, prefix="/api/v1/stream", tags=["Streaming"])
    app.include_router(websocket_router, prefix="/api/v1/fraud", tags=["Streaming"])

    return app
