Model Anatomy
=============

Directory Map
-------------

- ``config/``: rebuild spec, runtime config, run profile, and legacy XML-builder
  contract surfaces
- ``data/legacy_mkrf/``: archival compiled controls, tracks, spatial runtime,
  and generated XML evidence
- ``metadata/``: machine-readable lineage, reconciliation, and boundary ledgers
- ``models/mkrf_patchworks_model_poc/``: current PoC benchmark Patchworks
  package
- ``runbooks/``: operator-facing reconstruction and runtime notes
- ``runtime/logs/``: local smoke-test and headless runtime artifacts

Legacy Structural Logic
-----------------------

The original MKRF modeling notes describe a fairly conventional strategic
forest-estate structure:

- land-base/resultant preparation first;
- analysis-unit definition second;
- growth-and-yield assignment after that; and
- Patchworks heuristic scheduling and reporting on top of those prepared
  surfaces.

The current PoC instance mirrors that structure at a different level of
materialization:

- upstream/raw geometry and yield-prep evidence remain outside the current PoC
  runtime package;
- reviewed contract surfaces live in ``config/legacy_xml_builder/``;
- the generated runtime package lives under
  ``models/mkrf_patchworks_model_poc/``; and
- lineage/reconciliation evidence lives under ``metadata/`` and ``runbooks/``.

PoC Package Layout
------------------

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
- ``config/patchworks.runtime.windows.yaml``
- ``config/legacy_xml_builder/*.yaml``
- ``runbooks/*.md``
- ``metadata/*.yaml``

These editable surfaces are the current contract/source-of-truth lane for the
PoC package. They carry the reviewed interpretation of the workbook builder,
generated XML reconciliation, runtime-package layout, and claim boundaries.

Regenerate instead of hand-edit:

- ``models/mkrf_patchworks_model_poc/XML/baseMKRF.xml``
- ``models/mkrf_patchworks_model_poc/Tracks/*.csv``

That matches the original analyst model split reasonably well:

- builder/contract logic belongs in the editable-source lane;
- emitted XML and track tables belong in the generated runtime lane.

Use caution:

- ``models/mkrf_patchworks_model_poc/analysis/base.pin``
- ``models/mkrf_patchworks_model_poc/InitialTargets/00_Target_Descriptions.bsh``

Those runtime entrypoints are valid PoC/operator surfaces, but they are not the
final architecture contract for the later canonical rebuild.

Original Modeling Assumptions That Shape This Anatomy
-----------------------------------------------------

The legacy notes identify the main conceptual surfaces that still matter for the
PoC:

- land-base classes: total area, PFLB, THLB, long-term THLB;
- analysis units stratified by management era, site index, and BEC;
- natural-stand yields from VDYP;
- managed-stand yields from TIPSY;
- two silvicultural systems:
  - clearcut with reserves; and
  - CT followed by clearcut twenty years later;
- minimum harvest ages driven by operability and treatment type.

Those assumptions explain why the PoC package is centered on:

- stratification/constant contracts;
- emitted runtime XML;
- matrix-built tracks; and
- Patchworks runtime entrypoints.
