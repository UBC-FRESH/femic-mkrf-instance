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
- placeholder `XML/` and `Tracks/` directories for future FEMIC-generated XML
  and Patchworks matrix-build outputs.

Current boundary:

- `XML/baseMKRF.xml` is not generated here yet;
- `Tracks/*.csv` in this directory are not generated yet;
- `analysis/ScenarioSet.bsh` still depends on unresolved target-description
  semantics under `InitialTargets/00_Target_Descriptions.bsh`; and
- this scaffold is not yet a runnable FEMIC/Patchworks rebuild claim.
