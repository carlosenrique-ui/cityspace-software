#!/usr/bin/env python3
# ==========================================================
# IPT — FUNDO CANÔNICO DA MESA (16 x 8)
#
# Objetivo:
# - Ler o DXF ORIGINAL do IPT
# - Aplicar APENAS a rotação trigonométrica validada (154.63°)
# - Preservar ruas e edifícios
# - Gerar PNG limpo para fundo da mesa virtual e real
#
# Autor: Carlos E. H. Simoes
# ==========================================================

import os
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.affinity import rotate

# ----------------------------------------------------------
# CONFIGURAÇÕES
# ----------------------------------------------------------
DXF_PATH = "/mnt/c/IPT-CitySpace-2018/data/dxf/IPT-2018-DXF.dxf"
OUT_PNG = "visualization/debug/ipt_dxf_mesa_16x8.png"

ANGLE_DEG = 154.63  # rotação trigonométrica validada

# ----------------------------------------------------------
def main():
    print("=" * 70)
    print("IPT | FUNDO CANÔNICO DA MESA 16x8")
    print(f"DXF: {DXF_PATH}")
    print(f"Rotação: {ANGLE_DEG}°")

    os.makedirs("visualization/debug", exist_ok=True)

    # ------------------------------------------------------
    # LEITURA DO DXF
    # ------------------------------------------------------
    gdf = gpd.read_file(DXF_PATH, layer="entities")
    print(f"Geometrias carregadas: {len(gdf)}")

    # ------------------------------------------------------
    # ROTAÇÃO RÍGIDA (CORPO ÚNICO)
    # ------------------------------------------------------
    minx, miny, maxx, maxy = gdf.total_bounds
    cx = (minx + maxx) / 2
    cy = (miny + maxy) / 2

    gdf["geometry"] = gdf["geometry"].apply(
        lambda geom: rotate(
            geom,
            ANGLE_DEG,
            origin=(cx, cy),
            use_radians=False
        )
    )

    # ------------------------------------------------------
    # RENDER LIMPO
    # ------------------------------------------------------
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.set_aspect("equal")
    ax.axis("off")

    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")

    # IPT em branco (ruas + edifícios)
    gdf.plot(
        ax=ax,
        color="white",
        linewidth=0.6,
        alpha=1.0
    )

    plt.savefig(
        OUT_PNG,
        dpi=200,
        bbox_inches="tight",
        pad_inches=0,
        facecolor="black"
    )
    plt.close()

    print("PNG GERADO COM SUCESSO")
    print(f"→ {OUT_PNG}")
    print("=" * 70)


if __name__ == "__main__":
    main()
