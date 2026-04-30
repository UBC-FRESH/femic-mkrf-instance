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

PoC Package Layout
------------------

Inside ``models/mkrf_patchworks_model_poc/``:

- ``analysis/``: Patchworks PIN and checkpoint target-control files
- ``InitialTargets/``: current target-description seam
- ``Scripts/``: runtime control/report scripts
- ``Spatial/``: fragments and topology runtime family
- ``Tracks/``: compiled/generated Patchworks tracks
- ``XML/``: FEMIC-emitted runtime XML

Editable vs Generated
---------------------

Safe to edit directly:

- ``config/rebuild.spec.yaml``
- ``config/rebuild.allowlist.yaml``
- ``config/patchworks.runtime.windows.yaml``
- ``config/legacy_xml_builder/*.yaml``
- ``runbooks/*.md``
- ``metadata/*.yaml``

Regenerate instead of hand-edit:

- ``models/mkrf_patchworks_model_poc/XML/baseMKRF.xml``
- ``models/mkrf_patchworks_model_poc/Tracks/*.csv``

Use caution:

- ``models/mkrf_patchworks_model_poc/analysis/base.pin``
- ``models/mkrf_patchworks_model_poc/InitialTargets/00_Target_Descriptions.bsh``

Those runtime entrypoints are valid PoC/operator surfaces, but they are not the
final architecture contract for the later canonical rebuild.
