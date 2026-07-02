# offline/loading/load_vector.py

import geopandas as gpd
from pathlib import Path


def load_vector(path):
    """
    OFFLINE / LOADING
    -----------------
    Lê um vetor (ex: DXF) e retorna um GeoDataFrame.

    CONTRATO IMPORTANTE:
    - NÃO valida CRS
    - NÃO atribui CRS
    - NÃO reprojeta
    - NÃO corrige geometria
    - Apenas lê e inspeciona

    Qualquer correção geométrica deve ocorrer em offline/geo
    """

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"[LoadVector] Arquivo não encontrado: {path}")

    print(f"[LoadVector] Lendo vetor: {path}")

    gdf = gpd.read_file(path)

    print("[LoadVector] OK")
    print(f"[LoadVector] Total de feições: {len(gdf)}")
    print(f"[LoadVector] CRS: {gdf.crs}")

    if "Layer" in gdf.columns:
        print("[LoadVector] Layers encontrados:")
        print(gdf["Layer"].value_counts())

    print("[LoadVector] Tipos de geometria:")
    print(gdf.geometry.geom_type.value_counts())

    return gdf
