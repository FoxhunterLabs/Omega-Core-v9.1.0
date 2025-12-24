"""
Omega Core – Visualization UI (Non-Canonical)

This UI is for inspection only.
All governance logic lives in omega_core/.
"""

import streamlit as st
import pandas as pd

from omega_core.core.clock import DeterministicClock
from omega_core.core.constants import HASH_DISPLAY_LENGTH
from omega_core.governance.state_machine import GovernanceStateMachine
from omega_core.governance.enums import GovernanceEventType, GovernanceState
from omega_core.governance.invariants import assert_governance_invariants
from omega_core.evidence.negative_authority import (
    generate_verifiable_negative_authority_proof,
)
from omega_core.evidence.models import VerifiableEvidence
from omega_core.evidence.verifier import ProofVerifier
from omega_core.threat.threat_model import ThreatModelMode
from omega_core.tests.test_negative_authority import (
    test_negative_authority_includes_numeric_absence,
)


def main():
    st.set_page_config(
        page_title="Omega Core v9.1.0 — Visualization",
        layout="wide",
    )

    st.title("Omega Core v9.1.0")
    st.caption(
        "Deterministic governance kernel — visualization layer only"
    )

    # Sidebar disclaimer
    with st.sidebar:
        st.warning("UI is non-canonical")
        st.text("All authority lives in omega_core/")
        st.markdown("---")

    # ---- demo kernel ----
    clock = DeterministicClock("ui_demo")
    sm = GovernanceStateMachine(clock)

    sm.transition(
        event_type=GovernanceEventType.OBSERVATION_RECORDED,
        tick=1,
        payload={"observation": "startup"},
        actor="ui_demo",
        target_state=GovernanceState.ASSESSED,
    )
    sm.transition(
        event_type=GovernanceEventType.ASSESSMENT_COMPLETED,
        tick=2,
        payload={"assessment": "nominal"},
        actor="ui_demo",
        target_state=GovernanceState.DECIDED,
    )
    sm.transition(
        event_type=GovernanceEventType.DECISION_MADE,
        tick=3,
        payload={"decision": "proceed"},
        actor="ui_demo",
        target_state=GovernanceState.COMMITTED,
    )

    # ---- governance state ----
    st.subheader("Governance State")

    states = [s.value for s in GovernanceState]
    cols = st.columns(len(states))
    for i, state in enumerate(states):
        with cols[i]:
            if state == sm.current_state.value:
                st.success(state)
            elif states.index(state) < states.index(sm.current_state.value):
                st.info(state)
            else:
                st.text(state)

    # ---- event log ----
    st.subheader("Event Log (Canonical Truth)")

    rows = []
    for e in sm.events:
        rows.append({
            "Event ID": e.event_id,
            "Type": e.event_type.value,
            "State": f"{e.state_before.value} → {e.state_after.value}",
            "Hash": e.event_hash[:HASH_DISPLAY_LENGTH] + "...",
        })

    st.dataframe(pd.DataFrame(rows), use_container_width=True)

    # ---- invariant check ----
    st.subheader("Invariant Check")

    if st.button("Validate Governance Invariants"):
        try:
            assert_governance_invariants(sm.events)
            st.success("All invariants satisfied")
        except Exception as e:
            st.error(str(e))

    # ---- evidence verification ----
    st.subheader("Verifiable Evidence")

    if st.button("Generate + Verify Evidence"):
        proof, capsule = generate_verifiable_negative_authority_proof(
            tick=1,
            authority_claims=[],
        )

        verifier = ProofVerifier(capsule)
        ev = VerifiableEvidence.from_dict(
            proof.asserted_absences[0]["evidence"]
        )

        result = verifier.verify_evidence(ev)

        if result.valid:
            st.success("Evidence verified from capsule")
        else:
            st.error(result.failure_reason)

    # ---- threat model ----
    st.subheader("Adversarial Mode")

    if st.checkbox("Enable Threat Simulation"):
        threat = ThreatModelMode(enabled=True)

        original = {"data": "clean", "timestamp": "t"}
        tampered = threat.simulate_log_tampering(original)

        detected, msg = threat.detect_and_refuse(
            original_data=original,
            processed_data=tampered,
        )

        if detected:
            st.error(msg)
        else:
            st.success("No tampering detected")

    # ---- property test demo ----
    st.subheader("Kernel Property Test (Demo)")

    if st.button("Run Numeric Authority Test"):
        try:
            test_negative_authority_includes_numeric_absence()
            st.success("Numeric authority prohibition verified")
        except AssertionError:
            st.error("Test failed")

    # ---- footer ----
    st.markdown("---")
    st.caption(
        "This UI is a visualization only. "
        "Omega Core is deterministic, replayable, and UI-agnostic."
    )


if __name__ == "__main__":
    main()
