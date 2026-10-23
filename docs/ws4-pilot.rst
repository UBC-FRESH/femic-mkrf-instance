ws4 Runtime
===========

**ws4 is the primary MKRF/NICC runtime.** The Patchworks XML/fragments package
is an interchange input to ws4, and the retained Patchworks packages are
reference-only. The translated inputs and runnable entrypoints live under
``ws4/`` in the repository; the full translation table and results are in
``ws4/README.md``.

The current MKRF staff decisions are recorded in
``planning/2026-10-21_basecamp_mkrf_decisions.md``; the public/private data
boundary is in ``planning/data_publication_boundary.md``.

Translation boundary
--------------------

The ws4 runtime keeps the canonical recipe and inventory:

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

The shares are ceilings (MKRF staff, October 2026); the runtime maps Very High to
10,000,000 and High to 1,000,000. The 100 m ``patch.sepblk`` green-up surface remains only in
the legacy Patchworks reference package.

Patch-first construction
------------------------

Random moves do not reliably form same-year openings, so the pilot builds them
directly with ``ws4/build_patch_schedule.py``:

1. aggregate managed fragments to blocks;
2. grow connected openings of touching blocks until they reach 5-40 ha;
3. assign each opening a harvest year, filling target periods toward 304,000 m3;
4. write ``schedules/patch_first.csv`` for ws4.

The builder merges small clusters where capacity allows and caps the 40-50 ha
class at 5%. Openings beyond the period capacity are left unharvested.

Running it
----------

From the instance root:

.. code-block:: bash

   python ws4/run_pilot.py --rebuild
   python ws4/build_patch_schedule.py \
     --dataset ws4/runtime/matrix \
     --topology ws4/topology.csv \
     --out ws4/schedules/patch_first.csv
   python ws4/run_pilot.py --skip-build \
     --schedule ws4/schedules/patch_first.csv \
     --run ws4/runtime/patch_first
   python ws4/run_optimize.py --iterations 50
   ws4/serve_pilot.sh

Current pilot result
--------------------

The patch-first schedule produces 364 openings, all in the 5-40 ha class, and
the target periods report 100% of patch area in that class. It schedules 1,226
blocks and meets all 32 targets. Harvest by period is 303,751, 303,789,
301,958, 302,521, 303,775, 303,146, 302,950, 303,481, 300,075 and 300,763 m3.

The 50-iteration search from that schedule keeps every target met and reaches
objective 0.

Limits
------

- The opening-size shares are confirmed as ceilings; the numeric Very High/High
  weights are an implementation calibration and may need further tuning.
- The builder uses a 304,000 m3 period target (the 300,000 policy floor plus a
  buffer) and caps the 40-50 ha class at 5%. The final run uses no 40-50 ha
  openings; the cap remains a guard for future data.
- The legacy 500,000 m3/decade harvest floor is retained in
  ``ws4/targets_legacy.yaml`` for parity, but the runnable pilot uses 300,000
  for the 4,810 ha model.
- The public model uses published cost/price bases only; raw MKRF cost/revenue
  spreadsheets and private financial overlays live in the tracked private
  overlay repo.
- Legacy scenario targets that depend on THLB, biodiversity, ECA, UWR or VQO
  accounts are not mapped because the canonical MKRF dataset has no such
  accounts.
