from omega_core.evidence.negative_authority import (
    generate_verifiable_negative_authority_proof
)


def test_negative_authority_includes_numeric_absence():
    proof, capsule = generate_verifiable_negative_authority_proof(
        tick=1,
        authority_claims=[],
    )

    claims = [a["claim"] for a in proof.asserted_absences]

    assert "No numeric value directly caused refusal" in claims
