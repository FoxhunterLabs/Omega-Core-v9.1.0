from dataclasses import dataclass
from typing import Dict, Any, Optional, Literal

from omega_core.core.hashing import deterministic_hash


@dataclass
class FleetAccountabilityWorkflow:
    """
    Workflow contract enforcing acknowledgment obligations.
    Blocks governance closure while unresolved.
    """
    tick: int
    event_hash: str
    ack_deadline_policy: str
    ack_deadline_value: int
    escalation_rule: str
    status: Literal["PENDING", "ACKNOWLEDGED", "EXPIRED", "ESCALATED"]
    acknowledger: str
    ack_timestamp: Optional[str]
    workflow_hash: str
    blocks_closure: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tick": self.tick,
            "event_hash": self.event_hash,
            "ack_deadline_policy": self.ack_deadline_policy,
            "ack_deadline_value": self.ack_deadline_value,
            "escalation_rule": self.escalation_rule,
            "status": self.status,
            "acknowledger": self.acknowledger,
            "ack_timestamp": self.ack_timestamp,
            "workflow_hash": self.workflow_hash,
            "blocks_closure": self.blocks_closure,
        }


def create_fleet_accountability_workflow(
    *,
    tick: int,
    event_hash: str,
    ack_deadline_ticks: int = 100,
    escalation_rule: str = "auto_STOP",
) -> FleetAccountabilityWorkflow:
    """
    Create a deterministic accountability workflow contract.
    """
    body = {
        "tick": tick,
        "event_hash": event_hash,
        "ack_deadline_policy": "N_ticks",
        "ack_deadline_value": ack_deadline_ticks,
        "escalation_rule": escalation_rule,
        "status": "PENDING",
        "blocks_closure": True,
    }

    workflow_hash = deterministic_hash(body, "FleetAccountabilityWorkflow")

    return FleetAccountabilityWorkflow(
        tick=tick,
        event_hash=event_hash,
        ack_deadline_policy="N_ticks",
        ack_deadline_value=ack_deadline_ticks,
        escalation_rule=escalation_rule,
        status="PENDING",
        acknowledger="PENDING",
        ack_timestamp=None,
        workflow_hash=workflow_hash,
        blocks_closure=True,
    )
