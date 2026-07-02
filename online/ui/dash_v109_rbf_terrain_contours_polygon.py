from pathlib import Path
import json
import numpy as np
import dash
from dash import dcc, html
import plotly.graph_objects as go

THIS_FILE = Path(__file__).resolve()
CORE_ROOT = THIS_FILE.parents[2]

SURFACE_PATH = CORE_ROOT / "offline/products/scientific/rbf_terrain_surface_polygon.npy"
CONTOUR_PATH = CORE_ROOT / "offline/products/scientific/curvas_rbf_terrain_2m_polygon.geojson"

surface = np.load(SURFACE_PATH)

with open(CONTOUR_PATH, "r", encoding="utf-8") as f:
    geojson = json.load(f)

app = dash.Dash(__name__)
fig = go.Figure()

fig.add_trace(
    go.Heatmap(
        z=surface,
        colorscale="Viridis",
        showscale=True,
        colorbar=dict(title="Terreno<br>(m)"),
        hovertemplate="x=%{x}<br>y=%{y}<br>z=%{z:.2f} m<extra></extra>",
    )
)

for feat in geojson["features"]:
    elev = feat["properties"]["elevation"]
    geom = feat["geometry"]

    lines = [geom["coordinates"]] if geom["type"] == "LineString" else geom["coordinates"]

    width = 2.4 if int(elev) % 10 == 0 else 1.0
    opacity = 0.9 if int(elev) % 10 == 0 else 0.55

    for coords in lines:
        xs = [p[0] / 15 * (surface.shape[1] - 1) for p in coords]
        ys = [p[1] / 7 * (surface.shape[0] - 1) for p in coords]

        fig.add_trace(
            go.Scatter(
                x=xs,
                y=ys,
                mode="lines",
                line=dict(color="black", width=width),
                opacity=opacity,
                showlegend=False,
                hovertemplate=f"{elev:.0f} m<extra></extra>",
            )
        )

fig.update_layout(
    title="V109 — Superfície RBF do terreno + curvas 2m dentro do polígono IPT",
    margin=dict(l=0, r=0, t=36, b=0),
    xaxis=dict(visible=False),
    yaxis=dict(visible=False, autorange="reversed"),
    plot_bgcolor="white",
    paper_bgcolor="white",
)

app.layout = html.Div(
    [dcc.Graph(figure=fig, config={"displayModeBar": False}, style={"width": "100vw", "height": "100vh"})],
    style={"margin": "0", "padding": "0"},
)

if __name__ == "__main__":
    print("V109 — RBF terrain contours polygon")
    print("SURFACE:", SURFACE_PATH)
    print("CONTOURS:", CONTOUR_PATH)
    print("features:", len(geojson["features"]))
    app.run(debug=True)
