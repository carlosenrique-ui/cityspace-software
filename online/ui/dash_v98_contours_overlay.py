# =========================================
# DASH V98 – GRID + WATERMARK + CONTOURS
# =========================================

import base64
import numpy as np
import pandas as pd
from io import BytesIO
from PIL import Image
import dash
from dash import dcc, html
import plotly.graph_objects as go
import geopandas as gpd

# =========================================
# CONFIG
# =========================================

GRID_PATH = "offline/products/scientific/grid_metrics_utm.csv"

CONTOUR_PATH = "offline/products/scientific/grid_contours_rotated_scientific.gpkg"

PNG_PATH = "/mnt/c/workspace/ipt-cityspace-engine/backup_git_20260317_191244/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_v3.png"

ROTATION_DEG = -7.20
SCALE = 0.62
OFFSET_X = -0.03
OFFSET_Y = +0.06

# =========================================
# LOAD GRID
# =========================================

df = pd.read_csv(GRID_PATH)
grid = df.pivot(index="row", columns="col", values="z_total_m").values
rows, cols = grid.shape

# =========================================
# LOAD CONTOURS
# =========================================

gdf = gpd.read_file(CONTOUR_PATH)

# normalizar para grid (escala simples)
minx, miny, maxx, maxy = gdf.total_bounds


def normalize(x, xmin, xmax, n):
    return (x - xmin) / (xmax - xmin) * (n - 1)


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
img = img.rotate(ROTATION_DEG, expand=True)

buf = BytesIO()
img.save(buf, format="PNG")
encoded = base64.b64encode(buf.getvalue()).decode()

# =========================================
# DASH
# =========================================

app = dash.Dash(__name__)

fig = go.Figure()

# =========================================
# HEATMAP
# =========================================

fig.add_trace(
    go.Heatmap(
        z=grid,
        colorscale="Viridis",
        showscale=False,
        xgap=0,
        ygap=0,
    )
)

# =========================================
# CONTOURS (linhas)
# =========================================

for geom in gdf.geometry:

    if geom.geom_type == "LineString":
        xs, ys = geom.xy

        xs = [normalize(x, minx, maxx, cols) for x in xs]
        ys = [normalize(y, miny, maxy, rows) for y in ys]

        fig.add_trace(
            go.Scatter(
                x=xs,
                y=ys,
                mode="lines",
                line=dict(width=1, color="black"),
                opacity=0.4,
                showlegend=False,
            )
        )

# =========================================
# WATERMARK
# =========================================

fig.add_layout_image(
    dict(
        source=f"data:image/png;base64,{encoded}",
        xref="paper",
        yref="paper",
        x=0.5 + OFFSET_X,
        y=0.5 + OFFSET_Y,
        sizex=SCALE,
        sizey=SCALE,
        xanchor="center",
        yanchor="middle",
        opacity=0.25,
        layer="below",
    )
)

# =========================================
# LAYOUT
# =========================================

fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    xaxis=dict(visible=False),
    yaxis=dict(visible=False, autorange="reversed"),
)

app.layout = html.Div([dcc.Graph(figure=fig, config={"displayModeBar": False})])

# =========================================
# RUN
# =========================================

if __name__ == "__main__":
    app.run(debug=True)
