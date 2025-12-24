from omega_core.core.exceptions import NumericAuthorityViolation
from omega_core.reasoning.enums import SymbolicRefusalReason
from omega_core.reasoning.refusal_builder import RefusalDecisionBuilder


def test_numeric_values_blocked_in_refusal_causality():
    builder = RefusalDecisionBuilder()

    try:
        builder.add_symbolic_cause(
            node_id="bad_node",
            reason=SymbolicRefusalReason.INVARIANT_VIOLATED,
            evidence_refs=["ok_ref", 42],  # numeric = illegal
        )
        assert False, "Numeric authority should be rejected"
    except NumericAuthorityViolation:
        assert True
