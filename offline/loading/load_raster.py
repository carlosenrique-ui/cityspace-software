# offline/loading/load_raster.py

import rasterio
from pathlib import Path


def load_raster(path):
    """
    OFFLINE / LOADING
    -----------------
    Lê um raster (DSM ou DTM) e retorna:
    - array (banda 1)
    - metadata completa

    CONTRATO:
    - NÃO normaliza
    - NÃO reprojeta
    - NÃO corrige valores
    """

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"[LoadRaster] Arquivo não encontrado: {path}")

    print(f"[LoadRaster] Lendo raster: {path}")

    with rasterio.open(path) as src:
        array = src.read(1)
        meta = src.meta.copy()

    print("[LoadRaster] OK")
    print(f"[LoadRaster] Shape: {array.shape}")
    print(f"[LoadRaster] CRS: {meta.get('crs')}")

    return array, meta
