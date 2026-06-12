"""Threat Observatory API Routes"""
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from src.threat_observatory import get_observatory, ThreatType

router = APIRouter(prefix="/api/v1/observatory", tags=["observatory"])

class AddEventRequest(BaseModel):
    threat_type: str
    severity: float
    location: str

def verify_api_key(x_api_key: str = Header(None)) -> str:
    if x_api_key != "SUPER_ADMIN":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@router.get("/health")
async def health_check():
    return {"status": "healthy", "module": "observatory", "timestamp": datetime.now(timezone.utc).isoformat()}

@router.post("/events")
async def add_event(request: AddEventRequest, api_key: str = Header(None)):
    verify_api_key(api_key)
    obs = get_observatory()
    try:
        ttype = ThreatType(request.threat_type)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid type")
    event_id = obs.add_event(ttype, request.severity, request.location)
    return {"event_id": event_id, "status": "added"}

@router.get("/stats")
async def get_stats(api_key: str = Header(None)):
    verify_api_key(api_key)
    return get_observatory().get_stats()