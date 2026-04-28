# Legacy Netdown Translation

This note records the P55.16 review-to-build contract for the legacy MKRF
`Netdown` workbook surface.

## Source

- Workbook: `MKRF_Cosmin_Model/MKRF/04_Models/PW_MKRF/XML/002_base.xlsm`
- Sheet: `Netdown`
- Named ranges:
  - `netdownCriteria`
  - `netdownNames`
  - `netdownFactors`
- Parent review extracts:
  - `metadata/mkrf_xlsm_review/netdown.review.csv`
  - `metadata/mkrf_xlsm_review/ranges/netdown_criteria.review.csv`
  - `metadata/mkrf_xlsm_review/ranges/netdown_names.review.csv`
  - `metadata/mkrf_xlsm_review/ranges/netdown_factors.review.csv`

## Accepted Contract

The translated contract lives at:

- `config/legacy_xml_builder/netdown.mkrf.yaml`
- `metadata/legacy_netdown_translation.yaml`

The two complete review-to-build candidate rules are:

- `status in managed and oper in operable` reassigned to `status = unmanaged`
  with netdown proportion `0.1`;
- `status in managed and oper in lowoper` reassigned to `status = unmanaged`
  with netdown proportion `0.2`.

Both complete rules assign `feature.area.retention.total` with factor `1`.

## Review-Only Values

The reviewed named ranges also contain one unmatched feature-factor row with
value `1` and 85 trailing `0.07` values in the Netdown column with no complete
selection or reassignment row. Those values are preserved as review metadata
only.

## Runtime Boundary

This slice does not activate `dumpRetention` emission and does not make the
current MKRF exporter split/reassign fragment area from the legacy Netdown
table.

The next bounded move is the P55.17 `Attrib` review-to-build contract.
