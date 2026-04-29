# MKRF Patchworks Runtime Scaffold

This directory is the P57.2 materialized runtime scaffold for the first
minimally runnable MKRF Patchworks model.

Included now:

- `analysis/base.pin` as the sanitized runtime PIN entrypoint derived from the
  archived `baseMKRF.pin`;
- `Spatial/fragments.*` and `Spatial/topo_frag100.csv` as the accepted legacy
  compiled runtime inputs;
- `Scripts/*.bsh` and `Targets/*.bsh` copied into instance-relative runtime
  homes; and
- generated `XML/baseMKRF.xml` plus generated `Tracks/*.csv` outputs from the
  minimally runnable Phase 57 proof.

Current boundary:

- `analysis/ScenarioSet.bsh` still depends on unresolved target-description
  semantics under `InitialTargets/00_Target_Descriptions.bsh`;
- formula-heavy Attrib logic still arrives via compatibility passthrough;
- the accepted merch-tail variance remains documented for very-old-stand
  behavior; and
- this directory now represents a minimally runnable MKRF Patchworks runtime
  surface, not a raw-source reconstruction or exact legacy-equivalence claim.
