Operator Runbook
================

Minimal Operator Path
---------------------

1. Validate the instance spec:

   - ``femic instance validate-spec --spec config/rebuild.spec.yaml``

2. Review the current runtime wiring:

   - ``config/patchworks.runtime.windows.yaml``

3. Launch the PoC runtime package from:

   - ``models/mkrf_patchworks_model_poc/analysis/base.pin``

4. Use the PoC package for:

   - benchmark comparison;
   - runtime smoke;
   - operator demonstration; and
   - reverse-engineering reference.

Do Not Treat This As
--------------------

- the final canonical MKRF rebuild package;
- a source-faithful rebuild claim; or
- the final target/control architecture for the later from-scratch lane.

Key Reads
---------

- ``README.md``
- ``runbooks/REBUILD_RUNBOOK.md``
- ``runbooks/LEGACY_REBUILD_READINESS_CRITERIA.md``
- ``runbooks/LEGACY_SOURCE_REPRODUCIBILITY_BOUNDARY.md``
