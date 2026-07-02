#!/usr/bin/env python3
# ==========================================================
# IPT-CitySpace — MESA VIRTUAL 2D / 2.5D (VERBOSA)
# Zig-zag temporal com DXF do IPT como base
# ==========================================================

import os
import glob
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib import patches
from PIL import Image
import imageio.v2 as imageio

# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

DXF_PATH = "/mnt/c/IPT-CitySpace-2018/data/dxf/IPT-2018-DXF.dxf"
BMP_DIR  = "/mnt/c/IPT-CitySpace-2018/data/output/bmp"

OUT_DIR  = "visualization/gif"
GIF_PATH = f"{OUT_DIR}/mesa_ipt_zigzag_temporal_verbose.gif"

ROWS, COLS = 8, 16
ALTURA_MAX_METROS = 30.0

FRAMES_MIN = 2
FRAMES_MAX = 12

FASES = [
    (1940, "Fase de Implantação na USP (1934–1950)"),
    (1950, "Expansão dos Laboratórios (1950–1970)"),
    (1970, "Consolidação Tecnológica (1970–1990)"),
    (1990, "Modernização e Integração (1990–2010)"),
    (2010, "IPT Contemporâneo"),
]

# ==========================================================
# FUNÇÕES
# ==========================================================

def log(msg):
    print(msg)

def localizar_bmp():
    arquivos = sorted(glob.glob(os.path.join(BMP_DIR, "BMP_1cm_rot_*.bmp")))
    if not arquivos:
        raise FileNotFoundError("Nenhum BMP_1cm_rot encontrado.")
    return arquivos[-1]

def bmp_para_alturas(bmp):
    img = Image.open(bmp).convert("L")
    gray = np.array(img, dtype=float)
    alturas = (gray / 255.0) * ALTURA_MAX_METROS
    return alturas

def frames_por_altura(h):
    f = FRAMES_MIN + (h / ALTURA_MAX_METROS) * (FRAMES_MAX - FRAMES_MIN)
    return int(round(f))

def fase_por_ano(ano):
    nome = FASES[0][1]
    for a, f in FASES:
        if ano >= a:
            nome = f
    return nome

def canvas_to_rgb(fig):
    canvas = fig.canvas
    canvas.draw()
    w, h = canvas.get_width_height()
    buf = np.frombuffer(canvas.tostring_argb(), dtype=np.uint8)
    buf = buf.reshape((h, w, 4))
    return buf[:, :, 1:4]

# ==========================================================
# MAIN
# ==========================================================

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    log("====================================================")
    log("IPT-CitySpace — MESA VIRTUAL 2D/2.5D (VERBOSA)")
    log("====================================================")

    # --------------------------------------------------
    # BMP → ALTURAS
    # --------------------------------------------------
    bmp = localizar_bmp()
    log(f"[INFO] BMP rotacionado usado: {bmp}")

    alturas = bmp_para_alturas(bmp)
    log(f"[INFO] Altura mínima: {alturas.min():.2f} m")
    log(f"[INFO] Altura máxima: {alturas.max():.2f} m")

    # --------------------------------------------------
    # DXF
    # --------------------------------------------------
    log("[INFO] Carregando DXF do IPT (base visual)")
    gdf = gpd.read_file(DXF_PATH, layer="entities")
    log(f"[INFO] Entidades no DXF: {len(gdf)}")

    frames = []
    ano_base = 1940
    idx_global = 0

    # --------------------------------------------------
    # ZIG-ZAG
    # --------------------------------------------------
    for col in range(COLS):
        sentido = "↓" if col % 2 == 0 else "↑"
        log(f"[SCAN] Coluna {col} | Sentido {sentido}")

        linhas = range(ROWS) if col % 2 == 0 else reversed(range(ROWS))

        for row in linhas:
            idx_global += 1
            ano = ano_base + idx_global
            fase = fase_por_ano(ano)

            h = alturas[row, col]
            n_frames = frames_por_altura(h)

            log(
                f"[CELL] row={row}, col={col} | "
                f"altura={h:.2f} m | "
                f"frames={n_frames} | "
                f"ano={ano}"
            )

            for f in range(n_frames):
                fig, ax = plt.subplots(figsize=(14, 6))

                # DXF base
                gdf.plot(
                    ax=ax,
                    color="none",
                    edgecolor="white",
                    linewidth=1,
                    zorder=1
                )

                # Alturas
                ax.imshow(
                    alturas,
                    cmap="inferno",
                    vmin=0,
                    vmax=ALTURA_MAX_METROS,
                    alpha=0.85,
                    zorder=2
                )

                # Célula ativa
                rect = patches.Rectangle(
                    (col, row), 1, 1,
                    edgecolor="white",
                    linewidth=2,
                    facecolor="none",
                    zorder=3
                )
                ax.add_patch(rect)

                ax.set_xlim(0, COLS)
                ax.set_ylim(ROWS, 0)
                ax.set_facecolor("black")

                ax.set_xlabel("Ano / Av. Politécnica", color="white")
                ax.set_ylabel("USP", color="white")

                ax.set_title(
                    f"IPT-CitySpace — {fase} — {ano}",
                    color="white"
                )

                ax.tick_params(colors="white")
                ax.grid(color="gray", linestyle=":", linewidth=0.5)

                frame = canvas_to_rgb(fig)
                frames.append(frame)
                plt.close(fig)

    # --------------------------------------------------
    # GIF
    # --------------------------------------------------
    imageio.mimsave(GIF_PATH, frames, fps=10)
    log("====================================================")
    log(f"[OK] GIF GERADO: {GIF_PATH}")
    log("====================================================")

if __name__ == "__main__":
    main()
