# MKRF Legacy XML Builder Authority Review

This note records the current authority-chain decision for the legacy MKRF XML
builder lane under `MKRF_Cosmin_Model/MKRF/04_Models/PW_MKRF/XML`.

## Decision

Treat `002_base.xlsm` as the **governing editable-source surface** for the core
legacy ForestModel XML structure.

Treat these files as **generated or helper surfaces**, not as the governing
authoring surface:

- `baseMKRF.xml`
- `Curves.xml`
- `001_makeCurves_XML.py`
- `003_MakeAccounts.py`

## Why

The embedded SPS VBA in `002_base.xlsm` exposes a top-level `DumpXML(filename)`
routine that writes the XML in ordered sections:

- `dumpProlog`
- `dumpCurves`
- `dumpRetention`
- `dumpUnmanaged`
- `dumpStratum`
- `dumpAttributes`

The workbook-owned data surfaces feeding that serializer include:

- `Input Variables`
- `Netdown`
- `curveNames` curve-library ranges
- stratum sheet ranges such as `stratumCriteria`, `stratumFeatures`,
  `stratumSuccession`, `stratumProducts`, `stratumTreatments`, and
  `stratumFactors`
- attribute-sheet `attributes`
- constants-sheet `constantValues`

`baseMKRF.xml` itself carries the SPS generator fingerprint:

- it identifies `Simple ForestModel Spreadsheet Tool`; and
- it records `002_base.xlsm` in the generated header.

It also includes `Curves.xml` through the `beforeCurves` entity, which means
the checked-in XML is already an assembled/generated artifact rather than the
primary edit surface.

## FEMIC interpretation

For FEMIC recovery work, the workbook data surfaces are the part worth
preserving.

The VBA is still useful as **evidence of serialization semantics**, but not as
the desired long-term runtime path. The intended translation is:

- preserve workbook tables and named ranges as reviewable source evidence;
- refactor those surfaces into FEMIC-native config and tabular inputs; and
- replace the SPS VBA serializer with FEMIC-native exporters/builders.

## Boundary

- This note resolves the authority seam at the **metadata** level only.
- No workbook payload has been copied into the MKRF instance by this slice.
- No runnable rebuild path is claimed yet.
- `03_MappingAnalysisData/*`, `Outputs/*`, and roads discovery remain out of
  scope for this slice.
