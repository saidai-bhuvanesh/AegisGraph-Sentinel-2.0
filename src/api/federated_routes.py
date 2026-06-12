"""Federated Learning API Routes"""
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from src.federated_learning import get_federated_engine, NodeRole

router = APIRouter(prefix="/api/v1/federated", tags=["federated"])

class RegisterNodeRequest(BaseModel):
    name: str
    role: str = "PARTICIPANT"

def verify_api_key(x_api_key: str = Header(None)) -> str:
    if x_api_key != "SUPER_ADMIN":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@router.get("/health")
async def health_check():
    return {"status": "healthy", "module": "federated", "timestamp": datetime.now(timezone.utc).isoformat()}

@router.post("/nodes")
async def register_node(request: RegisterNodeRequest, api_key: str = Header(None)):
    verify_api_key(api_key)
    try:
        role = NodeRole(request.role)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid role")
    node_id = get_federated_engine().register_node(request.name, role)
    return {"node_id": node_id, "status": "registered"}

@router.get("/stats")
async def get_stats(api_key: str = Header(None)):
    verify_api_key(api_key)
    return get_federated_engine().get_stats()