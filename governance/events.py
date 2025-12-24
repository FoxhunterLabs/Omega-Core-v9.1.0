from dataclasses import dataclass
from typing import Dict, Any

from omega_core.core.hashing import deterministic_hash
from omega_core.core.constants import HASH_REFERENCE_LENGTH
from .enums import GovernanceEventType, GovernanceState


@dataclass(frozen=True)
class GovernanceEvent:
    event_id: str
    event_type: GovernanceEventType
    tick: int
    prev_event_hash: str
    payload_hash: str
    actor: str
    timestamp: str
    state_before: GovernanceState
    state_after: GovernanceState
    event_hash: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "tick": self.tick,
            "prev_event_hash": self.prev_event_hash,
            "payload_hash": self.payload_hash,
            "actor": self.actor,
            "timestamp": self.timestamp,
            "state_before": self.state_before.value,
            "state_after": self.state_after.value,
            "event_hash": self.event_hash,
        }


def create_governance_event(
    *,
    event_type: GovernanceEventType,
    tick: int,
    prev_event_hash: str,
    payload: Dict[str, Any],
    actor: str,
    state_before: GovernanceState,
    state_after: GovernanceState,
    clock,
) -> GovernanceEvent:
    payload_hash = deterministic_hash(payload, "EventPayload")
    payload_id = payload_hash[:HASH_REFERENCE_LENGTH]

    event_id = f"gov_{tick}_{event_type.value}_{payload_id}"
    timestamp = clock.ts(tick=tick, local_seq=0)

    body = {
        "event_id": event_id,
        "event_type": event_type.value,
        "tick": tick,
        "prev_event_hash": prev_event_hash,
        "payload_hash": payload_hash,
        "actor": actor,
        "timestamp": timestamp,
        "state_before": state_before.value,
        "state_after": state_after.value,
    }

    event_hash = deterministic_hash(body, "GovernanceEvent")

    return GovernanceEvent(
        event_id=event_id,
        event_type=event_type,
        tick=tick,
        prev_event_hash=prev_event_hash,
        payload_hash=payload_hash,
        actor=actor,
        timestamp=timestamp,
        state_before=state_before,
        state_after=state_after,
        event_hash=event_hash,
    )
