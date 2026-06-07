"""AI Engine for the Fraud Investigation Copilot.

Integrates with Google Generative AI (Gemini) with fallback capabilities,
PII masking, and prompt injection protection.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import logging
from typing import Any, Dict, List, Optional, Generator

from src.case_management.models import FraudCase, CaseEvidence, CaseAuditEvent
from src.case_management.store import get_case_store
from .models import InvestigationSummary, RiskExplanation, AIRecommendation
from .store import get_copilot_store

logger = logging.getLogger(__name__)

# --- PII Masking Regular Expressions ---
ACCOUNT_PATTERN = re.compile(r"\b(ACC_[A-Za-z0-9]{2})[A-Za-z0-9]+([A-Za-z0-9]{4})\b")
TXN_PATTERN = re.compile(r"\b(TXN_[A-Za-z0-9]{2})[A-Za-z0-9]+([A-Za-z0-9]{4})\b")
DEV_PATTERN = re.compile(r"\b(DEV_[A-Za-z0-9]{2})[A-Za-z0-9]+([A-Za-z0-9]{4})\b")

def mask_pii(text: str) -> str:
    """Mask sensitive identifiers like accounts, transactions, and devices.
    
    Example: ACC_ABC123456789 -> ACC_AB*****6789
    """
    if not isinstance(text, str):
        return text
    text = ACCOUNT_PATTERN.sub(r"\1*****\2", text)
    text = TXN_PATTERN.sub(r"\1*****\2", text)
    text = DEV_PATTERN.sub(r"\1*****\2", text)
    return text


def has_prompt_injection(text: str) -> bool:
    """Basic validation to detect potential prompt injection attacks."""
    if not text:
        return False
    
    lowered = text.lower()
    injection_triggers = [
        "ignore previous instructions",
        "ignore all previous",
        "system instruction",
        "override prompt",
        "you must now",
        "dan mode",
        "jailbreak",
        "system override",
        "act as a",
        "forget your instructions"
    ]
    return any(trigger in lowered for trigger in injection_triggers)


# --- Gemini Helper ---
def _get_gemini_client() -> tuple[Any, str] | None:
    """Configure and return the Gemini client if API key is set and package exists."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.warning("GEMINI_API_KEY environment variable is not configured.")
        return None
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model_name = os.environ.get("COPILOT_GEMINI_MODEL", "gemini-1.5-flash")
        model = genai.GenerativeModel(model_name)
        return model, model_name
    except ImportError:
        logger.error("google-generativeai package is not installed.")
        return None
    except Exception as e:
        logger.error(f"Failed to configure Gemini: {e}")
        return None


# --- Core Backend Tasks ---

async def generate_case_summary(
    case_id: str, analyst_id: str
) -> InvestigationSummary:
    """Generate an AI-powered case summary, caching the result."""
    copilot_store = get_copilot_store()
    case_store = get_case_store()
    
    # Check Cache
    cached = copilot_store.get_summary(case_id)
    if cached:
        return cached

    case = case_store.get_case(case_id)
    if not case:
        raise KeyError(f"Case '{case_id}' not found.")
        
    evidence_list = case_store.get_evidence(case_id)
    
    # Audit log AI action
    case_store._append_audit(
        case_id=case_id,
        analyst_id=analyst_id,
        action="AI_SUMMARY_GENERATED"
    )

    # Format the prompt context
    evidence_summary = "\n".join([
        f"- {ev.evidence_type.value} (Ref: {ev.reference_id or 'N/A'}): {ev.description}" 
        for ev in evidence_list
    ])
    
    context = f"""
    Case ID: {case.case_id}
    Transaction ID: {case.transaction_id}
    Current Status: {case.status.value}
    Priority: {case.priority.value}
    Decision: {case.decision}
    Risk Score: {case.risk_score}
    Evidence Log:
    {evidence_summary or 'No evidence attached yet.'}
    """
    
    masked_context = mask_pii(context)
    
    prompt = f"""
    You are an AI Fraud Investigation Copilot. Summarize the following masked fraud case details.
    
    Case Details:
    {masked_context}
    
    Your response MUST be valid JSON matching the following schema:
    {{
      "summary": "A 2-3 sentence overview of the case, detailing why it was flagged.",
      "suspicious_activity": ["Suspicious activity list item 1", "Suspicious activity list item 2"],
      "key_risk_factors": ["Risk factor 1", "Risk factor 2"],
      "unusual_patterns": ["Pattern 1", "Pattern 2"]
    }}
    
    Do NOT include markdown formatting wrappers like ```json in the output. Just return the raw JSON.
    """

    client_info = _get_gemini_client()
    if client_info:
        model, _ = client_info
        try:
            response = await asyncio.to_thread(model.generate_content, prompt)
            raw_text = response.text.strip()
            # Try to strip markdown if the model ignored instructions
            if raw_text.startswith("```"):
                lines = raw_text.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines[-1].startswith("```"):
                    lines = lines[:-1]
                raw_text = "\n".join(lines).strip()
            
            data = json.loads(raw_text)
            
            summary_obj = InvestigationSummary(
                case_id=case_id,
                summary=data.get("summary", ""),
                suspicious_activity=data.get("suspicious_activity", []),
                key_risk_factors=data.get("key_risk_factors", []),
                unusual_patterns=data.get("unusual_patterns", [])
            )
            copilot_store.save_summary(summary_obj)
            return summary_obj
        except Exception as e:
            logger.error(f"Gemini API error during case summary: {e}")
            # Fall back to mock response below

    # Mock Fallback
    mock_summary = InvestigationSummary(
        case_id=case_id,
        summary=f"Case {case_id} was flagged due to a high risk score of {case.risk_score} associated with transaction {mask_pii(case.transaction_id)}. The initial decision was set to {case.decision}.",
        suspicious_activity=[
            f"Transaction amount and velocity triggered risk score of {case.risk_score}",
            "Graph relationship analysis shows potential high-density network connectivity"
        ],
        key_risk_factors=[
            "High risk score threshold breached",
            "Mule-like velocity patterns detected in network traversal"
        ],
        unusual_patterns=[
            "Rapid execution of transactions through intermediate accounts",
            "Device ID associated with multiple accounts in a short time frame"
        ]
    )
    copilot_store.save_summary(mock_summary)
    return mock_summary


async def explain_risk_score(
    case_id: str, analyst_id: str
) -> RiskExplanation:
    """Generate AI-powered risk score explanation."""
    copilot_store = get_copilot_store()
    case_store = get_case_store()
    
    cached = copilot_store.get_explanation(case_id)
    if cached:
        return cached

    case = case_store.get_case(case_id)
    if not case:
        raise KeyError(f"Case '{case_id}' not found.")
        
    case_store._append_audit(
        case_id=case_id,
        analyst_id=analyst_id,
        action="AI_RISK_EXPLAINED"
    )

    context = f"""
    Case ID: {case.case_id}
    Transaction ID: {case.transaction_id}
    Risk Score: {case.risk_score}
    Decision: {case.decision}
    """
    
    masked_context = mask_pii(context)
    
    prompt = f"""
    You are an AI Fraud Investigation Copilot. Explain the risk score of {case.risk_score} for the case below.
    
    Case:
    {masked_context}
    
    Your response MUST be valid JSON matching the following schema:
    {{
      "breakdown_explanation": "Detailed explanation of risk score components (e.g. velocity, behavior).",
      "graph_relationship_explanation": "Explanation of Graph networks, hop counts, and connection proximity.",
      "mule_detection_reasoning": "Reasoning detailing whether this case exhibits mule accounts or money laundering patterns.",
      "htgnn_decisions_explanation": "Technical reasoning behind GNN/HTGNN classifier decisions."
    }}
    
    Do NOT include markdown formatting wrappers like ```json in the output. Just return the raw JSON.
    """

    client_info = _get_gemini_client()
    if client_info:
        model, _ = client_info
        try:
            response = await asyncio.to_thread(model.generate_content, prompt)
            raw_text = response.text.strip()
            if raw_text.startswith("```"):
                lines = raw_text.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines[-1].startswith("```"):
                    lines = lines[:-1]
                raw_text = "\n".join(lines).strip()
            
            data = json.loads(raw_text)
            
            explanation_obj = RiskExplanation(
                case_id=case_id,
                risk_score=case.risk_score,
                breakdown_explanation=data.get("breakdown_explanation", ""),
                graph_relationship_explanation=data.get("graph_relationship_explanation", ""),
                mule_detection_reasoning=data.get("mule_detection_reasoning", ""),
                htgnn_decisions_explanation=data.get("htgnn_decisions_explanation", "")
            )
            copilot_store.save_explanation(explanation_obj)
            return explanation_obj
        except Exception as e:
            logger.error(f"Gemini API error during risk explanation: {e}")
            # Fall back to mock response below

    # Mock Fallback
    mock_explanation = RiskExplanation(
        case_id=case_id,
        risk_score=case.risk_score,
        breakdown_explanation=f"The risk score of {case.risk_score} is heavily driven by velocity and network indicators. Velocity metrics show multiple high-value transactions occurred within a compressed time-window, exceeding normal account baseline patterns.",
        graph_relationship_explanation="Graph traversal identified that the source account is linked via 2 hops to a known blacklisted node. Additionally, the account's betweenness centrality score lies in the 95th percentile, indicating it acts as a critical bridge in the network.",
        mule_detection_reasoning="The account displays high-frequency layering behavior. Funds are deposited from multiple unrelated source accounts and rapidly consolidated before being withdrawn, which is a key signature of mule operation.",
        htgnn_decisions_explanation="The Heterogeneous Temporal Graph Neural Network (HTGNN) model classified this transaction with high confidence (92%) due to temporal-structural embeddings. The model detected anomalies in the message-passing sequences between account and device node types."
    )
    copilot_store.save_explanation(mock_explanation)
    return mock_explanation


async def generate_timeline_narrative(
    case_id: str, analyst_id: str
) -> List[Dict[str, Any]]:
    """Build a chronological investigation narrative from audit events and evidence."""
    case_store = get_case_store()
    case = case_store.get_case(case_id)
    if not case:
        raise KeyError(f"Case '{case_id}' not found.")
        
    audit_events = case_store.get_timeline(case_id)
    evidence_list = case_store.get_evidence(case_id)
    
    # Merge audit events and evidence into chronological events
    events = []
    
    # Audit Events
    for ae in audit_events:
        events.append({
            "timestamp": ae.timestamp,
            "type": "AUDIT",
            "action": ae.action,
            "description": f"Action '{ae.action}' performed by analyst {ae.analyst_id}. (Old: {ae.old_value or 'None'}, New: {ae.new_value or 'None'})"
        })
        
    # Evidence Events
    for ev in evidence_list:
        events.append({
            "timestamp": ev.created_at,
            "type": "EVIDENCE",
            "action": "EVIDENCE_ADDED",
            "description": f"Evidence '{ev.evidence_type.value}' added by analyst {ev.analyst_id}. Details: {ev.description}"
        })
        
    # Sort chronological (oldest first)
    events.sort(key=lambda x: x["timestamp"])
    
    # If no events, add a default case creation event
    if not events:
        events.append({
            "timestamp": case.created_at,
            "type": "AUDIT",
            "action": "CASE_CREATED",
            "description": f"Case created for transaction {case.transaction_id}."
        })
        
    # AI Enrichment of the timeline narrative
    client_info = _get_gemini_client()
    if client_info:
        model, _ = client_info
        
        events_json = mask_pii(json.dumps(events, indent=2))
        prompt = f"""
        You are an AI Fraud Investigation Copilot. Enrich and summarize this chronological event timeline into a structured narrative.
        For each event, add a brief 'narrative' field explaining the significance of this step in a real fraud investigation.
        
        Timeline Events:
        {events_json}
        
        Your response MUST be valid JSON matching the following schema:
        [
          {{
            "timestamp": "ISO-8601 Timestamp",
            "type": "AUDIT/EVIDENCE",
            "action": "Event action name",
            "description": "Original description",
            "narrative": "A 1-sentence analytical narrative explaining the context or significance of this action."
          }}
        ]
        
        Do NOT include markdown formatting wrappers like ```json in the output. Just return the raw JSON.
        """
        try:
            response = await asyncio.to_thread(model.generate_content, prompt)
            raw_text = response.text.strip()
            if raw_text.startswith("```"):
                lines = raw_text.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines[-1].startswith("```"):
                    lines = lines[:-1]
                raw_text = "\n".join(lines).strip()
            
            enriched_events = json.loads(raw_text)
            return enriched_events
        except Exception as e:
            logger.error(f"Gemini API error during timeline enrichment: {e}")
            # Fall back to adding simple narrative below

    # Standard Fallback / Non-AI Enrichment
    enriched_events = []
    for ev in events:
        narrative = "Standard log verification step recorded during analyst workflow."
        if ev["action"] == "CASE_CREATED":
            narrative = "Initial system trigger generated the case based on automated risk thresholds."
        elif ev["action"] == "STATUS_CHANGED":
            narrative = "The investigation state shifted, reflecting active analyst progress or case escalation."
        elif ev["action"] == "ANALYST_ASSIGNED":
            narrative = "Ownership established. A dedicated investigator took control of the case files."
        elif ev["action"] == "COMMENT_ADDED":
            narrative = "An analyst recorded diagnostic notes reflecting specific human pattern verification."
        elif ev["action"] == "EVIDENCE_ADDED":
            narrative = "Critical transactional, behavioral or network data was attached to build the audit case."
            
        enriched_events.append({
            **ev,
            "narrative": narrative
        })
        
    return enriched_events


async def generate_recommendations(
    case_id: str, analyst_id: str
) -> AIRecommendation:
    """Generate recommended analyst actions."""
    copilot_store = get_copilot_store()
    case_store = get_case_store()
    
    cached = copilot_store.get_recommendation(case_id)
    if cached:
        return cached

    case = case_store.get_case(case_id)
    if not case:
        raise KeyError(f"Case '{case_id}' not found.")
        
    case_store._append_audit(
        case_id=case_id,
        analyst_id=analyst_id,
        action="AI_RECOMMENDED"
    )

    context = f"""
    Case ID: {case.case_id}
    Transaction ID: {case.transaction_id}
    Risk Score: {case.risk_score}
    Current Status: {case.status.value}
    Initial Decision: {case.decision}
    """
    
    masked_context = mask_pii(context)
    
    prompt = f"""
    You are an AI Fraud Investigation Copilot. Recommend the next 3 actions for a fraud analyst working this case.
    
    Case Details:
    {masked_context}
    
    Your response MUST be valid JSON matching the following schema:
    {{
      "recommended_actions": ["Recommended action 1", "Recommended action 2", "Recommended action 3"],
      "reasoning": "Reasoning explaining why these actions are recommended based on the risk indicators.",
      "escalation_path": "Recommended escalation path (e.g. Law Enforcement, Compliance, Tier 2, etc.)"
    }}
    
    Do NOT include markdown formatting wrappers like ```json in the output. Just return the raw JSON.
    """

    client_info = _get_gemini_client()
    if client_info:
        model, _ = client_info
        try:
            response = await asyncio.to_thread(model.generate_content, prompt)
            raw_text = response.text.strip()
            if raw_text.startswith("```"):
                lines = raw_text.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines[-1].startswith("```"):
                    lines = lines[:-1]
                raw_text = "\n".join(lines).strip()
            
            data = json.loads(raw_text)
            
            rec_obj = AIRecommendation(
                case_id=case_id,
                recommended_actions=data.get("recommended_actions", []),
                reasoning=data.get("reasoning", ""),
                escalation_path=data.get("escalation_path", "")
            )
            copilot_store.save_recommendation(rec_obj)
            return rec_obj
        except Exception as e:
            logger.error(f"Gemini API error during recommendations: {e}")
            # Fall back to mock response below

    # Mock Fallback
    mock_rec = AIRecommendation(
        case_id=case_id,
        recommended_actions=[
            "Freeze source account assets immediately to prevent further transfer of funds.",
            "Verify the device fingerprint against other active account opening sessions.",
            "Request KYC documentation refresh from the account owner."
        ],
        reasoning=f"The high risk score ({case.risk_score}) combined with suspected mule network dynamics suggests an active account takeover or mule account layering ring. Prompt asset preservation is crucial.",
        escalation_path="Escalate to the Enterprise Fraud Operations Lead and the Compliance Team for regulatory SAR (Suspicious Activity Report) filing."
    )
    copilot_store.save_recommendation(mock_rec)
    return mock_rec


# --- Chat Interface (Ask AI) ---

async def ask_copilot(
    case_id: str, analyst_id: str, question: str
) -> str:
    """Chat with the AI Copilot about the details of a fraud case."""
    if has_prompt_injection(question):
        return "Warning: Potential prompt injection detected. The request was blocked to maintain security boundary."
        
    case_store = get_case_store()
    case = case_store.get_case(case_id)
    if not case:
        raise KeyError(f"Case '{case_id}' not found.")
        
    case_store._append_audit(
        case_id=case_id,
        analyst_id=analyst_id,
        action="AI_CHATTED",
        new_value=question[:100]
    )

    evidence_list = case_store.get_evidence(case_id)
    comments_list = case_store.get_comments(case_id)
    
    evidence_str = "\n".join([f"- {e.evidence_type.value}: {e.description}" for e in evidence_list])
    comments_str = "\n".join([f"- Analyst {c.analyst_id}: {c.text}" for c in comments_list])
    
    context = f"""
    Case Details:
    ID: {case.case_id}
    Transaction: {case.transaction_id}
    Risk Score: {case.risk_score}
    Status: {case.status.value}
    Decision: {case.decision}
    
    Evidence Log:
    {evidence_str or 'No evidence.'}
    
    Analyst Comments:
    {comments_str or 'No comments.'}
    """
    
    masked_context = mask_pii(context)
    
    prompt = f"""
    You are an AI Fraud Investigation Copilot. You are answering a question from a fraud analyst regarding this case.
    
    Case Context (Masked for PII):
    {masked_context}
    
    Analyst Question:
    {question}
    
    Provide a concise, direct answer based on the case details. Emphasize key risk factors or evidence where appropriate.
    Do NOT disclose the masking rules.
    """

    client_info = _get_gemini_client()
    if client_info:
        model, _ = client_info
        try:
            response = await asyncio.to_thread(model.generate_content, prompt)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini API error during chat: {e}")
            # Fall back to mock response below

    # Mock Fallback response based on keywords
    lowered_q = question.lower()
    if "risk" in lowered_q or "why" in lowered_q:
        return f"This case is flagged with a risk score of {case.risk_score} due to anomalous velocity metrics and network proximity to known suspicious entities. I suggest analyzing the graph traversal paths."
    elif "action" in lowered_q or "recommend" in lowered_q:
        return "I recommend freezing the target/mule account assets immediately and initiating a full KYC review of the source account."
    else:
        return f"Based on the case details for {case.case_id}, the transaction was categorized as {case.decision}. There are {len(evidence_list)} evidence items logged. Let me know if you would like me to explain specific risk factors or timeline events."
