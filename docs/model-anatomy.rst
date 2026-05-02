Model Anatomy
=============

Directory Map
-------------

- ``config/``: rebuild spec, runtime config, run profile, and legacy XML-builder
  contract surfaces
- ``data/legacy_mkrf/``: archival compiled controls, tracks, spatial runtime,
  and generated XML evidence
- ``metadata/``: machine-readable lineage, reconciliation, and boundary ledgers
- ``models/mkrf_patchworks_model/``: active canonical runtime/package lane
- ``models/mkrf_patchworks_model_poc/``: retained PoC benchmark/reference
  package
- ``runbooks/``: operator-facing reconstruction and runtime notes
- ``runtime/logs/``: local smoke-test and headless runtime artifacts
- ``plots/``: checked-in strata and yield-curve QA/interpretation figures

Legacy Structural Logic
-----------------------

The original MKRF modeling notes describe a fairly conventional strategic
forest-estate structure:

- land-base/resultant preparation first;
- analysis-unit definition second;
- growth-and-yield assignment after that; and
- Patchworks heuristic scheduling and reporting on top of those prepared
  surfaces.

The current canonical instance mirrors that structure at a different level of
materialization:

- upstream/raw geometry and yield-prep evidence remain outside the checked-in
  runtime package;
- reviewed contract surfaces live in ``config/legacy_xml_builder/``;
- the active generated runtime package lives under
  ``models/mkrf_patchworks_model/``;
- the retained benchmark/reference package lives under
  ``models/mkrf_patchworks_model_poc/``; and
- lineage/reconciliation evidence lives under ``metadata/`` and ``runbooks/``.

Canonical Package Layout
------------------------

Inside ``models/mkrf_patchworks_model/``:

- ``analysis/``: canonical control lane, manifests, and rebuild audits
- ``initial_targets/``: currently thin placeholder surface kept in canonical
  layout
- ``scripts/``: canonical runtime support scripts
- ``spatial/``: source-faithful fragments runtime family
- ``tracks/``: Matrix-Builder-owned runtime tracks
- ``xml/``: FEMIC-emitted canonical runtime XML

The most important practical split is:

- ``analysis/`` and ``scripts/`` are the canonical runtime/operator entry
  surfaces;
- ``xml/`` and ``tracks/`` are the canonical generated runtime payloads; and
- ``spatial/`` is the checked-in source-faithful geometry handoff for the
  active release lane.

Retained PoC Package Layout
---------------------------

Inside ``models/mkrf_patchworks_model_poc/``:

- ``analysis/``: Patchworks PIN and checkpoint target-control files
- ``InitialTargets/``: current target-description seam
- ``Scripts/``: runtime control/report scripts
- ``Spatial/``: fragments and topology runtime family
- ``Tracks/``: compiled/generated Patchworks tracks
- ``XML/``: FEMIC-emitted runtime XML

The most important practical split is:

- ``analysis/`` and ``Scripts/`` are runtime/operator entry surfaces;
- ``XML/`` and ``Tracks/`` are generated contract/runtime payloads; and
- ``InitialTargets/`` is still a legacy-seam boundary, not a fully reconstructed
  final control architecture.

Editable vs Generated
---------------------

Safe to edit directly:

- ``config/rebuild.spec.yaml``
- ``config/rebuild.allowlist.yaml``
- ``config/patchworks.runtime.mkrf_rebuild.windows.yaml``
- ``config/legacy_xml_builder/*.yaml``
- ``runbooks/*.md``
- ``metadata/*.yaml``

These editable surfaces are the current contract/source-of-truth lane for the
canonical rebuild package. They carry the reviewed interpretation of the
workbook builder, runtime-package layout, semantic-repair rules, release
boundary, and retained benchmark evidence.

Regenerate instead of hand-edit:

- ``models/mkrf_patchworks_model/xml/forestmodel.xml``
- ``models/mkrf_patchworks_model/tracks/*.csv``
- ``models/mkrf_patchworks_model_poc/XML/baseMKRF.xml``
- ``models/mkrf_patchworks_model_poc/Tracks/*.csv``

That matches the original analyst model split reasonably well:

- builder/contract logic belongs in the editable-source lane;
- emitted XML and track tables belong in the generated runtime lane.

Use caution:

- ``models/mkrf_patchworks_model/analysis/base.pin``
- ``models/mkrf_patchworks_model_poc/analysis/base.pin``
- ``models/mkrf_patchworks_model_poc/InitialTargets/00_Target_Descriptions.bsh``

The canonical ``base.pin`` is a real operator/runtime surface for the current
release lane. The PoC runtime entrypoints remain valid benchmark/operator
surfaces, but they are not the active architecture contract for the canonical
release.

Logic References
----------------

This page is primarily about package anatomy, not detailed runtime behavior.

For the current canonical model logic, use:

- :doc:`treatments-and-state-logic` for ``CC``/``CT``, state families, and the
  managed/unmanaged versus natural/treated split; and
- :doc:`analysis-units-and-yield-curves` for the stratification -> AU ->
  selected-AU -> runtime remap/yield-curve mapping chain.

Original Modeling Assumptions That Shape This Anatomy
-----------------------------------------------------

The legacy notes identify the main conceptual surfaces that still matter for the
canonical rebuild and the retained PoC benchmark:

- land-base classes: total area, PFLB, THLB, long-term THLB;
- analysis units stratified by management era, site index, and BEC;
- natural-stand yields from VDYP;
- managed-stand yields from TIPSY;
- two silvicultural systems:
  - clearcut with reserves; and
  - CT followed by clearcut twenty years later;
- minimum harvest ages driven by operability and treatment type.

Those assumptions explain why the active canonical package is centered on:

- stratification/constant contracts;
- emitted runtime XML;
- matrix-built tracks; and
- Patchworks runtime entrypoints.

The retained PoC package still matters for benchmark/reference comparison, but
it is no longer the package this page is teaching as current.

Current figure references:

- treatment and AU/yield logic:
  :doc:`treatments-and-state-logic` and
  :doc:`analysis-units-and-yield-curves`
- student/operator-facing treated overlay gallery: :doc:`yield-curve-comparisons`
- broader strata and yield diagnostics appendix: :doc:`figure-appendix`
