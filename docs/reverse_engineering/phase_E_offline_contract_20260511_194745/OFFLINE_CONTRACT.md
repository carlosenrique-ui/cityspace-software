# Offline Contract — IPT CitySpace

## Status

Reverse-engineered from the current `offline/` tree.

No code was modified in this phase.

## Core scientific rule

`z_total_m = z_terrain_m + z_building_m`

## Offline responsibility

The OFFLINE layer is responsible for the scientific/geospatial processing of the IPT CitySpace system.

It prepares deterministic products that are consumed by the ONLINE/UI layer.

## Main expected products

- `offline/products/scientific/grid_metrics_utm.csv`
- `offline/products/runtime/grid.npy`
- `offline/products/runtime/actuator_plan.json`
- `offline/products/runtime/metadata.json`
- `offline/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_final.png`

## Architectural rule

The ONLINE/UI layer must consume OFFLINE products.

The ONLINE/UI layer must not recompute the scientific/geospatial pipeline.

## Contract conclusion

The OFFLINE system should be treated as the canonical producer of scientific products.

Any future 3D, Cesium, traffic, carbon or tangible-table integration should consume this contract instead of bypassing it.
