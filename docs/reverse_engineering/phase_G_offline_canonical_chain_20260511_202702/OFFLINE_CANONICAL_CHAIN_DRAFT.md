# Offline Canonical Chain Draft — IPT CitySpace

## Status

Diagnostic draft only.

No code was modified.

## Goal

Identify the canonical OFFLINE execution chain that produces the scientific/runtime products consumed by the ONLINE/UI layer.

## Candidate official entrypoints to inspect

- `offline/run_offline_pipeline.py`
- `offline/pipeline_runner.py`
- `offline/scientific_runner.py`
- `offline/raster/pipeline/scientific_raster_runner.py`

## Candidate numbered pipeline scripts

See:

`02_pipeline_numbered_files.txt`

## Execution traces

See:

`04_execution_traces.txt`

## I/O contract

See:

`05_pipeline_io_contract.txt`

## Validation gates

See:

`06_validation_gates.txt`

## Online-consumable products

Expected products:

- `offline/products/scientific/grid_metrics_utm.csv`
- `offline/products/runtime/grid.npy`
- `offline/products/runtime/actuator_plan.json`
- `offline/products/runtime/metadata.json`
- `offline/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_final.png`

See:

`07_online_consumable_products_traces.txt`

## Provisional architectural rule

The canonical OFFLINE chain must be the only producer of products consumed by ONLINE/UI.

The ONLINE/UI layer must not recompute scientific grid, altimetry, CRS, contours, rotation, PCA, or actuator plan.

## Next decision after this phase

Select one of the following:

1. `offline/run_offline_pipeline.py` is the canonical entrypoint
2. `offline/pipeline_runner.py` is the canonical entrypoint
3. A new documented runner is needed later, but not yet created
