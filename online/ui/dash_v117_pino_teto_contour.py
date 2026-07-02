from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image

import dash
from dash import dcc, html
import plotly.graph_objects as go

from scipy.ndimage import zoom, gaussian_filter
import matplotlib.pyplot as plt


THIS_FILE = Path(__file__).resolve()
CORE_ROOT = THIS_FILE.parents[2]
PROJECT_ROOT = CORE_ROOT.parent

CSV_PATH = CORE_ROOT / "offline/products/scientific/grid_metrics_utm.csv"

PNG_CANDIDATES = [
    CORE_ROOT / "offline/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_final.png",
    PROJECT_ROOT / "offline/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_final.png",
]

GRID_ROWS = 8
GRID_COLS = 16

OFFSET_X = -0.90
OFFSET_Y = -0.10
PNG_SCALE_X = 0.76
PNG_SCALE_Y = 0.60
PNG_OPACITY = 0.80
GRID_OPACITY = 0.88

SHOW_CONTOUR = True


def first_existing(paths):
    for p in paths:
        if p.exists():
            return p
    raise FileNotFoundError("Nenhum PNG encontrado.")


def build_grids(df):
    z_terrain_m = np.full((GRID_ROWS, GRID_COLS), np.nan)
    z_total_m = np.full((GRID_ROWS, GRID_COLS), np.nan)
    z_total_cm = np.full((GRID_ROWS, GRID_COLS), np.nan)

    for _, r in df.iterrows():
        row = int(r["row"])
        col = int(r["col"])

        terrain = float(r["z_terrain_m"])
        total = float(r["z_total_m"])

        if terrain > 0:
            z_terrain_m[row, col] = terrain

        if total > 0:
            z_total_m[row, col] = total
            z_total_cm[row, col] = total * 100.0

    return z_terrain_m, z_total_m, z_total_cm


def fix_grid_like_v42_and_flip(grid):
    g = grid.copy()
    g[6:, 0:3] = np.nan
    g = np.roll(g, -1, axis=0)
    g = np.flipud(g)
    return g


def load_png(path):
    img = Image.open(path).convert("L")
    arr = np.array(img).astype(float)
    arr = (arr - arr.min()) / (np.ptp(arr) + 1e-6)
    return arr


def add_watermark(fig, png, rows, cols):
    x_left = -0.5 + OFFSET_X
    x_right = cols - 0.5 + OFFSET_X
    y_top = -0.5 + OFFSET_Y
    y_bottom = rows - 0.5 + OFFSET_Y

    cx = (x_left + x_right) / 2
    cy = (y_top + y_bottom) / 2

    width = (x_right - x_left) * PNG_SCALE_X
    height = (y_bottom - y_top) * PNG_SCALE_Y

    x_left = cx - width / 2
    x_right = cx + width / 2
    y_top = cy - height / 2
    y_bottom = cy + height / 2

    fig.add_trace(
        go.Heatmap(
            z=png,
            x0=x_left,
            dx=(x_right - x_left) / png.shape[1],
            y0=y_top,
            dy=(y_bottom - y_top) / png.shape[0],
            colorscale="Greys",
            showscale=False,
            opacity=PNG_OPACITY,
            hoverinfo="skip",
            name="BASE_RASTER",
        )
    )


def add_terrain_contours(fig, z_terrain_m):
    Z = z_terrain_m.copy()

    if np.all(np.isnan(Z)):
        return

    upscale = 35
    smooth_sigma = 1.10
    interval_m = 2.0

    Z_fill = Z.copy()
    Z_fill[np.isnan(Z_fill)] = np.nanmean(Z_fill)

    Z_hi = zoom(Z_fill, upscale, order=3)
    Z_hi = gaussian_filter(Z_hi, sigma=smooth_sigma)

    mask_hi = zoom((~np.isnan(Z)).astype(float), upscale, order=0) > 0.5
    Z_hi[~mask_hi] = np.nan

    rows, cols = Z.shape
    ny, nx = Z_hi.shape

    x = np.linspace(0, cols - 1, nx)
    y = np.linspace(0, rows - 1, ny)
    X, Y = np.meshgrid(x, y)

    zmin = np.nanmin(Z_hi)
    zmax = np.nanmax(Z_hi)

    levels = np.arange(
        np.ceil(zmin / interval_m) * interval_m,
        zmax + interval_m,
        interval_m,
    )

    if len(levels) == 0:
        return

    fig_tmp, ax = plt.subplots()
    cs = ax.contour(X, Y, Z_hi, levels=levels)
    plt.close(fig_tmp)

    for level, segments in zip(cs.levels, cs.allsegs):
        for coords in segments:
            if len(coords) < 6:
                continue

            fig.add_trace(
                go.Scatter(
                    x=coords[:, 0],
                    y=coords[:, 1],
                    mode="lines",
                    line=dict(color="black", width=2.0 if int(level) % 10 == 0 else 1.0),
                    opacity=0.80 if int(level) % 10 == 0 else 0.50,
                    showlegend=False,
                    hovertemplate=f"terreno={level:.0f} m<extra></extra>",
                    name="CONTOUR_TERRAIN",
                )
            )


def make_fig(z_total_cm, z_total_m, z_terrain_m, png):
    rows, cols = z_total_cm.shape
    fig = go.Figure()

    add_watermark(fig, png, rows, cols)

    fig.add_trace(
        go.Heatmap(
            z=z_total_cm,
            colorscale="Viridis",
            showscale=True,
            colorbar=dict(title="Pino<br>(cm)"),
            opacity=GRID_OPACITY,
            xgap=0,
            ygap=0,
            hovertemplate="col=%{x}<br>row=%{y}<br>pino=%{z:.1f} cm<extra></extra>",
            name="PINO_Z_TOTAL_CM",
        )
    )

    if SHOW_CONTOUR:
        add_terrain_contours(fig, z_terrain_m)

    fig.add_trace(
        go.Heatmap(
            z=z_total_m,
            colorscale="Viridis",
            showscale=False,
            opacity=0.0,
            hovertemplate="col=%{x}<br>row=%{y}<br>teto=%{z:.2f} m<extra></extra>",
            name="TETO_Z_TOTAL_M",
        )
    )

    for c in range(cols + 1):
        fig.add_trace(
            go.Scatter(
                x=[c - 0.5, c - 0.5],
                y=[-0.5, rows - 0.5],
                mode="lines",
                line=dict(color="rgba(255,255,255,0.45)", width=1),
                showlegend=False,
                hoverinfo="skip",
                name="GRID",
            )
        )

    for r in range(rows + 1):
        fig.add_trace(
            go.Scatter(
                x=[-0.5, cols - 0.5],
                y=[r - 0.5, r - 0.5],
                mode="lines",
                line=dict(color="rgba(255,255,255,0.45)", width=1),
                showlegend=False,
                hoverinfo="skip",
                name="GRID",
            )
        )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False, range=[-0.5, cols - 0.5], constrain="domain"),
        yaxis=dict(visible=False, range=[rows - 0.5, -0.5], scaleanchor="x", scaleratio=1),
        plot_bgcolor="white",
        paper_bgcolor="white",
        autosize=True,
    )

    return fig


PNG_PATH = first_existing(PNG_CANDIDATES)

df = pd.read_csv(CSV_PATH)

z_terrain_raw, z_total_m_raw, z_total_cm_raw = build_grids(df)

z_terrain_m = fix_grid_like_v42_and_flip(z_terrain_raw)
z_total_m = fix_grid_like_v42_and_flip(z_total_m_raw)
z_total_cm = fix_grid_like_v42_and_flip(z_total_cm_raw)

png = load_png(PNG_PATH)

fig = make_fig(z_total_cm, z_total_m, z_terrain_m, png)

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(
            id="cityspace-v117",
            figure=fig,
            config={"displayModeBar": False, "scrollZoom": False, "responsive": True},
            style={"width": "100vw", "height": "100vh"},
        )
    ],
    style={"margin": 0, "padding": 0, "width": "100vw", "height": "100vh", "overflow": "hidden"},
)

if __name__ == "__main__":
    print("========================================")
    print("V117 — PINO / TETO / CONTOUR")
    print("========================================")
    print("CSV:", CSV_PATH)
    print("PNG:", PNG_PATH)
    print("Pino cm min/max:", float(np.nanmin(z_total_cm)), float(np.nanmax(z_total_cm)))
    print("Teto m min/max:", float(np.nanmin(z_total_m)), float(np.nanmax(z_total_m)))
    print("Terrain m min/max:", float(np.nanmin(z_terrain_m)), float(np.nanmax(z_terrain_m)))
    print("Contour layer:", SHOW_CONTOUR)
    print("========================================")
    app.run(debug=True)
