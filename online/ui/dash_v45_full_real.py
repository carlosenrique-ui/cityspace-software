# ==========================================================
# IPT-CitySpace – V45 FULL REAL DIGITAL TWIN
# (zigzag + motion + acumulativo + eixo + base física)
# ==========================================================

import base64
import io
import math
import numpy as np
import matplotlib.pyplot as plt

import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State

# =========================================
# CONFIG (trocar depois pelos CSV reais)
# =========================================

ROWS = 8
COLS = 16

ALTURA_MAX_PINO = 0.10

grid = np.random.rand(ROWS, COLS) * ALTURA_MAX_PINO
grid_z = np.random.rand(ROWS, COLS) * 40

estado_global = np.zeros_like(grid)

anos = np.linspace(1940, 2015, COLS).astype(int)

# =========================================
# FASES
# =========================================

FASES = [
    (1940, 1959, "Implantação na USP", "#2E86C1"),
    (1960, 1979, "Expansão", "#239B56"),
    (1980, 1999, "Consolidação", "#C0392B"),
    (2000, 2015, "Inovação", "#E67E22"),
]

def get_fase(ano):
    for i, f, nome, cor in FASES:
        if i <= ano <= f:
            return nome, cor, f"{i}-{f}"
    return "Fase", "#444", ""

# =========================================
# ZIGZAG REAL
# =========================================

def zigzag(rows, cols):
    traj = []
    for x in range(cols):
        ys = range(rows) if x % 2 == 0 else range(rows - 1, -1, -1)
        for y in ys:
            traj.append((x, y))
    return traj

traj = zigzag(ROWS, COLS)

# =========================================
# MOTION PROFILE (mais realista)
# =========================================

def motion_steps(h):

    steps_up = 20
    steps_down = 10

    subida = np.linspace(0, h, steps_up)
    descida = np.linspace(h, 0, steps_down)

    return list(subida) + list(descida)

# =========================================
# RUNTIME ENGINE
# =========================================

class Runtime:

    def __init__(self):
        self.t_global = 0
        self.t_local = 0
        self.steps = []
        self.estado = np.zeros_like(grid)

    def step(self):

        if self.t_global >= len(traj):
            return self.estado

        x, y = traj[self.t_global]
        altura = grid[y, x]

        # gerar steps de subida/descida
        if self.t_local == 0:
            self.steps = motion_steps(altura)

        h = self.steps[self.t_local]

        # 🔥 acumulativo real (não pisca)
        self.estado[y, x] = max(self.estado[y, x], h)

        self.t_local += 1

        # terminou célula → próxima
        if self.t_local >= len(self.steps):
            self.t_local = 0
            self.t_global += 1

        return self.estado

runtime = Runtime()

# =========================================
# RENDER (EQUIVALENTE AO SEU)
# =========================================

def render_frame(estado):

    fig, ax = plt.subplots(figsize=(12,6))

    # =========================================
    # 🔥 RASTER PLACEHOLDER (trocar depois)
    # =========================================
    raster = np.ones_like(estado) * 0.5

    ax.imshow(
        raster,
        cmap="gray",
        alpha=0.2,
        extent=(-0.5, COLS-0.5, ROWS-0.5, -0.5),
        zorder=0
    )

    # GRID
    im = ax.imshow(
        estado,
        cmap="viridis",
        origin="upper",
        vmin=0,
        vmax=ALTURA_MAX_PINO,
        alpha=0.85,
        zorder=1
    )

    # =========================================
    # TÍTULO + FASE
    # =========================================

    col_idx = min(runtime.t_global, COLS-1)
    ano = anos[col_idx]

    fase_nome, fase_cor, periodo = get_fase(ano)

    ax.set_title(
        f"IPT – CitySpace | {fase_nome} ({periodo})",
        fontsize=18,
        color=fase_cor
    )

    # =========================================
    # EIXO X DINÂMICO
    # =========================================

    visible = min(runtime.t_global + 1, COLS)

    ax.set_xticks(range(visible))
    ax.set_xticklabels(anos[:visible])

    ax.set_xlabel("Av. Escola Politécnica →", fontsize=14)
    ax.set_ylabel("USP →", fontsize=12)

    # =========================================
    # COLORBAR PISO/TETO
    # =========================================

    cbar = plt.colorbar(im, ax=ax, fraction=0.04, pad=0.03)

    ticks = np.linspace(0, ALTURA_MAX_PINO, 6)
    labels = []

    for tck in ticks:
        teto = (tck / ALTURA_MAX_PINO) * grid_z.max()
        labels.append(f"{tck:.2f} / {teto:.2f}")

    cbar.set_ticks(ticks)
    cbar.set_ticklabels(labels)
    cbar.set_label("Pino / Teto (m)")

    # =========================================
    # EXPORT FRAME
    # =========================================

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)

    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

# =========================================
# DASH UI
# =========================================

app = dash.Dash(__name__)

app.layout = html.Div([

    html.H2("IPT CitySpace – Digital Twin V45"),

    html.Img(id="frame", style={"width":"100%"}),

    html.Div([
        html.Button("⏮ Backward", id="back"),
        html.Button("⏯ Play/Pause", id="play"),
        html.Button("⏭ Forward", id="forward"),
        html.Button("🔌 Mesa Física OFF", id="mesa")
    ]),

    dcc.Interval(id="clock", interval=60, disabled=True),

    dcc.Store(id="playing", data=False),
    dcc.Store(id="mesa_on", data=False)
])

# =========================================
# CONTROLES
# =========================================

@app.callback(
    Output("clock", "disabled"),
    Output("playing", "data"),
    Input("play", "n_clicks"),
    State("playing", "data"),
    prevent_initial_call=True
)
def toggle_play(n, playing):
    playing = not playing
    return not playing, playing

@app.callback(
    Output("mesa", "children"),
    Output("mesa_on", "data"),
    Input("mesa", "n_clicks"),
    State("mesa_on", "data"),
    prevent_initial_call=True
)
def toggle_mesa(n, estado):
    estado = not estado
    return ("🔌 Mesa Física ON" if estado else "🔌 Mesa Física OFF"), estado

# =========================================
# LOOP PRINCIPAL
# =========================================

@app.callback(
    Output("frame", "src"),
    Input("clock", "n_intervals")
)
def update(n):
    estado = runtime.step()
    return render_frame(estado)

# =========================================

if __name__ == "__main__":
    app.run(debug=True)