from pathlib import Path
import base64
import numpy as np
import pandas as pd
from PIL import Image

import dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go

from scipy.ndimage import zoom, gaussian_filter
import matplotlib.pyplot as plt


# =========================================
# PATHS / CONFIG
# =========================================

THIS_FILE = Path(__file__).resolve()
CORE_ROOT = THIS_FILE.parents[2]
PROJECT_ROOT = CORE_ROOT.parent

CSV_PATH = CORE_ROOT / "offline/products/scientific/grid_metrics_utm.csv"

PNG_CANDIDATES = [
    CORE_ROOT / "offline/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_final.png",
    PROJECT_ROOT / "offline/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_final.png",
]

NORTH_CANDIDATES = [
    CORE_ROOT / "online/assets/north_arrow_scale.png",
    PROJECT_ROOT / "online/assets/north_arrow_scale.png",
    CORE_ROOT / "assets/north_arrow_scale.png",
    PROJECT_ROOT / "assets/north_arrow_scale.png",
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

TETO_MAX_M = 40.0
PINO_MAX_CM = 10.0


# =========================================
# LOADERS
# =========================================

def first_existing(paths, required=True):
    for p in paths:
        if p.exists():
            return p
    if required:
        raise FileNotFoundError("Nenhum arquivo encontrado.")
    return None


def image_to_data_uri(path):
    if path is None:
        return None
    data = Path(path).read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:image/png;base64,{b64}"


def fix_like_v42(grid):
    g = grid.copy()
    g = np.roll(g, -1, axis=0)
    g = np.flipud(g)
    return g


def build_grids(df):
    z_terrain_m = np.full((GRID_ROWS, GRID_COLS), np.nan)
    z_total_m = np.full((GRID_ROWS, GRID_COLS), np.nan)

    for _, r in df.iterrows():
        row = int(r["row"])
        col = int(r["col"])

        terrain = float(r["z_terrain_m"])
        total = float(r["z_total_m"])

        if terrain > 0:
            z_terrain_m[row, col] = terrain

        if total > 0:
            z_total_m[row, col] = total

    z_terrain_m = fix_like_v42(z_terrain_m)
    z_total_m = fix_like_v42(z_total_m)

    z_pino_cm = (z_total_m / TETO_MAX_M) * PINO_MAX_CM
    z_pino_cm = np.clip(z_pino_cm, 0, PINO_MAX_CM)

    return z_terrain_m, z_total_m, z_pino_cm


# =========================================
# ZIGZAG — COLUNA / CANTO SUPERIOR ESQUERDO
# =========================================

def build_zigzag_path():
    path = []

    for c in range(0, GRID_COLS):
        if c % 2 == 0:
            rows = range(0, GRID_ROWS)
        else:
            rows = range(GRID_ROWS - 1, -1, -1)

        for r in rows:
            path.append((r, c))

    return path


# =========================================
# CONTOURS
# =========================================

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


# =========================================
# DRAW HELPERS
# =========================================

def add_watermark(fig):
    x_left = -0.5 + OFFSET_X
    x_right = GRID_COLS - 0.5 + OFFSET_X
    y_top = -0.5 + OFFSET_Y
    y_bottom = GRID_ROWS - 0.5 + OFFSET_Y

    cx = (x_left + x_right) / 2
    cy = (y_top + y_bottom) / 2

    width = (x_right - x_left) * PNG_SCALE_X
    height = (y_bottom - y_top) * PNG_SCALE_Y

    x_left = cx - width / 2
    y_top = cy - height / 2

    fig.add_layout_image(
        dict(
            source=PNG_URI,
            xref="x",
            yref="y",
            x=x_left,
            y=y_top,
            sizex=width,
            sizey=height,
            sizing="stretch",
            opacity=PNG_OPACITY,
            layer="below",
            xanchor="left",
            yanchor="top",
        )
    )


def add_north_scale(fig):
    if NORTH_URI is not None:
        fig.add_layout_image(
            dict(
                source=NORTH_URI,
                xref="paper",
                yref="paper",
                x=-0.035,
                y=0.02,
                sizex=0.25,
                sizey=0.25,
                sizing="contain",
                opacity=1.0,
                layer="above",
                xanchor="left",
                yanchor="bottom",
            )
        )
    else:
        fig.add_annotation(
            x=-0.035,
            y=0.02,
            xref="paper",
            yref="paper",
            text="N ↑",
            showarrow=False,
        )


def add_grid_lines(fig):
    for c in range(GRID_COLS + 1):
        fig.add_trace(go.Scatter(
            x=[c - 0.5, c - 0.5],
            y=[-0.5, GRID_ROWS - 0.5],
            mode="lines",
            line=dict(color="rgba(255,255,255,0.50)", width=1),
            showlegend=False,
            hoverinfo="skip",
            name="GRID",
        ))

    for r in range(GRID_ROWS + 1):
        fig.add_trace(go.Scatter(
            x=[-0.5, GRID_COLS - 0.5],
            y=[r - 0.5, r - 0.5],
            mode="lines",
            line=dict(color="rgba(255,255,255,0.50)", width=1),
            showlegend=False,
            hoverinfo="skip",
            name="GRID",
        ))


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


def add_annotations(fig, cell_mode):
    fig.add_annotation(
        x=-0.035,
        y=0.22,
        xref="paper",
        yref="paper",
        text="USP",
        showarrow=False,
        textangle=-90,
        font=dict(size=18, color="black"),
        bgcolor="rgba(255,255,255,0.78)",
        bordercolor="black",
        borderwidth=1,
        xanchor="center",
        yanchor="middle",
    )

    fig.add_annotation(
        x=0.50,
        y=-0.12,
        xref="paper",
        yref="paper",
        text="Av. Escola Politécnica",
        showarrow=False,
        font=dict(size=18, color="black"),
        bgcolor="rgba(255,255,255,0.78)",
        bordercolor="black",
        borderwidth=1,
        xanchor="center",
        yanchor="top",
    )


def current_grid(step):
    z = np.zeros_like(Z_PINO_CM)

    step = int(step or 0)
    step = max(0, min(step, TOTAL_STEPS - 1))

    for i in range(step + 1):
        r, c = ZIGZAG_PATH[i]
        val = Z_PINO_CM[r, c]
        if np.isfinite(val) and val > 0:
            z[r, c] = val

    return z


def make_fig(layers, step, cell_mode, projector_mode):
    fig = go.Figure()

    if "base" in layers:
        add_watermark(fig)

    z_display = current_grid(step)

    if "pinos" in layers:
        fig.add_trace(go.Heatmap(
            z=z_display,
            customdata=Z_TOTAL_M,
            colorscale=[
                [0.00, "black"],
                [0.001, "black"],
                [0.02, "#440154"],
                [0.25, "#31688e"],
                [0.50, "#35b779"],
                [0.75, "#fde725"],
                [1.00, "#fde725"],
            ],
            showscale=True,
            colorbar=dict(
                title="Pino(cm)<br>Teto(m)",
                tickmode="array",
                tickvals=[0, 2.5, 5, 7.5, 10],
                ticktext=["0 / 0", "2.5 / 10", "5 / 20", "7.5 / 30", "10 / 40"],
                x=1.02,
            ),
            opacity=GRID_OPACITY,
            zmin=0,
            zmax=PINO_MAX_CM,
            xgap=0,
            ygap=0,
            hovertemplate=(
                "col=%{x}<br>row=%{y}<br>"
                "pino=%{z:.2f} cm<br>"
                "teto=%{customdata:.2f} m<extra></extra>"
            ),
            name="PINO_Z_TOTAL_CM",
        ))

    if "contour_terrain" in layers:
        add_contours(fig, TERRAIN_CONTOURS, "TERRENO", "black", "solid", "cota_terrain" in layers)

    if "contour_total" in layers:
        add_contours(fig, TOTAL_CONTOURS, "TETO", "white", "dash", "cota_total" in layers)

    if "grid" in layers:
        add_grid_lines(fig)

    step = max(0, min(int(step or 0), TOTAL_STEPS - 1))
    row, col = ZIGZAG_PATH[step]
    fig.update_layout(shapes=[active_cell_shape(row, col)])

    add_annotations(fig, cell_mode)
    add_north_scale(fig)

    x_range = [-0.5, GRID_COLS - 0.5]
    y_range = [GRID_ROWS - 0.5, -0.5]

    if projector_mode == "invertido":
        x_range = [GRID_COLS - 0.5, -0.5]
        y_range = [-0.5, GRID_ROWS - 0.5]

    fig.update_layout(
        margin=dict(l=95, r=90, t=70, b=260),
        xaxis=dict(visible=False, range=x_range, constrain="domain"),
        yaxis=dict(visible=False, range=y_range, scaleanchor="x", scaleratio=1),
        plot_bgcolor="white",
        paper_bgcolor="white",
        autosize=True,
        uirevision="v128_7_18",
    )

    return fig


def send_to_real_table(row, col, value_cm, mesa_on):
    if not mesa_on:
        return "Mesa Real OFF"

    if not np.isfinite(value_cm) or value_cm <= 0:
        value_cm = 0.0

    return f"MODO REAL SIMULADO row={row} col={col} z_cm={value_cm:.2f}"


# =========================================
# DATA LOAD
# =========================================

PNG_PATH = first_existing(PNG_CANDIDATES)
NORTH_PATH = first_existing(NORTH_CANDIDATES, required=False)

DF = pd.read_csv(CSV_PATH)

Z_TERRAIN_M, Z_TOTAL_M, Z_PINO_CM = build_grids(DF)

# Remover ruído: 3 células do canto superior direito
Z_TERRAIN_M[0, GRID_COLS-3:GRID_COLS] = np.nan
Z_TOTAL_M[0, GRID_COLS-3:GRID_COLS] = np.nan
Z_PINO_CM[0, GRID_COLS-3:GRID_COLS] = np.nan

PNG_URI = image_to_data_uri(PNG_PATH)
NORTH_URI = image_to_data_uri(NORTH_PATH) if NORTH_PATH is not None else None

TERRAIN_CONTOURS = contour_segments(Z_TERRAIN_M, interval_m=2.0)
TOTAL_CONTOURS = contour_segments(Z_TOTAL_M, interval_m=5.0)

ZIGZAG_PATH = build_zigzag_path()
TOTAL_STEPS = len(ZIGZAG_PATH)


# =========================================
# DASH
# =========================================

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Store(id="step-store", data=0),
    dcc.Store(id="playing-store", data=False),
    dcc.Store(id="direction-store", data=1),

    dcc.Interval(
        id="clock",
        interval=VIRTUAL_INTERVAL_MS,
        n_intervals=0,
        disabled=True,
    ),

    html.Div([
        html.Button("☰ MENU", id="btn-menu", n_clicks=0),

        html.Div(id="menu-body", children=[
            html.Br(),

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

            html.Div("Escala visual"),
            dcc.RadioItems(
                id="cell-mode",
                options=[
                    {"label": "1 x 1 cm", "value": "1x1 cm"},
                    {"label": "2 x 2 cm", "value": "2x2 cm"},
                ],
                value="1x1 cm",
            ),

            html.Hr(),

            html.Div(id="cartographic-scale", style={
                "fontWeight": "bold",
                "marginBottom": "6px",
            }),

            html.Hr(),

            dcc.RadioItems(
                id="projector-mode",
                options=[
                    {"label": "Normal", "value": "normal"},
                    {"label": "Invertido 180°", "value": "invertido"},
                ],
                value="normal",
            ),

            html.Hr(),

            html.Div("Mesa"),
            dcc.RadioItems(
                id="mesa-real",
                options=[
                    {"label": "OFF", "value": "off"},
                    {"label": "ON — real", "value": "on"},
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

            html.Div(id="status", style={"display": "none"}),
        ]),

    ], id="menu-panel", style={
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

    html.Div([
        dcc.Graph(
            id="cityspace-v128718",
            config={"displayModeBar": False, "scrollZoom": False, "responsive": True},
            style={"width": "100%", "height": "100%"},
        )
    ], id="graph-wrap", style={
        "width": "fit-content",
        "minWidth": "32cm",
        "margin": "24px auto",
        "display": "block",
    })

], style={
    "margin": 0,
    "padding": 0,
    "width": "100vw",
    "minHeight": "100vh",
    "overflowX": "auto",
    "overflowY": "auto",
    "background": "white",
})



@app.callback(
    Output("cartographic-scale", "children"),
    Input("cell-mode", "value"),
)
def update_cartographic_scale(cell_mode):
    if cell_mode == "2x2 cm":
        return "Escala Cartográfica: 1:4433"
    return "Escala Cartográfica: 1:8867"


# =========================================
# CALLBACK — MENU
# =========================================

@app.callback(
    Output("menu-body", "style"),
    Output("menu-panel", "style"),
    Input("btn-menu", "n_clicks"),
)
def toggle_menu(n_clicks):
    open_menu = (n_clicks or 0) % 2 == 1

    panel_style = {
        "position": "fixed",
        "left": "8px",
        "top": "8px",
        "zIndex": 10,
        "background": "rgba(255,255,255,0.90)",
        "padding": "10px",
        "border": "1px solid #ccc",
        "borderRadius": "8px",
        "fontFamily": "Arial",
        "fontSize": "13px",
    }

    if open_menu:
        panel_style["width"] = "350px"
        return {"display": "block"}, panel_style

    panel_style["width"] = "95px"
    return {"display": "none"}, panel_style


# =========================================
# CALLBACK — CONTROLES
# =========================================

@app.callback(
    Output("step-store", "data"),
    Output("playing-store", "data"),
    Output("direction-store", "data"),
    Output("clock", "disabled"),
    Output("clock", "interval"),
    Input("btn-forward", "n_clicks"),
    Input("btn-back", "n_clicks"),
    Input("btn-pause", "n_clicks"),
    Input("btn-reset", "n_clicks"),
    Input("clock", "n_intervals"),
    State("step-store", "data"),
    State("playing-store", "data"),
    State("direction-store", "data"),
    State("mesa-real", "value"),
)
def control_loop(nf, nb, npause, nr, tick, step, playing, direction, mesa_real):
    trigger = ctx.triggered_id

    step = int(step or 0)
    playing = bool(playing)
    direction = int(direction or 1)

    if trigger == "btn-reset":
        step = 0
        playing = False
        direction = 1

    elif trigger == "btn-forward":
        direction = 1
        step = min(step + 1, TOTAL_STEPS - 1)
        playing = True

    elif trigger == "btn-back":
        direction = -1
        step = max(step - 1, 0)
        playing = True

    elif trigger == "btn-pause":
        playing = False

    elif trigger == "clock" and playing:
        step = step + direction

        if step >= TOTAL_STEPS:
            step = TOTAL_STEPS - 1
            playing = False

        if step < 0:
            step = 0
            playing = False

    interval = REAL_INTERVAL_MS if mesa_real == "on" else VIRTUAL_INTERVAL_MS

    return step, playing, direction, not playing, interval


# =========================================
# CALLBACK — RENDER
# =========================================

@app.callback(
    Output("cityspace-v128718", "figure"),
    Output("status", "children"),
    Output("graph-wrap", "style"),
    Input("layers", "value"),
    Input("step-store", "data"),
    Input("cell-mode", "value"),
    Input("mesa-real", "value"),
)
def update_ui(layers, step, cell_mode, mesa_real):
    projector_mode = "normal"
    step = int(step or 0)
    step = max(0, min(step, TOTAL_STEPS - 1))

    row, col = ZIGZAG_PATH[step]
    val = Z_PINO_CM[row, col]

    mesa_on = mesa_real == "on"
    hw_msg = send_to_real_table(row, col, val, mesa_on)

    fig = make_fig(layers or [], step, cell_mode, projector_mode)

    status = (
        f"step: {step + 1}/{TOTAL_STEPS}\\n"
        f"zigzag: coluna, topo-esquerda\\n"
        f"row={row} col={col}\\n"
        f"pino_cm={0.0 if not np.isfinite(val) else val:.2f}\\n"
        f"teto_m={0.0 if not np.isfinite(Z_TOTAL_M[row, col]) else Z_TOTAL_M[row, col]:.2f}\\n"
        f"escala_visual={cell_mode}\\n"
        f"mesa_real={'ON' if mesa_on else 'OFF'}\\n"
        f"clock={'REAL lento' if mesa_on else 'VIRTUAL acelerado'}\\n"
        f"projector={projector_mode}\\n"
        f"{hw_msg}"
    )

    if cell_mode == "1x1 cm":
        width = "32cm"
        height = "16cm"
    else:
        width = "64cm"
        height = "32cm"

    style = {
        "width": width,
        "height": height,
        "margin": "24px auto 0 auto",
        "display": "block",
    }

    return fig, status, style


if __name__ == "__main__":
    print("========================================")
    print("V128.7.18 — NORTH LEFT FINAL")
    print("========================================")
    print("CSV:", CSV_PATH)
    print("PNG:", PNG_PATH)
    print("NORTH:", NORTH_PATH)
    print("Total cells:", TOTAL_STEPS)
    print("Zigzag starts:", ZIGZAG_PATH[0])
    print("Virtual interval ms:", VIRTUAL_INTERVAL_MS)
    print("Real interval ms:", REAL_INTERVAL_MS)
    print("Pino cm min/max:", float(np.nanmin(Z_PINO_CM)), float(np.nanmax(Z_PINO_CM)))
    print("Teto m min/max:", float(np.nanmin(Z_TOTAL_M)), float(np.nanmax(Z_TOTAL_M)))
    print("Contours terreno:", len(TERRAIN_CONTOURS))
    print("Contours teto:", len(TOTAL_CONTOURS))
    print("========================================")
    app.run(debug=True)
