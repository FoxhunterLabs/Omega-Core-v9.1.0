"""
Deterministic hashing with domain separation.
"""

import json
import hashlib
from typing import Any, Optional

from .canonical import canonicalize_for_hash


def deterministic_json_bytes(obj: Any) -> bytes:
    canonical = canonicalize_for_hash(obj)
    return json.dumps(
        canonical,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")


def deterministic_hash(obj: Any, domain_separator: Optional[str] = None) -> str:
    if domain_separator:
        obj = {
            "__type__": domain_separator,
            "__data__": obj,
        }

    return hashlib.sha256(
        deterministic_json_bytes(obj)
    ).hexdigest()
