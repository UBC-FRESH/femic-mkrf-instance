Analysis Units and Yield Curves
===============================

Purpose
-------

This page explains how the canonical MKRF rebuild moves from inventory-derived
strata into analysis units (AUs), how the selected top-N AU subset is used, and
how natural and treated yield curves are mapped to those AUs at runtime.

Use this page when you need to answer questions such as:

- how inventory/fragment surfaces become canonical MKRF AUs;
- why only a selected top-N AU subset gets its own published canonical curve
  lane;
- what happens to non-top-N strata/AUs; and
- how the canonical runtime chooses between natural and treated yield curves.

Stratification Chain
--------------------

The current canonical chain is:

1. source inventory/fragment evidence;
2. AU construction from BEC plus ordered top-2 leading species;
3. selected top-N AU publication by cumulative covered area;
4. natural-origin and treated-origin curve publication on the selected AU set;
   and
5. runtime AU normalization/remap of non-selected raw AUs onto that canonical
   selected set.

The main checked-in evidence surfaces are:

- ``data/model_input_bundle/selected_au_table.csv``
- ``data/model_input_bundle/stand_au_assignment.csv``
- ``data/model_input_bundle/stand_origin_assignment.csv``
- ``models/mkrf_patchworks_model/analysis/runtime_au_remap_audit.csv``
- ``models/mkrf_patchworks_model/xml/forestmodel.xml``

Selected Top-N AU Rule
----------------------

The canonical rebuild publishes a selected AU subset rather than carrying the
full raw AU universe as independent runtime curve families.

Current rule:

- selected AUs come from ``selected_au_table.csv``;
- they are ordered by cumulative covered area; and
- the current target is the published ``95%`` covered-area subset.

That selected subset is the canonical AU universe for the runtime package.

Yield-Curve Mapping
-------------------

The canonical runtime maps yield provenance by origin:

- natural-origin area uses the natural/VDYP lane; and
- treated-origin area uses the treated/TIPSY lane.

Both lanes are keyed by canonical AU id. The runtime therefore needs two
separate questions answered:

1. what canonical AU should this area use? and
2. should that area read from the natural or treated curve family?

Those are separate decisions in the canonical lane.

Natural and Treated Source Surfaces
-----------------------------------

The main data surfaces behind those choices are:

- ``stand_origin_assignment.csv``:
  answers which origin class a source stand/forest-cover id was assigned
  (natural or treated)
- ``stand_au_assignment.csv``:
  answers which raw AU the stand evidence most strongly supports
- ``selected_au_table.csv``:
  answers which AUs were retained in the canonical selected set

The generated runtime then emits canonical AU and origin lookups into:

- ``models/mkrf_patchworks_model/xml/forestmodel.xml``

Non-Top-N AU Remap / Imputation
-------------------------------

The current canonical rebuild does have non-top-N AU imputation logic.

It is implemented as runtime AU normalization/remap onto the selected canonical
AU set, not as a second independent curve-fitting lane for every dropped AU.

Current behavior:

- raw non-selected AUs are remapped onto the selected canonical AU set at
  runtime;
- remap scoring prefers:
  - same BEC;
  - same primary species;
  - stronger runtime coverage; and
  - then selected rank; and
- the authoritative audit is:
  ``models/mkrf_patchworks_model/analysis/runtime_au_remap_audit.csv``

So the correct reading is:

- non-top-N strata do not each carry their own published canonical yield-curve
  family;
- instead, they are normalized onto the selected canonical AU universe before
  runtime yield lookup.

What The Audit Surfaces Answer
------------------------------

Use these files to answer different questions:

- ``data/model_input_bundle/stand_au_assignment.csv``:
  what raw AU did the stand evidence support?
- ``data/model_input_bundle/stand_origin_assignment.csv``:
  what origin class was assigned?
- ``models/mkrf_patchworks_model/analysis/runtime_au_remap_audit.csv``:
  what canonical selected AU did runtime actually use after normalization?
- ``models/mkrf_patchworks_model/analysis/runtime_species_share_audit.csv``:
  what species-share surface was published for that canonical AU and origin
  lane?

Figure Surfaces
---------------

For visual interpretation of the published curve families, use:

- :doc:`yield-curve-comparisons` for treated TIPSY-vs-VDYP overlays
- :doc:`figure-appendix` for strata distribution, VDYP envelopes, and selected
  fit diagnostics

Those figures are aids for interpreting the selected canonical AU families.
They do not imply that every raw non-top-N AU has its own separate published
curve family.
