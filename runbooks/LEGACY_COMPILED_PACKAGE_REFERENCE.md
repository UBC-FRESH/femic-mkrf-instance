# MKRF Legacy Compiled Package Reference

This note records the **stable compiled-package anatomy** imported from the
legacy circa-2016 MKRF Patchworks model as review metadata only.

Authoritative legacy source lane for this note:

- `MKRF_Cosmin_Model/MKRF/04_Models/PW_MKRF`

This note does **not** mean the legacy payload itself is published here. It is
only the instance-local reference contract for the compiled package shape.

Copied archival files now live under:

- `data/legacy_mkrf/compiled_controls/entrypoints/`
- `data/legacy_mkrf/compiled_controls/scripts/`
- `data/legacy_mkrf/compiled_controls/targets/`
- `data/legacy_mkrf/compiled_tracks/`
- `data/legacy_mkrf/compiled_spatial/`

Those copied files are preserved for review and interpretation only.

## Primary entrypoints

- `baseMKRF.pin`
  primary compiled Patchworks model entrypoint
- `runME.bsh`
  one-line launcher that sources `ScenarioSet.bsh`
- `ScenarioSet.bsh`
  scenario-set controller with convergence and target activation logic

## Stable compiled package families

- `Tracks/*.csv`
  compiled Patchworks matrix/runtime tables
- `Spatial/fragments.*`
  fragment geometry surface
- `Spatial/topo_frag100.csv`
  topology sidecar
- `Targets/*.bsh`
  target-control scripts
- `Scripts/*.bsh`
  report/runtime helper scripts

## Relevant editable-source companions

These are now classified more narrowly:

- `XML/baseMKRF.xml`
- `XML/Curves.xml`
- `XML/002_base.xlsm`
- `XML/001_makeCurves_XML.py`
- `XML/003_MakeAccounts.py`

See `runbooks/LEGACY_XML_BUILDER_AUTHORITY_REVIEW.md` for the current authority
decision across those surfaces.

## Intended FEMIC interpretation

- `baseMKRF.pin`
  future analysis/runtime wrapper reference
- `Tracks/*.csv`
  future checked-in Patchworks runtime payload family
- `Spatial/fragments.*` and `topo_frag100.csv`
  future validated fragments/runtime spatial family
- `ScenarioSet.bsh`, `runME.bsh`, `Scripts/*.bsh`, `Targets/*.bsh`
  future runbook/analysis-control reference family

## Current boundary

- the small control layer plus the `Tracks/*.csv` family are copied into this
  instance by this slice;
- the `Spatial/fragments.*` family plus `topo_frag100.csv` are also copied
  into this instance by this slice;
- `patchworksLog.csv`, outputs, and mapping-analysis payloads remain deferred;
- no upstream mapping-analysis geodatabases or VDYP payloads are imported here;
- the workbook data surfaces are now treated as the governing editable-source
  truth for the core XML builder lane; and
- this note is for review metadata only, not runnable rebuild instructions.
