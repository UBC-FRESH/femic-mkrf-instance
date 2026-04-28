# Legacy Runtime Model Layout

This note records the P57.2 materialization of the MKRF runtime model
directory.

## Decision

The runtime model directory now exists at `models/mkrf_patchworks_model/`.

It contains:

- a sanitized `analysis/base.pin` derived from the archived legacy PIN;
- copied `Scripts/*.bsh` and `Targets/*.bsh` controls in instance-relative
  runtime homes; and
- copied compiled `Spatial/fragments.*` plus `Spatial/topo_frag100.csv` from
  the local planning-corpus runtime lane.

## Current Boundary

P57.2 does not generate `XML/baseMKRF.xml`, does not populate runtime
`Tracks/*.csv`, does not rewire Patchworks runtime config, and does not run
Patchworks matrix build or launch.

The scenario-control lane remains partial: `ScenarioSet.bsh` depends on
`InitialTargets/00_Target_Descriptions.bsh`, and that legacy file was not
recovered in the compiled control slice. The placeholder under
`models/mkrf_patchworks_model/InitialTargets/` fails fast by design so the gap
is explicit.

## Why The Spatial Copy Uses The Planning Corpus

The archived `data/legacy_mkrf/compiled_spatial/` lane is annex-backed, but
the configured annex remote was not usable in the active shell during P57.2.
To avoid leaving the runtime scaffold full of annex pointer stubs, the runtime
`Spatial/` payload was copied from the already-available local planning corpus
holding the same compiled legacy runtime family.
