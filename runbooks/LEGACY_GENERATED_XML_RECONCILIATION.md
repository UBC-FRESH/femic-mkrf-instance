# Legacy Generated XML Reconciliation

This note records the P56.2 reconciliation of the generated MKRF XML artifacts
against the translated workbook-derived contracts.

## Decision

Generated XML review artifacts: **partly materialized for review**.

Runnable rebuild readiness: **no-go**.

The instance now carries inert review copies of:

- `data/legacy_mkrf/generated_xml/baseMKRF.xml`
- `data/legacy_mkrf/generated_xml/CSV/CURVE_TABLE.csv`

`Curves.xml` was located and reconciled from the legacy planning corpus, but it
is not copied into the instance in P56.2. The tracked `CSV/CURVE_TABLE.csv`
generator input is sufficient to preserve the generated curve-fragment contract
for this bounded slice.

These review artifacts do not activate `beforeCurves`, do not activate XML
builders, and do not make the MKRF instance runnable.

## Contract Findings

`baseMKRF.xml` matches the translated `Input Variables` contract for the
literal generated ForestModel description field, start year, 300-year horizon,
max inventory age, block/area/age/exclude expressions, additional
stratification source expressions, and scalar constants.

The literal generated description is `Base TFL26`. That is preserved as source
evidence only and is not accepted as the MKRF case identity. The identity
mismatch remains a metadata/reproducibility question for the later
source-input publication and rebuild-readiness criteria tasks.

The generated base XML carries the workbook Curve Library curves `zero`, `age`,
`le10`, `lt20`, `gt60`, `lt80`, and `gt250` with matching point coordinates.
It also carries built-in curve `one`, which is generator scaffolding rather
than a workbook Curve Library curve.

The located `Curves.xml` and tracked `CSV/CURVE_TABLE.csv` match by curve
identifier, age coordinate, and numeric value:

- 1,049 generated yield curves;
- 37,764 points;
- 36 age points per curve; and
- an age axis from 0 to 350 in 10-year steps.

Row order is not treated as the contract surface. The accepted comparison is
by curve identifier, age, and value.

## Remaining Blockers

`beforeCurves` remains inactive. P56.2 proves that the generated curve fragment
and its CSV generator input are now reviewable, but it does not decide or
activate a live include/emission path.

P56.3 verified existing legacy compiled track-table evidence (`curves.csv`,
`features.csv`, and `products.csv`) without regenerating those tables through
XML emission, fragment rebuild, or Patchworks matrix build.

The next bounded move is P56.4: design the builder activation and matrix-build
handoff order while keeping archival legacy evidence separate from future
FEMIC-regenerated outputs.

P56.2 did not ingest upstream mapping data, roads, outputs, direct workbook
payloads, or new raw/source inputs.
