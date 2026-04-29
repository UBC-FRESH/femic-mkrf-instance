# Legacy Source Reproducibility Boundary

This note records the Phase 58 closeout boundary between:

- the currently accepted minimal-runnable MKRF runtime claim; and
- any future source-faithful rebuild claim.

## Current Allowed Claim

The current MKRF instance can claim:

- FEMIC-managed runtime XML emission;
- successful Patchworks matrix build against that emitted XML;
- successful launch from the generated runtime model directory; and
- use of accepted compiled spatial runtime inputs as the runtime input lane.

That is the current minimal-runnable boundary.

## Current Disallowed Claim

The current MKRF instance cannot yet claim a source-faithful rebuild from the
legacy planning corpus.

Specifically, it cannot claim that:

- runtime `Spatial/fragments.*` was regenerated from upstream mapping inputs;
- runtime `topo_frag100.csv` was regenerated from upstream source geometry; or
- checkpoint-derived or compiled-runtime artifacts are equivalent to raw source.

## Raw Source Means

For MKRF, raw source means the upstream mapping/yield-prep lane under
`03_MappingAnalysisData/*`, including the source and resultant geodatabases and
the reviewed supporting source families.

The currently reconstructed direct precursor to runtime `fragments.*` is:

- `03_MappingAnalysisData/Resultant.gdb/Resultant`

The currently reconstructed runtime publication rule is:

1. start from `Resultant.gdb/Resultant`;
2. filter to `CONTCLAS != 'X'`;
3. project to the runtime field subset; and
4. publish through shapefile naming/type normalization.

This contract has been reconstructed and verified at the metadata level. It has
not been re-executed as a reproduced source workflow.

## What Does Not Count As Raw Source

The following are not acceptable substitutes for raw source:

- legacy compiled runtime `Spatial/fragments.*`
- legacy compiled runtime `Spatial/topo_frag100.csv`
- instance archival copies under `data/legacy_mkrf/compiled_spatial/*`
- restart checkpoints, resume checkpoints, and debug boundary artifacts
- any derivative fragment exports produced from already-compiled runtime lanes

Those surfaces remain useful for runtime validation, comparison, and debugging.
They do not answer source-faithful provenance questions.

## Future Gate For A Source-Faithful Claim

A future source-faithful MKRF rebuild claim should not be made until the
following are satisfied:

1. the authoritative upstream source families are materialized or linked in a
   reviewable way;
2. the transformation from upstream source to `Resultant` is documented well
   enough to audit or reproduce;
3. the `Resultant -> fragments.*` publication step is reproduced or otherwise
   audited beyond metadata-only reconstruction; and
4. the existing `Base TFL26` identity caveat remains explicit in any
   user-facing claim.

Until then, the correct claim surface is:

- minimally runnable MKRF instance, not source-faithful MKRF rebuild.
