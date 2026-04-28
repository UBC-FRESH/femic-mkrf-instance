# MKRF Legacy Input Variables Translation

This note records the first live FEMIC-native translation of the legacy MKRF
workbook `Input Variables` surface.

## What is live now

The translated config at `config/legacy_xml_builder/input_variables.mkrf.yaml`
is now wired into Patchworks export as an **opt-in** input surface.

Live exporter fields:

- `description`
  drives ForestModel `description`
- `start_year`
  drives ForestModel `year`
- `horizon_years`
  drives ForestModel `horizon`
- `staged.exclude_expression`
  drives ForestModel `input.exclude`
- `staged.unique_record_label_expression`
  drives ForestModel `input.block` and exported fragments `BLOCK`
- `staged.polygon_area_expression`
  drives ForestModel `input.area` and exported fragments `AREA_HA`
- `staged.stand_age_expression`
  drives ForestModel `input.age` and exported fragments `F_AGE`
- `staged.additional_stratification_columns`
  drive exported fragments `status`, `au_1`, `auf`, `oper`, `ct`, and `aux`
- `staged.treatment_eligibility_expression`
  drives exported fragments `treat_inel` as `Y` when true and `N` when false
- `staged.constant_contract`
  controls which translated matrix-builder constants are available as live
  legacy expression symbols

These workbook-derived values now affect exporter behavior in this slice.
When the live expressions reference checkpoint source columns such as
`RES_KEY`, `AGE_2020`, or `CONTCLAS`, those columns must be present in the
checkpoint and are passed through into the exported fragments surface.
The live additional-stratification bindings use the same rule. The workbook
key `au` is written as fragment field `au_1` so it does not collide with the
base required `AU` fragments field that already exists in the Patchworks
fragments schema. The live treatment-eligibility seam is currently narrower
than the legacy SPS XML builder: it evaluates the workbook expression against
the live additional stratification bindings plus constants allowed by
`staged.constant_contract` and writes the result to the review field
`treat_inel`.
The live constants contract currently exposes only scalar legacy values:
`managed`, `unmanaged`, `operable`, and `lowoper`. Formula-like workbook values
such as `frd` remain preserved but deferred, so they cannot silently become
live expression inputs before a builder consumer is identified.

## What remains inactive

The translated config also preserves legacy workbook seams that are **not yet
live**:

- `max_inventory_age`
  preserved as review metadata; the current exporter derives curve evaluation
  spans from `horizon_years` and source curve ages
- `before_curves`
  blocked because the workbook value points at generated `Curves.xml`; this
  requires the Curve Library review-to-build contract before activation
- blank include-fragment hooks
  preserved as review metadata
- formula-like or otherwise unclaimed legacy matrix-builder constants such as
  `frd`

Those fields remain staged because the current FEMIC exporter is checkpoint-
first and already assumes bundle/context inputs rather than rebuilding matrix
layout semantics from workbook-authored expressions.

## Source of truth

- translated config:
  `config/legacy_xml_builder/input_variables.mkrf.yaml`
- lineage/status map:
  `metadata/legacy_input_variables_translation.yaml`
- parent-side extracted review evidence:
  `metadata/mkrf_xlsm_review/`

## Current boundary

- This slice does not make the full legacy workbook live.
- This slice does not publish the workbook itself into the instance.
- This slice does not rebuild the legacy unmanaged-track select logic.
- This slice does not activate include hooks or the broader matrix-builder
  semantics beyond the explicit scalar constants contract.
- This slice does not treat generated `Curves.xml` as editable source.
- This slice does not claim a runnable MKRF rebuild contract.
