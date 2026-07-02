import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy as np

def reproject_raster(src_array, src_meta, target_crs):
    print("[ReprojectRaster] Iniciando reprojeção do raster")

    src_crs = src_meta["crs"]
    if src_crs == target_crs:
        print("[ReprojectRaster] Raster já está no CRS destino")
        return src_array, src_meta

    transform, width, height = calculate_default_transform(
        src_crs,
        target_crs,
        src_meta["width"],
        src_meta["height"],
        *src_meta["bounds"]
    )

    dst_array = np.zeros((height, width), dtype=src_array.dtype)

    reproject(
        source=src_array,
        destination=dst_array,
        src_transform=src_meta["transform"],
        src_crs=src_crs,
        dst_transform=transform,
        dst_crs=target_crs,
        resampling=Resampling.nearest
    )

    dst_meta = src_meta.copy()
    dst_meta.update({
        "crs": target_crs,
        "transform": transform,
        "width": width,
        "height": height
    })

    print(f"[ReprojectRaster] Novo shape: {dst_array.shape}")
    print("[ReprojectRaster] Reprojeção concluída\n")

    return dst_array, dst_meta
