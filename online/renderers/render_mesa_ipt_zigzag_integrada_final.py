#!/usr/bin/env python3
# ============================================================
# IPT-CITYSPACE — MESA VIRTUAL 2D / 2.5D
# Scanner Zig-Zag Integrado FINAL (CANÔNICO)
#
# Autor: Carlos E. H. Simoes
# Consolidação técnica e integração: ChatGPT
#
# Entrada:
#   - CSV 8x16 com alturas físicas (m) já calculadas no offline
#   - DXF do IPT já rotacionado (base visual)
#
# Saída:
#   - GIF final integrado com:
#       * Scanner zig-zag
#       * Tempo proporcional à altura
#       * Destaque da célula ativa
#       * Fases históricas no título
# ============================================================

import os
import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import geopandas as gpd
from matplotlib.patches import Rectangle

# ============================================================
# CONFIGURAÇÕES FIXAS (CANÔNICAS)
# ============================================================

CSV_ALTURAS = "/mnt/c/IPT-CitySpace-2018/data/output/BMP_1cm_rot.csv"

DXF_IPT = "/mnt/c/IPT-CitySpace-2018/data/dxf/IPT-2018-DXF.dxf"

OUT_DIR = "/mnt/c/IPT-CitySpace-2018/ipt-cityspace-engine/visualization/gif"
OUT_GIF = os.path.join(OUT_DIR, "mesa_ipt_zigzag_integrada_final.gif")

GRID_Y, GRID_X = 8, 16   # mesa 8x16
FPS_BASE = 6             # base de frames
FPS_GAIN = 12            # ganho proporcional à altura

# Fases históricas (a partir de 1940)
FASES = [
    (1940, 1950, "Fase de implantação na USP (1934–1950)"),
    (1951, 1970, "Fase de consolidação e expansão (1951–1970)"),
    (1971, 1990, "Fase de modernização científica (1971–1990)"),
    (1991, 2010, "Fase de integração tecnológica (1991–2010)"),
    (2011, 2030, "Fase contemporânea e inovação aberta (2011– )"),
]

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def log(msg):
    print(msg)

def carregar_alturas():
    log("[INFO] Carregando CSV de alturas reais (m)")
    z = np.loadtxt(CSV_ALTURAS, delimiter=",")
    log(f"[INFO] Shape: {z.shape} | Min: {z.min():.2f} m | Max: {z.max():.2f} m")
    return z

def carregar_dxf():
    log("[INFO] Carregando DXF do IPT (base branca)")
    gdf = gpd.read_file(DXF_IPT)
    return gdf

def fase_por_indice(idx):
    ano = 1940 + idx  # aproximação temporal simbólica
    for a0, a1, nome in FASES:
        if a0 <= ano <= a1:
            return nome
    return FASES[-1][2]

def ordem_zigzag(nx, ny):
    ordem = []
    for x in range(nx):
        ys = range(ny) if x % 2 == 0 else range(ny - 1, -1, -1)
        for y in ys:
            ordem.append((x, y))
    return ordem

# ============================================================
# MAIN
# ============================================================

def main():
    log("=" * 64)
    log("IPT-CITYSPACE — MESA VIRTUAL 2D / 2.5D")
    log("Scanner Zig-Zag Integrado (FINAL)")
    log("=" * 64)

    os.makedirs(OUT_DIR, exist_ok=True)

    alturas = carregar_alturas()
    gdf = carregar_dxf()

    ordem = ordem_zigzag(GRID_X, GRID_Y)

    frames = []
    estado = np.zeros_like(alturas)

    idx_global = 0

    for i, (x, y) in enumerate(ordem):
        h = alturas[y, x]
        estado[y, x] = h

        fase = fase_por_indice(i)

        n_frames = int(FPS_BASE + FPS_GAIN * (h / alturas.max()))

        log(f"[SCAN] Célula {i+1:03d}/128 | (x={x}, y={y}) | h={h:.2f} m | frames={n_frames}")

        for f in range(n_frames):
            fig, ax = plt.subplots(figsize=(12, 6))
            fig.patch.set_facecolor("black")

            im = ax.imshow(
                estado,
                cmap="viridis",
                vmin=0,
                vmax=alturas.max(),
                origin="upper",
                extent=[0, GRID_X, GRID_Y, 0],
                alpha=0.95,
            )

            # DXF base (branco)
            gdf.plot(ax=ax, facecolor="none", edgecolor="white", linewidth=0.8)

            # Destaque da célula ativa
            ax.add_patch(
                Rectangle((x, y), 1, 1, fill=False, edgecolor="white", linewidth=2)
            )

            ax.set_title(
                f"Mesa Virtual IPT — Evolução Temporal\n"
                f"{fase}\n"
                f"Célula {i+1}/128 | (x={x}, y={y}) | Altura = {h:.2f} m",
                color="white",
                fontsize=12,
            )

            ax.set_xlabel("Ano / Av. Politécnica", color="white")
            ax.set_ylabel("USP", color="white")

            ax.tick_params(colors="white")
            for spine in ax.spines.values():
                spine.set_edgecolor("white")

            cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
            cbar.set_label("Altura (m)", color="white")
            cbar.ax.yaxis.set_tick_params(color="white")
            plt.setp(cbar.ax.get_yticklabels(), color="white")

            fig.canvas.draw()
            frame = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
            frame = frame.reshape(fig.canvas.get_width_height()[::-1] + (4,))
            frames.append(frame)

            plt.close(fig)

        idx_global += 1

    log("[INFO] Gravando GIF final")
    imageio.mimsave(OUT_GIF, frames, fps=12)
    log(f"[OK] GIF gerado com sucesso em:\n{OUT_GIF}")

# ============================================================

if __name__ == "__main__":
    main()
