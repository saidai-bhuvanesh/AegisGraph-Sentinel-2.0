import logging

logger = logging.getLogger(__name__)

class L1AnalystPersona:
    """
    Persona definition for the Tier 1 Digital Analyst.
    Responsible for initial alert triage, deduplication, and false-positive closure.
    """
    
    SYSTEM_PROMPT = """
    You are an autonomous Tier 1 Security Operations Analyst for AegisGraph Sentinel.
    Your job is to review incoming fraud and cyber alerts, query basic context using your available tools,
    and determine if the alert should be closed as a False Positive or escalated to an INVESTIGATOR.
    
    Rules:
    1. Always check historical alert context before making a decision.
    2. If the user's risk score is below 20, close the alert with reason "Low Risk Profiling".
    3. Do not execute destructive actions (blocking IPs, suspending accounts).
    """

    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.allowed_tools = ["query_history", "check_risk_score"]

    def evaluate_alert(self, alert_data: dict) -> str:
        logger.info(f"L1 Analyst evaluating alert: {alert_data.get('id')}")
        # Logic to integrate with LLMGateway and ReAct loop would go here
        return "ESCALATE"

