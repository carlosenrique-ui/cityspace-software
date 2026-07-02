# =========================================
# DASH V99 – CONTOURS EM MESA SPACE
# caminho corrigido fora do ipt_core_clean
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
# PATHS ROBUSTOS
# =========================================

THIS_FILE = Path(__file__).resolve()

# /mnt/c/workspace/ipt-cityspace-engine/ipt_core_clean
CORE_ROOT = THIS_FILE.parents[2]

# /mnt/c/workspace/ipt-cityspace-engine
PROJECT_ROOT = CORE_ROOT.parent

GRID_PATH = CORE_ROOT / "offline/products/scientific/grid_metrics_utm.csv"

CONTOUR_PATH = PROJECT_ROOT / "offline/products/terrain/curvas_nivel_mesa_space.geojson"

PNG_PATH = PROJECT_ROOT / "backup_git_20260317_191244/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_v3.png"


# =========================================
# CHECKS
# =========================================

for label, path in [
    ("GRID_PATH", GRID_PATH),
    ("CONTOUR_PATH", CONTOUR_PATH),
    ("PNG_PATH", PNG_PATH),
]:
    if not path.exists():
        raise FileNotFoundError(f"{label} não encontrado: {path}")


# =========================================
# LOAD GRID
# =========================================

df = pd.read_csv(GRID_PATH)
grid = df.pivot(index="row", columns="col", values="z_total_m").values
rows, cols = grid.shape


# =========================================
# LOAD CONTOURS — JÁ EM MESA SPACE
# =========================================

gdf = gpd.read_file(CONTOUR_PATH)


# =========================================
# LOAD PNG WATERMARK
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
# DASH FIGURE
# =========================================

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


# =========================================
# CONTOURS — SEM PCA / SEM NORMALIZE
# =========================================

for geom in gdf.geometry:
    if geom is None:
        continue

    if geom.geom_type == "LineString":
        xs, ys = geom.xy
        fig.add_trace(
            go.Scatter(
                x=list(xs),
                y=list(ys),
                mode="lines",
                line=dict(width=1, color="black"),
                opacity=0.55,
                showlegend=False,
                hoverinfo="skip",
            )
        )

    elif geom.geom_type == "MultiLineString":
        for line in geom.geoms:
            xs, ys = line.xy
            fig.add_trace(
                go.Scatter(
                    x=list(xs),
                    y=list(ys),
                    mode="lines",
                    line=dict(width=1, color="black"),
                    opacity=0.55,
                    showlegend=False,
                    hoverinfo="skip",
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


# =========================================
# LAYOUT
# =========================================

fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    xaxis=dict(
        visible=False,
        range=[-0.5, cols - 0.5],
        constrain="domain",
    ),
    yaxis=dict(
        visible=False,
        range=[rows - 0.5, -0.5],
        scaleanchor="x",
        scaleratio=1,
    ),
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


# =========================================
# RUN
# =========================================

if __name__ == "__main__":
    print("GRID_PATH:", GRID_PATH)
    print("CONTOUR_PATH:", CONTOUR_PATH)
    print("PNG_PATH:", PNG_PATH)
    print("Grid shape:", rows, cols)
    print("Contours:", len(gdf))
    print("Contour bounds:", gdf.total_bounds)
    app.run(debug=True)
