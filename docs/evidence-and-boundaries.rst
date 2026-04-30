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
- the later from-scratch rebuild must still start from the reviewed upstream
  source lane and does not get to claim source-faithful status merely because
  the PoC is runnable.

Reference Runbooks
------------------

- ``runbooks/LEGACY_SOURCE_INPUT_PUBLICATION_BOUNDARY.md``
- ``runbooks/LEGACY_SOURCE_REPRODUCIBILITY_BOUNDARY.md``
- ``runbooks/LEGACY_RUNTIME_MODEL_LAYOUT.md``
- ``runbooks/LEGACY_RUNTIME_XML_EMISSION.md``
- ``runbooks/LEGACY_RUNTIME_TRACK_RECONCILIATION.md``
