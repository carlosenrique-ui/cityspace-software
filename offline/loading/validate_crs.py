# offline/loading/validate_crs.py

def validate_crs(raster_meta, vector_gdf):
    """
    OFFLINE / LOADING
    -----------------
    Valida se raster e vetor possuem CRS compatível.

    REGRAS:
    - Raster SEMPRE deve ter CRS
    - Vetor SEM CRS é ERRO (não será assumido automaticamente)
    - Nenhuma reprojeção ocorre aqui
    """

    raster_crs = raster_meta.get("crs")
    vector_crs = vector_gdf.crs

    if raster_crs is None:
        raise RuntimeError("[ValidateCRS] Raster sem CRS. Pipeline interrompido.")

    if vector_crs is None:
        raise RuntimeError(
            "[ValidateCRS] Vetor (DXF) sem CRS.\n"
            "Georreferenciamento explícito é obrigatório em offline/geo."
        )

    if raster_crs != vector_crs:
        raise RuntimeError(
            "[ValidateCRS] CRS incompatíveis.\n"
            f"Raster: {raster_crs}\n"
            f"Vetor:  {vector_crs}\n"
            "Reprojeção deve ocorrer em offline/geo."
        )

    print("[ValidateCRS] OK — CRS compatíveis.")
