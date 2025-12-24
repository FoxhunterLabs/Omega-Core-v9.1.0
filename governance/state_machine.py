from typing import List, Dict, Any

from omega_core.core.exceptions import GovernanceInvariantViolation
from .enums import GovernanceState, GovernanceEventType
from .events import GovernanceEvent, create_governance_event


class GovernanceStateMachine:
    """
    Canonical governance state machine.
    All truth derives from events.
    """

    def __init__(self, clock):
        self.clock = clock
        self.current_state = GovernanceState.OBSERVED
        self.events: List[GovernanceEvent] = []
        self.last_event_hash = "genesis"
        self.blocked_workflows: List[str] = []

    def transition(
        self,
        *,
        event_type: GovernanceEventType,
        tick: int,
        payload: Dict[str, Any],
        actor: str,
        target_state: GovernanceState,
    ) -> GovernanceEvent:

        if target_state == GovernanceState.CLOSED and self.blocked_workflows:
            raise GovernanceInvariantViolation(
                f"CLOSED blocked by workflows: {self.blocked_workflows}"
            )

        if (
            event_type == GovernanceEventType.DECISION_MADE
            and payload.get("decision") == "refuse"
            and self.current_state != GovernanceState.ASSESSED
        ):
            raise GovernanceInvariantViolation(
                "Refusal requires ASSESSED state"
            )

        if not self._valid_transition(self.current_state, target_state):
            raise GovernanceInvariantViolation(
                f"Invalid transition {self.current_state} → {target_state}"
            )

        event = create_governance_event(
            event_type=event_type,
            tick=tick,
            prev_event_hash=self.last_event_hash,
            payload=payload,
            actor=actor,
            state_before=self.current_state,
            state_after=target_state,
            clock=self.clock,
        )

        self.events.append(event)
        self.last_event_hash = event.event_hash
        self.current_state = target_state

        return event

    @staticmethod
    def _valid_transition(
        from_state: GovernanceState,
        to_state: GovernanceState,
    ) -> bool:
        allowed = {
            GovernanceState.OBSERVED: {GovernanceState.ASSESSED},
            GovernanceState.ASSESSED: {GovernanceState.DECIDED},
            GovernanceState.DECIDED: {GovernanceState.COMMITTED},
            GovernanceState.COMMITTED: {
                GovernanceState.ACKED,
                GovernanceState.CLOSED,
            },
            GovernanceState.ACKED: {GovernanceState.CLOSED},
        }
        return to_state in allowed.get(from_state, set())
