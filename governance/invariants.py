from omega_core.core.exceptions import GovernanceInvariantViolation
from omega_core.core.hashing import deterministic_hash

from .events import GovernanceEvent


def assert_governance_invariants(events: list[GovernanceEvent]) -> None:
    prev_hash = "genesis"

    for event in events:
        if event.prev_event_hash != prev_hash:
            raise GovernanceInvariantViolation(
                f"Event chain broken at {event.event_id}"
            )

        body = {
            "event_id": event.event_id,
            "event_type": event.event_type.value,
            "tick": event.tick,
            "prev_event_hash": event.prev_event_hash,
            "payload_hash": event.payload_hash,
            "actor": event.actor,
            "timestamp": event.timestamp,
            "state_before": event.state_before.value,
            "state_after": event.state_after.value,
        }

        recomputed = deterministic_hash(body, "GovernanceEvent")
        if recomputed != event.event_hash:
            raise GovernanceInvariantViolation(
                f"Event hash mismatch at {event.event_id}"
            )

        prev_hash = event.event_hash

    for i in range(1, len(events)):
        if events[i].state_before != events[i - 1].state_after:
            raise GovernanceInvariantViolation(
                "State continuity violated"
            )
