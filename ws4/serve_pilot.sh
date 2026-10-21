#!/usr/bin/env bash
# Serve the MKRF ws4 pilot in the ws4 web UI.
#
# Run `python ws4/run_pilot.py` first so the matrix, run, geometry and report
# files exist. The UI is read-only unless --allow-runs is added below.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTANCE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WS4_ROOT="${WS4_ROOT:-$INSTANCE_ROOT/../../../ws4}"
PORT="${PORT:-8011}"

cd "$WS4_ROOT"
exec python -m ws4.cli serve \
  --dataset "$INSTANCE_ROOT/ws4/runtime/matrix" \
  --runs "$INSTANCE_ROOT/ws4/runtime" \
  --targets "$INSTANCE_ROOT/ws4/targets.yaml" \
  --geometry "$INSTANCE_ROOT/ws4/runtime/fragments.geojson" \
  --crs EPSG:3005 \
  --topology "$INSTANCE_ROOT/ws4/topology.csv" \
  --patch-accounts "$INSTANCE_ROOT/ws4/patch_accounts.yaml" \
  --host 127.0.0.1 \
  --port "$PORT"
