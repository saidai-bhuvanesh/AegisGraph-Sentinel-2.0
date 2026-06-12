"""Cyber Genome API Routes"""
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from src.cyber_genome import get_cyber_genome_engine, GenomeType

router = APIRouter(prefix="/api/v1/cyber-genome", tags=["cyber-genome"])

class DiscoverRequest(BaseModel):
    name: str
    genome_type: str
    indicators: list = []

def verify_api_key(x_api_key: str = Header(None)) -> str:
    if x_api_key != "SUPER_ADMIN":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@router.get("/health")
async def health_check():
    return {"status": "healthy", "module": "cyber-genome", "timestamp": datetime.now(timezone.utc).isoformat()}

@router.post("/discover")
async def discover_genome(request: DiscoverRequest, api_key: str = Header(None)):
    verify_api_key(api_key)
    try:
        gtype = GenomeType(request.genome_type)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid type")
    genome_id = get_cyber_genome_engine().discover_genome(request.name, gtype, request.indicators)
    return {"genome_id": genome_id, "status": "discovered"}

@router.get("/stats")
async def get_stats(api_key: str = Header(None)):
    verify_api_key(api_key)
    return get_cyber_genome_engine().get_stats()