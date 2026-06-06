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

Canonical ``CT`` behavior now uses a cedar-pole commercial-thinning contract:

- available on
  ``status in managed and oper in operable and ct eq 'Y' and not startswith(au,'thn')``;
- further constrained to AUs with base planted Cw plus Fd share greater than
  or equal to ``50%``;
- relies on the current runtime CT/operability evidence as the ground-based
  treatment seam, with the provisional planning rule that CT is only active
  where slope is less than ``50%``;
- uses 5-year CT buckets over the ``35`` to ``50`` operability window,
  excluding age ``50``:

  - ``CT35`` for ages ``35-39``
  - ``CT40`` for ages ``40-44``
  - ``CT45`` for ages ``45-49``

- keeps the treatment ``retain="20"`` attribute as the same 20-year
  post-treatment scheduling lock; and
- after treatment, the post-treatment stratum is rewritten as follows, using
  the bucket-specific thinned lane:

  - ``CT35`` -> ``au = 'thn035_' + au``
  - ``CT40`` -> ``au = 'thn040_' + au``
  - ``CT45`` -> ``au = 'thn045_' + au``.

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

- treatment-year CT harvested product is provisionally represented by the
  medium-intensity target of ``45%`` basal-area removal;
- post-CT THN standing yield for later ages =
  ``max(0, base_curve(x) - extracted_ct_bucket_gap)``.

That means:

- the extracted CT volume is constant within the bucket and anchored to the
  bucket midpoint age;
- the post-CT standing lane carries a constant absolute gap rather than a
  constant proportional gap; and
- ``CC`` from the thinned lane harvests the residual standing curve, not the
  untreated base curve.

The current published runtime keeps low/medium/high planning intensities in
the silviculture contract:

- low: ``35%`` basal-area removal;
- medium: ``45%`` basal-area removal; and
- high: ``55%`` basal-area removal.

The compiled package currently publishes the medium-intensity lane as the
active runtime surface. CT product species accounting is target-bounded and
Hw-first: Cw product volume is zero, Hw receives the CT product volume up to the
``45%`` medium removal target, and Fd receives only any target balance not met
by Hw. This retains Cw first, then Fd, while still allowing Fd-leading and pure
Fd plantations to receive CT when they pass the combined Cw/Fd eligibility
criterion. The residual-state and cedar pole response rules remain documented
calibration assumptions until local CT response curves are available.

Representative rebuilt track evidence from the canonical runtime package shows
the constant-gap arithmetic:

- ``CT40`` example:

  - base standing at age ``100`` = ``764.8``
  - ``CT40`` extracted volume = ``73.64``
  - ``thn040`` standing at age ``100`` = ``691.16``
  - ``73.64 + 691.16 = 764.8``

The eligibility filter is recorded in
``models/mkrf_patchworks_model/analysis/ct_eligibility_audit.csv``. That table
shows each selected AU's base Cw, Fd, and combined Cw/Fd share; whether it
passed the inclusive ``>=50%`` Cw/Fd threshold; and whether it passed the
current runtime CT/operability seam.
The implemented CT product split is recorded in
``models/mkrf_patchworks_model/analysis/ct_intensity_audit.csv`` and summarized
in ``models/mkrf_patchworks_model/analysis/ct_intensity_summary.csv``.

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
