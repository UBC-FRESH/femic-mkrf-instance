Benchmark Results
=================

Accepted PoC Benchmark Surface
------------------------------

The accepted benchmark comparison used:

- legacy summary-report outputs under ``Outputs/001_Base/``
- PoC headless saved-stage outputs from the FEMIC runtime lane

Primary report pairs:

- ``Forest_Attributes/yield.csv``
- ``Harvest_Attributes/harvestVolumeControls.csv``
- ``Harvest_Attributes/yield_treat.csv``

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

Interpretation
--------------

The current PoC behaves like the same model family as the legacy package. It is
good enough for benchmark/reference use and reverse-engineering handoff, but it
does not claim exact legacy-equivalence over the full horizon.
