# =========================================
# DASH V100 – CONTOURS DTM (ALINHAMENTO CORRETO)
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

# =========================================
# PATHS
# =========================================

THIS_FILE = Path(__file__).resolve()
CORE_ROOT = THIS_FILE.parents[2]
PROJECT_ROOT = CORE_ROOT.parent

GRID_PATH = CORE_ROOT / "offline/products/scientific/grid_metrics_utm.csv"

CONTOUR_PATH = CORE_ROOT / "offline/products/scientific/curvas_dtm_true_2m.gpkg"

PNG_PATH = PROJECT_ROOT / "backup_git_20260317_191244/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_v3.png"

# =========================================
# LOAD GRID
# =========================================

df = pd.read_csv(GRID_PATH)
grid = df.pivot(index="row", columns="col", values="z_total_m").values
rows, cols = grid.shape

# =========================================
# LOAD CONTOURS (UTM REAL)
# =========================================

gdf = gpd.read_file(CONTOUR_PATH)

minx, miny, maxx, maxy = gdf.total_bounds

def norm_x(x):
    return (x - minx) / (maxx - minx) * (cols - 1)

def norm_y(y):
    return (y - miny) / (maxy - miny) * (rows - 1)

# =========================================
# LOAD PNG
# =========================================

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

# =========================================
# DASH
# =========================================

app = dash.Dash(__name__)
fig = go.Figure()

# HEATMAP
fig.add_trace(
    go.Heatmap(
        z=grid,
        colorscale="Viridis",
        showscale=False,
    )
)

# =========================================
# CONTOURS CORRETOS (DTM)
# =========================================

for geom in gdf.geometry:

    if geom is None:
        continue

    if geom.geom_type == "LineString":
        xs, ys = geom.xy

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

    elif geom.geom_type == "MultiLineString":
        for line in geom.geoms:
            xs, ys = line.xy

            xs = [norm_x(x) for x in xs]
            ys = [norm_y(y) for y in ys]

            fig.add_trace(
                go.Scatter(
                    x=xs,
                    y=ys,
                    mode="lines",
                    line=dict(width=1, color="black"),
                    opacity=0.42,
                    showlegend=False,
                )
            )

# WATERMARK
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

# LAYOUT
fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    xaxis=dict(visible=False),
    yaxis=dict(visible=False, autorange="reversed"),
)

app.layout = html.Div([dcc.Graph(figure=fig)])

if __name__ == "__main__":
    print("V102 — DTM TRUE curves 2m")
    print("Contours:", len(gdf))
    print("Bounds:", gdf.total_bounds)
    app.run(debug=True)
