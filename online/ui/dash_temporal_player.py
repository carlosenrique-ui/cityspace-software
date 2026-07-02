"""
IPT-CITYSPACE
Dash — Observador com TemporalPlayer (Opção C)

- UI NÃO controla tempo diretamente
- UI chama TemporalPlayer
- TemporalPlayer roda em thread
- Grid observa EventBus
"""

import threading
from pathlib import Path

import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# ===============================
# CORE
# ===============================
from offline.loading.offline_product import OfflineProduct

from online.core.event_bus import EventBus
from online.core.temporal_state import TemporalState
from online.core.temporal_conductor import TemporalConductor
from online.core.temporal_player import TemporalPlayer
from online.core.actuator_events import MovePinEvent


# ===============================
# BUILD SEQUENCE
# ===============================
def build_sequence_from_grid(grid):
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
                    phase="SCAN",
                    x=x,
                    y=y,
                    z_real_m=z_cm / 100.0,
                    z_pin_cm=z_cm,
                )
            )
            index += 1

    return sequence


# ===============================
# EVENT SNAPSHOT (OBSERVADOR)
# ===============================
class EventSnapshot:
    def __init__(self, rows, cols):
        self.lock = threading.Lock()
        self.grid = np.zeros((rows, cols), dtype=float)

    def on_move_pin(self, event: MovePinEvent):
        with self.lock:
            self.grid[event.y, event.x] = event.z_real_m


# ===============================
# SETUP CORE
# ===============================
snapshot_path = Path("offline/products/snapshots/1cm_rotated")
product = OfflineProduct(snapshot_path)

grid = product.grid
rows, cols = grid.shape

sequence = build_sequence_from_grid(grid)

bus = EventBus()
snapshot = EventSnapshot(rows, cols)

bus.subscribe(
    "MOVE_PIN",
    lambda evt: snapshot.on_move_pin(evt),
)

conductor = TemporalConductor(
    bus=bus,
    step_delay_s=0.05,
    loop=False,
)

conductor.load_sequence(sequence)

player = TemporalPlayer(conductor)

# ===============================
# DASH APP
# ===============================
app = dash.Dash(__name__)

app.layout = html.Div(
    style={"width": "900px", "margin": "auto"},
    children=[
        html.H2("IPT-CitySpace — Dash + TemporalPlayer"),

        dcc.Graph(id="grid-view"),

        html.Div(
            children=[
                html.Button("▶ Play", id="btn-play"),
                html.Button("⏸ Pause", id="btn-pause"),
                html.Button("⏹ Stop", id="btn-stop"),
                html.Button("⏭ Step", id="btn-step", disabled=False),
            ],
            style={"marginTop": "10px"},
        ),

        html.Div(
            id="player-status",
            style={
                "marginTop": "15px",
                "padding": "8px",
                "border": "1px solid #ccc",
                "fontFamily": "monospace",
                "whiteSpace": "pre-line",
            },
        ),

        # 🔑 Interval observa heartbeat
        dcc.Interval(id="refresh", interval=200),
    ],
)


# ===============================
# CALLBACK — CONTROLES
# ===============================
@app.callback(
    Output("btn-play", "n_clicks"),
    Input("btn-play", "n_clicks"),
    Input("btn-pause", "n_clicks"),
    Input("btn-stop", "n_clicks"),
    Input("btn-step", "n_clicks"),
    prevent_initial_call=True,
)
def control_buttons(play, pause, stop, step):
    ctx = dash.callback_context
    btn = ctx.triggered[0]["prop_id"].split(".")[0]

    if btn == "btn-play":
        player.play()
    elif btn == "btn-pause":
        player.pause()
    elif btn == "btn-stop":
        player.stop()
    elif btn == "btn-step":
        player.step_forward()

    return play


# ===============================
# CALLBACK — GRID VIEW
# ===============================
@app.callback(
    Output("grid-view", "figure"),
    Input("refresh", "n_intervals"),
)
def update_view(_):
    player.get_tick()  # heartbeat observacional

    with snapshot.lock:
        grid_view = snapshot.grid.copy()

    fig = px.imshow(
        grid_view,
        color_continuous_scale="Viridis",
        labels=dict(
            x="X",
            y="Y",
            color="Altura (m)",
        ),
    )

    fig.update_layout(
        yaxis_autorange="reversed",
        xaxis=dict(scaleanchor="y", scaleratio=1),
    )

    return fig


# ===============================
# CALLBACK — STATUS DO PLAYER
# ===============================
@app.callback(
    Output("player-status", "children"),
    Input("refresh", "n_intervals"),
)
def update_player_status(_):
    tick = player.get_tick()

    thread_alive = (
        player._thread is not None
        and player._thread.is_alive()
    )

    status = "PLAYING" if thread_alive else "IDLE"

    return (
        "TemporalPlayer STATUS\n"
        f"- Estado: {status}\n"
        f"- Heartbeat (tick): {tick}\n"
    )


# ===============================
# CALLBACK — DESABILITAR STEP DURANTE PLAY
# ===============================
@app.callback(
    Output("btn-step", "disabled"),
    Input("refresh", "n_intervals"),
)
def disable_step_when_playing(_):
    return (
        player._thread is not None
        and player._thread.is_alive()
    )


# ===============================
# ENTRYPOINT
# ===============================
if __name__ == "__main__":
    app.run(debug=False)
