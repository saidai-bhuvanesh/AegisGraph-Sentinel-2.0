"""
FastAPI routing endpoints for Financial Ecosystem Risk Platform
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Dict, List, Any, Optional
from .schemas import ExecutionRequest, ExecutionResponse
from .service import FinancialEcosystemRiskPlatformService, get_service

router = APIRouter(prefix="/api/v1/phase145", tags=["Phase145"])

def verify_rbac(x_api_key: str = Header(None)) -> str:
    if x_api_key != "SUPER_ADMIN":
        raise HTTPException(status_code=401, detail="Unauthorized access")
    return x_api_key

@router.get("/status")
async def get_status(api_key: str = Depends(verify_rbac)):
    return {"status": "healthy", "phase": 145, "name": "Financial Ecosystem Risk Platform"}

@router.post("/execute", response_model=ExecutionResponse)
async def execute_module(request: ExecutionRequest, api_key: str = Depends(verify_rbac)):
    srv = get_service()
    res = srv.execute(request.tenant_id, request.parameters)
    return ExecutionResponse(status="success", phase=145, result=res)
