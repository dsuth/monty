from monty.engine.runner import run_trials
from monty.engine.runner import run_trials, RunResult
from monty.models.bernoulli import BernoulliModel
import pytest
from unittest.mock import Mock

def test_run_trials_valid_input():
    mock_model = Mock()
    mock_model.trial.return_value = False
    result = run_trials(mock_model, trials=5)
    assert result.failures == 0
    assert result.trials == 5
    assert mock_model.trial.call_count == 5


def test_run_trials_with_failures():
    mock_model = Mock()
    mock_model.trial.side_effect = [True, False, True, False, False]
    result = run_trials(mock_model, trials=5)
    assert result.failures == 2
    assert result.trials == 5
    assert mock_model.trial.call_count == 5


def test_run_trials_all_failures():
    mock_model = Mock()
    mock_model.trial.return_value = True
    result = run_trials(mock_model, trials=3)
    assert result.failures == 3
    assert result.trials == 3


def test_run_trials_invalid_trials_zero():
    mock_model = Mock()
    with pytest.raises(ValueError, match="trials must be > 0"):
        run_trials(mock_model, trials=0)


def test_run_trials_invalid_trials_negative():
    mock_model = Mock()
    with pytest.raises(ValueError, match="trials must be > 0"):
        run_trials(mock_model, trials=-1)


def test_run_trials_with_seed():
    model = BernoulliModel(0.5)
    result1 = run_trials(model, trials=100, seed=42)
    result2 = run_trials(model, trials=100, seed=42)
    assert result1 == result2


def test_run_trials_single_trial():
    mock_model = Mock()
    mock_model.trial.return_value = False
    result = run_trials(mock_model, trials=1)
    assert result.failures == 0
    assert result.trials == 1
