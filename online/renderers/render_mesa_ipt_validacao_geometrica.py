#!/usr/bin/env python3
# ======================================================
# MESA VIRTUAL IPT — VALIDAÇÃO GEOMÉTRICA E NARRATIVA
#
# Objetivo:
#   - Validar visualmente o encaixe do IPT no grid 8x16
#   - Usar DXF completo (ruas + quadras + eixos)
#   - Aplicar rotação consolidada (154.63°)
#   - Executar scanner zig-zag (como GIF legado)
#   - Mostrar célula ativa (borda branca)
#   - Narrar fases temporais (anos no título)
#
# NÃO usa:
#   - DSM / DTM
#   - Alturas reais
#   - BMP / GeoTIFF
#
# Ambiente:
#   geo_env_2018 (WSL / Ubuntu)
#
# Autor: Carlos E. H. Simoes
# ======================================================

import os
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import imageio.v2 as imageio
from shapely.affinity import rotate
from matplotlib.patches import Rectangle
from datetime import datetime

# ------------------------------------------------------
# CONFIGURAÇÃO DA MESA
# ------------------------------------------------------
ROWS = 8
COLS = 16
N_CELLS = ROWS * COLS

EXTENT = [0, COLS, ROWS, 0]  # grid físico

# ------------------------------------------------------
# ARQUIVOS
# ------------------------------------------------------
DXF_PATH = "/mnt/c/IPT-CitySpace-2018/data/vetor/dxf_corrigido.dxf"

OUT_BASE = "visualization/gif"
FRAMES_DIR = os.path.join(OUT_BASE, "frames_validacao_geometrica")
GIF_PATH = os.path.join(OUT_BASE, "mesa_ipt_validacao_geometrica.gif")

os.makedirs(FRAMES_DIR, exist_ok=True)

# ------------------------------------------------------
# ROTAÇÃO CONSOLIDADA (OFFLINE VALIDADA)
# ------------------------------------------------------
ANGLE_DEG = 154.63  # alinhamento IPT ↔ eixo físico da mesa

# ------------------------------------------------------
# VISUAL
# ------------------------------------------------------
DXF_COLOR = "white"
DXF_ALPHA = 0.9
DXF_LINEWIDTH = 0.9

VISITED_COLOR = 0.6  # cinza claro para células já varridas

GIF_FPS = 5

# ------------------------------------------------------
# FASES TEMPORAIS (NARRATIVA)
# ------------------------------------------------------
TEMPORAL_PHASES = [
    (0, 20, "Fase de implantação na USP (1934–1950)"),
    (21, 50, "Fase de expansão do campus (1950–1980)"),
    (51, 90, "Fase de consolidação institucional (1980–2000)"),
    (91, 999, "IPT contemporâneo (2000–hoje)")
]

# ------------------------------------------------------
# LOG
# ------------------------------------------------------
def log(msg):
    print(msg)

# ------------------------------------------------------
# SCANNER ZIG-ZAG (IGUAL AO GIF LEGADO)
# ------------------------------------------------------
def zigzag_path(rows, cols):
    """
    Varredura por COLUNA:
    - coluna par: Norte → Sul
    - coluna ímpar: Sul → Norte
    """
    path = []
    for c in range(cols):
        if c % 2 == 0:
            for r in range(rows):
                path.append((r, c))
        else:
            for r in reversed(range(rows)):
                path.append((r, c))
    return path

# ------------------------------------------------------
# PREPARAÇÃO DO DXF
# ------------------------------------------------------
def prepare_dxf(dxf_path):
    log(f"[DXF] Carregando arquivo: {dxf_path}")
    gdf = gpd.read_file(dxf_path, layer="entities")

    log("[DXF] Mantendo ruas, eixos e quadras (LineString + MultiLineString)")
    gdf = gdf[gdf.geom_type.isin(["LineString", "MultiLineString"])].copy()

    log(f"[DXF] Aplicando rotação trigonométrica: {ANGLE_DEG:.2f}°")
    gdf["geometry"] = gdf["geometry"].apply(
        lambda g: rotate(g, ANGLE_DEG, origin="center", use_radians=False)
    )

    minx, miny, maxx, maxy = gdf.total_bounds
    log("[DXF] Normalizando geometria para grid físico 8x16")

    def normalize(geom):
        x, y = geom.xy
        x = (np.array(x) - minx) / (maxx - minx) * COLS
        y = (np.array(y) - miny) / (maxy - miny) * ROWS
        return type(geom)(zip(x, y))

    gdf["geometry"] = gdf["geometry"].apply(normalize)

    return gdf

# ------------------------------------------------------
# FASE TEMPORAL ATUAL
# ------------------------------------------------------
def get_temporal_phase(idx):
    for start, end, label in TEMPORAL_PHASES:
        if start <= idx <= end:
            return label
    return ""

# ------------------------------------------------------
# RENDER FRAME
# ------------------------------------------------------
def render_frame(visited, gdf, active_cell, idx, frame_path):
    fig, ax = plt.subplots(figsize=(10, 5))

    # ------------------------------
    # ESTADO ACUMULADO (scanner)
    # ------------------------------
    ax.imshow(
        visited,
        cmap="gray",
        extent=EXTENT,
        origin="upper",
        vmin=0,
        vmax=1,
        interpolation="nearest",
        zorder=3
    )

    # ------------------------------
    # PLANTA IPT (SEMPRE VISÍVEL)
    # ------------------------------
    gdf.plot(
        ax=ax,
        color=DXF_COLOR,
        linewidth=DXF_LINEWIDTH,
        alpha=DXF_ALPHA,
        zorder=6
    )

    # ------------------------------
    # CÉLULA ATIVA
    # ------------------------------
    r, c = active_cell
    ax.add_patch(
        Rectangle(
            (c, r), 1, 1,
            fill=False,
            edgecolor="white",
            linewidth=3,
            zorder=10
        )
    )

    # ------------------------------
    # TÍTULOS E EIXOS
    # ------------------------------
    phase_label = get_temporal_phase(idx)

    ax.set_title(
        f"Mesa Virtual IPT — Validação Geométrica\n"
        f"{phase_label}\n"
        f"Célula {idx+1}/{N_CELLS}  |  (x={c}, y={r})"
    )

    ax.set_xlabel("Eixo X — Sentido Bairro (Av. Escola Politécnica)")
    ax.set_ylabel("Eixo Y — Sentido Campus (USP)")

    ax.set_xticks(np.arange(0, COLS + 1))
    ax.set_yticks(np.arange(0, ROWS + 1))
    ax.grid(alpha=0.2)

    ax.set_xlim(0, COLS)
    ax.set_ylim(ROWS, 0)

    plt.tight_layout()
    plt.savefig(frame_path, dpi=150)
    plt.close()

# ------------------------------------------------------
# MAIN
# ------------------------------------------------------
def main():

    log("=" * 70)
    log("MESA IPT — VALIDAÇÃO GEOMÉTRICA E TEMPORAL")
    log(f"Início: {datetime.now()}")
    log("=" * 70)

    gdf = prepare_dxf(DXF_PATH)

    path = zigzag_path(ROWS, COLS)
    visited = np.zeros((ROWS, COLS), dtype=float)

    frames = []

    log("[SCAN] Iniciando scanner zig-zag por coluna")

    for idx, (r, c) in enumerate(path):
        log(f"[SCAN] Célula {idx+1}/{N_CELLS} — (x={c}, y={r})")

        visited[r, c] = VISITED_COLOR

        frame_path = os.path.join(FRAMES_DIR, f"frame_{idx:03d}.png")

        render_frame(
            visited=visited,
            gdf=gdf,
            active_cell=(r, c),
            idx=idx,
            frame_path=frame_path
        )

        frames.append(frame_path)

    log("[GIF] Gerando GIF final")

    images = [imageio.imread(f) for f in frames]
    imageio.mimsave(GIF_PATH, images, fps=GIF_FPS)

    log("=" * 70)
    log("GIF GERADO COM SUCESSO")
    log(f"Arquivo: {GIF_PATH}")
    log("=" * 70)

# ------------------------------------------------------
if __name__ == "__main__":
    main()
