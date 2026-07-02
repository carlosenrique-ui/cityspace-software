# ==========================================================
# IPT-CitySpace – DASH V100.1 (ALTURA PROPORCIONAL + GRID)
# ==========================================================

import json
import numpy as np
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go

ROWS = 8
COLS = 16

PLAN_PATH = "ipt_core_clean/products/final/actuator_plan_zigzag.json"

# =========================================
# LOAD PLAN
# =========================================
with open(PLAN_PATH) as f:
    data = json.load(f)

events = data.get("events", data)

sequence = []
pos = (0, 0)

for e in events:
    if e.get("type") == "move":
        pos = (e["row"], e["col"])
    elif e.get("type") == "set_height_cm":
        h = e.get("value_cm", 0.0)
        sequence.append((pos, h))

print(">>> SEQ LEN:", len(sequence))

# =========================================
# TEMPO PROPORCIONAL À ALTURA
# =========================================
BASE_STEPS = 5
SCALE = 2

steps_per_cell = [BASE_STEPS + int(h * SCALE) for (_, h) in sequence]

cum_steps = np.cumsum([0] + steps_per_cell)
TOTAL_STEPS = int(cum_steps[-1])

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

    dcc.Store(id="t", data=0),
    dcc.Store(id="run", data=False),
    dcc.Store(id="dir", data=1)
])

# =========================================
# CONTROLES
# =========================================
@app.callback(
    Output("run", "data"),
    Input("play", "n_clicks"),
    Input("pause", "n_clicks"),
    prevent_initial_call=True
)
def run(p, s):
    ctx = dash.callback_context
    if "play" in ctx.triggered[0]["prop_id"]:
        return True
    return False


@app.callback(
    Output("dir", "data"),
    Input("fwd", "n_clicks"),
    Input("back", "n_clicks"),
    prevent_initial_call=True
)
def direction(f, b):
    ctx = dash.callback_context
    if "back" in ctx.triggered[0]["prop_id"]:
        return -1
    return 1


# =========================================
# LOOP PRINCIPAL
# =========================================
@app.callback(
    Output("g", "figure"),
    Output("t", "data"),
    Input("interval", "n_intervals"),
    State("t", "data"),
    State("run", "data"),
    State("dir", "data")
)
def update(n, t, run, direction):

    if run:
        t += direction

    t = max(0, min(t, TOTAL_STEPS - 1))

    estado = np.zeros((ROWS, COLS))

    idx = np.searchsorted(cum_steps, t, side="right") - 1

    # células completas
    for i in range(idx):
        (r, c), h = sequence[i]
        estado[r, c] = h

    # célula atual
    if idx < len(sequence):
        (r, c), h = sequence[idx]

        local_t = t - cum_steps[idx]
        steps = steps_per_cell[idx]

        if steps > 0:
            frac = local_t / steps
        else:
            frac = 1

        estado[r, c] = h * frac

    fig = go.Figure()

    fig.add_trace(go.Heatmap(
        z=estado,
        colorscale="Viridis",
        zmin=0,
        zmax=10,
        xgap=2,
        ygap=2
    ))

    fig.update_yaxes(autorange="reversed")
    fig.update_yaxes(scaleanchor="x", scaleratio=1)

    fig.update_layout(
        margin=dict(l=0, r=0, t=20, b=0),
        plot_bgcolor="black",
        paper_bgcolor="black"
    )

    return fig, t


# =========================================
# RUN
# =========================================
if __name__ == "__main__":
    app.run(debug=False)
