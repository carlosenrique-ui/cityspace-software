import json, numpy as np, pandas as pd, dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go

# =========================================
# LOAD GRID REAL
# =========================================
df = pd.read_csv("products/final/grid_height.csv")

grid = df.pivot(index="row", columns="col", values="z_cm").values[:8, :16]
grid = np.flipud(grid)

ny, nx = grid.shape

# escala REAL (fix crítico)
ZMAX = np.max(grid)

# =========================================
# ANOS
# =========================================
anos = [
    1940,
    1945,
    1950,
    1956,
    1961,
    1966,
    1972,
    1977,
    1982,
    1988,
    1993,
    1998,
    2004,
    2009,
    2014,
    2020,
]

fase_cor = {
    "1940-1959": "#4A90E2",
    "1960-1979": "#50E3C2",
    "1980-1999": "#F5A623",
    "2000-2020": "#D0021B",
}


def cor_ano(a):
    if a <= 1959:
        return fase_cor["1940-1959"]
    if a <= 1979:
        return fase_cor["1960-1979"]
    if a <= 1999:
        return fase_cor["1980-1999"]
    return fase_cor["2000-2020"]


# =========================================
# ZIGZAG CORRETO (ATUADOR)
# =========================================
traj = []
for c in range(nx):
    if c % 2 == 0:
        for r in range(ny):  # topo → baixo (corrigido)
            traj.append((r, c))
    else:
        for r in range(ny - 1, -1, -1):  # baixo → topo
            traj.append((r, c))

TMAX = len(traj)

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
def run(a, b, c):
    if ctx.triggered_id == "play":
        return True
    if ctx.triggered_id == "pause":
        return False
    return c


@app.callback(
    Output("direction", "data"),
    Input("fwd", "n_clicks"),
    Input("back", "n_clicks"),
    State("direction", "data"),
    prevent_initial_call=True,
)
def direcao(a, b, c):
    if ctx.triggered_id == "fwd":
        return 1
    if ctx.triggered_id == "back":
        return -1
    return c


@app.callback(
    Output("time", "data"),
    Input("interval", "n_intervals"),
    State("running", "data"),
    State("direction", "data"),
    State("time", "data"),
)
def tempo(n, r, d, t):
    if not r:
        return t
    return max(0, min(TMAX - 1, t + d))


# =========================================
# RENDER
# =========================================
@app.callback(Output("graph", "figure"), Input("time", "data"))
def render(t):

    step = int(t)

    Z = np.zeros_like(grid)
    for i in range(step + 1):
        r, c = traj[i]
        Z[r][c] = grid[r][c]

    r, c = traj[step]

    fig = go.Figure()

    # watermark IPT (corrigido e estável)
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

    # heatmap REAL
    fig.add_trace(
        go.Heatmap(
            z=Z,
            colorscale="Jet",
            zmin=0,
            zmax=ZMAX,
            xgap=1,
            ygap=1,
            colorbar=dict(title="Altura (cm)"),
        )
    )

    # célula ativa (borda branca forte)
    fig.add_shape(
        type="rect",
        x0=c - 0.5,
        x1=c + 0.5,
        y0=r - 0.5,
        y1=r + 0.5,
        line=dict(color="white", width=4),
    )

    ano = anos[min(c, len(anos) - 1)]

    fig.update_layout(
        title=dict(
            text=f"<b>IPT – CitySpace | {ano}</b>",
            x=0.5,
            font=dict(size=20, color=cor_ano(ano)),
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        plot_bgcolor="white",
    )

    fig.update_xaxes(
        tickvals=list(range(nx)),
        ticktext=[f"<b>{a}</b>" for a in anos],
        title="Av. Escola Politécnica →",
    )

    fig.update_yaxes(
        autorange="reversed", scaleanchor="x", showticklabels=False, title="USP →"
    )

    return fig


# =========================================
# RUN
# =========================================
if __name__ == "__main__":
    print(">>> V95.1 REAL CORRETO <<<", flush=True)
    app.run(host="0.0.0.0", port=8050, debug=False)
