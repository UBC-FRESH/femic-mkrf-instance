#!/usr/bin/env python3
"""Build a simple green-up-aware clearcut schedule for the MKRF pilot.

The schedule is deliberately conservative: one block per opening, no two
selected blocks adjacent within 100 m, and no block adjacent to a block
disturbed in the previous five years. Blocks larger than the opening ceiling
are left unharvested.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--topology", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--years", type=int, default=100)
    parser.add_argument("--greenup", type=int, default=5)
    parser.add_argument("--max-opening-ha", type=float, default=50.0)
    parser.add_argument("--min-age", type=int, default=60)
    args = parser.parse_args()

    fragments = pd.read_parquet(args.dataset / "fragments.parquet")
    block_area = fragments.groupby("block_id")["area_ha"].sum().to_dict()
    block_age = fragments.groupby("block_id")["age"].min().to_dict()
    topology = pd.read_csv(args.topology)
    neighbours: dict[int, set[int]] = defaultdict(set)
    for row in topology.itertuples(index=False):
        a, b = int(row.BLOCK1), int(row.BLOCK2)
        if a < 0 or b < 0:
            continue
        neighbours[a].add(b)
        neighbours[b].add(a)

    last_disturbed = {block: -10_000 for block in block_area}
    next_eligible = {
        block: max(0, args.min_age - int(age)) for block, age in block_age.items()
    }
    selected_by_year: dict[int, list[int]] = defaultdict(list)
    for year in range(args.years):
        candidates = [
            block
            for block, ready in next_eligible.items()
            if ready <= year and block_area[block] <= args.max_opening_ha
        ]
        # Oldest first, then largest, to favour the stands closest to a rotation.
        candidates.sort(
            key=lambda block: (year - block_age[block], block_area[block]),
            reverse=True,
        )
        chosen: list[int] = []
        chosen_set: set[int] = set()
        for block in candidates:
            if any(
                neighbour in chosen_set
                or year - last_disturbed[neighbour] <= args.greenup
                for neighbour in neighbours.get(block, ())
            ):
                continue
            if year - last_disturbed[block] <= args.greenup:
                continue
            chosen.append(block)
            chosen_set.add(block)
            last_disturbed[block] = year
            next_eligible[block] = year + args.min_age
        selected_by_year[year] = chosen

    rows = [
        {"block_id": block, "treatment": "CC", "period": year}
        for year, blocks in selected_by_year.items()
        for block in blocks
    ]
    schedule = pd.DataFrame(rows, columns=["block_id", "treatment", "period"])
    schedule = schedule.sort_values(["period", "block_id"], kind="stable")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    schedule.to_csv(args.out, index=False)
    print(f"wrote {len(schedule)} events to {args.out}")
    print(schedule.groupby("period").size().head(20).to_string())


if __name__ == "__main__":
    main()
