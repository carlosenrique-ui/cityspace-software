from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image

import dash
from dash import dcc, html, Input, Output, State, ctx
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

VIRTUAL_INTERVAL_MS = 250
REAL_INTERVAL_MS = 1200


def first_existing(paths):
    for p in paths:
        if p.exists():
            return p
    raise FileNotFoundError("Nenhum PNG encontrado.")


def fix_like_v42(grid):
    g = grid.copy()
    if g.dtype.kind in "fc":
        g[6:, 0:3] = np.nan
    else:
        g[6:, 0:3] = False
    g = np.roll(g, -1, axis=0)
    g = np.flipud(g)
    return g


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

    return (
        fix_like_v42(z_terrain_m),
        fix_like_v42(z_total_m),
        fix_like_v42(z_total_cm),
    )


def load_png(path):
    img = Image.open(path).convert("L")
    arr = np.array(img).astype(float)
    arr = (arr - arr.min()) / (np.ptp(arr) + 1e-6)
    return arr


def add_watermark(fig, png):
    rows, cols = GRID_ROWS, GRID_COLS

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
        name="BASE_IPT",
    ))


def contour_segments(Z, interval_m):
    if np.all(np.isnan(Z)):
        return []

    upscale = 35
    smooth_sigma = 1.10

    Z_fill = Z.copy()
    Z_fill[np.isnan(Z_fill)] = np.nanmean(Z_fill)

    Z_hi = zoom(Z_fill, upscale, order=3)
    Z_hi = gaussian_filter(Z_hi, sigma=smooth_sigma)

    mask_hi = zoom((~np.isnan(Z)).astype(float), upscale, order=0) > 0.5
    Z_hi[~mask_hi] = np.nan

    ny, nx = Z_hi.shape
    x = np.linspace(0, GRID_COLS - 1, nx)
    y = np.linspace(0, GRID_ROWS - 1, ny)
    X, Y = np.meshgrid(x, y)

    zmin = np.nanmin(Z_hi)
    zmax = np.nanmax(Z_hi)

    start = max(interval_m, np.ceil(zmin / interval_m) * interval_m)
    levels = np.arange(start, zmax + interval_m, interval_m)

    if len(levels) == 0:
        return []

    fig_tmp, ax = plt.subplots()
    cs = ax.contour(X, Y, Z_hi, levels=levels)
    plt.close(fig_tmp)

    out = []
    for level, segs in zip(cs.levels, cs.allsegs):
        for coords in segs:
            if len(coords) >= 6:
                out.append((float(level), coords))

    return out


def add_contours(fig, segments, name, color, dash, show_labels):
    for level, coords in segments:
        fig.add_trace(go.Scatter(
            x=coords[:, 0],
            y=coords[:, 1],
            mode="lines",
            line=dict(
                color=color,
                width=2.2 if int(level) % 10 == 0 else 1.0,
                dash=dash,
            ),
            opacity=0.85 if int(level) % 10 == 0 else 0.55,
            showlegend=False,
            hovertemplate=f"{name}={level:.0f} m<extra></extra>",
            name=name,
        ))

        if show_labels:
            mid = coords[len(coords) // 2]
            fig.add_trace(go.Scatter(
                x=[mid[0]],
                y=[mid[1]],
                mode="text",
                text=[f"{level:.0f}"],
                textfont=dict(color=color, size=12),
                showlegend=False,
                hoverinfo="skip",
                name=f"COTA_{name}",
            ))


def add_grid_lines(fig):
    for c in range(GRID_COLS + 1):
        fig.add_trace(go.Scatter(
            x=[c - 0.5, c - 0.5],
            y=[-0.5, GRID_ROWS - 0.5],
            mode="lines",
            line=dict(color="rgba(255,255,255,0.45)", width=1),
            showlegend=False,
            hoverinfo="skip",
            name="GRID",
        ))

    for r in range(GRID_ROWS + 1):
        fig.add_trace(go.Scatter(
            x=[-0.5, GRID_COLS - 0.5],
            y=[r - 0.5, r - 0.5],
            mode="lines",
            line=dict(color="rgba(255,255,255,0.45)", width=1),
            showlegend=False,
            hoverinfo="skip",
            name="GRID",
        ))


def build_zigzag_path():
    path = []
    for c in range(GRID_COLS - 1, -1, -1):
        offset = GRID_COLS - 1 - c
        rows = range(0, GRID_ROWS) if offset % 2 == 0 else range(GRID_ROWS - 1, -1, -1)
        for r in rows:
            path.append((r, c))
    return path


def current_grid(step):
    grid = np.full_like(Z_TOTAL_CM, np.nan)
    step = max(0, min(step, len(ZIGZAG_PATH) - 1))

    for i in range(step + 1):
        r, c = ZIGZAG_PATH[i]
        val = Z_TOTAL_CM[r, c]
        if np.isfinite(val) and val > 0:
            grid[r, c] = val

    return grid


def send_to_real_table(row, col, value_cm, mesa_on):
    if not mesa_on:
        return "Mesa Real OFF"

    if not np.isfinite(value_cm) or value_cm <= 0:
        value_cm = 0.0

    return f"SEND_TO_MESA row={row} col={col} z_cm={value_cm:.1f}"


def active_cell_shape(row, col):
    return dict(
        type="rect",
        x0=col - 0.5,
        x1=col + 0.5,
        y0=row - 0.5,
        y1=row + 0.5,
        line=dict(color="white", width=4),
        fillcolor="rgba(255,255,255,0)",
        layer="above",
    )


def add_annotations(fig, cell_mode, projector_mode):
    fig.add_annotation(
        x=7.5,
        y=8.25,
        text="Av. Escola Politécnica →",
        showarrow=False,
        font=dict(size=18, color="black"),
    )

    fig.add_annotation(
        x=14.8,
        y=0.15,
        text=f"N ↑<br>Escala célula: {cell_mode}",
        showarrow=False,
        align="center",
        font=dict(size=13, color="black"),
        bgcolor="rgba(255,255,255,0.70)",
        bordercolor="black",
        borderwidth=1,
    )

    if projector_mode == "invertido":
        fig.add_annotation(
            x=1.2,
            y=0.15,
            text="PROJETOR: 180°",
            showarrow=False,
            font=dict(size=12, color="red"),
            bgcolor="rgba(255,255,255,0.75)",
        )


def make_fig(layers, step, cell_mode, projector_mode):
    fig = go.Figure()

    grid_now = current_grid(step)

    if "base" in layers:
        add_watermark(fig, PNG)

    if "pinos" in layers:
        fig.add_trace(go.Heatmap(
            z=grid_now,
            customdata=np.dstack([Z_TOTAL_M, Z_TERRAIN_M]),
            colorscale="Viridis",
            showscale=True,
            colorbar=dict(title="Pino / Teto<br>(cm / m)"),
            opacity=GRID_OPACITY,
            zmin=np.nanmin(Z_TOTAL_CM),
            zmax=np.nanmax(Z_TOTAL_CM),
            xgap=0,
            ygap=0,
            hovertemplate=(
                "col=%{x}<br>row=%{y}<br>"
                "pino=%{z:.1f} cm<br>"
                "teto=%{customdata[0]:.2f} m<br>"
                "terreno=%{customdata[1]:.2f} m<extra></extra>"
            ),
            name="PINO_Z_TOTAL_CM",
        ))

    if "contour_terrain" in layers:
        add_contours(fig, TERRAIN_CONTOURS, "TERRENO", "black", "solid", "cota_terrain" in layers)

    if "contour_total" in layers:
        add_contours(fig, TOTAL_CONTOURS, "TETO", "white", "dash", "cota_total" in layers)

    if "grid" in layers:
        add_grid_lines(fig)

    step = max(0, min(step, len(ZIGZAG_PATH) - 1))
    r, c = ZIGZAG_PATH[step]
    fig.update_layout(shapes=[active_cell_shape(r, c)])

    add_annotations(fig, cell_mode, projector_mode)

    x_range = [-0.5, GRID_COLS - 0.5]
    y_range = [GRID_ROWS - 0.5, -0.5]

    if projector_mode == "invertido":
        x_range = [GRID_COLS - 0.5, -0.5]
        y_range = [-0.5, GRID_ROWS - 0.5]

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False, range=x_range, constrain="domain"),
        yaxis=dict(visible=False, range=y_range, scaleanchor="x", scaleratio=1),
        plot_bgcolor="white",
        paper_bgcolor="white",
        autosize=True,
    )

    return fig


PNG_PATH = first_existing(PNG_CANDIDATES)
DF = pd.read_csv(CSV_PATH)

Z_TERRAIN_M, Z_TOTAL_M, Z_TOTAL_CM = build_grids(DF)
PNG = load_png(PNG_PATH)

TERRAIN_CONTOURS = contour_segments(Z_TERRAIN_M, interval_m=2.0)
TOTAL_CONTOURS = contour_segments(Z_TOTAL_M, interval_m=5.0)

ZIGZAG_PATH = build_zigzag_path()
TOTAL_STEPS = len(ZIGZAG_PATH)

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Store(id="step-store", data=0),
    dcc.Store(id="playing-store", data=False),

    dcc.Interval(
        id="clock",
        interval=VIRTUAL_INTERVAL_MS,
        n_intervals=0,
        disabled=True,
    ),

    html.Div([
        html.Div("V127 — CitySpace Mesa Final", style={"fontWeight": "bold", "marginBottom": "8px"}),

        dcc.Checklist(
            id="layers",
            options=[
                {"label": "Base IPT", "value": "base"},
                {"label": "Pinos / Teto z_total", "value": "pinos"},
                {"label": "Contour terreno z_terrain_m", "value": "contour_terrain"},
                {"label": "Cotas terreno", "value": "cota_terrain"},
                {"label": "Contour teto z_total_m", "value": "contour_total"},
                {"label": "Cotas teto", "value": "cota_total"},
                {"label": "Grid 16x8", "value": "grid"},
            ],
            value=["base", "pinos", "contour_total", "cota_total", "grid"],
        ),

        html.Hr(),

        html.Div("Célula da mesa"),
        dcc.RadioItems(
            id="cell-mode",
            options=[
                {"label": "1 x 1 cm", "value": "1x1 cm"},
                {"label": "2 x 2 cm", "value": "2x2 cm"},
            ],
            value="1x1 cm",
        ),

        html.Hr(),

        html.Div("Projetor"),
        dcc.RadioItems(
            id="projector-mode",
            options=[
                {"label": "Normal", "value": "normal"},
                {"label": "Invertido 180°", "value": "invertido"},
            ],
            value="normal",
        ),

        html.Hr(),

        html.Div("Mesa real"),
        dcc.RadioItems(
            id="mesa-real",
            options=[
                {"label": "OFF — virtual acelerado", "value": "off"},
                {"label": "ON — mesa real lenta", "value": "on"},
            ],
            value="off",
        ),

        html.Hr(),

        html.Button("◀ Backward", id="btn-back", n_clicks=0),
        html.Button("⏸ Pause", id="btn-pause", n_clicks=0),
        html.Button("▶ Forward", id="btn-forward", n_clicks=0),
        html.Button("⟲ Reset", id="btn-reset", n_clicks=0),

        html.Br(),
        html.Br(),

        html.Div(id="status", style={"fontFamily": "monospace", "fontSize": "12px", "whiteSpace": "pre-wrap"}),

    ], style={
        "position": "fixed",
        "left": "8px",
        "top": "8px",
        "zIndex": 10,
        "width": "350px",
        "background": "rgba(255,255,255,0.90)",
        "padding": "10px",
        "border": "1px solid #ccc",
        "borderRadius": "8px",
        "fontFamily": "Arial",
        "fontSize": "13px",
    }),

    dcc.Graph(
        id="cityspace-v127",
        config={"displayModeBar": False, "scrollZoom": False, "responsive": True},
        style={"width": "100vw", "height": "100vh"},
    )
], style={"margin": 0, "padding": 0, "width": "100vw", "height": "100vh", "overflow": "hidden"})


@app.callback(
    Output("step-store", "data"),
    Output("playing-store", "data"),
    Output("clock", "disabled"),
    Output("clock", "interval"),
    Input("btn-forward", "n_clicks"),
    Input("btn-back", "n_clicks"),
    Input("btn-pause", "n_clicks"),
    Input("btn-reset", "n_clicks"),
    Input("clock", "n_intervals"),
    State("step-store", "data"),
    State("playing-store", "data"),
    State("mesa-real", "value"),
)
def control_loop(nf, nb, npause, nr, tick, step, playing, mesa_real):
    trigger = ctx.triggered_id
    step = int(step or 0)
    playing = bool(playing)

    if trigger == "btn-reset":
        step = 0
        playing = False
    elif trigger == "btn-forward":
        step = min(step + 1, TOTAL_STEPS - 1)
        playing = True
    elif trigger == "btn-back":
        step = max(step - 1, 0)
        playing = False
    elif trigger == "btn-pause":
        playing = False
    elif trigger == "clock" and playing:
        step = min(step + 1, TOTAL_STEPS - 1)
        if step >= TOTAL_STEPS - 1:
            playing = False

    interval = REAL_INTERVAL_MS if mesa_real == "on" else VIRTUAL_INTERVAL_MS
    return step, playing, not playing, interval


@app.callback(
    Output("cityspace-v127", "figure"),
    Output("status", "children"),
    Input("layers", "value"),
    Input("step-store", "data"),
    Input("cell-mode", "value"),
    Input("mesa-real", "value"),
    Input("projector-mode", "value"),
)
def update_ui(layers, step, cell_mode, mesa_real, projector_mode):
    step = int(step or 0)
    row, col = ZIGZAG_PATH[max(0, min(step, TOTAL_STEPS - 1))]
    val = Z_TOTAL_CM[row, col]

    mesa_on = mesa_real == "on"
    hw_msg = send_to_real_table(row, col, val, mesa_on)

    fig = make_fig(layers or [], step, cell_mode, projector_mode)

    status = (
        f"step: {step + 1}/{TOTAL_STEPS}\n"
        f"zigzag: coluna, topo-direita\n"
        f"row={row} col={col}\n"
        f"pino_cm={0.0 if not np.isfinite(val) else val:.1f}\n"
        f"cell={cell_mode}\n"
        f"mesa_real={'ON' if mesa_on else 'OFF'}\n"
        f"clock={'REAL lento' if mesa_on else 'VIRTUAL acelerado'}\n"
        f"projector={projector_mode}\n"
        f"{hw_msg}"
    )

    return fig, status


if __name__ == "__main__":
    print("========================================")
    print("V127 — UI FINAL OPERACIONAL")
    print("========================================")
    print("CSV:", CSV_PATH)
    print("PNG:", PNG_PATH)
    print("Total cells:", TOTAL_STEPS)
    print("Zigzag starts:", ZIGZAG_PATH[0])
    print("Virtual interval ms:", VIRTUAL_INTERVAL_MS)
    print("Real interval ms:", REAL_INTERVAL_MS)
    print("Pino cm min/max:", float(np.nanmin(Z_TOTAL_CM)), float(np.nanmax(Z_TOTAL_CM)))
    print("Contours terreno:", len(TERRAIN_CONTOURS))
    print("Contours teto:", len(TOTAL_CONTOURS))
    print("========================================")
    app.run(debug=True)
