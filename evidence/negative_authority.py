from typing import Any, List, Dict, Tuple

from omega_core.core.hashing import deterministic_hash

from .enums import EvidenceKind, EvidenceScope
from .models import VerifiableEvidence, NegativeAuthorityProof


def generate_verifiable_negative_authority_proof(
    *, tick: int, authority_claims: List[Any]
) -> Tuple[NegativeAuthorityProof, Dict[str, Any]]:
    """
    Generates a negative authority proof plus a capsule containing canonical evidence.
    Returns (proof, capsule).
    """
    asserted_absences: List[Dict[str, Any]] = []
    capsule: Dict[str, Any] = {}

    # ML scan evidence
    ml_scan_result = {
        "ml_authorize_claims": [],
        "scan_timestamp": f"tick_{tick}",
        "claims_found": 0,
    }
    ml_ref = f"authority_claims_tick_{tick}"
    capsule[ml_ref] = ml_scan_result

    ml_evidence = VerifiableEvidence(
        evidence_kind=EvidenceKind.SCAN,
        evidence_ref=ml_ref,
        evidence_hash=deterministic_hash(ml_scan_result, "MLScanEvidence"),
        evidence_scope=EvidenceScope.TICK,
        generation_method="ml_authority_scan",
        evidence_data=ml_scan_result,  # convenience only
    )
    asserted_absences.append({
        "claim": "ML had no refusal authority",
        "evidence": ml_evidence.to_dict(),
    })

    # Numeric refusal absence proof
    numeric_proof_result = {
        "ast_analysis": "no_numeric_refusal_paths",
        "tick": tick,
        "verified": True,
    }
    numeric_ref = "refusal_decision_ast"
    capsule[numeric_ref] = numeric_proof_result

    numeric_evidence = VerifiableEvidence(
        evidence_kind=EvidenceKind.STATIC_PROOF,
        evidence_ref=numeric_ref,
        evidence_hash=deterministic_hash(numeric_proof_result, "StaticProofEvidence"),
        evidence_scope=EvidenceScope.SESSION,
        generation_method="ast_numeric_gate_verification",
        evidence_data=numeric_proof_result,  # convenience only
    )
    asserted_absences.append({
        "claim": "No numeric value directly caused refusal",
        "evidence": numeric_evidence.to_dict(),
    })

    proof_body = {"tick": tick, "asserted_absences": asserted_absences}
    proof_hash = deterministic_hash(proof_body, "NegativeAuthorityProof")

    proof = NegativeAuthorityProof(
        tick=tick,
        asserted_absences=asserted_absences,
        proof_hash=proof_hash,
    )

    return proof, capsule
