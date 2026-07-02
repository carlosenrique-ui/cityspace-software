import pandas as pd
import geopandas as gpd
from pathlib import Path

# =========================================
# PATHS
# =========================================
BASE = Path("offline/products/scientific")

CSV_PATH = BASE / "grid_metrics_utm.csv"
GPKG_PATH = BASE / "grid_8x16_metric.gpkg"
OUT_PATH = BASE / "grid_8x16_enriched.gpkg"

# =========================================
# LOAD
# =========================================
print("📥 Loading CSV...")
df = pd.read_csv(CSV_PATH)

print("📥 Loading GPKG...")
gdf = gpd.read_file(GPKG_PATH)

print("📊 Shapes:")
print("CSV:", df.shape)
print("GPKG:", gdf.shape)

# =========================================
# CHECK KEYS
# =========================================
required_cols = ["row", "col"]

for col in required_cols:
    if col not in df.columns:
        raise Exception(f"❌ CSV missing column: {col}")
    if col not in gdf.columns:
        raise Exception(f"❌ GPKG missing column: {col}")

# =========================================
# JOIN
# =========================================
print("🔗 Performing JOIN on (row, col)...")

gdf_merged = gdf.merge(df, on=["row", "col"], how="left")

# =========================================
# VALIDATION
# =========================================
nulls = gdf_merged["z_total_m"].isna().sum()

if nulls > 0:
    print(f"⚠️ WARNING: {nulls} células sem match!")
else:
    print("✅ JOIN completo (sem perdas)")

# =========================================
# EXPORT
# =========================================
print("💾 Saving enriched GPKG...")
gdf_merged.to_file(OUT_PATH, driver="GPKG")

print("✅ OUTPUT:", OUT_PATH)
