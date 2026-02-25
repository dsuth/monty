import argparse
import random

def estimate_failure(probability: float, trials: int, seed: int | None = None) -> float:
    rng = random.Random(seed)
    failures = 0
    for _ in range(trials):
        failures += rng.random() < probability
    return failures / trials

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="monty", description="Monte Carlo estimation tool")
    p.add_argument("--p", type=float, required=True, help="Failure probability (0..1)")
    p.add_argument("--trials", type=int, default=10000, help="Number of trials")
    p.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    return p

def main() -> int:
    args = build_parser().parse_args()

    if not (0.0 <= args.p <= 1.0):
        raise ValueError("--p must be between 0 and 1")
    if args.trials <= 0:
        raise ValueError("--trials must be >0")
    
    rate = estimate_failure(args.p, args.trials, args.seed)
    print(f"Estimated failure rate: {rate:.6f} (p={args.p}, trials = {args.trials}, seed={args.seed})")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
