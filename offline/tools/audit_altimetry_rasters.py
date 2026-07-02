from pathlib import Path
import rasterio

ROOT = Path(__file__).resolve().parents[2]

print("\nIPT-CitySpace – Altimetry Raster Audit\n")

paths = [
"offline/products/snapshots/ipt_fase0/z_terrain_real.tif",
"offline/products/snapshots/ipt_fase0/z_building_real.tif",
"offline/products/snapshots/ipt_fase0/z_total_real.tif",
"offline/products/snapshots/ipt_fase1_1cm/z_total_rotated.tif",
]

for p in paths:

    path = ROOT / p

    if not path.exists():
        print("MISSING:", p)
        continue

    with rasterio.open(path) as src:
        data = src.read(1)

    print("\nFILE:", p)
    print("shape:", data.shape)
    print("min:", float(data.min()))
    print("max:", float(data.max()))

print("\nRaster audit finished.\n")