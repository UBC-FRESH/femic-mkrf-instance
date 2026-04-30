Benchmark Results
=================

Accepted PoC Benchmark Surface
------------------------------

The accepted benchmark comparison used:

- legacy summary-report outputs under ``Outputs/001_Base/``
- PoC headless saved-stage outputs from the FEMIC runtime lane

Representative Scenario Surfaces
--------------------------------

Legacy benchmark scenario surface:

- legacy scripted scenario/run package:
  ``Outputs/001_Base/``
- original scripted run settings recorded in:
  ``Analyze_safe.txt`` and ``ScenarioSet.bsh``

PoC benchmark scenario surface:

- FEMIC headless run from:
  ``models/mkrf_patchworks_model_poc/analysis/base.pin``
- saved PoC stage used for the accepted benchmark:
  ``runtime/logs/headless_stage/p58_6_poc_smoke_r4/``

The accepted PoC comparison was the stabilized ``r4`` run, not the earlier
shorter smoke runs.

Primary report pairs:

- ``Forest_Attributes/yield.csv``
- ``Harvest_Attributes/harvestVolumeControls.csv``
- ``Harvest_Attributes/yield_treat.csv``

Those report pairs are the representative benchmark scenario surfaces for the
current PoC docs lane. They are the surfaces operators should reuse when they
want to answer "does the PoC still generally behave like the accepted legacy
baseline?"

Why These KPIs
--------------

The original MKRF modeling notes frame the base-case results around harvest
rate, THLB standing volume, merchantable standing volume, management-state
transition, operability split, age-at-harvest, and harvest-system mix. The PoC
benchmark therefore focused on the closest shared summary-report surfaces rather
than raw target-state inputs or raw schedule rows.

The chosen report pairs let us compare the two highest-signal outcomes first:

- total growing stock through ``Forest_Attributes/yield.csv``; and
- harvested volume and treatment contribution through the harvest-attributes
  reports.

Accepted Result
---------------

The benchmark was accepted as "generally lines up" rather than exact parity.

At the accepted PoC comparison run:

- initial total growing stock was effectively identical;
- early-period total growing stock was roughly ``+1%`` to ``+4%`` high in the
  PoC;
- early-period harvested volume was roughly ``-5%`` to ``-8%`` low in the PoC;
- longer-horizon divergence was larger, but accepted as non-blocking for the
  PoC benchmark lane.

Legacy Result Context
---------------------

The original legacy notes describe the base-case run as maintaining a harvest
rate near ``37,000 m3/year`` initially, declining modestly before returning to
an approximately long-run sustainable level near ``36,000 m3/year``. They also
describe a gradual decline in THLB standing volume from about ``1.5 million
m3`` toward ``1.0 million m3`` and frame the long-run sustainable yield as
``37,674 m3/year`` from the effective ``3,653 ha`` THLB.

Those legacy result descriptions are the reason the PoC benchmark is judged on
general alignment rather than exact parity. The legacy model itself was already
presented as a heuristic, assumption-bearing strategic analysis surface rather
than a mathematically exact truth surface.

Interpretation
--------------

The current PoC behaves like the same model family as the legacy package. It is
good enough for benchmark/reference use and reverse-engineering handoff, but it
does not claim exact legacy-equivalence over the full horizon.

That is the accepted PoC claim boundary.
