"""
Deterministic logical clock.
No wall time. No entropy.
"""

class DeterministicClock:
    def __init__(self, session_id: str):
        self.session_id = session_id

    def ts(self, *, tick: int, local_seq: int = 0) -> str:
        return f"OMEGA_T{int(tick):09d}_S{int(local_seq):06d}"
