
import json

PLAN_PATH = "products/latest/actuator_plan.json"

with open(PLAN_PATH, "r") as f:
    PLAN = json.load(f)


"""
IPT-CITYSPACE
Dash — Grid Observador do EventBus (OFICIAL + CONTROLES)

- UI OBSERVADORA
- Controles: Play / Pause / Step / Reset
- Core roda em thread
"""

import threading
import time
from pathlib import Path

import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px

from offline.loading.offline_product import OfflineProduct
from online.core.temporal_conductor import TemporalConductor
from online.core.temporal_state import TemporalState
from online.core.event_bus import EventBus
from online.core.state_manager import StateManager
from online.core.state import State
from online.core.actuator_events import MovePinEvent


# ============================================================
# STATECHART
# ============================================================
class InitState(State):
    name = "INIT"

    def on_event(self, event_type, payload):
        if event_type == "MOVE_PIN":
            return ScanningState()
        return self


class ScanningState(State):
    name = "SCANNING"

    def on_event(self, event_type, payload):
        if event_type == "END_OF_SEQUENCE":
            return EndState()
        return self


class EndState(State):
    name = "END"

    def on_event(self, event_type, payload):
        return self


# ============================================================
# SEQUENCE
# ============================================================
def build_sequence_from_grid(grid):
    seq = []
    idx = 0
    rows, cols = grid.shape

    for y in range(rows):
        xs = range(cols) if y % 2 == 0 else reversed(range(cols))
        for x in xs:
            z = int(grid[y, x])
            seq.append(
                TemporalState(
                    index=idx,
                    x=x,
                    y=y,
                    z_pin_cm=z,
                    z_real_m=z / 100.0,
                    phase="scan",
                )
            )
            idx += 1
    return seq


# ============================================================
# SNAPSHOT
# ============================================================
class Snapshot:
    def __init__(self, rows, cols):
        self.lock = threading.Lock()
        self.grid = np.zeros((rows, cols), float)
        self.current = None
        self.state = "INIT"

    def reset(self):
        with self.lock:
            self.grid[:] = 0.0
            self.current = None
            self.state = "INIT"

    def on_move(self, evt, sm):
        with self.lock:
            self.grid[evt.y, evt.x] = evt.z_real_m
            self.current = (evt.x, evt.y)
            self.state = sm.current_state.name


# ============================================================
# CORE CONTROLLER
# ============================================================
class Core:
    def __init__(self, snapshot):
        self.snapshot = snapshot
        self.running = False
        self.step_once = False

        product = # OfflineProduct REMOVIDO (snapshot antigo)
# # OfflineProduct REMOVIDO (snapshot antigo)
# OfflineProduct(
            Path("offline/products/snapshots/1cm_rotated")
        )
        self.sequence = build_sequence_from_grid(product.grid)

        self.bus = EventBus()
        self.sm = StateManager(event_bus=self.bus)
        self.sm.current_state = InitState()
        self.sm.initialized = True

        self.bus.subscribe(
            "MOVE_PIN",
            lambda e: self.snapshot.on_move(e, self.sm),
        )
        self.bus.subscribe(
            "MOVE_PIN",
            lambda e: self.sm.handle_event(e.event_type, e),
        )

        self.conductor = TemporalConductor(
            bus=self.bus,
            step_delay_s=0.0,
            loop=False,
        )
        self.conductor.load_sequence(self.sequence)

        threading.Thread(target=self.loop, daemon=True).start()

    def loop(self):
        while True:
            if self.running or self.step_once:
                if self.conductor.has_next():
                    self.conductor.step_forward()
                self.step_once = False
            time.sleep(0.05)

    def play(self):
        self.running = True

    def pause(self):
        self.running = False

    def step(self):
        self.step_once = True

    def reset(self):
        self.pause()
        self.conductor.reset()
        self.snapshot.reset()
        self.sm.current_state = InitState()


# ============================================================
# DASH
# ============================================================
def create_app(snapshot, core):
    app = dash.Dash(__name__)

    app.layout = html.Div(
        style={"width": "900px", "margin": "auto"},
        children=[
            html.H2("IPT-CitySpace — Dash Observador (EventBus)"),
            html.Div(id="state-label"),
            dcc.Graph(id="grid"),
            dcc.Store(id="command"),

            html.Div(
                [
                    html.Button("▶ Play", id="play"),
                    html.Button("⏸ Pause", id="pause"),
                    html.Button("⏭ Step", id="step"),
                    html.Button("⟲ Reset", id="reset"),
                ],
                style={"margin": "10px"},
            ),

            dcc.Interval(id="tick", interval=200),
        ],
    )

    # --- UI → COMMAND ---
    @app.callback(
        Output("command", "data"),
        Input("play", "n_clicks"),
        Input("pause", "n_clicks"),
        Input("step", "n_clicks"),
        Input("reset", "n_clicks"),
        prevent_initial_call=True,
    )
    def send_cmd(p, pa, s, r):
        ctx = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
        return ctx

    # --- COMMAND → CORE ---
    @app.callback(
        Output("state-label", "children"),
        Input("command", "data"),
        prevent_initial_call=True,
    )
    def handle_cmd(cmd):
        if cmd == "play":
            core.play()
        elif cmd == "pause":
            core.pause()
        elif cmd == "step":
            core.step()
        elif cmd == "reset":
            core.reset()
        return dash.no_update

    # --- REFRESH VIEW ---
    @app.callback(
        Output("grid", "figure"),
        Output("state-label", "children"),
        Input("tick", "n_intervals"),
    )
    def refresh(_):
        with snapshot.lock:
            grid = snapshot.grid.copy()
            state = snapshot.state
            cur = snapshot.current

        fig = px.imshow(
            grid,
            color_continuous_scale="Viridis",
            labels=dict(x="X", y="Y", color="Altura (m)"),
        )

        if cur:
            fig.add_scatter(
                x=[cur[0]], y=[cur[1]],
                mode="markers",
                marker=dict(color="red", size=12),
            )

        fig.update_layout(
            yaxis_autorange="reversed",
            xaxis=dict(scaleanchor="y", scaleratio=1),
        )

        return fig, f"STATE: {state}"

    return app


# ============================================================
# ENTRYPOINT
# ============================================================
if __name__ == "__main__":
    product = # OfflineProduct REMOVIDO (snapshot antigo)
# # OfflineProduct REMOVIDO (snapshot antigo)
# OfflineProduct(
        Path("offline/products/snapshots/1cm_rotated")
    )
    rows, cols = product.grid.shape

    snapshot = Snapshot(rows, cols)
    core = Core(snapshot)

    app = create_app(snapshot, core)
    app.run(debug=False)
