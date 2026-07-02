# MKRF FreshForge Materialization Overlay

This note records the MKRF-owned materialization overlay added for FEMIC P101.
The workflow is meant to be run from the parent FEMIC checkout with MKRF mounted
as `external/femic-mkrf-instance`.

MKRF uses the generic FEMIC materialization provider:

- `femic.materialization.check_toolchain`
- `femic.materialization.check_python_environment`
- `femic.materialization.install_packages`
- `femic.materialization.init_submodules`
- `femic.materialization.init_annex`
- `femic.materialization.enable_special_remote`
- `femic.materialization.materialize_paths`
- `femic.materialization.audit_annex_availability`
- `femic.materialization.write_materialization_report`

The overlay materializes `models`, `config`, `workflows`, and `data/source`.
Those paths cover the current canonical runtime package plus the source FileGDB
used by the MKRF model-build workflow. The report is written under
`runtime/freshforge/`, which is ignored.

The install step includes the parent FEMIC `dev` and `freshforge` extras and
installs this MKRF repository editable. That makes the MKRF-owned `mkrf`
FreshForge provider available for later model-build workflow commands.
