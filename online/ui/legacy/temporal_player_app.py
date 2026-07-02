# online/ui/temporal_player_app.py

import json
import dash
from dash import html, dcc, Input, Output, State

from online.core.event_bus import EventBus
from online.contracts.temporal_event import TemporalEvent, TemporalEventType
from online.time.temporal_conductor import TemporalConductor
from online.time.construction_timeline import ConstructionTimeline
from online.renderers.renderer2d import Renderer2D
from online.actuators.virtual_actuator import VirtualActuator


# =========================================================
# Infraestrutura do sistema
# =========================================================

bus = EventBus()

timeline = ConstructionTimeline()
timeline.add_event(1, "create", "Building_A")
timeline.add_event(2, "create", "Building_B")
timeline.add_event(3, "update", "Building_B")
timeline.add_event(4, "remove", "Building_A")

actuator = VirtualActuator()
renderer = Renderer2D(actuator)

conductor = TemporalConductor(
    timeline=timeline,
    renderer=renderer,
    start_t=0,
    end_t=5,
    fps=1.0
)

# EventBus → Player
bus.subscribe(TemporalEventType.STEP_FORWARD, conductor.handle_event)
bus.subscribe(TemporalEventType.STEP_BACKWARD, conductor.handle_event)
bus.subscribe(TemporalEventType.SEEK, conductor.handle_event)


# =========================================================
# App Dash
# =========================================================

app = dash.Dash(__name__)
app.title = "IPT-CitySpace — Player Temporal (Demo)"

app.layout = html.Div(
    style={"fontFamily": "Arial", "padding": "20px"},
    children=[
        html.H2("IPT-CitySpace — Player Temporal (Demonstração)"),

        html.Div(
            style={"marginBottom": "15px"},
            children=[
                html.Button("◀ Step -1", id="btn-back"),
                html.Button("Step +1 ▶", id="btn-forward"),
            ],
        ),

        dcc.Slider(
            id="time-slider",
            min=0,
            max=5,
            step=1,
            value=0,
            marks={i: f"t={i}" for i in range(6)},
        ),

        html.H4("Estado da Mesa Virtual"),
        html.Pre(
            id="state-output",
            style={
                "background": "#f5f5f5",
                "padding": "10px",
                "border": "1px solid #ccc",
                "minHeight": "120px",
            },
        ),

        dcc.Store(id="current-time", data=0),
    ],
)


# =========================================================
# Callbacks
# =========================================================

@app.callback(
    Output("current-time", "data"),
    Input("btn-forward", "n_clicks"),
    Input("btn-back", "n_clicks"),
    Input("time-slider", "value"),
    State("current-time", "data"),
    prevent_initial_call=True,
)
def control_time(n_fwd, n_back, slider_t, current_t):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]["prop_id"]

    if "btn-forward" in trigger:
        bus.emit(TemporalEvent(event_type=TemporalEventType.STEP_FORWARD))
        return conductor.t

    if "btn-back" in trigger:
        bus.emit(TemporalEvent(event_type=TemporalEventType.STEP_BACKWARD))
        return conductor.t

    if "time-slider" in trigger:
        bus.emit(TemporalEvent(event_type=TemporalEventType.SEEK, t=slider_t))
        return slider_t

    return current_t


@app.callback(
    Output("state-output", "children"),
    Input("current-time", "data"),
)
def update_state(_):
    return json.dumps(actuator.snapshot(), indent=2)


# =========================================================
# Run (DASH NOVO)
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)
