#!/usr/bin/env python3
# ==========================================================
# IPT-CitySpace — MESA VIRTUAL 2D / 2.5D
# Geração de GIF com varredura zig-zag
# ==========================================================

import os
import glob
import time
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib import patches
from PIL import Image
import imageio.v2 as imageio

# ================= CONFIG ================================

DXF_PATH = "/mnt/c/IPT-CitySpace-2018/data/dxf/IPT-2018-DXF.dxf"
BMP_DIR  = "/mnt/c/IPT-CitySpace-2018/data/output/bmp"

OUT_DIR  = "visualization/gif"
GIF_PATH = f"{OUT_DIR}/mesa_ipt_zigzag_temporal.gif"

ROWS, COLS = 8, 16
ALTURA_MAX_METROS = 30.0

TEMPO_MIN = 0.05
TEMPO_MAX = 0.30

FASES = [
    (0,  "Fase de Implantação na USP (1934–1950)"),
    (12, "Expansão dos Laboratórios (1950–1970)"),
    (32, "Consolidação Tecnológica (1970–1990)"),
    (64, "Modernização e Integração (1990–2010)"),
    (96, "IPT Contemporâneo"),
]

# ================= FUNÇÕES ===============================

def localizar_bmp():
    arquivos = sorted(glob.glob(os.path.join(BMP_DIR, "BMP_1cm_rot_*.bmp")))
    if not arquivos:
        raise FileNotFoundError("Nenhum BMP_1cm_rot encontrado.")
    return arquivos[-1]

def bmp_para_alturas(bmp):
    img = Image.open(bmp).convert("L")
    gray = np.array(img, dtype=float)
    return (gray / 255.0) * ALTURA_MAX_METROS

def tempo_por_altura(h):
    return TEMPO_MIN + (h / ALTURA_MAX_METROS) * (TEMPO_MAX - TEMPO_MIN)

def fase_por_idx(idx):
    nome = FASES[0][1]
    for limite, f in FASES:
        if idx >= limite:
            nome = f
    return nome

def canvas_to_rgb(fig):
    canvas = fig.canvas
    canvas.draw()
    w, h = canvas.get_width_height()
    buf = np.frombuffer(canvas.tostring_argb(), dtype=np.uint8)
    buf = buf.reshape((h, w, 4))
    # ARGB → RGB
    return buf[:, :, 1:4]

# ================= MAIN ==================================

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    bmp = localizar_bmp()
    alturas = bmp_para_alturas(bmp)

    gdf = gpd.read_file(DXF_PATH, layer="entities")

    frames = []
    idx = 0

    for col in range(COLS):
        rows = range(ROWS) if col % 2 == 0 else reversed(range(ROWS))

        for row in rows:
            idx += 1

            fig, ax = plt.subplots(figsize=(14, 6))

            # Fundo DXF
            gdf.plot(ax=ax, color="none", edgecolor="white", linewidth=1)

            ax.imshow(
                alturas,
                cmap="inferno",
                vmin=0,
                vmax=ALTURA_MAX_METROS,
                alpha=0.85
            )

            rect = patches.Rectangle(
                (col, row), 1, 1,
                edgecolor="white",
                linewidth=2,
                facecolor="none"
            )
            ax.add_patch(rect)

            ax.set_xlim(0, COLS)
            ax.set_ylim(ROWS, 0)
            ax.set_facecolor("black")

            ax.set_xlabel("Ano / Av. Politécnica", color="white")
            ax.set_ylabel("USP", color="white")

            ax.set_title(
                f"IPT-CitySpace — {fase_por_idx(idx)}",
                color="white"
            )

            ax.tick_params(colors="white")
            ax.grid(color="gray", linestyle=":", linewidth=0.5)

            frame = canvas_to_rgb(fig)
            frames.append(frame)

            plt.close(fig)

            time.sleep(tempo_por_altura(alturas[row, col]))

    imageio.mimsave(GIF_PATH, frames, fps=10)
    print(f"\nGIF GERADO COM SUCESSO:\n{GIF_PATH}\n")

if __name__ == "__main__":
    main()
