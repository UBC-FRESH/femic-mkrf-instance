# femic-mkrf-instance

Private standalone **MKRF FEMIC instance** for bootstrap, contract hardening,
and later publication of the real MKRF model payload.

## Current status

This repository is intentionally a **thin baseline**.

Included now:

- standard FEMIC instance scaffold;
- `config/rebuild.spec.yaml` and `config/rebuild.allowlist.yaml`;
- `config/run_profile.mkrf.yaml`, `config/silviculture.mkrf.yaml`, and
  `config/tipsy/tsamkrf.yaml` starter surfaces;
- instance-local legacy compiled-package reference metadata plus a copied
  archival control layer for the stable 2016 `PW_MKRF` package;
- `runbooks/REBUILD_RUNBOOK.md`;
- metadata ledgers for provenance and checksum tracking; and
- one non-sensitive annex-backed smoke artifact used to validate publication
  and cold-clone materialization.

Not included yet:

- the real MKRF bulky data/model payload;
- public/docs-hosted student-facing documentation; and
- packaged built-in registration in the parent FEMIC repo.

## Legacy Compiled Package Reference

This instance now carries a **metadata-only intake** of the stable compiled
legacy MKRF Patchworks package.

Instance-local reference surfaces:

- `runbooks/LEGACY_COMPILED_PACKAGE_REFERENCE.md`
- `metadata/legacy_compiled_package_reference.yaml`
- `data/legacy_mkrf/compiled_controls/`

These surfaces summarize the discovered compiled package anatomy:

- `baseMKRF.pin` as the primary compiled model entrypoint;
- `Tracks/*.csv` as the compiled matrix/runtime table family;
- `Spatial/fragments.*` plus `Spatial/topo_frag100.csv` as the spatial runtime
  family; and
- `ScenarioSet.bsh`, `runME.bsh`, `Scripts/*.bsh`, and `Targets/*.bsh` as the
  scenario/control seam.

Copied archival controls now present in-instance:

- `data/legacy_mkrf/compiled_controls/entrypoints/`
- `data/legacy_mkrf/compiled_controls/scripts/`
- `data/legacy_mkrf/compiled_controls/targets/`

Important boundary:

- these copied files are **archival references only**;
- the full legacy compiled runtime payload itself is not published into this
  instance yet;
- the bulky upstream mapping-analysis lane is still deferred; and
- this does not make the instance runnable as a legacy Patchworks rebuild.

## DataLad dataset policy

This repository is intended to follow the **large-only DataLad/git-annex**
pattern used by `femic-tsa29-instance`.

Policy:

- keep docs, config, runbooks, metadata ledgers, and other small canonical text
  in Git;
- annex bulky runtime/model/publication artifacts only; and
- do not publish transient local scratch or machine-specific secrets.

## Quickstart

1. Validate the rebuild contract:
   `femic instance validate-spec --spec config/rebuild.spec.yaml`
2. Dry-run the rebuild sequence:
   `femic instance rebuild --spec config/rebuild.spec.yaml --dry-run --run-id mkrf_dryrun`
3. Review the legacy compiled-package reference note:
   `runbooks/LEGACY_COMPILED_PACKAGE_REFERENCE.md`
4. Inspect the copied archival control layer under:
   `data/legacy_mkrf/compiled_controls/`
5. If this is a thin clone, materialize the annex smoke artifact:
   `python -m datalad get data/annex_smoke/mkrf_bootstrap_smoke.bin`
6. Run full `femic prep validate-case --run-config config/run_profile.mkrf.yaml --tipsy-config-dir config/tipsy`
   only after the real MKRF boundary and checkpoint inputs are published.

See `runbooks/REBUILD_RUNBOOK.md` for the current thin-baseline boundary.
