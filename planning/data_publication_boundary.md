# Data publication boundary

Status: active for the MKRF instance
Date: 2026-10-21

This note records what may be published from `femic-mkrf-instance` when the
repository is public by default, and where internal-only material belongs.

It implements the Basecamp decision recorded in
`planning/2026-10-21_basecamp_mkrf_decisions.md`.

## Classification

| Surface | Publication status | Notes |
| --- | --- | --- |
| Source code, configs, docs, metadata | Public | The public model must be runnable from these alone. |
| Model XML, fragments, tracks, generated runtime package | Approved for the open workflow | MKRF spatial data is not claimed as public data; it is carried for the workflow with MKRF's approval. |
| `config/harvest_costs.mkrf.yaml` | Public | Coast Appraisal Manual rates plus explicitly flagged assumptions. No MKRF contractor rates. |
| `config/log_grade_prices.mkrf.yaml` | Public | Published Vancouver Log Market series. |
| Raw MKRF cost/revenue workbooks (sorts, revenues, contractor rates) | **Do not publish** | Keep outside the repo or in the private overlay. |
| Detailed private financial cash-flow parameters | **Do not publish** | Private overlay only. |
| Derived tables that reproduce private rates | **Do not publish** | Aggregate or anonymize before publishing. |
| Legacy compiled model outputs | Public | Model outputs, not raw financial workbooks. |

## Public model vs private overlay

The public model is the teaching/research/default model. It carries the open
cost and price basis and must not require a private file to run.

The private overlay is for internal MKRF planning. It is **tracked**, in its
own private GitHub repository, and linked into internal checkouts as a git
submodule. Suggested composition:

```text
femic-mkrf-instance/                 public repository
  external/femic-mkrf-private/       private overlay submodule (private repo)
    config/harvest_costs.mkrf.yaml
    config/log_grade_prices.mkrf.yaml
    config/financial_assumptions.mkrf.yaml
```

The public model must not require the private submodule. A public clone runs
from the public configs alone; an internal checkout initializes the private
submodule and points the run at the overlay configs. If the private submodule
cannot be exposed to public clones, use a private superproject that composes
the public instance and the private overlay, rather than putting an
inaccessible submodule in the public clone path.

The private overlay may override the public cost or price config at run time;
the public configs remain the defaults. Record the overlay repo and submodule
commit in the internal planning note.

## Controls

- `.gitignore` rejects spreadsheet workbooks and local private scratch
  (`config/private.local/`, `*.local.yaml`). The tracked private overlay is a
  submodule, not an ignored path.
- The cost config header repeats the boundary so a reader does not mistake the
  assumption flags for published MKRF rates.
- Before changing repository visibility, run:

```bash
git ls-files | grep -Ei '\.(xlsx|xls|xlsm)$'
git grep -nEi 'contractor|private|confidential' -- config planning docs
```

Both should be empty or explainable.

## Open work

- Confirm whether the public model should use field-school averages or the
  current CAM/VLM basis. The Basecamp thread accepts either.
- Build the private overlay and compare its results with the public model.
- Add a release checklist item that reruns the two audit commands above.
