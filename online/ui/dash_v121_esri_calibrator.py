from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go

# =========================================
# PATHS
# =========================================

BASE = Path(__file__).resolve().parents[2]
CSV = BASE / "offline/products/scientific/grid_metrics_utm.csv"
ESRI = BASE / "offline/products/snapshots/ipt_fase2_semantic/esri_overlay_grid.png"

ROWS = 8
COLS = 16

# =========================================
# LOAD GRID
# =========================================

df = pd.read_csv(CSV)

z = np.full((ROWS, COLS), np.nan)

for _, r in df.iterrows():
    row = int(r["row"])
    col = int(r["col"])
    if r["z_total_m"] > 0:
        z[row, col] = r["z_total_m"] * 100

z = np.roll(z, -1, axis=0)
z = np.flipud(z)

# =========================================
# LOAD ESRI IMAGE
# =========================================

img = Image.open(ESRI).convert("L")
esri = np.array(img).astype(float)
esri = (esri - esri.min()) / (np.ptp(esri) + 1e-6)

# =========================================
# FIGURE BUILDER
# =========================================

def make_fig(offset_x, offset_y, scale_x, scale_y, opacity):
    fig = go.Figure()

    # ESRI overlay
    x_left = -0.5 + offset_x
    y_top = -0.5 + offset_y

    fig.add_trace(go.Heatmap(
        z=esri,
        x0=x_left,
        dx=(COLS * scale_x) / esri.shape[1],
        y0=y_top,
        dy=(ROWS * scale_y) / esri.shape[0],
        colorscale="Greys",
        showscale=False,
        opacity=opacity,
        hoverinfo="skip"
    ))

    # PINOS
    fig.add_trace(go.Heatmap(
        z=z,
        colorscale="Viridis",
        showscale=True,
        opacity=0.9,
        hovertemplate="pino=%{z:.1f} cm<extra></extra>"
    ))

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False, range=[-0.5, COLS - 0.5]),
        yaxis=dict(visible=False, range=[ROWS - 0.5, -0.5]),
    )

    return fig

# =========================================
# DASH
# =========================================

app = dash.Dash(__name__)

app.layout = html.Div([

    html.Div([
        "Offset X",
        dcc.Slider(-2, 2, 0.01, value=0, id="ox"),

        "Offset Y",
        dcc.Slider(-2, 2, 0.01, value=0, id="oy"),

        "Scale X",
        dcc.Slider(0.5, 2, 0.01, value=1, id="sx"),

        "Scale Y",
        dcc.Slider(0.5, 2, 0.01, value=1, id="sy"),

        "Opacity",
        dcc.Slider(0.1, 1, 0.05, value=0.5, id="op"),

    ], style={"width": "300px"}),

    dcc.Graph(id="g")

])

@app.callback(
    Output("g", "figure"),
    Input("ox", "value"),
    Input("oy", "value"),
    Input("sx", "value"),
    Input("sy", "value"),
    Input("op", "value"),
)
def update(ox, oy, sx, sy, op):
    return make_fig(ox, oy, sx, sy, op)

if __name__ == "__main__":
    app.run(debug=True)
