"""The small-polygon analysis keeps only attribute-safe merges."""

from __future__ import annotations

import geopandas as gpd
from shapely.geometry import box
from small_polygons import (
    area_hectares,
    attribute_safe,
    histogram,
    merge_safe,
    neighbours,
    summarize,
)


def _frame() -> gpd.GeoDataFrame:
    """Return a large polygon, two touching smalls, and one isolated small."""
    return gpd.GeoDataFrame(
        {
            "RES_KEY": [1, 2, 3, 4],
            "Operabilit": ["Operable", "Operable", "Riparian", "Operable"],
            "CONTCLAS": ["C", "C", "N", "C"],
            "CT_eligib": ["Y", "Y", "N", "Y"],
            "AU_EX": ["10", "10", "20", "30"],
            "AU_FU": ["100", "100", "200", "300"],
        },
        geometry=[
            box(0, 0, 100, 200),
            box(100, 0, 120, 20),
            box(100, 20, 120, 40),
            box(1000, 1000, 1020, 1020),
        ],
        crs="EPSG:3005",
    )


def test_area_and_histogram_use_hectares() -> None:
    """The large fixture is two hectares and the small ones are 0.04 ha."""
    frame = _frame()
    areas = area_hectares(frame)
    assert areas.tolist() == [2.0, 0.04, 0.04, 0.04]
    bins = histogram(areas)
    assert bins[0]["polygons"] == 3


def test_only_same_attribute_neighbour_is_safe() -> None:
    """The opposite-operability small is a touching candidate but not a safe merge."""
    frame = _frame()
    frame["area_ha"] = area_hectares(frame)
    candidates = neighbours(frame, threshold=1.0, target_min_ha=1.0)
    assert set(candidates[candidates["source_index"].isin([1, 2])]["kind"]) == {
        "touching"
    }
    safe = attribute_safe(frame, candidates)
    assert safe["source_key"].tolist() == [2]
    assert safe["target_key"].tolist() == [1]


def test_merge_preserves_area_and_target_key() -> None:
    """The safe merge drops the small feature and keeps the target geometry area."""
    frame = _frame()
    frame["area_ha"] = area_hectares(frame)
    safe = attribute_safe(frame, neighbours(frame, threshold=1.0, target_min_ha=1.0))
    merged, log = merge_safe(frame, safe)
    assert len(log) == 1
    assert len(merged) == 3
    assert 2 not in merged["RES_KEY"].tolist()
    assert merged["area_ha"].sum() == frame["area_ha"].sum()
    assert merged.loc[merged["RES_KEY"] == 1, "area_ha"].iloc[0] > 2.0


def test_summary_reports_small_and_unique_au_counts() -> None:
    """The summary keeps the small-polygon and unique-AU evidence."""
    summary = summarize(_frame(), threshold=1.0)
    assert summary["small_polygons"] == 3
    assert summary["merge_pairs"] == 1
    assert summary["unique_au_polygons"] == 2
    assert summary["small_area_fraction"] > 0
