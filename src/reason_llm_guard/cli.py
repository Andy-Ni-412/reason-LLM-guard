from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .analysis import ObjectiveWeights, analyze
from .demo import generate_demo_records
from .schema import read_jsonl, write_jsonl


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cips")
    commands = parser.add_subparsers(dest="command", required=True)

    demo = commands.add_parser("demo", help="generate synthetic paired results")
    demo.add_argument("--output", required=True)
    demo.add_argument("--samples", type=int, default=150)
    demo.add_argument("--seed", type=int, default=42)

    report = commands.add_parser("analyze", help="analyze paired intervention results")
    report.add_argument("path")
    report.add_argument("--bootstrap", type=int, default=2000)
    report.add_argument("--seed", type=int, default=42)
    report.add_argument("--unsafe-weight", type=float, default=1.0)
    report.add_argument("--utility-loss-weight", type=float, default=1.0)
    report.add_argument("--cost-weight", type=float, default=0.05)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "demo":
        records = generate_demo_records(samples=args.samples, seed=args.seed)
        write_jsonl(args.output, records)
        print(f"wrote {len(records)} intervention results to {args.output}")
        return

    weights = ObjectiveWeights(
        unsafe=args.unsafe_weight,
        utility_loss=args.utility_loss_weight,
        cost=args.cost_weight,
    )
    report = analyze(
        read_jsonl(args.path), weights=weights, bootstrap=args.bootstrap, seed=args.seed
    )
    print(json.dumps(asdict(report), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

