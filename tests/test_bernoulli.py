
from monty.bernoulli import estimate_failure

def test_seed_reproducibility():
    result1 = estimate_failure(0.5, 1000, seed=123)
    result2 = estimate_failure(0.5, 1000, seed=123)
    assert result1 == result2

def test_zero_probability():
    assert estimate_failure(0.0, 100, seed=1) == 0.0

def test_one_probability():
    assert estimate_failure(1.0, 100, seed=1) == 1.0

def test_results_in_range():
    r = estimate_failure(0.5, 1000, seed=123)
    assert 0.0 <= r <= 1.0