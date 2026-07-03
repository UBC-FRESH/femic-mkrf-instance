# MKRF FreshForge Executable Model-Build Acceptance

This note records the MKRF-side work for FEMIC P106.

The MKRF instance owns the executable workflow and the `mkrf.*` provider
namespace. FEMIC core supplies reusable `femic.*` stages such as case
validation, geospatial preflight, Patchworks preflight, and Matrix Builder.

P106 updates the MKRF adapter to the released FreshForge execution API:
`run_node(...)` returns `ProviderRunResult` with `RunStatus`, deterministic
command metadata, diagnostics, outputs, and JSON-safe artifacts. The adapter
continues to launch instance-owned `python -m mkrf_femic ...` commands rather
than moving MKRF workflow code into FEMIC core.

The model-build workflow runs from the parent FEMIC checkout. Its
`instance_root` parameters should be `external/femic-mkrf-instance`; all other
workflow paths remain instance-relative unless they are intentionally
parent-owned FreshForge runtime paths.

Materialization remains a prerequisite workflow. If the MKRF submodule is thin
or incomplete, run the MKRF materialization workflow before the model-build
workflow.
