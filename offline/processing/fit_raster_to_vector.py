import numpy as np
from affine import Affine

def fit_raster_to_vector(raster_array, raster_meta, vector_gdf):
    """
    Ajusta o raster para o sistema local do vetor (mesa).
    Recalcula o transform usando o bounding box do vetor.
    """

    print("[FitRaster] Ajustando raster ao sistema local da mesa")

    minx, miny, maxx, maxy = vector_gdf.total_bounds

    height, width = raster_array.shape

    px = (maxx - minx) / width
    py = (maxy - miny) / height

    transform = Affine.translation(minx, maxy) * Affine.scale(px, -py)

    raster_meta = raster_meta.copy()
    raster_meta.update({
        "transform": transform,
        "crs": None  # sistema local da mesa
    })

    print("[FitRaster] Novo transform definido")
    print("[FitRaster] Sistema local aplicado\n")

    return raster_array, raster_meta
