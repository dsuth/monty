import random
from monty.models.bernoulli import BernoulliModel

def test_zero_probability():
    rng = random.Random(1)
    model = BernoulliModel(0.0)
    assert model.trial(rng) is False

def test_one_probability():
    rng = random.Random(1)
    model = BernoulliModel(1.0)
    assert model.trial(rng) is True

def test_returns_boolean():
    rng = random.Random(1)
    model = BernoulliModel(0.5)

    result = model.trial(rng)

    assert isinstance(result, bool)