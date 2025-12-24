"""
Core exception types.
Fail-fast. Fail-closed.
"""

class GovernanceInvariantViolation(Exception):
    """Governance invariant violated - system must halt"""
    pass


class DeterminismViolation(Exception):
    """Deterministic replay requirement violated"""
    pass


class NumericAuthorityViolation(Exception):
    """Numeric authority constraint violated"""
    pass


class EvidenceVerificationError(Exception):
    """Evidence verification failed"""
    pass


class VerificationIncompleteError(Exception):
    """Refuse to certify partial truth"""
    pass
