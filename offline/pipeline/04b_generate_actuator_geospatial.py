import geopandas as gpd
from pathlib import Path

BASE = Path('offline/products/scientific')

IN_PATH = BASE / 'grid_8x16_enriched.gpkg'
OUT_PATH = BASE / 'grid_8x16_actuators.gpkg'

print('STEP 04B – ACTUATOR GEOSPATIAL')

gdf = gpd.read_file(IN_PATH, engine='pyogrio')

print('Loaded:', gdf.shape)

gdf['zone_type'] = gdf['z_total_m'].apply(
    lambda z: 'HIGH_RISE' if z > 30 else ('MID_RISE' if z > 15 else 'LOW_RISE')
)

gdf['actuator_intensity'] = gdf['z_total_m'] / 10

gdf['risk_level'] = gdf['z_building_m'].apply(
    lambda z: 'HIGH' if z > 10 else ('MEDIUM' if z > 5 else 'LOW')
)

gdf.to_file(OUT_PATH, driver='GPKG', engine='pyogrio')

print('OUTPUT:', OUT_PATH)
