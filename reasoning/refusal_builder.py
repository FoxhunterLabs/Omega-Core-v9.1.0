from typing import List, Tuple

from omega_core.core.hashing import deterministic_hash
from omega_core.core.exceptions import NumericAuthorityViolation

from .enums import SymbolicRefusalReason
from .models import CausalNode, CausalDAG


class RefusalDecisionBuilder:
    """
    Build a symbolic causal DAG for refusal decisions.
    INVARIANT: Numeric values cannot influence refusal causality.
    """

    def __init__(self):
        self._nodes: List[CausalNode] = []
        self._edges: List[Tuple[str, str]] = []

    def add_symbolic_cause(
        self,
        *,
        node_id: str,
        reason: SymbolicRefusalReason,
        evidence_refs: List[str],
    ) -> None:
        # Type-level-ish enforcement at runtime: no numeric evidence refs
        if any(isinstance(ref, (int, float)) for ref in evidence_refs):
            raise NumericAuthorityViolation(
                "Numeric values prohibited in refusal causality; use symbolic refs only"
            )

        self._nodes.append(
            CausalNode(
                node_id=node_id,
                symbolic_reason=reason,
                evidence_refs=list(evidence_refs),
            )
        )

    def add_causal_edge(self, *, from_node: str, to_node: str) -> None:
        self._edges.append((from_node, to_node))

    def build_causal_dag(self) -> CausalDAG:
        # HARD FAIL if any numeric leaks through
        for node in self._nodes:
            for ref in node.evidence_refs:
                if isinstance(ref, (int, float)):
                    raise NumericAuthorityViolation(
                        "HARD FAIL: Numeric value detected in causal DAG"
                    )

        body = {
            "nodes": [n.to_dict() for n in self._nodes],
            "edges": list(self._edges),
        }
        dag_hash = deterministic_hash(body, "CausalDAG")

        return CausalDAG(nodes=self._nodes, edges=self._edges, dag_hash=dag_hash)
