# MKRF full-estate 3D scene

`mkrf_scene.json` is the WS4 studio-3D scene pack for the Malcolm Knapp
Research Forest instance.

- 1,763 public block polygons covering 4,810.85 ha
- 2016 LidarBC 5 m CHM and 1 m DEM terrain/canopy
- CHM coverage is 99.6% of the block area; CHM no-data gaps are filled from
  block height for display only and are labelled as fallback, not measured
  canopy
- approximately 3.58M synthetic stem positions at block density
- block density and height come from the WS4 matrix; species composition comes
  from the MKRF AU summary
- the scene starts on a central production block and opens at a stand-scale
  camera; use the in-scene **Render all trees** control for the full-tree field
  or the LOD view on a smaller GPU
- source: MKRF public block geometry, 2016 LidarBC DEM/CHM, WS4 matrix, and AU
  summary

The scene is a visual screening product, not a measured tree inventory. The
reported CHM fraction is a coverage diagnostic; it is not a canopy-height
validation.

The scene JSON is a generated deployment artifact. The metrics table used to
build it is tracked so the scene can be regenerated:

```bash
python ../../../fhops-public-demo/scripts/build_afrf_studio3d.py \
  --blocks ws4/runtime/fragments.geojson \
  --metrics planning/fhops/mkrf_scene_metrics.csv \
  --id-field block_id \
  --density-field density \
  --height-field height_m \
  --species-field species \
  --au-field au_id \
  --resolution 15 \
  --dem "$MKRF_DEM" \
  --chm "$MKRF_CHM" \
  --label "MKRF full estate" \
  --subtitle "Mackenzie River Forest — all blocks; 2016 LidarBC CHM; stems synthesised at block density." \
  --source-note "LidarBC 2016 5 m CHM and 1 m DEM; MKRF public block geometry; block density, height and species mix from the WS4 matrix and AU summary. Stem positions are synthetic, not measured." \
  --out planning/studio3d/mkrf_scene.json
```

`$MKRF_DEM` and `$MKRF_CHM` are the extracted LidarBC raster paths supplied by
the deployment environment.
