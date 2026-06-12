"""Multi-Cloud Security Fabric Models"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict
from uuid import uuid4

class CloudProvider(Enum):
    AWS = "AWS"
    AZURE = "AZURE"
    GCP = "GCP"
    HYBRID = "HYBRID"

@dataclass
class CloudConnector:
    connector_id: str
    provider: CloudProvider
    status: str = "CONNECTED"
    resources: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {"connector_id": self.connector_id, "provider": self.provider.value,
                "status": self.status, "resources": self.resources}

@dataclass
class SecurityDataFabric:
    fabric_id: str
    name: str
    cloud_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {"fabric_id": self.fabric_id, "name": self.name, "cloud_count": self.cloud_count}