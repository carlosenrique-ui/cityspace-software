import geopandas as gpd
import numpy as np
from shapely.geometry import box
from shapely.affinity import scale, translate

def build_mask_local_grid(grid_meta, shapefile_path):
    """
    FASE B — Máscara de edifícios em grid local da mesa (1cm)

    Pipeline LOCAL correto:
    1. Carrega shapefile (sem CRS)
    2. Translada para origem (0,0)
    3. ESCALA para dimensões físicas da mesa (8x16 cm)
    4. Interseção célula × polígono
    """

    print("[MaskLocal] Construindo máscara local de edifícios")

    # ------------------------------------------------------------
    # METADADOS DO GRID DA MESA
    # ------------------------------------------------------------
    n_rows = grid_meta["rows"]      # 8
    n_cols = grid_meta["cols"]      # 16
    cell_size = grid_meta["cell_size"]  # 1 cm

    mesa_width  = n_cols * cell_size   # 16 cm
    mesa_height = n_rows * cell_size   # 8 cm

    print(f"[MaskLocal] Mesa física: {mesa_width} x {mesa_height} cm")

    # ------------------------------------------------------------
    # CARREGAR SHAPEFILE (SISTEMA LOCAL)
    # ------------------------------------------------------------
    gdf = gpd.read_file(shapefile_path)

    print(f"[MaskLocal] Edifícios carregados: {len(gdf)}")
    print("[MaskLocal] CRS ignorado (sistema local da mesa)")

    # ------------------------------------------------------------
    # NORMALIZAÇÃO (OFFSET)
    # ------------------------------------------------------------
    minx, miny, maxx, maxy = gdf.total_bounds
    print(f"[MaskLocal] Bounds originais: {minx, miny, maxx, maxy}")

    gdf["geometry"] = gdf.geometry.apply(
        lambda g: translate(g, xoff=-minx, yoff=-miny)
    )

    minx, miny, maxx, maxy = gdf.total_bounds
    print(f"[MaskLocal] Bounds após offset: {minx, miny, maxx, maxy}")

    # ------------------------------------------------------------
    # ESCALONAMENTO PARA A MESA FÍSICA
    # ------------------------------------------------------------
    scale_x = mesa_width  / maxx
    scale_y = mesa_height / maxy

    print(f"[MaskLocal] Aplicando escala:")
    print(f"            scale_x = {scale_x}")
    print(f"            scale_y = {scale_y}")

    gdf["geometry"] = gdf.geometry.apply(
        lambda g: scale(g, xfact=scale_x, yfact=scale_y, origin=(0, 0))
    )

    minx, miny, maxx, maxy = gdf.total_bounds
    print(f"[MaskLocal] Bounds finais (mesa): {minx, miny, maxx, maxy}")

    # ------------------------------------------------------------
    # CONSTRUÇÃO DA MÁSCARA LOCAL
    # ------------------------------------------------------------
    mask = np.zeros((n_rows, n_cols), dtype=np.uint8)

    for r in range(n_rows):
        for c in range(n_cols):
            x0 = c * cell_size
            y0 = r * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size

            cell = box(x0, y0, x1, y1)

            for geom in gdf.geometry:
                if geom is not None and geom.intersects(cell):
                    mask[r, c] = 1
                    break

    pixels = int(mask.sum())
    print(f"[MaskLocal] Células marcadas como edifício: {pixels}")
    print("[MaskLocal] Máscara local construída com sucesso\n")

    return mask
