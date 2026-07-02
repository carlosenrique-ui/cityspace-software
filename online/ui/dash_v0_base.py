# ==========================================================
# IPT-CitySpace – V0 BASE (GRID REAL CORRIGIDO)
# ==========================================================

import pandas as pd
import dash
from dash import dcc, html
import plotly.graph_objects as go

CSV_PATH = "offline/products/scientific/grid_metrics_utm.csv"

# =========================================
# LOAD REAL DATA
# =========================================
df = pd.read_csv(CSV_PATH)

# 🔥 COLUNA CORRETA
VALUE_COL = "z_total_m"

grid = df.pivot(index="row", columns="col", values=VALUE_COL)

# ordenação consistente
grid = grid.sort_index(ascending=True)
grid = grid.sort_index(axis=1, ascending=True)

print("GRID SHAPE:", grid.shape)

# =========================================
# FIGURE
# =========================================
fig = go.Figure()

fig.add_trace(go.Heatmap(
    z=grid.values,
    colorscale="Viridis"
))

# 🔥 SEM DISTORÇÃO
fig.update_yaxes(scaleanchor="x", scaleratio=1)
fig.update_yaxes(autorange="reversed")

fig.update_layout(
    margin=dict(l=0, r=0, t=20, b=0),
    plot_bgcolor="black",
    paper_bgcolor="black"
)

# =========================================
# DASH
# =========================================
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(
        id="g",
        figure=fig,
        config={"displayModeBar": False},
        style={"height": "90vh"}
    )
])

# =========================================
# RUN
# =========================================
if __name__ == "__main__":
    app.run(debug=False)
