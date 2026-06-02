# MKRF Patchworks Canonical Rebuild Package

This directory is the target home for the source-faithful MKRF rebuild package
tracked under `P60.8+`.

Current scope:

- this is a path-distinct canonical package root for the rebuild lane;
- it is separate from the PoC benchmark package at
  `models/mkrf_patchworks_model_poc/`; and
- it contains the active canonical runtime package artifacts used for the
  current MKRF rebuild lane.

Planned contents:

- `analysis/`
- `xml/`
- `tracks/`
- `spatial/`
- `scripts/`
- `targets/`
- `initial_targets/`

Current boundary:

- `tracks/` is the active compiled track-table surface;
- `xml/` is the active XML/runtime contract surface; and
- `analysis/ct_eligibility_audit.csv` records the current cedar-pole CT
  eligibility filter used to constrain the active commercial-thinning lane.

Current CT contract:

- active CT treatments are `CT35`, `CT40`, and `CT45`;
- active CT eligibility requires the runtime ground/operability seam plus
  strict `Cw > 15%`; and
- CT intensity is documented in `metadata/ct_treatment_contract.yaml`, with the
  medium 45% basal-area removal lane represented in the current runtime.
