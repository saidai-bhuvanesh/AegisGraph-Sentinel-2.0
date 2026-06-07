"""AI Fraud Investigation Copilot Package."""

from .models import (
    InvestigationSummary,
    RiskExplanation,
    AIRecommendation,
    AnalystFeedback,
)
from .store import get_copilot_store, CopilotStore
from .engine import (
    generate_case_summary,
    explain_risk_score,
    generate_timeline_narrative,
    generate_recommendations,
    ask_copilot,
    mask_pii,
    has_prompt_injection,
)
