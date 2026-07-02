# Online Contract Compact — V128.7.19

## Canonical UI

`online/ui/dash_v128_7_19_menu_final.py`

## Inputs consumed

- `offline/products/scientific/grid_metrics_utm.csv`
- `offline/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_final.png`
- `online/assets/north_arrow_scale.png`

## Grid

- 8 rows
- 16 columns
- 128 total cells

## Rendering pipeline

Main function:

`make_fig(layers, step, cell_mode, projector_mode)`

Layer order:

1. Base IPT watermark/image
2. Current pino heatmap from `current_grid(step)`
3. Terrain contours
4. Total/teto contours
5. Grid lines
6. Active cell shape
7. Text annotations
8. North/scale asset

## Motion contract

Zigzag is column-based.

Start:

`row=0, col=0`

Rule:

- even columns: top to bottom
- odd columns: bottom to top

## Dash callbacks

Main callbacks:

- `update_cartographic_scale`
- `toggle_menu`
- `control_loop`
- `update_ui`

## Control loop

Controls currently present:

- Forward
- Back
- Pause
- Reset

The reset button still exists in the frozen UI.

## Mesa Real

`send_to_real_table(row, col, value_cm, mesa_on)`

Current behavior:

- OFF: returns `Mesa Real OFF`
- ON: returns simulated message only

No real serial, ACK, retry or hardware protocol is connected yet.

## Projector mode

`projector_mode = "normal"` is hardcoded inside `update_ui()`.

The inverted mode exists inside `make_fig()`, but is not exposed in the current callback flow.

## Status text still contains

- `REAL lento`
- `VIRTUAL acelerado`
- `projector=normal`

## Architectural conclusion

V128.7.19 is a valid frozen online baseline.

It should not be modified directly.

Any next UI change should be created as a copied working version, for example:

`online/ui/dash_v128_7_20_work_from_719.py`
