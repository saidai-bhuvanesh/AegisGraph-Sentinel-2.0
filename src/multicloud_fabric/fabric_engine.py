"""Multi-Cloud Security Fabric Engine"""
from datetime import datetime, timezone
from typing import Any, Dict
from uuid import uuid4

from .models import CloudConnector, CloudProvider, SecurityDataFabric

class MultiCloudFabric:
    def __init__(self):
        self.connectors: Dict[str, CloudConnector] = {}
        self.fabrics: Dict[str, SecurityDataFabric] = {}
    
    def add_connector(self, provider: CloudProvider) -> str:
        connector_id = str(uuid4())
        connector = CloudConnector(connector_id=connector_id, provider=provider)
        self.connectors[connector_id] = connector
        return connector_id
    
    def get_connector(self, connector_id: str) -> CloudConnector:
        return self.connectors.get(connector_id)
    
    def create_fabric(self, name: str) -> str:
        fabric_id = str(uuid4())
        fabric = SecurityDataFabric(fabric_id=fabric_id, name=name, cloud_count=len(self.connectors))
        self.fabrics[fabric_id] = fabric
        return fabric_id
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_connectors": len(self.connectors),
            "total_fabrics": len(self.fabrics),
            "providers": {p.value: len([c for c in self.connectors.values() if c.provider == p]) for p in CloudProvider}
        }

def get_multicloud_fabric() -> MultiCloudFabric:
    global _multicloud_fabric
    if _multicloud_fabric is None:
        _multicloud_fabric = MultiCloudFabric()
    return _multicloud_fabric

_multicloud_fabric = None