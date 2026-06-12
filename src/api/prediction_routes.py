"""Threat Prediction API Routes"""
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from src.threat_prediction import get_prediction_engine, PredictionType

router = APIRouter(prefix="/api/v1/prediction", tags=["prediction"])

class PredictRequest(BaseModel):
    prediction_type: str
    description: str = ""

def verify_api_key(x_api_key: str = Header(None)) -> str:
    if x_api_key != "SUPER_ADMIN":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@router.get("/health")
async def health_check():
    return {"status": "healthy", "module": "prediction", "timestamp": datetime.now(timezone.utc).isoformat()}

@router.post("/predict")
async def predict(request: PredictRequest, api_key: str = Header(None)):
    verify_api_key(api_key)
    try:
        ptype = PredictionType(request.prediction_type)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid type")
    pred_id = get_prediction_engine().predict(ptype, request.description)
    return {"prediction_id": pred_id, "status": "predicted"}

@router.get("/stats")
async def get_stats(api_key: str = Header(None)):
    verify_api_key(api_key)
    return get_prediction_engine().get_stats()