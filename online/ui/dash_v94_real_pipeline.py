import json, numpy as np, pandas as pd, dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go

# =========================================
# LOAD REAL GRID (PIPELINE FINAL)
# =========================================
df = pd.read_csv("products/final/grid_height.csv")

# 🔥 usar diretamente z_cm (já normalizado pelo pipeline)
grid = df.pivot(index="row", columns="col", values="z_cm").values[:8, :16]

# 🔥 alinhar sistema visual (origem topo-esquerdo)
grid = np.flipud(grid)

ny, nx = grid.shape

# =========================================
# LOAD ACTUATOR PLAN (TRAJETÓRIA REAL)
# =========================================
raw = json.load(open("products/final/actuator_plan.json"))
E = raw.get("events", raw)

p = []
pos = (0, 0)

for e in E:
    if e["type"] == "move":
        pos = (e["row"], e["col"])
    elif e["type"] == "set_height_cm":
        p.append(pos)

# limitar grid físico
p = [(min(r, ny - 1), min(c, nx - 1)) for r, c in p]

# =========================================
# TEMPO (MANTIDO — SEM INVENTAR)
# =========================================
tl = [0]
d = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])

for i in range(1, len(p)):
    tl.append(tl[-1] + 0.2 * d(p[i - 1], p[i]))

TMAX = tl[-1] if tl else 0

# =========================================
# DASH
# =========================================
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
        dcc.Interval(id="interval", interval=60),
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
def run(a, b, c):
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
def direction(a, b, c):
    return -1 if ctx.triggered_id == "back" else 1 if ctx.triggered_id == "fwd" else c


@app.callback(
    Output("time", "data"),
    Input("interval", "n_intervals"),
    State("running", "data"),
    State("direction", "data"),
    State("time", "data"),
)
def tempo(n, r, d, t):
    return t if not r else max(0, min(TMAX, t + d * 0.05))


# =========================================
# STEP
# =========================================
def get_step(t):
    for i, x in enumerate(tl):
        if x >= t:
            return i
    return len(tl) - 1


# =========================================
# RENDER (CORREÇÃO REAL)
# =========================================
@app.callback(Output("graph", "figure"), Input("time", "data"))
def render(t):

    s = get_step(t)

    # 🔥 estado começa vazio
    Z = np.zeros_like(grid)

    # 🔥 preencher com DADO REAL (CSV)
    for i, (r, c) in enumerate(p):
        if i <= s:
            Z[r][c] = grid[r][c]

    fig = go.Figure()

    # watermark IPT (mantido)
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
                opacity=0.30,
                layer="below",
            )
        ]
    )

    # 🔥 heatmap REAL
    fig.add_trace(go.Heatmap(z=Z, colorscale="Jet", zmin=0, zmax=10, xgap=1, ygap=1))

    # célula ativa
    if s < len(p):
        r, c = p[s]
        fig.add_shape(
            type="rect",
            x0=c - 0.5,
            x1=c + 0.5,
            y0=r - 0.5,
            y1=r + 0.5,
            line=dict(color="white", width=2),
            fillcolor="rgba(255,255,255,0.25)",
        )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(range=[-0.5, nx - 0.5], visible=False),
        yaxis=dict(
            range=[-0.5, ny - 0.5], autorange="reversed", visible=False, scaleanchor="x"
        ),
        plot_bgcolor="white",
    )

    return fig


# =========================================
# RUN
# =========================================
if __name__ == "__main__":
    print(">>> V94 REAL PIPELINE <<<", flush=True)
    app.run(host="0.0.0.0", port=8050, debug=False)
