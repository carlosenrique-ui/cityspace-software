import json, os
import numpy as np
import pandas as pd
import dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go

BASE = "/mnt/c/workspace/ipt-cityspace-engine"

GRID_PATH = f"{BASE}/products/final/grid_height.csv"
PLAN_PATH = f"{BASE}/products/final/actuator_plan.json"
MASK_PATH = "assets/ipt_mask_rotated_simple.png"

ROWS, COLS = 8, 16

print(">>> START V95.4", flush=True)

df = pd.read_csv(GRID_PATH)

grid = df.pivot(index="row", columns="col", values="z_cm").values[:ROWS, :COLS]

print(">>> GRID OK", grid.shape, flush=True)

raw = json.load(open(PLAN_PATH))

if isinstance(raw, dict) and "events" in raw:
    E = raw["events"]
else:
    E = raw

p = []
v = []
pos = None

for e in E:
    if e.get("type") == "move":
        pos = (e["row"], e["col"])
    elif e.get("type") == "set_height_cm":
        p.append(pos)
        v.append(e["value_cm"])

print(">>> PLAN LEN:", len(p), flush=True)

if len(p) != 128:
    raise Exception("PLAN INVALIDO")

app = dash.Dash(__name__, assets_folder="assets")

app.layout = html.Div(
    [
        dcc.Graph(id="g", style={"height": "85vh"}),
        html.Button("Play", id="play"),
        dcc.Interval(id="i", interval=80),
        dcc.Store(id="step", data=0),
        dcc.Store(id="run", data=False),
    ]
)


@app.callback(
    Output("run", "data"), Input("play", "n_clicks"), prevent_initial_call=True
)
def run(n):
    return True


@app.callback(
    Output("step", "data"),
    Input("i", "n_intervals"),
    State("run", "data"),
    State("step", "data"),
)
def tick(n, run, s):
    if not run:
        return s
    return min(127, s + 1)


@app.callback(Output("g", "figure"), Input("step", "data"))
def render(step):

    Z = np.zeros((ROWS, COLS))

    for i in range(step + 1):
        r, c = p[i]
        Z[r][c] = v[i]

    r, c = p[step]

    fig = go.Figure()

    fig.update_layout(
        images=[
            dict(
                source=MASK_PATH,
                xref="x",
                yref="y",
                x=-0.5,
                y=ROWS - 0.5,
                sizex=COLS,
                sizey=ROWS,
                sizing="stretch",
                opacity=0.3,
                layer="below",
            )
        ]
    )

    fig.add_trace(go.Heatmap(z=Z, colorscale="Jet", xgap=1, ygap=1))

    fig.add_shape(
        type="rect",
        x0=c - 0.5,
        x1=c + 0.5,
        y0=r - 0.5,
        y1=r + 0.5,
        line=dict(color="white", width=3),
    )

    fig.update_yaxes(range=[ROWS - 0.5, -0.5], scaleanchor="x")
    fig.update_xaxes(range=[-0.5, COLS - 0.5])

    return fig


if __name__ == "__main__":
    app.run(port=8050, debug=False)  # (cole o código completo aqui)
