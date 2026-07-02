import json
import numpy as np
import pandas as pd
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go

# ===============================
# LOAD GRID REAL
# ===============================
df = pd.read_csv("/mnt/c/workspace/ipt-cityspace-engine/products/final/grid_height.csv")

grid = df.pivot(index="row", columns="col", values="z_total_cm").values

# ===============================
# LOAD ACTUATOR PLAN (REAL)
# ===============================
with open(
    "/mnt/c/workspace/ipt-cityspace-engine/products/final/actuator_plan.json"
) as f:
    raw = json.load(f)

EVENTS = raw.get("events", raw)

# ===============================
# 🔥 CAMINHO REAL (SEM INVENTAR)
# ===============================
path = []
values = []

pos = None

for e in EVENTS:
    if e["type"] == "move":
        pos = (e["row"], e["col"])
    elif e["type"] == "set_height_cm":
        if pos is not None:
            path.append(pos)
            values.append(e["value_cm"])

TOTAL = len(values)


# ===============================
# TEMPO (INALTERADO)
# ===============================
def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


timeline = [0]

for i in range(1, TOTAL):
    d = dist(path[i - 1], path[i])
    h = abs(values[i] - values[i - 1])
    dt = 0.2 * d + 0.08 * h
    timeline.append(timeline[-1] + dt)

TMAX = timeline[-1] if timeline else 0

# ===============================
# DASH
# ===============================
app = dash.Dash(__name__, assets_folder="assets")

app.layout = html.Div(
    [
        html.Div(
            id="status",
            style={
                "background": "black",
                "color": "white",
                "padding": "6px",
                "textAlign": "center",
            },
        ),
        html.Div(
            [dcc.Graph(id="g", config={"displayModeBar": False})],
            style={"display": "flex", "justifyContent": "center"},
        ),
        html.Div(
            [
                html.Button("<<", id="back"),
                html.Button("Play", id="play"),
                html.Button("Pause", id="pause"),
                html.Button(">>", id="fwd"),
                html.Button("1x / 2x", id="zoom_btn"),
            ],
            style={"textAlign": "center", "marginTop": "10px"},
        ),
        dcc.Interval(id="t", interval=50, n_intervals=0),
        dcc.Store(id="time", data=0),
        dcc.Store(id="run", data=False),
        dcc.Store(id="dir", data=1),
        dcc.Store(id="zoom_state", data=1),
    ]
)


@app.callback(
    Output("run", "data"),
    Input("play", "n_clicks"),
    Input("pause", "n_clicks"),
    prevent_initial_call=True,
)
def run(p, pa):
    return dash.callback_context.triggered_id == "play"


@app.callback(
    Output("dir", "data"),
    Input("fwd", "n_clicks"),
    Input("back", "n_clicks"),
    prevent_initial_call=True,
)
def direction(f, b):
    return -1 if dash.callback_context.triggered_id == "back" else 1


@app.callback(
    Output("zoom_state", "data"),
    Input("zoom_btn", "n_clicks"),
    State("zoom_state", "data"),
    prevent_initial_call=True,
)
def zoom_toggle(n, z):
    return 2 if z == 1 else 1


@app.callback(
    Output("time", "data"),
    Input("t", "n_intervals"),
    Input("run", "data"),
    Input("dir", "data"),
    Input("time", "data"),
    prevent_initial_call=True,
)
def tick(n, run, dir, time):
    if not run:
        return time
    t = time + dir * 0.05
    return max(0, min(TMAX, t))


def get_step(time):
    for i, t in enumerate(timeline):
        if t >= time:
            return i
    return len(timeline) - 1 if timeline else 0


@app.callback(
    Output("g", "figure"),
    Output("status", "children"),
    Input("time", "data"),
    Input("zoom_state", "data"),
)
def render(time, zoom):

    step = get_step(time)

    z = np.zeros_like(grid).astype(float)

    for i in range(min(step + 1, TOTAL)):
        r, c = path[i]
        z[r][c] = values[i]

    fig = go.Figure()

    fig.add_trace(
        go.Heatmap(z=z, colorscale="Jet", zmin=0, zmax=10, xgap=0, ygap=0, opacity=0.65)
    )

    if step < TOTAL:
        r, c = path[step]

        fig.add_trace(
            go.Scatter(
                x=[c],
                y=[r],
                mode="markers",
                marker=dict(color="rgba(255,255,255,0.3)", size=26),
                showlegend=False,
            )
        )

        fig.add_trace(
            go.Scatter(
                x=[c],
                y=[r],
                mode="markers",
                marker=dict(color="white", size=10),
                showlegend=False,
            )
        )

    ny, nx = z.shape

    fig.update_xaxes(
        range=[-0.5, nx - 0.5],
        constrain="domain",
        scaleanchor="y",
        scaleratio=1,
        showgrid=False,
        zeroline=False,
        visible=False,
    )

    fig.update_yaxes(
        range=[ny - 0.5, -0.5],
        constrain="domain",
        showgrid=False,
        zeroline=False,
        visible=False,
    )

    fig.update_layout(
        width=900 if zoom == 1 else 1800,
        height=450 if zoom == 1 else 900,
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor="black",
        paper_bgcolor="black",
        images=[
            dict(
                source="/assets/ipt_mask_rotated_simple.png",
                xref="paper",
                yref="paper",
                x=0,
                y=1,
                sizex=1,
                sizey=1,
                sizing="stretch",
                opacity=0.32,
                layer="below",
            )
        ],
    )

    val = values[step] if step < TOTAL else 0
    status = f"STEP {step}/{TOTAL} | {val:.1f} cm"

    return fig, status


app.run(debug=True, port=8050)
