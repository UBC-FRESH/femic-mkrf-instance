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

Legacy source and PoC benchmark CT behavior is:

- available on
  ``status in managed and oper in operable and ct eq 'Y' and not startswith(au,'t')``;
- minimum age ``40``;
- maximum age ``150``;
- uses the treatment ``retain="20"`` attribute, which acts here as a 20-year
  post-treatment re-entry lock for automated scheduling; and
- transitions to a thinned AU lane via ``au = 'thn_' + au``.

That legacy/PoC contract uses a constant proportional commercial-thinning
split:

- treatment-year extracted harvest/product signal = ``0.4 * base curve``; and
- post-thin standing THN signal for later ages = ``0.6 * base curve(x)``.

This is not a constant absolute gap model of the form
``f(x) - 0.4 * f(x_ct)``.

The canonical rebuild no longer uses that legacy/PoC proportional-gap rule as
its active target behavior. It is retained as benchmark/reference only.

Canonical ``CT`` behavior now uses a bucketed constant-absolute-gap design
intended for release line ``v0.0.2a1``:

- available on
  ``status in managed and oper in operable and ct eq 'Y' and not startswith(au,'thn')``;
- uses 10-year midpoint CT buckets rather than one continuous-age treatment:

  - ``CT40`` for ages ``35-44``
  - ``CT50`` for ages ``45-54``
  - ``CT60`` for ages ``55-64``
  - continuing in the same pattern through ``CT150`` for ages ``145-154``

- keeps the treatment ``retain="20"`` attribute as the same 20-year
  post-treatment scheduling lock; and
- after treatment, the post-treatment stratum is rewritten as follows, using
  the bucket-specific thinned lane:

  - ``CT40`` -> ``au = 'thn040_' + au``
  - ``CT50`` -> ``au = 'thn050_' + au``
  - and so on through the full bucket family.

Unlike ``CC``, ``CT`` does not reset origin. It preserves the current natural
or treated origin lane and marks THN from the thinned AU identity.

Why the canonical lane is bucketed
----------------------------------

The desired CT response depends on treatment age. Patchworks ForestModel XML
does not provide a clean generic way to persist arbitrary ``x_ct`` into
post-treatment state for later curve evaluation.

The canonical workaround is therefore to discretize CT into a finite family of
treatments and precompile the response for each bucket anchor age. That keeps
the runtime XML legal and auditable while still moving away from the old
proportional-gap approximation.

Current Thinning Yield Logic
----------------------------

The canonical runtime now uses bucket-anchored extracted and residual curves.

For each CT bucket with midpoint anchor ``x_ct``:

- treatment-year CT harvested product =
  ``0.4 * base_curve(x_ct)``
- post-CT THN standing yield for later ages =
  ``max(0, base_curve(x) - 0.4 * base_curve(x_ct))``

That means:

- the extracted CT volume is constant within the bucket and anchored to the
  bucket midpoint age;
- the post-CT standing lane carries a constant absolute gap rather than a
  constant proportional gap; and
- ``CC`` from the thinned lane harvests the residual standing curve, not the
  untreated base curve.

Representative rebuilt track evidence from the canonical runtime package shows
the intended arithmetic:

- ``CT40`` example:

  - base standing at age ``100`` = ``764.8``
  - ``CT40`` extracted volume = ``73.64``
  - ``thn040`` standing at age ``100`` = ``691.16``
  - ``73.64 + 691.16 = 764.8``

- ``CT100`` example:

  - base standing at age ``120`` = ``895.3``
  - ``CT100`` extracted volume = ``305.92``
  - ``thn100`` standing at age ``120`` = ``589.38``
  - ``305.92 + 589.38 = 895.3``

Those checks are why the canonical docs now describe CT as a bucketed
constant-absolute-gap model rather than the older legacy proportional-gap
contract.

State Families
--------------

The canonical runtime publishes the familiar state-family surface:

- ``EM``
- ``EN``
- ``FM``
- ``THN``

In the current canonical lane:

- ``THN`` is driven from the explicit post-``CT`` ``thn_`` AU lane;
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
- ``data/legacy_mkrf/generated_xml/baseMKRF.xml``
- ``models/mkrf_patchworks_model_poc/XML/baseMKRF.xml``

Where To Read Next
------------------

- :doc:`analysis-units-and-yield-curves` for how inventory records map into AUs
  and then onto natural/treated yield curves
- :doc:`yield-curve-comparisons` for the current treated TIPSY-vs-VDYP figure
  gallery
- :doc:`metadata-and-lineage` for the audit surfaces behind runtime AU remap
  and species-share publication
