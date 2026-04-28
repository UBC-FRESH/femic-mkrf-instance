# Legacy Source Input Publication Boundary

This note records the P56.5 source-input publication boundary for the MKRF
legacy rebuild lane.

## Decision

Source-input publication boundary: **resolved for the next readiness gate**.

Payload intake: **not started**.

Runnable rebuild readiness: **no-go**.

## Matrix-Build Candidate Inputs

A future matrix-build candidate requires validated fragments/topology inputs
plus FEMIC-generated ForestModel XML.

The readable legacy planning corpus contains `Spatial/fragments.*` and
`Spatial/topo_frag100.csv`. The fragment shapefile has 1,763 polygon features
in EPSG:3005 and carries the fields required by the generated XML/input
contract:

- `RES_KEY`
- `CONTCLAS`
- `AGE_2020`
- `AU_EX`
- `AU_FU`
- `Operabilit`
- `CT_eligib`

The current instance fragment files remain pointer-sized and require
DataLad/git-annex before they can be treated as published instance-local
payloads. `topo_frag100.csv` is available as archival evidence.

## Reproducibility Boundary

The archived compiled fragments/topology lane is not the same thing as raw
source reproducibility.

Full source reproducibility would require a later decision on
`03_MappingAnalysisData/*`, including `Source.gdb`, `Resultant.gdb`,
`Resultant_info_v1.xlsx`, and the VDYP yield-prep family.

Roads are not required for the current legacy PIN because `useRoutes=false`.
Outputs are validation/report evidence, not source inputs. Direct workbook
publication is not required for the current FEMIC contract because workbook
values are already represented by tracked extracts and translated config
contracts.

## Identity Boundary

The generated XML literal description is `Base TFL26`. That value is preserved
as source evidence only. It is not accepted as the MKRF case identity.

The mismatch must remain visible in rebuild-readiness criteria before any
user-facing runnable rebuild claim.

P56.5 did not ingest mapping data, outputs, roads, or workbook payloads; did
not generate XML; did not regenerate fragments; and did not run Patchworks
matrix build.
