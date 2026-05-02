Rebuild and QA
==============

Current Rebuild Meaning
-----------------------

For the current canonical lane, rebuild/QA means:

- regenerate the canonical runtime XML/package surfaces from rebuild-owned
  inputs;
- rebuild the runtime track package through Patchworks Matrix Builder;
- inspect the rebuilt runtime outputs directly; and
- compare the rebuilt runtime surface against the accepted PoC benchmark
  package where that comparison still matters for acceptance.

The retained PoC rebuild loop remains a separate benchmark/reference lane. It
is no longer the primary meaning of MKRF rebuild/QA in this instance.

Core Validation Surfaces
------------------------

- ``femic instance validate-spec --spec config/rebuild.spec.yaml``
- runtime XML under ``models/mkrf_patchworks_model/xml/``
- runtime tracks under ``models/mkrf_patchworks_model/tracks/``
- runtime spatial under ``models/mkrf_patchworks_model/spatial/``
- runtime species-share audit under
  ``models/mkrf_patchworks_model/analysis/runtime_species_share_audit.csv``
- benchmark comparison reports described in :doc:`benchmark-results`

High-Signal QA Logic
--------------------

The accepted QA stack for the canonical lane is:

1. validate the instance spec and runtime wiring;
2. regenerate the canonical XML/package surfaces from rebuild-owned inputs;
3. rebuild tracks through Matrix Builder;
4. inspect the rebuilt features/products/accounts directly; and
5. compare the resulting runtime surface against the accepted PoC benchmark
   package and legacy evidence where those still matter for acceptance.
6. run a canonical saved-stage sanity audit so source-share and emitted
   ``indsp.*`` signal agree.

The retained PoC benchmark lane still matters as comparison evidence, but it is
not the primary runtime/package acceptance lane anymore.

Benchmark Acceptance Reading
----------------------------

The original legacy notes frame the base case around:

- long-run sustained yield;
- harvest rate over time;
- THLB standing volume over time; and
- harvest-system/age/operability breakdowns.

That is why the retained benchmark lane used summary-report comparisons for:

- total growing stock; and
- harvested volume/treatment contribution.

The current accepted reading is:

- early-period behavior generally aligns with the legacy baseline; and
- longer-horizon divergence is visible but acceptable for a PoC benchmark lane.

Current Quality Bar
-------------------

The current quality bar is:

- canonical rebuild runtime/package confidence with explicit benchmark
  comparison boundaries and explicit runtime-signal sanity checks

It is not:

- exact long-horizon parity
- full legacy helper recovery
- a rebuilt source-faithful control/entrypoint lane

Current MKRF semantic contract
------------------------------

The canonical MKRF rebuild now treats these concepts separately:

- ``managed`` / ``unmanaged`` means Patchworks treatment eligibility only;
- ``natural`` / ``treated`` origin means yield-curve provenance only; and
- retention can move area from managed to unmanaged without changing origin.

For this instance, runtime origin is currently classified from the reviewed
2020-age rule:

- ``AGE_2020 >= 80`` -> ``natural``
- ``AGE_2020 < 80`` -> ``treated``

Do not interpret first-growth curve availability as a proxy for IFM state in
the canonical lane.

Canonical ``v0`` validation lane
--------------------------------

The current accepted operator-grade smoke for the canonical lane is:

1. regenerate the package;
2. rerun Matrix Builder;
3. run the canonical even-flow harvest-volume smoke at ``100000`` iterations;
   and
4. audit the saved stage with:

   - ``femic instance mkrf-audit-runtime-sanity --instance-root . --stage-dir <saved-stage>``

The saved-stage sanity audit is intended to catch cases where a species family
is emitted structurally but carries zero or contradictory signal relative to
the published source-share contract.

What Still Belongs To The Later Rebuild
---------------------------------------

The following items remain intentionally outside the current canonical QA
contract:

- full target-helper reconstruction;
- unexplained legacy seams such as ``THLB4070(...)`` and ``UWR(...)``;
- exact compiled-curve parity; and
- a source-faithful control/entrypoint rebuild claim.

Why This Separation Matters
---------------------------

If the team treats benchmark/reference evidence as though it were already the
canonical rebuild contract, it will overfit the MKRF rebuild to the older
compiled package and its unexplained seams.

The retained PoC lane should instead provide:

- a runnable benchmark package;
- accepted benchmark comparison surfaces;
- operator-facing explanation of what the PoC does and does not prove; and
- preserved evidence for the next rebuild phase to evaluate critically.

The canonical closeout phase should decide:

- what architecture to keep from the PoC because it is justified;
- what legacy behavior to re-implement because source evidence or benchmark
  necessity requires it; and
- what legacy seams to leave behind because they are not part of the desired
  FEMIC-native structure.
