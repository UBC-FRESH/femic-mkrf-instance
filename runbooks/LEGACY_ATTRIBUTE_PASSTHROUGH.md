# Legacy Attribute Passthrough

This note records `P57.4`, which adds the explicit compatibility passthrough
for the deferred formula-heavy MKRF Attrib blocks.

## Decision

The runtime XML at `models/mkrf_patchworks_model/XML/baseMKRF.xml` now carries
five extracted legacy `<select>` blocks copied from the reconciled archival
`data/legacy_mkrf/generated_xml/baseMKRF.xml`.

This is a compatibility contract, not a native FEMIC Attrib builder.

The passthrough was accepted because the emitted XML now validates the narrow
dependencies those legacy blocks still require:

- define fields `status`, `au`, `aux`, `treatment`, `managed`, and `frd`;
- static curves `one` and `le10`; and
- emitted generated `Yield_*` curves.

## Included Blocks

- feature area and total-yield block;
- merchantable-yield block;
- individual-species-yield block;
- seral `le10` area block; and
- product area/yield/treatment block.

## Current Boundary

`P57.4` does not claim a native FEMIC reimplementation of the deferred Attrib
formulas. It only makes the emitted runtime XML structurally compatible enough
to proceed to runtime config wiring in the next bounded move.

No Patchworks runtime config was rewired here. No matrix build or Patchworks
launch proof was run here. The minimal runnable claim remains blocked until
later Phase 57 gates complete.
