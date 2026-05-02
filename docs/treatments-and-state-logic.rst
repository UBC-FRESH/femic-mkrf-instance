Treatments and State Logic
==========================

Purpose
-------

This page explains the current canonical MKRF treatment and state logic for the
active runtime/package lane under ``models/mkrf_patchworks_model/``.

Use this page when you need to answer questions such as:

- what ``managed`` and ``unmanaged`` mean in Patchworks for this model;
- what ``natural`` and ``treated`` mean in the canonical yield lane;
- whether the canonical model includes both ``CC`` and ``CT``; and
- how ``EM``, ``EN``, ``FM``, and ``THN`` are used in the current runtime.

Canonical Semantic Split
------------------------

The canonical MKRF rebuild treats these concepts separately:

- ``managed`` / ``unmanaged`` means treatment eligibility only;
- ``natural`` / ``treated`` means yield-curve provenance only; and
- the ``<retention>`` XML element may move area from managed to unmanaged
  without changing origin.

For this instance, origin is currently classified from the reviewed 2020 age
rule:

- ``AGE_2020 >= 80`` -> ``natural``
- ``AGE_2020 < 80`` -> ``treated``

Do not read first-growth curve availability as a proxy for management state in
the canonical lane.

Canonical Treatment Surface
---------------------------

The current canonical runtime defines both ``CC`` and ``CT`` in:

- ``models/mkrf_patchworks_model/xml/forestmodel.xml``

The corresponding generated Patchworks operator/control surface is:

- ``models/mkrf_patchworks_model/analysis/base.pin``

Clearcut (``CC``)
-----------------

Canonical ``CC`` behavior is:

- available on ``status in managed``;
- minimum age is ``if(oper in operable, 60, 150)``; and
- after treatment, the post-treatment stratum is rewritten as follows:

  - ``au = auf``: use the post-treatment AU for subsequent lookup;
  - ``origin = treated``: move regenerated area onto the treated-origin yield
    lane; and
  - ``statecode = FM``: mark the post-clearcut managed state.

This means ``CC`` is the regeneration event that explicitly moves post-harvest
area onto the treated-origin yield lane.

Commercial Thinning (``CT``)
----------------------------

Canonical ``CT`` behavior is:

- available on
  ``status in managed and oper in operable and ct eq 'Y' and statecode ne 'THN'``;
- minimum age ``40``;
- maximum age ``150``;
- uses the treatment ``retain="20"`` attribute, which acts here as a 20-year
  post-treatment re-entry lock for automated scheduling; and
- after treatment, the post-treatment stratum is rewritten as follows:

  - ``au = auf``: use the post-treatment AU for subsequent lookup; and
  - ``statecode = THN``: mark the area as being in the thinned state.

Unlike ``CC``, the current ``CT`` transition does not reset origin. It leaves
the stand on the same canonical AU and marks the post-treatment state as
thinned.

Current Thinning Yield Logic
----------------------------

The canonical runtime currently uses a simple thinning factor in the generated
yield/product logic:

- ``if(treatment eq 'CT' or statecode eq 'THN', 0.6, 1)``

That factor is applied to the active origin-driven yield lane, so the thinning
adjustment is separate from the natural-versus-treated curve choice.

State Families
--------------

The canonical runtime publishes the familiar state-family surface:

- ``EM``
- ``EN``
- ``FM``
- ``THN``

In the current canonical lane:

- ``THN`` is the explicit post-``CT`` thinned state;
- ``FM`` is the post-``CC`` managed treated state; and
- the remaining non-``THN`` states are derived from explicit origin and runtime
  state semantics rather than from first-growth-curve availability.

The important rule is that these state labels sit on top of the explicit
``managed/unmanaged`` and ``natural/treated`` contracts; they do not replace
them.

Current GUI Treatment Layers
----------------------------

The canonical ``base.pin`` now includes GUI map layers for:

- default blocks;
- current treatments via ``CURRENTTREATMENT``; and
- latest treatments via ``LASTTREATMENT``.

It also includes guarded patch themes when patch displays are enabled.

Primary evidence surfaces:

- ``models/mkrf_patchworks_model/analysis/base.pin``
- ``models/mkrf_patchworks_model/xml/forestmodel.xml``

Where To Read Next
------------------

- :doc:`analysis-units-and-yield-curves` for how inventory records map into AUs
  and then onto natural/treated yield curves
- :doc:`yield-curve-comparisons` for the current treated TIPSY-vs-VDYP figure
  gallery
- :doc:`metadata-and-lineage` for the audit surfaces behind runtime AU remap
  and species-share publication
