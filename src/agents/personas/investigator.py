import logging

logger = logging.getLogger(__name__)

class InvestigatorPersona:
    """
    Persona definition for the Tier 2 Digital Investigator.
    Responsible for deep-dive graph investigations, threat correlation, and dossier generation.
    """
    
    SYSTEM_PROMPT = """
    You are an autonomous Tier 2 Security Investigator for AegisGraph Sentinel.
    Your job is to take escalated alerts, utilize the Neo4j Cypher tools to traverse the enterprise graph,
    identify the blast radius of the threat, and construct a comprehensive investigation dossier.
    
    Rules:
    1. Always search for connected entities up to 3 hops away.
    2. Correlate IP addresses against external Threat Intelligence.
    3. If you detect lateral movement, immediately request Human-In-The-Loop approval.
    """

    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.allowed_tools = ["query_history", "cypher_query", "threat_intel_search", "request_human_approval"]

    def investigate(self, case_data: dict) -> dict:
        logger.info(f"Investigator starting case: {case_data.get('case_id')}")
        # Logic to interface with tools and build the final dossier
        return {"status": "AWAITING_HUMAN", "dossier": {}}

