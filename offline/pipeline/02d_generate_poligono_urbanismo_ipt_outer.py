from pathlib import Path
import geopandas as gpd
from shapely.ops import unary_union
from shapely.geometry import Polygon, MultiPolygon

BASE = Path(__file__).resolve().parents[2]

INPUT = BASE / "offline/products/scientific/urban_envelope_scientific_rotated_clean.gpkg"
OUTPUT = BASE / "offline/products/scientific/poligono_urbanismo_ipt_outer.gpkg"

gdf = gpd.read_file(INPUT)

print("INPUT:", INPUT)
print("rows:", len(gdf))
print("crs:", gdf.crs)
print("bounds:", gdf.total_bounds)
print("geom types:", gdf.geometry.geom_type.value_counts().to_dict())

geom = unary_union(gdf.geometry)

# dissolve + limpeza
geom = geom.buffer(0)

# preencher buracos internos e corredores internos
# buffer positivo/negativo fecha vazios estreitos sem alterar muito a borda externa
geom = geom.buffer(35).buffer(-35)

# se ainda for MultiPolygon, mantém a maior parte
if isinstance(geom, MultiPolygon):
    geom = max(list(geom.geoms), key=lambda g: g.area)

# remove buracos internos explicitamente
if isinstance(geom, Polygon):
    geom = Polygon(geom.exterior)

# suavização leve da borda externa
geom = geom.simplify(5, preserve_topology=True)

out = gpd.GeoDataFrame(
    {"id": [1], "name": ["poligono_urbanismo_ipt_outer"]},
    geometry=[geom],
    crs=gdf.crs
)

out.to_file(OUTPUT)

print("========================================")
print("OUTPUT:", OUTPUT)
print("rows:", len(out))
print("bounds:", out.total_bounds)
print("area:", float(out.geometry.area.iloc[0]))
print("========================================")
