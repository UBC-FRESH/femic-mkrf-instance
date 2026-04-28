# Legacy Runtime XML Emission

This note records the `P57.3` emission of the first FEMIC-managed MKRF runtime
ForestModel XML.

## Decision

The runtime XML now exists at
`models/mkrf_patchworks_model/XML/baseMKRF.xml`.

It is emitted from the recovered MKRF contracts:

- `config/legacy_xml_builder/input_variables.mkrf.yaml`
- `config/legacy_xml_builder/curve_library.mkrf.yaml`
- `config/legacy_xml_builder/netdown.mkrf.yaml`
- `config/legacy_xml_builder/strata/treat.mkrf.yaml`
- `data/legacy_mkrf/generated_xml/CSV/CURVE_TABLE.csv`

The emitted XML carries the recovered input/output contract, stratification
defines, live scalar constants, Curve Library curves, inlined generated
`Yield_*` curves, Netdown retention rules, unmanaged catch-track, default
succession, and `CC` / `CT` treatments.

## Current Boundary

`P57.3` does not emit Attrib compatibility-passthrough blocks, does not rewire
runtime config, and does not run matrix build or launch proof. The emitted XML
is a runtime input candidate, not yet a runnable rebuild claim.
