# ==========================================================
# IPT-CitySpace – DASH V94 (PLAN REAL + VALUE_CM FIX)
# ==========================================================

import json
import numpy as np
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go

# =========================================
# CONFIG
# =========================================
ROWS = 8
COLS = 16

PLAN_PATH = "ipt_core_clean/products/final/actuator_plan.json"

# =========================================
# LOAD PLAN
# =========================================
with open(PLAN_PATH) as f:
    data = json.load(f)

events = data.get("events", data)

# =========================================
# BUILD SEQUENCE (MOVE + HEIGHT)
# =========================================
sequence = []

pos = (0, 0)

for e in events:
    if e.get("type") == "move":
        pos = (e.get("row"), e.get("col"))
    elif e.get("type") == "set_height_cm":
        h = (
            e.get("value_cm")
            or e.get("height_cm")
            or e.get("cm")
            or e.get("value")
            or 0.0
        )
        sequence.append((pos, h))

print(">>> SEQ LEN:", len(sequence))

# =========================================
# STATE (PERSISTENTE)
# =========================================
estado = np.zeros((ROWS, COLS))

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

    dcc.Interval(id="interval", interval=200, n_intervals=0),

    dcc.Store(id="idx", data=0),
    dcc.Store(id="running", data=False),
    dcc.Store(id="dir", data=1)
])

# =========================================
# CONTROLES
# =========================================
@app.callback(Output("running", "data"),
              Input("play", "n_clicks"),
              Input("pause", "n_clicks"),
              prevent_initial_call=True)
def control_run(p, s):
    ctx = dash.callback_context
    if not ctx.triggered:
        return False
    if ctx.triggered[0]["prop_id"].startswith("play"):
        return True
    return False


@app.callback(Output("dir", "data"),
              Input("fwd", "n_clicks"),
              Input("back", "n_clicks"),
              prevent_initial_call=True)
def control_dir(f, b):
    ctx = dash.callback_context
    if not ctx.triggered:
        return 1
    if ctx.triggered[0]["prop_id"].startswith("back"):
        return -1
    return 1


# =========================================
# LOOP PRINCIPAL
# =========================================
@app.callback(
    Output("g", "figure"),
    Output("idx", "data"),
    Input("interval", "n_intervals"),
    State("idx", "data"),
    State("running", "data"),
    State("dir", "data")
)
def update(n, idx, running, direction):

    global estado

    if running:
        idx += direction

    idx = max(0, min(idx, len(sequence) - 1))

    # aplica estado acumulado até idx
    estado = np.zeros((ROWS, COLS))
    for i in range(idx + 1):
        (r, c), h = sequence[i]
        estado[r, c] = h

    fig = go.Figure(data=go.Heatmap(
        z=estado,
        colorscale="Viridis",
        zmin=0,
        zmax=max(1, np.max(estado))
    ))

    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0)
    )

    return fig, idx


# =========================================
# RUN
# =========================================
if __name__ == "__main__":
    app.run(debug=False)
