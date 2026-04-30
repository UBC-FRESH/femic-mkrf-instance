# MKRF Patchworks PoC Runtime Scaffold

This directory is the P57.2+ materialized runtime scaffold for the current
MKRF **PoC benchmark/intermediate** Patchworks model.

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
  semantics under `InitialTargets/00_Target_Descriptions.bsh`, including the
  absent legacy helper names `THLB4070(...)` and `UWR(...)`;
- for the PoC benchmark lane, `analysis/base.pin` now loads the legacy
  `initialTargetSummary.csv` and `initialTargetStatus.csv` checkpoint surfaces
  copied from the known-good `Outputs/001_Base/scenario/` run instead of
  waiting for full helper-library reconstruction;
- the representative PoC runtime proof is the active-target Patchworks GUI run
  saved under `analysis/scenarios/foo`;
- formula-heavy Attrib logic still arrives via compatibility passthrough;
- the accepted merch-tail variance remains documented for very-old-stand
  behavior; and
- this directory now represents a minimally runnable **MKRF PoC** runtime
  surface, not a raw-source reconstruction, exact legacy-equivalence claim, or
  the final canonical rebuild package.

Future boundary:

- the later source-faithful MKRF rebuild is expected to live alongside this
  PoC package in the same instance repository; and
- this directory should therefore be treated as benchmark/reference evidence
  only, not as the target architecture contract for the later rebuild.
