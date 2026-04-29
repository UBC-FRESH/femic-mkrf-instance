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
     stratification fragment bindings, the live treatment-eligibility review
     flag, and the explicit scalar constants contract for legacy expression
     symbol resolution, plus the P55.14 inactive-field classification for
     `max_inventory_age` and include-fragment hooks;
   - use `config/legacy_xml_builder/curve_library.mkrf.yaml`,
     `metadata/legacy_curve_library_translation.yaml`, and
     `runbooks/LEGACY_CURVE_LIBRARY_TRANSLATION.md` as the source of truth for
     the P55.15 Curve Library review-to-build contract, while keeping
     `beforeCurves` inactive pending generated `Curves.xml` reconciliation;
   - use `config/legacy_xml_builder/netdown.mkrf.yaml`,
     `metadata/legacy_netdown_translation.yaml`, and
     `runbooks/LEGACY_NETDOWN_TRANSLATION.md` as the source of truth for the
     P55.16 Netdown review-to-build contract, while keeping `dumpRetention`
     inactive pending retention builder/exporter activation;
   - use `config/legacy_xml_builder/attributes.mkrf.yaml`,
     `metadata/legacy_attributes_translation.yaml`, and
     `runbooks/LEGACY_ATTRIBUTES_TRANSLATION.md` as the source of truth for the
     P55.17 Attrib review-to-build contract, while keeping `dumpAttributes`
     inactive pending attribute builder/exporter activation;
   - use `config/legacy_xml_builder/strata/treat.mkrf.yaml`,
     `metadata/legacy_treat_translation.yaml`, and
     `runbooks/LEGACY_TREAT_TRANSLATION.md` as the source of truth for the
     P55.18 Treat stratum-bundle review-to-build contract, while keeping
     `dumpStratum` inactive pending stratum builder/reconciliation work;
   - use `metadata/legacy_workbook_compiled_reconciliation.yaml` and
     `runbooks/LEGACY_REBUILD_READINESS_REVIEW.md` as the source of truth for
     the P55.19 metadata-recovery go / runnable-rebuild no-go decision;
   - use `metadata/legacy_generated_xml_reconciliation.yaml` and
     `runbooks/LEGACY_GENERATED_XML_RECONCILIATION.md` as the source of truth
     for the P56.2 generated XML review artifacts and the still-blocked
     `beforeCurves` / XML-builder activation boundary;
   - use `metadata/legacy_compiled_track_evidence_reconciliation.yaml` and
     `runbooks/LEGACY_COMPILED_TRACK_EVIDENCE_RECONCILIATION.md` as the source
     of truth for the P56.3 existing legacy compiled curves/features/products
     track evidence and the git-annex publication boundary;
   - use `metadata/legacy_builder_activation_plan.yaml` and
     `runbooks/LEGACY_BUILDER_ACTIVATION_PLAN.md` as the source of truth for
     the P56.4 design-only builder activation and matrix-build handoff order;
   - use `metadata/legacy_source_input_publication_boundary.yaml` and
     `runbooks/LEGACY_SOURCE_INPUT_PUBLICATION_BOUNDARY.md` as the source of
     truth for the P56.5 fragments/topology, raw-source reproducibility, and
     identity-caveat publication boundary;
   - use `metadata/legacy_rebuild_readiness_criteria.yaml` and
     `runbooks/LEGACY_REBUILD_READINESS_CRITERIA.md` as the source of truth
     for the P56.6 metadata-recovery complete / runnable-rebuild no-go
     criteria;
   - use `metadata/legacy_runtime_model_layout.yaml` and
     `runbooks/LEGACY_RUNTIME_MODEL_LAYOUT.md` as the source of truth for the
     P57.2 materialized runtime scaffold, copied spatial/control inputs, and
     unresolved `InitialTargets` / XML / tracks gaps;
   - use `metadata/legacy_runtime_xml_emission.yaml` and
     `runbooks/LEGACY_RUNTIME_XML_EMISSION.md` as the source of truth for the
     P57.3 / P57.4 emitted `models/mkrf_patchworks_model/XML/baseMKRF.xml`
     runtime input candidate and the still-blocked no-run boundary;
   - use `metadata/legacy_attribute_passthrough.yaml` and
     `runbooks/LEGACY_ATTRIBUTE_PASSTHROUGH.md` as the source of truth for the
     explicit deferred-Attrib compatibility contract carried through the
     generated runtime XML;
   - use `metadata/legacy_runtime_config_wiring.yaml` and
     `runbooks/LEGACY_RUNTIME_CONFIG_WIRING.md` as the source of truth for the
     MKRF Patchworks runtime config wiring, builtin variant registration, and
     the passed preflight gate;
   - treat `data/legacy_mkrf/compiled_controls/` and
     `data/legacy_mkrf/compiled_tracks/` and
     `data/legacy_mkrf/compiled_spatial/` and
     `data/legacy_mkrf/generated_xml/` as inert archival references, not as an
     approved runnable rebuild surface;
   - treat `models/mkrf_patchworks_model/` as a partial runtime scaffold only
     until tracks generation and launch proof are completed;
   - finalize the real run profile, silviculture surface, and TIPSY rules;
   - publish the real MKRF boundary and checkpoint inputs required by `femic prep validate-case`;
   - classify bulky payload families in `.gitattributes`;
   - update metadata checksum ledgers; and
   - replace this thin-baseline runbook section with the real compile/BTC/Patchworks workflow.

## DataLad / annex smoke

1. `git annex enableremote arbutus-s3`
2. `python -m datalad get data/annex_smoke/mkrf_bootstrap_smoke.bin`
3. `git annex whereis data/annex_smoke/mkrf_bootstrap_smoke.bin`
