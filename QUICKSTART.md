# FEMIC Deployment Instance Quickstart

1. Validate CLI install:
   `femic --help`
2. Validate the rebuild-spec structure:
   `femic instance validate-spec --spec config/rebuild.spec.yaml`
3. Validate geospatial runtime dependencies (Fiona/GDAL):
   `femic prep geospatial-preflight`
4. Customize `config/run_profile.mkrf.yaml`.
5. Customize `config/rebuild.spec.yaml` for your case sequence/invariants.
6. Optionally update `config/rebuild.allowlist.yaml` for intentional baseline diffs.
7. Review the current legacy compiled-package reference in
   `runbooks/LEGACY_COMPILED_PACKAGE_REFERENCE.md`.
8. Add case-specific instructions to `runbooks/REBUILD_RUNBOOK.md`.
9. Add/edit `config/tipsy/tsamkrf.yaml`.
10. Use `femic prep validate-case --run-config config/run_profile.mkrf.yaml`
   only after the real MKRF boundary and checkpoint inputs have been published
   into this instance.
