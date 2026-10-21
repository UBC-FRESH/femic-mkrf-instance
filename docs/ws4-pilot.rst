ws4 Pilot
=========

MKRF is the flagship pilot instance for moving the control layer from
Patchworks to ws4. The translated inputs and the runnable pilot live under
``ws4/`` in the repository; the full translation table and results are in
``ws4/README.md``.

Translation boundary
--------------------

The ws4 pilot keeps the canonical recipe and inventory:

- ``models/mkrf_patchworks_model/xml/forestmodel.xml``
- ``models/mkrf_patchworks_model/spatial/fragments.shp``

Everything that used to live in the Patchworks control layer is translated:

- ``analysis/base.pin`` horizon, topology, and patch targets;
- ``Targets/01_harvest.bsh`` harvest floors;
- ``Targets/07_flow.bsh`` even-flow and non-declining-yield controls;
- ``Targets/06_patch.bsh`` opening and separation-block size limits;
- ``RATIO_ACCOUNTS.bsh`` flow-ratio accounts; and
- ``headless_runtime_common.bsh``/``ScenarioSet.bsh`` scenario intent.

The canonical runtime now enables the optional ``greenup`` block with
``seral.le5``. The 5-year green-up and 50 ha opening rules are therefore both
the patch-account criterion and the ws4 spatial check
(``min_green_up_years`` and ``max_opening_ha``).

Running it
----------

From the instance root:

.. code-block:: bash

   python ws4/run_pilot.py --rebuild
   python ws4/run_optimize.py
   ws4/serve_pilot.sh

``run_pilot.py`` builds the ws4 matrix, replays the green-up-aware schedule
with the translated patch accounts, and writes
``ws4/runtime/greenup_greedy/`` plus a ``pilot_summary.json``.
``run_optimize.py`` starts the ws4 search from that schedule and writes a
normal search run under ``ws4/runtime/optimized/``. The web UI lists both runs.

Current pilot result
--------------------

The constructed schedule reports **zero spatial violations**. The optimized
run started from it also reports **zero spatial violations**, schedules 1,742
blocks, and meets 30 of the 32 translated targets. The harvest and
growing-stock profiles, QMD account coverage and patch-size shares are recorded
in ``ws4/README.md``.

Limits
------

- The legacy 500,000 m3/decade harvest floor is retained in
  ``ws4/targets_legacy.yaml`` for parity, but the runnable pilot uses a
  calibrated 300,000 floor for the 4,810 ha model.
- The ws4 incremental delta evaluator prices targets only, so the pilot
  harness uses the whole-schedule evaluator to keep the opening/green-up
  penalty in every move. Folding that penalty into the delta path is the next
  ws4-side improvement.
- Legacy scenario targets that depend on THLB, biodiversity, ECA, UWR or VQO
  accounts are not mapped because the canonical MKRF dataset has no such
  accounts.
