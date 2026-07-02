import json, numpy as np, pandas as pd, dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go

df = pd.read_csv("/mnt/c/workspace/ipt-cityspace-engine/products/final/grid_height.csv")
grid = df.pivot(index="row", columns="col", values="z_cm").values

# 🔥 FORÇA GRID 16x8
grid = grid[:8, :16]

raw = json.load(
    open("/mnt/c/workspace/ipt-cityspace-engine/products/final/actuator_plan.json")
)
E = raw.get("events", raw)
p = []
v = []
pos = (0, 0)
for e in E:
    if e["type"] == "move":
        pos = (e["row"], e["col"])
    elif e["type"] == "set_height_cm":
        p.append(pos)
        v.append(e["value_cm"])

# 🔥 GARANTE QUE PONTOS ESTÃO NO GRID
p = [(min(r, 7), min(c, 15)) for r, c in p]

T = len(v)
d = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])
tl = [0]
for i in range(1, len(p)):
    tl.append(tl[-1] + 0.2 * d(p[i - 1], p[i]) + 0.08 * abs(v[i] - v[i - 1]))
TMAX = tl[-1] if tl else 0

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
def r(a, b):
    return dash.callback_context.triggered_id == "play"


@app.callback(
    Output("dir", "data"),
    Input("fwd", "n_clicks"),
    Input("back", "n_clicks"),
    prevent_initial_call=True,
)
def dr(a, b):
    return -1 if dash.callback_context.triggered_id == "back" else 1


@app.callback(
    Output("zoom_state", "data"),
    Input("zoom_btn", "n_clicks"),
    State("zoom_state", "data"),
    prevent_initial_call=True,
)
def z(a, b):
    return 2 if b == 1 else 1


@app.callback(
    Output("time", "data"),
    Input("t", "n_intervals"),
    Input("run", "data"),
    Input("dir", "data"),
    Input("time", "data"),
    prevent_initial_call=True,
)
def tk(n, rn, d, t):
    return t if not rn else max(0, min(TMAX, t + d * 0.05))


def gs(t):
    for i, x in enumerate(tl):
        if x >= t:
            return i
    return len(tl) - 1


@app.callback(
    Output("g", "figure"),
    Output("status", "children"),
    Input("time", "data"),
    Input("zoom_state", "data"),
)
def rd(t, zm):
    s = gs(t)
    Z = np.zeros((8, 16))
    for i, (r, c) in enumerate(p):
        if i <= s:
            Z[r][c] = v[i]
    sc = 2 if zm == 2 else 1
    fig = go.Figure()
    fig.add_trace(go.Heatmap(z=Z, colorscale="Jet", zmin=0, zmax=10, xgap=3, ygap=3))
    if s < len(p):
        r, c = p[s]
        fig.add_trace(
            go.Scatter(
                x=[c],
                y=[r],
                mode="markers",
                marker=dict(color="white", size=12),
                showlegend=False,
            )
        )
    fig.update_layout(
        width=900 * sc,
        height=450 * sc,
        plot_bgcolor="black",
        paper_bgcolor="black",
        xaxis=dict(range=[-0.5, 15.5]),
        yaxis=dict(range=[7.5, -0.5]),
    )
    fig.update_xaxes(
        dtick=1,
        tickmode="array",
        tickvals=list(range(16)),
        ticktext=list(range(2040, 2040 + 5 * 16, 5)),
        title="Av. Politécnica",
    )
    fig.update_yaxes(title="USP", showticklabels=False)
    val = v[s] if s < len(v) else 0
    return fig, f"STEP {s}/{T} | {val:.1f} cm | {val/100:.2f} m"


if __name__ == "__main__":
    print(">>> STARTING DASH <<<")
    app.run(host="127.0.0.1", port=8050, debug=False, use_reloader=False)
