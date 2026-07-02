#!/usr/bin/env python3
# ==========================================================
# ONLINE — VALIDAÇÃO VISUAL DA MESA IPT (SEM ROTAÇÃO)
#
# - DXF já rotacionado e corrigido
# - BMP 1cm já rotacionado (8x16)
# - Conversão gray → altura física (m)
#
# OBJETIVO:
# Validar APENAS as alturas físicas
#
# Autor: Carlos E. H. Simoes
# ==========================================================

import os
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib import cm

# ==========================================================
# CONFIGURAÇÕES (FIXAS)
# ==========================================================

BMP_PATH = "/mnt/c/IPT-CitySpace-2018/data/output/bmp/BMP_1cm_rot.bmp"

# DXF JÁ CORRIGIDO / ROTACIONADO (NÃO MEXER)
DXF_PATH = "/mnt/c/IPT-CitySpace-2018/data/vetor/dxf_corrigido.dxf"

OUT_PNG = "visualization/debug/mesa_ipt_validacao_alturas_sem_rotacao.png"

ROWS, COLS = 8, 16

# ALTURA MÁXIMA FÍSICA (MESMO VALOR DO OFFLINE)
ALTURA_MAX_METROS = 30.0

COLORMAP = cm.inferno

# ==========================================================
# FUNÇÕES
# ==========================================================

def log(msg):
    print(f"[INFO] {msg}")

def carregar_bmp():
    log("Carregando BMP (gray, já rotacionado)")
    bmp = plt.imread(BMP_PATH)

    if bmp.ndim == 3:
        bmp = bmp[:, :, 0]

    bmp = bmp.astype(np.float32)

    log(f"Gray min={bmp.min():.1f} | max={bmp.max():.1f}")

    return bmp[:ROWS, :COLS]

def converter_para_altura(bmp):
    log("Convertendo gray → altura física (m)")
    altura_m = (bmp / 255.0) * ALTURA_MAX_METROS

    log(
        f"Altura física → "
        f"min={altura_m.min():.2f} m | "
        f"max={altura_m.max():.2f} m"
    )
    return altura_m

def carregar_dxf():
    log("Carregando DXF corrigido (sem rotação)")
    gdf = gpd.read_file(DXF_PATH, layer="entities")
    log(f"Geometrias DXF: {len(gdf)}")
    return gdf

# ==========================================================
# MAIN
# ==========================================================

def main():
    print("=" * 72)
    print("ONLINE — VALIDAÇÃO DE ALTURAS (DXF JÁ ROTACIONADO)")
    print("=" * 72)

    os.makedirs("visualization/debug", exist_ok=True)

    bmp = carregar_bmp()
    altura_m = converter_para_altura(bmp)
    gdf = carregar_dxf()

    fig, ax = plt.subplots(figsize=(16, 8))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.axis("off")

    # -------------------------------
    # ALTURAS (BASE COLORIDA)
    # -------------------------------
    im = ax.imshow(
        altura_m,
        cmap=COLORMAP,
        origin="upper",
        alpha=0.95
    )

    plt.colorbar(im, ax=ax, fraction=0.025, label="Altura (m)")

    # -------------------------------
    # GRID DA MESA (8x16)
    # -------------------------------
    for x in range(COLS + 1):
        ax.axvline(x - 0.5, color="lightgray", linewidth=0.4)
    for y in range(ROWS + 1):
        ax.axhline(y - 0.5, color="lightgray", linewidth=0.4)

    # -------------------------------
    # DXF IPT (FUNDO FIXO)
    # -------------------------------
    log("Desenhando DXF do IPT como base fixa")
    gdf.plot(
        ax=ax,
        color="white",
        linewidth=0.7,
        zorder=10
    )

    ax.set_xlim(-0.5, COLS - 0.5)
    ax.set_ylim(ROWS - 0.5, -0.5)

    ax.set_title(
        "IPT — Validação das Alturas Físicas\n"
        "BMP rotacionado → metros | DXF corrigido",
        fontsize=14
    )

    plt.savefig(OUT_PNG, dpi=200, bbox_inches="tight")
    plt.close()

    print("=" * 72)
    print("IMAGEM GERADA COM SUCESSO")
    print(f"Arquivo: {OUT_PNG}")
    print("=" * 72)


if __name__ == "__main__":
    main()
