import numpy as np
from rasterio.features import rasterize

def rasterize_mask(vector_gdf, raster_meta):
    """
    Rasteriza polígonos de edifícios sobre a grade do raster.
    Retorna máscara binária:
      1 = edifício
      0 = fundo
    """

    print("[Rasterize] Iniciando rasterizacao da mascara")

    height = raster_meta["height"]
    width = raster_meta["width"]
    transform = raster_meta["transform"]

    print(f"[Rasterize] Raster shape: ({height}, {width})")

    # geometria → valor 1
    shapes = [(geom, 1) for geom in vector_gdf.geometry if geom is not None]

    print(f"[Rasterize] Geometrias para rasterizacao: {len(shapes)}")

    mask = rasterize(
        shapes=shapes,
        out_shape=(height, width),
        transform=transform,
        fill=0,
        dtype="uint8",
        all_touched=True  # <- CRÍTICO
    )

    pixels = int(mask.sum())
    print(f"[Rasterize] Pixels de edificio: {pixels}")
    print("[Rasterize] Rasterizacao concluida\n")

    return mask
