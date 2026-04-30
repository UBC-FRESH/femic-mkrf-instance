Data Package Crosswalk
======================

Instance Role Split
-------------------

The current MKRF instance separates four evidence families:

- legacy compiled-package references under ``data/legacy_mkrf/``
- reviewed workbook-derived contracts under ``config/legacy_xml_builder/``
- machine-readable lineage/reconciliation ledgers under ``metadata/``
- the current generated PoC runtime package under
  ``models/mkrf_patchworks_model_poc/``

Legacy to PoC Crosswalk
-----------------------

Legacy compiled controls:

- ``data/legacy_mkrf/compiled_controls/``

Legacy compiled track evidence:

- ``data/legacy_mkrf/compiled_tracks/``

Legacy spatial runtime evidence:

- ``data/legacy_mkrf/compiled_spatial/``

Legacy generated XML evidence:

- ``data/legacy_mkrf/generated_xml/``

Current PoC runtime package:

- ``models/mkrf_patchworks_model_poc/``

Boundary
--------

The archival legacy surfaces are evidence and comparison aids. The checked-in
PoC package is the current runnable benchmark surface. Neither should be
confused with the later source-faithful from-scratch rebuild lane.
