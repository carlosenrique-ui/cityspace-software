import json, numpy as np, pandas as pd, dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go

df = pd.read_csv("products/final/grid_height.csv")
grid = df.pivot(index="row", columns="col", values="z_cm")
grid = grid.reindex(index=range(8), columns=range(16))
grid = grid.values
df_full = df.pivot(index="row", columns="col", values="z_total")
df_full = df_full.reindex(index=range(8), columns=range(16)).values
raw = json.load(open("products/final/actuator_plan.json"))
E = raw.get("events", raw)
traj = []
cols = 16
rows = 8
for c in reversed(range(cols)):
    if (cols - c) % 2 == 1:
        for r in range(rows):
            traj.append((r, c))
    else:
        for r in reversed(range(rows)):
            traj.append((r, c))
p = []
v = []
idx = 0
for r, c in traj:
    if idx < len(E):
        p.append((r, c))
        v.append(grid[r][c])
        idx += 1
tl = [0.0]
for i in range(1, len(p)):
    tl.append(tl[-1] + 0.05)
TMAX = tl[-1] if tl else 0
FASES = [
    (1940, 1959, "Implantação", "#2E86C1"),
    (1960, 1979, "Expansão", "#239B56"),
    (1980, 1999, "Consolidação", "#C0392B"),
    (2000, 2020, "Inovação", "#E67E22"),
]


def fase(ano):
    for i, f, n, c in FASES:
        if i <= ano <= f:
            return n, c
    return "Fase", "#444"


anos = np.linspace(1940, 2020, 16).astype(int)
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
        dcc.Interval(id="interval", interval=60),
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
    Z = np.zeros((8, 16))
    last = None
    for i, (r, c) in enumerate(p):
        if i <= s:
            Z[r][c] = grid[r][c]
            last = (r, c)
    fig = go.Figure()
    fig.update_layout(
        images=[
            dict(
                source="assets/ipt_mask_rotated_simple.png",
                xref="x",
                yref="y",
                x=-0.5,
                y=-0.5,
                sizex=16,
                sizey=8,
                sizing="stretch",
                opacity=0.25,
                layer="below",
            )
        ]
    )
    fig.add_trace(
        go.Heatmap(
            z=Z,
            colorscale="Jet",
            zmin=0,
            zmax=10,
            xgap=1,
            ygap=1,
            opacity=0.8,
            colorbar=dict(
                title="Pino (cm) / Teto (m)",
                tickvals=[0, 2, 4, 6, 8, 10],
                ticktext=[
                    f"{v} / {round(v/10*df_full.max(),1)}" for v in [0, 2, 4, 6, 8, 10]
                ],
            ),
        )
    )
    if last:
        r, c = last
        fig.add_shape(
            type="rect",
            x0=c - 0.5,
            x1=c + 0.5,
            y0=r - 0.5,
            y1=r + 0.5,
            line=dict(color="yellow", width=4),
        )
        ano = anos[c]
        nome, cor = fase(ano)
        fig.update_layout(
            title=dict(
                text=f"IPT – CitySpace | {nome} ({ano})", font=dict(size=20, color=cor)
            )
        )
    fig.update_xaxes(
        tickvals=list(range(16)), ticktext=[str(a) for a in anos], showgrid=False
    )
    for i, a in enumerate(anos):
        _, cor = fase(a)
        fig.add_annotation(
            x=i, y=8.2, text=str(a), showarrow=False, font=dict(color=cor, size=12)
        )
    fig.update_layout(
        margin=dict(l=40, r=0, t=50, b=40),
        xaxis_title="Av. Escola Politécnica →",
        yaxis_title="USP →",
        xaxis=dict(range=[-0.5, 15.5]),
        yaxis=dict(range=[7.5, -0.5], scaleanchor="x"),
        plot_bgcolor="white",
    )
    return fig


if __name__ == "__main__":
    print(">>> V95 FINAL (ZIGZAG CORRETO + UI CIENTÍFICA) <<<")
    app.run(host="0.0.0.0", port=8050, debug=False)
