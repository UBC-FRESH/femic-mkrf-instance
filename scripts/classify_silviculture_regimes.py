#!/usr/bin/env python3
"""Classify MKRF fragments into Anna Tobiasz's silviculture regimes.

The classifier joins each fragment to its stand site index, applies the
site-index/operability group rules, and writes a fragment-level assignment table
for the next model rebuild.

This is an input-classification step.  It does not yet create the repeated-entry
selection treatment family or a hard over-130-year harvest exclusion.
"""

from __future__ import annotations

import json
from pathlib import Path

import geopandas as gpd
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
FRAGMENTS = ROOT / "models" / "mkrf_patchworks_model" / "spatial" / "fragments.shp"
STAND_SI = ROOT / "data" / "model_input_bundle" / "stand_origin_assignment.csv"
CONFIG = ROOT / "config" / "silviculture_regimes.mkrf.yaml"
OUT = ROOT / "data" / "model_input_bundle"

GROUP_TARGETS = {
    "si_lt20": 212.57,
    "si_20_24": 1020.20,
    "si_25_29": 1265.50,
    "si_30_34": 618.96,
    "si_ge35": 449.98,
    "low_operability_vr20": 553.40,
}


def regime_for(operability: str, site_index: float) -> str:
    if operability == "Low Operability":
        return "low_operability_vr20"
    if operability != "Operable":
        return f"excluded_{operability.lower().replace(' ', '_')}"
    if site_index < 20.0:
        return "si_lt20"
    if site_index < 25.0:
        return "si_20_24"
    if site_index < 30.0:
        return "si_25_29"
    if site_index < 35.0:
        return "si_30_34"
    return "si_ge35"


def main() -> None:
    config = yaml.safe_load(CONFIG.read_text())
    groups = config["groups"]

    fragments = gpd.read_file(FRAGMENTS, engine="pyogrio")
    fragments["area_ha"] = fragments.geometry.area / 10_000.0
    si = pd.read_csv(STAND_SI)
    si = si[["forest_cover_id", "site_index"]].drop_duplicates("forest_cover_id")
    frame = fragments.merge(
        si,
        left_on="FOREST_COV",
        right_on="forest_cover_id",
        how="left",
    )
    if frame["site_index"].isna().any():
        raise ValueError("fragments with missing site index")

    frame["silv_group"] = [
        regime_for(str(operability), float(site_index))
        for operability, site_index in zip(
            frame["Operabilit"], frame["site_index"], strict=True
        )
    ]
    frame["ct_allowed"] = [
        bool(groups.get(group, {}).get("ct_eligible", False)) and str(ct).upper() == "Y"
        for group, ct in zip(frame["silv_group"], frame["CT_eligib"], strict=True)
    ]
    frame["retention_pct"] = frame["silv_group"].map(
        lambda group: groups.get(group, {}).get("retention_pct")
    )
    frame["over_130"] = frame["AGE_2020"] > 130
    frame["planting_mix"] = frame["silv_group"].map(
        lambda group: json.dumps(
            groups.get(group, {}).get("planting", {}), sort_keys=True
        )
    )

    columns = [
        "RES_KEY",
        "FOREST_COV",
        "AU_EX",
        "AU_FU",
        "Operabilit",
        "CT_eligib",
        "AGE_2020",
        "site_index",
        "silv_group",
        "ct_allowed",
        "retention_pct",
        "over_130",
        "planting_mix",
        "area_ha",
        "geometry",
    ]
    frame[columns].to_file(
        OUT / "silviculture_regime_assignment.gpkg",
        layer="silviculture_regime_assignment",
        driver="GPKG",
    )
    frame[columns[:-1]].to_csv(OUT / "silviculture_regime_assignment.csv", index=False)

    summary_rows: list[dict] = []
    for group, target in GROUP_TARGETS.items():
        actual = float(frame.loc[frame["silv_group"] == group, "area_ha"].sum())
        summary_rows.append(
            {
                "silv_group": group,
                "target_area_ha": target,
                "actual_area_ha": round(actual, 3),
                "difference_ha": round(actual - target, 3),
            }
        )
    summary = pd.DataFrame(summary_rows)
    summary.to_csv(OUT / "silviculture_regime_summary.csv", index=False)

    over_130 = frame[frame["over_130"]]
    payload = {
        "schema_version": "mkrf.silviculture.regimes.v1",
        "fragments": len(frame),
        "total_area_ha": round(float(frame["area_ha"].sum()), 3),
        "group_summary": summary.to_dict(orient="records"),
        "over_130": {
            "area_ha": round(float(over_130["area_ha"].sum()), 3),
            "operable_ha": round(
                float(
                    over_130.loc[over_130["Operabilit"] == "Operable", "area_ha"].sum()
                ),
                3,
            ),
            "low_operability_ha": round(
                float(
                    over_130.loc[
                        over_130["Operabilit"] == "Low Operability", "area_ha"
                    ].sum()
                ),
                3,
            ),
            "fragments": len(over_130),
        },
        "ct_allowed_area_ha": round(
            float(frame.loc[frame["ct_allowed"], "area_ha"].sum()), 3
        ),
        "retention_area_ha": {
            str(pct): round(float(group["area_ha"].sum()), 3)
            for pct, group in frame.dropna(subset=["retention_pct"]).groupby(
                "retention_pct"
            )
        },
        "caveats": [
            "CT eligibility is the group rule intersected with the current CT_eligib proxy.",
            "Cable-ground terrain is not yet a separate layer; CT_eligib=N is the proxy.",
            "Selection (group) for SI 25-29 is classified but not yet a WS4 treatment family.",
            "Over-130-year exclusion is a flag, not yet a hard model constraint.",
        ],
    }
    (OUT / "silviculture_regime_summary.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(payload, indent=2), flush=True)


if __name__ == "__main__":
    main()
