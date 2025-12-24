"""
Deterministic canonicalization for hashing.
Unknown types fail closed.
"""

import dataclasses
from datetime import datetime
from enum import Enum
from typing import Any

from .constants import CANON_FLOAT_DIGITS


def canonicalize_for_hash(obj: Any) -> Any:
    if isinstance(obj, float):
        return round(obj, CANON_FLOAT_DIGITS)

    if isinstance(obj, dict):
        return {k: canonicalize_for_hash(v) for k in sorted(obj.keys())}

    if isinstance(obj, (list, tuple)):
        return [canonicalize_for_hash(v) for v in obj]

    if isinstance(obj, set):
        return sorted(canonicalize_for_hash(v) for v in obj)

    if isinstance(obj, Enum):
        return obj.value

    if dataclasses.is_dataclass(obj):
        return canonicalize_for_hash(dataclasses.asdict(obj))

    if hasattr(obj, "to_dict"):
        return canonicalize_for_hash(obj.to_dict())

    if isinstance(obj, bytes):
        return obj.hex()

    if isinstance(obj, datetime):
        return obj.isoformat()

    if obj is None or isinstance(obj, (str, int, bool)):
        return obj

    raise TypeError(
        f"Cannot canonicalize type {type(obj)} — explicit to_dict() required"
    )
