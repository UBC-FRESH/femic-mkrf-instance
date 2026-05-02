Operator Runbook
================

Minimal Operator Path
---------------------

1. Validate the instance spec:

   - ``femic instance validate-spec --spec config/rebuild.spec.yaml``

2. Review the current runtime wiring:

   - ``config/patchworks.runtime.mkrf_rebuild.windows.yaml``

3. Inspect or launch the canonical runtime package from:

   - runtime XML: ``models/mkrf_patchworks_model/xml/forestmodel.xml``
   - runtime tracks: ``models/mkrf_patchworks_model/tracks/``
   - runtime spatial: ``models/mkrf_patchworks_model/spatial/``

4. Use the canonical package for:

   - current runtime/package inspection;
   - Matrix Builder rebuild validation; and
   - operator-facing canonical runtime review.

5. For canonical scenario smoke validation, use the canonical base lane and do
   not rely on very short scheduler samples:

   - ``femic patchworks run-default-scenario mkrf.base``

   The built-in canonical MKRF even-flow smoke is now configured at
   ``100000`` iterations because shorter samples were not stable enough for
   meaningful runtime validation.

6. After a canonical smoke run, audit the saved stage directly:

   - ``femic instance mkrf-audit-runtime-sanity --instance-root . --stage-dir runtime/logs/headless_stage/<run-id>``

5. Use the retained PoC package only for benchmark/reference comparison:

   - ``models/mkrf_patchworks_model_poc/analysis/base.pin``
   - ``models/mkrf_patchworks_model_poc/analysis/initialTargetSummary.csv``
   - ``models/mkrf_patchworks_model_poc/analysis/initialTargetStatus.csv``

Legacy Runtime Context
----------------------

The original analyst workflow was heuristic and stage-based rather than a
single deterministic batch solve. The modeling notes describe a solution
development approach where harvest objectives were activated first, patch
objectives were added next, harvest-flow controls were imposed later, and the
model was then allowed to converge toward a stable solution over large
iteration counts.

Operators using the retained PoC lane should interpret it in that same spirit:

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

That supports the current split usage pattern: use the canonical package for
current runtime/package work and the retained PoC lane for benchmark/reference
comparison against the legacy model family.

Current canonical runtime semantics
-----------------------------------

For the canonical MKRF rebuild lane:

- ``managed`` / ``unmanaged`` means treatment eligibility only;
- ``natural`` / ``treated`` means curve provenance only; and
- retention may move area to unmanaged without changing origin.

For this instance, the reviewed runtime origin rule is:

- stands younger than 80 years in 2020 are treated-origin;
- stands 80 years or older in 2020 are natural-origin.

That semantic split is now part of the accepted operator contract for the
canonical rebuild package.

What the current ``v0`` smoke proves
------------------------------------

The current canonical ``v0`` checkpoint is based on more than "the model
launched":

- Matrix Builder runs cleanly against the canonical package;
- the canonical even-flow smoke runs cleanly at ``100000`` iterations;
- the active total-yield even-flow objective is numerically stable in the
  saved stage; and
- the species-share sanity audit confirms that emitted ``indsp.*`` signals are
  consistent with the published source-share surface.

Do Not Treat This As
--------------------

- a rebuilt source-faithful control/entrypoint lane;
- a source-faithful claim for ``THLB4070(...)`` / ``UWR(...)`` /
  ``InitialTargets/00_Target_Descriptions.bsh``; or
- proof of exact legacy-equivalence across all remaining control seams.

Key Reads
---------

- ``README.md``
- ``runbooks/REBUILD_RUNBOOK.md``
- ``runbooks/LEGACY_REBUILD_READINESS_CRITERIA.md``
- ``runbooks/LEGACY_SOURCE_REPRODUCIBILITY_BOUNDARY.md``
