#!/usr/bin/env python3
# ============================================================
# IPT-CitySpace — Mesa Virtual 2D / 2.5D
# Scanner Zig-Zag Canônico
#
# BASE:
#   - DXF IPT já rotacionado e validado (ruas + edifícios)
#   - BMP rotacionado (valores de altura)
#
# OBJETIVO:
#   - Gerar GIF temporal com sensação de subida
#   - Zig-zag coluna a coluna
#   - Célula ativa destacada
#   - DXF branco como base visual
#   - Títulos históricos variando no tempo
#
# ============================================================

print("============================================================")
print("[BOOT] render_mesa_ipt_zigzag_canonico.py carregado")
print("============================================================")

import os
import time
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import imageio.v2 as imageio

# ============================================================
# CONFIGURAÇÕES GERAIS
# ============================================================

BASE_PATH = "/mnt/c/IPT-CitySpace-2018/ipt-cityspace-engine"

DXF_PATH = f"{BASE_PATH}/data/dxf/IPT-2018-DXF.dxf"
BMP_DIR  = f"{BASE_PATH}/outputs/output/bmp"

OUT_DIR  = f"{BASE_PATH}/visualization/gif"
OUT_GIF  = f"{OUT_DIR}/mesa_ipt_zigzag_canonico.gif"

GRID_ROWS = 8
GRID_COLS = 16

ALTURA_MAX_M = 30.0   # altura física máxima (m)

TEMPO_BASE   = 0.05   # tempo mínimo por célula
TEMPO_ESCALA = 0.30   # incremento proporcional à altura

# Fases históricas (indexadas pela célula percorrida)
FASES = [
    (0,  "Fase de implantação na USP (1934–1950)"),
    (32, "Expansão inicial dos laboratórios (1950–1970)"),
    (64, "Consolidação do campus do IPT (1970–1990)"),
    (96, "Modernização e ampliação (1990–2020)")
]

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def log(msg):
    print(f"[INFO] {msg}")

def titulo_fase(idx):
    nome = FASES[0][1]
    for limite, f in FASES:
        if idx >= limite:
            nome = f
    return nome

def localizar_bmp_rotacionado():
    log("Procurando BMP rotacionado em data/output/bmp")

    arquivos = sorted(
        f for f in os.listdir(BMP_DIR)
        if f.startswith("BMP_1cm_rot_") and f.lower().endswith(".bmp")
    )

    if not arquivos:
        raise FileNotFoundError("Nenhum BMP_1cm_rot_*.bmp encontrado")

    bmp_path = os.path.join(BMP_DIR, arquivos[-1])
    log(f"Usando BMP: {bmp_path}")
    return bmp_path

def carregar_alturas():
    bmp_path = localizar_bmp_rotacionado()
    bmp = imageio.imread(bmp_path).astype(float)

    log(f"BMP min={bmp.min()} | max={bmp.max()}")

    alturas = (bmp / 255.0) * ALTURA_MAX_M

    log(f"Altura convertida: {alturas.min():.2f} m → {alturas.max():.2f} m")
    return alturas

def gerar_ordem_zigzag():
    ordem = []
    for c in range(GRID_COLS):
        linhas = range(GRID_ROWS) if c % 2 == 0 else reversed(range(GRID_ROWS))
        for r in linhas:
            ordem.append((r, c))
    return ordem

# ============================================================
# MAIN
# ============================================================

def main():
    print("============================================================")
    print("[MAIN] Iniciando renderização da Mesa Virtual IPT")
    print("============================================================")

    os.makedirs(OUT_DIR, exist_ok=True)

    # --------------------------------------------------------
    # Alturas
    # --------------------------------------------------------
    alturas = carregar_alturas()

    # --------------------------------------------------------
    # DXF
    # --------------------------------------------------------
    log("Carregando DXF do IPT (base visual)")
    gdf = gpd.read_file(DXF_PATH)
    log(f"Entidades DXF: {len(gdf)}")

    # --------------------------------------------------------
    # Scanner Zig-Zag
    # --------------------------------------------------------
    ordem = gerar_ordem_zigzag()
    estado = np.zeros((GRID_ROWS, GRID_COLS))

    frames = []

    for idx, (r, c) in enumerate(ordem):
        altura = alturas[r, c]
        estado[r, c] = altura

        tempo = TEMPO_BASE + (altura / ALTURA_MAX_M) * TEMPO_ESCALA

        log(
            f"Célula {idx+1:03d}/128 | "
            f"(row={r}, col={c}) | "
            f"altura={altura:.2f} m | "
            f"tempo={tempo:.2f}s"
        )

        fig, ax = plt.subplots(figsize=(14, 6))
        ax.set_facecolor("black")

        # Heatmap acumulado
        im = ax.imshow(
            estado,
            cmap="inferno",
            vmin=0,
            vmax=ALTURA_MAX_M,
            origin="upper",
            alpha=0.9
        )

        # DXF como base (branco)
        gdf.plot(
            ax=ax,
            edgecolor="white",
            facecolor="none",
            linewidth=0.8
        )

        # Grid fino
        for x in range(GRID_COLS + 1):
            ax.axvline(x - 0.5, color="white", alpha=0.15, linewidth=0.5)
        for y in range(GRID_ROWS + 1):
            ax.axhline(y - 0.5, color="white", alpha=0.15, linewidth=0.5)

        # Célula ativa
        ax.add_patch(
            Rectangle(
                (c - 0.5, r - 0.5),
                1, 1,
                fill=False,
                edgecolor="white",
                linewidth=2.5
            )
        )

        ax.set_xlim(-0.5, GRID_COLS - 0.5)
        ax.set_ylim(GRID_ROWS - 0.5, -0.5)

        ax.set_xlabel("Ano / Av. Escola Politécnica")
        ax.set_ylabel("USP")

        ax.set_title(
            f"IPT-CitySpace — {titulo_fase(idx)}\n"
            f"Célula {idx+1}/128",
            fontsize=12
        )

        fig.colorbar(im, ax=ax, label="Altura (m)")

        fig.canvas.draw()
        frame = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
        frame = frame.reshape(fig.canvas.get_width_height()[::-1] + (4,))
        frames.append(frame)

        plt.close(fig)
        time.sleep(tempo)

    # --------------------------------------------------------
    # GIF FINAL
    # --------------------------------------------------------
    log("Gerando GIF final")
    imageio.mimsave(OUT_GIF, frames, fps=12)

    print("============================================================")
    print("[OK] GIF GERADO COM SUCESSO")
    print(f"Arquivo: {OUT_GIF}")
    print("============================================================")

# ============================================================
# EXEC
# ============================================================

if __name__ == "__main__":
    print("[BOOT] __main__ detectado — chamando main()")
    main()
