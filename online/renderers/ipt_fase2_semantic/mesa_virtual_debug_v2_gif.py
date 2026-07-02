#!/usr/bin/env python3
# ==========================================================
# MESA VIRTUAL — DEBUG V2 (GIF DINÂMICO)
# IPT CitySpace
# ==========================================================

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import imageio.v2 as imageio

# ----------------------------------------------------------
# PATHS
# ----------------------------------------------------------

ENGINE_ROOT = Path(__file__).resolve().parents[3]

GRID_PATH = (
    ENGINE_ROOT
    / "offline"
    / "products"
    / "snapshots"
    / "ipt_fase2_semantic"
    / "grid_z_total_m.csv"
)

DXF_PATH = (
    ENGINE_ROOT
    / "offline"
    / "products"
    / "fase2"
    / "dxf"
    / "IPT-2018-DXF-Rotacionado.dxf"
)

OUT_DIR = ENGINE_ROOT / "online" / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

GIF_PATH = OUT_DIR / "mesa_virtual_debug_v2.gif"

# ----------------------------------------------------------
# CONFIGURAÇÃO DA MESA
# ----------------------------------------------------------

ROWS = 8
COLS = 16
FPS = 6

# ----------------------------------------------------------
# FASES HISTÓRICAS IPT
# ----------------------------------------------------------

FASES = [
    "1940–1959 · Formação inicial",
    "1960–1979 · Consolidação tecnológica",
    "1980–1999 · Expansão institucional",
    "2000–2015 · Modernização",
    "2016–2025 · Inovação & sustentabilidade",
]

def fase_por_frame(i, total):
    bloco = total // len(FASES)
    return FASES[min(i // bloco, len(FASES) - 1)]

# ----------------------------------------------------------
# LOAD GRID (Z TOTAL REAL)
# ----------------------------------------------------------

print("[LOAD] Grid Z_total_real")
grid = np.loadtxt(GRID_PATH, delimiter=";")
assert grid.shape == (ROWS, COLS)

Z_MIN = np.nanmin(grid)
Z_MAX = np.nanmax(grid)

# ----------------------------------------------------------
# LOAD DXF (FLIP EM Y CORRETO)
# ----------------------------------------------------------

print("[LOAD] DXF IPT")
gdf = gpd.read_file(DXF_PATH)

minx, miny, maxx, maxy = gdf.total_bounds

def norm_x(x):
    return (x - minx) / (maxx - minx) * COLS

def norm_y(y):
    return (maxy - y) / (maxy - miny) * ROWS

# ----------------------------------------------------------
# TRAJETÓRIA ZIG-ZAG (ESQUERDA → DIREITA)
# ----------------------------------------------------------

trajetoria = []
for c in range(COLS):
    if c % 2 == 0:
        for r in range(ROWS):
            trajetoria.append((r, c))
    else:
        for r in range(ROWS - 1, -1, -1):
            trajetoria.append((r, c))

# ----------------------------------------------------------
# RENDER DINÂMICO
# ----------------------------------------------------------

frames = []
estado = np.zeros_like(grid)

print("[RENDER] Gerando frames...")

for i, (r, c) in enumerate(trajetoria):

    estado[r, c] = grid[r, c]
    fase_txt = fase_por_frame(i, len(trajetoria))

    fig, ax = plt.subplots(figsize=(10, 5))

    im = ax.imshow(
        estado,
        cmap="inferno",
        vmin=Z_MIN,
        vmax=Z_MAX,
        origin="upper"
    )

    ax.set_xticks(range(COLS))
    ax.set_yticks(range(ROWS))
    ax.grid(color="white", linewidth=0.5, alpha=0.4)

    anos = np.linspace(1940, 2025, COLS, dtype=int)
    ax.set_xticklabels(anos)
    ax.set_xlabel("Anos / Av. Escola Politécnica")
    ax.set_ylabel("USP")

    for geom in gdf.geometry:
        if geom.geom_type == "Polygon":
            xs, ys = geom.exterior.xy
            ax.plot(
                [norm_x(x) for x in xs],
                [norm_y(y) for y in ys],
                color="red",
                linewidth=1.2,
                alpha=0.5
            )

    ax.scatter(
        c, r,
        s=120,
        facecolors="none",
        edgecolors="white",
        linewidths=2
    )

    ax.set_title(
        "Mesa Virtual IPT — DEBUG V2\n"
        f"{fase_txt}",
        fontsize=11
    )

    cbar = plt.colorbar(im, ax=ax, fraction=0.046)
    cbar.set_label("Altura total real (terreno + pino) [m]")

    # ---------- CAPTURA COMPATÍVEL (ARGB → RGB) ----------
    fig.canvas.draw()
    w, h = fig.canvas.get_width_height()

    argb = np.frombuffer(
        fig.canvas.tostring_argb(),
        dtype=np.uint8
    ).reshape((h, w, 4))

    rgb = np.zeros((h, w, 3), dtype=np.uint8)
    rgb[..., 0] = argb[..., 1]
    rgb[..., 1] = argb[..., 2]
    rgb[..., 2] = argb[..., 3]

    frames.append(rgb)
    plt.close(fig)

# ----------------------------------------------------------
# SAVE GIF
# ----------------------------------------------------------

print("[SAVE] Gerando GIF...")
imageio.mimsave(GIF_PATH, frames, fps=FPS)

print("[OK] GIF gerado:")
print(GIF_PATH)
