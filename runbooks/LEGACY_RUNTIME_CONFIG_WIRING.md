# Legacy Runtime Config Wiring

This note records `P57.5`, which wires the MKRF Patchworks runtime config to
the generated runtime model directory and validates preflight without starting
matrix build.

## Decision

The instance runtime config at `config/patchworks.runtime.windows.yaml` now
points at:

- `models/mkrf_patchworks_model_poc/Spatial/fragments.dbf`
- `models/mkrf_patchworks_model_poc/XML/baseMKRF.xml`
- `models/mkrf_patchworks_model_poc/Tracks`

The builtin Patchworks registry now exposes `mkrf.base` as the minimal MKRF
launch surface for later launch proof.

## Preflight

`femic patchworks preflight --config external/femic-mkrf-instance/config/patchworks.runtime.windows.yaml`
passed in the active Windows shell.

The validated runtime used:

- Patchworks jar at `C:/Program Files/Spatial Planning Systems/Patchworks/patchworks.jar`
- launcher `C:/Program Files/Eclipse Adoptium/jdk-8.0.452.9-hotspot/bin/java.EXE`
- license env `SPS_LICENSE_SERVER`
- license host `auth.spatial.ca`
- `SPSHOME` `C:/Program Files/Spatial Planning Systems/Patchworks`

## Current Boundary

`P57.5` does not run matrix build and does not prove Patchworks launch. It
only confirms that the runtime config and local Patchworks installation resolve
cleanly enough to proceed to the matrix-build gate.

