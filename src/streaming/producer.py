"""Asynchronous Kafka Producer Wrapper with local mock fallback."""

from __future__ import annotations

import json
from typing import Any, Dict, Optional
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaConnectionError

from src.observability import get_logger

logger = get_logger("streaming.producer")


class KafkaProducerWrapper:
    """Asynchronous Kafka producer supporting graceful mock fallback in dev."""

    def __init__(self, bootstrap_servers: str) -> None:
        self.bootstrap_servers = bootstrap_servers
        self._producer: Optional[AIOKafkaProducer] = None
        self._mock_mode = False
        self._mock_broker: Dict[str, list] = {}

    async def start(self) -> None:
        """Start the producer. Falls back to mock mode if connection fails."""
        if not self.bootstrap_servers:
            logger.warning(
                "No Kafka bootstrap servers specified. Running in MOCK mode.",
                event_type="streaming_producer_mock_mode_no_config",
            )
            self._mock_mode = True
            return

        logger.info(
            f"Starting Kafka producer pointing to {self.bootstrap_servers}",
            event_type="streaming_producer_starting",
            metadata={"bootstrap_servers": self.bootstrap_servers},
        )
        
        try:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                request_timeout_ms=5000,
                bootstrap_timeout_ms=5000,
            )
            await self._producer.start()
            self._mock_mode = False
            logger.info(
                "Kafka producer started successfully.",
                event_type="streaming_producer_started",
            )
        except (KafkaConnectionError, Exception) as exc:
            logger.warning(
                f"Failed to connect to Kafka broker at {self.bootstrap_servers} ({exc}). Falling back to local MOCK mode.",
                event_type="streaming_producer_fallback_to_mock",
                metadata={"exception": str(exc)},
            )
            self._mock_mode = True
            self._producer = None

    async def stop(self) -> None:
        """Stop the producer, flushing any outstanding messages."""
        if self._mock_mode or self._producer is None:
            logger.info("Stopping mock Kafka producer.", event_type="streaming_producer_stopped")
            return

        logger.info("Stopping Kafka producer (draining messages)...", event_type="streaming_producer_stopping")
        try:
            await self._producer.stop()
            logger.info("Kafka producer stopped successfully.", event_type="streaming_producer_stopped")
        except Exception as exc:
            logger.error(
                f"Error stopping Kafka producer: {exc}",
                event_type="streaming_producer_stop_error",
                metadata={"exception": str(exc)},
            )

    async def send_json(self, topic: str, value: Any, key: Optional[str] = None) -> bool:
        """Publish a JSON payload to a Kafka topic."""
        key_bytes = key.encode("utf-8") if key is not None else None
        
        if self._mock_mode:
            logger.info(
                f"[MOCK KAFKA] Publish to '{topic}': {value}",
                event_type="mock_kafka_publish",
                metadata={"topic": topic, "key": key},
            )
            if topic not in self._mock_broker:
                self._mock_broker[topic] = []
            self._mock_broker[topic].append((key, value))
            
            if topic == "aegis-transactions":
                from src.streaming.consumer import get_mock_queue
                get_mock_queue().put_nowait(value)
            return True

        if self._producer is None:
            logger.error(
                f"Cannot publish message to '{topic}'. Producer not initialized.",
                event_type="streaming_producer_uninitialized",
            )
            return False

        try:
            await self._producer.send_and_wait(topic, value=value, key=key_bytes)
            logger.info(
                f"Published message to '{topic}' successfully.",
                event_type="streaming_message_published",
                metadata={"topic": topic, "key": key},
            )
            return True
        except Exception as exc:
            logger.error(
                f"Failed to publish message to '{topic}': {exc}",
                event_type="streaming_publish_failed",
                metadata={"topic": topic, "key": key, "exception": str(exc)},
            )
            return False
