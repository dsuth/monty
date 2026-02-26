from __future__ import annotations

import random

def estimate_failure(probability: float, trials: int, seed: int | None = None) -> float:
    rng = random.Random(seed)
    failures = 0
    for _ in range(trials):
        failures += rng.random() < probability

    if trials <= 0:
        raise ValueError("trials must be > 0")
    return failures / trials
