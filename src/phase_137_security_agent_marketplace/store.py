"""
Thread-safe store for Security Agent Marketplace
"""

import threading
from typing import Dict, List, Optional, Any
from .models import AgentBlueprint, MarketplaceListing, DeploymentInstance, AgentSubscription

class SecurityAgentMarketplaceStore:
    def __init__(self):
        self.lock = threading.RLock()
        self._agentblueprints: Dict[str, AgentBlueprint] = {}
        self._marketplacelistings: Dict[str, MarketplaceListing] = {}
        self._deploymentinstances: Dict[str, DeploymentInstance] = {}
        self._agentsubscriptions: Dict[str, AgentSubscription] = {}

    def add_agentblueprint(self, obj: AgentBlueprint) -> AgentBlueprint:
        with self.lock:
            self._agentblueprints[obj.blueprint_id] = obj
            return obj

    def get_agentblueprint(self, key: str) -> Optional[AgentBlueprint]:
        with self.lock:
            return self._agentblueprints.get(key)

    def list_agentblueprints(self) -> List[AgentBlueprint]:
        with self.lock:
            return list(self._agentblueprints.values())

    def add_marketplacelisting(self, obj: MarketplaceListing) -> MarketplaceListing:
        with self.lock:
            self._marketplacelistings[obj.listing_id] = obj
            return obj

    def get_marketplacelisting(self, key: str) -> Optional[MarketplaceListing]:
        with self.lock:
            return self._marketplacelistings.get(key)

    def list_marketplacelistings(self) -> List[MarketplaceListing]:
        with self.lock:
            return list(self._marketplacelistings.values())

    def add_deploymentinstance(self, obj: DeploymentInstance) -> DeploymentInstance:
        with self.lock:
            self._deploymentinstances[obj.instance_id] = obj
            return obj

    def get_deploymentinstance(self, key: str) -> Optional[DeploymentInstance]:
        with self.lock:
            return self._deploymentinstances.get(key)

    def list_deploymentinstances(self) -> List[DeploymentInstance]:
        with self.lock:
            return list(self._deploymentinstances.values())

    def add_agentsubscription(self, obj: AgentSubscription) -> AgentSubscription:
        with self.lock:
            self._agentsubscriptions[obj.subscription_id] = obj
            return obj

    def get_agentsubscription(self, key: str) -> Optional[AgentSubscription]:
        with self.lock:
            return self._agentsubscriptions.get(key)

    def list_agentsubscriptions(self) -> List[AgentSubscription]:
        with self.lock:
            return list(self._agentsubscriptions.values())

_store_instance = None
def get_store() -> SecurityAgentMarketplaceStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = SecurityAgentMarketplaceStore()
    return _store_instance
