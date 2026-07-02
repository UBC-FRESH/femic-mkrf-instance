Rebuild and QA
==============

Current Rebuild Meaning
-----------------------

For the current canonical lane, rebuild/QA means:

- regenerate the canonical runtime XML/package surfaces from rebuild-owned
  inputs;
- rebuild the runtime track package through Patchworks Matrix Builder;
- inspect the rebuilt runtime outputs directly; and
- compare the rebuilt runtime surface against the accepted PoC benchmark
  package where that comparison still matters for acceptance.

The retained PoC rebuild loop remains a separate benchmark/reference lane. It
is no longer the primary meaning of MKRF rebuild/QA in this instance.

Core Validation Surfaces
------------------------

- ``femic instance validate-spec --spec config/rebuild.spec.yaml``
- ``freshforge validate workflows/freshforge/mkrf_model_build_workflow.yaml``
- ``freshforge inspect workflows/freshforge/mkrf_model_build_workflow.yaml``
- ``freshforge plan workflows/freshforge/mkrf_model_build_workflow.yaml``
- ``freshforge run workflows/freshforge/mkrf_model_build_workflow.yaml --workdir runtime/freshforge --namespace mkrf/model-build --json``
- ``freshforge validate external/femic-mkrf-instance/workflows/freshforge/mkrf_materialization_workflow.yaml``
- ``freshforge inspect external/femic-mkrf-instance/workflows/freshforge/mkrf_materialization_workflow.yaml``
- ``freshforge plan external/femic-mkrf-instance/workflows/freshforge/mkrf_materialization_workflow.yaml``
- ``freshforge run external/femic-mkrf-instance/workflows/freshforge/mkrf_materialization_workflow.yaml --workdir runtime/freshforge --namespace mkrf/materialization --json``
- runtime XML under ``models/mkrf_patchworks_model/xml/``
- runtime tracks under ``models/mkrf_patchworks_model/tracks/``
- runtime spatial under ``models/mkrf_patchworks_model/spatial/``
- runtime species-share audit under
  ``models/mkrf_patchworks_model/analysis/runtime_species_share_audit.csv``
- benchmark comparison reports described in :doc:`benchmark-results`

High-Signal QA Logic
--------------------

The accepted QA stack for the canonical lane is:

1. validate the FreshForge graph, instance spec, and runtime wiring;
2. regenerate the canonical XML/package surfaces from rebuild-owned inputs;
3. rebuild tracks through Matrix Builder;
4. inspect the rebuilt features/products/accounts directly; and
5. compare the resulting runtime surface against the accepted PoC benchmark
   package and legacy evidence where those still matter for acceptance.
6. run a canonical saved-stage sanity audit so source-share and emitted
   ``indsp.*`` signal agree.

The retained PoC benchmark lane still matters as comparison evidence, but it is
not the primary runtime/package acceptance lane anymore.

FreshForge Workflow Boundary
----------------------------

The FreshForge workflow at
``workflows/freshforge/mkrf_model_build_workflow.yaml`` is the declarative
contract for the MKRF rebuild graph. It records the validate-case through
matrix-build order, reusable FEMIC provider references, MKRF-owned provider
references, MKRF-owned configuration paths, and declared runtime artifacts.

FreshForge validation, inspection, and planning are non-mutating. FreshForge
``run`` explicitly launches provider-owned FEMIC commands in planned order,
including the MKRF-owned runtime-package regeneration commands and Patchworks
Matrix Builder. FreshForge materialization is a separate workflow that can
prepare a thin parent checkout by initializing the MKRF submodule, installing
dependencies, enabling ``arbutus-s3``, materializing required MKRF paths, and
writing an ignored report. The current MKRF executable graph does not use the
older TSA-style ``femic run`` and BTC/post-TIPSY nodes because those still
require legacy checkpoint files outside the accepted MKRF source contract.
``femic instance rebuild --dry-run`` remains the legacy execution dry-run
comparison surface for ``config/rebuild.spec.yaml``.

Install this repository's adapter package before running FreshForge commands:

.. code-block:: bash

   python -m pip install -e .

The adapter exposes provider id ``mkrf``. FEMIC core exposes reusable provider
id ``femic`` and no longer owns MKRF-specific ``mkrf-*`` commands. The MKRF instance package owns those commands through ``mkrf-femic`` and ``python -m mkrf_femic``.

Benchmark Acceptance Reading
----------------------------

The original legacy notes frame the base case around:

- long-run sustained yield;
- harvest rate over time;
- THLB standing volume over time; and
- harvest-system/age/operability breakdowns.

That is why the retained benchmark lane used summary-report comparisons for:

- total growing stock; and
- harvested volume/treatment contribution.

The current accepted reading is:

- early-period behavior generally aligns with the legacy baseline; and
- longer-horizon divergence is visible but acceptable for a PoC benchmark lane.

Current Quality Bar
-------------------

The current quality bar is:

- canonical rebuild runtime/package confidence with explicit benchmark
  comparison boundaries and explicit runtime-signal sanity checks

It is not:

- exact long-horizon parity
- full legacy helper recovery
- a rebuilt source-faithful control/entrypoint lane

Current MKRF semantic contract
------------------------------

The canonical MKRF rebuild now treats these concepts separately:

- ``managed`` / ``unmanaged`` means Patchworks treatment eligibility only;
- ``natural`` / ``treated`` origin means yield-curve provenance only; and
- retention can move area from managed to unmanaged without changing origin.

For this instance, runtime origin is currently classified from the reviewed
2020-age rule:

- ``AGE_2020 >= 80`` -> ``natural``
- ``AGE_2020 < 80`` -> ``treated``

Do not interpret first-growth curve availability as a proxy for IFM state in
the canonical lane.

Canonical ``v0`` validation lane
--------------------------------

The current accepted operator-grade smoke for the canonical lane is:

1. regenerate the package;
2. rerun Matrix Builder;
3. run the canonical even-flow harvest-volume smoke at ``100000`` iterations;
   and
4. audit the saved stage with:

   - ``mkrf-femic mkrf-audit-runtime-sanity --instance-root . --stage-dir <saved-stage>``

The saved-stage sanity audit is intended to catch cases where a species family
is emitted structurally but carries zero or contradictory signal relative to
the published source-share contract.

Cedar-pole CT validation lane
-----------------------------

After changing the canonical cedar-pole ``CT`` implementation, regenerate the
managed inputs, managed curves, and runtime package from this MKRF instance checkout after installing the instance package:

- ``mkrf-femic mkrf-build-managed-au-inputs --instance-root external\femic-mkrf-instance --resultant-gdb external\femic-mkrf-instance\data\source\03_MappingAnalysisData\Resultant.gdb``
- ``mkrf-femic mkrf-build-managed-au-curves --instance-root external\femic-mkrf-instance``
- ``mkrf-femic mkrf-init-runtime-package --instance-root external\femic-mkrf-instance``

Then validate the CT-specific runtime surface:

- ``femic patchworks preflight --instance-root external\femic-mkrf-instance --config config\patchworks.runtime.mkrf_rebuild.windows.yaml``
- ``femic patchworks matrix-build --instance-root external\femic-mkrf-instance --config config\patchworks.runtime.mkrf_rebuild.windows.yaml --run-id <ct-run-id>``
- ``femic patchworks run-default-scenario mkrf.base --run-id <ct-smoke-run-id>``
- ``mkrf-femic mkrf-audit-runtime-sanity --instance-root external\femic-mkrf-instance --stage-dir <saved-stage>``
- ``pytest tests/test_mkrf_managed.py tests/test_mkrf_runtime_package.py tests/test_tipsy_config.py``
- confirm ``models/mkrf_patchworks_model/xml/forestmodel.xml`` contains
  ``CT35``, ``CT40``, and ``CT45`` only for CT bucket treatments;
- confirm no active ``CT50`` / ``thn050`` or older ``CT150`` / ``thn150``
  behavior remains;
- inspect ``models/mkrf_patchworks_model/analysis/ct_eligibility_audit.csv``;
  and
- inspect ``models/mkrf_patchworks_model/analysis/ct_intensity_summary.csv``.

AU stratification validation lane
---------------------------------

After changing MKRF AU stratification, aggregation, or selected-AU publication
logic, regenerate the AU and runtime surfaces from the parent FEMIC checkout
using the project virtual environment:

- ``mkrf-femic mkrf-build-au-inputs --instance-root external\femic-mkrf-instance --resultant-gdb external\femic-mkrf-instance\data\source\03_MappingAnalysisData\Resultant.gdb``
- ``mkrf-femic mkrf-select-aus --instance-root external\femic-mkrf-instance``
- ``mkrf-femic mkrf-build-managed-au-inputs --instance-root external\femic-mkrf-instance --resultant-gdb external\femic-mkrf-instance\data\source\03_MappingAnalysisData\Resultant.gdb``
- ``mkrf-femic mkrf-build-managed-au-curves --instance-root external\femic-mkrf-instance --run-id <run-id>``
- ``mkrf-femic mkrf-init-runtime-package --instance-root external\femic-mkrf-instance``

Then validate the regenerated runtime:

- ``femic patchworks preflight --instance-root external\femic-mkrf-instance --config config\patchworks.runtime.mkrf_rebuild.windows.yaml``
- ``femic patchworks matrix-build --instance-root external\femic-mkrf-instance --config config\patchworks.runtime.mkrf_rebuild.windows.yaml --run-id <matrix-run-id>``
- ``femic patchworks run-default-scenario mkrf.base --run-id <smoke-run-id>``
- ``mkrf-femic mkrf-audit-runtime-sanity --instance-root external\femic-mkrf-instance --stage-dir <saved-stage>``
- ``pytest tests/test_mkrf_au.py tests/test_mkrf_managed.py tests/test_mkrf_runtime_package.py``
- inspect ``data/model_input_bundle/au_aggregation_audit.csv`` and
  ``data/model_input_bundle/selected_au_table.csv`` directly;
- confirm no raw AU ids intended only as aggregation sources remain in the
  selected AU table; and
- confirm runtime status, XML contract counts, and Matrix Builder outputs agree
  with the regenerated selected AU count.

What Still Belongs To The Later Rebuild
---------------------------------------

The following items remain intentionally outside the current canonical QA
contract:

- full target-helper reconstruction;
- unexplained legacy seams such as ``THLB4070(...)`` and ``UWR(...)``;
- exact compiled-curve parity; and
- a source-faithful control/entrypoint rebuild claim.

Why This Separation Matters
---------------------------

If the team treats benchmark/reference evidence as though it were already the
canonical rebuild contract, it will overfit the MKRF rebuild to the older
compiled package and its unexplained seams.

The retained PoC lane should instead provide:

- a runnable benchmark package;
- accepted benchmark comparison surfaces;
- operator-facing explanation of what the PoC does and does not prove; and
- preserved evidence for the next rebuild phase to evaluate critically.

The canonical closeout phase should decide:

- what architecture to keep from the PoC because it is justified;
- what legacy behavior to re-implement because source evidence or benchmark
  necessity requires it; and
- what legacy seams to leave behind because they are not part of the desired
  FEMIC-native structure.

