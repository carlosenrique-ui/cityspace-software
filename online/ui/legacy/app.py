# online/ui/app.py

from dash import Dash, html, dcc, Input, Output
import dash_leaflet as dl

# === CORE =====================================================
from online.core.event_bus import EventBus
from online.core.temporal_state import TemporalState
from online.core.temporal_conductor import TemporalConductor

# === ACTUATOR + ADAPTER ======================================
from online.actuators.visual_actuator import VisualActuator
from online.ui.visual_adapter import VisualAdapter

# =============================================================
# Infraestrutura mínima ONLINE (mock)
# =============================================================
bus = EventBus()
visual = VisualActuator(bus)
adapter = VisualAdapter(visual)

conductor = TemporalConductor(bus)

# =============================================================
# Sequência temporal dummy (16 pinos)
# =============================================================
sequence = [
    TemporalState(
        index=i,
        phase="P1",
        x=i % 4,
        y=i // 4,
        z_real_m=0.1 * (i % 4),
        z_pin_cm=5 + (i % 4) * 5,
    )
    for i in range(16)
]

conductor.load_sequence(sequence)

# =============================================================
# Conversão GRID → MAPA (simples e previsível)
# =============================================================
def grid_to_latlon(x, y):
    """
    Conversão simples:
    grid (0,0) = canto superior direito
    """
    lat0 = -23.55
    lon0 = -46.65

    cell_deg = 0.0002  # escala visual (ajustável depois)

    lat = lat0 - y * cell_deg
    lon = lon0 + x * cell_deg

    return lat, lon

# =============================================================
# APP
# =============================================================
app = Dash(__name__)

app.layout = html.Div(
    style={"padding": "10px"},
    children=[
        html.H3("IPT CitySpace – Visualização de Pinos"),

        # -----------------------
        # CONTROLES
        # -----------------------
        html.Div([
            html.Button("⏵ PLAY", id="btn-play", n_clicks=0),
            html.Button("⏸ PAUSE", id="btn-pause", n_clicks=0),
            html.Button("⏹ STOP", id="btn-stop", n_clicks=0),
        ], style={"marginBottom": "10px"}),

        dcc.Slider(
            id="timeline-slider",
            min=0,
            max=len(sequence) - 1,
            step=1,
            value=0,
        ),

        # -----------------------
        # MAPA
        # -----------------------
        dl.Map(
            center=[-23.55, -46.65],
            zoom=16,
            style={"width": "100%", "height": "60vh"},
            children=[
                dl.TileLayer(),
                dl.LayerGroup(id="pins-layer"),
            ]
        ),

        html.Pre(id="debug", style={"marginTop": "10px"}),
    ]
)

# =============================================================
# CALLBACKS
# =============================================================

@app.callback(
    Output("pins-layer", "children"),
    Output("debug", "children"),
    Input("timeline-slider", "value"),
)
def update_pins(idx):
    conductor.seek(idx)

    pins = adapter.get_pins()

    circles = []
    for pin in pins:
        lat, lon = grid_to_latlon(pin["x"], pin["y"])

        circles.append(
            dl.CircleMarker(
                center=[lat, lon],
                radius=pin["z_pin_cm"],  # altura → raio
                color="red",
                fill=True,
                fillOpacity=0.6,
            )
        )

    return circles, f"Pinos ativos: {len(pins)} | frame={idx}"


@app.callback(
    Output("timeline-slider", "value"),
    Input("btn-play", "n_clicks"),
    Input("btn-pause", "n_clicks"),
    Input("btn-stop", "n_clicks"),
    Input("timeline-slider", "value"),
)
def control_player(play, pause, stop, current):
    ctx = dcc.callback_context
    if not ctx.triggered:
        return current

    btn = ctx.triggered[0]["prop_id"].split(".")[0]

    if btn == "btn-play":
        conductor.play()
    elif btn == "btn-pause":
        conductor.pause()
    elif btn == "btn-stop":
        conductor.stop()
        return 0

    return current

# =============================================================
# RUN
# =============================================================
if __name__ == "__main__":
    app.run(debug=True)
