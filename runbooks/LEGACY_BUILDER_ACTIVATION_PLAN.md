# Legacy Builder Activation Plan

This note records the P56.4 design for MKRF builder activation and Patchworks
matrix-build handoff order.

## Decision

Builder activation: **not started**.

Patchworks matrix build: **not run**.

Runnable rebuild readiness: **no-go**.

P56.4 defines the order of future implementation only. It does not activate
curve, retention, attribute, stratum, full XML, or matrix-build behavior.

## Activation Order

1. Curve emission.
2. Retention/netdown emission.
3. Attribute emission.
4. Stratum/treat emission.
5. Full ForestModel XML emission.
6. Patchworks matrix-build handoff.

Each surface must pass its validation gate before the next surface can claim
live behavior. The default exporter behavior remains unchanged, and MKRF
builder behavior must stay opt-in.

## Evidence Boundary

Legacy compiled controls, generated XML, spatial runtime files, and compiled
track tables are archival evidence. They may be used for comparison and
acceptance gates, but they are not FEMIC-regenerated outputs.

Future FEMIC-regenerated outputs are only produced after FEMIC emits XML from
the translated contracts and a Patchworks matrix build runs against validated
fragments/topology/source inputs.

## Next Boundary

P56.5 must resolve the real MKRF source-input publication boundary, including
fragments, checkpoint/boundary requirements, and the `Base TFL26` literal
description mismatch.

P56.4 did not generate ForestModel XML, regenerate fragments, run Patchworks
matrix build, import compiled track payloads, or introduce a runnable rebuild
claim.
