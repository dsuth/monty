import argparse
from monty.models.bernoulli import BernoulliModel
from monty.models.series_parallel import SeriesModel, ParallelModel
from monty.engine.runner import run_trials
from monty.engine.stats import failure_rate, wilson_interval

# ---- CLI-specific validators ----

def parse_probability(value: str) -> float:
    try:
        p = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError("probability must be a number")
    if not 0 <= p <= 1:
        raise argparse.ArgumentTypeError("probability must be between 0..1"
        )
    return p

def parse_positive_int(value: str) -> int:
    try:
        i = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("trials must be a number")
    if i <= 0:
        raise argparse.ArgumentTypeError("trials must be a positive integer")
    return i

# ---- CLI arg parsing ----
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="monty", description="Monte Carlo estimation tool")
    p.add_argument("--model", choices=["bernoulli", "series", "parallel"], required=True, help="Which model to use")
    p.add_argument("--p", type=parse_probability, help="Failure probability (0..1)")
    p.add_argument("--ps", type=parse_probability, nargs="+", help="Space separated entries for parallel / series model")
    p.add_argument("--trials", type=parse_positive_int, default=10000, help="Number of trials")
    p.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
       
    return p

# ---- main (currently contains model, to be moved out) ----
def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.model == "bernoulli":
        if args.p is None:
            parser.error("--p is required when --model bernoulli")
        if args.ps is not None:
            parser.error("--ps is not valid when --model bernoulli")

    elif args.model in ("series", "parallel"):
        if args.ps is None:
            parser.error("--ps is required when --model series|parallel")
        if args.p is not None:
            parser.error("--p is not valid when --model series|parallel")

    else:
        # Should never happen because argparse choices=... prevents it,
        # but keep as a guard in case something changes later.
        parser.error(f"Unknown model: {args.model}")  
    
    if args.model == "bernoulli":
        model = BernoulliModel(args.p)
    elif args.model == "series":
        model = SeriesModel(args.ps)
    elif args.model == "parallel":
        model = ParallelModel(args.ps)
 

    result = run_trials(model, args.trials, args.seed)
    rate = failure_rate(result.failures, result.trials)
    low, high = wilson_interval(result.failures, result.trials)

    if args.model == "bernoulli":
        print(
            f"Estimated failure rate: {rate:.6f} "
            f"(95% CI: {low:.6f} to {high:.6f}) "
            f"(model={args.model}, p={args.p}, trials={args.trials}, seed={args.seed})"
        )
    else: 
        print(
            f"Estimated failure rate: {rate:.6f} "
             f"(95% CI: {low:.6f} to {high:.6f}) "
            f"(model={args.model}, ps={args.ps}, trials={args.trials}, seed={args.seed})"
        )
    
    return 0
# ---- if called directly, run main() ----
if __name__ == "__main__":
    raise SystemExit(main())
