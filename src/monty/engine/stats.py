from __future__ import annotations

import math

def failure_rate(failures: int, trials: int) -> float:
    if trials <= 0:
        raise ValueError("trials must be > 0")
    if failures < 0:
        raise ValueError("failures must be >= 0")
    if failures > trials:
        raise ValueError("failures must be <= trials")
    
    return failures / trials

def wilson_interval(failures: int, trials: int, z: float = 1.96) -> tuple[float, float]:
    if trials <= 0:
        raise ValueError("trials must be > 0")
    if failures < 0:
        raise ValueError("failures must be >= 0")
    if failures > trials:
        raise ValueError("failures must be <= trials")
    if z <= 0:
        raise ValueError("z must be > 0")
    
    p_hat = failures / trials
    z2 = z ** 2
    denominator = 1 + z2 / trials

    centre = (p_hat + z2 / (2 * trials)) / denominator
    margin = (
        z
        * math.sqrt((p_hat * (1 - p_hat) / trials) + (z2 / (4 * trials ** 2)))
    )
    return centre - margin, centre + margin
