from omega_core.core.clock import DeterministicClock
from omega_core.governance.enums import GovernanceEventType, GovernanceState
from omega_core.governance.events import create_governance_event


def test_event_hash_determinism():
    clock = DeterministicClock("determinism_test")

    event1 = create_governance_event(
        event_type=GovernanceEventType.OBSERVATION_RECORDED,
        tick=1,
        prev_event_hash="genesis",
        payload={"a": 1},
        actor="tester",
        state_before=GovernanceState.OBSERVED,
        state_after=GovernanceState.ASSESSED,
        clock=clock,
    )

    event2 = create_governance_event(
        event_type=GovernanceEventType.OBSERVATION_RECORDED,
        tick=1,
        prev_event_hash="genesis",
        payload={"a": 1},
        actor="tester",
        state_before=GovernanceState.OBSERVED,
        state_after=GovernanceState.ASSESSED,
        clock=clock,
    )

    assert event1.event_hash == event2.event_hash
    assert event1.event_id == event2.event_id
