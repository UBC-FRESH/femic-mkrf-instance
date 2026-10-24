#!/usr/bin/env python
"""Analyze and optionally merge sub-hectare stand polygons.

The analysis answers the MKRF sliver question: how many sub-hectare polygons
exist, how much area they cover, where the size histogram has cutoffs, and whether
an attribute-safe merge would lose operability, CT, contributing-class, or AU
information.

The optional merge is deliberately conservative. A small polygon is merged only
into a touching, at-least-threshold neighbour whose ``Operabilit``, ``CONTCLAS``,
``CT_eligib``, ``AU_EX`` and ``AU_FU`` values all match. The default is analysis
only; pass ``--merge-out`` to write a merged copy of the inventory.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.ops import unary_union

ATTRIBUTE_FIELDS = ("Operabilit", "CONTCLAS", "CT_eligib", "AU_EX", "AU_FU")
AREA_CRS = "EPSG:3005"


def area_hectares(frame: gpd.GeoDataFrame, crs: str = AREA_CRS) -> pd.Series:
    """Return polygon areas in hectares.

    Parameters
    ----------
    frame : geopandas.GeoDataFrame
        The inventory.
    crs : str
        Projected CRS used for the area calculation.

    Returns
    -------
    pandas.Series
        Area per row, in hectares.
    """
    projected = (
        frame.to_crs(crs) if frame.crs is not None and str(frame.crs) != crs else frame
    )
    return projected.geometry.area / 10_000.0


def histogram(
    areas: pd.Series, *, upper: float = 1.0, step: float = 0.05
) -> list[dict[str, float]]:
    """Return polygon counts and area by size bin.

    Parameters
    ----------
    areas : pandas.Series
        Polygon areas in hectares.
    upper : float
        Last bin edge.
    step : float
        Bin width.

    Returns
    -------
    list of dict
        ``lower``, ``upper``, ``polygons`` and ``area_ha`` per bin.
    """
    edges = np.arange(0.0, upper + step / 2.0, step)
    counts, _ = np.histogram(areas.clip(lower=0.0, upper=upper), bins=edges)
    rows: list[dict[str, float]] = []
    for index, count in enumerate(counts):
        lower = float(edges[index])
        top = float(edges[index + 1])
        selected = areas[(areas >= lower) & (areas < top)]
        rows.append(
            {
                "lower": round(lower, 4),
                "upper": round(top, 4),
                "polygons": int(count),
                "area_ha": round(float(selected.sum()), 4),
            }
        )
    return rows


def cumulative(
    areas: pd.Series, thresholds: tuple[float, ...]
) -> list[dict[str, float]]:
    """Return counts and area at or below each threshold."""
    total_area = float(areas.sum())
    return [
        {
            "threshold_ha": threshold,
            "polygons": int((areas <= threshold).sum()),
            "area_ha": round(float(areas[areas <= threshold].sum()), 4),
            "area_fraction": round(
                float(areas[areas <= threshold].sum()) / total_area, 6
            )
            if total_area
            else 0.0,
        }
        for threshold in thresholds
    ]


def neighbours(
    frame: gpd.GeoDataFrame,
    *,
    threshold: float,
    target_min_ha: float,
) -> pd.DataFrame:
    """Return each small polygon's largest touching at-least-threshold neighbour.

    Parameters
    ----------
    frame : geopandas.GeoDataFrame
        Inventory with an ``area_ha`` column.
    threshold : float
        Small-polygon cutoff, in hectares.
    target_min_ha : float
        Minimum area of a merge target.

    Returns
    -------
    pandas.DataFrame
        One row per small polygon with source/target indices, target key,
        distance kind and candidate count.
    """
    index = frame.sindex
    rows: list[dict[str, Any]] = []
    for source_index, row in frame[frame["area_ha"] < threshold].iterrows():
        touching: list[tuple[int, float]] = []
        near: list[tuple[int, float]] = []
        for candidate in index.query(row.geometry.buffer(1.0), predicate="intersects"):
            target_index = int(candidate)
            if target_index == int(source_index):
                continue
            target = frame.geometry.iloc[target_index]
            distance = float(row.geometry.distance(target))
            shared = (
                float(row.geometry.intersection(target).length)
                if distance <= 1e-6
                else 0.0
            )
            if shared > 0.0:
                touching.append((target_index, shared))
            elif (
                distance <= 10.0
                and float(frame["area_ha"].iloc[target_index]) >= target_min_ha
            ):
                near.append((target_index, distance))
        chosen: int | None = None
        kind = "none"
        nearest = float("nan")
        if touching:
            candidates = [
                target_index
                for target_index, _ in touching
                if float(frame["area_ha"].iloc[target_index]) >= target_min_ha
            ]
            if candidates:
                chosen = max(
                    candidates,
                    key=lambda target_index: frame["area_ha"].iloc[target_index],
                )
                kind = "touching"
        elif near:
            chosen = min(near, key=lambda item: item[1])[0]
            kind = "within10m"
            nearest = min(distance for _, distance in near)
        rows.append(
            {
                "source_index": int(source_index),
                "target_index": chosen,
                "target_key": int(frame["RES_KEY"].iloc[chosen])
                if chosen is not None
                else None,
                "nearest_m": nearest,
                "kind": kind,
                "candidate_count": len(touching) + len(near),
            }
        )
    return pd.DataFrame(rows)


def attribute_safe(frame: gpd.GeoDataFrame, candidates: pd.DataFrame) -> pd.DataFrame:
    """Return candidate pairs whose five inventory attributes all match.

    Parameters
    ----------
    frame : geopandas.GeoDataFrame
        Inventory with ``RES_KEY`` and the attribute fields.
    candidates : pandas.DataFrame
        Output of :func:`neighbours`.

    Returns
    -------
    pandas.DataFrame
        The safe subset, with the source area in hectares.
    """
    rows: list[dict[str, Any]] = []
    for row in candidates.itertuples(index=False):
        if row.target_index is None or not np.isfinite(row.target_index):
            continue
        source = frame.iloc[int(row.source_index)]
        target = frame.iloc[int(row.target_index)]
        if all(str(source[field]) == str(target[field]) for field in ATTRIBUTE_FIELDS):
            rows.append(
                {
                    "source_index": int(row.source_index),
                    "target_index": int(row.target_index),
                    "source_key": int(source["RES_KEY"]),
                    "target_key": int(target["RES_KEY"]),
                    "area_ha": float(frame["area_ha"].iloc[int(row.source_index)]),
                }
            )
    return pd.DataFrame(rows)


def merge_safe(
    frame: gpd.GeoDataFrame, safe: pd.DataFrame
) -> tuple[gpd.GeoDataFrame, pd.DataFrame]:
    """Merge safe small polygons into their target polygons.

    Parameters
    ----------
    frame : geopandas.GeoDataFrame
        Inventory with an ``area_ha`` column.
    safe : pandas.DataFrame
        Output of :func:`attribute_safe`.

    Returns
    -------
    tuple
        The merged frame and the merge log. The frame preserves the target
        feature's attributes and RES_KEY, and updates Shape_Area/Shape_Leng when
        those fields exist.
    """
    if safe.empty:
        return frame.copy(), safe.copy()
    grouped: dict[int, list[int]] = defaultdict(list)
    log_rows: list[dict[str, Any]] = []
    for row in safe.itertuples(index=False):
        grouped[int(row.target_index)].append(int(row.source_index))
        log_rows.append(
            {
                "source_key": int(row.source_key),
                "target_key": int(row.target_key),
                "area_ha": float(row.area_ha),
            }
        )
    merged = frame.copy()
    drop: set[int] = set()
    for target_index, source_indices in grouped.items():
        target = merged.geometry.iloc[target_index]
        merged_geometry = unary_union(
            [target, *[merged.geometry.iloc[i] for i in source_indices]]
        )
        merged.at[merged.index[target_index], "geometry"] = merged_geometry
        drop.update(source_indices)
    merged = merged.drop(index=merged.index[list(drop)]).copy()
    projected = merged.to_crs(AREA_CRS)
    if "Shape_Area" in merged.columns:
        merged["Shape_Area"] = projected.geometry.area.to_numpy()
    if "Shape_Leng" in merged.columns:
        merged["Shape_Leng"] = projected.geometry.length.to_numpy()
    merged["area_ha"] = area_hectares(merged)
    return merged.reset_index(drop=True), pd.DataFrame(log_rows)


def summarize(
    frame: gpd.GeoDataFrame,
    *,
    threshold: float,
) -> dict[str, Any]:
    """Return the analysis payload for one inventory."""
    work = frame.copy()
    work["area_ha"] = area_hectares(work)
    small = work[work["area_ha"] < threshold]
    candidates = neighbours(work, threshold=threshold, target_min_ha=threshold)
    safe = attribute_safe(work, candidates)
    safe_groups = candidates[candidates["kind"] == "touching"]
    summary = {
        "polygons": len(work),
        "area_ha": round(float(work["area_ha"].sum()), 4),
        "threshold_ha": threshold,
        "small_polygons": len(small),
        "small_area_ha": round(float(small["area_ha"].sum()), 4),
        "small_count_fraction": round(len(small) / len(work), 6) if len(work) else 0.0,
        "small_area_fraction": round(
            float(small["area_ha"].sum()) / float(work["area_ha"].sum()), 6
        )
        if len(work)
        else 0.0,
        "min_small_ha": round(float(small["area_ha"].min()), 4) if len(small) else 0.0,
        "median_small_ha": round(float(small["area_ha"].median()), 4)
        if len(small)
        else 0.0,
        "histogram": histogram(small["area_ha"]),
        "cumulative": cumulative(
            work["area_ha"], (0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.75, 0.9, 1.0)
        ),
        "neighbour_kinds": candidates["kind"].value_counts().to_dict(),
        "touch_candidates": len(safe_groups),
        "attribute_safe_pairs": len(safe),
        "attribute_safe_area_ha": round(float(safe["area_ha"].sum()), 4),
        "merge_pairs": len(safe),
        "merge_area_ha": round(float(safe["area_ha"].sum()), 4),
        "attribute_fields": list(ATTRIBUTE_FIELDS),
    }
    for field in ("Operabilit", "CONTCLAS", "CT_eligib"):
        if field in small:
            summary[f"small_{field.lower()}"] = (
                small.groupby(field)["area_ha"].sum().round(4).to_dict()
            )
    large_keys = set(
        map(
            tuple,
            work.loc[work["area_ha"] >= threshold, ["AU_EX", "AU_FU"]]
            .astype(str)
            .values,
        )
    )
    if len(small):
        unique = small[
            ~small[["AU_EX", "AU_FU"]].astype(str).apply(tuple, axis=1).isin(large_keys)
        ]
        summary["unique_au_polygons"] = len(unique)
        summary["unique_au_area_ha"] = round(float(unique["area_ha"].sum()), 4)
    return summary


def main() -> None:
    """Run the analysis and optionally write the merged inventory."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fragments", type=Path, required=True)
    parser.add_argument("--threshold", type=float, default=1.0)
    parser.add_argument("--summary-out", type=Path)
    parser.add_argument(
        "--small-out", type=Path, help="CSV of small polygons and neighbours"
    )
    parser.add_argument(
        "--merge-out", type=Path, help="Write the attribute-safe merged inventory"
    )
    parser.add_argument("--merge-log", type=Path)
    args = parser.parse_args()
    frame = gpd.read_file(args.fragments)
    payload = summarize(frame, threshold=args.threshold)
    work = frame.copy()
    work["area_ha"] = area_hectares(work)
    candidates = neighbours(
        work, threshold=args.threshold, target_min_ha=args.threshold
    )
    safe = attribute_safe(work, candidates)
    payload["merge_pairs"] = len(safe)
    payload["merge_area_ha"] = round(float(safe["area_ha"].sum()), 4)
    print(json.dumps(payload, indent=2, sort_keys=True))
    if args.summary_out:
        args.summary_out.parent.mkdir(parents=True, exist_ok=True)
        args.summary_out.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n"
        )
    if args.small_out:
        small = work[work["area_ha"] < args.threshold].copy()
        detail = small.merge(
            candidates,
            left_index=True,
            right_on="source_index",
            how="left",
        )
        detail.to_csv(args.small_out, index=False)
    if args.merge_out:
        merged, log = merge_safe(work, safe)
        args.merge_out.parent.mkdir(parents=True, exist_ok=True)
        driver = (
            "GPKG" if args.merge_out.suffix.lower() == ".gpkg" else "ESRI Shapefile"
        )
        merged.drop(columns=["area_ha"]).to_file(args.merge_out, driver=driver)
        if args.merge_log:
            args.merge_log.parent.mkdir(parents=True, exist_ok=True)
            log.to_csv(args.merge_log, index=False)


if __name__ == "__main__":
    main()
