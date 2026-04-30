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

This split reflects the way the PoC is meant to be used:

- legacy package material is preserved as evidence;
- reviewed builder translations are the editable contract lane;
- lineage metadata explains what each artifact can and cannot prove; and
- the PoC runtime package is the current runnable benchmark surface.

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

How To Read That Crosswalk
--------------------------

The crosswalk is intentionally not a one-to-one "this legacy file became that
PoC file" story.

Instead:

- ``compiled_controls`` explains the original runtime/control seam;
- ``compiled_tracks`` and ``compiled_spatial`` explain the accepted benchmark
  evidence lane;
- ``generated_xml`` explains the legacy generated artifact side of the builder
  seam; and
- ``models/mkrf_patchworks_model_poc`` is the reconstructed FEMIC-managed
  runtime package that now stands in for the runnable benchmark surface.

That is why the current instance can support benchmark and runtime claims
without yet claiming a source-faithful rebuild from raw mapping inputs.

Boundary
--------

The archival legacy surfaces are evidence and comparison aids. The checked-in
PoC package is the current runnable benchmark surface. Neither should be
confused with the later source-faithful from-scratch rebuild lane.

In particular:

- archival evidence tells us what existed and how the original model behaved;
- the PoC package tells us what FEMIC can currently emit, build, and run; and
- the future rebuild lane is the only place where raw-source reproduction
  should become the main claim surface.
