# MKRF ws4 pilot

This directory is the ws4-native replacement for the MKRF Patchworks control
surface. The model recipe stays `models/mkrf_patchworks_model/xml/forestmodel.xml`
and the inventory stays
`models/mkrf_patchworks_model/spatial/fragments.shp`; everything below translates
the old `.pin` / `.bsh` behaviour to ws4 inputs.

The current MKRF staff policy is recorded in
`planning/2026-10-21_basecamp_mkrf_decisions.md`: opening size is controlled by
size-class targets and weights, not by a 100 m adjacency rule. The public/private
data boundary is in `planning/data_publication_boundary.md`.

## Quick start

```bash
cd /path/to/femic-mkrf-instance
python ws4/run_pilot.py --rebuild
python ws4/build_patch_schedule.py \
  --dataset ws4/runtime/matrix \
  --topology ws4/topology.csv \
  --out ws4/schedules/patch_first.csv
python ws4/run_pilot.py --skip-build \
  --schedule ws4/schedules/patch_first.csv \
  --run ws4/runtime/patch_first
python ws4/run_optimize.py --iterations 200
```

`run_pilot.py` compiles the recipe and fragments into `ws4/runtime/matrix/`.
`build_patch_schedule.py` grows connected 5-40 ha openings, assigns harvest
years to fill decades toward 300,000 m3, and writes
`ws4/schedules/patch_first.csv`. `run_pilot.py` replays it with the translated
patch accounts into `ws4/runtime/patch_first/`. `run_optimize.py` starts the ws4
search from that schedule and writes `ws4/runtime/patch_first_search/`.

Requires an importable `ws4` (`pip install -e /path/to/ws4`). The pilot was run
against the ws4 checkout at `/srv/shared-data/gep/ws4/ws4`.

## Web UI

```bash
ws4/serve_pilot.sh
```

Open <http://127.0.0.1:8011/>. The service lists the current-policy baseline and
search, the older baseline, and the legacy green-up comparison. `PORT=...`
overrides the port. The default bind is loopback only; ws4 provides no
authentication, so do not expose it with `--allow-remote` unless you put it
behind a trusted proxy.

## Opening-size policy

| Size class | Target share | Weight |
| --- | --- | --- |
| `<= 1 ha` | 0% | Very High |
| `> 1 and <= 5 ha` | 10% | High |
| `> 5 and <= 40 ha` | no target | None |
| `> 40 and <= 50 ha` | 5% | High |
| `> 50 ha` | 0% | High |

The pilot treats the shares as maxima and maps Very High = 1,000,000 and High =
100,000. `patch_accounts.yaml` defines one account, `patch.grpblk`, on
`product.area.managed.treat.CC`, with `search_distance: 0.0` (touching blocks
only). The 100 m `patch.sepblk` green-up account remains only in the legacy
Patchworks reference surface.

## Translation map

| Patchworks file / construct | ws4 equivalent |
| --- | --- |
| `analysis/base.pin` `periods = 30`, `Horizon.setHorizon(periods, 10)` | dataset horizon; target `period_width: 10` |
| `base.pin` `block_shape`, `block_key = "RES_KEY"` | `--fragments` shapefile; compiler block key |
| `base.pin` `control.inputTopology(..., 20d)` | `ws4/topology.csv`; `patch.grpblk.search_distance` |
| `base.pin` `control.addPatchTarget("product.area.managed.treat.CC", "patch.grpblk...")` | `patch_accounts.yaml` `patch.grpblk` |
| `base.pin` `control.addPatchTarget("feature.area.managed.seral.le5", "patch.sepblk...")` | legacy/reference only; not the active ws4 policy |
| `Targets/01_harvest.bsh` minimum periodic harvest | `targets.yaml` `product.yield.managed.total` minimum entries |
| `Targets/07_flow.bsh` `feature.flow.yield.total` | `targets.yaml` `feature.yield.managed.total` `flow: ndy` |
| `Targets/07_flow.bsh` `product.flow.yield.even` | `targets.yaml` `product.yield.managed.total` `flow: even` |
| `RATIO_ACCOUNTS.bsh` `product.ratio.ct.area` / `product.ratio.ct.yield` | not mapped; reporting only, no target reads them |
| `RATIO_ACCOUNTS.bsh` flow ratios | folded into the two ws4 flow targets above |
| `Targets/06_patch.bsh` opening size classes | `targets.yaml` `patch.grpblk.*.size` |
| 5-year/100 m green-up | legacy reference; not the active ws4 policy |
| `scripts/reports_*.bsh` | `python -m ws4.cli report --run ... --out ...` |
| `headless_runtime_common.bsh` max-even-flow smoke | `run_pilot.py`; `ws4 optimize` for target-driven search |
| `ScenarioSet.bsh` `GRNUP` | legacy `min_green_up_years`; not used by the current pilot |
| `ScenarioSet.bsh` `Flow_GS`, flow targets | `targets.yaml` flow entries |
| `ScenarioSet.bsh` `THLB4070`, `BIOD`, `ECA`, `UWR`, `VQO` | not mapped: the canonical MKRF dataset has no such accounts |
| `01_Topology_fragments.bsh` `ProximalTopology` | `ws4/topology.csv`, generated from the current fragments |

## Files

| File | Purpose |
| --- | --- |
| `targets.yaml` | 100-year pilot targets: harvest floor, even flow, non-declining growing stock, opening-size classes |
| `targets_legacy.yaml` | the same targets with the literal legacy 500,000 m3/decade floor |
| `patch_accounts.yaml` | `patch.grpblk` opening-size account (touching blocks only) |
| `topology.csv` | proximal topology generated from the current `fragments.shp` |
| `build_patch_schedule.py` | grows 5-40 ha openings and assigns harvest years |
| `schedules/cc_at_60.csv` | aggressive baseline: every block clearcut at age 60 |
| `schedules/greenup_greedy.csv` | older constructed baseline, retained for comparison |
| `schedules/patch_first.csv` | current patch-first schedule |
| `make_greenup_schedule.py` | older baseline builder, retained for comparison |
| `run_pilot.py` | compiles the matrix and replays a schedule |
| `run_optimize.py` | starts the ws4 search from the patch-first schedule |
| `evidence/patch_first/` | patch-first simulation summary and target report |
| `evidence/patch_first_search/` | patch-first search summary and target report |
| `evidence/baseline/` | older constructed baseline |
| `evidence/legacy_greenup/` | previous 100 m green-up search, retained for comparison |

## Running the optimizer

```bash
python ws4/run_optimize.py --iterations 200
```

The ws4 move-delta evaluator prices the patch accounts and the optional
opening/green-up/core-area penalties. The pilot no longer passes
`min_green_up_years`; the opening targets are the policy instrument.
`--max-opening-ha` remains available as an optional hard ceiling.
`--coalesce-min-area-ha`/`--coalesce-max-area-ha` control the area-aware
coalesce move; the current default band is 5-40 ha.

## Pilot result (2026-10-21)

Patch-first simulation (`patch_first`):

- openings: 399, all in the 5-40 ha class
- patch shares at the target periods: **100% 5-40 ha**, 0% in 0-1, 1-5, 40-50
  and 50+ ha
- harvest by decade (m3): 299,022, 299,879, 299,094, 299,674, 298,376,
  299,893, 297,427, 299,344, 299,637, 214,215
- QMD numerator accounts: 81 (27 AUs x CT35/CT40/CT45)

Patch-first search (`patch_first_search`, 200 iterations):

- 973 blocks scheduled
- objective **101,863**
- patch targets met: 0% in 0-1, 1-5, 40-50 and 50+ ha at the target periods
- harvest by decade (m3): 293,361, 297,575, 297,901, 299,204, 294,875,
  299,466, 298,028, 299,344, 297,930, 214,298
- five harvest floors are slightly below 300,000; the final decade is the main
  shortfall because the patch builder leaves sub-5 ha clusters and blocks larger
  than 40 ha unharvested

Legacy comparison (`legacy_greenup_search`, previous 100 m policy):

- 1,742 blocks, zero spatial violations, objective 3,591,307
- 30 of 32 targets met; retained only as a comparison surface

## Boundaries and next steps

- The current opening-size targets are maxima, matching the legacy Patchworks
  `setMaximumPeriodic` semantics. Confirm that interpretation with MKRF staff.
- The numeric Very High/High weights are pilot defaults; confirm them before
  treating the patch targets as calibrated policy.
- The remaining harvest shortfall is in the final decade. The next step is to
  use the unharvested blocks: merge small clusters into existing openings or
  allow a capped 40-50 ha class, then rerun the patch-first builder.
- The public model uses published cost/price bases only. Raw MKRF cost/revenue
  spreadsheets and private financial overlays live in the tracked private
  overlay repo; see `planning/data_publication_boundary.md`.
- ws4 writes its canonical Parquet matrix, not the Patchworks `tracks/*.csv`
  contract. Patchworks remains the reference lane until the cutover is complete.
