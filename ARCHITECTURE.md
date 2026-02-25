monty/
  pyproject.toml
  README.md
  LICENSE
  ARCHITECTURE.md

  src/
    monty/
      __init__.py
      cli.py

      config.py

      engine/
        __init__.py
        rng.py
        runner.py
        stats.py

      models/
        __init__.py
        base.py
        bernoulli.py
        series_parallel.py

      io/
        __init__.py
        output.py
        schema.py

  tests/
    test_cli_validation.py
    test_rng.py
    test_runner.py
    test_stats.py
    test_models_bernoulli.py
    test_models_series_parallel.py


#    Layering and responsibilities
# cli.py — Command-line interface only

Purpose: Parse arguments, select model, call engine, print output, set exit codes.
Rules:

No simulation logic here.

Minimal branching.

Errors should be user-friendly (argparse validation; no tracebacks for invalid args).

Typical flow:

parse args → 2) build config → 3) build model → 4) run simulation → 5) format output

# config.py — Typed, validated configuration objects

Purpose: Convert CLI arguments (strings/ints) into clean, validated config structures.

Example conceptual objects:

RunConfig(trials, seed)

ModelConfig(kind, params...)

OutputConfig(format="text|json")

Why it exists: stops “loose dict soup” and centralizes validation.

# Engine (generic Monte Carlo machinery)
# engine/rng.py — RNG creation + interface

Purpose: One place to create and manage random generators.

Key idea: pass an RNG object around (testable, reproducible).

v0: wraps random.Random(seed)

v1: optionally supports NumPy RNG behind same interface

# engine/runner.py — Run N trials, collect outcomes

Purpose: The generic simulation loop.

Conceptual API:

run_trials(model, run_config) -> Results

Rules:

Runner does not know domain logic.

Runner just asks the model for a trial outcome.

# engine/stats.py — Summarize outcomes

Purpose: Convert raw outcomes into useful stats.

Examples:

mean/failure rate

counts

basic confidence intervals (later)

quantiles for numeric outcomes (later)

Rule: mostly pure functions (easy unit tests).

# Models (domain logic)
# models/base.py — Model interface

Purpose: Define what a “model” must provide.

Conceptual protocol:

trial(rng) -> outcome

(optionally) describe() -> dict/str for reporting

Outcome types (phased approach):

v0/v1: boolean (fail/success)

later: numeric loss (severity), or structured outcome

# models/bernoulli.py — simplest model

Purpose: single event with probability p.

trial(rng) draws uniform random and compares to p.

# models/series_parallel.py — reliability composition

Purpose: series/parallel logic over component probabilities.

series (AND): system fails if all components fail

parallel (OR): system fails if any component fails

(And later: mixed topologies / fault tree nodes.)

# IO (presentation / interchange)
io/output.py — human-readable output formatting

Purpose: print tables/lines for CLI.

io/schema.py — JSON output structure

Purpose: define stable JSON keys so results are machine-readable.

# Tests (non-negotiable in this project)

Philosophy: test boundaries + determinism + composition logic.

test_cli_validation.py: invalid args yield clean errors, correct exit codes

test_rng.py: same seed → same sequence (and isolated RNG)

test_runner.py: runner calls model correct number of times; determinism with seed

test_stats.py: stats correctness on known arrays

test_models_*: model correctness for p=0, p=1, series/parallel edge cases

# Milestones to implement incrementally
# Milestone 1 — Clean CLI errors + first tests

Use argparse type validators for --p and --trials

Add pytest

Add boundary tests: p=0 → 0, p=1 → 1

# Milestone 2 — Split into engine + model modules

Extract estimate_failure() into models/bernoulli.py + engine/runner.py

CLI becomes thin orchestration

# Milestone 3 — Add series/parallel model

--model bernoulli|series|parallel

--ps 0.02 0.05 0.01 style input

Tests for OR/AND logic

# Milestone 4 — Output modes

default text

--json output with stable schema

# Milestone 5 — (Optional) NumPy backend

drop-in vectorized runner for speed

keep API stable; tests unchanged

# One-line “contract” for the whole architecture

CLI parses → config validates → model defines one trial → runner repeats trials → stats summarizes → output prints.