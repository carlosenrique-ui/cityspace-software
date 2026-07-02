import json, numpy as np, pandas as pd, dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go

df = pd.read_csv("/mnt/c/workspace/ipt-cityspace-engine/products/final/grid_height.csv")
Z0 = df.pivot(index="row", columns="col", values="z_cm").values[:8, :16]
nx, ny = 16, 8
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
    tl.append(tl[-1] + 0.2 * d(p[i - 1], p[i]) + 0.12 * abs(v[i]))
TMAX = tl[-1] if tl else 0


def cube(x, y, h, s=0.9):
    x0, x1 = x - s / 2, x + s / 2
    y0, y1 = y - s / 2, y + s / 2
    z0, z1 = 0, h
    X = [x0, x1, x1, x0, x0, x1, x1, x0]
    Y = [y0, y0, y1, y1, y0, y0, y1, y1]
    Z = [z0, z0, z0, z0, z1, z1, z1, z1]
    I = [0, 0, 0, 4, 4, 5, 1, 2, 3, 6, 7, 6]
    J = [1, 2, 3, 5, 6, 6, 5, 6, 7, 7, 4, 5]
    K = [2, 3, 1, 6, 7, 7, 6, 7, 4, 4, 5, 4]
    return X, Y, Z, I, J, K


def gs(t):
    for i, x in enumerate(tl):
        if x >= t:
            return i
    return len(tl) - 1


app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id="g", style={"width": "100%", "height": "90vh"}),
        html.Div(
            [
                html.Button("<<", id="b"),
                html.Button("Play", id="p"),
                html.Button("Pause", id="s"),
                html.Button(">>", id="f"),
            ],
            style={"textAlign": "center"},
        ),
        dcc.Interval(id="i", interval=80),
        dcc.Store(id="t", data=0),
        dcc.Store(id="r", data=False),
        dcc.Store(id="d", data=1),
    ]
)


@app.callback(
    Output("r", "data"),
    Input("p", "n_clicks"),
    Input("s", "n_clicks"),
    State("r", "data"),
    prevent_initial_call=True,
)
def run(a, b, c):
    return True if ctx.triggered_id == "p" else False if ctx.triggered_id == "s" else c


@app.callback(
    Output("d", "data"),
    Input("f", "n_clicks"),
    Input("b", "n_clicks"),
    State("d", "data"),
    prevent_initial_call=True,
)
def dir(a, b, c):
    return 1 if ctx.triggered_id == "f" else -1 if ctx.triggered_id == "b" else c


@app.callback(
    Output("t", "data"),
    Input("i", "n_intervals"),
    State("r", "data"),
    State("d", "data"),
    State("t", "data"),
)
def step(n, r, d, t):
    return t if not r else max(0, min(TMAX, t + d * 0.05))


@app.callback(Output("g", "figure"), Input("t", "data"))
def draw(t):
    s = gs(t)
    Z = np.zeros((ny, nx))
    for i, (r, c) in enumerate(p):
        if i <= s:
            Z[r][c] = v[i]
    fig = go.Figure()
    for r in range(ny):
        for c in range(nx):
            h = Z[r][c]
            if h > 0:
                X, Y, Zv, I, J, K = cube(c, r, h)
                fig.add_trace(
                    go.Mesh3d(
                        x=X,
                        y=Y,
                        z=Zv,
                        i=I,
                        j=J,
                        k=K,
                        intensity=[h] * len(X),
                        colorscale="Jet",
                        cmin=0,
                        cmax=10,
                        opacity=1.0,
                        showscale=False,
                        lighting=dict(ambient=0.4, diffuse=0.9, specular=0.3),
                        lightposition=dict(x=100, y=100, z=200),
                    )
                )
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(title="Altura"),
            camera=dict(eye=dict(x=1.7, y=1.7, z=1.0)),
        ),
        margin=dict(l=0, r=0, t=0, b=0),
    )
    return fig


if __name__ == "__main__":
    print(">>> V99 3D BUILDINGS ZIGZAG <<<", flush=True)
    app.run(host="0.0.0.0", port=8050, debug=False)
