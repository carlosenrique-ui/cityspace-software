"""
IPT-CITYSPACE
Dash — Sistema de Coordenadas Definitivo

DECISÃO FECHADA:
- (0,0) no canto superior esquerdo
- Y cresce para baixo
- Grid lógico = tela = projeção
"""

from pathlib import Path
import numpy as np

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px

from offline.loading.offline_product import OfflineProduct
from online.core.temporal_state import TemporalState


# ============================================================
# PARÂMETROS GLOBAIS
# ============================================================

FRAME_DT_S = 0.3  # segundos por frame
CELL_SIZE_CM = 1.0  # decisão física alvo (projeção)


# ============================================================
# BUILD SEQUENCE (varredura)
# ============================================================

def build_sequence_from_grid(grid):
    """
    Varredura linha a linha, compatível com:
    - origem no topo
    - Y cresce para baixo
    """
    sequence = []
    index = 0
    rows, cols = grid.shape

    for y in range(rows):
        x_range = range(cols) if y % 2 == 0 else reversed(range(cols))
        for x in x_range:
            z_cm = int(grid[y, x])
            sequence.append(
                TemporalState(
                    index=index,
                    x=x,
                    y=y,
                    z_pin_cm=z_cm,
                    z_real_m=z_cm / 100.0,
                    phase="scan",
                )
            )
            index += 1

    return sequence


# ============================================================
# LOAD SNAPSHOT REAL
# ============================================================

snapshot_path = Path("offline/products/snapshots/1cm_rotated")
product = OfflineProduct(snapshot_path)

GRID_REAL_M = product.grid.astype(float) / 100.0
ROWS, COLS = GRID_REAL_M.shape

SEQUENCE = build_sequence_from_grid(product.grid)
MAX_INDEX = len(SEQUENCE) - 1


# ============================================================
# DASH APP
# ============================================================

app = dash.Dash(__name__)

app.layout = html.Div(
    style={"width": "1000px", "margin": "auto"},
    children=[

        html.H2("IPT-CitySpace — Superfície Física (CSV)"),

        dcc.Graph(
            id="surface-view",
            figure=px.imshow(
                GRID_REAL_M,
                color_continuous_scale="Viridis",
                labels=dict(
                    x="X (célula / cm)",
                    y="Y (célula / cm)",
                    color="Altura (m)",
                ),
            ).update_layout(
                yaxis_autorange="reversed",  # 🔑 ORIGEM NO TOPO
                xaxis=dict(scaleanchor="y", scaleratio=1),
            ),
        ),

        html.Hr(),

        html.H2("Processo Temporal — Varredura da Mesa"),

        dcc.Graph(id="temporal-view"),

        dcc.Slider(
            id="time-slider",
            min=0,
            max=MAX_INDEX,
            step=1,
            value=0,
            marks={
                0: "0 s",
                MAX_INDEX: f"{MAX_INDEX * FRAME_DT_S:.1f} s",
            },
        ),

        html.Div(
            children=[
                html.Button("▶ Play", id="btn-play"),
                html.Button("⏸ Pause", id="btn-pause"),
                html.Button("⏹ Stop", id="btn-stop"),
            ],
            style={"marginTop": "10px"},
        ),

        dcc.Store(id="playing", data=False),
        dcc.Interval(
            id="play-interval",
            interval=int(FRAME_DT_S * 1000),
            disabled=True,
        ),
    ],
)


# ============================================================
# CALLBACK — TEMPORAL VIEW
# ============================================================

@app.callback(
    Output("temporal-view", "figure"),
    Input("time-slider", "value"),
)
def update_temporal_view(frame):
    grid_view = np.zeros((ROWS, COLS), dtype=float)

    for i in range(frame + 1):
        s = SEQUENCE[i]
        grid_view[s.y, s.x] = s.z_real_m

    t_sec = frame * FRAME_DT_S

    fig = px.imshow(
        grid_view,
        color_continuous_scale="Viridis",
        labels=dict(
            x="X (célula / cm)",
            y="Y (célula / cm)",
            color="Altura (m)",
        ),
        title=f"Tempo = {t_sec:.2f} s | Frame {frame}",
    )

    fig.update_layout(
        yaxis_autorange="reversed",   # 🔑 ORIGEM DEFINITIVA
        xaxis=dict(scaleanchor="y", scaleratio=1),
    )

    return fig


# ============================================================
# CALLBACKS — CONTROLES
# ============================================================

@app.callback(
    Output("play-interval", "disabled"),
    Output("playing", "data"),
    Input("btn-play", "n_clicks"),
    Input("btn-pause", "n_clicks"),
    Input("btn-stop", "n_clicks"),
    State("playing", "data"),
)
def control_play(n_play, n_pause, n_stop, playing):
    ctx = dash.callback_context
    if not ctx.triggered:
        return True, playing

    btn = ctx.triggered[0]["prop_id"].split(".")[0]

    if btn == "btn-play":
        return False, True
    if btn == "btn-pause":
        return True, False
    if btn == "btn-stop":
        return True, False

    return True, playing


@app.callback(
    Output("time-slider", "value"),
    Input("play-interval", "n_intervals"),
    State("time-slider", "value"),
)
def advance_time(_, current):
    return min(current + 1, MAX_INDEX)


# ============================================================
# ENTRYPOINT
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)
