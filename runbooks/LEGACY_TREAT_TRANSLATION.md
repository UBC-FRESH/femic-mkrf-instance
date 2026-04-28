# Legacy Treat Translation

This note records the P55.18 review-to-build contract for the legacy MKRF
`Treat` workbook stratum bundle.

## Source

- Workbook: `MKRF_Cosmin_Model/MKRF/04_Models/PW_MKRF/XML/002_base.xlsm`
- Sheet: `Treat`
- Named ranges:
  - `stratumCriteria`
  - `stratumSuccession`
  - `stratumFeatures`
  - `stratumTreatments`
  - `stratumFactors`
  - `stratumProducts`
- Parent review extracts:
  - `metadata/mkrf_xlsm_review/treat.review.csv`
  - `metadata/mkrf_xlsm_review/ranges/treat_stratum_*.review.csv`

## Accepted Contract

The translated contract lives at:

- `config/legacy_xml_builder/strata/treat.mkrf.yaml`
- `metadata/legacy_treat_translation.yaml`

The accepted review-to-build candidates are:

- the empty stratum criteria surface as an explicit default-scope candidate;
- the default succession rule, `breakup_at = 999` and `renewal_age = 0`;
- the `CC` treatment definition; and
- the `CT` treatment definition.

The feature and product ranges preserve default/template values, but no row has
a `Feature Name` or `Product Name`. Those rows remain review metadata only.

## Archival Cross-Check

Copied compiled track tables confirm that `CC` and `CT` are materialized labels
in the archived runtime family. That evidence is not a source replacement and
does not make the instance runnable.

## Runtime Boundary

No Treat row is live exporter/build behavior in this slice. `dumpStratum`
remains inactive until a later stratum builder/reconciliation task accepts the
full treatment, product, account, and track semantics.

The next bounded move is P55.19 workbook-vs-compiled-output reconciliation.
