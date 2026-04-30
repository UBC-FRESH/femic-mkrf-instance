# Legacy Runtime XML Emission

This note records the `P57.3` through `P58.2` emission of the FEMIC-managed MKRF
runtime ForestModel XML and its later use in the Phase 57 minimally runnable
proof.

## Decision

The runtime XML now exists at
`models/mkrf_patchworks_model_poc/XML/baseMKRF.xml`.

It is emitted from the recovered MKRF contracts:

- `config/legacy_xml_builder/input_variables.mkrf.yaml`
- `config/legacy_xml_builder/curve_library.mkrf.yaml`
- `config/legacy_xml_builder/netdown.mkrf.yaml`
- `config/legacy_xml_builder/strata/treat.mkrf.yaml`
- `data/legacy_mkrf/generated_xml/CSV/CURVE_TABLE.csv`

The emitted XML carries the recovered input/output contract, stratification
defines, live scalar constants plus the compatibility-required `frd` constant,
Curve Library curves, inlined generated `Yield_*` curves, Netdown retention
rules, unmanaged catch-track, default succession, `CC` / `CT` treatments, and
the native Attrib feature/product blocks rebuilt from the reviewed workbook
contract.

## Current Boundary

This XML now participates in the minimally runnable MKRF claim when paired with
the accepted compiled spatial inputs, the generated runtime `Tracks/*.csv`
outputs, and the proven launch surface from the generated runtime directory.

It does not by itself claim:

- raw-source reconstruction from `03_MappingAnalysisData/*`;
- exact legacy compiled equivalence; or
- broader post-minimal-runnable hardening beyond the current native Attrib
  replacement.

