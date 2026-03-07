from __future__ import annotations
from dataclasses import dataclass

import random

@dataclass
class RunResult:
    failures: int
    trials: int


def run_trials(model, trials: int, seed: int | None = None) -> RunResult:
    if trials <= 0:
        raise ValueError("trials must be > 0")
    
    rng = random.Random(seed)
    
    failures = 0

    for _ in range(trials):
        if model.trial(rng):
            failures += 1

    return RunResult(failures = failures, trials = trials)
