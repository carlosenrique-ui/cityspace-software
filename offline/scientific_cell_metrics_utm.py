import geopandas as gpd, rasterio, numpy as np, pandas as pd
from rasterio.mask import mask
from shapely.geometry import box

GRID = "offline/products/scientific/grid_8x16_metric.gpkg"
DSM = "offline/data/processed/dsm/IPT_2018_DSM_CLIP.tif"
DTM = "offline/data/processed/dtm/IPT_2018_DTM_CLIP.tif"
OUT = "products/final/grid_height.csv"


def main():
    print("SCIENTIFIC CELL METRICS UTM (FINAL MAX+MEDIAN+SHIFT)")

    gdf = gpd.read_file(GRID, engine="pyogrio")
    dsm = rasterio.open(DSM)
    dtm = rasterio.open(DTM)

    rb = box(*dtm.bounds)
    gdf = gdf[gdf.intersects(rb)].copy()

    rows = []

    for _, row in gdf.iterrows():
        geom = [row.geometry]

        try:
            dsm_img, _ = mask(dsm, geom, crop=True)
            dtm_img, _ = mask(dtm, geom, crop=True)
        except:
            continue

        dsm_vals = dsm_img[0]
        dtm_vals = dtm_img[0]

        m = (dsm_vals != dsm.nodata) & (dtm_vals != dtm.nodata)

        if not np.any(m):
            continue

        dsm_vals = dsm_vals[m]
        dtm_vals = dtm_vals[m]

        z_terrain = np.median(dtm_vals)
        z_building = np.max(dsm_vals - dtm_vals)
        z_total = z_terrain + z_building

        rows.append(
            {
                "row": row["row"],
                "col": row["col"],
                "z_terrain": float(z_terrain),
                "z_building": float(z_building),
                "z_total": float(z_total),
            }
        )

    df = pd.DataFrame(rows)

    shift = -df["z_total"].min()
    df["z_total"] += shift
    df["z_terrain"] += shift

    df.to_csv(OUT, index=False)

    print("Saved:", OUT)
    print("Cells:", len(df))
    print("Shift:", shift)
    print("Z max:", df["z_total"].max())


if __name__ == "__main__":
    main()
