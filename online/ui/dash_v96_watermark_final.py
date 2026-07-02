# =========================================
# DASH V96 – WATERMARK FINAL (SEM DISTORÇÃO)
# =========================================

import numpy as np
import pandas as pd
import dash
from dash import dcc, html
import plotly.graph_objects as go
import base64

# =========================================
# LOAD GRID (NÃO ALTERAR)
# =========================================
df = pd.read_csv(
    "/mnt/c/workspace/ipt-cityspace-engine/ipt_core_clean/offline/products/scientific/grid_metrics_utm.csv"
)

grid = df.pivot(index="row", columns="col", values="z_total_m").values * 100
rows, cols = grid.shape

# =========================================
# LOAD WATERMARK (SEU ARQUIVO CORRETO)
# =========================================
WATERMARK_PATH = "/mnt/c/workspace/ipt-cityspace-engine/backup_git_20260317_191244/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_v3.png"

with open(WATERMARK_PATH, "rb") as f:
    encoded = base64.b64encode(f.read()).decode()

# =========================================
# AJUSTES FINOS (SÓ ISSO VOCÊ VAI MEXER)
# =========================================
SCALE_X = 0.62
SCALE_Y = 0.54

OFFSET_X = -0.035
OFFSET_Y = 0.045

OPACITY = 0.30

# posição final
x0 = (1 - SCALE_X) / 2 + OFFSET_X
y1 = 1 - ((1 - SCALE_Y) / 2 + OFFSET_Y)

# =========================================
# DASH
# =========================================
app = dash.Dash(__name__)

fig = go.Figure()

# HEATMAP (NÃO MEXER)
fig.add_trace(go.Heatmap(z=grid, colorscale="Viridis", showscale=False))

# WATERMARK (SOMENTE POSICIONAMENTO)
fig.add_layout_image(
    dict(
        source=f"data:image/png;base64,{encoded}",
        xref="paper",
        yref="paper",
        x=x0,
        y=y1,
        sizex=SCALE_X,
        sizey=SCALE_Y,
        xanchor="left",
        yanchor="top",
        opacity=OPACITY,
        layer="below",
    )
)

# LAYOUT LIMPO
fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
)

# =========================================
# APP
# =========================================
app.layout = html.Div([dcc.Graph(figure=fig, config={"displayModeBar": False})])

if __name__ == "__main__":
    app.run(debug=True)
