import random

from monty.models.series_parallel import SeriesModel, ParallelModel


def test_series_any_one_means_system_fails():
    rng = random.Random(1)
    model = SeriesModel([0.0, 0.0, 1.0])
    assert model.trial(rng) is True


def test_series_all_zeros_means_system_does_not_fail():
    rng = random.Random(1)
    model = SeriesModel([0.0, 0.0, 0.0])
    assert model.trial(rng) is False


def test_series_all_ones_means_system_fails():
    rng = random.Random(1)
    model = SeriesModel([1.0, 1.0, 1.0])
    assert model.trial(rng) is True


def test_parallel_all_ones_required_for_system_failure():
    rng = random.Random(1)
    model = ParallelModel([1.0, 1.0, 1.0])
    assert model.trial(rng) is True


def test_parallel_any_zero_means_system_does_not_fail():
    rng = random.Random(1)
    model = ParallelModel([0.0, 1.0, 1.0])
    assert model.trial(rng) is False


def test_parallel_all_zeros_means_system_does_not_fail():
    rng = random.Random(1)
    model = ParallelModel([0.0, 0.0, 0.0])
    assert model.trial(rng) is False


def test_series_returns_boolean():
    rng = random.Random(1)
    model = SeriesModel([0.2, 0.3, 0.4])
    result = model.trial(rng)
    assert isinstance(result, bool)


def test_parallel_returns_boolean():
    rng = random.Random(1)
    model = ParallelModel([0.2, 0.3, 0.4])
    result = model.trial(rng)
    assert isinstance(result, bool)