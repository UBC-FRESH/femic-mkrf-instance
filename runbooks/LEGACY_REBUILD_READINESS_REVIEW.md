# Legacy Rebuild Readiness Review

This note records the P55.19 reconciliation of the translated workbook-derived
MKRF ForestModel contract against the compiled legacy outputs currently carried
by the instance.

## Decision

Runnable rebuild readiness: **no-go**.

Metadata recovery readiness: **go** for planning the next recovery phase.

Phase 55 recovered the workbook-owned model contract into FEMIC-ready metadata,
but it did not make this instance a runnable legacy Patchworks rebuild.

## Evidence Available

Available in the instance:

- `data/legacy_mkrf/compiled_controls/entrypoints/baseMKRF.pin`
- materialized copied track tables:
  - `accounts.csv`
  - `protoaccounts.csv`
  - `strata.csv`
  - `treatments.csv`
  - `tracknames.csv`
  - `blocks.csv`
  - `groups.csv`
- translated workbook contracts under `config/legacy_xml_builder/`

The generated `baseMKRF.xml` and `Curves.xml` artifacts are not tracked in this
instance. `Tracks/curves.csv`, `Tracks/features.csv`, and `Tracks/products.csv`
are present only as pointer files in this working copy.

## Contract-Level Findings

`baseMKRF.pin` matches the translated horizon width at the contract level:
30 periods at 10 years each equals the translated 300-year horizon.

The copied accounts and protoaccounts tables support the translated account
surface at a review level: treatment accounts for `CC` and `CT` are present,
and `feature.area.managed.seral.le10` is present.

The copied treatments table supports the translated `CC` and `CT` treatment
labels at a review level. It contains 2,024 treatment rows: 1,434 `CC` rows and
590 `CT` rows.

## Blocking Gaps

Before claiming a runnable FEMIC/Patchworks rebuild, the next phase must:

- reconcile generated `baseMKRF.xml`;
- reconcile generated `Curves.xml` and/or `CSV/CURVE_TABLE.csv`;
- implement and validate FEMIC-native curve, retention, attribute, and stratum
  builders;
- define the matrix-build handoff that will later produce FEMIC-generated track
  outputs from FEMIC XML plus valid fragments/source inputs;
- publish the real MKRF boundary/checkpoint inputs required by the run profile;
  and
- decide whether `03_MappingAnalysisData`, roads, outputs, or direct workbook
  publication are required for reproducibility.

No upstream mapping data, report outputs, road-network payloads, or direct
workbook artifacts were ingested by P55.19.
