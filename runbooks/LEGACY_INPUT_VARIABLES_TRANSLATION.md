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

These are the only workbook-derived values that currently affect exporter
behavior in this slice.

## What remains staged only

The translated config also preserves legacy workbook seams that are **not yet
live**:

- `max_inventory_age`
- legacy matrix-builder expressions for exclude, block key, polygon area, and
  stand age
- additional stratification column bindings
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
- This slice does not activate legacy include hooks, constants, or matrix-
  builder expressions.
- This slice does not claim a runnable MKRF rebuild contract.
