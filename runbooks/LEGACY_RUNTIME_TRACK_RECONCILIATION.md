# Legacy Runtime Track Reconciliation

This note records the `P57.6` / `P57.7` smoke reconciliation of generated MKRF
runtime track tables against the legacy compiled track evidence, plus the
`P57.8` launch proof from the generated runtime directory.

## Decision

Patchworks matrix build now writes real generated track tables under
`models/mkrf_patchworks_model/Tracks/`.

The minimal-runnable smoke comparison is good enough to move forward:

- generated `curves.csv`, `features.csv`, `products.csv`, `treatments.csv`,
  `accounts.csv`, and `blocks.csv` now exist;
- representative generated-vs-legacy track cohort identity matches for
  `track 2` (`tracknames.csv`, `strata.csv`, and `blocks.csv`);
- generated `features.csv` and `products.csv` row counts and label sets match
  the legacy compiled planning-corpus references; and
- representative managed total-yield curve shapes match the legacy compiled
  track evidence.

Patchworks launch is also now proven from the generated runtime directory:

- generated launch surface: `models/mkrf_patchworks_model/analysis/base.pin`;
- runtime config surface: `config/patchworks.runtime.windows.yaml`; and
- observed result: the developer confirmed that the generated model opened in
  Patchworks from the generated runtime directory on 2026-04-29.

## Accepted Variance

The remaining non-blocking variance is in
`feature.yield.managed.merch.total`.

For all common managed merch tracks checked during `P57.7`:

- generated merch curves preserve the same pre-tail shape but end with
  `500 -> 501 -> 0`; and
- legacy merch curves preserve the same pre-tail shape but end with
  `650 -> 651 -> 0`.

This variance is accepted for the minimal runnable phase because it does not
change track cohort identity or present-day initial conditions in the way that
would block a first runnable MKRF instance. It remains a documented caveat for
very-old-stand merchantable-yield behavior.

## Current Boundary

This closeout still does not claim raw-source reconstruction or exact legacy
compiled equivalence. The minimally runnable claim is limited to FEMIC-managed
XML emission, successful matrix build, accepted smoke reconciliation, and a
proven Patchworks launch from the generated runtime directory.
