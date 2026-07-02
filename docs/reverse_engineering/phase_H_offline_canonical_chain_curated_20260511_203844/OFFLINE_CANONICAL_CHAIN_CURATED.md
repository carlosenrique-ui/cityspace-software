# Offline Canonical Chain Curated — IPT CitySpace

## Status

Curated analysis only.

No code was modified.

## Main conclusion

`offline/run_offline_pipeline.py` is the strongest current candidate for the official OFFLINE entrypoint.

## Reason

It has a `main()` function, runs the PCA alignment gate, uses `python -m offline.pipeline.<module>`, and executes scripts from `offline/pipeline`.

## Critical risk

The current runner executes all `offline/pipeline/*.py` files by sorted filename.

This may include backup, recompute, contour experiments, ESRI overlays, auxiliary products, and historical steps.

Therefore, `offline/run_offline_pipeline.py` is probably the right entrypoint, but the execution chain still needs curation.

## Proposed minimal canonical chain

### Gate

`offline/validation/validate_rotation_pca_grid.py`

### Entrypoint

`offline/run_offline_pipeline.py`

### Strong canonical candidates

- `offline/pipeline/01_build_scientific_grid.py`
- `offline/pipeline/02_compute_cell_metrics.py`
- `offline/pipeline/02_join_grid_metrics_with_geom.py`
- `offline/pipeline/03_scientific_to_semantic.py`
- `offline/pipeline/04_generate_actuator_plan.py`

## Supporting validation scripts

- `offline/validation/validate_contract_master.py`
- `offline/validation/validate_scientific_grid_metrics.py`
- `offline/validation/validate_rotation_pca_grid.py`

## Not minimal canonical yet

- `offline/pipeline/01_build_scientific_grid_BACKUP.py`
- `offline/pipeline/02b_build_grid_metrics_from_recompute.py`
- `offline/pipeline/02d_generate_poligono_urbanismo_ipt_outer.py`
- `offline/pipeline/03b_generate_contours_clean_UI.py`
- `offline/pipeline/03c_generate_contours_from_DTM_TRUE.py`
- `offline/pipeline/03d_apply_scientific_transform_to_dtm_contours.py`
- `offline/pipeline/03e_generate_grid_terrain_contours_nan_polygon.py`
- `offline/pipeline/03f_generate_rbf_terrain_contours_polygon.py`
- `offline/pipeline/04b_generate_actuator_geospatial.py`
- `offline/pipeline/05_apply_rotation_to_contours.py`
- `offline/pipeline/05_generate_grid_mask_from_polygon.py`
- `offline/pipeline/06_generate_esri_overlay_grid.py`
- `offline/pipeline/06b_esri_to_grid_simple.py`

## Required OFFLINE products for ONLINE/UI

- `offline/products/scientific/grid_metrics_utm.csv`
- `offline/products/runtime/grid.npy`
- `offline/products/runtime/actuator_plan.json`
- `offline/products/runtime/metadata.json`
- `offline/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_final.png`

## Architectural rule

The OFFLINE layer is the only producer of scientific and runtime products.

The ONLINE/UI layer must consume these products and must not recompute CRS, grid, altimetry, PCA, rotation, contours or actuator plan.

## Next recommended phase

FASE I — create a dry-run canonical manifest.

This manifest should list the intended canonical steps explicitly, without changing the current runner yet.
