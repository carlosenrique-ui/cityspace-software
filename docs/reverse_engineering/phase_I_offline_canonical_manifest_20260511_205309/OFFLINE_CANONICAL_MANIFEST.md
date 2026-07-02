# OFFLINE Canonical Manifest — IPT CitySpace

Status: dry-run documentation only.

Does not execute pipeline.
Does not modify code.
Does not modify runner.

Entrypoint candidate: `offline/run_offline_pipeline.py`

Validation gate: `offline/validation/validate_rotation_pca_grid.py`

Canonical steps:
1. `offline/pipeline/01_build_scientific_grid.py`
2. `offline/pipeline/02_compute_cell_metrics.py`
3. `offline/pipeline/02_join_grid_metrics_with_geom.py`
4. `offline/pipeline/03_scientific_to_semantic.py`
5. `offline/pipeline/04_generate_actuator_plan.py`

Required ONLINE products:
- `offline/products/scientific/grid_metrics_utm.csv`
- `offline/products/runtime/grid.npy`
- `offline/products/runtime/actuator_plan.json`
- `offline/products/runtime/metadata.json`
- `offline/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_final.png`
