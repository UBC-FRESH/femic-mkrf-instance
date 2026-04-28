# Legacy Curve Library Translation

This note records the P55.15 review-to-build contract for the legacy MKRF
`Curve Library` workbook surface.

## Source

- Workbook: `MKRF_Cosmin_Model/MKRF/04_Models/PW_MKRF/XML/002_base.xlsm`
- Sheet: `Curve Library`
- Named range: `curveNames`
- Parent review extracts:
  - `metadata/mkrf_xlsm_review/curve_library.review.csv`
  - `metadata/mkrf_xlsm_review/ranges/curve_names.review.csv`

The generated `Curves.xml` fragment remains generated-reference evidence only.
The workbook-owned table is the reviewed source surface for future FEMIC-native
curve emission.

## Accepted Contract

The translated contract lives at:

- `config/legacy_xml_builder/curve_library.mkrf.yaml`
- `metadata/legacy_curve_library_translation.yaml`

The accepted fields are:

- `curve_id`: every nonblank workbook header cell after `Age`;
- `age`: the workbook `Age` column; and
- `value`: every nonblank cell under a named curve column.

Blank workbook value cells are absent points, not zero-valued points.

Accepted curve identifiers:

- `zero`
- `age`
- `le10`
- `lt20`
- `gt60`
- `lt80`
- `gt250`

## Runtime Boundary

This slice does not activate `beforeCurves` or claim that FEMIC can regenerate
the legacy `Curves.xml` fragment. That activation requires a later
fragment-equivalence pass against the generated `Curves.xml` contract.

The next bounded move is the P55.16 `Netdown` review-to-build contract.
