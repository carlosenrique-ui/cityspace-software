# ==========================================================
# IPT-CitySpace – DASH V87 (FIX FINAL REAL + LOCKED)
# ==========================================================

import json
import pandas as pd
import numpy as np
from PIL import Image
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go

# =========================================
# PATHS
# =========================================
CSV_PATH = "offline/products/scientific/grid_metrics_utm.csv"
PLAN_PATH = "ipt_core_clean/products/final/actuator_plan_zigzag.json"
IPT_LOGO = "assets/ipt_mask.png"

# =========================================
# LOAD GRID REAL
# =========================================
df = pd.read_csv(CSV_PATH)
VALUE_COL = "z_total_m"

grid_base = df.pivot(index="row", columns="col", values=VALUE_COL)
grid_base = grid_base.sort_index().sort_index(axis=1)

ROWS, COLS = grid_base.shape

# =========================================
# LOAD ACTUATOR PLAN REAL
# =========================================
with open(PLAN_PATH) as f:
    plan = json.load(f)

events = plan.get("events", plan)

sequence = []
pos = (0, 0)

for e in events:
    if e.get("type") == "move":
        pos = (e["row"], e["col"])
    elif e.get("type") == "set_height_cm":
        h = e.get("value_cm", 0.0)
        sequence.append((pos, h))

print("SEQ LEN:", len(sequence))

# =========================================
# LOAD IPT LOGO (GRID SPACE)
# =========================================
img = Image.open(IPT_LOGO).convert("L")
img = img.resize((COLS, ROWS))
logo = np.array(img) / 255.0

# =========================================
# DASH
# =========================================
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="g", config={"displayModeBar": False}, style={"height": "85vh"}),

    html.Div([
        html.Button("<<", id="back"),
        html.Button("Play", id="play"),
        html.Button("Pause", id="pause"),
        html.Button(">>", id="fwd"),
    ], style={"textAlign": "center"}),

    dcc.Interval(id="interval", interval=80),

    dcc.Store(id="idx", data=0),
    dcc.Store(id="run", data=False),
    dcc.Store(id="dir", data=1)
])

# =========================================
# CONTROLES
# =========================================
@app.callback(Output("run","data"),
              Input("play","n_clicks"),
              Input("pause","n_clicks"),
              prevent_initial_call=True)
def run(p,s):
    ctx = dash.callback_context
    return "play" in ctx.triggered[0]["prop_id"]

@app.callback(Output("dir","data"),
              Input("fwd","n_clicks"),
              Input("back","n_clicks"),
              prevent_initial_call=True)
def direction(f,b):
    ctx = dash.callback_context
    return -1 if "back" in ctx.triggered[0]["prop_id"] else 1

# =========================================
# LOOP
# =========================================
@app.callback(Output("g","figure"),
              Output("idx","data"),
              Input("interval","n_intervals"),
              State("idx","data"),
              State("run","data"),
              State("dir","data"))
def update(n, idx, run, direction):

    if run:
        idx += direction

    idx = max(0, min(idx, len(sequence)-1))

    # 🔥 GRID COMEÇA VAZIO (CORREÇÃO)
    estado = np.zeros_like(grid_base.values)

    # 🔥 PREENCHIMENTO REAL (SEM INVENTAR)
    for i in range(idx+1):
        (r,c),_ = sequence[i]
        estado[r,c] = grid_base.values[r,c]

    # 🔥 IPT LOCKED (SÓ ONDE TEM DADO)
    mask = (estado > 0).astype(float)
    overlay = logo * mask

    fig = go.Figure()

    # BASE
    fig.add_trace(go.Heatmap(
        z=estado,
        colorscale="Viridis"
    ))

    # IPT
    fig.add_trace(go.Heatmap(
        z=overlay,
        colorscale=[
            [0, "rgba(0,0,0,0)"],
            [1, "rgba(255,255,255,0.25)"]
        ],
        showscale=False
    ))

    # CURSOR
    (r,c),_ = sequence[idx]
    fig.add_trace(go.Scatter(
        x=[c-0.5,c+0.5,c+0.5,c-0.5,c-0.5],
        y=[r-0.5,r-0.5,r+0.5,r+0.5,r-0.5],
        mode="lines",
        line=dict(color="white", width=3),
        showlegend=False
    ))

    fig.update_yaxes(autorange="reversed", scaleanchor="x", scaleratio=1)

    fig.update_layout(
        margin=dict(l=0,r=0,t=20,b=0),
        plot_bgcolor="black",
        paper_bgcolor="black"
    )

    return fig, idx

# =========================================
# RUN
# =========================================
if __name__ == "__main__":
    app.run(debug=False)
