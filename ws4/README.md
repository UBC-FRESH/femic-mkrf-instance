# MKRF ws4 pilot

This directory is the ws4-native replacement for the MKRF Patchworks control
surface. The model recipe stays `models/mkrf_patchworks_model/xml/forestmodel.xml`
and the inventory stays
`models/mkrf_patchworks_model/spatial/fragments.shp`; everything below translates
the old `.pin` / `.bsh` behaviour to ws4 inputs.

## Quick start

```bash
cd /path/to/femic-mkrf-instance
python ws4/run_pilot.py --rebuild
python ws4/run_optimize.py
```

`run_pilot.py` compiles the recipe and fragments into `ws4/runtime/matrix/`,
replays `ws4/schedules/greenup_greedy.csv` with the translated patch accounts
and the 5-year / 50 ha constraints, and writes
`ws4/runtime/greenup_greedy/pilot_summary.json`. `run_optimize.py` starts the
ws4 search from that schedule, keeps the spatial weight high, and writes
`ws4/runtime/optimized/`. Use `--rebuild` after changing the runtime XML or
fragments; otherwise the cached matrix is reused.

Requires an importable `ws4` (`pip install -e /path/to/ws4`). The pilot was run
against the ws4 checkout at `/srv/shared-data/gep/ws4/ws4`.

## Web UI

After `run_pilot.py`, serve the pilot in the ws4 web UI:

```bash
ws4/serve_pilot.sh
```

Then open <http://127.0.0.1:8011/>. The launcher points the UI at the
pilot matrix, the `greenup_greedy` simulation and `optimized` search runs, the
translated targets, the 100 m topology, the patch accounts, and the fragments
GeoJSON. `PORT=...` overrides the port. The default bind is loopback only; ws4
provides no authentication, so do not expose it with `--allow-remote` unless
you put it behind a trusted proxy.

## Translation map

| Patchworks file / construct | ws4 equivalent |
| --- | --- |
| `analysis/base.pin` `periods = 30`, `Horizon.setHorizon(periods, 10)` | dataset horizon; `run_pilot.py --years`; target `period_width: 10` |
| `base.pin` `block_shape`, `block_key = "RES_KEY"` | `--fragments` shapefile; compiler block key |
| `base.pin` `control.inputTopology(..., 20d/100d)` | `ws4/topology.csv`; `patch_accounts.yaml` `search_distance` |
| `base.pin` `control.addPatchTarget("product.area.managed.treat.CC", "patch.grpblk...")` | `patch_accounts.yaml` `patch.grpblk` |
| `base.pin` `control.addPatchTarget("feature.area.managed.seral.le5", "patch.sepblk...")` | `patch_accounts.yaml` `patch.sepblk` |
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
| `run_optimize.py` | starts the ws4 search from `greenup_greedy.csv` and writes a normal search run |
| `evidence/` | captured summaries and target reports for the simulation and optimized runs |

## Running the optimizer

The same inputs drive the ws4 target search:

```bash
python ws4/run_optimize.py --iterations 50
```

`run_optimize.py` loads `greenup_greedy.csv`, starts the ws4 search from it,
and writes a normal ws4 search run. The ws4 move-delta evaluator now prices the
opening, green-up and core-area penalties, so the fast path keeps the spatial
rules in every move. `--full-evaluation` is available as a whole-schedule
cross-check.

The pilot keeps `spatial_weight` at 1,000,000. The `--seed-greedy` path is
expensive on the full 1,763-block model because it scores every candidate
chain for every block; the translated schedule is the pilot's warm start.

## Pilot result (2026-10-21)

The canonical runtime now enables `greenup` with `seral.le5`, so the patch
accounts and the exact ws4 spatial check use the same five-year criterion.

`greenup_greedy.csv` with `min_green_up_years=5` and `max_opening_ha=50`:

- spatial violations: **0**
- harvest by decade (m3): 680,096, 554,651, 308,150, 445,647, 330,787,
  266,906, 528,417, 510,859, 391,284, 439,393
- growing stock at decade ends (m3): 1,443,347 -> 858,346 by year 90
- QMD numerator accounts: 81 (27 AUs x CT35/CT40/CT45)
- 0-40 ha separation-block share: 78.4% at year 0, 100% from year 30 onward;
  40-50 ha and 50+ ha shares are 0% after the initial young-stand snapshot

`run_optimize.py --iterations 50` from that schedule (the ws4 move-delta path,
with the spatial penalty priced per move):

- spatial violations: **0**
- blocks scheduled: 1,742
- incumbent objective: 3,591,307
- harvest by decade (m3): 679,762, 546,062, 307,063, 445,879, 330,787,
  266,205, 527,989, 505,597, 387,684, 439,205
- growing stock: stable around 1.0-1.1 million m3 after the first rotation
- target status: 30 of 32 met; the decade-40 harvest floor and the even-flow
  band are the two remaining shortfalls

## Boundaries and next steps

- The legacy harvest floor of 500,000 m3/decade is preserved in
  `targets_legacy.yaml`, but the runnable pilot uses 300,000 because the
  canonical MKRF model is a 4,810 ha research forest.
- Green-up is now enabled in the canonical runtime config. Set
  `greenup.enabled: false` and rebuild to return to the old surface.
- The ws4 move-delta evaluator now includes the opening, green-up and core-area
  penalties. `--full-evaluation` remains available as a slower cross-check.
- ws4 writes its canonical Parquet matrix, not the Patchworks `tracks/*.csv`
  column contract. The Patchworks runtime package remains in the instance for
  comparison until the project finishes the cutover.
