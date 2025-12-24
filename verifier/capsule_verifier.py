from typing import Dict, Any, Tuple, List

from omega_core.core.hashing import deterministic_hash
from omega_core.core.exceptions import VerificationIncompleteError
from omega_core.governance.events import GovernanceEvent


class OmegaVerifier:
    """
    Standalone verifier for Omega capsules.

    INVARIANT:
    Evidence verification must re-derive all hashes or fail.
    Partial verification is treated as INVALID.
    """

    def __init__(self, capsule: Dict[str, Any]):
        self.capsule = capsule
        self.verification_log: List[str] = []

    def verify_capsule(self) -> Tuple[bool, str]:
        try:
            self._verify_governance_spec()
            self._verify_authority_claim_ids()
            self._verify_negative_authority_proof()
            self._verify_event_chain()

            return True, "VALID"

        except VerificationIncompleteError as e:
            return False, f"INVALID: verification_incomplete: {e}"
        except Exception as e:
            return False, f"INVALID: verification_exception: {e}"

    # ---- individual verification steps ----

    def _verify_governance_spec(self) -> None:
        governance = self.capsule.get("governance", {})
        spec = governance.get("spec")
        expected_hash = governance.get("spec_hash")

        if not spec or not expected_hash:
            raise VerificationIncompleteError("Missing governance spec or hash")

        recomputed = deterministic_hash(spec, "GovernanceSpec")

        if recomputed != expected_hash:
            raise VerificationIncompleteError(
                "Governance spec hash mismatch"
            )

        self.verification_log.append("Governance spec hash verified")

    def _verify_authority_claim_ids(self) -> None:
        # Explicit refusal until implemented
        raise VerificationIncompleteError(
            "Authority claim ID verification not implemented"
        )

    def _verify_negative_authority_proof(self) -> None:
        raise VerificationIncompleteError(
            "Negative authority proof verification not implemented"
        )

    def _verify_event_chain(self) -> None:
        events = self.capsule.get("events")
        if not events:
            raise VerificationIncompleteError("No governance events present")

        # Explicit refusal until full replay logic exists
        raise VerificationIncompleteError(
            "Event chain replay verification not implemented"
        )
