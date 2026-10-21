#!/usr/bin/env python3
"""Run the MKRF ws4 pilot from the translated Patchworks control inputs.

The script compiles the MKRF ForestModelXML + fragments into the ws4 matrix,
replays the green-up-aware schedule, and writes a compact evidence summary.

Run from anywhere:

    python ws4/run_pilot.py

Requires the ws4 package (``python -m ws4.cli --help``) and its geo extras.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

INSTANCE_ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = INSTANCE_ROOT / "models" / "mkrf_patchworks_model"
WS4_ROOT = INSTANCE_ROOT / "ws4"
DEFAULT_DATASET = WS4_ROOT / "runtime" / "matrix"
DEFAULT_RUN = WS4_ROOT / "runtime" / "patch_first"


def _require_ws4() -> None:
    try:
        import ws4  # noqa: F401
    except ImportError as exc:  # pragma: no cover - environment guard
        raise SystemExit(
            "ws4 is not importable. Install it with "
            "`pip install -e /path/to/ws4` or run from the ws4 checkout."
        ) from exc


def build_dataset(dataset_dir: Path) -> Path:
    """Compile the MKRF recipe and fragments into a ws4 canonical dataset."""
    from ws4.build.compiler import build_canonical_dataset

    if (dataset_dir / "manifest.json").is_file():
        return dataset_dir
    dataset_dir.parent.mkdir(parents=True, exist_ok=True)
    return build_canonical_dataset(
        xml_path=MODEL_ROOT / "xml" / "forestmodel.xml",
        fragments_path=MODEL_ROOT / "spatial" / "fragments.shp",
        out_dir=dataset_dir,
    )


def run_simulation(
    *,
    dataset_dir: Path,
    schedule_path: Path,
    run_dir: Path,
    years: int,
) -> Path:
    """Replay the schedule with the translated patch accounts and green-up rule."""
    from ws4.patch.accounts import load_patch_accounts
    from ws4.sim.engine import Simulator

    run_dir.mkdir(parents=True, exist_ok=True)
    simulator = Simulator.from_dataset(dataset_dir)
    simulator.run(
        schedule_csv=schedule_path,
        years=years,
        out_dir=run_dir,
        topology_csv=WS4_ROOT / "topology.csv",
        patch_accounts=load_patch_accounts(WS4_ROOT / "patch_accounts.yaml"),
        patch_membership=True,
    )
    return run_dir


def write_ui_assets(run_dir: Path) -> None:
    """Write the geometry and report files the ws4 web UI reads."""
    import geopandas as gpd
    import pandas as pd
    from ws4.opt.objective import load_targets
    from ws4.report import write_report

    runtime_dir = run_dir.parent
    geometry_path = runtime_dir / "fragments.geojson"
    fragments = gpd.read_file(MODEL_ROOT / "spatial" / "fragments.shp")
    fragments["block_id"] = fragments["RES_KEY"].astype(int)
    fragments[["block_id", "geometry"]].to_file(geometry_path, driver="GeoJSON")

    values = pd.read_csv(run_dir / "account_values.csv")
    write_report(values, load_targets(WS4_ROOT / "targets.yaml"), run_dir)


def summarise(run_dir: Path) -> dict[str, object]:
    """Return the pilot's headline evidence from a completed simulation."""
    import pandas as pd

    products = pd.read_csv(run_dir / "product_values.csv")
    accounts = pd.read_csv(run_dir / "account_values.csv")
    patches = pd.read_csv(run_dir / "patch_accounts.csv")

    harvest = products.loc[
        products["account"] == "product.yield.managed.total", ["year", "value"]
    ].copy()
    harvest["decade"] = (harvest["year"] // 10) * 10
    harvest_by_decade = (
        harvest.groupby("decade", sort=True)["value"].sum().round(2).to_dict()
    )

    growing_stock = accounts.loc[
        accounts["account"] == "feature.yield.managed.total", ["year", "value"]
    ]
    decade_rows = growing_stock[growing_stock["year"].isin(range(0, 101, 10))]
    growing_stock_by_decade = {
        int(row.year): round(float(row.value), 2)
        for row in decade_rows.itertuples(index=False)
    }

    size_columns = [
        column
        for column in patches.columns
        if column.startswith("patch.grpblk.") and column.endswith(".size")
    ]
    patch_frame = patches.loc[
        patches["year"].isin(range(0, 101, 10)),
        ["year", *size_columns, "patch.grpblk.TOTAL.frequency"],
    ].copy()
    grpblk_by_decade = {
        int(row["year"]): {
            **{
                column.removeprefix("patch.grpblk.").removesuffix(".size")
                + "_pct": round(float(row[column]), 3)
                for column in size_columns
            },
            "patch_count": float(row["patch.grpblk.TOTAL.frequency"]),
        }
        for row in patch_frame.to_dict("records")
    }

    violations_path = run_dir / "spatial_violations.csv"
    violations = (
        pd.read_csv(violations_path) if violations_path.is_file() else pd.DataFrame()
    )
    qmd_accounts = sorted(
        account
        for account in accounts["account"].dropna().unique()
        if str(account).startswith("product.QMDNumerator.managed.")
    )

    summary: dict[str, object] = {
        "harvest_by_decade_m3": harvest_by_decade,
        "growing_stock_by_decade_m3": growing_stock_by_decade,
        "grpblk_by_decade": grpblk_by_decade,
        "spatial_violation_count": len(violations),
        "spatial_violation_kinds": (
            violations.groupby("kind").size().to_dict() if len(violations) else {}
        ),
        "qmd_numerator_account_count": len(qmd_accounts),
        "qmd_numerator_accounts_sample": qmd_accounts[:5],
    }
    (run_dir / "pilot_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--run", type=Path, default=DEFAULT_RUN)
    parser.add_argument(
        "--schedule",
        type=Path,
        default=WS4_ROOT / "schedules" / "patch_first.csv",
    )
    parser.add_argument("--years", type=int, default=100)
    parser.add_argument("--skip-build", action="store_true")
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Recompile the ws4 matrix even when a cached manifest exists.",
    )
    args = parser.parse_args()

    _require_ws4()
    if args.rebuild:
        import shutil

        shutil.rmtree(args.dataset, ignore_errors=True)
    dataset = args.dataset if args.skip_build else build_dataset(args.dataset)
    run_dir = run_simulation(
        dataset_dir=dataset,
        schedule_path=args.schedule,
        run_dir=args.run,
        years=args.years,
    )
    write_ui_assets(run_dir)
    summary = summarise(run_dir)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
