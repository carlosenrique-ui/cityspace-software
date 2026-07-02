from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go


THIS_FILE = Path(__file__).resolve()
CORE_ROOT = THIS_FILE.parents[2]
PROJECT_ROOT = CORE_ROOT.parent

CSV_PATH = CORE_ROOT / "offline/products/scientific/grid_metrics_utm.csv"

PNG_CANDIDATES = [
    CORE_ROOT / "offline/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_final.png",
    PROJECT_ROOT / "offline/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_final.png",
    PROJECT_ROOT / "backup_git_20260317_191244/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_v3.png",
]

GRID_ROWS = 8
GRID_COLS = 16

DEFAULT_OFFSET_X = 0.50
DEFAULT_OFFSET_Y = -0.50
DEFAULT_SCALE_X = 0.92
DEFAULT_SCALE_Y = 0.90
DEFAULT_OPACITY = 0.30


def first_existing(paths):
    for p in paths:
        if p.exists():
            return p
    raise FileNotFoundError("Nenhum PNG encontrado.")


def build_grid(df):
    grid = np.zeros((GRID_ROWS, GRID_COLS), dtype=float)
    for _, r in df.iterrows():
        grid[int(r["row"]), int(r["col"])] = float(r["z_total_m"])
    return grid


def fix_grid_like_v42(grid):
    g = grid.copy()
    g[6:, 0:3] = 0
    g = np.roll(g, -1, axis=0)
    g = np.flipud(g)
    return g


def load_png(path):
    img = Image.open(path).convert("L")
    arr = np.array(img).astype(float)
    arr = (arr - arr.min()) / (np.ptp(arr) + 1e-6)
    return arr


PNG_PATH = first_existing(PNG_CANDIDATES)

df = pd.read_csv(CSV_PATH)
grid = fix_grid_like_v42(build_grid(df))
png = load_png(PNG_PATH)

rows, cols = grid.shape


def make_fig(offset_x, offset_y, scale_x, scale_y, opacity):
    fig = go.Figure()

    # Watermark usando extent equivalente ao Matplotlib V42
    x_left = -0.5 + offset_x
    x_right = cols - 0.5 + offset_x
    y_top = -0.5 + offset_y
    y_bottom = rows - 0.5 + offset_y

    # Aplicar escala em torno do centro do grid
    cx = (x_left + x_right) / 2
    cy = (y_top + y_bottom) / 2
    width = (x_right - x_left) * scale_x
    height = (y_bottom - y_top) * scale_y

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
            opacity=opacity,
            hoverinfo="skip",
        )
    )

    fig.add_trace(
        go.Heatmap(
            z=grid,
            colorscale="Viridis",
            showscale=True,
            colorbar=dict(title="Pino / Teto<br>(m)"),
            opacity=0.85,
            xgap=0,
            ygap=0,
            hovertemplate="col=%{x}<br>row=%{y}<br>z_total=%{z:.2f} m<extra></extra>",
        )
    )

    for c in range(cols + 1):
        fig.add_trace(
            go.Scatter(
                x=[c - 0.5, c - 0.5],
                y=[-0.5, rows - 0.5],
                mode="lines",
                line=dict(color="rgba(255,255,255,0.35)", width=1),
                showlegend=False,
                hoverinfo="skip",
            )
        )

    for r in range(rows + 1):
        fig.add_trace(
            go.Scatter(
                x=[-0.5, cols - 0.5],
                y=[r - 0.5, r - 0.5],
                mode="lines",
                line=dict(color="rgba(255,255,255,0.35)", width=1),
                showlegend=False,
                hoverinfo="skip",
            )
        )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False, range=[-0.5, cols - 0.5]),
        yaxis=dict(visible=False, range=[rows - 0.5, -0.5], scaleanchor="x", scaleratio=1),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    return fig


app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div("V114 Watermark Calibrator", style={"fontWeight": "bold", "marginBottom": "6px"}),

                html.Label("offset_x"),
                dcc.Slider(-2, 2, 0.05, value=DEFAULT_OFFSET_X, id="offset-x",
                           marks={-2: "-2", 0: "0", 2: "2"}),

                html.Label("offset_y"),
                dcc.Slider(-2, 2, 0.05, value=DEFAULT_OFFSET_Y, id="offset-y",
                           marks={-2: "-2", 0: "0", 2: "2"}),

                html.Label("scale_x"),
                dcc.Slider(0.60, 1.40, 0.01, value=DEFAULT_SCALE_X, id="scale-x",
                           marks={0.6: "0.6", 1.0: "1.0", 1.4: "1.4"}),

                html.Label("scale_y"),
                dcc.Slider(0.60, 1.40, 0.01, value=DEFAULT_SCALE_Y, id="scale-y",
                           marks={0.6: "0.6", 1.0: "1.0", 1.4: "1.4"}),

                html.Label("opacity"),
                dcc.Slider(0.05, 0.80, 0.05, value=DEFAULT_OPACITY, id="opacity",
                           marks={0.05: "0.05", 0.3: "0.3", 0.8: "0.8"}),

                html.Pre(id="params", style={"fontSize": "12px", "whiteSpace": "pre-wrap"}),
            ],
            style={
                "position": "fixed",
                "left": "8px",
                "top": "8px",
                "zIndex": 10,
                "width": "330px",
                "background": "rgba(255,255,255,0.88)",
                "padding": "10px",
                "border": "1px solid #ccc",
                "borderRadius": "8px",
                "fontFamily": "Arial",
                "fontSize": "13px",
            },
        ),
        dcc.Graph(
            id="graph",
            config={"displayModeBar": False, "scrollZoom": False, "responsive": True},
            style={"width": "100vw", "height": "100vh"},
        ),
    ],
    style={"margin": 0, "padding": 0, "overflow": "hidden", "background": "white"},
)


@app.callback(
    Output("graph", "figure"),
    Output("params", "children"),
    Input("offset-x", "value"),
    Input("offset-y", "value"),
    Input("scale-x", "value"),
    Input("scale-y", "value"),
    Input("opacity", "value"),
)
def update(offset_x, offset_y, scale_x, scale_y, opacity):
    fig = make_fig(offset_x, offset_y, scale_x, scale_y, opacity)
    txt = (
        f"OFFSET_X = {offset_x:.2f}\n"
        f"OFFSET_Y = {offset_y:.2f}\n"
        f"PNG_SCALE_X = {scale_x:.2f}\n"
        f"PNG_SCALE_Y = {scale_y:.2f}\n"
        f"PNG_OPACITY = {opacity:.2f}"
    )
    return fig, txt


if __name__ == "__main__":
    print("========================================")
    print("V114 — WATERMARK CALIBRATOR")
    print("========================================")
    print("CSV:", CSV_PATH)
    print("PNG:", PNG_PATH)
    print("Grid min/max:", float(np.nanmin(grid)), float(np.nanmax(grid)))
    print("========================================")
    app.run(debug=True)
