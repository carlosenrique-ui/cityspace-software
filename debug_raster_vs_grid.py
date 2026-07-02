import rasterio
import geopandas as gpd

print("==== DEBUG START ====")

r = rasterio.open("offline/data/processed/dtm/IPT_2018_DTM_CLIP.tif")
print("RASTER CRS:", r.crs)

gdf = gpd.read_file("offline/products/scientific/grid_8x16_metric.gpkg", engine="pyogrio")
print("GRID CRS:", gdf.crs)

geom = gdf.geometry.iloc[0]
x, y = geom.centroid.x, geom.centroid.y

print("Sample point:", x, y)

val = list(r.sample([(x, y)]))[0][0]

print("Sample value:", val)

print("==== DEBUG END ====")
