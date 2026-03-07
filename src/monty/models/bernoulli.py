from __future__ import annotations

class BernoulliModel:
    def __init__(self, p: float) -> None:
        if not 0 <= p <= 1:
            raise ValueError("p must be between 0..1")
        self.p = p

    def trial(self, rng) -> bool:
        return rng.random() < self.p

