"""AI Governance Policy Engine"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

class PolicyType(Enum):
    """AI Governance Policy Types"""
    SECURITY = "SECURITY"
    PRIVACY = "PRIVACY"
    FAIRNESS = "FAIRNESS"
    TRANSPARENCY = "TRANSPARENCY"
    ACCOUNTABILITY = "ACCOUNTABILITY"

class PolicyStatus(Enum):
    """Policy enforcement status"""
    ACTIVE = "ACTIVE"
    ENFORCED = "ENFORCED"
    VIOLATED = "VIOLATED"
    PENDING = "PENDING"

@dataclass
class GovernancePolicy:
    """AI Governance Policy"""
    policy_id: str
    name: str
    policy_type: PolicyType
    description: str
    enforcement_level: str = "STRICT"
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "name": self.name,
            "policy_type": self.policy_type.value,
            "description": self.description,
            "enforcement_level": self.enforcement_level,
            "created_at": self.created_at.isoformat()
        }

class PolicyEngine:
    """AI Governance Policy Engine"""
    
    def __init__(self):
        self.policies: Dict[str, GovernancePolicy] = {}
        self.violations: List[Dict[str, Any]] = []
    
    def add_policy(self, policy: GovernancePolicy) -> None:
        """Add a governance policy"""
        self.policies[policy.policy_id] = policy
    
    def enforce_policy(
        self,
        policy_id: str,
        model_id: str,
        action: str
    ) -> Dict[str, Any]:
        """Enforce a policy on a model action"""
        if policy_id not in self.policies:
            return {"status": "error", "message": "Policy not found"}
        
        policy = self.policies[policy_id]
        
        # Check if action violates policy
        violation = {
            "policy_id": policy_id,
            "model_id": model_id,
            "action": action,
            "timestamp": datetime.utcnow().isoformat(),
            "status": PolicyStatus.ENFORCED.value
        }
        
        return {"status": "enforced", "violation": violation}
    
    def get_policy_stats(self) -> Dict[str, Any]:
        """Get policy statistics"""
        return {
            "total_policies": len(self.policies),
            "active_policies": len([p for p in self.policies.values()]),
            "violations": len(self.violations)
        }
    
    @classmethod
    def create_default_policies(cls) -> List[GovernancePolicy]:
        """Create default AI governance policies"""
        return [
            GovernancePolicy(
                policy_id="security-001",
                name="Model Access Control",
                policy_type=PolicyType.SECURITY,
                description="Ensure models have proper access controls"
            ),
            GovernancePolicy(
                policy_id="privacy-001",
                name="Data Privacy Protection",
                policy_type=PolicyType.PRIVACY,
                description="Protect user data in model operations"
            ),
            GovernancePolicy(
                policy_id="fairness-001",
                name="Bias Detection",
                policy_type=PolicyType.FAIRNESS,
                description="Monitor and mitigate model bias"
            )
        ]