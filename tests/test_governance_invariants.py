from omega_core.core.clock import DeterministicClock
from omega_core.core.exceptions import GovernanceInvariantViolation
from omega_core.governance.enums import GovernanceEventType, GovernanceState
from omega_core.governance.state_machine import GovernanceStateMachine
from omega_core.governance.invariants import assert_governance_invariants


def test_event_chain_integrity():
    clock = DeterministicClock("test_session")
    sm = GovernanceStateMachine(clock)

    sm.transition(
        event_type=GovernanceEventType.OBSERVATION_RECORDED,
        tick=1,
        payload={},
        actor="test",
        target_state=GovernanceState.ASSESSED,
    )
    sm.transition(
        event_type=GovernanceEventType.ASSESSMENT_COMPLETED,
        tick=2,
        payload={},
        actor="test",
        target_state=GovernanceState.DECIDED,
    )

    # Should not raise
    assert_governance_invariants(sm.events)


def test_closure_blocked_by_workflow():
    clock = DeterministicClock("test_session")
    sm = GovernanceStateMachine(clock)

    sm.blocked_workflows.append("blocking_workflow")

    sm.transition(
        event_type=GovernanceEventType.OBSERVATION_RECORDED,
        tick=1,
        payload={},
        actor="test",
        target_state=GovernanceState.ASSESSED,
    )
    sm.transition(
        event_type=GovernanceEventType.ASSESSMENT_COMPLETED,
        tick=2,
        payload={},
        actor="test",
        target_state=GovernanceState.DECIDED,
    )
    sm.transition(
        event_type=GovernanceEventType.DECISION_MADE,
        tick=3,
        payload={"decision": "proceed"},
        actor="test",
        target_state=GovernanceState.COMMITTED,
    )

    try:
        sm.transition(
            event_type=GovernanceEventType.CYCLE_CLOSED,
            tick=4,
            payload={},
            actor="test",
            target_state=GovernanceState.CLOSED,
        )
        assert False, "Closure should have been blocked"
    except GovernanceInvariantViolation:
        assert True
