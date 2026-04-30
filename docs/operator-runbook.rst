Operator Runbook
================

Minimal Operator Path
---------------------

1. Validate the instance spec:

   - ``femic instance validate-spec --spec config/rebuild.spec.yaml``

2. Review the current runtime wiring:

   - ``config/patchworks.runtime.windows.yaml``

3. Launch the PoC runtime package from:

   - ``models/mkrf_patchworks_model_poc/analysis/base.pin``

4. Use the PoC package for:

   - benchmark comparison;
   - runtime smoke;
   - operator demonstration; and
   - reverse-engineering reference.

Legacy Runtime Context
----------------------

The original analyst workflow was heuristic and stage-based rather than a
single deterministic batch solve. The modeling notes describe a solution
development approach where harvest objectives were activated first, patch
objectives were added next, harvest-flow controls were imposed later, and the
model was then allowed to converge toward a stable solution over large
iteration counts.

Operators using the current PoC should interpret it in that same spirit:

- as a practical benchmark and runtime surface;
- as something that can be smoke-tested and compared meaningfully;
- but not as a fully reconstructed final control architecture.

What the Original Notes Suggest About Use
-----------------------------------------

The legacy notes also make clear that:

- commercial thinning assumptions were simplified;
- no genetic gain was applied;
- no extra natural-disturbance loss assumptions were applied; and
- some controls were explicitly candidates for future sensitivity analysis.

That supports the current PoC usage pattern: use the package to benchmark and
understand the legacy model family, then do the real contract redesign in the
later from-scratch rebuild lane.

Do Not Treat This As
--------------------

- the final canonical MKRF rebuild package;
- a source-faithful rebuild claim; or
- the final target/control architecture for the later from-scratch lane.

Key Reads
---------

- ``README.md``
- ``runbooks/REBUILD_RUNBOOK.md``
- ``runbooks/LEGACY_REBUILD_READINESS_CRITERIA.md``
- ``runbooks/LEGACY_SOURCE_REPRODUCIBILITY_BOUNDARY.md``
