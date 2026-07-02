import numpy as np, pandas as pd, dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go

df = pd.read_csv("/mnt/c/workspace/ipt-cityspace-engine/products/final/grid_height.csv")
Z = df.pivot(index="row", columns="col", values="z_cm").values[:8, :16]
nx, ny = 16, 8
app = dash.Dash(__name__)
app.layout = html.Div([dcc.Graph(id="g", style={"width": "100%", "height": "90vh"})])


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


@app.callback(Output("g", "figure"), Input("g", "id"))
def draw(_):
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
                    )
                )
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(title="Altura"),
            camera=dict(eye=dict(x=1.8, y=1.8, z=1.0)),
        ),
        margin=dict(l=0, r=0, t=0, b=0),
    )
    return fig


if __name__ == "__main__":
    print(">>> V98 3D BUILDINGS <<<", flush=True)
    app.run(host="0.0.0.0", port=8050, debug=False)
