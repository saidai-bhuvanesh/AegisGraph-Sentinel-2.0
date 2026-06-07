"""Stream routing endpoints for AegisGraph Sentinel 2.0."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from src.api.schemas import TransactionCheckRequest
from src.core.dependency_container import container
from src.streaming.producer import KafkaProducerWrapper

router = APIRouter()


def get_kafka_producer() -> KafkaProducerWrapper:
    """Retrieve the singleton KafkaProducerWrapper from the DI container."""
    try:
        producer = container.get("kafka_producer")
        return producer
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Kafka producer service unavailable"
        ) from exc


@router.post(
    "/ingest",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Streaming"],
    summary="Ingest transaction to event stream",
    description="Validate and push a transaction to the Kafka event queue for async fraud analysis."
)
async def ingest_transaction(
    request: TransactionCheckRequest,
    producer: KafkaProducerWrapper = Depends(get_kafka_producer),
):
    """Ingest a validated transaction payload into the streaming pipeline."""
    payload = request.model_dump()
    success = await producer.send_json(
        topic="aegis-transactions",
        value=payload,
        key=request.transaction_id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to publish transaction payload to streaming queue"
        )
        
    return {
        "status": "ingested",
        "transaction_id": request.transaction_id,
        "message": "Transaction queued for real-time fraud analysis"
    }
