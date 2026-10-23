"""The patch-first builder emits the ws4 offset clock, never the legacy period clock."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd

_SCRIPT = Path(__file__).resolve().parents[1] / "ws4" / "build_patch_schedule.py"
_OPTIMIZE_SCRIPT = Path(__file__).resolve().parents[1] / "ws4" / "run_optimize.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("mkrf_build_patch_schedule", _SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_optimize_module():
    spec = importlib.util.spec_from_file_location("mkrf_run_optimize", _OPTIMIZE_SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_dataset(root: Path) -> Path:
    """Write the smallest matrix the builder reads, with two touching 6 ha blocks."""
    dataset = root / "matrix"
    dataset.mkdir()
    pd.DataFrame(
        [
            {"block_id": 1, "track_id": 1, "area_ha": 2.5, "age": 70.0},
            {"block_id": 2, "track_id": 1, "area_ha": 2.5, "age": 70.0},
            {"block_id": 3, "track_id": 1, "area_ha": 6.0, "age": 50.0},
        ]
    ).to_parquet(dataset / "fragments.parquet", index=False)
    pd.DataFrame([{"track_id": 1, "name": "status(C) oper(Operable)"}]).to_parquet(
        dataset / "tracks.parquet", index=False
    )
    pd.DataFrame(
        [
            {
                "track_id": 1,
                "label": "feature.yield.managed.total",
                "curve_id": 1,
            }
        ]
    ).to_parquet(dataset / "features.parquet", index=False)
    pd.DataFrame(
        [
            {"curve_id": 1, "x": 0.0, "y": 100.0},
            {"curve_id": 1, "x": 200.0, "y": 100.0},
        ]
    ).to_parquet(dataset / "curves.parquet", index=False)
    return dataset


def _topology(root: Path) -> Path:
    path = root / "topology.csv"
    pd.DataFrame(
        [
            {"BLOCK1": 1, "BLOCK2": 2, "DISTANCE": 0.0},
        ]
    ).to_csv(path, index=False)
    return path


def test_patch_first_assigns_offsets_and_never_emits_a_period_column(
    tmp_path: Path,
) -> None:
    """The builder uses offset 0 for the first simulation year and the offset schedule schema."""
    module = _load_module()
    dataset = _write_dataset(tmp_path)
    blocks, _ = module._load_blocks(dataset)
    adjacency = module._read_adjacency(_topology(tmp_path), blocks)
    openings = module._build_openings(blocks, adjacency, min_area=5.0, max_area=50.0)
    assert len(openings) == 2

    module._assign_offsets(
        openings,
        blocks,
        {},
        years=20,
        target_per_decade=1_000_000.0,
    )
    scheduled = [opening for opening in openings if "offset" in opening]
    frame = module.schedule_frame(scheduled)

    assert len(frame) == 3
    assert 0 in set(frame["offset"])
    assert list(frame.columns) == ["block_id", "treatment", "offset"]
    assert set(frame["treatment"]) == {"CC"}
    assert frame["offset"].min() >= 0
    assert "period" not in frame.columns
    assert set(frame["block_id"]) <= {1, 2, 3}


def test_patch_first_puts_a_later_ready_opening_in_the_next_offset_decade(
    tmp_path: Path,
) -> None:
    """A block that needs 15 years is not scheduled in the offset 0-9 period."""
    module = _load_module()
    dataset = _write_dataset(tmp_path)
    blocks, _ = module._load_blocks(dataset)
    finding = {
        "blocks": (3,),
        "area": 6.0,
        "ready": 10,
    }
    module._assign_offsets(
        [finding],
        blocks,
        {},
        years=20,
        target_per_decade=1_000_000.0,
    )
    assert finding["target_period"] == 2
    assert finding["offset"] == 10
    assert finding["offset"] >= 10


def test_an_empty_schedule_still_has_the_offset_header(tmp_path: Path) -> None:
    """A run with no opening still writes a valid empty offset schedule."""
    module = _load_module()
    frame = module.schedule_frame([])
    assert list(frame.columns) == ["block_id", "treatment", "offset"]
    assert frame.empty


def test_the_optimizer_loader_reads_offsets_and_rejects_period(tmp_path: Path) -> None:
    """The harness passes offsets to the optimizer; a legacy period file is refused."""
    module = _load_optimize_module()
    schedule = tmp_path / "schedule.csv"
    pd.DataFrame(
        [
            {"block_id": 1, "treatment": "CC", "offset": 0},
            {"block_id": 1, "treatment": "CT", "offset": 10},
        ]
    ).to_csv(schedule, index=False)
    assert module.load_schedule_csv(schedule) == {1: (("CC", 0), ("CT", 10))}

    legacy = tmp_path / "legacy.csv"
    pd.DataFrame([{"block_id": 1, "treatment": "CC", "period": 1}]).to_csv(
        legacy, index=False
    )
    try:
        module.load_schedule_csv(legacy)
    except ValueError as error:
        assert "offset" in str(error)
    else:  # pragma: no cover - the contract says this must fail
        raise AssertionError("a period-only schedule must be refused")
