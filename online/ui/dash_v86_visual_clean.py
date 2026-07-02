import json, numpy as np, pandas as pd, dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go
from PIL import Image

df = pd.read_csv("/mnt/c/workspace/ipt-cityspace-engine/products/final/grid_height.csv")
grid = df.pivot(index="row", columns="col", values="z_cm").values[:8, :16]
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
p = [(min(r, 7), min(c, 15)) for r, c in p]
tl = [0]
d = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])
for i in range(1, len(p)):
    tl.append(tl[-1] + 0.2 * d(p[i - 1], p[i]) + 0.08 * abs(v[i] - v[i - 1]))
TMAX = tl[-1] if tl else 0
img = Image.open("assets/ipt_mask_rotated_simple.png")
W, H = img.size
nx, ny = 16, 8
app = dash.Dash(__name__, assets_folder="assets")
app.layout = html.Div(
    [
        dcc.Graph(
            id="graph",
            config={"displayModeBar": False},
            style={"width": "100%", "height": "85vh"},
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
        dcc.Interval(id="interval", interval=50),
        dcc.Store(id="time", data=0),
        dcc.Store(id="running", data=False),
        dcc.Store(id="direction", data=1),
    ]
)


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


def gs(t):
    for i, x in enumerate(tl):
        if x >= t:
            return i
    return len(tl) - 1


@app.callback(Output("graph", "figure"), Input("time", "data"))
def rd(t):
    s = gs(t)
    Z = np.zeros((ny, nx))
    for i, (r, c) in enumerate(p):
        if i <= s:
            Z[r][c] = v[i]
    fig = go.Figure()
    fig.update_layout(
        images=[
            dict(
                source="assets/ipt_mask_rotated_simple.png",
                xref="x",
                yref="y",
                x=0,
                y=0,
                sizex=nx,
                sizey=ny,
                sizing="stretch",
                opacity=0.35,
                layer="below",
            )
        ]
    )
    fig.add_trace(
        go.Heatmap(z=Z, colorscale="Jet", zmin=0, zmax=10, xgap=1, ygap=1, opacity=0.65)
    )
    if s < len(p):
        r, c = p[s]
        fig.add_trace(
            go.Scatter(
                x=[c + 0.5],
                y=[r + 0.5],
                mode="markers",
                marker=dict(size=14, color="white", line=dict(width=2, color="black")),
                showlegend=False,
            )
        )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(range=[0, nx], visible=False),
        yaxis=dict(range=[ny, 0], visible=False, scaleanchor="x"),
        plot_bgcolor="white",
    )
    return fig


if __name__ == "__main__":
    print(">>> V87 IMAGE-LOCK GRID <<<", flush=True)
    app.run(host="0.0.0.0", port=8050, debug=False)
