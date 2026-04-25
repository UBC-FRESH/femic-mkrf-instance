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

These workbook-derived values now affect exporter behavior in this slice.
When the live expressions reference checkpoint source columns such as
`RES_KEY`, `AGE_2020`, or `CONTCLAS`, those columns must be present in the
checkpoint and are passed through into the exported fragments surface.
The live additional-stratification bindings use the same rule. The workbook
key `au` is written as fragment field `au_1` so it does not collide with the
base required `AU` fragments field that already exists in the Patchworks
fragments schema.

## What remains staged only

The translated config also preserves legacy workbook seams that are **not yet
live**:

- `max_inventory_age`
- treatment-eligibility expression
- legacy include-fragment hooks
- legacy matrix-builder constants

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
- This slice does not activate treatment eligibility, include hooks, or
  constants.
- This slice does not claim a runnable MKRF rebuild contract.
