Getting Started
===============

Purpose
-------

``femic-mkrf-instance`` is the private standalone MKRF FEMIC instance used for:

- bootstrap and contract hardening;
- legacy reverse-engineering;
- PoC benchmark/runtime comparison; and
- handoff into the later from-scratch MKRF rebuild.

Current Runtime Surface
-----------------------

The checked-in Patchworks package is:

- ``models/mkrf_patchworks_model_poc/``

This is the current PoC benchmark/intermediate surface. It is not the final
canonical rebuild package.

Quick Operator Surface
----------------------

Primary files:

- runtime config:
  ``config/patchworks.runtime.windows.yaml``
- Patchworks PIN:
  ``models/mkrf_patchworks_model_poc/analysis/base.pin``
- runtime XML:
  ``models/mkrf_patchworks_model_poc/XML/baseMKRF.xml``
- runtime tracks:
  ``models/mkrf_patchworks_model_poc/Tracks/``
- spatial runtime:
  ``models/mkrf_patchworks_model_poc/Spatial/``

Recommended first reads:

- ``README.md``
- ``runbooks/REBUILD_RUNBOOK.md``
- ``runbooks/LEGACY_RUNTIME_XML_EMISSION.md``
- ``runbooks/LEGACY_RUNTIME_TRACK_RECONCILIATION.md``

What This Guide Covers
----------------------

This guide documents the current MKRF PoC benchmark lane:

- what the instance contains;
- how the runtime package is wired;
- what benchmark evidence was accepted;
- what boundaries and caveats still exist; and
- how this PoC relates to the later from-scratch rebuild lane.
