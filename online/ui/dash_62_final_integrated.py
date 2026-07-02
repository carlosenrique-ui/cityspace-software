import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import json
from pathlib import Path

# =========================================
# CONFIG
# =========================================

ROWS = 8
COLS = 16

PLAN_PATH = Path("products/final/actuator_plan.json")
CSV_PATH = Path("products/final/grid_height.csv")

# =========================================
# LOAD DATA (PIPELINE FINAL)
# =========================================

EVENTS = []
GRID = np.zeros((ROWS, COLS))

# ---- LOAD ACTUATOR PLAN
try:
    with open(PLAN_PATH, "r") as f:
        raw = json.load(f)
        EVENTS = raw.get("events", raw)
    print(f"[UI] Loaded actuator plan: {len(EVENTS)} events")
except Exception as e:
    print(f"[UI] ERROR loading actuator plan: {e}")

# ---- LOAD GRID CSV
try:
    df = pd.read_csv(CSV_PATH)

    # usa altura total em metros
    GRID = df.pivot(index="row", columns="col", values="z_total_m") \
             .sort_index(ascending=True) \
             .values

    print(f"[UI] Grid loaded: {GRID.shape}")

except Exception as e:
    print(f"[UI] ERROR loading grid: {e}")
    GRID = np.zeros((ROWS, COLS))

# =========================================
# BUILD GRID FROM EVENTS (ZIGZAG)
# =========================================

def build_grid(events, step):
    grid = np.zeros((ROWS, COLS))
    r, c = 0, 0

    for e in events[:step]:
        if e.get("type") == "move":
            r = e.get("row", r)
            c = e.get("col", c)

        elif e.get("type") == "set_height_cm":
            grid[r][c] = e.get("value_cm", 0) / 100.0  # cm → m

    return grid

# =========================================
# DASH APP
# =========================================

app = dash.Dash(__name__)

app.layout = html.Div([

    html.H2("IPT CitySpace – V62 FINAL"),

    dcc.Graph(id="grid"),

    dcc.Slider(
        id="step",
        min=0,
        max=max(len(EVENTS), 1),
        step=1,
        value=len(EVENTS),
        tooltip={"placement": "bottom"}
    )

])

# =========================================
# CALLBACK
# =========================================

@app.callback(
    Output("grid", "figure"),
    Input("step", "value")
)
def update(step):

    # usa eventos (temporal)
    if EVENTS:
        z = build_grid(EVENTS, step)
    else:
        z = GRID

    fig = go.Figure()

    fig.add_trace(go.Heatmap(
        z=z,
        colorscale="Viridis",
        colorbar=dict(title="Altura (m)")
    ))

    fig.update_layout(
        title=f"Altura Total (m) – Step {step}",
        xaxis_title="Colunas",
        yaxis_title="Linhas",
        yaxis_autorange="reversed",

        # 🔥 GRID QUADRADO
        width=800,
        height=800
    )

    return fig

# =========================================
# MAIN
# =========================================

if __name__ == "__main__":
    app.run(debug=True, port=8050)