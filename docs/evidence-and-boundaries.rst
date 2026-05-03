Evidence and Boundaries
=======================

Accepted Evidence Surfaces
--------------------------

The current MKRF instance relies on two distinct evidence families:

- canonical rebuild runtime outputs under
  ``models/mkrf_patchworks_model/``;
- retained PoC benchmark/reference outputs under
  ``models/mkrf_patchworks_model_poc/``;
- accepted compiled spatial runtime evidence;
- workbook-reviewed contract translations under
  ``config/legacy_xml_builder/``; and
- archival legacy compiled-package evidence under ``data/legacy_mkrf/``.

Accepted Runtime Package Surface
--------------------------------

The current accepted canonical runtime package is:

- ``models/mkrf_patchworks_model/``

The retained benchmark/reference package is:

- ``models/mkrf_patchworks_model_poc/``

The operator-important sub-surfaces inside the canonical package are:

- generated runtime XML:
  ``models/mkrf_patchworks_model/xml/forestmodel.xml``
- generated runtime tracks:
  ``models/mkrf_patchworks_model/tracks/*.csv``
- canonical runtime spatial lane:
  ``models/mkrf_patchworks_model/spatial/fragments.*``

The retained operator-important benchmark/reference sub-surfaces inside the PoC
package are:

- runtime PIN / launch surface:
  ``models/mkrf_patchworks_model_poc/analysis/base.pin``
- checkpoint target-control lane used by the PoC operator surface:
  ``models/mkrf_patchworks_model_poc/analysis/initialTargetSummary.csv`` and
  ``models/mkrf_patchworks_model_poc/analysis/initialTargetStatus.csv``

These are the surfaces a user/operator should treat as:

- the current canonical rebuild runtime package; and
- the retained benchmark/reference control lane.

Legacy Analyst Boundary Context
-------------------------------

The original modeling notes are explicit that the baseline model was built from
an upstream resultant/data-preparation lane and then carried into a Patchworks
estate model. The land-base logic in those notes is still the most direct
statement of analyst intent for:

- productive forest land base versus THLB;
- exclusions for roads, non-forest, reserves, and riparian areas;
- low-operability retention;
- and the future roads/trails/landings reduction logic.

Primary legacy narrative reference:

- :download:`reference/MKRF_Modeling_Notes.pdf`

In particular, the legacy notes document:

- a low-operability retention rule of ``20%``;
- wildlife tree patch retention of ``10%`` in Operable areas and ``20%`` in Low
  Operability areas; and
- a ``2.7%`` future roads/trails/landings netdown based on the developed THLB.

Those are legacy analyst assumptions that the PoC preserves as benchmark
context, not newly invented FEMIC behavior.

Important Boundaries
--------------------

Raw source:

- ``03_MappingAnalysisData/*``

Compiled runtime evidence:

- ``data/legacy_mkrf/compiled_spatial/``
- ``data/legacy_mkrf/compiled_tracks/``
- ``models/mkrf_patchworks_model_poc/Spatial/``
- ``models/mkrf_patchworks_model_poc/Tracks/``

Generated runtime package:

- ``models/mkrf_patchworks_model/``
- ``models/mkrf_patchworks_model_poc/``

The current claim boundary is:

- source-faithful canonical runtime/package rebuild plus accepted
  benchmark/reference comparison boundaries

The current claim boundary is not:

- exact legacy-equivalence
- source-faithful reconstruction of the control/entrypoint helper lane

The practical reading is:

- the canonical package is now the active MKRF runtime/package surface;
- the PoC preserves enough of the older compiled/runtime contract to benchmark
  and reason about model behavior; and
- the retained PoC control lane does not become a canonical rebuild claim just
  because it remains useful for benchmark/reference comparison.

Benchmark/Reference Evidence vs. Canonical Rebuild Contract
-----------------------------------------------------------

For the current MKRF docs lane, treat the following as benchmark/reference
evidence:

- archival legacy compiled package surfaces under ``data/legacy_mkrf/``;
- the current PoC runtime package under
  ``models/mkrf_patchworks_model_poc/``;
- the accepted benchmark saved stage and report-pair KPI surface; and
- the reviewed workbook/builder translations that explain the current PoC
  emission/runtime contract.

Treat the following as belonging to the active canonical rebuild contract:

- source-faithful raw-input reconstruction from ``03_MappingAnalysisData/*``;
- canonical runtime package generation under
  ``models/mkrf_patchworks_model/``; and
- accepted runtime-surface parity against the PoC benchmark package.

For the explicit repo-local archive guide to ``data/legacy_mkrf/``, use:

- :doc:`legacy-archive-reference`

Accepted Legacy-Only Control Seams
----------------------------------

The following control seams remain accepted legacy-only benchmark/reference
evidence unless a later task explicitly reopens source-faithful control-lane
rebuild:

- ``THLB4070(...)``
- ``UWR(...)``
- ``InitialTargets/00_Target_Descriptions.bsh``

Handoff to the Canonical Rebuild
--------------------------------

The next architecture-defining work is closeout of the canonical rebuild claim
boundary under parent issue ``#173`` and FEMIC roadmap Phase 60.

That closeout lane should inherit the retained PoC docs/control surfaces only
as:

- benchmark/reference evidence;
- a record of accepted PoC variances;
- a runtime/operator baseline for comparison; and
- a checklist of seams that still require source-faithful replacement.

It should not reinterpret the retained PoC control lane as part of the
canonical source-faithful claim boundary by default.

Reference Runbooks
------------------

- ``runbooks/LEGACY_SOURCE_INPUT_PUBLICATION_BOUNDARY.md``
- ``runbooks/LEGACY_SOURCE_REPRODUCIBILITY_BOUNDARY.md``
- ``runbooks/LEGACY_RUNTIME_MODEL_LAYOUT.md``
- ``runbooks/LEGACY_RUNTIME_XML_EMISSION.md``
- ``runbooks/LEGACY_RUNTIME_TRACK_RECONCILIATION.md``
