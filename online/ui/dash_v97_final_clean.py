from __future__ import annotations

import json
from pathlib import Path

import dash
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, State, ctx, dcc, html

# ============================================================
# IPT-CITYSPACE | ONLINE/UI | DASH V97 FINAL CLEAN
# Baseline evoluído a partir do V96
# - prioriza runtime oficial
# - fallback para produtos legados
# - mantém player simples
# - mantém watermark
# - mantém highlight da célula ativa
# ============================================================

# ------------------------------------------------------------
# PATHS BASE
# ------------------------------------------------------------
ENGINE_ROOT = Path("/mnt/c/workspace/ipt-cityspace-engine")
CORE_ROOT = ENGINE_ROOT / "ipt_core_clean"

OFFICIAL_RUNTIME_DIR = CORE_ROOT / "offline" / "products" / "runtime"
OFFICIAL_SCIENTIFIC_DIR = CORE_ROOT / "offline" / "products" / "scientific"
OFFICIAL_ASSETS_DIR = CORE_ROOT / "online" / "assets"

LEGACY_PRODUCTS_DIR = ENGINE_ROOT / "products" / "final"
LEGACY_ASSETS_DIR = ENGINE_ROOT / "assets"

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8050

ROWS = 8
COLS = 16
NX = COLS
NY = ROWS


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------
def _print_header(title: str) -> None:
    print("\n" + "=" * 60, flush=True)
    print(title, flush=True)
    print("=" * 60, flush=True)


def _resolve_asset_image() -> str | None:
    """
    Retorna o caminho do asset de watermark, priorizando o online/assets oficial.
    O Plotly aceita string path local.
    """
    candidates = [
        OFFICIAL_ASSETS_DIR / "ipt_mask_rotated_simple.png",
        LEGACY_ASSETS_DIR / "ipt_mask_rotated_simple.png",
    ]

    for path in candidates:
        if path.exists():
            print(f"[OK] watermark encontrada: {path}", flush=True)
            return str(path)

    print("[WARN] watermark não encontrada em nenhum path conhecido.", flush=True)
    return None


def _load_runtime_grid() -> np.ndarray | None:
    """
    Prioriza runtime oficial:
    - grid.npy
    """
    grid_npy = OFFICIAL_RUNTIME_DIR / "grid.npy"

    if grid_npy.exists():
        print(f"[OK] carregando runtime grid: {grid_npy}", flush=True)
        arr = np.load(grid_npy)
        arr = np.asarray(arr, dtype=float)

        if arr.ndim != 2:
            raise ValueError(f"grid.npy deve ser 2D, shape atual={arr.shape}")

        arr = arr[:ROWS, :COLS]

        if arr.shape[0] < ROWS or arr.shape[1] < COLS:
            padded = np.full((ROWS, COLS), np.nan, dtype=float)
            padded[: arr.shape[0], : arr.shape[1]] = arr
            arr = padded

        return arr

    print("[WARN] grid.npy oficial não encontrado.", flush=True)
    return None


def _load_legacy_grid() -> np.ndarray | None:
    """
    Fallback legado:
    - products/final/grid_height.csv
    """
    grid_csv = LEGACY_PRODUCTS_DIR / "grid_height.csv"

    if not grid_csv.exists():
        print("[WARN] grid_height.csv legado não encontrado.", flush=True)
        return None

    print(f"[OK] carregando grid legado: {grid_csv}", flush=True)
    df = pd.read_csv(grid_csv)

    required = {"row", "col", "z_cm"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"grid_height.csv sem colunas obrigatórias: {sorted(missing)}")

    grid = (
        df.pivot(index="row", columns="col", values="z_cm")
        .reindex(index=range(ROWS), columns=range(COLS))
        .values
    )

    return np.asarray(grid, dtype=float)


def load_base_grid() -> np.ndarray:
    """
    Carrega grid base preferencialmente do runtime oficial.
    Fallback para legado.
    """
    grid = _load_runtime_grid()
    if grid is not None:
        return grid

    grid = _load_legacy_grid()
    if grid is not None:
        return grid

    raise FileNotFoundError(
        "Nenhum grid encontrado. Verifique runtime oficial ou legado."
    )


def _load_official_plan() -> dict | list | None:
    plan_json = OFFICIAL_RUNTIME_DIR / "actuator_plan.json"
    if plan_json.exists():
        print(f"[OK] carregando actuator_plan oficial: {plan_json}", flush=True)
        with open(plan_json, "r", encoding="utf-8") as f:
            return json.load(f)

    print("[WARN] actuator_plan oficial não encontrado.", flush=True)
    return None


def _load_legacy_plan() -> dict | list | None:
    plan_json = LEGACY_PRODUCTS_DIR / "actuator_plan.json"
    if plan_json.exists():
        print(f"[OK] carregando actuator_plan legado: {plan_json}", flush=True)
        with open(plan_json, "r", encoding="utf-8") as f:
            return json.load(f)

    print("[WARN] actuator_plan legado não encontrado.", flush=True)
    return None


def load_plan_events() -> list[dict]:
    raw = _load_official_plan()
    if raw is None:
        raw = _load_legacy_plan()

    if raw is None:
        raise FileNotFoundError(
            "Nenhum actuator_plan.json encontrado no runtime oficial nem no legado."
        )

    events = raw.get("events", raw) if isinstance(raw, dict) else raw

    if not isinstance(events, list):
        raise ValueError(
            "actuator_plan deve ser uma lista de eventos ou dict com key 'events'."
        )

    print(f"[OK] total de eventos carregados: {len(events)}", flush=True)
    return events


def build_timeline(
    events: list[dict],
) -> tuple[list[tuple[int, int]], list[float], list[float]]:
    """
    Constrói:
    - p = lista de posições (row, col)
    - v = lista de alturas
    - tl = timeline acumulada
    """
    positions: list[tuple[int, int]] = []
    heights: list[float] = []

    pos = (0, 0)

    for event in events:
        event_type = event.get("type")

        if event_type == "move":
            row = int(event.get("row", 0))
            col = int(event.get("col", 0))
            pos = (min(max(row, 0), ROWS - 1), min(max(col, 0), COLS - 1))

        elif event_type == "set_height_cm":
            value_cm = float(event.get("value_cm", 0.0))
            positions.append(pos)
            heights.append(value_cm)

    if not positions:
        print("[WARN] timeline vazia: nenhum set_height_cm encontrado.", flush=True)
        return [], [], [0.0]

    def manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    tl = [0.0]
    for i in range(1, len(positions)):
        move_cost = 0.2 * manhattan(positions[i - 1], positions[i])
        height_cost = 0.12 * abs(heights[i])
        tl.append(tl[-1] + move_cost + height_cost)

    return positions, heights, tl


def get_step_index(current_time: float, timeline: list[float]) -> int:
    for i, t in enumerate(timeline):
        if t >= current_time:
            return i
    return max(0, len(timeline) - 1)


# ------------------------------------------------------------
# DATA LOAD
# ------------------------------------------------------------
_print_header(">>> IPT-CITYSPACE V97 | LOAD DATA <<<")

BASE_GRID = load_base_grid()
EVENTS = load_plan_events()
P, V, TL = build_timeline(EVENTS)

TMAX = TL[-1] if TL else 0.0
WATERMARK_PATH = _resolve_asset_image()

print(f"[OK] BASE_GRID shape = {BASE_GRID.shape}", flush=True)
print(f"[OK] steps timeline = {len(P)}", flush=True)
print(f"[OK] TMAX = {TMAX:.3f}", flush=True)

# ------------------------------------------------------------
# APP
# ------------------------------------------------------------
app = dash.Dash(__name__, assets_folder=str(OFFICIAL_ASSETS_DIR))

app.layout = html.Div(
    [
        dcc.Graph(
            id="graph",
            config={"displayModeBar": False},
            style={"width": "100%", "height": "85vh"},
        ),
        html.Div(
            [
                html.Button("<<", id="back", n_clicks=0),
                html.Button("Play", id="play", n_clicks=0),
                html.Button("Pause", id="pause", n_clicks=0),
                html.Button(">>", id="fwd", n_clicks=0),
            ],
            style={
                "textAlign": "center",
                "display": "flex",
                "justifyContent": "center",
                "gap": "12px",
                "padding": "10px 0",
            },
        ),
        dcc.Interval(id="interval", interval=60, n_intervals=0),
        dcc.Store(id="time", data=0.0),
        dcc.Store(id="running", data=False),
        dcc.Store(id="direction", data=1),
    ],
    style={
        "width": "100%",
        "height": "100vh",
        "margin": "0",
        "padding": "0",
        "overflow": "hidden",
        "backgroundColor": "white",
    },
)


# ------------------------------------------------------------
# CALLBACKS
# ------------------------------------------------------------
@app.callback(
    Output("running", "data"),
    Input("play", "n_clicks"),
    Input("pause", "n_clicks"),
    State("running", "data"),
    prevent_initial_call=True,
)
def cb_running(play_clicks: int, pause_clicks: int, current_running: bool) -> bool:
    trig = ctx.triggered_id
    if trig == "play":
        return True
    if trig == "pause":
        return False
    return current_running


@app.callback(
    Output("direction", "data"),
    Input("fwd", "n_clicks"),
    Input("back", "n_clicks"),
    State("direction", "data"),
    prevent_initial_call=True,
)
def cb_direction(fwd_clicks: int, back_clicks: int, current_direction: int) -> int:
    trig = ctx.triggered_id
    if trig == "back":
        return -1
    if trig == "fwd":
        return 1
    return current_direction


@app.callback(
    Output("time", "data"),
    Input("interval", "n_intervals"),
    State("running", "data"),
    State("direction", "data"),
    State("time", "data"),
)
def cb_time(
    n_intervals: int, running: bool, direction: int, current_time: float
) -> float:
    if not running:
        return current_time

    dt = 0.05
    next_time = current_time + direction * dt
    return max(0.0, min(TMAX, next_time))


@app.callback(Output("graph", "figure"), Input("time", "data"))
def cb_render(current_time: float) -> go.Figure:
    step = get_step_index(current_time, TL)

    z = np.zeros((NY, NX), dtype=float)

    for i, (row, col) in enumerate(P):
        if i <= step:
            z[row, col] = V[i]

    fig = go.Figure()

    if WATERMARK_PATH is not None:
        fig.update_layout(
            images=[
                dict(
                    source=WATERMARK_PATH,
                    xref="x",
                    yref="y",
                    x=-0.52,
                    y=-0.85,
                    sizex=NX,
                    sizey=NY,
                    sizing="stretch",
                    opacity=0.35,
                    layer="below",
                )
            ]
        )

    fig.add_trace(
        go.Heatmap(
            z=z,
            colorscale="Jet",
            zmin=0,
            zmax=10,
            xgap=1,
            ygap=1,
            opacity=0.65,
            showscale=False,
        )
    )

    if P and step < len(P):
        row, col = P[step]
        fig.add_shape(
            type="rect",
            x0=col - 0.5,
            y0=row - 0.5,
            x1=col + 0.5,
            y1=row + 0.5,
            line=dict(color="white", width=2),
            fillcolor="rgba(255,255,255,0.25)",
        )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(
            range=[-0.5, NX - 0.5],
            visible=False,
            constrain="domain",
        ),
        yaxis=dict(
            range=[NY - 0.5, -0.5],
            visible=False,
            scaleanchor="x",
            scaleratio=1,
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    return fig


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
if __name__ == "__main__":
    _print_header(">>> V97 FINAL CLEAN <<<")
    print(f"[OK] host={DEFAULT_HOST} port={DEFAULT_PORT}", flush=True)
    app.run(host=DEFAULT_HOST, port=DEFAULT_PORT, debug=False)
