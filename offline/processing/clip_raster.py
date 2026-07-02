import rasterio
from rasterio.mask import mask
import numpy as np

def clip_raster_by_vector(raster_array, raster_meta, vector_gdf):
    """
    Recorta o raster usando a extensão do vetor.
    Retorna raster e metadata compatíveis com rasterização.
    """

    print("[ClipRaster] Recortando raster pela extensão do vetor")

    geometries = [geom for geom in vector_gdf.geometry if geom is not None]

    if not geometries:
        raise RuntimeError("[ClipRaster] Vetor sem geometrias válidas")

    with rasterio.io.MemoryFile() as memfile:
        with memfile.open(**raster_meta) as dataset:
            dataset.write(raster_array, 1)

            out_image, out_transform = mask(
                dataset,
                geometries,
                crop=True,
                filled=True,
                nodata=raster_meta.get("nodata", 0)
            )

    out_meta = raster_meta.copy()
    out_meta.update({
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform
    })

    print(f"[ClipRaster] Novo shape: {out_image.shape[1:]}")
    return out_image[0], out_meta
