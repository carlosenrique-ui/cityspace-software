#!/usr/bin/env python3
# ==========================================================
# MESA VIRTUAL IPT — ANIMAÇÃO 2D / 2.5D (ZIG-ZAG CANÔNICO)
#
# OBJETIVO
# ----------------------------------------------------------
# Visualizar a evolução temporal da mesa virtual (8x16),
# usando:
#   - DXF do IPT como base fixa (ruas + edifícios)
#   - Varredura em zig-zag (coluna a coluna)
#   - Célula ativa destacada com borda branca
#   - Altura controla cor e tempo de permanência
#
# IMPORTANTE
# ----------------------------------------------------------
# - O DXF NÃO é modificado visualmente (apenas rotacionado)
# - A animação NÃO cobre o IPT (fica sempre por cima)
# - Pensado para equivalência futura com mesa física
#
# Autor: Carlos E. H. Simoes
# ==========================================================

import os
import time
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.affinity import rotate
from matplotlib.patches import Rectangle
from matplotlib import cm
import imageio


# ==========================================================
# CONFIGURAÇÕES GERAIS
# ==========================================================

DXF_PATH = "/mnt/c/IPT-CitySpace-2018/data/dxf/IPT-2018-DXF.dxf"

# CSV já ROTACIONADO no offline (8x16)
CSV_ALTURAS = "/mnt/c/IPT-CitySpace-2018/data/output/csv/BMP_1cm_rot_base.csv"

OUT_GIF = "visualization/gif/mesa_ipt_zigzag_temporal.gif"

# Ângulo trigonométrico validado anteriormente
ANGLE_DEG = 154.63

ROWS, COLS = 8, 16

# Controle temporal (segundos)
T_MIN = 0.05   # células baixas
T_MAX = 0.40   # células altas

COLORMAP = cm.inferno


# ==========================================================
# FUNÇÕES AUXILIARES
# ==========================================================

def log(msg):
    """Log padronizado no terminal"""
    print(f"[INFO] {msg}")


def carregar_dxf_rotacionado():
    """
    Carrega o DXF original do IPT e aplica SOMENTE
    a rotação trigonométrica já validada.
    """
    log("Carregando DXF do IPT")
    gdf = gpd.read_file(DXF_PATH, layer="entities")

    log("Calculando centro geométrico do DXF")
    minx, miny, maxx, maxy = gdf.total_bounds
    cx = (minx + maxx) / 2
    cy = (miny + maxy) / 2

    log(f"Aplicando rotação trigonométrica: {ANGLE_DEG:.2f}°")
    gdf["geometry"] = gdf["geometry"].apply(
        lambda g: rotate(g, ANGLE_DEG, origin=(cx, cy), use_radians=False)
    )

    log("DXF rotacionado com sucesso")
    return gdf


def carregar_alturas():
    """
    Carrega a matriz 8x16 de alturas (já rotacionada no offline)
    e normaliza para [0,1].
    """
    log("Carregando CSV de alturas (offline)")
    z = np.loadtxt(CSV_ALTURAS, delimiter=";")

    z = z[:ROWS, :COLS]
    zmin, zmax = z.min(), z.max()

    log(f"Alturas — mínimo: {zmin:.3f} | máximo: {zmax:.3f}")

    z_norm = (z - zmin) / (zmax - zmin + 1e-9)
    return z_norm


def gerar_ordem_zigzag(rows, cols):
    """
    Gera a sequência de varredura:
    - Coluna a coluna
    - Zig-zag vertical
    - Início no canto superior esquerdo
    """
    log("Gerando ordem de varredura zig-zag")
    ordem = []

    for c in range(cols):
        if c % 2 == 0:
            for r in range(rows):
                ordem.append((r, c))
        else:
            for r in reversed(range(rows)):
                ordem.append((r, c))

    log(f"Total de células na varredura: {len(ordem)}")
    return ordem


# ==========================================================
# MAIN
# ==========================================================

def main():
    print("=" * 72)
    print("MESA VIRTUAL IPT — ANIMAÇÃO ZIG-ZAG (VALIDAÇÃO VISUAL)")
    print("=" * 72)

    os.makedirs("visualization/gif", exist_ok=True)

    # ------------------------------------------------------
    # 1. Dados base
    # ------------------------------------------------------
    gdf = carregar_dxf_rotacionado()
    alturas = carregar_alturas()
    ordem = gerar_ordem_zigzag(ROWS, COLS)

    # ------------------------------------------------------
    # 2. Preparação da figura
    # ------------------------------------------------------
    log("Inicializando figura matplotlib")

    fig, ax = plt.subplots(figsize=(16, 8))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.axis("off")

    # Limites da mesa virtual
    ax.set_xlim(0, COLS)
    ax.set_ylim(ROWS, 0)

    # ------------------------------------------------------
    # 3. DXF de fundo (sempre visível)
    # ------------------------------------------------------
    log("Desenhando DXF do IPT como base fixa")
    gdf.plot(ax=ax, color="white", linewidth=0.6, zorder=1)

    # Grid fino da mesa
    for x in range(COLS + 1):
        ax.axvline(x, color="lightgray", linewidth=0.3, zorder=0)
    for y in range(ROWS + 1):
        ax.axhline(y, color="lightgray", linewidth=0.3, zorder=0)

    # ------------------------------------------------------
    # 4. Loop de animação
    # ------------------------------------------------------
    frames = []

    log("Iniciando animação temporal")

    for idx, (r, c) in enumerate(ordem):
        altura = alturas[r, c]
        tempo = T_MIN + altura * (T_MAX - T_MIN)

        log(
            f"Célula {idx+1:03d}/128 | "
            f"(linha={r}, coluna={c}) | "
            f"altura_norm={altura:.2f} | "
            f"tempo={tempo:.2f}s"
        )

        # Célula colorida
        ax.add_patch(
            Rectangle((c, r), 1, 1,
                      facecolor=COLORMAP(altura),
                      alpha=0.85,
                      zorder=2)
        )

        # Destaque branco da célula ativa
        ax.add_patch(
            Rectangle((c, r), 1, 1,
                      fill=False,
                      edgecolor="white",
                      linewidth=2.0,
                      zorder=3)
        )

        ax.set_title(
            "Planta Baixa do IPT — Varredura Temporal\n"
            f"Célula {idx+1}/128 | Altura normalizada = {altura:.2f}",
            fontsize=12
        )

        fig.canvas.draw()

        image = np.frombuffer(
            fig.canvas.tostring_rgb(), dtype=np.uint8
        ).reshape(fig.canvas.get_width_height()[::-1] + (3,))

        frames.append(image)

        ax.patches.clear()
        time.sleep(tempo)

    plt.close(fig)

    # ------------------------------------------------------
    # 5. GIF final
    # ------------------------------------------------------
    log("Gerando GIF final")
    imageio.mimsave(OUT_GIF, frames, fps=10)

    print("=" * 72)
    print("PROCESSO FINALIZADO COM SUCESSO")
    print(f"Arquivo gerado: {OUT_GIF}")
    print("=" * 72)


if __name__ == "__main__":
    main()
