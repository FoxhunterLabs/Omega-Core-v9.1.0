from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from omega_core.core.hashing import deterministic_hash
from omega_core.core.constants import HASH_REFERENCE_LENGTH
from omega_core.governance.events import GovernanceEvent
from omega_core.evidence.models import NegativeAuthorityProof


@dataclass
class MinimalProofBundle:
    """
    Minimal proof bundle for audit requirements.
    Intended to be portable and independently verifiable.
    """
    governance_spec: Dict[str, Any]
    governance_spec_hash: str

    admissibility_report: Dict[str, Any]
    admissibility_hash: str

    authority_claims: List[Dict[str, Any]]
    authority_claim_ids: List[str]

    negative_authority_proof: Dict[str, Any]

    event_chain_slice: List[Dict[str, Any]]
    invariant_proof_subset: Optional[List[Dict[str, Any]]]

    bundle_hash: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "governance_spec": self.governance_spec,
            "governance_spec_hash": self.governance_spec_hash,
            "admissibility_report": self.admissibility_report,
            "admissibility_hash": self.admissibility_hash,
            "authority_claims": self.authority_claims,
            "authority_claim_ids": self.authority_claim_ids,
            "negative_authority_proof": self.negative_authority_proof,
            "event_chain_slice": self.event_chain_slice,
            "invariant_proof_subset": self.invariant_proof_subset,
            "bundle_hash": self.bundle_hash,
        }


def export_minimal_proof_bundle(
    *,
    governance_spec: Dict[str, Any],
    governance_events: List[GovernanceEvent],
    authority_claims: List[Any],
    negative_authority_proof: NegativeAuthorityProof,
    invariant_proofs: Optional[List[Dict[str, Any]]] = None,
    event_slice_size: int = 5,
) -> MinimalProofBundle:
    """
    Export a deterministic minimal proof bundle.

    Notes:
    - Admissibility report here is a derived view (non-canonical).
    - Events are canonical truth; this bundle is an export artifact.
    """

    # Governance spec hash (deterministic)
    governance_spec_hash = deterministic_hash(governance_spec, "GovernanceSpec")

    # Minimal derived admissibility view (deliberately simple + deterministic)
    admissibility_report = {
        "derived_from_events": True,
        "event_count": len(governance_events),
    }
    admissibility_hash = deterministic_hash(admissibility_report, "AdmissibilityReport")

    # Export last N events as slice for minimal audit trail
    chain_slice = [e.to_dict() for e in governance_events[-event_slice_size:]]

    # Normalize authority claims
    claims_data: List[Dict[str, Any]] = []
    claim_ids: List[str] = []

    for claim in authority_claims:
        claim_dict = claim.to_dict() if hasattr(claim, "to_dict") else claim
        claims_data.append(claim_dict)

        if hasattr(claim, "claim_id"):
            claim_ids.append(str(claim.claim_id))
        else:
            cid = deterministic_hash(claim_dict, "AuthorityClaim")[:HASH_REFERENCE_LENGTH]
            claim_ids.append(f"claim_{cid}")

    # Bundle hash ties together the minimal invariant backbone
    bundle_body = {
        "governance_spec_hash": governance_spec_hash,
        "admissibility_hash": admissibility_hash,
        "authority_claim_ids": claim_ids,
        "negative_authority_proof_hash": negative_authority_proof.proof_hash,
        "event_chain_count": len(chain_slice),
    }
    bundle_hash = deterministic_hash(bundle_body, "MinimalProofBundle")

    return MinimalProofBundle(
        governance_spec=governance_spec,
        governance_spec_hash=governance_spec_hash,
        admissibility_report=admissibility_report,
        admissibility_hash=admissibility_hash,
        authority_claims=claims_data,
        authority_claim_ids=claim_ids,
        negative_authority_proof=negative_authority_proof.to_dict(),
        event_chain_slice=chain_slice,
        invariant_proof_subset=invariant_proofs,
        bundle_hash=bundle_hash,
    )
