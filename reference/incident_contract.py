"""Synthetic contract-level model. Not a SCADA/OT integration or production service."""
from dataclasses import dataclass, field
from typing import Dict, List

class ContractViolation(ValueError):
    """Rejected request: invariant is not satisfied."""

@dataclass
class Incident:
    incident_id: str
    source_event_id: str
    topology_version: str
    status: str = "QUALIFIED"
    approved_by: str = ""
    work_order_id: str = ""
    audit: List[str] = field(default_factory=list)

class IncidentLedger:
    """In-memory reference for non-regression tests; no I/O, no commands to assets."""
    def __init__(self, authorized_roles=None):
        self.authorized_roles = frozenset(authorized_roles or {"OPERATOR_AUTHORIZED"})
        self.events: Dict[str, str] = {}
        self.incidents: Dict[str, Incident] = {}
        self.idempotency_keys: Dict[str, str] = {}

    def observe(self, source: str, event_id: str, topology_version: str, quality: str = "VALID") -> Incident:
        if not source.strip() or not event_id.strip() or not topology_version.strip():
            raise ContractViolation("source/event/topology-version required")
        if quality != "VALID":
            raise ContractViolation("source quality rejected, quarantine required")
        key = f"{source}:{event_id}"
        if key in self.events:
            return self.incidents[self.events[key]]
        iid = "INC-" + str(len(self.incidents) + 1).zfill(4)
        record = Incident(iid, event_id, topology_version, audit=["OBSERVATION_ACCEPTED", "INCIDENT_QUALIFIED"])
        self.events[key] = iid
        self.incidents[iid] = record
        return record

    def authorize_intervention(self, incident_id: str, role: str, assessed_topology_version: str) -> Incident:
        incident = self.incidents[incident_id]
        if role not in self.authorized_roles:
            raise ContractViolation("role is not authorized")
        if assessed_topology_version != incident.topology_version:
            raise ContractViolation("stale topology snapshot")
        if incident.status == "CLOSED":
            raise ContractViolation("closed incident")
        incident.approved_by = role
        incident.status = "APPROVED"
        incident.audit.append("HUMAN_APPROVAL")
        return incident

    def request_work_order(self, incident_id: str, idempotency_key: str) -> str:
        incident = self.incidents[incident_id]
        if not idempotency_key.strip():
            raise ContractViolation("idempotency key required")
        key = f"{incident_id}:{idempotency_key}"
        if key in self.idempotency_keys:
            return self.idempotency_keys[key]
        if incident.status != "APPROVED" or not incident.approved_by:
            raise ContractViolation("human authorization required")
        if incident.work_order_id:
            raise ContractViolation("a work order already exists for this incident")
        wid = "WO-" + incident_id
        incident.work_order_id = wid
        incident.status = "FIELDWORK"
        incident.audit.append("WORK_ORDER_CREATED")
        self.idempotency_keys[key] = wid
        return wid

    def close_after_restoration(self, incident_id: str, confirmed: bool) -> Incident:
        incident = self.incidents[incident_id]
        if incident.status != "FIELDWORK" or not confirmed:
            raise ContractViolation("authorized restoration evidence required")
        incident.status = "CLOSED"
        incident.audit.append("RESTORATION_CONFIRMED")
        incident.audit.append("INCIDENT_CLOSED")
        return incident
