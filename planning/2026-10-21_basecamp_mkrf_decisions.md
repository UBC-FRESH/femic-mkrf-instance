# MKRF Basecamp decisions: publication boundary and patch logic

Date recorded: 2026-10-21

Source: MKRF Basecamp thread, Anna Tobiasz and Greg Paradis. The cost/revenue
exchange is from 2026-10-05; the patch-logic guidance is from the following day
and was restated as "yesterday" in the thread.

This note turns the thread into instance decisions. It is the planning surface
for the corresponding config, docs and ws4 changes.

## 1. Data publication boundary

### Decisions

- The MKRF spatial data is **not publicly available**, but MKRF is not
  concerned about it being used in this workflow. The instance may carry the
  spatial runtime payload, but it must not claim that payload is public data.
- The raw cost/revenue spreadsheets Anna supplied (sorts, revenues, contractor
  rates, and similar internal financial detail) **must not be published**.
- The public model should remain fully open. It should use generic or
  field-school average cost/revenue information that represents the situation
  without exposing private contractor rates.
- A private internal-planning version may carry more detailed financial
  cash-flow parameters. That version is not published.
- Comparing the public average-based model with the private detailed model is
  useful evidence; it is not a prerequisite for publishing the public model.

### Implementation boundary

The public instance carries:

- source code, configs, docs, metadata and model structure;
- the published-model cost basis in `config/harvest_costs.mkrf.yaml`, which is
  built from Coast Appraisal Manual rates plus explicitly flagged assumptions;
- published Vancouver Log Market prices in
  `config/log_grade_prices.mkrf.yaml`; and
- generated model/track/spatial surfaces that do not embed raw internal
  financial spreadsheets.

The public instance does **not** carry:

- raw MKRF cost/revenue workbooks or contractor-rate tables;
- the private financial cash-flow overlay; or
- any derived table that reproduces those private rates.

The private overlay is tracked in its own private GitHub repository and linked
into internal checkouts as a git submodule (for example
`external/femic-mkrf-private/`). It is not required by the public model: a
public clone runs from the public configs alone. A private superproject can
compose the public instance and the private overlay when both are needed.

### Audit performed

- No raw `.xlsx`, `.xls` or `.xlsm` files are tracked in the instance.
- The tracked cost config uses CAM published rates and assumption flags. It
  does not contain MKRF contractor rates.
- The tracked price config uses the public Vancouver Log Market series.
- Legacy compiled track/XML payloads are model outputs, not the raw financial
  workbooks.

## 2. Opening-size policy (supersedes the 100 m adjacency rule)

### Decision

Use **opening-size targets and weights**, not an arbitrary 100 m adjacency
rule. This follows the approach used previously for Mission and MKRF, minus the
additional 100 m groups rule.

| Size class | Target share | Weight |
| --- | --- | --- |
| `<= 1 ha` | 0% | Very High |
| `> 1 and <= 5 ha` | 10% | High |
| `> 5 and <= 40 ha` | no target | None |
| `> 40 and <= 50 ha` | 5% | High |
| `> 50 ha` | 0% | High |

The current implementation treats the shares as **maxima**, matching the legacy
Patchworks `setMaximumPeriodic` targets. Numeric weight mapping used by the ws4
pilot:

- Very High = 1,000,000
- High = 100,000
- None = target omitted

### ws4 implementation

- `ws4/patch_accounts.yaml` defines one account, `patch.grpblk`, on
  `product.area.managed.treat.CC`, with size classes
  `[1, 5, 40, 50, inf]` and `search_distance: 0.0` (touching blocks only).
- `ws4/targets.yaml` carries the five-class targets per accounting period.
- The ws4 pilot no longer passes `min_green_up_years`; the 100 m adjacency rule
  is not part of the active policy.
- `max_opening_ha` is optional and off by default; the size-class targets are
  the policy instrument.
- The Patchworks `greenup` block remains in the canonical runtime as a
  reference/legacy surface. It is not the active ws4 policy.

### Open questions

1. Confirm that the table's "Target (%)" means a maximum share, not a minimum
   share. The current implementation follows the legacy Patchworks maximum
   semantics.
2. Confirm the numeric mapping for "Very High" and "High" weights. The values
   above are the pilot defaults; they are not from the Basecamp thread.
3. Decide whether the public model should use field-school averages directly
   or the published CAM/VLM basis already in the config. The Basecamp thread
   approves either, provided no private rates are exposed.
4. Name the private overlay repository and submodule path, and decide whether
   internal checkouts use the instance as the superproject or a separate private
   superproject that composes public + private.

## 3. Current pilot status

The constructive patch-first schedule meets all 32 period targets. It has 364
openings and 1,226 scheduled blocks; at the target periods, 100% of openings are
in the 5-40 ha class, with 0% in the `<=1`, `>1-5`, `>40-50` and `>50` classes.
The warm-start search reaches objective 0 while keeping the patch and harvest
targets met.

The legacy 100 m green-up run remains available as a comparison surface. The
two policy questions above were posted to the MKRF Basecamp ws4 thread on
2026-10-21; the pilot continues to treat the shares as maxima and the weights as
pilot defaults until MKRF confirms them.
