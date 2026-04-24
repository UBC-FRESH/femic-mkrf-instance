# MKRF Legacy XLSM Surface Map

This note maps the governing workbook `002_base.xlsm` into the main source
surface families we expect to refactor into FEMIC-native inputs.

## Core workbook surfaces

- `Input Variables`
  problem metadata, inventory-field bindings, constants, unmanaged-track query,
  and XML include-fragment hooks
- `Codes`
  workbook registry and enum surface for active strata, attributes, curves,
  choices, and lookup/constants families
- `Curve Library`
  age-by-curve point library used by `dumpCurves`
- `Netdown`
  aspatial netdown rules and optional feature reassignment/factor surface
- `Attrib`
  general attribute assignments emitted after stratum-specific rules
- `Treat`
  the currently active stratum bundle, including criteria, features,
  succession, products, and treatments
- `Post Renewal Succession`
  supporting treatment-response / transition lookup surface
- `Lookups`
  lookup-table and CSV bridge support surface

## FEMIC interpretation

The workbook is no longer just "one spreadsheet". It is a bundle of future
FEMIC-facing surfaces:

- config-like problem and include settings
- enum and registry surfaces
- rule tables
- curve tables
- stratum bundles
- lookup and transition tables

## Current boundary

- This map classifies workbook surfaces only.
- It does not yet materialize those values into tracked CSV/YAML tables.
- It does not reimplement the SPS VBA.
- It does not publish the workbook itself into the instance.
