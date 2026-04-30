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

Reference Runbooks
------------------

- ``runbooks/LEGACY_SOURCE_INPUT_PUBLICATION_BOUNDARY.md``
- ``runbooks/LEGACY_SOURCE_REPRODUCIBILITY_BOUNDARY.md``
- ``runbooks/LEGACY_RUNTIME_MODEL_LAYOUT.md``
- ``runbooks/LEGACY_RUNTIME_XML_EMISSION.md``
- ``runbooks/LEGACY_RUNTIME_TRACK_RECONCILIATION.md``
