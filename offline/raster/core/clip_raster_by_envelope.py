import rasterio
from rasterio.mask import mask
import pyogrio
from pathlib import Path


def clip_raster_by_envelope(raster_path, envelope_path, output_path):
    print("\n[CLIP RASTER]")
    print("Raster:", raster_path)
    print("Envelope:", envelope_path)

    # carregar envelope com pyogrio
    gdf = pyogrio.read_dataframe(envelope_path)

    geom = [gdf.geometry.iloc[0]]

    with rasterio.open(raster_path) as src:

        print("Raster bounds:", src.bounds)
        print("Raster CRS:", src.crs)

        out_image, out_transform = mask(
            src,
            geom,
            crop=True
        )

        out_meta = src.meta.copy()

    out_meta.update(
        {
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform,
        }
    )

    with rasterio.open(output_path, "w", **out_meta) as dest:
        dest.write(out_image)

    print("[OK] Saved:", output_path)