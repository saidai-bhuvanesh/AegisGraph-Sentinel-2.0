# tests/api/test_integration.py
import datetime
import os
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
import pytest
import pytest_asyncio

from src.api.app_factory import create_app

@pytest.fixture(scope="module")
def app() -> FastAPI:
    # Ensure environment is set for development
    os.environ["ENV"] = "dev"
    return create_app()

@pytest_asyncio.fixture(scope="module")
async def async_client(app: FastAPI) -> AsyncClient:
    transport = ASGITransport(app=app)
    async with app.router.lifespan_context(app):
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            yield client

# Basic health check integration test
@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    response = await async_client.get("/api/v1/health/")
    assert response.status_code == 200
    json_body = response.json()
    assert "status" in json_body
    assert json_body["status"] == "healthy"

# Detailed health endpoint test
@pytest.mark.asyncio
async def test_health_details(async_client: AsyncClient):
    response = await async_client.get("/api/v1/health/details")
    assert response.status_code == 200
    json_body = response.json()
    assert "uptime_seconds" in json_body
    assert isinstance(json_body["uptime_seconds"], (int, float))

# Fraud check endpoint success case
@pytest.mark.asyncio
async def test_fraud_check_success(async_client: AsyncClient):
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    payload = {
        "transaction_id": "TXN_INT_001",
        "source_account": "ACC987654321",
        "target_account": "ACC123456789",
        "amount": 250.00,
        "currency": "INR",
        "mode": "UPI",
        "timestamp": timestamp
    }
    response = await async_client.post("/api/v1/fraud/check", json=payload)
    assert response.status_code == 200
    json_body = response.json()
    assert "risk_score" in json_body
    assert "decision" in json_body

# Fraud check endpoint validation error
@pytest.mark.asyncio
async def test_fraud_check_invalid(async_client: AsyncClient):
    # Pass a malformed payload (missing required field transaction_id)
    payload = {
        "source_account": "ACC987654321",
        "target_account": "ACC123456789",
        "amount": -50.0,  # invalid amount (must be > 0)
    }
    response = await async_client.post("/api/v1/fraud/check", json=payload)
    assert response.status_code == 422  # FastAPI validation error
