from dataclasses import dataclass
from typing import Dict, Any, Optional, List


from .enums import EvidenceKind, EvidenceScope


@dataclass(frozen=True)
class VerifiableEvidence:
    """
    evidence_ref points to canonical capsule artifact.
    evidence_data is optional convenience copy and NOT authoritative.
    """
    evidence_kind: EvidenceKind
    evidence_ref: str
    evidence_hash: str
    evidence_scope: EvidenceScope
    generation_method: str
    evidence_data: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "evidence_kind": self.evidence_kind.value,
            "evidence_ref": self.evidence_ref,
            "evidence_hash": self.evidence_hash,
            "evidence_scope": self.evidence_scope.value,
            "generation_method": self.generation_method,
            "evidence_data": self.evidence_data,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "VerifiableEvidence":
        return VerifiableEvidence(
            evidence_kind=EvidenceKind(d["evidence_kind"]),
            evidence_ref=d["evidence_ref"],
            evidence_hash=d["evidence_hash"],
            evidence_scope=EvidenceScope(d["evidence_scope"]),
            generation_method=d["generation_method"],
            evidence_data=d.get("evidence_data"),
        )


@dataclass(frozen=True)
class NegativeAuthorityProof:
    tick: int
    asserted_absences: List[Dict[str, Any]]
    proof_hash: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tick": self.tick,
            "asserted_absences": list(self.asserted_absences),
            "proof_hash": self.proof_hash,
        }


@dataclass
class VerificationResult:
    valid: bool
    failure_reason: Optional[str]
    recomputed_hash: Optional[str]
    expected_hash: str
