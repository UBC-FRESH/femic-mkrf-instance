Caveats and Deferred Seams
==========================

Accepted PoC Caveats
--------------------

The current PoC lane accepts several non-blocking variances:

- merchantable-yield tail variance:
  generated ``500/501`` vs legacy ``650/651`` for very-old-stand behavior
- exact compiled curve-id parity is not required
- longer-horizon benchmark divergence is larger than early-period divergence

Accepted Benchmark Variances
----------------------------

The accepted benchmark interpretation for the current PoC is:

- initial total growing stock should line up essentially exactly;
- early-period growing stock can be modestly high in the PoC;
- early-period harvested volume can be modestly low in the PoC; and
- longer-horizon divergence can be materially larger without invalidating the
  PoC benchmark claim.

Concretely, the currently accepted comparison surface records:

- early-period total growing stock roughly ``+1%`` to ``+4%`` high; and
- early-period harvested volume roughly ``-5%`` to ``-8%`` low.

Those are accepted PoC variances, not open defects for the benchmark lane.

These caveats are accepted because the PoC is being used as:

- a benchmark/reference surface;
- a reverse-engineering stepping stone; and
- an operator-facing intermediate model.

They would not be strong enough for a final canonical rebuild claim, but they
are strong enough for the current PoC contract.

Deferred Legacy Seams
---------------------

The following seams remain intentionally unresolved in the PoC lane:

- missing legacy ``00_Target_Descriptions.bsh`` helper library
- unresolved helper families such as ``THLB4070(...)`` and ``UWR(...)``
- broader source-faithful target/control reconstruction

Current Claim Boundary
----------------------

Given the accepted benchmark variances and the unresolved helper seams, the
current PoC can claim:

- runnable FEMIC-managed MKRF benchmark package;
- generated runtime XML and generated runtime tracks;
- accepted benchmark-level behavioral similarity to the legacy baseline; and
- operator-facing value as a reverse-engineering stepping stone.

It cannot claim:

- exact legacy-equivalence;
- full recovery of the original target-helper/control layer; or
- source-faithful reconstruction from raw upstream source inputs.

What We Know About Those Seams
------------------------------

The missing target-helper seam is not random damage. The current evidence says:

- ``000_Targets_Builder.xlsx`` behaves like a deterministic source surface for
  much of the target/control lane;
- the helper/object wrapper layer that fed ``ScenarioSet.bsh`` was not
  preserved in the recovered corpus; and
- some helper families remain source-identifiable only at the intent level, not
  yet at the exact implementation level.

That is why these seams are pinned instead of being "creatively" patched into a
fake full recovery.

Why They Are Deferred
---------------------

These gaps do not block the current PoC benchmark/intermediate contract. They
are pinned for the later from-scratch rebuild rather than being chased further
inside the benchmark lane.

The practical rule is:

- if a seam changes the benchmark conclusion, it belongs in the PoC lane;
- if it does not change the benchmark conclusion, it belongs in the later
  canonical rebuild lane.
