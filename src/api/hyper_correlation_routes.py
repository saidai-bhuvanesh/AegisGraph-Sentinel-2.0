"""Hyper Correlation API Routes"""
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from src.hyper_correlation import get_correlation_engine, CorrelationType

router = APIRouter(prefix="/api/v1/hyper-correlation", tags=["hyper-correlation"])

class CorrelateRequest(BaseModel):
    correlation_type: str
    related_events: list = []

def verify_api_key(x_api_key: str = Header(None)) -> str:
    if x_api_key != "SUPER_ADMIN":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@router.get("/health")
async def health_check():
    return {"status": "healthy", "module": "hyper-correlation", "timestamp": datetime.now(timezone.utc).isoformat()}

@router.post("/correlate")
async def correlate(request: CorrelateRequest, api_key: str = Header(None)):
    verify_api_key(api_key)
    try:
        ctype = CorrelationType(request.correlation_type)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid type")
    event_id = get_correlation_engine().correlate(ctype, request.related_events)
    return {"event_id": event_id, "status": "correlated"}

@router.get("/stats")
async def get_stats(api_key: str = Header(None)):
    verify_api_key(api_key)
    return get_correlation_engine().get_stats()