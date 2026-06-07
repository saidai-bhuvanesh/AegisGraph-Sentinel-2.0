"""Attack Reconstruction Engine to trace fraud paths and build attack chains."""

from __future__ import annotations

import logging
from typing import List, Optional

from src.case_management import get_case_store
from src.threat_intelligence import get_threat_store
from src.threat_intelligence.engine import extract_features_from_case
from .models import AttackChain
from .store import get_forensics_store

logger = logging.getLogger("forensics.reconstruction")


class AttackReconstructionEngine:
    """Discovers and reconstructs chronological multi-hop attack paths and fraud loops."""

    def __init__(self) -> None:
        self.forensics_store = get_forensics_store()
        self.threat_store = get_threat_store()
        self.case_store = get_case_store()

    def reconstruct_campaign(self, campaign_id: str) -> Optional[AttackChain]:
        """Trace transaction flows and indicators within a campaign to construct a chronological attack chain."""
        # 1. Check cache first
        cached_chain = self.forensics_store.get_chain_by_campaign(campaign_id)
        if cached_chain:
            return cached_chain

        campaign = self.threat_store.get_campaign(campaign_id)
        if not campaign:
            logger.warning(f"Campaign ID '{campaign_id}' not found.")
            return None

        # 2. Gather all cases associated with the campaign
        campaign_cases = []
        for case_id in campaign.case_ids:
            case = self.case_store.get_case(case_id)
            if case:
                campaign_cases.append(case)

        # Sort chronologically
        campaign_cases.sort(key=lambda c: c.created_at)

        # 3. Construct attack hops
        steps = []
        confidence_accum = 0.0
        
        for index, case in enumerate(campaign_cases):
            ip, device, account = extract_features_from_case(case)
            
            # Simple hop transition analysis
            transition_type = "INITIAL_COMPROMISE" if index == 0 else "LATERAL_PROPAGATION"
            if index == len(campaign_cases) - 1:
                transition_type = "FRAUD_CASHOUT"

            step = {
                "step_index": index,
                "case_id": case.case_id,
                "transaction_id": case.transaction_id,
                "risk_score": case.risk_score,
                "timestamp": case.created_at,
                "action": transition_type,
                "indicators": {
                    "ip": ip,
                    "device": device,
                    "account": account
                }
            }
            steps.append(step)
            confidence_accum += case.risk_score

        # Calculate a dynamic confidence score (average risk of cases + weight of indicator overlap)
        if steps:
            base_confidence = confidence_accum / len(steps)
            # Add premium if multiple common indicators are used
            confidence_score = min(0.95, base_confidence)
        else:
            confidence_score = 0.5

        chain = AttackChain(
            campaign_id=campaign_id,
            steps=steps,
            confidence_score=round(confidence_score, 3)
        )

        self.forensics_store.add_chain(chain)
        logger.info(f"Attack chain '{chain.id}' reconstructed successfully for campaign '{campaign_id}' with confidence {confidence_score}.")
        return chain

