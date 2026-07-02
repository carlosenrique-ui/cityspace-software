import json, numpy as np, pandas as pd, dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go

# =========================================
# LOAD REAL DATA (PIPELINE)
# =========================================
df = pd.read_csv("/mnt/c/workspace/ipt-cityspace-engine/products/final/grid_height.csv")

# 🔥 usa altura REAL TOTAL (m)
grid_m = df.pivot(index="row", columns="col", values="z_total_m").values[:8, :16]

# 🔥 orientação correta
grid_m = np.flipud(grid_m)

# 🔥 normalização física → atuador (cm)
ZMAX_REAL_M = np.max(grid_m)
grid_cm = (grid_m / ZMAX_REAL_M) * 10.0

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

# =========================================
# TEMPO (INALTERADO)
# =========================================
tl = [0]
d = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])

for i in range(1, len(p)):
    tl.append(tl[-1] + 0.2 * d(p[i - 1], p[i]) + 0.12 * abs(v[i]))

TMAX = tl[-1] if tl else 0

nx, ny = 16, 8

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
            # 🔥 usa valor do atuador (cm real do plano)
            Z[r][c] = v[i]

    fig = go.Figure()

    # watermark IPT
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

    # 🔥 heatmap em cm (atuador)
    fig.add_trace(
        go.Heatmap(
            z=Z,
            colorscale="Jet",
            zmin=0,
            zmax=10,
            xgap=1,
            ygap=1,
            opacity=0.75,
            colorbar=dict(title=f"Pino (cm)\n0–10 cm\n≙ 0–{ZMAX_REAL_M:.1f} m"),
        )
    )

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
    print(">>> V94.2 NORMALIZADO <<<", flush=True)
    app.run(host="0.0.0.0", port=8050, debug=False)
