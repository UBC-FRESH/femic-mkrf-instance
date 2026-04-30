Docs Ownership and Release
==========================

Purpose
-------

This page defines who owns the MKRF PoC docs set, how publication should be
validated, and how docs changes relate to the current PoC benchmark package and
the later canonical rebuild lane.

Ownership Matrix
----------------

+----------------------+----------------------------+-----------------------------+
| Area                 | Primary Owner              | Backup Owner                |
+======================+============================+=============================+
| Instance docs        | Case maintainer            | FEMIC maintainer            |
+----------------------+----------------------------+-----------------------------+
| Lineage/runbook      | Case maintainer            | FEMIC maintainer            |
+----------------------+----------------------------+-----------------------------+
| Sphinx template/CI   | FEMIC maintainer           | Case maintainer             |
+----------------------+----------------------------+-----------------------------+
| Publication checks   | FEMIC maintainer + reviewer| Case maintainer             |
+----------------------+----------------------------+-----------------------------+

Current Release Reading
-----------------------

The current published docs describe the MKRF PoC benchmark/intermediate package
under ``models/mkrf_patchworks_model_poc/``.

They do not describe:

- a final canonical MKRF rebuild release; or
- a source-faithful rebuild from raw upstream source inputs.

Any later publication for the canonical rebuild should either replace this docs
surface deliberately or live as a distinct release contract with its own claim
boundary.

Update Cadence
--------------

- update immediately after changes to:
  - runtime package pathing;
  - accepted claim boundaries;
  - benchmark interpretation;
  - lineage/reproducibility surfaces; or
  - operator launch/rebuild steps.
- rerun the standalone docs build before each docs checkpoint:
  - ``python -m sphinx -b html docs docs/_build/html -W``

Required Publication Checks
---------------------------

Before treating the MKRF docs as releasable:

- the standalone docs build must be warning-clean;
- the parent FEMIC docs contract checks must still pass if parent docs changed;
- the docs text must stay explicit that the current package is PoC-only; and
- user-local or machine-specific private paths must not leak into the published
  pages.

Current Sufficiency Reading
---------------------------

For the current PoC lane, this docs set is now intended to be sufficient for:

- operator orientation to the accepted runtime package;
- interpretation of the accepted benchmark/KPI comparison surface;
- review of the accepted claim boundary and deferred seams; and
- handoff into the later canonical rebuild lane without re-opening PoC
  archaeology by default.

That is the standard for "good enough" in the current lane. It does not mean
the PoC is the final architecture. It means the benchmark/intermediate surface
is now documented well enough that the team can stop treating it as
under-documented.

Versioning and Handoff
----------------------

For the current PoC lane:

- docs changes track the PoC benchmark package and its accepted interpretation;
- significant docs milestones should be reflected in the governing GitHub issue
  trail; and
- the later canonical rebuild phase should inherit this docs set as reference
  material, not as an architecture lock-in.

The concrete handoff target for that later lane is the from-scratch MKRF
rebuild under parent issue ``#173`` and FEMIC roadmap Phase 60.
