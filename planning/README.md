# MKRF planning notes

Active planning surfaces for the MKRF instance:

- `2026-10-21_basecamp_mkrf_decisions.md` — publication boundary and the
  current opening-size policy from MKRF staff.
- `data_publication_boundary.md` — public vs private data classification,
  private overlay/submodule composition, and release audit commands.
- `2026-11-18_variable-retention-basis.md` — BC retention-basis definitions and
  the proposed MKRF dispersed/group retention model, with source audit and a
  worked MKRF 684 example.
- `2026-11-18_retention_basis_example.csv` — worked BA/stem/crown retention
  comparison for MKRF 684.
- `2026-11-18_variable-retention-implementation.md` — first-pass retention
  profile, matrix variant, target-search results, and core-split next steps.

Implementation surfaces that follow these decisions:

- `ws4/targets.yaml` — period-indexed targets, including the opening-size
  classes.
- `ws4/patch_accounts.yaml` — `patch.grpblk` on touching clearcut blocks.
- `config/harvest_costs.mkrf.yaml` — public cost basis and publication note.
- `docs/ws4-pilot.rst` and `ws4/README.md` — pilot runbook and status.
