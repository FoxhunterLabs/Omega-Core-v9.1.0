from dataclasses import dataclass
from typing import Dict, Any, List, Tuple

from .enums import SymbolicRefusalReason


@dataclass(frozen=True)
class CausalNode:
    node_id: str
    symbolic_reason: SymbolicRefusalReason
    evidence_refs: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "symbolic_reason": self.symbolic_reason.value,
            "evidence_refs": list(self.evidence_refs),
        }


@dataclass
class CausalDAG:
    nodes: List[CausalNode]
    edges: List[Tuple[str, str]]
    dag_hash: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": list(self.edges),
            "dag_hash": self.dag_hash,
        }
