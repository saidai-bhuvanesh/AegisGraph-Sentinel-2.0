"""Trust Network API Routes"""
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from src.trust_network import get_trust_engine

router = APIRouter(prefix="/api/v1/trust", tags=["trust"])

class AddEntityRequest(BaseModel):
    name: str
    initial_score: float = 0.5

def verify_api_key(x_api_key: str = Header(None)) -> str:
    if x_api_key != "SUPER_ADMIN":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@router.get("/health")
async def health_check():
    return {"status": "healthy", "module": "trust", "timestamp": datetime.now(timezone.utc).isoformat()}

@router.post("/entities")
async def add_entity(request: AddEntityRequest, api_key: str = Header(None)):
    verify_api_key(api_key)
    entity_id = get_trust_engine().add_entity(request.name, request.initial_score)
    return {"entity_id": entity_id, "status": "added"}

@router.get("/stats")
async def get_stats(api_key: str = Header(None)):
    verify_api_key(api_key)
    return get_trust_engine().get_stats()