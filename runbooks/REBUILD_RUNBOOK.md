# MKRF Rebuild Runbook

This repository is intentionally a thin private-first baseline. Use this file
as the operator-facing boundary until the real MKRF payload and runtime
sequence are ready to publish.

## Thin-baseline checks

1. `femic instance validate-spec --spec config/rebuild.spec.yaml`
2. `femic instance rebuild --spec config/rebuild.spec.yaml --dry-run --run-id mkrf_dryrun`

## Current scope boundary

1. The real MKRF bulky data/model payload is not published in this slice.
2. The current repo carries only:
   - the standard FEMIC instance scaffold;
   - starter MKRF config surfaces;
   - instance-local metadata documenting the stable compiled legacy `PW_MKRF`
     package anatomy;
   - copied archival control files under `data/legacy_mkrf/compiled_controls/`;
   - copied archival track tables under `data/legacy_mkrf/compiled_tracks/`;
   - copied archival spatial runtime files under `data/legacy_mkrf/compiled_spatial/`;
   - metadata ledgers;
   - one annex-backed non-sensitive smoke artifact.
3. Before publishing the first substantive MKRF payload:
   - use `runbooks/LEGACY_COMPILED_PACKAGE_REFERENCE.md` and
     `metadata/legacy_compiled_package_reference.yaml` as the source of truth
     for the current compiled-package anatomy intake;
   - use `runbooks/LEGACY_XML_BUILDER_AUTHORITY_REVIEW.md` and
     `metadata/legacy_xml_builder_authority.yaml` as the source of truth for
     the current XML-builder authority-chain review;
   - use `runbooks/LEGACY_XLSM_SURFACE_MAP.md` and
     `metadata/legacy_xlsm_surface_map.yaml` as the source of truth for the
     current workbook sheet/range family map;
   - use `metadata/legacy_xlsm_review_extracts.yaml` as the source of truth
     for the parent-side tracked review extracts that materialize workbook
     values without copying the workbook into this instance;
   - use `config/legacy_xml_builder/input_variables.mkrf.yaml`,
     `metadata/legacy_input_variables_translation.yaml`, and
     `runbooks/LEGACY_INPUT_VARIABLES_TRANSLATION.md` as the source of truth
     for the first live-vs-staged Input Variables translation, including the
     live block/area/age/exclude export contract, the live additional
     stratification fragment bindings, and the live treatment-eligibility
     review flag;
   - treat `data/legacy_mkrf/compiled_controls/` and
     `data/legacy_mkrf/compiled_tracks/` and
     `data/legacy_mkrf/compiled_spatial/` as inert archival references, not as
     an approved runnable rebuild surface;
   - finalize the real run profile, silviculture surface, and TIPSY rules;
   - publish the real MKRF boundary and checkpoint inputs required by `femic prep validate-case`;
   - classify bulky payload families in `.gitattributes`;
   - update metadata checksum ledgers; and
   - replace this thin-baseline runbook section with the real compile/BTC/Patchworks workflow.

## DataLad / annex smoke

1. `git annex enableremote arbutus-s3`
2. `python -m datalad get data/annex_smoke/mkrf_bootstrap_smoke.bin`
3. `git annex whereis data/annex_smoke/mkrf_bootstrap_smoke.bin`
