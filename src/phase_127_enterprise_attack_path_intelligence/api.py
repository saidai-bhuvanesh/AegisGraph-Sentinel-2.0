"""
FastAPI routing endpoints for Enterprise Attack Path Intelligence Platform
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Dict, List, Any, Optional
from .schemas import ExecutionRequest, ExecutionResponse
from .service import EnterpriseAttackPathIntelligencePlatformService, get_service

router = APIRouter(prefix="/api/v1/phase127", tags=["Phase127"])

def verify_rbac(x_api_key: str = Header(None)) -> str:
    if x_api_key != "SUPER_ADMIN":
        raise HTTPException(status_code=401, detail="Unauthorized access")
    return x_api_key

@router.get("/status")
async def get_status(api_key: str = Depends(verify_rbac)):
    return {"status": "healthy", "phase": 127, "name": "Enterprise Attack Path Intelligence Platform"}

@router.post("/execute", response_model=ExecutionResponse)
async def execute_module(request: ExecutionRequest, api_key: str = Depends(verify_rbac)):
    srv = get_service()
    res = srv.execute(request.tenant_id, request.parameters)
    return ExecutionResponse(status="success", phase=127, result=res)
