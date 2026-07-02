import json
import numpy as np
import pandas as pd
import dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go
import os

print("\n==============================")
print(">>> V95.2 REAL BASE")
print("==============================\n")

# =========================================
# LOAD GRID REAL
# =========================================
csv_path = "products/final/grid_height.csv"
print(">>> CSV PATH:", os.path.abspath(csv_path))

df = pd.read_csv(csv_path)

print(">>> COLS:", df.columns)

grid = df.pivot(index="row", columns="col", values="z_cm").values[:8, :16]
grid = np.flipud(grid)

print(">>> GRID MIN/MAX:", np.min(grid), np.max(grid))

# 🔥 IMPORTANTE: fora do urbanismo → 0
grid = np.where(grid < 0.001, 0, grid)

nx, ny = 16, 8

# =========================================
# LOAD PLAN REAL
# =========================================
plan_path = "products/final/actuator_plan.json"
print(">>> PLAN PATH:", os.path.abspath(plan_path))

raw = json.load(open(plan_path))
E = raw.get("events", raw)

p = []
v = []
pos = (0, 0)

for e in E:
    if e["type"] == "move":
        pos = (e["row"], e["col"])
    elif e["type"] == "set_height_cm":
        p.append(pos)
        v.append(e.get("value_cm", 0))

print(">>> PLAN LEN:", len(p))
print(">>> FIRST 10:", p[:10])

# =========================================
# TIMELINE
# =========================================
tl = [0]
for i in range(1, len(p)):
    d = abs(p[i][0] - p[i - 1][0]) + abs(p[i][1] - p[i - 1][1])
    tl.append(tl[-1] + 0.2 * d + 0.12 * abs(v[i]))

TMAX = tl[-1] if tl else 0

# =========================================
# DASH
# =========================================
app = dash.Dash(__name__, assets_folder="assets")

app.layout = html.Div(
    [
        dcc.Graph(
            id="graph", config={"displayModeBar": False}, style={"height": "85vh"}
        ),
        html.Div(
            [
                html.Button("<<", id="back"),
                html.Button("Play", id="play"),
                html.Button("Pause", id="pause"),
                html.Button(">>", id="fwd"),
            ],
            style={"textAlign": "center"},
        ),
        dcc.Interval(id="interval", interval=80),
        dcc.Store(id="time", data=0),
        dcc.Store(id="running", data=False),
        dcc.Store(id="direction", data=1),
    ]
)


# =========================================
# CONTROLES
# =========================================
@app.callback(
    Output("running", "data"),
    Input("play", "n_clicks"),
    Input("pause", "n_clicks"),
    State("running", "data"),
    prevent_initial_call=True,
)
def r(a, b, c):
    return (
        True
        if ctx.triggered_id == "play"
        else False if ctx.triggered_id == "pause" else c
    )


@app.callback(
    Output("direction", "data"),
    Input("fwd", "n_clicks"),
    Input("back", "n_clicks"),
    State("direction", "data"),
    prevent_initial_call=True,
)
def d1(a, b, c):
    return -1 if ctx.triggered_id == "back" else 1 if ctx.triggered_id == "fwd" else c


@app.callback(
    Output("time", "data"),
    Input("interval", "n_intervals"),
    State("running", "data"),
    State("direction", "data"),
    State("time", "data"),
)
def t(n, r, d, t):
    return t if not r else max(0, min(TMAX, t + d * 0.05))


# =========================================
# STEP
# =========================================
def gs(t):
    for i, x in enumerate(tl):
        if x >= t:
            return i
    return len(tl) - 1


# =========================================
# RENDER
# =========================================
@app.callback(Output("graph", "figure"), Input("time", "data"))
def rd(t):

    s = gs(t)

    Z = np.zeros((ny, nx))

    for i, (r, c) in enumerate(p):
        if i <= s:
            Z[r][c] = grid[r][c]

    print(f">>> STEP {s} / {len(p)}")

    fig = go.Figure()

    # IPT WATERMARK
    fig.update_layout(
        images=[
            dict(
                source="assets/ipt_mask_rotated_simple.png",
                xref="x",
                yref="y",
                x=-0.5,
                y=ny - 0.5,
                sizex=nx,
                sizey=ny,
                sizing="stretch",
                opacity=0.25,
                layer="below",
            )
        ]
    )

    fig.add_trace(
        go.Heatmap(z=Z, colorscale="Jet", zmin=0, zmax=10, xgap=1, ygap=1, opacity=0.6)
    )

    # ATUADOR
    if s < len(p):
        r, c = p[s]
        fig.add_shape(
            type="rect",
            x0=c - 0.5,
            y0=r - 0.5,
            x1=c + 0.5,
            y1=r + 0.5,
            line=dict(color="white", width=3),
        )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(range=[-0.5, nx - 0.5], visible=False),
        yaxis=dict(range=[ny - 0.5, -0.5], visible=False, scaleanchor="x"),
        plot_bgcolor="white",
    )

    return fig


if __name__ == "__main__":
    print(">>> RUN V95.2")
    app.run(host="0.0.0.0", port=8050, debug=False)
