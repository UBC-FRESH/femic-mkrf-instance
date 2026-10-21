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

The new 5-year green-up and 50 ha opening rules are enforced directly by ws4
(``min_green_up_years`` and ``max_opening_ha``), not approximated by patch
targets.

Running it
----------

From the instance root:

.. code-block:: bash

   python ws4/run_pilot.py

The script builds the ws4 matrix, replays the green-up-aware schedule with the
translated patch accounts, and writes ``ws4/runtime/greenup_greedy/`` plus a
``pilot_summary.json``.

Current pilot result
--------------------

With the translated separation-block accounts and a 5-year green-up interval
on the 100 m topology, the constructed schedule reports **zero spatial
violations**. The harvest and growing-stock profiles, QMD account coverage and
patch-size shares are recorded in ``ws4/README.md``.

Limits
------

- The legacy 500,000 m3/decade harvest floor is retained in
  ``ws4/targets_legacy.yaml`` for parity, but the runnable pilot uses a
  calibrated 300,000 floor for the 4,810 ha model.
- The patch accounts use the legacy ``seral.le10`` criterion because the
  canonical XML carries it. The exact 5-year rule is the ws4 spatial check.
  Switching the patch criterion to ``seral.le5`` requires enabling the
  optional ``greenup`` block in ``config/silviculture.mkrf.yaml`` and
  rebuilding the runtime XML.
- Legacy scenario targets that depend on THLB, biodiversity, ECA, UWR or VQO
  accounts are not mapped because the canonical MKRF dataset has no such
  accounts.
