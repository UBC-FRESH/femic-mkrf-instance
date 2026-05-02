Getting Started
===============

Purpose
-------

``femic-mkrf-instance`` is the private standalone MKRF FEMIC instance used for:

- canonical runtime/package generation;
- legacy reverse-engineering and evidence retention;
- PoC benchmark/runtime comparison; and
- closeout of the from-scratch MKRF rebuild lane.

Original Legacy Model Intent
----------------------------

The original legacy MKRF model was prepared by Forsite for the University of
British Columbia Master of Sustainable Forest Management program as a baseline
GIS resultant and Patchworks forest estate model. Its stated purpose was to
support estimation of a sustainable harvest flow for Malcolm Knapp Research
Forest and to inform eventual annual allowable cut reconsideration.

The original legacy narrative is now carried in this private instance repo as:

- :download:`reference/MKRF_Modeling_Notes.pdf`

That framing still matters for the retained PoC/legacy evidence surfaces, but
the active FEMIC-hosted runtime package is now the canonical rebuild lane.

Current Runtime Surface
-----------------------

The active checked-in Patchworks package is:

- ``models/mkrf_patchworks_model/``

The retained benchmark/reference package is:

- ``models/mkrf_patchworks_model_poc/``

Use the canonical package for current runtime/package work. Use the PoC package
only for benchmark/reference comparison.

Quick Operator Surface
----------------------

Primary files:

- runtime config:
  ``config/patchworks.runtime.mkrf_rebuild.windows.yaml``
- runtime XML:
  ``models/mkrf_patchworks_model/xml/forestmodel.xml``
- runtime tracks:
  ``models/mkrf_patchworks_model/tracks/``
- spatial runtime:
  ``models/mkrf_patchworks_model/spatial/``
- retained benchmark/reference PIN:
  ``models/mkrf_patchworks_model_poc/analysis/base.pin``

Original Study Area and Legacy Baseline Context
-----------------------------------------------

The legacy notes describe MKRF as a volume-based private forest estate north of
Maple Ridge and adjacent to Golden Ears Provincial Park, overlapping the
Coastal Western Hemlock zone. The legacy baseline land-base summary used in the
original model was:

- gross area: ``5,126 ha``
- productive forest land base: ``4,811 ha``
- timber harvesting land base: ``4,121 ha``
- long-term THLB after WTP assumptions: ``3,653 ha``

Those numbers are useful orientation values for operators reading the retained
benchmark/reference materials and the canonical rebuild package.

Recommended first reads:

- ``README.md``
- ``runbooks/REBUILD_RUNBOOK.md``
- ``runbooks/LEGACY_RUNTIME_XML_EMISSION.md``
- ``runbooks/LEGACY_RUNTIME_TRACK_RECONCILIATION.md``

What This Guide Covers
----------------------

This guide documents the current MKRF instance surfaces:

- what the instance contains;
- how the canonical runtime package is wired;
- what benchmark/reference evidence was retained;
- what boundaries and caveats still exist; and
- how the canonical rebuild lane differs from the retained PoC package.

It does not treat the PoC package as the final canonical MKRF instance.

Read These First For Model Logic
--------------------------------

For the current canonical model behavior, start with:

- :doc:`treatments-and-state-logic`
- :doc:`analysis-units-and-yield-curves`

Those two pages explain the actual runtime logic behind:

- ``CC`` and ``CT``;
- managed/unmanaged versus natural/treated semantics;
- the selected top-N AU rule; and
- runtime AU remap/imputation for non-top-N strata.

Recommended figure surfaces:

- :doc:`yield-curve-comparisons` for the current treated TIPSY-vs-VDYP overlay
  gallery; and
- :doc:`figure-appendix` for the strata distribution plus the broader VDYP
  envelope and fit-diagnostic figure set.
