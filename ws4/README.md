# MKRF ws4 pilot

This directory is the ws4-native replacement for the MKRF Patchworks control
surface. The model recipe stays `models/mkrf_patchworks_model/xml/forestmodel.xml`
and the inventory stays
`models/mkrf_patchworks_model/spatial/fragments.shp`; everything below translates
the old `.pin` / `.bsh` behaviour to ws4 inputs.

## Quick start

```bash
cd /path/to/femic-mkrf-instance
python ws4/run_pilot.py
```

The script compiles the recipe and fragments into
`ws4/runtime/matrix/`, replays `ws4/schedules/greenup_greedy.csv` with the
translated patch accounts and the 5-year / 50 ha constraints, and writes
`ws4/runtime/greenup_greedy/pilot_summary.json`.

Requires an importable `ws4` (`pip install -e /path/to/ws4`). The pilot was run
against the ws4 checkout at `/srv/shared-data/gep/ws4/ws4`.

## Web UI

After `run_pilot.py`, serve the pilot in the ws4 web UI:

```bash
ws4/serve_pilot.sh
```

Then open <http://127.0.0.1:8011/>. The launcher points the UI at the
pilot matrix, the `greenup_greedy` run, the translated targets, the 100 m
topology, the patch accounts, and the fragments GeoJSON. `PORT=...` overrides
the port. The default bind is loopback only; ws4 provides no authentication,
so do not expose it with `--allow-remote` unless you put it behind a trusted
proxy.

## Translation map

| Patchworks file / construct | ws4 equivalent |
| --- | --- |
| `analysis/base.pin` `periods = 30`, `Horizon.setHorizon(periods, 10)` | dataset horizon; `run_pilot.py --years`; target `period_width: 10` |
| `base.pin` `block_shape`, `block_key = "RES_KEY"` | `--fragments` shapefile; compiler block key |
| `base.pin` `control.inputTopology(..., 20d/100d)` | `ws4/topology.csv`; `patch_accounts.yaml` `search_distance` |
| `base.pin` `control.addPatchTarget("product.area.managed.treat.CC", "patch.grpblk...")` | `patch_accounts.yaml` `patch.grpblk` |
| `base.pin` `control.addPatchTarget("feature.area.managed.seral.le10", "patch.sepblk...")` | `patch_accounts.yaml` `patch.sepblk` |
| `Targets/01_harvest.bsh` minimum periodic harvest | `targets.yaml` `product.yield.managed.total` minimum entries |
| `Targets/07_flow.bsh` `feature.flow.yield.total` | `targets.yaml` `feature.yield.managed.total` `flow: ndy` |
| `Targets/07_flow.bsh` `product.flow.yield.even` | `targets.yaml` `product.yield.managed.total` `flow: even` |
| `RATIO_ACCOUNTS.bsh` `product.ratio.ct.area` / `product.ratio.ct.yield` | not mapped; reporting only, no target reads them |
| `RATIO_ACCOUNTS.bsh` `feature.flow.yield.total` / `product.flow.yield.even` / `product.flow.yield.ndy` | folded into the two ws4 flow targets above |
| `Targets/06_patch.bsh` 40-50 ha max 5%, 50+ ha max 0 | `targets.yaml` `patch.sepblk.40_50.size` / `50_9999999.size` |
| 5-year green-up, 100 m adjacency (new policy) | `run_pilot.py` `min_green_up_years=5` with `topology.csv` |
| 50 ha maximum opening | `run_pilot.py` `max_opening_ha=50` |
| `scripts/reports_*.bsh` | `python -m ws4.cli report --run ... --out ...` |
| `headless_runtime_common.bsh` max-even-flow smoke | `run_pilot.py`; `ws4 optimize` for target-driven search |
| `ScenarioSet.bsh` `GRNUP` | `min_green_up_years` |
| `ScenarioSet.bsh` `Flow_GS`, flow targets | `targets.yaml` flow entries |
| `ScenarioSet.bsh` `THLB4070`, `BIOD`, `ECA`, `UWR`, `VQO` | not mapped: the canonical MKRF dataset has no THLB, biodiversity, ECA, UWR or VQO accounts |
| `01_Topology_fragments.bsh` `ProximalTopology` | `ws4/topology.csv`, generated from the current fragments |

## Files

| File | Purpose |
| --- | --- |
| `targets.yaml` | 100-year pilot targets: harvest floor, even flow, non-declining growing stock, separation-block limits |
| `targets_legacy.yaml` | the same targets with the literal legacy 500,000 m3/decade floor, for parity testing |
| `patch_accounts.yaml` | `patch.grpblk` and `patch.sepblk` definitions translated from `base.pin` |
| `topology.csv` | 100 m proximal topology generated from the current `fragments.shp` |
| `schedules/cc_at_60.csv` | aggressive baseline: every block clearcut at age 60 |
| `schedules/greenup_greedy.csv` | spatially constrained baseline used by `run_pilot.py` |
| `make_greenup_schedule.py` | builds the constrained schedule from fragments + topology |
| `run_pilot.py` | builds the matrix, replays the schedule, writes `pilot_summary.json` |

## Running the optimizer

The same inputs drive the ws4 target search:

```bash
python -m ws4.cli optimize \
  --dataset ws4/runtime/matrix \
  --targets ws4/targets.yaml \
  --years 100 \
  --iterations 500 \
  --topology ws4/topology.csv \
  --patch-accounts ws4/patch_accounts.yaml \
  --max-opening-ha 50 \
  --min-green-up-years 5 \
  --out ws4/runtime/optimized
```

`--seed-greedy` is the intended way to start from a target-satisfying schedule,
but it is expensive on the full 1,763-block model: it scores every candidate
chain for every block. The pilot therefore uses the constructed
`greenup_greedy.csv` schedule. A reduced-AU run or a faster seed is the next
ws4-side improvement.

## Pilot result (2026-10-21)

`greenup_greedy.csv` with `min_green_up_years=5` and `max_opening_ha=50`:

- spatial violations: **0**
- harvest by decade (m3): 672,753, 563,182, 507,431, 321,172, 278,578,
  257,143, 590,282, 553,524, 498,934, 332,902
- growing stock at decade ends (m3): 1,443,347 -> 657,156 by year 90
- QMD numerator accounts: 81 (27 AUs x CT35/CT40/CT45)

The `patch.sepblk` sub-accounts in the run use `feature.area.managed.seral.le10`
because that is the legacy Patchworks criterion. They therefore describe
10-year recent-harvest patches, not the 5-year policy. The exact 5-year rule is
the zero-violation `min_green_up_years=5` check above. If the project adopts
5-year green-up as the reporting criterion too, enable `greenup` in
`config/silviculture.mkrf.yaml`, rebuild the runtime XML so `seral.le5` exists,
and point `patch.sepblk.criteria` at it.

## Boundaries and next steps

- The legacy harvest floor of 500,000 m3/decade is preserved in the comments in
  `targets.yaml` but the pilot uses 300,000 because the canonical MKRF model is
  a 4,810 ha research forest. Restore 500,000 to test the literal legacy target.
- `ws4 optimize` is configured by the same `targets.yaml`, `patch_accounts.yaml`
  and `topology.csv`. On the full 1,763-block model the greedy seed is slow
  enough that the pilot uses a constructed schedule instead. A reduced-AU pilot
  or a faster seed is the next ws4-side improvement.
- ws4 writes its canonical Parquet matrix, not the Patchworks `tracks/*.csv`
  column contract. The Patchworks runtime package remains in the instance for
  comparison until the project finishes the cutover.
