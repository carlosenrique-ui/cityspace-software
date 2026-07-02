import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString
from shapely.affinity import rotate
from pathlib import Path

BASE = Path('offline/products/scientific')
IN_PATH = BASE / 'grid_8x16_enriched.gpkg'
OUT_PATH = BASE / 'grid_contours_clean.gpkg'

print('STEP 03 – CLEAN CONTOURS (UTM FIX)')

# carregar
gdf = gpd.read_file(IN_PATH, engine='pyogrio')

# 🔥 filtro urbano
gdf = gdf[(gdf['z_terrain_m'] > 0) | (gdf['z_building_m'] > 0)]

# ordenar
gdf = gdf.sort_values(['row','col'])

rows = int(gdf['row'].max() + 1)
cols = int(gdf['col'].max() + 1)

# matriz Z
Z = np.full((rows, cols), np.nan)

for _, r in gdf.iterrows():
    Z[int(r['row']), int(r['col'])] = r['z_terrain_m']

print('Z min/max:', np.nanmin(Z), np.nanmax(Z))

# 🔥 coordenadas UTM reais (CENTRO DAS CÉLULAS)
xs = gdf.groupby('col')['geometry'].first().centroid.x.sort_index().values
ys = gdf.groupby('row')['geometry'].first().centroid.y.sort_index().values

X, Y = np.meshgrid(xs, ys)

# níveis
levels = np.linspace(np.nanmin(Z), np.nanmax(Z), 10)

# contours
cs = plt.contour(X, Y, Z, levels=levels)

lines = []
values = []

for i, level in enumerate(cs.levels):
    segs = cs.allsegs[i]
    for seg in segs:
        if len(seg) > 1:
            lines.append(LineString(seg))
            values.append(level)

# 🔥 CRS correto
contours = gpd.GeoDataFrame({
    'elevation': values,
    'geometry': lines
}, crs=gdf.crs)

# 🔥 máscara urbana (agora FUNCIONA)
mask = gdf.geometry.union_all()
contours = contours[contours.intersects(mask)]

# rotação opcional
angle = 0
contours['geometry'] = contours['geometry'].apply(lambda g: rotate(g, angle, origin='center'))

# salvar
contours.to_file(OUT_PATH, driver='GPKG', engine='pyogrio')

print('Contours FINAL:', OUT_PATH)
