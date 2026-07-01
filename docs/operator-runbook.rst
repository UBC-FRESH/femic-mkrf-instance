Operator Runbook
================

Minimal Operator Path
---------------------

1. Validate and plan the FreshForge workflow graph:

   - ``freshforge providers``
   - ``freshforge validate workflows/freshforge/mkrf_model_build_workflow.yaml``
   - ``freshforge inspect workflows/freshforge/mkrf_model_build_workflow.yaml``
   - ``freshforge plan workflows/freshforge/mkrf_model_build_workflow.yaml``

   These commands are non-mutating graph checks.

2. Run the FreshForge workflow only when the local environment is ready for
   FEMIC, BTC, and Patchworks:

   - ``freshforge run workflows/freshforge/mkrf_model_build_workflow.yaml --run-id mkrf_freshforge_exec --report runtime/freshforge/runs/mkrf_freshforge_exec.json``

   ``freshforge run`` launches provider-owned FEMIC commands in planned order.
   The current executable graph uses the MKRF-owned runtime-package
   regeneration commands after geospatial preflight rather than the older
   TSA-style ``femic run`` and BTC/post-TIPSY lane. It does not materialize
   DataLad content or inspect declared artifact files in this phase.

3. Validate the instance spec:

   - ``femic instance validate-spec --spec config/rebuild.spec.yaml``

4. Review the current runtime wiring:

   - ``config/patchworks.runtime.mkrf_rebuild.windows.yaml``

5. Inspect or launch the canonical runtime package from:

   - runtime XML: ``models/mkrf_patchworks_model/xml/forestmodel.xml``
   - runtime tracks: ``models/mkrf_patchworks_model/tracks/``
   - runtime spatial: ``models/mkrf_patchworks_model/spatial/``

6. Use the canonical package for:

   - current runtime/package inspection;
   - Matrix Builder rebuild validation; and
   - operator-facing canonical runtime review.

   For the current model logic behind that package, read:

   - :doc:`treatments-and-state-logic`
   - :doc:`analysis-units-and-yield-curves`

6. For canonical scenario smoke validation, use the canonical base lane and do
   not rely on very short scheduler samples:

   - ``femic patchworks run-default-scenario mkrf.base``

   The built-in canonical MKRF even-flow smoke is now configured at
   ``100000`` iterations because shorter samples were not stable enough for
   meaningful runtime validation.

7. After a canonical smoke run, audit the saved stage directly:

   - ``femic instance mkrf-audit-runtime-sanity --instance-root . --stage-dir runtime/logs/headless_stage/<run-id>``

8. Use the retained PoC package only for benchmark/reference comparison:

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

Canonical treatment logic
-------------------------

The current canonical runtime includes both:

- ``CC``; and
- ``CT``.

Use :doc:`treatments-and-state-logic` for the exact current behavior,
including:

- ``CC`` minimum age and post-treatment transition;
- the cedar-pole ``CT35`` / ``CT40`` / ``CT45`` treatment family, its ``35``
  to ``50`` age window excluding age ``50``, retained scheduling lock, and
  explicit per-bucket ``thn035_`` / ``thn040_`` / ``thn045_`` transitions; and
- the current CT eligibility and intensity contract: runtime
  ground-operability evidence plus inclusive base planted ``Cw + Fd >= 50%``
  eligibility, with the target-bounded Hw-first medium ``45%`` basal-area
  removal lane active in the compiled runtime and low/high ``35%`` / ``55%``
  planning variants documented for calibration.

This redesign is the intended behavior for the next MKRF prerelease line
after ``v0.0.2a1``. The older legacy/PoC proportional split and broader
pre-cedar-pole CT age family are retained only as benchmark/reference context.

Canonical GUI map layers
------------------------

When launching the canonical ``base.pin`` in the Patchworks GUI, the default
map layer stack includes:

- ``Forest Outline`` as a very light gray model-extent context
  layer;
- ``Age Class (20-year)`` as a hidden-by-default dynamic mean-fragment-age
  layer using ``0.5 * (MANAGEDOFFSET + UNMANAGEDOFFSET)`` and a yellow-green
  graduated color ramp; and
- ``Current Treatments`` / ``Latest Treatments`` themes whose legend entries
  use the active treatment labels such as ``CC``, ``CT35``, ``CT40``, and
  ``CT45``.

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
