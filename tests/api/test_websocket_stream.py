# tests/api/test_websocket_stream.py
"""Integration tests for the WebSocket fraud stream endpoint."""

import os
import datetime
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.api.app_factory import create_app
from src.core.dependency_container import container


@pytest.fixture
def app() -> FastAPI:
    # Ensure environment is set to test with mock streaming
    os.environ["ENV"] = "test"
    os.environ["KAFKA_BOOTSTRAP_SERVERS"] = ""  # Triggers mock mode
    return create_app()


def test_websocket_stream_connection_and_ping(app: FastAPI):
    """Verify that clients can connect to the WebSocket stream and ping-pong works."""
    with TestClient(app) as client:
        with client.websocket_connect("/api/v1/fraud/stream/client_test_001") as websocket:
            websocket.send_text("ping")
            data = websocket.receive_text()
            assert data == "pong"
            
            # Verify the connection is active in the ws_manager
            ws_manager = container.get("websocket_manager")
            assert "client_test_001" in ws_manager.active_connections


def test_websocket_stream_broadcast_integration(app: FastAPI):
    """Verify that posting a transaction to /ingest broadcasts the results over WebSocket."""
    with TestClient(app) as client:
        # Start a websocket client connection
        with client.websocket_connect("/api/v1/fraud/stream/client_test_002") as websocket:
            # Trigger a transaction ingestion
            timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
            payload = {
                "transaction_id": "TXN_WS_001",
                "source_account": "ACC987654321",
                "target_account": "ACC123456789",
                "amount": 350.00,
                "currency": "INR",
                "mode": "UPI",
                "timestamp": timestamp
            }
            
            # Post transaction to ingest endpoint
            resp = client.post("/api/v1/stream/ingest", json=payload)
            assert resp.status_code == 202
            
            # Receive real-time scored event via the websocket
            event = websocket.receive_json()
            assert event["event_type"] == "transaction_scored"
            assert event["transaction"]["transaction_id"] == "TXN_WS_001"
            assert "result" in event
            assert "risk_score" in event["result"]
