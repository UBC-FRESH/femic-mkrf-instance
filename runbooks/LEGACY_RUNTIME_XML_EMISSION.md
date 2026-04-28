# Legacy Runtime XML Emission

This note records the `P57.3` / `P57.4` emission of the FEMIC-managed MKRF
runtime ForestModel XML.

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
defines, live scalar constants plus the compatibility-required `frd` constant,
Curve Library curves, inlined generated `Yield_*` curves, Netdown retention
rules, unmanaged catch-track, default succession, `CC` / `CT` treatments, and
the explicit deferred-Attrib compatibility passthrough blocks.

## Current Boundary

The Attrib formula-heavy blocks still arrive via compatibility passthrough from
the reconciled archival `baseMKRF.xml`, not through a native FEMIC builder.

`P57.4` still does not rewire runtime config or run matrix build or launch
proof. The emitted XML remains a runtime input candidate, not yet a runnable
rebuild claim.
