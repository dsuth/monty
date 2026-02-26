# Monty Roadmap

Monty is a learning-first Monte Carlo CLI tool that evolves toward a small, professional-grade probabilistic modelling framework.

The project progresses in layers:
- **CLI + clean architecture** (foundation)
- **Reusable simulation engine** (correctness + testability)
- **Model library** (engineering-relevant examples)
- **Time-based / maintenance-aware simulation** (discrete-event)
- **Graph-defined models / Petri-net style authoring** (long-term)

---

## Principles

- **Code stays modular:** CLI orchestration is separate from modelling and simulation logic.
- **Determinism is first-class:** seeded RNG support is required for tests and reproducible runs.
- **Test coverage grows with features:** every new model or engine capability gets unit tests.
- **No premature UI:** define stable model schemas and engine APIs before building any GUI.
- **Small increments, vertical slices:** each milestone should end in a working CLI tool.

---

## Milestones

### M1 — Professional CLI baseline (v0.1 → v0.2)
**Goal:** clean user experience and first test suite.

- Replace manual `ValueError` validation with argparse-native validation (clean error messages, no traceback).
- Add `pytest` and minimum tests:
  - boundary tests: p=0 → 0.0, p=1 → 1.0
  - seed reproducibility: same seed → same output
- Improve README quickstart and usage examples.
- Ensure `pip install -e ".[dev]"` works reliably.

Deliverables:
- `monty --help` is clean and accurate
- `pytest` passes
- invalid args produce user-friendly errors

---

### M2 — Modularize into engine + model (v0.2 → v0.3)
**Goal:** separate concerns; prepare for multiple models.

- Extract RNG creation into `engine/rng.py`
- Extract trial running loop into `engine/runner.py`
- Extract summarization into `engine/stats.py`
- Implement a `models/base.py` interface/protocol
- Move Bernoulli model to `models/bernoulli.py`

Deliverables:
- CLI becomes a thin orchestration layer
- engine/model boundaries are clear
- tests cover runner + bernoulli model

---

### M3 — Engineering-relevant models (v0.3 → v0.4)
**Goal:** reliability composition and fault-tree-like logic.

Add:
- `models/series_parallel.py`
- CLI options:
  - `--model bernoulli|series|parallel`
  - `--ps 0.02 0.05 0.01` (component probabilities)
- New tests:
  - series edge cases (AND): p=[0, …] → 0, p=[1,1,1] → 1
  - parallel edge cases (OR): any p=1 → 1, all p=0 → 0

Deliverables:
- simple reliability block diagram logic by CLI
- deterministic tests with fixed seeds

---

### M4 — Output modes and stable schema (v0.4 → v0.5)
**Goal:** support humans and machines.

- Add `--json` output mode
- Define a stable JSON schema (`io/schema.py`)
- Add an output module (`io/output.py`) for formatted console output
- Tests for output schema shape (keys exist, types correct)

Deliverables:
- `monty ... --json` produces stable machine-readable output
- console output remains clean and readable

---

### M5 — Timeline Monte Carlo (Discrete-Event) Engine (v0.5 → v0.7)
**Goal:** move from static probabilities to time-to-failure distributions.

Introduce a discrete-event simulation capability:
- event queue (next failure time, repair completion, proof test)
- component states: healthy, failed-safe, failed-dangerous-detected, failed-dangerous-undetected, under repair
- repair time distribution (start simple: fixed MTTR; later: lognormal)
- proof test interval T (detects latent failures)
- optional diagnostic coverage (splits dangerous failures into detected vs undetected)

Deliverables:
- simulate distributions like:
  - time-to-first-dangerous-failure
  - fraction of time unavailable
  - spurious trip rate (optional)
- CLI can run a “simple SIF” model:
  - sensor, logic solver, final element
- baseline plots may be out-of-scope initially; focus on summary stats

---

### M6 — Graph-defined models (Petri-net / state graph) (v0.7 → v1.0)
**Goal:** define models as graphs rather than hardcoded Python classes.

Key idea: separate into:
1) **core engine**: runs discrete-event Monte Carlo on a generic graph/state-machine definition
2) **model authoring**: define nets/graphs in JSON/YAML; (GUI later)

Define:
- a schema for places/states, transitions, and timing distributions
- mapping from Petri net concepts to the discrete-event engine
- validation tooling for graph definitions

Deliverables:
- load model from JSON/YAML
- run timeline simulation without writing new Python model classes
- stable reporting outputs

---

## Future Enhancements (Optional)

- NumPy backend for vectorized simulation (where applicable)
- confidence intervals and convergence diagnostics
- sensitivity analysis (vary key parameters; generate response surfaces)
- common-cause failures and dependency modelling
- CI pipeline (GitHub Actions) running tests on Windows/macOS/Linux
- packaging/distribution:
  - publish to PyPI
  - recommend `pipx install monty` for CLI users
  - optional PyInstaller builds for “no Python required” binaries

---

## North Star Use Case: Simple SIS / SIF Maintenance Planning

Build a Petri-net-ish / state-graph model of a SIF (Sensor → Logic → Final Element) to estimate:
- time-to-dangerous-failure distribution
- unavailability over time
- maintenance / proof test interval effects
- spurious trip distributions (optional)

Primary outcome: support maintenance planning and overhaul timing using probabilistic distributions rather than point estimates.