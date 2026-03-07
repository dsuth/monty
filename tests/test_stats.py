from monty.engine.stats import failure_rate, wilson_interval


def test_failure_rate_zero():
    assert failure_rate(0, 10) == 0.0


def test_failure_rate_one():
    assert failure_rate(10, 10) == 1.0


def test_failure_rate_half():
    assert failure_rate(5, 10) == 0.5


def test_wilson_interval_bounds_are_ordered():
    low, high = wilson_interval(5, 10)
    assert 0.0 <= low <= high <= 1.0


def test_wilson_interval_contains_estimate():
    p_hat = failure_rate(5, 10)
    low, high = wilson_interval(5, 10)
    assert low <= p_hat <= high