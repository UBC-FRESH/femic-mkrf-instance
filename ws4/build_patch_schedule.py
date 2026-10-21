#!/usr/bin/env python3
"""Build a patch-first clearcut schedule for the MKRF pilot.

The policy controls opening size with 5-40 ha targets. Random move-based search
struggles to form same-year openings, so this script builds them directly:

1. aggregate the managed fragments to blocks (area, age, yield curve);
2. grow connected clusters of touching blocks until they reach the 5-40 ha band;
3. assign each opening a harvest year, filling decades toward the target volume;
4. emit a ``block_id,treatment,period`` schedule for ws4.

Blocks larger than the upper band are left unharvested. Small clusters that
cannot reach the lower band are left unharvested as well. The output is a
starting schedule, not a final optimized plan.
"""

from __future__ import annotations

import argparse
from collections import defaultdict, deque
from pathlib import Path

import numpy as np
import pandas as pd


def _load_blocks(
    dataset: Path,
) -> tuple[dict[int, dict[str, object]], dict[int, float]]:
    """Return the managed block table and the yield curve per track."""
    fragments = pd.read_parquet(dataset / "fragments.parquet")
    tracks = pd.read_parquet(dataset / "tracks.parquet")
    features = pd.read_parquet(dataset / "features.parquet")
    curves = pd.read_parquet(dataset / "curves.parquet")

    joined = fragments.merge(tracks, on="track_id", how="left")
    joined["managed"] = joined["name"].str.contains(r"status\(C\)", regex=True)
    joined["operable"] = joined["name"].str.contains(r"oper\(Operable\)", regex=True)
    managed = joined[joined["managed"]].copy()

    curve_by_track = (
        features.loc[features["label"] == "feature.yield.managed.total"]
        .set_index("track_id")["curve_id"]
        .to_dict()
    )
    curve_arrays = {
        int(curve_id): group.sort_values("x")[["x", "y"]].to_numpy()
        for curve_id, group in curves.groupby("curve_id")
    }

    blocks: dict[int, dict[str, object]] = {}
    for block_id, group in managed.groupby("block_id"):
        area = float(group["area_ha"].sum())
        age = float(np.average(group["age"], weights=group["area_ha"]))
        blocks[int(block_id)] = {
            "block_id": int(block_id),
            "area": area,
            "age": age,
            "operable": bool(group["operable"].all()),
            "fragments": group,
        }
    return blocks, {
        int(track_id): curve_arrays[int(curve_id)]
        for track_id, curve_id in curve_by_track.items()
        if int(curve_id) in curve_arrays
    }


def _volume(
    block: dict[str, object],
    year: int,
    curves: dict[int, np.ndarray],
) -> float:
    """Return the managed volume at a harvest year for one block."""
    total = 0.0
    for fragment in block["fragments"].itertuples():  # type: ignore[attr-defined]
        curve = curves.get(int(fragment.track_id))
        if curve is None:
            continue
        density = float(np.interp(float(fragment.age) + year, curve[:, 0], curve[:, 1]))
        total += float(fragment.area_ha) * density
    return total


def _read_adjacency(
    topology: Path, blocks: dict[int, dict[str, object]]
) -> dict[int, set[int]]:
    """Return touching-block adjacency from the proximal topology."""
    frame = pd.read_csv(topology)
    adjacency: dict[int, set[int]] = defaultdict(set)
    for row in frame.itertuples(index=False):
        left, right = int(row.BLOCK1), int(row.BLOCK2)
        if left < 0 or right < 0 or float(row.DISTANCE) > 0.0:
            continue
        if left in blocks and right in blocks:
            adjacency[left].add(right)
            adjacency[right].add(left)
    return adjacency


def _build_openings(
    blocks: dict[int, dict[str, object]],
    adjacency: dict[int, set[int]],
    *,
    min_area: float,
    max_area: float,
) -> list[dict[str, object]]:
    """Grow connected openings in the area band and return them."""
    for block in blocks.values():
        min_age = 60.0 if block["operable"] else 150.0
        block["ready"] = max(0, int(np.ceil(min_age - float(block["age"]))))

    eligible = [block for block in blocks.values() if float(block["area"]) <= max_area]
    eligible.sort(
        key=lambda block: (block["ready"], -float(block["age"]), -float(block["area"]))
    )
    assigned: set[int] = set()
    openings: list[dict[str, object]] = []
    for seed in eligible:
        block_id = int(seed["block_id"])
        if block_id in assigned:
            continue
        cluster = [block_id]
        total = float(seed["area"])
        assigned.add(block_id)
        frontier = deque(sorted(adjacency.get(block_id, ())))
        while total < min_area and frontier:
            neighbour = frontier.popleft()
            if neighbour in assigned:
                continue
            other = blocks[neighbour]
            if float(other["area"]) > max_area:
                continue
            if total + float(other["area"]) > max_area:
                continue
            cluster.append(neighbour)
            total += float(other["area"])
            assigned.add(neighbour)
            frontier.extend(
                item for item in adjacency.get(neighbour, ()) if item not in assigned
            )
        if total < min_area:
            for item in cluster:
                assigned.add(item)
            continue
        openings.append(
            {
                "blocks": tuple(cluster),
                "area": total,
                "ready": max(int(blocks[item]["ready"]) for item in cluster),
            }
        )
    return openings


def _assign_years(
    openings: list[dict[str, object]],
    blocks: dict[int, dict[str, object]],
    curves: dict[int, np.ndarray],
    *,
    years: int,
    target_per_decade: float,
) -> dict[int, float]:
    """Assign opening years, filling each decade toward the target volume."""
    decades = {decade: 0.0 for decade in range(0, years, 10)}
    offsets = {decade: 0 for decade in decades}
    for opening in sorted(
        openings, key=lambda item: (item["ready"], -float(item["area"]))
    ):
        candidates = [decade for decade in decades if decade >= opening["ready"]]
        if not candidates:
            candidates = list(decades)
        choice: tuple[int, int, float] | None = None
        for decade in sorted(candidates):
            year = max(int(opening["ready"]), decade + (offsets[decade] % 10))
            volume = sum(
                _volume(blocks[item], year, curves) for item in opening["blocks"]
            )
            if decades[decade] + volume <= target_per_decade:
                choice = (decade, year, volume)
                break
        if choice is None:
            decade = min(candidates, key=lambda item: decades[item])
            year = max(int(opening["ready"]), decade + (offsets[decade] % 10))
            volume = sum(
                _volume(blocks[item], year, curves) for item in opening["blocks"]
            )
            choice = (decade, year, volume)
        decade, year, volume = choice
        offsets[decade] += 1
        opening["decade"] = decade
        opening["year"] = year
        opening["volume"] = volume
        decades[decade] += volume
    return decades


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--topology", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--years", type=int, default=100)
    parser.add_argument("--min-area", type=float, default=5.0)
    parser.add_argument("--max-area", type=float, default=40.0)
    parser.add_argument("--target-per-decade", type=float, default=300_000.0)
    args = parser.parse_args()

    blocks, curves = _load_blocks(args.dataset)
    adjacency = _read_adjacency(args.topology, blocks)
    openings = _build_openings(
        blocks, adjacency, min_area=args.min_area, max_area=args.max_area
    )
    decades = _assign_years(
        openings,
        blocks,
        curves,
        years=args.years,
        target_per_decade=args.target_per_decade,
    )

    rows = [
        {"block_id": block_id, "treatment": "CC", "period": int(opening["year"])}
        for opening in openings
        for block_id in opening["blocks"]
    ]
    schedule = pd.DataFrame(rows).sort_values(["period", "block_id"], kind="stable")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    schedule.to_csv(args.out, index=False)

    areas = sorted(float(opening["area"]) for opening in openings)
    print(
        f"blocks={len(blocks)} openings={len(openings)} "
        f"scheduled_blocks={len(schedule)} "
        f"area={sum(areas):.1f} ha "
        f"area_range={areas[0]:.1f}-{areas[-1]:.1f} ha"
    )
    print(
        "decade volumes:", {decade: round(value) for decade, value in decades.items()}
    )


if __name__ == "__main__":
    main()
