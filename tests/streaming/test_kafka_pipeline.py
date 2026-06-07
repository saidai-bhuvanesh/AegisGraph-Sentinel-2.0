"""Integration and unit tests for the Kafka Streaming Pipeline."""

import asyncio
import datetime
import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from src.api.app_factory import create_app
from src.core.dependency_container import container
from src.streaming.consumer import get_mock_queue


@pytest.fixture
def app() -> FastAPI:
    # Ensure tests run in test environment using mock streaming wrappers
    import os
    os.environ["ENV"] = "test"
    os.environ["KAFKA_BOOTSTRAP_SERVERS"] = "" # Triggers mock mode
    return create_app()


@pytest_asyncio.fixture
async def async_client(app: FastAPI) -> AsyncClient:
    transport = ASGITransport(app=app)
    async with app.router.lifespan_context(app):
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            yield client


@pytest.mark.asyncio
async def test_stream_ingest_endpoint_success(async_client: AsyncClient):
    """Verify that posting to /ingest accepts the transaction and places it on the mock stream."""
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    payload = {
        "transaction_id": "TXN_STREAM_001",
        "source_account": "ACC987654321",
        "target_account": "ACC123456789",
        "amount": 150.00,
        "currency": "INR",
        "mode": "UPI",
        "timestamp": timestamp
    }
    
    # Ingest transaction via endpoint
    response = await async_client.post("/api/v1/stream/ingest", json=payload)
    assert response.status_code == 202
    assert response.json()["status"] == "ingested"
    assert response.json()["transaction_id"] == "TXN_STREAM_001"

    # Give the background mock consumer loop a brief moment to process the event
    await asyncio.sleep(0.5)
    
    # Verify transaction was processed in the mock broker storage
    producer = container.get("kafka_producer")
    assert "aegis-transactions" in producer._mock_broker
    mocked_messages = producer._mock_broker["aegis-transactions"]
    assert len(mocked_messages) >= 1
    assert mocked_messages[-1][0] == "TXN_STREAM_001"
    assert mocked_messages[-1][1]["amount"] == 150.00


@pytest.mark.asyncio
async def test_stream_ingest_endpoint_invalid(async_client: AsyncClient):
    """Verify that malformed payloads fail request validation prior to streaming ingestion."""
    payload = {
        "source_account": "ACC987654321",
        "target_account": "ACC123456789",
        "amount": -20.00, # Invalid amount (must be > 0)
    }
    response = await async_client.post("/api/v1/stream/ingest", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_consumer_dlq_routing_on_failure(async_client: AsyncClient):
    """Verify that message failures trigger retries and get routed to the DLQ topic."""
    import unittest.mock as mock
    from src.api.services.fraud_service import FraudService
    
    # Force mock mode and obtain producer
    producer = container.get("kafka_producer")
    
    # We will trigger a failure by mocking detect_fraud to raise an exception.
    with mock.patch.object(FraudService, "detect_fraud", side_effect=ValueError("Simulated processing error")):
        malformed_transaction = {
            "transaction_id": "TXN_BAD_001",
            "source_account": "ACC987654321",
            "target_account": "ACC123456789",
        }
        
        # Put directly to mock stream queue to bypass schema validation of API endpoints
        get_mock_queue().put_nowait(malformed_transaction)
        
        # Wait for consumer to process (3 retries + backoffs will take about 0.5s to 1s)
        # Our base backoff starts at 1s, but we can speed up the test by temporarily
        # adjusting the backoff config of the consumer.
        consumer = container.get("kafka_consumer")
        original_backoff = consumer._base_backoff_seconds
        consumer._base_backoff_seconds = 0.05 # Fast backoff for testing
        
        try:
            await asyncio.sleep(1.0)
        finally:
            consumer._base_backoff_seconds = original_backoff
            
    # Verify that it got routed to Dead-Letter Queue
    assert "aegis-transactions-dlq" in producer._mock_broker
    dlq_messages = producer._mock_broker["aegis-transactions-dlq"]
    assert len(dlq_messages) >= 1
    assert dlq_messages[0][0] == "TXN_BAD_001"
    assert dlq_messages[0][1]["routing_reason"] == "processing_retries_exhausted"
    assert "error" in dlq_messages[0][1]
