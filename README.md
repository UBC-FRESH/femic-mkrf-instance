# femic-mkrf-instance

Private standalone **MKRF FEMIC instance** for bootstrap, contract hardening,
and later publication of the real MKRF model payload.

## Current status

This repository is intentionally a **thin baseline**.

Included now:

- standard FEMIC instance scaffold;
- `config/rebuild.spec.yaml` and `config/rebuild.allowlist.yaml`;
- `config/run_profile.mkrf.yaml`, `config/silviculture.mkrf.yaml`, and
  `config/tipsy/tsamkrf.yaml` starter surfaces;
- instance-local legacy compiled-package reference metadata plus a copied
  archival control layer plus archival track tables for the stable 2016
  `PW_MKRF` package, plus the archival spatial runtime family;
- `runbooks/REBUILD_RUNBOOK.md`;
- metadata ledgers for provenance and checksum tracking; and
- one non-sensitive annex-backed smoke artifact used to validate publication
  and cold-clone materialization.

Not included yet:

- the real MKRF bulky data/model payload;
- public/docs-hosted student-facing documentation; and
- packaged built-in registration in the parent FEMIC repo.

## Legacy Compiled Package Reference

This instance now carries a **metadata-only intake** of the stable compiled
legacy MKRF Patchworks package.

Instance-local reference surfaces:

- `runbooks/LEGACY_COMPILED_PACKAGE_REFERENCE.md`
- `runbooks/LEGACY_XML_BUILDER_AUTHORITY_REVIEW.md`
- `runbooks/LEGACY_XLSM_SURFACE_MAP.md`
- `runbooks/LEGACY_INPUT_VARIABLES_TRANSLATION.md`
- `metadata/legacy_compiled_package_reference.yaml`
- `metadata/legacy_xml_builder_authority.yaml`
- `metadata/legacy_xlsm_surface_map.yaml`
- `metadata/legacy_xlsm_review_extracts.yaml`
- `metadata/legacy_input_variables_translation.yaml`
- `config/legacy_xml_builder/input_variables.mkrf.yaml`
- `data/legacy_mkrf/compiled_controls/`
- `data/legacy_mkrf/compiled_tracks/`
- `data/legacy_mkrf/compiled_spatial/`

These surfaces summarize the discovered compiled package anatomy:

- `baseMKRF.pin` as the primary compiled model entrypoint;
- `Tracks/*.csv` as the compiled matrix/runtime table family;
- `Spatial/fragments.*` plus `Spatial/topo_frag100.csv` as the spatial runtime
  family; and
- `ScenarioSet.bsh`, `runME.bsh`, `Scripts/*.bsh`, and `Targets/*.bsh` as the
  scenario/control seam.

Copied archival controls now present in-instance:

- `data/legacy_mkrf/compiled_controls/entrypoints/`
- `data/legacy_mkrf/compiled_controls/scripts/`
- `data/legacy_mkrf/compiled_controls/targets/`

Copied archival track tables now present in-instance:

- `data/legacy_mkrf/compiled_tracks/`

Copied archival spatial runtime files now present in-instance:

- `data/legacy_mkrf/compiled_spatial/`

Important boundary:

- these copied files are **archival references only**;
- the copied bulky compiled runtime families now include `Tracks/*.csv`,
  `Spatial/fragments.*`, and `Spatial/topo_frag100.csv`;
- the governing editable-source seam for the core XML builder is now treated as
  workbook data surfaces from `002_base.xlsm`, not the checked-in generated XML;
- parent-side tracked workbook review extracts now live under
  `metadata/mkrf_xlsm_review/` in the parent FEMIC repo and are referenced here
  by `metadata/legacy_xlsm_review_extracts.yaml`;
- the first MKRF-first translated `Input Variables` config now lives at
  `config/legacy_xml_builder/input_variables.mkrf.yaml`, but only
  `description`, `start_year`, `horizon_years`, and the legacy block/area/age/
  exclude expressions plus the additional stratification fragment bindings are
  live in exporter behavior at this stage;
- `Spatial/patchworksLog.csv`, output, and upstream mapping-analysis payloads
  are still deferred; and
- this does not make the instance runnable as a legacy Patchworks rebuild.

## DataLad dataset policy

This repository is intended to follow the **large-only DataLad/git-annex**
pattern used by `femic-tsa29-instance`.

Policy:

- keep docs, config, runbooks, metadata ledgers, and other small canonical text
  in Git;
- annex bulky runtime/model/publication artifacts only; and
- do not publish transient local scratch or machine-specific secrets.

## Quickstart

1. Validate the rebuild contract:
   `femic instance validate-spec --spec config/rebuild.spec.yaml`
2. Dry-run the rebuild sequence:
   `femic instance rebuild --spec config/rebuild.spec.yaml --dry-run --run-id mkrf_dryrun`
3. Review the legacy compiled-package reference note:
   `runbooks/LEGACY_COMPILED_PACKAGE_REFERENCE.md`
4. Review the legacy XML-builder authority note:
   `runbooks/LEGACY_XML_BUILDER_AUTHORITY_REVIEW.md`
5. Review the legacy workbook surface map:
   `runbooks/LEGACY_XLSM_SURFACE_MAP.md`
6. Review the Input Variables translation note:
   `runbooks/LEGACY_INPUT_VARIABLES_TRANSLATION.md`
7. Review the parent-side workbook review extract pointer:
   `metadata/legacy_xlsm_review_extracts.yaml`
8. Review the translated Input Variables config:
   `config/legacy_xml_builder/input_variables.mkrf.yaml`
9. Inspect the copied archival control layer under:
   `data/legacy_mkrf/compiled_controls/`
10. Inspect the copied archival track tables under:
   `data/legacy_mkrf/compiled_tracks/`
11. Inspect the copied archival spatial runtime files under:
   `data/legacy_mkrf/compiled_spatial/`
12. If this is a thin clone, materialize the annex smoke artifact:
   `python -m datalad get data/annex_smoke/mkrf_bootstrap_smoke.bin`
13. Run full `femic prep validate-case --run-config config/run_profile.mkrf.yaml --tipsy-config-dir config/tipsy`
   only after the real MKRF boundary and checkpoint inputs are published.

See `runbooks/REBUILD_RUNBOOK.md` for the current thin-baseline boundary.
