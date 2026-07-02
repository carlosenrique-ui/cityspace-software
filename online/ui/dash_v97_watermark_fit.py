# =========================================
# DASH V97 – WATERMARK FIT (SEM CORTAR / SEM DEGRADAR)
# =========================================

import base64
import numpy as np
import pandas as pd
from io import BytesIO
from PIL import Image
import dash
from dash import dcc, html
import plotly.graph_objects as go

# =========================================
# CONFIG
# =========================================

PNG_PATH = "/mnt/c/workspace/ipt-cityspace-engine/backup_git_20260317_191244/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_v3.png"

ROTATION_DEG = -7.20  # ajuste fino
SCALE = 0.62  # escala do urbanismo (não do papel)
OFFSET_X = -0.03  # esquerda/direita
OFFSET_Y = +0.06  # sobe/desce

# =========================================
# LOAD GRID
# =========================================

df = pd.read_csv(
    "/mnt/c/workspace/ipt-cityspace-engine/ipt_core_clean/offline/products/scientific/grid_metrics_utm.csv"
)

grid = df.pivot(index="row", columns="col", values="z_total_m").values
rows, cols = grid.shape

# =========================================
# LOAD + CROP AUTOMÁTICO DO PNG
# =========================================

img = Image.open(PNG_PATH).convert("RGBA")

# remove fundo claro (crop automático)
np_img = np.array(img)

mask = np_img[:, :, 0:3].mean(axis=2) < 240  # remove branco/cinza claro

coords = np.argwhere(mask)

y0, x0 = coords.min(axis=0)
y1, x1 = coords.max(axis=0)

img = img.crop((x0, y0, x1, y1))

# =========================================
# ROTATE (SEM CORTAR)
# =========================================

img = img.rotate(ROTATION_DEG, expand=True)

# =========================================
# ENCODE
# =========================================

buf = BytesIO()
img.save(buf, format="PNG")
encoded = base64.b64encode(buf.getvalue()).decode()

# =========================================
# DASH
# =========================================

app = dash.Dash(__name__)

fig = go.Figure()

# HEATMAP (pinos)
fig.add_trace(
    go.Heatmap(
        z=grid,
        colorscale="Viridis",
        showscale=False,
        xgap=0,
        ygap=0,
    )
)

# WATERMARK (agora sem "papel")
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
        opacity=0.28,
        layer="below",
    )
)

# LAYOUT LIMPO
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
