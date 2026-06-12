"""Intelligence Federation API Routes"""
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from src.intelligence_federation import get_federation_engine, IndustryType, FederationRole

router = APIRouter(prefix="/api/v1/federation", tags=["federation"])

class JoinRequest(BaseModel):
    organization: str
    industry: str
    role: str = "BOTH"

def verify_api_key(x_api_key: str = Header(None)) -> str:
    if x_api_key != "SUPER_ADMIN":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@router.get("/health")
async def health_check():
    return {"status": "healthy", "module": "federation", "timestamp": datetime.now(timezone.utc).isoformat()}

@router.post("/join")
async def join_federation(request: JoinRequest, api_key: str = Header(None)):
    verify_api_key(api_key)
    engine = get_federation_engine()
    try:
        industry = IndustryType(request.industry)
        role = FederationRole(request.role)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid type")
    member_id = engine.join_federation(request.organization, industry, role)
    return {"member_id": member_id, "status": "joined"}

@router.get("/members")
async def list_members(api_key: str = Header(None)):
    verify_api_key(api_key)
    engine = get_federation_engine()
    members = list(engine.registry.members.values())
    return {"count": len(members), "members": [m.to_dict() for m in members]}

@router.get("/stats")
async def get_stats(api_key: str = Header(None)):
    verify_api_key(api_key)
    return get_federation_engine().get_federation_stats()