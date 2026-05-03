Data Package Crosswalk
======================

Instance Role Split
-------------------

The current MKRF instance separates four evidence families:

- legacy compiled-package references under ``data/legacy_mkrf/``
- reviewed workbook-derived contracts under ``config/legacy_xml_builder/``
- machine-readable lineage/reconciliation ledgers under ``metadata/``
- the canonical rebuild runtime package under
  ``models/mkrf_patchworks_model/``
- the retained PoC benchmark/reference package under
  ``models/mkrf_patchworks_model_poc/``

This split reflects the current MKRF role split:

- legacy package material is preserved as evidence;
- reviewed builder translations are the editable contract lane;
- lineage metadata explains what each artifact can and cannot prove; and
- the canonical runtime package is the active rebuild/runtime surface, while
  the PoC package is retained for benchmark/reference comparison.

Legacy / PoC / Canonical Crosswalk
----------------------------------

Legacy compiled controls:

- ``data/legacy_mkrf/compiled_controls/``

Legacy compiled track evidence:

- ``data/legacy_mkrf/compiled_tracks/``

Legacy spatial runtime evidence:

- ``data/legacy_mkrf/compiled_spatial/``

Legacy generated XML evidence:

- ``data/legacy_mkrf/generated_xml/``

Current canonical runtime package:

- ``models/mkrf_patchworks_model/``

Current PoC benchmark/reference package:

- ``models/mkrf_patchworks_model_poc/``

How To Read That Crosswalk
--------------------------

The crosswalk is intentionally not a one-to-one "this legacy file became that
canonical file" story.

Instead:

- ``compiled_controls`` explains the original runtime/control seam;
- ``compiled_tracks`` and ``compiled_spatial`` explain the accepted benchmark
  evidence lane;
- ``generated_xml`` explains the legacy generated artifact side of the builder
  seam; and
- ``models/mkrf_patchworks_model`` is the active FEMIC-managed canonical
  rebuild runtime package; while
- ``models/mkrf_patchworks_model_poc`` remains the reconstructed benchmark/
  reference runtime package.

That is why the current instance can support both:

- source-faithful runtime/package claims for the canonical lane; and
- benchmark/reference claims for the retained PoC lane.

Boundary
--------

The archival legacy surfaces are evidence and comparison aids. The checked-in
canonical package is the current rebuild/runtime surface. The retained PoC
package is a benchmark/reference surface. These roles should not be blurred.

In particular:

- archival evidence tells us what existed and how the original model behaved;
- the canonical package tells us what FEMIC now emits, builds, and runs as the
  accepted rebuild lane;
- the PoC package tells us what benchmark/reference surface we are still
  comparing against; and
- the retained legacy-only control seams still sit outside the canonical claim
  boundary unless a later task explicitly reopens control-lane reconstruction.

For the archive-oriented reading of those same legacy surfaces, use:

- :doc:`legacy-archive-reference`
