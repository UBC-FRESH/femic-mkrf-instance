ws4 Pilot
=========

MKRF is the flagship pilot instance for moving the control layer from
Patchworks to ws4. The translated inputs and the runnable pilot live under
``ws4/`` in the repository; the full translation table and results are in
``ws4/README.md``.

The current MKRF staff decisions are recorded in
``planning/2026-10-21_basecamp_mkrf_decisions.md``; the public/private data
boundary is in ``planning/data_publication_boundary.md``.

Translation boundary
--------------------

The ws4 pilot keeps the canonical recipe and inventory:

- ``models/mkrf_patchworks_model/xml/forestmodel.xml``
- ``models/mkrf_patchworks_model/spatial/fragments.shp``

Everything that used to live in the Patchworks control layer is translated:

- ``analysis/base.pin`` horizon, topology, and patch targets;
- ``Targets/01_harvest.bsh`` harvest floors;
- ``Targets/07_flow.bsh`` even-flow and non-declining-yield controls;
- ``Targets/06_patch.bsh`` opening size classes;
- ``RATIO_ACCOUNTS.bsh`` flow-ratio accounts; and
- ``headless_runtime_common.bsh``/``ScenarioSet.bsh`` scenario intent.

Current opening-size policy (MKRF staff guidance, October 2026) uses
size-class targets and weights instead of a 100 m adjacency rule:

============  =============  =========
Size class    Target share   Weight
============  =============  =========
<= 1 ha       0%             Very High
> 1-5 ha      10%            High
> 5-40 ha     none           None
> 40-50 ha    5%             High
> 50 ha       0%             High
============  =============  =========

The pilot treats the shares as maxima and maps Very High to 1,000,000 and High
to 100,000. The 100 m ``patch.sepblk`` green-up surface remains only in the
legacy Patchworks reference package.

Running it
----------

From the instance root:

.. code-block:: bash

   python ws4/run_pilot.py --rebuild
   python ws4/run_optimize.py
   ws4/serve_pilot.sh

``run_pilot.py`` builds the ws4 matrix, replays the constructed baseline with
the translated patch accounts, and writes ``ws4/runtime/baseline/`` plus a
``pilot_summary.json``. ``run_optimize.py`` starts the ws4 search from that
schedule and writes ``ws4/runtime/anna_policy_search/``. The web UI lists the
baseline, the current-policy search, and the retained legacy green-up search.

Current pilot result
--------------------

The current-policy baseline does not yet meet the small-opening maxima: many
openings remain in the 0-1 ha and 1-5 ha classes. The 800-iteration
current-policy search schedules 1,701 blocks and improves the objective, but
the patch targets still bind. This is now a patch-aware search problem, not a
config problem.

The previous 100 m green-up search remains in ``ws4/evidence/legacy_greenup``
as a comparison surface: 1,742 blocks, zero spatial violations, objective
3,591,307, and 30 of 32 targets met.

Limits
------

- Confirm that the opening-size shares are maxima, not minima, and confirm the
  numeric Very High/High weights before treating the patch targets as
  calibrated policy.
- The legacy 500,000 m3/decade harvest floor is retained in
  ``ws4/targets_legacy.yaml`` for parity, but the runnable pilot uses 300,000
  for the 4,810 ha model.
- The public model uses published cost/price bases only. Raw MKRF cost/revenue
  spreadsheets and private financial overlays live in the tracked private overlay repo.
- Legacy scenario targets that depend on THLB, biodiversity, ECA, UWR or VQO
  accounts are not mapped because the canonical MKRF dataset has no such
  accounts.
