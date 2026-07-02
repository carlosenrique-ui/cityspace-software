#!/usr/bin/env python3
# ==========================================================
# VALIDAÇÃO DXF IPT — ROTACIONADO (VERSÃO LIMPA)
#
# Características:
#   - Rotação global rígida (154.63°)
#   - Origem = centro do envelope do DXF
#   - Ruas neutras
#   - Edifícios com preenchimento
#   - Fundo branco
#   - SEM norte
#   - SEM título
#
# Esta versão é a base visual oficial do IPT rotacionado
#
# Autor: Carlos E. H. Simoes
# ==========================================================

import os
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.affinity import rotate
from datetime import datetime

# ----------------------------------------------------------
# CONFIGURAÇÃO
# ----------------------------------------------------------
DXF_PATH = "/mnt/c/IPT-CitySpace-2018/data/dxf/IPT-2018-DXF.dxf"

OUT_DIR = "visualization/debug"
OUT_PNG = f"{OUT_DIR}/ipt_dxf_original_rotacionado_CLEAN.png"

ANGLE_DEG = 154.63

os.makedirs(OUT_DIR, exist_ok=True)

# ----------------------------------------------------------
def log(msg):
    print(msg)

# ----------------------------------------------------------
def main():

    log("=" * 72)
    log("VALIDAÇÃO DXF IPT — ROTACIONADO (LIMPO)")
    log(f"Arquivo origem: {DXF_PATH}")
    log(f"Rotação aplicada: {ANGLE_DEG:.2f}°")
    log(f"Início: {datetime.now()}")
    log("=" * 72)

    # ------------------------------------------------------
    # Carregar DXF
    # ------------------------------------------------------
    gdf = gpd.read_file(DXF_PATH, layer="entities")

    # ------------------------------------------------------
    # Centro GLOBAL do DXF
    # ------------------------------------------------------
    minx, miny, maxx, maxy = gdf.total_bounds
    cx = (minx + maxx) / 2
    cy = (miny + maxy) / 2

    log(f"[ROT] Centro global do DXF: ({cx:.3f}, {cy:.3f})")

    # ------------------------------------------------------
    # Rotação GLOBAL (corpo rígido)
    # ------------------------------------------------------
    gdf["geometry"] = gdf["geometry"].apply(
        lambda g: rotate(g, ANGLE_DEG, origin=(cx, cy), use_radians=False)
    )

    # ------------------------------------------------------
    # Separação de camadas
    # ------------------------------------------------------
    ruas = gdf[gdf.geom_type.isin(["LineString", "MultiLineString"])]
    edificios = gdf[gdf.geom_type.isin(["Polygon", "MultiPolygon"])]

    # ------------------------------------------------------
    # PLOT (FUNDO BRANCO)
    # ------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect("equal")
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    # Ruas — neutras
    if len(ruas) > 0:
        ruas.plot(
            ax=ax,
            color="#9e9e9e",
            linewidth=0.7,
            alpha=0.9,
            zorder=1
        )

    # Edifícios — destaque
    if len(edificios) > 0:
        edificios.plot(
            ax=ax,
            facecolor="#d0d0d0",
            edgecolor="#404040",
            linewidth=0.8,
            alpha=1.0,
            zorder=2
        )

    # ------------------------------------------------------
    # FINALIZAÇÃO (SEM TÍTULO / SEM NORTE)
    # ------------------------------------------------------
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)

    plt.tight_layout()
    plt.savefig(OUT_PNG, dpi=200, facecolor="white")
    plt.close()

    log("=" * 72)
    log("VALIDAÇÃO CONCLUÍDA — VERSÃO LIMPA")
    log(f"Arquivo gerado: {OUT_PNG}")
    log("=" * 72)

# ----------------------------------------------------------
if __name__ == "__main__":
    main()
