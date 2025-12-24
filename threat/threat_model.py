from typing import Any, Dict, List, Tuple

from omega_core.core.hashing import deterministic_hash
from omega_core.governance.enums import GovernanceEventType
from omega_core.governance.state_machine import GovernanceStateMachine


class ThreatModelMode:
    """
    Adversarial testing mode.
    Threats block governance progression until acknowledged.
    """

    def __init__(self, enabled: bool = False):
        self.enabled = enabled
        self.threat_log: List[Dict[str, Any]] = []

    def simulate_log_tampering(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.enabled:
            return log_data

        tampered = dict(log_data)
        if "timestamp" in tampered:
            del tampered["timestamp"]
            self.threat_log.append({
                "threat": "field_deletion",
                "field": "timestamp",
            })

        return tampered

    def simulate_event_reordering(self, events: list) -> list:
        if not self.enabled or len(events) < 2:
            return events

        reordered = list(events)
        reordered[-1], reordered[-2] = reordered[-2], reordered[-1]

        self.threat_log.append({
            "threat": "event_reordering",
            "scope": "last_two_events",
        })

        return reordered

    def detect_and_refuse(
        self,
        *,
        original_data: Any,
        processed_data: Any,
    ) -> Tuple[bool, str]:
        if not self.enabled:
            return False, ""

        try:
            orig_hash = deterministic_hash(original_data, "ThreatDetection")
            proc_hash = deterministic_hash(processed_data, "ThreatDetection")
        except TypeError as e:
            return True, f"THREAT_DETECTED: non-canonicalizable data ({e})"

        if orig_hash != proc_hash:
            return (
                True,
                f"THREAT_DETECTED: hash mismatch "
                f"{orig_hash[:8]} vs {proc_hash[:8]}"
            )

        return False, ""

    def emit_threat_event(
        self,
        *,
        state_machine: GovernanceStateMachine,
        tick: int,
        threat_details: Dict[str, Any],
    ):
        payload = {
            "threat_type": threat_details.get("threat", "unknown"),
            "details": threat_details,
            "requires_ack": True,
        }

        workflow_id = f"threat_{tick}_{payload['threat_type']}"
        state_machine.blocked_workflows.append(workflow_id)

        return state_machine.transition(
            event_type=GovernanceEventType.THREAT_DETECTED,
            tick=tick,
            payload=payload,
            actor="threat_detector",
            target_state=state_machine.current_state,
        )

    def counterfactual_clearance(self) -> Dict[str, Any]:
        return {
            "clearance_conditions": {
                "disable_threat_mode": True,
                "verify_integrity": True,
                "replay_with_clean_inputs": True,
            },
            "threat_log": self.threat_log,
        }
