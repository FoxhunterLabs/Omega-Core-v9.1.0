from typing import Dict, Any

from omega_core.core.hashing import deterministic_hash
from omega_core.core.exceptions import EvidenceVerificationError

from .enums import EvidenceKind
from .models import VerifiableEvidence, VerificationResult


class ProofVerifier:
    """
    TRUST BOUNDARY: verification loads canonical evidence from capsule only.
    evidence_data is ignored for verification.
    """

    def __init__(self, capsule: Dict[str, Any]):
        self.capsule = capsule

    def _load_canonical(self, evidence: VerifiableEvidence) -> Dict[str, Any]:
        if evidence.evidence_ref not in self.capsule:
            raise EvidenceVerificationError(
                f"Evidence ref not found in capsule: {evidence.evidence_ref}"
            )
        return self.capsule[evidence.evidence_ref]

    def verify_evidence(self, evidence: VerifiableEvidence) -> VerificationResult:
        try:
            if evidence.evidence_kind == EvidenceKind.SCAN:
                return self._verify_scan(evidence)
            if evidence.evidence_kind == EvidenceKind.MANIFEST:
                return self._verify_manifest(evidence)
            if evidence.evidence_kind == EvidenceKind.LOG:
                return self._verify_log(evidence)
            if evidence.evidence_kind == EvidenceKind.STATIC_PROOF:
                return self._verify_static_proof(evidence)

            return VerificationResult(
                valid=False,
                failure_reason="Unknown evidence kind",
                recomputed_hash=None,
                expected_hash=evidence.evidence_hash,
            )

        except EvidenceVerificationError as e:
            return VerificationResult(
                valid=False,
                failure_reason=str(e),
                recomputed_hash=None,
                expected_hash=evidence.evidence_hash,
            )
        except Exception as e:
            return VerificationResult(
                valid=False,
                failure_reason=f"Verification exception: {str(e)}",
                recomputed_hash=None,
                expected_hash=evidence.evidence_hash,
            )

    def _verify_scan(self, evidence: VerifiableEvidence) -> VerificationResult:
        if evidence.generation_method != "ml_authority_scan":
            return VerificationResult(
                valid=False,
                failure_reason="Unknown scan method",
                recomputed_hash=None,
                expected_hash=evidence.evidence_hash,
            )

        canonical = self._load_canonical(evidence)
        recomputed = deterministic_hash(canonical, "MLScanEvidence")

        return VerificationResult(
            valid=recomputed == evidence.evidence_hash,
            failure_reason=None if recomputed == evidence.evidence_hash else "Hash mismatch",
            recomputed_hash=recomputed,
            expected_hash=evidence.evidence_hash,
        )

    def _verify_manifest(self, evidence: VerifiableEvidence) -> VerificationResult:
        canonical = self._load_canonical(evidence)
        recomputed = deterministic_hash(canonical, "ManifestEvidence")

        return VerificationResult(
            valid=recomputed == evidence.evidence_hash,
            failure_reason=None if recomputed == evidence.evidence_hash else "Hash mismatch",
            recomputed_hash=recomputed,
            expected_hash=evidence.evidence_hash,
        )

    def _verify_log(self, evidence: VerifiableEvidence) -> VerificationResult:
        canonical = self._load_canonical(evidence)
        recomputed = deterministic_hash(canonical, "LogEvidence")

        return VerificationResult(
            valid=recomputed == evidence.evidence_hash,
            failure_reason=None if recomputed == evidence.evidence_hash else "Hash mismatch",
            recomputed_hash=recomputed,
            expected_hash=evidence.evidence_hash,
        )

    def _verify_static_proof(self, evidence: VerifiableEvidence) -> VerificationResult:
        canonical = self._load_canonical(evidence)
        recomputed = deterministic_hash(canonical, "StaticProofEvidence")

        return VerificationResult(
            valid=recomputed == evidence.evidence_hash,
            failure_reason=None if recomputed == evidence.evidence_hash else "Hash mismatch",
            recomputed_hash=recomputed,
            expected_hash=evidence.evidence_hash,
        )
