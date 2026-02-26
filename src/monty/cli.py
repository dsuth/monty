import argparse
from monty.bernoulli import estimate_failure

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
    p.add_argument("--p", type=parse_probability, required=True, help="Failure probability (0..1)")
    p.add_argument("--trials", type=parse_positive_int, default=10000, help="Number of trials")
    p.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    return p

# ---- main (currently contains model, to be moved out) ----
def main() -> int:
    args = build_parser().parse_args()
      
    rate = estimate_failure(args.p, args.trials, args.seed)
    print(f"Estimated failure rate: {rate:.6f} (p={args.p}, trials = {args.trials}, seed={args.seed})")
    return 0

# ---- if called directly, run main() ----
if __name__ == "__main__":
    raise SystemExit(main())
