# Legacy Attributes Translation

This note records the P55.17 review-to-build contract for the legacy MKRF
`Attrib` workbook surface.

## Source

- Workbook: `MKRF_Cosmin_Model/MKRF/04_Models/PW_MKRF/XML/002_base.xlsm`
- Sheet: `Attrib`
- Named range: `attributes`
- Parent review extracts:
  - `metadata/mkrf_xlsm_review/attrib.review.csv`
  - `metadata/mkrf_xlsm_review/ranges/attrib_attributes.review.csv`

## Accepted Contract

The translated contract lives at:

- `config/legacy_xml_builder/attributes.mkrf.yaml`
- `metadata/legacy_attributes_translation.yaml`

The reviewed range contains 16 rows with nonblank `Attribute Name` values.
Those rows are grouped into:

- area accounting rows;
- yield aggregate rows;
- merchantable-yield row;
- individual-species yield rows; and
- the `le10` seral area row.

The remaining 143 nonblank workbook rows preserve template/default values but
have no `Attribute Name`, so they are review metadata only.

## Runtime Boundary

No Attrib row is live exporter/build behavior in this slice. The formulas that
depend on `frd`, `Yield_*` curve references, `LookupTable`, `treatment`, and
attribute-reference semantics remain blocked until later tasks translate those
dependencies and accept an attribute builder.

The next bounded move is the P55.18 `Treat` review-to-build contract.
