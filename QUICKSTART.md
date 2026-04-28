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
11. Review the current Curve Library translation note in
   `runbooks/LEGACY_CURVE_LIBRARY_TRANSLATION.md`.
12. Review the current Netdown translation note in
   `runbooks/LEGACY_NETDOWN_TRANSLATION.md`.
13. Review the parent-side workbook review extract pointer in
   `metadata/legacy_xlsm_review_extracts.yaml`.
14. Review the translated Input Variables config in
   `config/legacy_xml_builder/input_variables.mkrf.yaml`, including the live
   block/area/age/exclude export seam and the live additional stratification
   fragment bindings, treatment-eligibility review flag, and scalar constants
   contract, plus the inactive-field classification for `max_inventory_age`
   and include-fragment hooks.
15. Review the translated Curve Library contract in
   `config/legacy_xml_builder/curve_library.mkrf.yaml`; it is review-to-build
   metadata only and does not activate `beforeCurves`.
16. Review the translated Netdown contract in
   `config/legacy_xml_builder/netdown.mkrf.yaml`; it is review-to-build
   metadata only and does not activate `dumpRetention`.
17. Inspect the copied archival control layer in
   `data/legacy_mkrf/compiled_controls/`.
18. Inspect the copied archival track tables in
   `data/legacy_mkrf/compiled_tracks/`.
19. Inspect the copied archival spatial runtime files in
   `data/legacy_mkrf/compiled_spatial/`.
20. Add case-specific instructions to `runbooks/REBUILD_RUNBOOK.md`.
21. Add/edit `config/tipsy/tsamkrf.yaml`.
22. Use `femic prep validate-case --run-config config/run_profile.mkrf.yaml`
   only after the real MKRF boundary and checkpoint inputs have been published
   into this instance.
