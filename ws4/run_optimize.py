#!/usr/bin/env python3
"""Run a ws4 optimisation from the translated MKRF pilot schedule.

This is a thin pilot harness over the ws4 optimiser. It is deliberately
separate from the ws4 CLI so the pilot can be reproduced without changing the
ws4 package: the ws4 search already accepts an initial schedule through
``Optimizer._solve(initial=...)``, and this script loads the translated
``block_id,treatment,period`` CSV into that form.

The output directory is a normal ws4 search run: ``schedule.csv``,
``summary.json``, account/product values, patch accounts, spatial checks and
reports. The web UI can serve it alongside the simulation run.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

INSTANCE_ROOT = Path(__file__).resolve().parents[1]
WS4_ROOT = INSTANCE_ROOT / "ws4"
DEFAULT_DATASET = WS4_ROOT / "runtime" / "matrix"
DEFAULT_RUN = WS4_ROOT / "runtime" / "optimized"


def load_schedule_csv(path: Path) -> dict[int, tuple[tuple[str, int], ...]]:
    """Load a ``block_id,treatment,period`` schedule into ws4's chain form."""
    frame = pd.read_csv(path)
    required = {"block_id", "treatment", "period"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(
            f"schedule {path} is missing required columns: {', '.join(sorted(missing))}"
        )
    schedule: dict[int, tuple[tuple[str, int], ...]] = {}
    for block, group in frame.groupby("block_id", sort=False):
        schedule[int(block)] = tuple(
            sorted(
                (
                    (str(treatment), int(period))
                    for treatment, period in zip(
                        group["treatment"], group["period"], strict=True
                    )
                ),
                key=lambda event: event[1],
            )
        )
    return schedule


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--targets", type=Path, default=WS4_ROOT / "targets.yaml")
    parser.add_argument(
        "--initial-schedule",
        type=Path,
        default=WS4_ROOT / "schedules" / "greenup_greedy.csv",
    )
    parser.add_argument(
        "--patch-accounts", type=Path, default=WS4_ROOT / "patch_accounts.yaml"
    )
    parser.add_argument("--topology", type=Path, default=WS4_ROOT / "topology.csv")
    parser.add_argument("--years", type=int, default=100)
    parser.add_argument("--iterations", type=int, default=200)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--temperature", type=float, default=1000.0)
    parser.add_argument("--cooling", type=float, default=0.99)
    parser.add_argument("--out", type=Path, default=DEFAULT_RUN)
    parser.add_argument("--max-opening-ha", type=float, default=50.0)
    parser.add_argument("--min-green-up-years", type=int, default=5)
    parser.add_argument(
        "--spatial-weight",
        type=float,
        default=1_000_000.0,
        help="Penalty weight on the opening/green-up rules; the pilot keeps this high.",
    )
    args = parser.parse_args()

    import random

    from ws4.opt.core import Problem
    from ws4.opt.engine import OptimizeConfig, Optimizer
    from ws4.opt.objective import load_targets
    from ws4.opt.solvers import solve_sa
    from ws4.patch.accounts import load_patch_accounts
    from ws4.report import write_report
    from ws4.sim.engine import Simulator

    cfg = OptimizeConfig(
        targets_path=str(args.targets),
        years=args.years,
        iterations=args.iterations,
        seed=args.seed,
        workers=1,
        starts=1,
        topology_path=str(args.topology),
        patch_accounts_path=str(args.patch_accounts),
        max_opening_ha=args.max_opening_ha,
        min_green_up_years=args.min_green_up_years,
        spatial_weight=args.spatial_weight,
    )
    optimiser = Optimizer.from_dataset(args.dataset, cfg)
    initial = load_schedule_csv(args.initial_schedule)
    targets = load_targets(args.targets)
    # Use the whole-schedule evaluator so the opening/green-up penalty is part of
    # every move. The incremental delta path prices targets only, so a search on
    # that path can improve the targets by violating the spatial rules.
    problem = Problem(
        evaluate=lambda schedule: optimiser._evaluate(schedule, targets),
        candidates=optimiser.candidates(),
        registry=optimiser.registry,
    )
    best, objective = solve_sa(
        problem,
        random.Random(args.seed),
        iterations=args.iterations,
        temperature=args.temperature,
        cooling=args.cooling,
        initial=initial,
    )

    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    schedule_path = out / "schedule.csv"
    optimiser._schedule_frame(best).to_csv(schedule_path, index=False)

    simulator = Simulator.from_dataset(args.dataset)
    simulator.run(
        schedule_csv=schedule_path,
        years=args.years,
        out_dir=out,
        topology_csv=args.topology,
        patch_accounts=load_patch_accounts(args.patch_accounts),
        patch_membership=True,
        max_opening_ha=args.max_opening_ha,
        min_green_up_years=args.min_green_up_years,
    )

    values = pd.read_csv(out / "account_values.csv")
    write_report(values, targets, out)

    summary = {
        "status": "ok",
        "kind": "search",
        "incumbent_objective": objective,
        "iterations": args.iterations,
        "seed": args.seed,
        "years": args.years,
        "starts": 1,
        "blocks_scheduled": len(best),
        "initial_schedule_path": str(args.initial_schedule),
        "targets_path": str(args.targets),
        "topology_path": str(args.topology),
        "patch_accounts_path": str(args.patch_accounts),
        "max_opening_ha": args.max_opening_ha,
        "min_green_up_years": args.min_green_up_years,
        "spatial_weight": args.spatial_weight,
    }
    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
