from enum import Enum


class EvidenceKind(Enum):
    SCAN = "SCAN"
    MANIFEST = "MANIFEST"
    LOG = "LOG"
    STATIC_PROOF = "STATIC_PROOF"


class EvidenceScope(Enum):
    TICK = "TICK"
    SESSION = "SESSION"
    ASSET = "ASSET"
    FLEET = "FLEET"
