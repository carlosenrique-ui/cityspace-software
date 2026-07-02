# Offline Dependency Matrix — FASE L

## Status
Dependency matrix only.
No pipeline was executed.
No code was modified.
No runner was modified.

## Source
`docs/reverse_engineering/phase_K2_offline_manifest_io_inspection_20260511_210803/manifest_io_inspection_report.json`

## Matrix

| Script | Reads | Writes | Product paths | Execution risk | Risk level |
|---|---|---|---|---|---|
| `offline/pipeline/01_build_scientific_grid.py` | L15: gdf = gpd.read_file(INPUT_GPKG)<br>L85: with open(OUTPUT_DEBUG, "w") as f: | — | L11: INPUT_GPKG = "offline/products/scientific/grid_8x16_metric.gpkg"<br>L12: OUTPUT_DEBUG = "offline/products/scientific/grid_square_debug.txt" | — | LOW |
| `offline/pipeline/02_compute_cell_metrics.py` | — | — | — | — | LOW |
| `offline/pipeline/02_join_grid_metrics_with_geom.py` | L18: df = pd.read_csv(CSV_PATH)<br>L21: gdf = gpd.read_file(GPKG_PATH) | L59: gdf_merged.to_file(OUT_PATH, driver="GPKG") | L8: BASE = Path("offline/products/scientific") | — | LOW |
| `offline/pipeline/03_scientific_to_semantic.py` | — | — | — | — | LOW |
| `offline/pipeline/04_generate_actuator_plan.py` | L28: gdf = gpd.read_file(INPUT_GPKG)<br>L29: mask = gpd.read_file(MASK_GPKG) | L106: df_out.to_csv(OUTPUT_CSV, index=False) | L13: INPUT_GPKG = ENGINE_ROOT / "offline/products/scientific/grid_8x16_enriched.gpkg"<br>L14: MASK_GPKG = ENGINE_ROOT / "offline/products/scientific/urban_envelope_scientific_rotated.gpkg" | — | LOW |
| `offline/run_offline_pipeline.py` | — | — | — | L58: subprocess.run( | CONTROLLED_RISK |
| `offline/validation/validate_rotation_pca_grid.py` | L162: df = pd.read_csv(csv_path) | L203: out_dir.mkdir(parents=True, exist_ok=True)<br>L205: out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8") | — | — | LOW |

## Controlled findings

- The canonical OFFLINE manifest contains 7 Python files.
- Static inspection found read/write dependencies without executing the pipeline.
- `offline/run_offline_pipeline.py` contains `subprocess.run()`, which is expected for a runner but must remain explicitly controlled.
- Some wrapper steps delegate behavior through imports, so their real I/O may live in imported modules.

## Next safe phase

FASE M — inspect delegated imported modules used by wrapper steps, still without executing the pipeline.
