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
- `runbooks/LEGACY_CURVE_LIBRARY_TRANSLATION.md`
- `runbooks/LEGACY_NETDOWN_TRANSLATION.md`
- `runbooks/LEGACY_ATTRIBUTES_TRANSLATION.md`
- `runbooks/LEGACY_TREAT_TRANSLATION.md`
- `runbooks/LEGACY_REBUILD_READINESS_REVIEW.md`
- `metadata/legacy_compiled_package_reference.yaml`
- `metadata/legacy_xml_builder_authority.yaml`
- `metadata/legacy_xlsm_surface_map.yaml`
- `metadata/legacy_xlsm_review_extracts.yaml`
- `metadata/legacy_input_variables_translation.yaml`
- `metadata/legacy_curve_library_translation.yaml`
- `metadata/legacy_netdown_translation.yaml`
- `metadata/legacy_attributes_translation.yaml`
- `metadata/legacy_treat_translation.yaml`
- `metadata/legacy_workbook_compiled_reconciliation.yaml`
- `metadata/legacy_generated_xml_reconciliation.yaml`
- `metadata/legacy_compiled_track_evidence_reconciliation.yaml`
- `metadata/legacy_builder_activation_plan.yaml`
- `config/legacy_xml_builder/input_variables.mkrf.yaml`
- `config/legacy_xml_builder/curve_library.mkrf.yaml`
- `config/legacy_xml_builder/netdown.mkrf.yaml`
- `config/legacy_xml_builder/attributes.mkrf.yaml`
- `config/legacy_xml_builder/strata/treat.mkrf.yaml`
- `data/legacy_mkrf/compiled_controls/`
- `data/legacy_mkrf/compiled_tracks/`
- `data/legacy_mkrf/compiled_spatial/`
- `data/legacy_mkrf/generated_xml/`

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

Copied generated XML review artifacts now present in-instance:

- `data/legacy_mkrf/generated_xml/baseMKRF.xml`
- `data/legacy_mkrf/generated_xml/CSV/CURVE_TABLE.csv`

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
  exclude expressions plus the additional stratification fragment bindings and
  the `treat_inel` treatment-eligibility review flag are live in exporter
  behavior at this stage, with `managed`, `unmanaged`, `operable`, and
  `lowoper` available through the explicit scalar constants contract;
- `max_inventory_age` and blank include-fragment hooks are preserved as review
  metadata;
- the Curve Library surface is now translated into a review-to-build contract
  that preserves curve identifiers, the `Age` axis, and nonblank curve points,
  while `before_curves` remains inactive until generated `Curves.xml`
  reconciliation is explicitly scheduled;
- the Netdown surface is now translated into a review-to-build contract that
  preserves the two complete proportional reassignment rules while keeping
  incomplete tail values as review metadata and `dumpRetention` inactive;
- the Attrib surface is now translated into a review-to-build contract that
  preserves 16 rows with nonblank `Attribute Name` values while keeping formula
  dependencies and `dumpAttributes` inactive;
- the Treat stratum bundle is now translated into a review-to-build contract
  that preserves the CC/CT treatment definitions and default succession rule
  while keeping feature/product template rows and `dumpStratum` inactive;
- the P55.19 reconciliation records a metadata-recovery go decision and a
  runnable-rebuild no-go decision pending generated XML, builder, compiled
  track, and upstream-input gap closure;
- the P56.2 generated XML reconciliation materializes inert review copies of
  `baseMKRF.xml` and `CSV/CURVE_TABLE.csv`, matches the base XML to translated
  Input Variables and Curve Library contracts, and matches located `Curves.xml`
  to `CURVE_TABLE.csv` by curve identifier, age, and value;
- the P56.3 compiled track evidence reconciliation records that legacy
  `curves.csv`, `features.csv`, and `products.csv` are readable compiled-output
  evidence in the planning corpus, while current instance paths remain pointer
  files pending git-annex availability;
- the P56.4 builder activation plan defines the future curve, retention,
  attribute, stratum, full XML emission, and matrix-build handoff order while
  preserving the archival-evidence versus future-regenerated-output boundary;
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
7. Review the Curve Library translation note:
   `runbooks/LEGACY_CURVE_LIBRARY_TRANSLATION.md`
8. Review the Netdown translation note:
   `runbooks/LEGACY_NETDOWN_TRANSLATION.md`
9. Review the Attributes translation note:
   `runbooks/LEGACY_ATTRIBUTES_TRANSLATION.md`
10. Review the Treat translation note:
   `runbooks/LEGACY_TREAT_TRANSLATION.md`
11. Review the rebuild readiness review:
   `runbooks/LEGACY_REBUILD_READINESS_REVIEW.md`
12. Review the parent-side workbook review extract pointer:
   `metadata/legacy_xlsm_review_extracts.yaml`
13. Review the translated Input Variables config:
   `config/legacy_xml_builder/input_variables.mkrf.yaml`
14. Review the translated Curve Library contract:
   `config/legacy_xml_builder/curve_library.mkrf.yaml`
15. Review the translated Netdown contract:
   `config/legacy_xml_builder/netdown.mkrf.yaml`
16. Review the translated Attributes contract:
   `config/legacy_xml_builder/attributes.mkrf.yaml`
17. Review the translated Treat contract:
   `config/legacy_xml_builder/strata/treat.mkrf.yaml`
18. Inspect the copied archival control layer under:
   `data/legacy_mkrf/compiled_controls/`
19. Inspect the copied archival track tables under:
   `data/legacy_mkrf/compiled_tracks/`
20. Inspect the copied archival spatial runtime files under:
   `data/legacy_mkrf/compiled_spatial/`
21. If this is a thin clone, materialize the annex smoke artifact:
   `python -m datalad get data/annex_smoke/mkrf_bootstrap_smoke.bin`
22. Run full `femic prep validate-case --run-config config/run_profile.mkrf.yaml --tipsy-config-dir config/tipsy`
   only after the real MKRF boundary and checkpoint inputs are published.

See `runbooks/REBUILD_RUNBOOK.md` for the current thin-baseline boundary.
