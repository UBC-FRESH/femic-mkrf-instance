Troubleshooting
===============

Common Boundary Confusions
--------------------------

Problem:
  treating archival compiled evidence as though it were raw source

Fix:
  use the publication/reproducibility boundary runbooks to distinguish
  ``03_MappingAnalysisData/*`` from compiled runtime artifacts.

Problem:
  treating the current PoC package as the canonical rebuild

Fix:
  use ``models/mkrf_patchworks_model_poc/`` only as the benchmark/intermediate
  package. Keep the later from-scratch rebuild lane separate.

Problem:
  assuming unresolved helper seams block the PoC benchmark lane

Fix:
  the unresolved target-helper families are deferred seams, not a blocker to
  the accepted PoC benchmark contract.

Problem:
  using checkpoint target files as output KPIs

Fix:
  compare real scenario outputs and summary reports, not reloaded target-state
  inputs.
