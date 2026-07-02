from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image

import dash
from dash import dcc, html, Input, Output
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

MIN_COMPONENT_CELLS = 4


def first_existing(paths):
    for p in paths:
        if p.exists():
            return p
    raise FileNotFoundError("Nenhum PNG encontrado.")


def build_grids(df):
    z_terrain_m = np.full((GRID_ROWS, GRID_COLS), np.nan)
    z_total_m = np.full((GRID_ROWS, GRID_COLS), np.nan)
    z_total_cm = np.full((GRID_ROWS, GRID_COLS), np.nan)
    valid = np.zeros((GRID_ROWS, GRID_COLS), dtype=bool)

    for _, r in df.iterrows():
        row = int(r["row"])
        col = int(r["col"])

        terrain = float(r["z_terrain_m"])
        total = float(r["z_total_m"])

        if total > 0:
            valid[row, col] = True
            z_terrain_m[row, col] = terrain
            z_total_m[row, col] = total
            z_total_cm[row, col] = total * 100.0

    return z_terrain_m, z_total_m, z_total_cm, valid


def fix_like_v42(grid):
    g = grid.copy()
    g[6:, 0:3] = np.nan if g.dtype.kind == "f" else False
    g = np.roll(g, -1, axis=0)
    g = np.flipud(g)
    return g


def remove_small_components(mask, min_cells=4):
    mask = mask.copy()
    visited = np.zeros_like(mask, dtype=bool)
    rows, cols = mask.shape

    for r in range(rows):
        for c in range(cols):
            if not mask[r, c] or visited[r, c]:
                continue

            stack = [(r, c)]
            comp = []
            visited[r, c] = True

            while stack:
                rr, cc = stack.pop()
                comp.append((rr, cc))

                for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nr, nc = rr + dr, cc + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if mask[nr, nc] and not visited[nr, nc]:
                            visited[nr, nc] = True
                            stack.append((nr, nc))

            if len(comp) < min_cells:
                for rr, cc in comp:
                    mask[rr, cc] = False

    return mask


def apply_mask(Z, mask):
    out = Z.copy()
    out[~mask] = np.nan
    return out


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

    fig.add_trace(go.Heatmap(
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
    ))


def add_contours(fig, Z, mask, name, color, dash, interval_m, width_main=2.0):
    if np.all(np.isnan(Z)):
        return

    upscale = 35
    smooth_sigma = 1.10

    Z_fill = Z.copy()
    Z_fill[np.isnan(Z_fill)] = np.nanmean(Z_fill)

    Z_hi = zoom(Z_fill, upscale, order=3)
    Z_hi = gaussian_filter(Z_hi, sigma=smooth_sigma)

    mask_hi = zoom(mask.astype(float), upscale, order=0) > 0.5
    Z_hi[~mask_hi] = np.nan

    rows, cols = Z.shape
    ny, nx = Z_hi.shape

    x = np.linspace(0, cols - 1, nx)
    y = np.linspace(0, rows - 1, ny)
    X, Y = np.meshgrid(x, y)

    zmin = np.nanmin(Z_hi)
    zmax = np.nanmax(Z_hi)

    start = max(interval_m, np.ceil(zmin / interval_m) * interval_m)
    levels = np.arange(start, zmax + interval_m, interval_m)

    if len(levels) == 0:
        return

    fig_tmp, ax = plt.subplots()
    cs = ax.contour(X, Y, Z_hi, levels=levels)
    plt.close(fig_tmp)

    for level, segments in zip(cs.levels, cs.allsegs):
        for coords in segments:
            if len(coords) < 6:
                continue

            fig.add_trace(go.Scatter(
                x=coords[:, 0],
                y=coords[:, 1],
                mode="lines",
                line=dict(
                    color=color,
                    width=width_main if int(level) % 10 == 0 else 1.0,
                    dash=dash,
                ),
                opacity=0.82 if int(level) % 10 == 0 else 0.55,
                showlegend=False,
                hovertemplate=f"{name}={level:.0f} m<extra></extra>",
                name=name,
            ))


def add_grid_lines(fig, rows, cols):
    for c in range(cols + 1):
        fig.add_trace(go.Scatter(
            x=[c - 0.5, c - 0.5],
            y=[-0.5, rows - 0.5],
            mode="lines",
            line=dict(color="rgba(255,255,255,0.45)", width=1),
            showlegend=False,
            hoverinfo="skip",
            name="GRID",
        ))

    for r in range(rows + 1):
        fig.add_trace(go.Scatter(
            x=[-0.5, cols - 0.5],
            y=[r - 0.5, r - 0.5],
            mode="lines",
            line=dict(color="rgba(255,255,255,0.45)", width=1),
            showlegend=False,
            hoverinfo="skip",
            name="GRID",
        ))


def make_fig(layers):
    rows, cols = z_total_cm.shape
    fig = go.Figure()

    if "base" in layers:
        add_watermark(fig, png, rows, cols)

    if "pinos" in layers:
        fig.add_trace(go.Heatmap(
            z=z_total_cm,
            customdata=z_total_m,
            colorscale="Viridis",
            showscale=True,
            colorbar=dict(title="Pino<br>(cm)"),
            opacity=GRID_OPACITY,
            xgap=0,
            ygap=0,
            hovertemplate=(
                "col=%{x}<br>row=%{y}<br>"
                "pino=%{z:.1f} cm<br>"
                "teto=%{customdata:.2f} m<extra></extra>"
            ),
            name="PINO_Z_TOTAL_CM",
        ))

    if "contour_terrain" in layers:
        add_contours(
            fig,
            z_terrain_m,
            valid_mask,
            name="TERRENO",
            color="black",
            dash="solid",
            interval_m=2.0,
        )

    if "contour_total" in layers:
        add_contours(
            fig,
            z_total_m,
            valid_mask,
            name="TETO",
            color="white",
            dash="dash",
            interval_m=5.0,
            width_main=2.4,
        )

    if "grid" in layers:
        add_grid_lines(fig, rows, cols)

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

z_terrain_raw, z_total_m_raw, z_total_cm_raw, valid_raw = build_grids(df)

z_terrain_m = fix_like_v42(z_terrain_raw)
z_total_m = fix_like_v42(z_total_m_raw)
z_total_cm = fix_like_v42(z_total_cm_raw)

valid_mask = fix_like_v42(valid_raw).astype(bool)
valid_mask = remove_small_components(valid_mask, MIN_COMPONENT_CELLS)

z_terrain_m = apply_mask(z_terrain_m, valid_mask)
z_total_m = apply_mask(z_total_m, valid_mask)
z_total_cm = apply_mask(z_total_cm, valid_mask)

png = load_png(PNG_PATH)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Div("LAYERS", style={"fontWeight": "bold", "marginBottom": "6px"}),
        dcc.Checklist(
            id="layers",
            options=[
                {"label": "Base IPT", "value": "base"},
                {"label": "Pinos z_total_cm", "value": "pinos"},
                {"label": "Contour terreno z_terrain_m", "value": "contour_terrain"},
                {"label": "Contour teto z_total_m", "value": "contour_total"},
                {"label": "Grid 16x8", "value": "grid"},
            ],
            value=["base", "pinos", "contour_terrain", "contour_total", "grid"],
        ),
    ], style={
        "position": "fixed",
        "left": "8px",
        "top": "8px",
        "zIndex": 10,
        "background": "rgba(255,255,255,0.88)",
        "padding": "10px",
        "border": "1px solid #ccc",
        "borderRadius": "8px",
        "fontFamily": "Arial",
        "fontSize": "13px",
    }),
    dcc.Graph(
        id="cityspace-v118",
        config={"displayModeBar": False, "scrollZoom": False, "responsive": True},
        style={"width": "100vw", "height": "100vh"},
    )
], style={"margin": 0, "padding": 0, "width": "100vw", "height": "100vh", "overflow": "hidden"})


@app.callback(
    Output("cityspace-v118", "figure"),
    Input("layers", "value"),
)
def update(layers):
    return make_fig(layers or [])


if __name__ == "__main__":
    print("========================================")
    print("V118 — LAYERS / PINO / TETO / CONTOURS")
    print("========================================")
    print("CSV:", CSV_PATH)
    print("PNG:", PNG_PATH)
    print("Pino cm min/max:", float(np.nanmin(z_total_cm)), float(np.nanmax(z_total_cm)))
    print("Teto m min/max:", float(np.nanmin(z_total_m)), float(np.nanmax(z_total_m)))
    print("Terrain m min/max:", float(np.nanmin(z_terrain_m)), float(np.nanmax(z_terrain_m)))
    print("Valid cells:", int(valid_mask.sum()))
    print("========================================")
    app.run(debug=True)
