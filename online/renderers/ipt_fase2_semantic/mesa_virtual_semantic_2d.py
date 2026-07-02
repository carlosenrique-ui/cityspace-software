#!/usr/bin/env python3
# ==========================================================
# MESA VIRTUAL SEMÂNTICA 2D — IPT CITYSPACE
# ==========================================================
# Origem (0,0,0): CANTO SUPERIOR DIREITO
# Zig-zag: cima → baixo | esquerda → direita (mundo real)
# Cores: altura real (Z_total_real)
# DXF: planta do IPT como marca d’água
# ==========================================================

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import geopandas as gpd

# ==========================================================
# UTIL — CANVAS → RGB (Matplotlib moderno)
# ==========================================================

def canvas_to_rgb(fig):
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

    return rgb

# ==========================================================
# PATHS
# ==========================================================

ENGINE_ROOT = Path(__file__).resolve().parents[3]

SNAPSHOT_DIR = (
    ENGINE_ROOT
    / "offline"
    / "products"
    / "snapshots"
    / "ipt_fase2_semantic"
)

GRID_PATH = SNAPSHOT_DIR / "grid_z_total_m.csv"

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

GIF_PATH = OUT_DIR / "mesa_virtual_semantica_ipt.gif"

# ==========================================================
# CONFIGURAÇÕES DA MESA
# ==========================================================

ROWS = 8
COLS = 16
ALTURA_MAX_M = 0.10
FPS = 6
DXF_ALPHA = 0.30

# ==========================================================
# FASES DO IPT (DOCUMENTO OFICIAL)
# ==========================================================

FASES = [
    "1940–1959 · Formação inicial",
    "1960–1979 · Consolidação tecnológica",
    "1980–1999 · Expansão institucional",
    "2000–2015 · Modernização",
    "2016–2025 · Inovação & sustentabilidade",
]

def fase_por_indice(idx):
    total = ROWS * COLS
    bloco = total // len(FASES)
    return FASES[min(idx // bloco, len(FASES) - 1)]

# ==========================================================
# LOAD GRID
# ==========================================================

print("[LOAD] Grid semântico (Z_total_real)")
grid_m = np.loadtxt(GRID_PATH, delimiter=";")
assert grid_m.shape == (ROWS, COLS)

estado = np.zeros_like(grid_m)

# ==========================================================
# LOAD DXF
# ==========================================================

print("[LOAD] DXF (planta IPT)")
gdf = gpd.read_file(DXF_PATH)

minx, miny, maxx, maxy = gdf.total_bounds

def norm_x(x):
    # eixo X invertido (origem à direita)
    return (maxx - x) / (maxx - minx) * COLS

def norm_y(y):
    return (y - miny) / (maxy - miny) * ROWS

# ==========================================================
# SCANNER ZIG-ZAG (ORIGEM NO CANTO SUPERIOR DIREITO)
# ==========================================================

trajetoria = []

for c in range(COLS - 1, -1, -1):  # esquerda → direita (mundo real)
    if (COLS - 1 - c) % 2 == 0:
        for r in range(ROWS):            # cima → baixo
            trajetoria.append((r, c))
    else:
        for r in range(ROWS - 1, -1, -1):
            trajetoria.append((r, c))

# ==========================================================
# RENDER
# ==========================================================

frames = []

print("[RENDER] Gerando frames...")

for idx, (r, c) in enumerate(trajetoria, start=1):

    estado[r, c] = grid_m[r, c]
    fase_txt = fase_por_indice(idx - 1)

    fig, ax = plt.subplots(figsize=(10, 5))

    im = ax.imshow(
        estado,
        cmap="inferno",
        vmin=0,
        vmax=ALTURA_MAX_M,
        origin="upper"
    )

    # GRID
    ax.set_xticks(np.arange(-0.5, COLS, 1))
    ax.set_yticks(np.arange(-0.5, ROWS, 1))
    ax.grid(color="white", linewidth=0.5, alpha=0.4)

    ax.set_xticks(range(COLS))
    ax.set_yticks(range(ROWS))

    ax.set_xlabel("Ano / Av. Politécnica")
    ax.set_ylabel("USP")

    # DXF OVERLAY — PLANTA IPT
    for geom in gdf.geometry:
        if geom.geom_type == "Polygon":
            xs, ys = geom.exterior.xy
            ax.plot(
                [norm_x(x) for x in xs],
                [norm_y(y) for y in ys],
                color="red",
                linewidth=1.2,
                alpha=DXF_ALPHA
            )

    # SCANNER
    ax.scatter(
        c, r,
        s=120,
        facecolors="none",
        edgecolors="white",
        linewidths=2
    )

    ax.set_title(
        "Mesa Virtual 8×16 — IPT CitySpace\n"
        f"{fase_txt}\n"
        f"Célula {idx}/128 | Z_total = {estado[r, c]:.2f} m",
        fontsize=11
    )

    cbar = plt.colorbar(im, ax=ax, fraction=0.046)
    cbar.set_label("Altura real total (m)")

    frames.append(canvas_to_rgb(fig))
    plt.close(fig)

print("[RENDER] Salvando GIF...")

imageio.mimsave(GIF_PATH, frames, fps=FPS)

print("✔ GIF gerado com sucesso:")
print(GIF_PATH)
