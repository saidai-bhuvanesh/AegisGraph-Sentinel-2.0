# src/api/routes/websocket_routes.py
"""WebSocket routing for AegisGraph Sentinel 2.0."""

from __future__ import annotations

import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.core.dependency_container import container

logger = logging.getLogger("api.websocket_routes")
router = APIRouter()


@router.websocket("/stream/{client_id}")
async def fraud_stream_websocket(websocket: WebSocket, client_id: str):
    """Real-time fraud monitoring stream.

    Accepts client WebSocket connections, verifies reconnect limits, and loops
    for heartbeat 'ping' ping-pongs to keep connection active.
    """
    try:
        ws_manager = container.get("websocket_manager")
    except KeyError:
        logger.error("websocket_manager not registered in container. Rejecting connection.")
        await websocket.close(code=1011, reason="WebSocket server uninitialized")
        return

    accepted = await ws_manager.connect(websocket, client_id)
    if not accepted:
        return

    try:
        while True:
            data = await websocket.receive_text()
            if data.strip().lower() == "ping":
                await ws_manager.heartbeat(client_id)
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        await ws_manager.disconnect(client_id)
    except Exception as exc:
        logger.error(f"WebSocket error on client {client_id}: {exc}")
        await ws_manager.disconnect(client_id)


async def websocket_cleanup_loop(interval_seconds: int = 30) -> None:
    """Periodically clean up stale WebSocket connections."""
    import asyncio
    try:
        ws_manager = container.get("websocket_manager")
    except KeyError:
        logger.error("websocket_manager not registered in container. Exiting cleanup loop.")
        return

    try:
        while True:
            await asyncio.sleep(interval_seconds)
            try:
                await ws_manager.cleanup_stale_connections()
            except Exception as exc:
                logger.warning(f"WebSocket stale connection cleanup failed: {exc}")
    except asyncio.CancelledError:
        logger.info("WebSocket stale connection cleanup loop stopped")
        raise
