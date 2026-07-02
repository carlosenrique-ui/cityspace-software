import rasterio
import pyogrio
from pathlib import Path

print("\n=================================================")
print("IPT-CitySpace – VALIDAÇÃO RASTER ROTADO vs ENVELOPE")
print("=================================================\n")

BASE = Path.cwd()

RASTER_PATH = BASE / "offline/data/processed/dsm/IPT_2018_DSM_ROT.tif"
ENVELOPE_PATH = BASE / "offline/products/scientific/urban_envelope_scientific_rotated_clean.gpkg"

# -------------------------------------------------

# Raster

# -------------------------------------------------

print("[1/2] Lendo raster rotacionado...")

with rasterio.open(RASTER_PATH) as src:


    bounds = src.bounds

print("\nRaster bounds:")
print("left   :", bounds.left)
print("right  :", bounds.right)
print("bottom :", bounds.bottom)
print("top    :", bounds.top)


# -------------------------------------------------

# Envelope

# -------------------------------------------------

print("\n[2/2] Lendo envelope rotacionado...")

df = pyogrio.read_dataframe(ENVELOPE_PATH)

geom = df.geometry.iloc[0]
env = geom.bounds

print("\nEnvelope bounds:")
print("left   :", env[0])
print("right  :", env[2])
print("bottom :", env[1])
print("top    :", env[3])

# -------------------------------------------------

# Diagnóstico

# -------------------------------------------------

print("\n=================================================")
print("DIAGNÓSTICO")
print("=================================================")

dx = env[0] - bounds.left
dy = env[1] - bounds.bottom

print("\nΔX (envelope - raster):", dx)
print("ΔY (envelope - raster):", dy)

print("\nSe ΔX ou ΔY forem grandes,")
print("o raster rotacionado não está no mesmo referencial.\n")
