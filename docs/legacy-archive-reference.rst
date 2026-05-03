Legacy Archive Reference
========================

Purpose
-------

``data/legacy_mkrf/`` is the repo-local archival lane for the full legacy MKRF
Patchworks package currently retained in ``femic-mkrf-instance``.

This lane exists so later developers can inspect the historical package
directly inside the instance repo when adjudicating canonical rebuild behavior.
It is not the active runtime surface.

Role Split
----------

Treat the three MKRF package families this way:

- legacy archive under ``data/legacy_mkrf/``:
  archival/reference only
- PoC package under ``models/mkrf_patchworks_model_poc/``:
  retained benchmark/reference runtime package
- canonical package under ``models/mkrf_patchworks_model/``:
  active runtime/operator lane

Do not repoint runtime defaults, docs defaults, or release claims back to the
legacy archive.

Archive Contents
----------------

The retained legacy package families currently present are:

- compiled controls:
  ``data/legacy_mkrf/compiled_controls/``
- compiled tracks:
  ``data/legacy_mkrf/compiled_tracks/``
- compiled spatial runtime:
  ``data/legacy_mkrf/compiled_spatial/``
- generated XML review artifacts:
  ``data/legacy_mkrf/generated_xml/``

More specifically:

- entrypoint/control surfaces:
  ``compiled_controls/entrypoints/baseMKRF.pin``,
  ``compiled_controls/entrypoints/ScenarioSet.bsh``,
  ``compiled_controls/entrypoints/runME.bsh``
- legacy script and target families:
  ``compiled_controls/scripts/*.bsh`` and
  ``compiled_controls/targets/*.bsh``
- compiled matrix/runtime tables:
  ``compiled_tracks/*.csv``
- spatial runtime evidence:
  ``compiled_spatial/fragments.*`` and
  ``compiled_spatial/topo_frag100.csv``
- generated XML evidence:
  ``generated_xml/baseMKRF.xml`` and
  ``generated_xml/CSV/CURVE_TABLE.csv``

How To Use The Archive
----------------------

Use the legacy archive when the question is historical or comparative, for
example:

- what the stable legacy compiled package contained;
- what the legacy XML emitted for a treatment or attribute;
- what compiled track/control surfaces existed in the historical package; or
- whether a canonical behavior was inherited from legacy evidence or introduced
  by FEMIC-owned rebuild logic.

Use the canonical lane instead when the question is operational, for example:

- what package operators should launch today;
- what current releases claim to ship;
- what runtime package should be rebuilt or validated; or
- what docs should teach as the active model.

Reading Order
-------------

For legacy-package inspection, the most useful supporting pages are:

- :doc:`data-package-crosswalk`
- :doc:`evidence-and-boundaries`
- :doc:`metadata-and-lineage`

For the active operator/runtime lane, use:

- :doc:`model-anatomy`
- :doc:`treatments-and-state-logic`
- :doc:`operator-runbook`

Publication Boundary
--------------------

The archive is intentionally first-class and local to the instance repo, but it
still has a strict boundary:

- it is present for record, traceability, and comparative debugging;
- it is not the authoritative editable-source lane;
- it is not the active runtime package; and
- it is not the package shipped as the canonical MKRF release surface.
