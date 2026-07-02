"""
Alinhamento explícito de vetor em sistema local
para o espaço do raster (UTM).

Este módulo NÃO reprojeta CRS.
Ele aplica um shift + escala afim baseado nos extents.
"""

import geopandas as gpd
from shapely.affinity import scale, translate

def align_vector_to_raster(gdf, raster_bounds):
    """
    Ajusta o vetor (em sistema local) para o espaço do raster.

    raster_bounds: (minx, miny, maxx, maxy)
    """

    v_minx, v_miny, v_maxx, v_maxy = gdf.total_bounds
    r_minx, r_miny, r_maxx, r_maxy = raster_bounds

    # Escalas relativas
    scale_x = (r_maxx - r_minx) / (v_maxx - v_minx)
    scale_y = (r_maxy - r_miny) / (v_maxy - v_miny)

    gdf_scaled = gdf.copy()
    gdf_scaled["geometry"] = gdf_scaled.geometry.apply(
        lambda geom: scale(
            geom,
            xfact=scale_x,
            yfact=scale_y,
            origin=(v_minx, v_miny)
        )
    )

    # Translação para encaixar no raster
    gdf_aligned = gdf_scaled.copy()
    gdf_aligned["geometry"] = gdf_scaled.geometry.apply(
        lambda geom: translate(
            geom,
            xoff=r_minx - v_minx * scale_x,
            yoff=r_miny - v_miny * scale_y
        )
    )

    return gdf_aligned
