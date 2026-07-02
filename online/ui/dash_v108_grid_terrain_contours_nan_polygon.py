from pathlib import Path
import json
import numpy as np
import pandas as pd
import dash
from dash import dcc, html
import plotly.graph_objects as go

THIS_FILE = Path(__file__).resolve()
CORE_ROOT = THIS_FILE.parents[2]

GRID_PATH = CORE_ROOT / "offline/products/scientific/grid_metrics_utm.csv"
CONTOUR_PATH = CORE_ROOT / "offline/products/scientific/curvas_grid_terrain_2m_nan_polygon.geojson"
GRID_MASKED_PATH = CORE_ROOT / "offline/products/scientific/grid_terrain_nan_polygon.npy"

ROWS = 8
COLS = 16

df = pd.read_csv(GRID_PATH)

# Agora as cores também são DTM puro, não z_total.
grid = np.load(GRID_MASKED_PATH)

with open(CONTOUR_PATH, "r", encoding="utf-8") as f:
    geojson = json.load(f)

app = dash.Dash(__name__)
fig = go.Figure()

fig.add_trace(
    go.Heatmap(
        z=grid,
        colorscale="Viridis",
        showscale=True,
        colorbar=dict(title="Terreno<br>(m)"),
        xgap=0,
        ygap=0,
        hovertemplate="col=%{x}<br>row=%{y}<br>terreno=%{z:.2f} m<extra></extra>",
    )
)

for feat in geojson["features"]:
    geom = feat["geometry"]
    elev = feat["properties"]["elevation"]

    if geom["type"] == "LineString":
        lines = [geom["coordinates"]]
    elif geom["type"] == "MultiLineString":
        lines = geom["coordinates"]
    else:
        continue

    width = 2.2 if int(elev) % 10 == 0 else 1.0
    opacity = 0.85 if int(elev) % 10 == 0 else 0.55

    for coords in lines:
        xs = [p[0] for p in coords]
        ys = [p[1] for p in coords]

        fig.add_trace(
            go.Scatter(
                x=xs,
                y=ys,
                mode="lines",
                line=dict(width=width, color="black"),
                opacity=opacity,
                showlegend=False,
                hovertemplate=f"{elev:.0f} m<extra></extra>",
            )
        )

fig.update_layout(
    title="IPT-CitySpace — Terreno DTM por grid + curvas 2m + NaN fora do polígono",
    margin=dict(l=0, r=0, t=36, b=0),
    xaxis=dict(visible=False, range=[-0.5, COLS - 0.5]),
    yaxis=dict(visible=False, range=[ROWS - 0.5, -0.5]),
    plot_bgcolor="white",
    paper_bgcolor="white",
)

app.layout = html.Div(
    [dcc.Graph(figure=fig, config={"displayModeBar": False}, style={"width": "100vw", "height": "100vh"})],
    style={"margin": "0", "padding": "0"},
)

if __name__ == "__main__":
    print("V108 — grid z_terrain_m + contours 2m + NaN fora do polígono")
    print("GRID:", GRID_PATH)
    print("CONTOURS:", CONTOUR_PATH)
    print("GRID MASKED:", GRID_MASKED_PATH)
    print("features:", len(geojson["features"]))
    app.run(debug=True)
