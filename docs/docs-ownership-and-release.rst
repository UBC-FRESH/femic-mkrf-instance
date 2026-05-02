Docs Ownership and Release
==========================

Purpose
-------

This page defines who owns the MKRF instance docs set, how publication should
be validated, and how docs changes relate to the active canonical release lane
and the retained PoC benchmark/reference package.

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

The current published docs describe the canonical MKRF release lane under
``models/mkrf_patchworks_model/``.

They also retain benchmark/reference explanation for:

- ``models/mkrf_patchworks_model_poc/``; and
- selected legacy-only evidence/control surfaces that remain outside the
  canonical claim boundary.

They should not teach the PoC package as the active runtime/package lane.

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
- the instance repo GitHub Pages workflow must be able to rebuild the
  standalone docs from `main` pushes;
- the parent FEMIC docs contract checks must still pass if parent docs changed;
- the docs text must stay explicit that the canonical package is current and
  that the PoC package is benchmark/reference evidence only; and
- user-local or machine-specific private paths must not leak into the published
  pages.

Publication Channels
--------------------

The standalone MKRF docs now carry two publication/build contracts:

- `.github/workflows/docs-pages.yml` for GitHub Pages publication on `main`
  pushes in the instance repo; and
- `.readthedocs.yaml` as the repo-local standalone Sphinx build contract.

The GitHub Pages workflow is the expected public publication path for the
standalone instance docs. The Read the Docs config remains a portable build
contract and secondary hosting option.

Current Sufficiency Reading
---------------------------

For the current canonical release lane, this docs set is now intended to be
sufficient for:

- operator orientation to the active runtime package;
- interpretation of the accepted benchmark/KPI comparison surface against the
  retained PoC lane;
- review of the accepted canonical claim boundary and deferred seams; and
- handoff into later post-release canonical iterations without re-opening PoC
  archaeology by default.

That is the standard for "good enough" in the current lane. It means the active
canonical release is documented well enough for operator/developer use while
the retained PoC benchmark/reference surface remains clearly separated.

Versioning and Handoff
----------------------

For the current canonical lane:

- docs changes track the active canonical package and its accepted claim
  boundary;
- significant docs milestones should be reflected in the governing GitHub issue
  trail; and
- the retained PoC benchmark package should remain documented as reference
  material, not as the active architecture.

The concrete next handoff target after the `v0.0.1a1` release is the
post-release docs cleanup and later archival/reference publication work tracked
from the canonical rebuild closeout.
