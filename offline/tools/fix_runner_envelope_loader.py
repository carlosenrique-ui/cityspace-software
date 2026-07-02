from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
FILE = BASE / "offline/raster/pipeline/scientific_raster_runner.py"

code = FILE.read_text()

old = """
with fiona.open(ENVELOPE) as shp:
    geom = shape(shp[0]["geometry"])
"""

new = """
import geopandas as gpd

gdf = gpd.read_file(
    ENVELOPE,
    layer="urban_envelope_scientific_rotated_clean"
)

geom = gdf.geometry.iloc[0]
"""

code = code.replace(old, new)

FILE.write_text(code)

print("Runner envelope loader corrigido")