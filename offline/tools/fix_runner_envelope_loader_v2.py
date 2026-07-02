from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
FILE = BASE / "offline/raster/pipeline/scientific_raster_runner.py"

code = FILE.read_text()

# remover import fiona
code = code.replace("import fiona", "")

# substituir leitura do envelope
code = code.replace(
    'with fiona.open(ENVELOPE) as shp:',
    'import geopandas as gpd\n    gdf = gpd.read_file(ENVELOPE)'
)

# substituir linha geom
code = code.replace(
    'geom = shape(shp[0]["geometry"])',
    'geom = gdf.geometry.iloc[0]'
)

FILE.write_text(code)

print("✔ Runner atualizado para usar geopandas (sem fiona)")