def align_data(raster_meta, vector_gdf):
    """
    Estado OFF-LINE: AlignData
    --------------------------
    Sistema LOCAL da mesa.

    - Não reprojeta
    - Não translada
    - Apenas valida consistência conceitual
    """

    print("[AlignData] Iniciando alinhamento conceitual")

    raster_crs = raster_meta.get("crs")
    vector_crs = vector_gdf.crs

    print(f"[AlignData] CRS raster: {raster_crs}")
    print(f"[AlignData] CRS vetor : {vector_crs}")

    print("[AlignData] Sistema local assumido.")
    print("[AlignData] Nenhuma transformação aplicada.\n")

    return vector_gdf
