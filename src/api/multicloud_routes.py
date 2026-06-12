"""Multi-Cloud Fabric API Routes"""
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from src.multicloud_fabric import get_multicloud_fabric, CloudProvider

router = APIRouter(prefix="/api/v1/multicloud", tags=["multicloud"])

class AddConnectorRequest(BaseModel):
    provider: str

def verify_api_key(x_api_key: str = Header(None)) -> str:
    if x_api_key != "SUPER_ADMIN":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@router.get("/health")
async def health_check():
    return {"status": "healthy", "module": "multicloud", "timestamp": datetime.now(timezone.utc).isoformat()}

@router.post("/connectors")
async def add_connector(request: AddConnectorRequest, api_key: str = Header(None)):
    verify_api_key(api_key)
    try:
        provider = CloudProvider(request.provider)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid provider")
    connector_id = get_multicloud_fabric().add_connector(provider)
    return {"connector_id": connector_id, "status": "connected"}

@router.get("/stats")
async def get_stats(api_key: str = Header(None)):
    verify_api_key(api_key)
    return get_multicloud_fabric().get_stats()