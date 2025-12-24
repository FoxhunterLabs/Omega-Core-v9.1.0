________________________________________
Omega Core v9.1.0
Deterministic Governance Kernel for Autonomous Systems
________________________________________
What This Is
Omega Core is a deterministic, event-sourced governance kernel for autonomous and semi-autonomous systems.
It exists to answer one question rigorously:
Who (or what) was allowed to decide, why, and can that decision be independently verified later?
Omega Core enforces safety-critical constraints such as:
•	replayable decision history
•	cryptographic auditability
•	symbolic (non-numeric) refusal causality
•	verifiable evidence trust boundaries
•	adversarial tamper detection
•	explicit human accountability workflows
This is not an ML system.
This is not a UI framework.
This is not autonomy “policy glue.”
It is a governance kernel.
________________________________________
What This Is Not (Important)
Omega Core deliberately does not:
•	optimize decisions
•	learn policies
•	rank risks numerically
•	make operational control decisions
•	depend on wall-clock time
•	trust inline data over canonical artifacts
If you are looking for:
•	control loops
•	planners
•	perception pipelines
•	scoring engines
Those belong outside this repo.
________________________________________
Core Design Principles
1. Determinism Over Cleverness
Every decision, hash, timestamp, and ID is reproducible from inputs alone.
If replay produces different results, the system is considered invalid.
________________________________________
2. Event-Sourced Governance
All governance state is derived from immutable events.
There is no mutable “current truth.”
There is only what happened.
________________________________________
3. Symbolic Authority, Not Numeric Authority
Numeric values are explicitly prohibited from directly causing refusal decisions.
Refusals must be explained via symbolic reasons with evidence references.
This prevents:
•	threshold laundering
•	hidden scalar vetoes
•	post-hoc numeric justification
________________________________________
4. Hard Evidence Trust Boundary
Evidence is verified only from canonical artifacts stored in a capsule.
Inline evidence_data exists for convenience only and is never authoritative.
If the capsule artifact cannot be re-derived → verification fails.
________________________________________
5. Fail Closed, Always
If verification is incomplete, ambiguous, or unimplemented:
The system refuses to certify.
“No answer” is treated as unsafe.
________________________________________
Repository Structure
omega-core/
├── omega_core/          # Canonical kernel (authoritative)
│   ├── core/            # Deterministic primitives
│   ├── governance/      # Event-sourced governance law
│   ├── evidence/        # Verifiable evidence + capsule boundary
│   ├── reasoning/       # Symbolic causality (no numeric authority)
│   ├── threat/          # Adversarial tamper modeling
│   ├── workflows/       # Accountability & closure blocking
│   ├── proof/           # Minimal audit bundles
│   ├── verifier/        # Standalone capsule verifier
│   └── tests/           # Property-based invariant tests
│
├── ui/                  # Non-canonical visualization layer
│   ├── README.md
│   └── app.py
│
└── README.md             # You are here
Authority lives only in omega_core/.
Everything else is replaceable.
________________________________________
Governance Lifecycle (High Level)
OBSERVED
   ↓
ASSESSED
   ↓
DECIDED
   ↓
COMMITTED
   ↓
ACKED (optional)
   ↓
CLOSED
Enforced Invariants
•	Refusal decisions require prior ASSESSED state
•	Governance cannot CLOSE while workflows block closure
•	Event chains must hash-validate end-to-end
•	State continuity must hold across events
•	Threat detection freezes progression until acknowledged
Violations raise hard exceptions.
________________________________________
Evidence & Verification Model
Evidence Rules
1.	Evidence references a canonical capsule artifact
2.	Hashes are recomputed from the capsule only
3.	Inline copies are ignored for verification
4.	Mismatch = failure
Verification Philosophy
The verifier is allowed to say:
•	VALID
•	INVALID
•	INVALID: verification incomplete
It is not allowed to say “probably.”
________________________________________
Accountability Workflows
Certain governance events create obligations:
•	acknowledgment deadlines
•	escalation rules
•	closure blocking
These are modeled as workflow contracts, not comments or logs.
Governance cannot close while obligations remain unresolved.
________________________________________
Threat Modeling
Omega Core includes an adversarial mode to simulate:
•	log tampering
•	field deletion
•	event reordering
•	replay drift
Detected threats:
•	emit governance events
•	block progression
•	require explicit acknowledgment
This is for testing, not production monitoring.
________________________________________
Tests (What Is Proven)
The test suite asserts:
•	event hash determinism
•	governance invariant enforcement
•	numeric authority prohibition
•	negative authority proof completeness
Tests are:
•	deterministic
•	seed-controlled
•	kernel-only (no UI, no filesystem)
________________________________________
Requirements
Runtime
•	Python 3.10+
•	No external services required
Python Dependencies
Core kernel:
•	none (stdlib only)
UI (optional):
•	streamlit
•	pandas
Testing:
•	pytest
The kernel intentionally avoids heavy dependencies to preserve auditability.
________________________________________
Known Limitations (Honest)
The following are intentionally incomplete and currently cause verification to fail closed:
•	Full authority claim ID re-derivation
•	Full negative authority proof verification
•	Full governance event chain replay verification in the standalone verifier
These are not bugs.
They are explicit refusals to certify partial truth.
________________________________________
Intended Use Cases
•	autonomy oversight
•	human-in-the-loop safety gating
•	audit-grade decision provenance
•	infrastructure / fleet governance
•	regulated or liability-sensitive systems
________________________________________
Non-Goals
•	end-to-end autonomy
•	real-time control
•	probabilistic decision engines
•	“AI alignment” abstractions
•	policy optimization
Omega Core governs decisions, not behavior.
________________________________________
Final Note
If you are reading this looking for:
•	hype → you won’t find it here
•	guarantees → you will
•	shortcuts → none exist
Omega Core is built to be inspectable, replayable, and boring in court.
That’s the point.
________________________________________
