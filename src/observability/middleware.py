# src/observability/middleware.py
"""Observability middleware for request tracing and JSON logging.

Provides:
- A unique ``request_id`` (UUID) attached to ``request.state`` for downstream
  handlers.
- Structured JSON logs for request start and response completion, including
  method, path, status code, duration, and the request_id.

The middleware is deliberately lightweight and does not depend on external
logging frameworks beyond the standard library ``logging``. It can be added
to the FastAPI app via ``app.add_middleware``.
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("observability")
logger.setLevel(logging.INFO)
# Ensure at least one handler (stdout) – in real deployments configure handlers elsewhere.
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class RequestIDLoggingMiddleware(BaseHTTPMiddleware):
    """Inject a ``request_id`` into the request state and emit JSON logs.

    The middleware logs two events:
    1. **request_start** – when the request is received.
    2. **request_end** – after the response is generated.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        start_time = time.time()

        # Log request start
        logger.info(
            json.dumps(
                {
                    "event": "request_start",
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "timestamp": time.time(),
                }
            )
        )

        # Process request
        response = await call_next(request)

        duration_ms = (time.time() - start_time) * 1000
        # Log request end
        logger.info(
            json.dumps(
                {
                    "event": "request_end",
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": round(duration_ms, 2),
                    "timestamp": time.time(),
                }
            )
        )
        return response
