Rebuild and QA
==============

Current Rebuild Meaning
-----------------------

For the PoC lane, rebuild/QA means:

- regenerate the runtime XML from the reviewed contract surfaces;
- rebuild the runtime track package through Patchworks Matrix Builder;
- prove the runtime package launches; and
- compare benchmark summary reports against the accepted legacy benchmark lane.

This is intentionally narrower than the later canonical rebuild meaning. The
PoC rebuild loop is a contract-hardening and benchmark loop, not a full
source-faithful reconstruction loop.

Core Validation Surfaces
------------------------

- ``femic instance validate-spec --spec config/rebuild.spec.yaml``
- runtime XML under ``models/mkrf_patchworks_model_poc/XML/``
- runtime tracks under ``models/mkrf_patchworks_model_poc/Tracks/``
- benchmark comparison reports described in :doc:`benchmark-results`

High-Signal QA Logic
--------------------

The accepted QA stack for this PoC lane is:

1. validate the instance spec and runtime wiring;
2. regenerate the XML and tracks from the reviewed contract surfaces;
3. confirm that the runtime package launches;
4. run a representative benchmark scenario long enough to stabilize
   meaningfully; and
5. compare summary-report KPIs against the accepted legacy benchmark lane.

This follows the spirit of the original analyst workflow, where the model was
allowed to converge heuristically under substantial iteration budgets rather
than judged after a tiny smoke-only run.

Benchmark Acceptance Reading
----------------------------

The original legacy notes frame the base case around:

- long-run sustained yield;
- harvest rate over time;
- THLB standing volume over time; and
- harvest-system/age/operability breakdowns.

That is why the PoC benchmark acceptance used summary-report comparisons for:

- total growing stock; and
- harvested volume/treatment contribution.

The current accepted reading is:

- early-period behavior generally aligns with the legacy baseline; and
- longer-horizon divergence is visible but acceptable for a PoC benchmark lane.

Current Quality Bar
-------------------

The current quality bar is:

- operator-facing PoC benchmark confidence

It is not:

- exact long-horizon parity
- full legacy helper recovery
- source-faithful from-scratch rebuild acceptance

What Still Belongs To The Later Rebuild
---------------------------------------

The following items remain intentionally outside the PoC QA contract:

- full target-helper reconstruction;
- unexplained legacy seams such as ``THLB4070(...)`` and ``UWR(...)``;
- exact compiled-curve parity; and
- a raw-source-to-runtime rebuild claim from the upstream mapping-analysis lane.
