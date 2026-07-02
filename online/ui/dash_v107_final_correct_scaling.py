import base64
from pathlib import Path
from io import BytesIO

import numpy as np
import pandas as pd
from PIL import Image
import dash
from dash import dcc, html
import plotly.graph_objects as go
import geopandas as gpd

THIS_FILE = Path(__file__).resolve()
CORE_ROOT = THIS_FILE.parents[2]
PROJECT_ROOT = CORE_ROOT.parent

GRID_PATH = CORE_ROOT / "offline/products/scientific/grid_metrics_utm.csv"
CONTOUR_PATH = CORE_ROOT / "offline/products/scientific/curvas_dtm_true_2m.gpkg"
POLYGON_PATH = CORE_ROOT / "offline/products/scientific/urban_envelope_scientific_rotated_clean.gpkg"

# =========================================
# LOAD GRID
# =========================================

df = pd.read_csv(GRID_PATH)
grid = df.pivot(index="row", columns="col", values="z_total_m").values
rows, cols = grid.shape

# =========================================
# LOAD DATA
# =========================================

poly = gpd.read_file(POLYGON_PATH).dissolve()
gdf = gpd.read_file(CONTOUR_PATH, layer="curvas_dtm_true_2m")

# CLIP (CORRETO)
gdf = gpd.clip(gdf, poly)

# 🔥 SCALE USANDO CURVAS (não polígono)
minx, miny, maxx, maxy = gdf.total_bounds

def norm_x(x):
    return (x - minx) / (maxx - minx) * (cols - 1)

def norm_y(y):
    return (rows - 1) - ((y - miny) / (maxy - miny) * (rows - 1))

# =========================================
# DASH
# =========================================

app = dash.Dash(__name__)
fig = go.Figure()

fig.add_trace(
    go.Heatmap(
        z=grid,
        colorscale="Viridis",
        showscale=False,
    )
)

for row in gdf.itertuples():

    geom = row.geometry
    if geom is None:
        continue

    lines = geom.geoms if geom.geom_type == "MultiLineString" else [geom]

    for line in lines:

        xs, ys = line.xy

        xs = [norm_x(x) for x in xs]
        ys = [norm_y(y) for y in ys]

        fig.add_trace(
            go.Scatter(
                x=xs,
                y=ys,
                mode="lines",
                line=dict(width=1, color="black"),
                opacity=0.5,
                showlegend=False,
            )
        )

fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
)

app.layout = html.Div([dcc.Graph(figure=fig)])

if __name__ == "__main__":
    print("V107 — SCALE CORRETO")
    print("Contours:", len(gdf))
    print("Bounds curvas:", gdf.total_bounds)
    app.run(debug=True)
