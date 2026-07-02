from pathlib import Path
import base64
import numpy as np
import pandas as pd
from PIL import Image

import dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go

# =========================================
# PATHS
# =========================================

THIS_FILE = Path(__file__).resolve()
CORE_ROOT = THIS_FILE.parents[2]

CSV_PATH = CORE_ROOT / "offline/products/scientific/grid_metrics_utm.csv"
NORTH_PATH = CORE_ROOT / "online/assets/north_arrow_scale.png"

GRID_ROWS = 8
GRID_COLS = 16

# =========================================
# HELPERS
# =========================================

def image_to_uri(path):
    data = path.read_bytes()
    return "data:image/png;base64," + base64.b64encode(data).decode()

def build_grid(df):
    z = np.full((GRID_ROWS, GRID_COLS), np.nan)
    for _, r in df.iterrows():
        row = int(r["row"])
        col = int(r["col"])
        val = float(r["z_total_m"])
        if val > 0:
            z[row, col] = val
    return np.flipud(np.roll(z, -1, axis=0))

def zigzag():
    path = []
    for c in range(GRID_COLS):
        rows = range(GRID_ROWS) if c % 2 == 0 else range(GRID_ROWS-1, -1, -1)
        for r in rows:
            path.append((r, c))
    return path

# =========================================
# LOAD
# =========================================

df = pd.read_csv(CSV_PATH)
Z = build_grid(df)
PATH = zigzag()
TOTAL = len(PATH)

NORTH_URI = image_to_uri(NORTH_PATH)

# =========================================
# FIGURE
# =========================================

def make_fig(step):

    fig = go.Figure()

    z_disp = np.zeros_like(Z)

    for i in range(step+1):
        r,c = PATH[i]
        if np.isfinite(Z[r,c]):
            z_disp[r,c] = Z[r,c]

    fig.add_trace(go.Heatmap(
        z=z_disp,
        colorscale="Viridis",
        showscale=False
    ))

    # célula ativa
    r,c = PATH[step]
    fig.update_layout(shapes=[dict(
        type="rect",
        x0=c-0.5, x1=c+0.5,
        y0=r-0.5, y1=r+0.5,
        line=dict(color="white", width=3)
    )])

    # =========================================
    # NORTH SCALE (AJUSTE FINAL)
    # =========================================

    fig.add_layout_image(dict(
        source=NORTH_URI,
        xref="paper",
        yref="paper",
        x=-0.015,          # ← AJUSTE FINAL
        y=0.02,
        sizex=0.28,
        sizey=0.28,
        xanchor="left",
        yanchor="bottom",
        layer="above"
    ))

    fig.update_layout(
        margin=dict(l=90, r=40, t=40, b=220),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False, scaleanchor="x"),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    return fig

# =========================================
# DASH
# =========================================

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Store(id="step", data=0),

    html.Button("◀ Backward", id="back"),
    html.Button("⏸ Pause", id="pause"),
    html.Button("▶ Forward", id="fwd"),

    dcc.Interval(id="clock", interval=300, disabled=True),

    dcc.Graph(id="g", style={"width":"32cm","height":"16cm"})
])

@app.callback(
    Output("step","data"),
    Output("clock","disabled"),
    Input("fwd","n_clicks"),
    Input("back","n_clicks"),
    Input("pause","n_clicks"),
    Input("clock","n_intervals"),
    State("step","data")
)
def loop(f,b,p,t,step):
    trig = ctx.triggered_id

    if trig=="fwd":
        return min(step+1,TOTAL-1), False

    if trig=="back":
        return max(step-1,0), False

    if trig=="pause":
        return step, True

    if trig=="clock":
        return min(step+1,TOTAL-1), False

    return step, True

@app.callback(
    Output("g","figure"),
    Input("step","data")
)
def draw(step):
    return make_fig(step)

# =========================================
# RUN
# =========================================

if __name__ == "__main__":
    print("========================================")
    print("V128.7.8 — NORTH FORA DO GRID")
    print("========================================")
    app.run(debug=True)
