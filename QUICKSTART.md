# FEMIC Deployment Instance Quickstart

1. Validate CLI install:
   `femic --help`
2. Validate the rebuild-spec structure:
   `femic instance validate-spec --spec config/rebuild.spec.yaml`
3. Validate geospatial runtime dependencies (Fiona/GDAL):
   `femic prep geospatial-preflight`
4. Customize `config/run_profile.mkrf.yaml`.
5. Customize `config/rebuild.spec.yaml` for your case sequence/invariants.
6. Optionally update `config/rebuild.allowlist.yaml` for intentional baseline diffs.
7. Review the current legacy compiled-package reference in
   `runbooks/LEGACY_COMPILED_PACKAGE_REFERENCE.md`.
8. Review the current XML-builder authority note in
   `runbooks/LEGACY_XML_BUILDER_AUTHORITY_REVIEW.md`.
9. Review the current workbook surface map in
   `runbooks/LEGACY_XLSM_SURFACE_MAP.md`.
10. Review the current Input Variables translation note in
   `runbooks/LEGACY_INPUT_VARIABLES_TRANSLATION.md`.
11. Review the parent-side workbook review extract pointer in
   `metadata/legacy_xlsm_review_extracts.yaml`.
12. Review the translated Input Variables config in
   `config/legacy_xml_builder/input_variables.mkrf.yaml`, including the live
   block/area/age/exclude export seam and the live additional stratification
   fragment bindings, treatment-eligibility review flag, and scalar constants
   contract, plus the inactive-field classification for `max_inventory_age`
   and include-fragment hooks.
13. Inspect the copied archival control layer in
   `data/legacy_mkrf/compiled_controls/`.
14. Inspect the copied archival track tables in
   `data/legacy_mkrf/compiled_tracks/`.
15. Inspect the copied archival spatial runtime files in
   `data/legacy_mkrf/compiled_spatial/`.
16. Add case-specific instructions to `runbooks/REBUILD_RUNBOOK.md`.
17. Add/edit `config/tipsy/tsamkrf.yaml`.
18. Use `femic prep validate-case --run-config config/run_profile.mkrf.yaml`
   only after the real MKRF boundary and checkpoint inputs have been published
   into this instance.
