# src/api/routes/fraud_routes.py
"""Fraud API router – uses the DI‑registered FraudService.

The router demonstrates dependency injection: FastAPI's ``Depends`` fetches the
service instance from the global ``container`` defined in
``src.core.dependency_container``.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from ..schemas import TransactionCheckRequest, TransactionCheckResponse, RiskBreakdown
from ..services.fraud_service import FraudService
from src.core.dependency_container import container

router = APIRouter()


def get_fraud_service() -> FraudService:
    """Retrieve the singleton ``FraudService`` from the DI container.
    ``register_services`` (called during app startup) guarantees the service
    is present.
    """
    try:
        return container.get("fraud_service")
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Fraud service unavailable") from exc


@router.post(
    "/check",
    response_model=TransactionCheckResponse,
    tags=["Fraud"],
)
async def check_transaction(
    request: TransactionCheckRequest,
    fraud_service: FraudService = Depends(get_fraud_service),
):
    """Endpoint that delegates fraud detection to ``FraudService``.
    Returns a ``TransactionCheckResponse`` containing the risk score and a
    boolean ``is_fraud`` flag.
    """
    import datetime
    
    start_time = datetime.datetime.now(datetime.timezone.utc)
    result = fraud_service.detect_fraud(request.dict())
    
    raw_score = result["risk_score"]
    risk_score = raw_score / 100.0  # Scale to [0, 1]
    
    # Decide decision
    if raw_score >= 80.0:
        decision = "BLOCK"
    elif raw_score >= 50.0:
        decision = "REVIEW"
    else:
        decision = "ALLOW"
        
    breakdown = RiskBreakdown(
        graph=risk_score * 0.4,
        velocity=risk_score * 0.3,
        behavior=risk_score * 0.2,
        entropy=risk_score * 0.1
    )
    
    end_time = datetime.datetime.now(datetime.timezone.utc)
    processing_time_ms = (end_time - start_time).total_seconds() * 1000.0
    
    return TransactionCheckResponse(
        transaction_id=request.transaction_id,
        risk_score=risk_score,
        decision=decision,
        factors={
            "graph": risk_score * 0.4,
            "velocity": risk_score * 0.3,
            "behavior": risk_score * 0.2,
            "entropy": risk_score * 0.1
        },
        confidence=0.95 if decision != "REVIEW" else 0.70,
        breakdown=breakdown,
        explanation=f"Transaction risk evaluated with score {raw_score}. Decision: {decision}.",
        recommended_action="BLOCK_TRANSACTION" if decision == "BLOCK" else ("MANUAL_REVIEW" if decision == "REVIEW" else "NONE"),
        processing_time_ms=processing_time_ms,
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
        honeypot_activated=False,
        honeypot_id=None,
        deceptive_success_response=False,
        blockchain_evidence_id=None,
        behavioral_stress_detected=False,
        lateral_movement_detected=False
    )
