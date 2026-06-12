"""MLOps Platform API Routes"""
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from src.mlops_platform import get_mlops_engine

router = APIRouter(prefix="/api/v1/mlops", tags=["mlops"])

class RegisterRequest(BaseModel):
    name: str
    version: str

def verify_api_key(x_api_key: str = Header(None)) -> str:
    if x_api_key != "SUPER_ADMIN":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@router.get("/health")
async def health_check():
    return {"status": "healthy", "module": "mlops", "timestamp": datetime.now(timezone.utc).isoformat()}

@router.post("/register")
async def register_model(request: RegisterRequest, api_key: str = Header(None)):
    verify_api_key(api_key)
    model_id = get_mlops_engine().register_model(request.name, request.version)
    return {"model_id": model_id, "status": "registered"}

@router.get("/models")
async def list_models(api_key: str = Header(None)):
    verify_api_key(api_key)
    engine = get_mlops_engine()
    return {"count": len(engine.models), "models": [m.to_dict() for m in engine.models.values()]}

@router.get("/stats")
async def get_stats(api_key: str = Header(None)):
    verify_api_key(api_key)
    return get_mlops_engine().get_stats()