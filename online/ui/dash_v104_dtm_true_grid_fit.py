# =========================================
# DASH V104 – DTM TRUE FITADO NO GRID
# =========================================

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
PNG_PATH = PROJECT_ROOT / "backup_git_20260317_191244/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_v3.png"


df = pd.read_csv(GRID_PATH)
grid = df.pivot(index="row", columns="col", values="z_total_m").values
rows, cols = grid.shape

gdf = gpd.read_file(CONTOUR_PATH, layer="curvas_dtm_true_2m")
minx, miny, maxx, maxy = gdf.total_bounds


def norm_x(x):
    return (x - minx) / (maxx - minx) * (cols - 1)


def norm_y(y):
    return (rows - 1) - ((y - miny) / (maxy - miny) * (rows - 1))


img = Image.open(PNG_PATH).convert("RGBA")
np_img = np.array(img)
mask = np_img[:, :, 0:3].mean(axis=2) < 240
coords = np.argwhere(mask)

y0, x0 = coords.min(axis=0)
y1, x1 = coords.max(axis=0)

img = img.crop((x0, y0, x1, y1))
img = img.rotate(-7.20, expand=True)

buf = BytesIO()
img.save(buf, format="PNG")
encoded = base64.b64encode(buf.getvalue()).decode()


app = dash.Dash(__name__)
fig = go.Figure()

fig.add_trace(
    go.Heatmap(
        z=grid,
        colorscale="Viridis",
        showscale=False,
        xgap=0,
        ygap=0,
    )
)

for row in gdf.itertuples():
    geom = row.geometry
    if geom is None:
        continue

    lines = []
    if geom.geom_type == "LineString":
        lines = [geom]
    elif geom.geom_type == "MultiLineString":
        lines = list(geom.geoms)

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
                opacity=0.48,
                showlegend=False,
                hoverinfo="skip",
            )
        )

fig.add_layout_image(
    dict(
        source=f"data:image/png;base64,{encoded}",
        xref="paper",
        yref="paper",
        x=0.5 - 0.03,
        y=0.5 + 0.06,
        sizex=0.62,
        sizey=0.62,
        xanchor="center",
        yanchor="middle",
        opacity=0.25,
        layer="below",
    )
)

fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    xaxis=dict(visible=False, range=[-0.5, cols - 0.5]),
    yaxis=dict(visible=False, range=[rows - 0.5, -0.5]),
    plot_bgcolor="white",
    paper_bgcolor="white",
)

app.layout = html.Div(
    [
        dcc.Graph(
            figure=fig,
            config={"displayModeBar": False},
            style={"width": "100vw", "height": "100vh"},
        )
    ],
    style={"margin": "0", "padding": "0"},
)

if __name__ == "__main__":
    print("V104 — DTM TRUE grid fit")
    print("GRID:", GRID_PATH)
    print("CONTOURS:", CONTOUR_PATH)
    print("Contours rows:", len(gdf))
    print("Contour bounds:", gdf.total_bounds)
    print("Grid shape:", rows, cols)
    app.run(debug=True)
