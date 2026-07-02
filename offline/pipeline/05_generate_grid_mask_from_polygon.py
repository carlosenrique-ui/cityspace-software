from pathlib import Path
import pandas as pd
import geopandas as gpd

BASE = Path(__file__).resolve().parents[2]

GRID_GPKG = BASE / "offline/products/scientific/grid_8x16_enriched.gpkg"
GRID_CSV = BASE / "offline/products/scientific/grid_metrics_utm.csv"

POLYGON_CANDIDATES = [
    BASE / "offline/products/scientific/poligono_urbanismo_ipt_outer_real.gpkg",
    BASE / "offline/products/scientific/urban_envelope_scientific_rotated_clean.gpkg",
    BASE / "offline/products/scientific/urban_envelope_scientific_rotated.gpkg",
    BASE / "offline/products/scientific/urban_envelope_scientific.gpkg",
]

OUT_GPKG = BASE / "offline/products/scientific/grid_8x16_enriched_masked.gpkg"
OUT_CSV = BASE / "offline/products/scientific/grid_metrics_utm_masked.csv"

print("========================================")
print("05 — GRID MASK FROM POLÍGONO")
print("========================================")

polygon_path = next((p for p in POLYGON_CANDIDATES if p.exists()), None)
if polygon_path is None:
    print("Candidatos não encontrados:")
    for p in POLYGON_CANDIDATES:
        print(" -", p)
    raise FileNotFoundError("Polígono urbanístico não encontrado.")

grid = gpd.read_file(GRID_GPKG)
poly = gpd.read_file(polygon_path)

if grid.crs != poly.crs:
    poly = poly.to_crs(grid.crs)

polygon_union = poly.geometry.union_all()

grid["cell_area"] = grid.geometry.area
grid["intersection_area"] = grid.geometry.intersection(polygon_union).area
grid["inside_ratio"] = grid["intersection_area"] / grid["cell_area"]
grid["is_inside_polygon"] = grid["inside_ratio"] >= 0.20

print("POLYGON:", polygon_path)
print("Total células:", len(grid))
print("Dentro:", int(grid["is_inside_polygon"].sum()))
print("Fora:", int((~grid["is_inside_polygon"]).sum()))

grid.to_file(OUT_GPKG, driver="GPKG")

df = pd.read_csv(GRID_CSV)
mask_cols = grid[["row", "col", "inside_ratio", "is_inside_polygon"]].copy()
df = df.merge(mask_cols, on=["row", "col"], how="left")
df["inside_ratio"] = df["inside_ratio"].fillna(0.0)
df["is_inside_polygon"] = df["is_inside_polygon"].fillna(False)

df.to_csv(OUT_CSV, index=False)

print("OUTPUT_CSV:", OUT_CSV)
print("OUTPUT_GPKG:", OUT_GPKG)
print("========================================")
