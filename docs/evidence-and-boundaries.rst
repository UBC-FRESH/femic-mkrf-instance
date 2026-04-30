Evidence and Boundaries
=======================

Accepted Evidence Surfaces
--------------------------

The current MKRF PoC lane relies on:

- generated runtime XML and tracks under
  ``models/mkrf_patchworks_model_poc/``;
- accepted compiled spatial runtime evidence;
- workbook-reviewed contract translations under
  ``config/legacy_xml_builder/``; and
- archival legacy compiled-package evidence under ``data/legacy_mkrf/``.

Accepted Runtime Package Surface
--------------------------------

The current accepted runnable package is the PoC package root:

- ``models/mkrf_patchworks_model_poc/``

The operator-important sub-surfaces inside that package are:

- runtime PIN / launch surface:
  ``models/mkrf_patchworks_model_poc/analysis/base.pin``
- generated runtime XML:
  ``models/mkrf_patchworks_model_poc/XML/baseMKRF.xml``
- generated runtime tracks:
  ``models/mkrf_patchworks_model_poc/Tracks/*.csv``
- accepted runtime spatial lane:
  ``models/mkrf_patchworks_model_poc/Spatial/fragments.*`` and
  ``models/mkrf_patchworks_model_poc/Spatial/topo_frag100.csv``
- checkpoint target-control lane used by the PoC operator surface:
  ``models/mkrf_patchworks_model_poc/analysis/initialTargetSummary.csv`` and
  ``models/mkrf_patchworks_model_poc/analysis/initialTargetStatus.csv``

These are the surfaces a user/operator should treat as the current PoC runtime
package. They are the right place to look when the question is "what does the
current FEMIC-managed MKRF package actually run with?"

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

- ``models/mkrf_patchworks_model_poc/``

The current claim boundary is:

- minimally runnable PoC benchmark/intermediate

The current claim boundary is not:

- source-faithful rebuild
- exact legacy-equivalence
- final canonical MKRF model architecture

The practical reading is:

- the PoC preserves enough of the legacy compiled/runtime contract to benchmark
  and reason about model behavior;
- the current generated XML/tracks plus accepted spatial lane are the active
  PoC runtime surface;
- the later from-scratch rebuild must still start from the reviewed upstream
  source lane and does not get to claim source-faithful status merely because
  the PoC is runnable.

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

Treat the following as belonging to the later canonical rebuild contract
instead:

- source-faithful raw-input reconstruction from ``03_MappingAnalysisData/*``;
- final target/control architecture decisions;
- any future canonical runtime package path distinct from the PoC package; and
- any stronger claim of identity with the original legacy model than the
  accepted PoC benchmark claim.

That distinction is deliberate. The PoC lane is meant to preserve evidence,
runtime intuition, and benchmark leverage. It is not meant to lock the future
architecture in place.

Reference Runbooks
------------------

- ``runbooks/LEGACY_SOURCE_INPUT_PUBLICATION_BOUNDARY.md``
- ``runbooks/LEGACY_SOURCE_REPRODUCIBILITY_BOUNDARY.md``
- ``runbooks/LEGACY_RUNTIME_MODEL_LAYOUT.md``
- ``runbooks/LEGACY_RUNTIME_XML_EMISSION.md``
- ``runbooks/LEGACY_RUNTIME_TRACK_RECONCILIATION.md``
