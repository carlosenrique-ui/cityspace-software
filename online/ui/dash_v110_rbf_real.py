from pathlib import Path
import json
import numpy as np
import geopandas as gpd
import dash
from dash import dcc, html
import plotly.graph_objects as go

THIS_FILE = Path(__file__).resolve()
CORE_ROOT = THIS_FILE.parents[2]

SURFACE = CORE_ROOT / "offline/products/scientific/rbf_terrain_surface_real.npz"
CONTOURS = CORE_ROOT / "offline/products/scientific/curvas_rbf_terrain_2m_real.geojson"
POLY = CORE_ROOT / "offline/products/scientific/poligono_urbanismo_ipt_outer_real.gpkg"

data = np.load(SURFACE)
x, y, z = data["x"], data["y"], data["z"]

with open(CONTOURS, "r", encoding="utf-8") as f:
    geojson = json.load(f)

poly = gpd.read_file(POLY)

app = dash.Dash(__name__)
fig = go.Figure()

fig.add_trace(go.Heatmap(
    x=x,
    y=y,
    z=z,
    colorscale="Viridis",
    showscale=True,
    colorbar=dict(title="Terreno<br>(m)"),
))

for feat in geojson["features"]:
    elev = feat["properties"]["elevation"]
    coords = feat["geometry"]["coordinates"]

    xs = [p[0] for p in coords]
    ys = [p[1] for p in coords]

    fig.add_trace(go.Scatter(
        x=xs,
        y=ys,
        mode="lines",
        line=dict(color="black", width=2.2 if int(elev) % 10 == 0 else 1.0),
        opacity=0.85 if int(elev) % 10 == 0 else 0.5,
        showlegend=False,
        hovertemplate=f"{elev:.0f} m<extra></extra>",
    ))

for geom in poly.geometry:
    xs, ys = geom.exterior.xy
    fig.add_trace(go.Scatter(
        x=list(xs),
        y=list(ys),
        mode="lines",
        line=dict(color="white", width=3),
        showlegend=False,
        hoverinfo="skip",
    ))

fig.update_layout(
    title="V110 REAL — RBF terreno em coordenadas reais",
    margin=dict(l=0, r=0, t=36, b=0),
    xaxis=dict(visible=False),
    yaxis=dict(visible=False, scaleanchor="x", scaleratio=1),
    plot_bgcolor="white",
    paper_bgcolor="white",
)

app.layout = html.Div(
    [dcc.Graph(figure=fig, config={"displayModeBar": False}, style={"width": "100vw", "height": "100vh"})],
    style={"margin": "0", "padding": "0"},
)

if __name__ == "__main__":
    print("V110 REAL")
    print("SURFACE:", SURFACE)
    print("CONTOURS:", CONTOURS)
    print("POLY:", POLY)
    print("features:", len(geojson["features"]))
    app.run(debug=True)
