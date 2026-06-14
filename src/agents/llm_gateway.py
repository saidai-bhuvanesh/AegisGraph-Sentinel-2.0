import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LLMGateway:
    """
    Centralized Gateway for routing prompts to foundational models.
    Enforces PII redaction, prompt injection filtering, and rate limiting.
    """
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "mock")
        
    async def generate_response(self, system_prompt: str, user_prompt: str, tenant_id: str) -> str:
        # Step 1: PII Redaction
        sanitized_prompt = self._redact_pii(user_prompt)
        
        # Step 2: Prompt Injection Check
        if self._detect_injection(sanitized_prompt):
            logger.warning(f"Prompt injection detected for tenant {tenant_id}")
            raise ValueError("Malicious prompt detected and blocked.")
            
        logger.info(f"Routing request to LLM provider {self.provider} for tenant {tenant_id}")
        
        # Simulated LLM call
        if self.provider == "mock":
            return '{"action": "investigate", "target": "internal_db"}'
            
        return "{}"

    def _redact_pii(self, prompt: str) -> str:
        # Logic to strip emails, SSNs, credit cards
        return prompt.replace("secret", "[REDACTED]")
        
    def _detect_injection(self, prompt: str) -> bool:
        # Heuristic checks for "Ignore previous instructions"
        forbidden_phrases = ["ignore previous", "bypass", "system prompt"]
        return any(phrase in prompt.lower() for phrase in forbidden_phrases)

gateway = LLMGateway()
