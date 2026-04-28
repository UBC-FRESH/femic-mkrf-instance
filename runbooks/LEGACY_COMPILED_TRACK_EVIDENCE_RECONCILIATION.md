# Legacy Compiled Track Evidence Reconciliation

This note records the P56.3 review of existing legacy compiled track-table
evidence for `curves.csv`, `features.csv`, and `products.csv`.

## Decision

Legacy compiled track evidence: **available in the planning corpus**.

Instance payload publication: **blocked pending git-annex availability**.

Runnable rebuild readiness: **no-go**.

The legacy source CSVs are readable and are not missing. The current instance
paths for these three files remain pointer files:

- `data/legacy_mkrf/compiled_tracks/curves.csv`
- `data/legacy_mkrf/compiled_tracks/features.csv`
- `data/legacy_mkrf/compiled_tracks/products.csv`

Because `git annex` is unavailable in the active shell, P56.3 does not import
the large CSV payloads into the instance. They must not be committed as normal
Git blobs.

## Contract Findings

`curves.csv` is readable in the legacy planning corpus and contains 283,654
rows across 10,172 compiled numeric curve identifiers. It is compiled matrix
evidence, not a substitute for the translated workbook Curve Library contract.

`features.csv` is readable and contains 29,364 rows across 2,116 tracks and 38
labels. It carries managed/unmanaged area and yield label families that support
the translated Attrib review-to-build surface at the contract level.

`products.csv` is readable and contains 28,336 rows across 1,434 tracks and 22
labels. It carries CC and CT treatment product labels that support the
translated Treat and account surfaces at the contract level.

These tables are existing legacy compiled outputs. They are not
FEMIC-regenerated outputs and were not produced by this slice.

## Remaining Boundary

P56.4 must design the builder activation and matrix-build handoff order that
will eventually produce future FEMIC-generated XML and track outputs. That
future proof remains separate from the archival legacy evidence reviewed here.

P56.3 did not generate ForestModel XML, regenerate fragments, run Patchworks
matrix build, ingest upstream mapping data, publish direct workbook payloads,
or introduce a runnable rebuild claim.
