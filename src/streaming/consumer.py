"""Asynchronous Kafka Consumer Worker with Retry and DLQ routing."""

from __future__ import annotations

import asyncio
import json
from typing import Any, Dict, Optional
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError

from src.observability import get_logger
from src.core.dependency_container import container
from src.streaming.producer import KafkaProducerWrapper

logger = get_logger("streaming.consumer")

# Shared queue reference for in-memory mock fallback in dev/test environments
_MOCK_STREAM_QUEUE: Optional[asyncio.Queue[Dict[str, Any]]] = None


class KafkaConsumerWorker:
    """Kafka background consumer worker with built-in retry and DLQ logic."""

    def __init__(self, bootstrap_servers: str, group_id: str, topic: str) -> None:
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.topic = topic
        self._consumer: Optional[AIOKafkaConsumer] = None
        self._mock_mode = False
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._max_retries = 3
        self._base_backoff_seconds = 1.0

    async def start(self) -> None:
        """Start the consumer background worker task."""
        self._running = True
        
        # Check if we should fall back to mock mode
        if not self.bootstrap_servers:
            logger.warning(
                "No Kafka bootstrap servers specified. Running consumer in MOCK mode.",
                event_type="streaming_consumer_mock_mode_no_config",
            )
            self._mock_mode = True
            self._task = asyncio.create_task(self._mock_consume_loop())
            return

        try:
            self._consumer = AIOKafkaConsumer(
                self.topic,
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                enable_auto_commit=True,
                auto_offset_reset="latest",
                request_timeout_ms=5000,
                bootstrap_timeout_ms=5000,
            )
            await self._consumer.start()
            self._mock_mode = False
            self._task = asyncio.create_task(self._consume_loop())
            logger.info(
                f"Kafka consumer worker started on topic '{self.topic}'.",
                event_type="streaming_consumer_started",
                metadata={"topic": self.topic, "group_id": self.group_id},
            )
        except (KafkaConnectionError, Exception) as exc:
            logger.warning(
                f"Failed to start Kafka consumer at {self.bootstrap_servers} ({exc}). Falling back to local MOCK loop.",
                event_type="streaming_consumer_fallback_to_mock",
                metadata={"exception": str(exc)},
            )
            self._mock_mode = True
            self._consumer = None
            self._task = asyncio.create_task(self._mock_consume_loop())

    async def stop(self) -> None:
        """Gracefully stop the consumer worker task and commit offsets."""
        self._running = False
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

        if not self._mock_mode and self._consumer is not None:
            logger.info("Stopping Kafka consumer...", event_type="streaming_consumer_stopping")
            try:
                await self._consumer.stop()
                logger.info("Kafka consumer stopped successfully.", event_type="streaming_consumer_stopped")
            except Exception as exc:
                logger.error(
                    f"Error stopping Kafka consumer: {exc}",
                    event_type="streaming_consumer_stop_error",
                    metadata={"exception": str(exc)},
                )

    async def _consume_loop(self) -> None:
        """Main Kafka polling and consumption loop."""
        if self._consumer is None:
            return
            
        try:
            async for message in self._consumer:
                if not self._running:
                    break
                await self._process_message_with_retry(message.value)
        except asyncio.CancelledError:
            pass
        except Exception as exc:
            logger.error(
                f"Exception in Kafka consumer loop: {exc}",
                event_type="streaming_consumer_loop_crash",
                metadata={"exception": str(exc)},
            )

    async def _mock_consume_loop(self) -> None:
        """In-memory mock consumption loop for local dev and testing."""
        logger.info(
            f"Mock consumption loop active for topic '{self.topic}'.",
            event_type="mock_consumer_loop_active",
        )
        try:
            while self._running:
                # Fetch message from the shared mock queue
                queue = get_mock_queue()
                value = await queue.get()
                try:
                    await self._process_message_with_retry(value)
                finally:
                    queue.task_done()
        except asyncio.CancelledError:
            pass

    async def _process_message_with_retry(self, transaction: Dict[str, Any]) -> None:
        """Processes transaction message, applying retry backoff and DLQ routing on exhaustion."""
        retries = 0
        while retries <= self._max_retries:
            try:
                await self._process_transaction(transaction)
                return  # Success!
            except Exception as exc:
                retries += 1
                if retries <= self._max_retries:
                    backoff = self._base_backoff_seconds * (2 ** (retries - 1))
                    logger.warning(
                        f"Temporary processing error on transaction (attempt {retries}/{self._max_retries+1}): {exc}. Backing off for {backoff}s.",
                        event_type="streaming_processing_retry",
                        metadata={"retry_attempt": retries, "backoff_seconds": backoff, "exception": str(exc)},
                    )
                    await asyncio.sleep(backoff)
                else:
                    logger.error(
                        f"Retries exhausted for transaction. Routing to DLQ. Error: {exc}",
                        event_type="streaming_processing_failed_dlq",
                        metadata={"exception": str(exc)},
                    )
                    await self._route_to_dlq(transaction, exc)

    async def _process_transaction(self, transaction: Dict[str, Any]) -> None:
        """Executes actual scoring and fraud detection pipeline."""
        logger.info(
            f"Consuming transaction '{transaction.get('transaction_id')}'",
            event_type="streaming_message_consumed",
            metadata={"transaction_id": transaction.get("transaction_id")},
        )
        
        # Fetch the DI container registered FraudService
        fraud_service = container.get("fraud_service")
        
        # Execute fraud check logic
        result = fraud_service.detect_fraud(transaction)
        logger.info(
            f"Processed transaction '{transaction.get('transaction_id')}'. Score: {result['risk_score']}. Fraud: {result['is_fraud']}",
            event_type="streaming_transaction_scored",
            metadata={
                "transaction_id": transaction.get("transaction_id"),
                "risk_score": result["risk_score"],
                "is_fraud": result["is_fraud"],
            },
        )
        
        # Broadcast the decision to WebSocket clients for real-time dashboard updates
        try:
            ws_manager = container.optional_get("websocket_manager")
            if ws_manager is not None:
                await ws_manager.broadcast({
                    "event_type": "transaction_scored",
                    "transaction": transaction,
                    "result": {
                        "risk_score": result["risk_score"],
                        "is_fraud": result["is_fraud"],
                    }
                })
        except Exception as exc:
            logger.warning(
                f"Failed to broadcast transaction scored event via WebSocket: {exc}",
                event_type="websocket_broadcast_error"
            )
        
        # If it is high risk or fraud, send alert downstream
        if result["is_fraud"] or result["risk_score"] >= 50.0:
            await self._send_alert(transaction, result)

    async def _send_alert(self, transaction: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Dispatches an alert downstream to the aegis-alerts topic."""
        producer: Optional[KafkaProducerWrapper] = container.optional_get("kafka_producer")
        if producer is None:
            return
            
        alert_payload = {
            "transaction_id": transaction.get("transaction_id"),
            "risk_score": result["risk_score"] / 100.0, # Scale to 0-1
            "decision": "BLOCK" if result["is_fraud"] else "REVIEW",
            "source_account": transaction.get("source_account"),
            "target_account": transaction.get("target_account"),
            "amount": transaction.get("amount"),
            "currency": transaction.get("currency"),
            "timestamp": transaction.get("timestamp"),
            "reason": f"High risk transaction detected on stream. Score: {result['risk_score']}",
        }
        
        await producer.send_json(
            topic="aegis-alerts",
            value=alert_payload,
            key=transaction.get("transaction_id"),
        )

    async def _route_to_dlq(self, transaction: Dict[str, Any], exception: Exception) -> None:
        """Publishes failed message payload to Dead-Letter Queue."""
        producer: Optional[KafkaProducerWrapper] = container.optional_get("kafka_producer")
        if producer is None:
            return
            
        dlq_payload = {
            "original_payload": transaction,
            "error": str(exception),
            "error_type": exception.__class__.__name__,
            "routing_reason": "processing_retries_exhausted",
        }
        
        await producer.send_json(
            topic="aegis-transactions-dlq",
            value=dlq_payload,
            key=transaction.get("transaction_id"),
        )


def get_mock_queue() -> asyncio.Queue[Dict[str, Any]]:
    """Returns the shared queue used to pass messages locally in mock mode.
    
    Dynamically creates/resets the queue bound to the current event loop if needed.
    """
    global _MOCK_STREAM_QUEUE
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        if _MOCK_STREAM_QUEUE is None:
            _MOCK_STREAM_QUEUE = asyncio.Queue()
        return _MOCK_STREAM_QUEUE

    if _MOCK_STREAM_QUEUE is None or getattr(_MOCK_STREAM_QUEUE, "_loop", None) is not loop:
        _MOCK_STREAM_QUEUE = asyncio.Queue()
    return _MOCK_STREAM_QUEUE
