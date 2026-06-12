"""
Enterprise Risk Brain API Routes
"""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Header, Query
from pydantic import BaseModel

from src.risk_brain import (
    EnterpriseRiskBrain,
    get_risk_brain,
    RiskCategory,
    ForecastHorizon,
)


router = APIRouter(prefix="/api/v1/risk-brain", tags=["risk-brain"])


class AssessRiskRequest(BaseModel):
    """Request to assess risk."""
    name: str
    risk_category: str
    factors: List[Dict[str, Any]] = []


def verify_api_key(x_api_key: str = Header(None)) -> str:
    """Verify API key."""
    if x_api_key != "SUPER_ADMIN":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "module": "risk_brain",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.post("/assess")
async def assess_risk(
    request: AssessRiskRequest,
    api_key: str = Header(None),
):
    """Assess risk for an entity."""
    verify_api_key(api_key)
    brain = get_risk_brain()
    
    try:
        category = RiskCategory(request.risk_category)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid risk category")
    
    result = brain.assess_risk(
        name=request.name,
        risk_category=category,
        factors=request.factors,
    )
    
    return result


@router.get("/entities")
async def list_entities(
    risk_category: Optional[str] = None,
    api_key: str = Header(None),
):
    """List risk entities."""
    verify_api_key(api_key)
    brain = get_risk_brain()
    
    entities = list(brain.risk_graph.entities.values())
    
    if risk_category:
        try:
            cat = RiskCategory(risk_category)
            entities = [e for e in entities if e.risk_category == cat]
        except ValueError:
            pass
    
    return {
        "count": len(entities),
        "entities": [e.to_dict() for e in entities],
    }


@router.get("/entities/{entity_id}")
async def get_entity(
    entity_id: str,
    api_key: str = Header(None),
):
    """Get a risk entity."""
    verify_api_key(api_key)
    brain = get_risk_brain()
    
    entity = brain.risk_graph.get_entity(entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    return {"entity": entity.to_dict()}


@router.get("/forecasts")
async def list_forecasts(
    entity_id: Optional[str] = None,
    horizon: Optional[str] = None,
    api_key: str = Header(None),
):
    """List risk forecasts."""
    verify_api_key(api_key)
    brain = get_risk_brain()
    
    forecasts = list(brain.forecast_engine.forecasts.values())
    
    if entity_id:
        forecasts = [f for f in forecasts if f.entity_id == entity_id]
    
    if horizon:
        try:
            h = ForecastHorizon(horizon)
            forecasts = [f for f in forecasts if f.horizon == h]
        except ValueError:
            pass
    
    return {
        "count": len(forecasts),
        "forecasts": [f.to_dict() for f in forecasts],
    }


@router.get("/recommendations")
async def list_recommendations(
    entity_id: Optional[str] = None,
    api_key: str = Header(None),
):
    """List risk recommendations."""
    verify_api_key(api_key)
    brain = get_risk_brain()
    
    if entity_id:
        recs = brain.recommendation_engine.get_recommendations_by_entity(entity_id)
    else:
        recs = list(brain.recommendation_engine.recommendations.values())
    
    return {
        "count": len(recs),
        "recommendations": [r.to_dict() for r in recs],
    }


@router.get("/analysis/{entity_id}")
async def analyze_risk(
    entity_id: str,
    api_key: str = Header(None),
):
    """Analyze risk for an entity."""
    verify_api_key(api_key)
    brain = get_risk_brain()
    
    try:
        analysis = brain.analytics.analyze_risk(entity_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"analysis": analysis.to_dict()}


@router.get("/dashboard")
async def get_executive_dashboard(api_key: str = Header(None)):
    """Get executive dashboard."""
    verify_api_key(api_key)
    brain = get_risk_brain()
    
    return brain.get_executive_dashboard()


@router.get("/summary")
async def get_risk_summary(api_key: str = Header(None)):
    """Get risk summary."""
    verify_api_key(api_key)
    brain = get_risk_brain()
    
    return brain.analytics.get_risk_summary()