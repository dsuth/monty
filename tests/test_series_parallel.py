from monty.models.series_parallel import series_estimate_failure
from monty.models.series_parallel import parallel_estimate_failure

def test_series_any_one_means_system_always_fails():
    # OR fail: if any component always fails, system always fails
    assert series_estimate_failure([0, 0, 1], trials=100, seed=123) == 1.0


def test_series_all_zeros_means_system_never_fails():
    assert series_estimate_failure([0, 0, 0], trials=100, seed=123) == 0.0


def test_series_all_ones_means_system_always_fails():
    assert series_estimate_failure([1, 1, 1], trials=100, seed=123) == 1.0


def test_parallel_all_ones_required_for_system_always_fails():
    # AND fail: system fails only if all components fail
    assert parallel_estimate_failure([1, 1, 1], trials=100, seed=123) == 1.0


def test_parallel_any_zero_means_system_never_fails():
    assert parallel_estimate_failure([0, 1, 1], trials=100, seed=123) == 0.0


def test_parallel_all_zeros_means_system_never_fails():
    assert parallel_estimate_failure([0, 0, 0], trials=100, seed=123) == 0.0


def test_seed_reproducibility_series():
    ps = [0.2, 0.3, 0.4]
    a = series_estimate_failure(ps, trials=5000, seed=7)
    b = series_estimate_failure(ps, trials=5000, seed=7)
    assert a == b


def test_seed_reproducibility_parallel():
    ps = [0.2, 0.3, 0.4]
    a = parallel_estimate_failure(ps, trials=5000, seed=7)
    b = parallel_estimate_failure(ps, trials=5000, seed=7)
    assert a == b