"""
IPT-CITYSPACE
Mesa Virtual — GIF Temporal V41.2 (WATERMARK FIX)

✔ Raster IPT sempre visível
✔ Grid sobreposto (viridis)
✔ Sem branco artificial
✔ Compatível NumPy 2
✔ Robusto (WSL + CSV)
"""

# ============================================================
# ROOT DETECTION (BLINDADO)
# ============================================================

import sys
from pathlib import Path

ENGINE_ROOT = Path(__file__).resolve()
while ENGINE_ROOT.name != "ipt-cityspace-engine":
    ENGINE_ROOT = ENGINE_ROOT.parent

if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
from PIL import Image

from online.core.physical_motion_profile import generate_motion_steps

# ============================================================
# PATHS
# ============================================================

DATA_DIR = ENGINE_ROOT / "offline/products/snapshots/ipt_fase2_semantic"

GRID_PINO_CM = DATA_DIR / "grid_pino_cm.csv"
GRID_Z_TOTAL = DATA_DIR / "grid_z_total_m.csv"
RASTER_IPT = DATA_DIR / "ipt_base_raster_aligned_final.png"

OUT_DIR = ENGINE_ROOT / "visualization"
OUT_DIR.mkdir(parents=True, exist_ok=True)

GIF_PATH = OUT_DIR / "mesa_virtual_v41_2.gif"

# ============================================================
# PARAMETROS
# ============================================================

ALTURA_MAX_PINO_M = 0.10
DURACAO_FRAME = 0.10
URBAN_THRESHOLD = 0.35

# ============================================================
# FASES (DALTONICO SAFE)
# ============================================================

FASES = [
    (1940, 1959, "Implantação", "#440154"),
    (1960, 1979, "Expansão", "#31688E"),
    (1980, 1999, "Consolidação", "#35B779"),
    (2000, 2015, "Inovação", "#FDE725"),
]

# ============================================================

def load_csv_robust(path):
    try:
        return np.loadtxt(path, delimiter=";")
    except:
        try:
            return np.loadtxt(path, delimiter=",")
        except:
            data = []
            with open(path) as f:
                for line in f:
                    if ";" in line:
                        parts = line.strip().split(";")
                    else:
                        parts = line.strip().split(",")
                    data.append([float(x) for x in parts])
            return np.array(data)

# ============================================================

def get_fase(ano):
    for inicio, fim, nome, cor in FASES:
        if inicio <= ano <= fim:
            return nome, cor, f"{inicio}–{fim}"
    return "Fase", "#444444", ""

def canvas_to_rgb(fig):
    fig.canvas.draw()
    w, h = fig.canvas.get_width_height()
    argb = np.frombuffer(fig.canvas.tostring_argb(), dtype=np.uint8)
    argb = argb.reshape((h, w, 4))
    return argb[..., 1:4]

def zigzag(rows, cols):
    traj = []
    for x in range(cols):
        ys = range(rows) if x % 2 == 0 else range(rows - 1, -1, -1)
        for y in ys:
            traj.append((x, y))
    return traj

# ============================================================

def main():

    print("\n======================================")
    print("IPT-CITYSPACE — RENDER V41.2 (WATERMARK)")
    print("======================================")

    print("[1] Loading CSVs...")

    grid_cm = load_csv_robust(GRID_PINO_CM)
    grid_z = load_csv_robust(GRID_Z_TOTAL)

    print("[2] Loading raster...")

    raster = np.array(Image.open(RASTER_IPT).convert("L"))
    raster = (raster - raster.min()) / (np.ptp(raster) + 1e-6)

    urban_mask = raster > URBAN_THRESHOLD

    rows, cols = grid_cm.shape
    anos = np.linspace(1940, 2015, cols).astype(int)

    estado = np.zeros_like(grid_cm) / 100
    grid_m = grid_cm / 100

    traj = zigzag(rows, cols)

    print(f"[3] Grid: {rows}x{cols}")
    print(f"[4] Steps: {len(traj)}\n")

    cmap = plt.cm.viridis

    with imageio.get_writer(GIF_PATH, mode="I", duration=DURACAO_FRAME) as writer:

        for idx, (x, y) in enumerate(traj, start=1):

            altura = grid_m[y, x]

            ano = anos[x]
            fase_nome, fase_cor, periodo = get_fase(ano)

            print(f"[{idx:03d}/128] x={x} y={y} | {fase_nome}")

            ry = int((y / rows) * raster.shape[0])
            rx = int((x / cols) * raster.shape[1])

            is_urban = urban_mask[ry, rx]

            if is_urban:
                estado[y, x] = altura
            else:
                estado[y, x] = 0.0

            fig, ax = plt.subplots(figsize=(12, 6))

            # ===== BASE: IPT SEMPRE VISÍVEL =====
            ax.imshow(
                raster,
                cmap="gray",
                extent=(-0.5, cols-0.5, rows-0.5, -0.5),
                alpha=0.35,
                zorder=0
            )

            # ===== GRID SOBREPOSTO =====
            im = ax.imshow(
                estado,
                cmap=cmap,
                origin="upper",
                vmin=0,
                vmax=ALTURA_MAX_PINO_M,
                alpha=0.85,
                zorder=1
            )

            ax.add_patch(
                plt.Rectangle(
                    (x-0.5, y-0.5),
                    1, 1,
                    fill=False,
                    edgecolor="black",
                    linewidth=1.2
                )
            )

            ax.set_title(
                f"IPT – CitySpace | {fase_nome} ({periodo})",
                fontsize=14,
                fontweight="bold",
                color=fase_cor
            )

            ax.set_xticks(range(x+1))
            ax.set_xticklabels(anos[:x+1], fontsize=9)

            ax.set_yticks([])

            cbar = plt.colorbar(im, ax=ax, fraction=0.04, pad=0.03)
            cbar.set_label("Altura (m)", fontsize=9)

            frame = canvas_to_rgb(fig)
            writer.append_data(frame)
            plt.close(fig)

    print("\n[OK] GIF gerado:")
    print(GIF_PATH)

# ============================================================

if __name__ == "__main__":
    main()