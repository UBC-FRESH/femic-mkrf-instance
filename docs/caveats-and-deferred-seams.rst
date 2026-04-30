Caveats and Deferred Seams
==========================

Accepted PoC Caveats
--------------------

The current PoC lane accepts several non-blocking variances:

- merchantable-yield tail variance:
  generated ``500/501`` vs legacy ``650/651`` for very-old-stand behavior
- exact compiled curve-id parity is not required
- longer-horizon benchmark divergence is larger than early-period divergence

Deferred Legacy Seams
---------------------

The following seams remain intentionally unresolved in the PoC lane:

- missing legacy ``00_Target_Descriptions.bsh`` helper library
- unresolved helper families such as ``THLB4070(...)`` and ``UWR(...)``
- broader source-faithful target/control reconstruction

Why They Are Deferred
---------------------

These gaps do not block the current PoC benchmark/intermediate contract. They
are pinned for the later from-scratch rebuild rather than being chased further
inside the benchmark lane.
