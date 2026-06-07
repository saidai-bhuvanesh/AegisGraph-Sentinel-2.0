# src/api/routes/blockchain_routes.py
"""Blockchain API router – placeholder implementation.

In a full system this would expose endpoints for sealing, verifying, and
exporting blockchain evidence. For now we provide minimal stubs that return
static responses so the router can be imported and the app remains functional.
"""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class SealRequest(BaseModel):
    data: str

class SealResponse(BaseModel):
    seal_id: str
    status: str = "sealed"

@router.post("/seal", response_model=SealResponse)
async def seal(request: SealRequest):
    # In production this would create a blockchain seal.
    return SealResponse(seal_id=f"seal-{hash(request.data) % 10000}")


class VerifyRequest(BaseModel):
    seal_id: str

class VerifyResponse(BaseModel):
    seal_id: str
    valid: bool

@router.post("/verify", response_model=VerifyResponse)
async def verify(request: VerifyRequest):
    # Dummy verification logic – always true for demo.
    return VerifyResponse(seal_id=request.seal_id, valid=True)


class ExportResponse(BaseModel):
    seal_id: str
    export_data: str

@router.get("/export/{seal_id}", response_model=ExportResponse)
async def export(seal_id: str):
    # Dummy export – returns placeholder data.
    return ExportResponse(seal_id=seal_id, export_data="{\"dummy\": true}")
