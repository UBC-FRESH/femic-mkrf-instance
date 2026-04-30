Troubleshooting
===============

Common Boundary Confusions
--------------------------

Problem:
  treating archival compiled evidence as though it were raw source

Fix:
  use the publication/reproducibility boundary runbooks to distinguish
  ``03_MappingAnalysisData/*`` from compiled runtime artifacts.

Why this happens:
  the PoC intentionally carries both archival compiled evidence and generated
  runtime artifacts in the same instance repo, so path adjacency alone is not a
  proof of provenance.

Problem:
  treating the current PoC package as the canonical rebuild

Fix:
  use ``models/mkrf_patchworks_model_poc/`` only as the benchmark/intermediate
  package. Keep the later from-scratch rebuild lane separate.

Why this matters:
  the PoC package is designed to coexist with the future canonical rebuild in
  the same instance repo, so naming and claim boundaries are part of the
  contract.

Problem:
  assuming unresolved helper seams block the PoC benchmark lane

Fix:
  the unresolved target-helper families are deferred seams, not a blocker to
  the accepted PoC benchmark contract.

Check first:
  ask whether the unresolved seam changes the accepted benchmark conclusion. If
  not, it probably belongs to the later rebuild lane.

Problem:
  using checkpoint target files as output KPIs

Fix:
  compare real scenario outputs and summary reports, not reloaded target-state
  inputs.

Why this matters:
  `targetSummary`/`targetStatus` files are valid saved target-control state, but
  they are not the model-output surface you use to compare behavior across
  builds.

Problem:
  judging the PoC against a short, non-stabilized run and then treating the
  mismatch as a model defect

Fix:
  compare against a run budget that is large enough to stabilize meaningfully
  for the benchmark question being asked, then compare summary-report KPIs.
