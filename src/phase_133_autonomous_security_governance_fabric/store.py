"""
Thread-safe store for Autonomous Security Governance Fabric
"""

import threading
from typing import Dict, List, Optional, Any
from .models import GovernancePolicy, ComplianceControl, AuditRecord, GovernanceWorkflow

class AutonomousSecurityGovernanceFabricStore:
    def __init__(self):
        self.lock = threading.RLock()
        self._governancepolicys: Dict[str, GovernancePolicy] = {}
        self._compliancecontrols: Dict[str, ComplianceControl] = {}
        self._auditrecords: Dict[str, AuditRecord] = {}
        self._governanceworkflows: Dict[str, GovernanceWorkflow] = {}

    def add_governancepolicy(self, obj: GovernancePolicy) -> GovernancePolicy:
        with self.lock:
            self._governancepolicys[obj.policy_id] = obj
            return obj

    def get_governancepolicy(self, key: str) -> Optional[GovernancePolicy]:
        with self.lock:
            return self._governancepolicys.get(key)

    def list_governancepolicys(self) -> List[GovernancePolicy]:
        with self.lock:
            return list(self._governancepolicys.values())

    def add_compliancecontrol(self, obj: ComplianceControl) -> ComplianceControl:
        with self.lock:
            self._compliancecontrols[obj.control_id] = obj
            return obj

    def get_compliancecontrol(self, key: str) -> Optional[ComplianceControl]:
        with self.lock:
            return self._compliancecontrols.get(key)

    def list_compliancecontrols(self) -> List[ComplianceControl]:
        with self.lock:
            return list(self._compliancecontrols.values())

    def add_auditrecord(self, obj: AuditRecord) -> AuditRecord:
        with self.lock:
            self._auditrecords[obj.audit_id] = obj
            return obj

    def get_auditrecord(self, key: str) -> Optional[AuditRecord]:
        with self.lock:
            return self._auditrecords.get(key)

    def list_auditrecords(self) -> List[AuditRecord]:
        with self.lock:
            return list(self._auditrecords.values())

    def add_governanceworkflow(self, obj: GovernanceWorkflow) -> GovernanceWorkflow:
        with self.lock:
            self._governanceworkflows[obj.workflow_id] = obj
            return obj

    def get_governanceworkflow(self, key: str) -> Optional[GovernanceWorkflow]:
        with self.lock:
            return self._governanceworkflows.get(key)

    def list_governanceworkflows(self) -> List[GovernanceWorkflow]:
        with self.lock:
            return list(self._governanceworkflows.values())

_store_instance = None
def get_store() -> AutonomousSecurityGovernanceFabricStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = AutonomousSecurityGovernanceFabricStore()
    return _store_instance
