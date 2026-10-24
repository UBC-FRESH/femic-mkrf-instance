# MKRF sub-hectare stand polygons

Status: analysis complete; attribute-safe merge is optional and not applied to the canonical inventory.

## Question

Are the 0-1 ha openings caused by slivers in the original VRI inventory, and
should the input polygons below 1 ha be merged into their largest neighbour?

## Inventory

Source: `models/mkrf_patchworks_model/spatial/fragments.shp` (EPSG:3005)

| Quantity | Value |
| --- | ---: |
| Total polygons | 1,763 |
| Total area | 4,810.85 ha |
| Polygons < 1 ha | 628 |
| Share of polygons | 35.6% |
| Area < 1 ha | 277.07 ha |
| Share of area | 5.76% |
| Minimum polygon | 0.1002 ha |
| Median small polygon | 0.3805 ha |

There are **no polygons below 0.10 ha**. That is a hard source-data floor.

## Size histogram

| Bin (ha) | Polygons | Area (ha) |
| --- | ---: | ---: |
| 0.10-0.15 | 92 | 11.36 |
| 0.15-0.20 | 53 | 9.47 |
| 0.20-0.25 | 59 | 13.07 |
| 0.25-0.30 | 44 | 12.11 |
| 0.30-0.40 | 80 | 28.23 |
| 0.40-0.50 | 57 | 25.36 |
| 0.50-0.60 | 52 | 28.78 |
| 0.60-0.70 | 59 | 38.04 |
| 0.70-0.80 | 48 | 35.66 |
| 0.80-0.90 | 47 | 40.05 |
| 0.90-1.00 | 37 | 34.94 |

At 0.01 ha resolution the strongest local modes are 0.10-0.11 ha (29
polygons), 0.13-0.14 ha (22), 0.18-0.21 ha (35), and 0.57-0.58 ha (14). The
distribution has a **hard boundary at 0.10 ha** and a broad 0.10-0.21 ha
cluster; there is no sharp gap at 0.25, 0.5 or 1.0 ha. A 1 ha cutoff is an
opening-policy line, not a natural break in the source data.

## What the small polygons contain

| Attribute | Area (ha) |
| --- | ---: |
| Operable | 200.32 |
| Riparian | 45.55 |
| Reserve | 25.47 |
| Low operability | 5.72 |
| `CONTCLAS = N` | 71.03 |
| CT eligible | 175.34 |

Small polygons are overrepresented in riparian/reserve and non-contributing
classes relative to the ≥1 ha population. They are not all geometric noise.

## Merge effects

Using the largest touching neighbour:

- 584 small polygons have a touching target of at least 1 ha;
- 44 small polygons have no touching/nearby target of at least 1 ha;
- merging all 628 into their largest neighbour would change:
  - operability on 188 polygons / 79.35 ha;
  - CT eligibility on 216 / 94.16 ha;
  - `CONTCLAS` on 142 / 57.62 ha;
  - AU pair on about 506 / 216.74 ha;
- 172 small polygons / 78.64 ha carry AU_EX/AU_FU combinations that do not
  occur in any ≥1 ha polygon.

A blanket merge is therefore a strata/land-base edit, not a neutral sliver
cleanup.

## Recommendation

Do not merge all polygons below 1 ha.

Use an **attribute-safe merge** only where the small polygon and its largest
touching ≥1 ha neighbour share `Operabilit`, `CONTCLAS`, `CT_eligib`, `AU_EX`
and `AU_FU`.

- Safe pairs: **95**
- Area: **45.46 ha**
- The canonical inventory is not changed by default.
- The 0-1 ha harvest-opening rule remains a separate scheduling constraint: an
  isolated block should wait for a neighbouring block.

## Tooling

```bash
python scripts/small_polygons.py \
  --fragments models/mkrf_patchworks_model/spatial/fragments.shp \
  --summary-out runtime/small_polygons_summary.json \
  --small-out runtime/small_polygons.csv

# Optional conservative merge
python scripts/small_polygons.py \
  --fragments models/mkrf_patchworks_model/spatial/fragments.shp \
  --merge-out runtime/mkrf_fragments_attr_safe.gpkg \
  --merge-log runtime/mkrf_fragments_attr_safe.csv
```
