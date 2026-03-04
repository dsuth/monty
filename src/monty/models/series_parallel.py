from __future__ import annotations

import random

# ---- CURRENTLY JUST COPIES OF ESTIMATE_FAILURE - TBD ----
def series_estimate_failure(ps: list[float], trials: int, seed: int | None = None) -> float:
    
    if trials <= 0:
        raise ValueError("trials must be > 0")
    if len(ps) == 0:
        raise ValueError("ps must contain at least one entry")
    for p in ps:
        if not 0 <= p <= 1:
            raise ValueError("ps must be between 0..1")
    rng = random.Random(seed)
    
    failures = 0
    
    
    for _ in range(trials):
        # In a series system, if any component fails, the entire system fails
        system_failed = False

        for p in ps:
            if rng.random() < p:
                system_failed = True
                break
        
        if system_failed:
            failures += 1

    return failures / trials

def parallel_estimate_failure(ps: list[float], trials: int, seed: int | None = None) -> float:
    if trials <= 0:
        raise ValueError("trials must be > 0")
    if len(ps) == 0:
        raise ValueError("ps must contain at least one entry")
    for p in ps:
        if not 0 <= p <= 1:
            raise ValueError("ps must be between 0..1")

    rng = random.Random(seed)
    
    failures = 0
    
    for _ in range(trials):
        # In a parallel system, the system fails if all components fail
        system_failed = True
        for p in ps:
            if rng.random() >= p:
                system_failed = False
                break
        if system_failed:
            failures += 1

    return failures / trials