from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
from PIL import Image

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go

from shapely.ops import unary_union, transform
from shapely.geometry import Polygon, MultiPolygon
from shapely.affinity import scale, rotate, translate


THIS_FILE = Path(__file__).resolve()
CORE_ROOT = THIS_FILE.parents[2]
PROJECT_ROOT = CORE_ROOT.parent

CSV_PATH = CORE_ROOT / "offline/products/scientific/grid_metrics_utm.csv"

PNG_CANDIDATES = [
    CORE_ROOT / "offline/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_final.png",
    PROJECT_ROOT / "offline/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_final.png",
]

POLYGON_CANDIDATES = [
    CORE_ROOT / "offline/products/scientific/poligono_urbanismo_ipt_outer_real.gpkg",
    CORE_ROOT / "offline/products/scientific/urban_envelope_scientific_rotated_clean.gpkg",
    CORE_ROOT / "offline/products/scientific/urban_envelope_scientific_rotated.gpkg",
    CORE_ROOT / "offline/products/scientific/urban_envelope_scientific.gpkg",
]

GRID_ROWS = 8
GRID_COLS = 16

OFFSET_X = -0.90
OFFSET_Y = -0.10
PNG_SCALE_X = 0.76
PNG_SCALE_Y = 0.60
PNG_OPACITY = 0.80
GRID_OPACITY = 0.86


def first_existing(paths):
    for p in paths:
        if p.exists():
            return p
    raise FileNotFoundError("Nenhum arquivo encontrado.")


def build_grid(df):
    z_total_cm = np.full((GRID_ROWS, GRID_COLS), np.nan)
    for _, r in df.iterrows():
        row = int(r["row"])
        col = int(r["col"])
        z = float(r["z_total_m"])
        if z > 0:
            z_total_cm[row, col] = z * 100.0
    return z_total_cm


def fix_like_v42(grid):
    g = grid.copy()
    g[6:, 0:3] = np.nan
    g = np.roll(g, -1, axis=0)
    g = np.flipud(g)
    return g


def load_png(path):
    img = Image.open(path).convert("L")
    arr = np.array(img).astype(float)
    arr = (arr - arr.min()) / (np.ptp(arr) + 1e-6)
    return arr


def load_polygon(path):
    gdf = gpd.read_file(path)
    geom = unary_union(gdf.geometry).buffer(0)

    if isinstance(geom, MultiPolygon):
        geom = max(list(geom.geoms), key=lambda g: g.area)

    if isinstance(geom, Polygon):
        geom = Polygon(geom.exterior)

    return geom


def polygon_to_grid_space(geom):
    minx, miny, maxx, maxy = geom.bounds
    width = maxx - minx
    height = maxy - miny

    def mapper(x, y, z=None):
        gx = -0.5 + ((x - minx) / width) * GRID_COLS
        gy = -0.5 + ((maxy - y) / height) * GRID_ROWS
        return gx, gy

    return transform(mapper, geom)


def transform_polygon(poly_grid, dx, dy, sx, sy, angle):
    origin = ((GRID_COLS - 1) / 2, (GRID_ROWS - 1) / 2)
    g = scale(poly_grid, xfact=sx, yfact=sy, origin=origin)
    g = rotate(g, angle, origin=origin, use_radians=False)
    g = translate(g, xoff=dx, yoff=dy)
    return g


def add_watermark(fig, png):
    rows, cols = GRID_ROWS, GRID_COLS

    x_left = -0.5 + OFFSET_X
    x_right = cols - 0.5 + OFFSET_X
    y_top = -0.5 + OFFSET_Y
    y_bottom = rows - 0.5 + OFFSET_Y

    cx = (x_left + x_right) / 2
    cy = (y_top + y_bottom) / 2

    width = (x_right - x_left) * PNG_SCALE_X
    height = (y_bottom - y_top) * PNG_SCALE_Y

    x_left = cx - width / 2
    x_right = cx + width / 2
    y_top = cy - height / 2
    y_bottom = cy + height / 2

    fig.add_trace(go.Heatmap(
        z=png,
        x0=x_left,
        dx=(x_right - x_left) / png.shape[1],
        y0=y_top,
        dy=(y_bottom - y_top) / png.shape[0],
        colorscale="Greys",
        showscale=False,
        opacity=PNG_OPACITY,
        hoverinfo="skip",
        name="BASE_RASTER",
    ))


def add_grid_lines(fig):
    for c in range(GRID_COLS + 1):
        fig.add_trace(go.Scatter(
            x=[c - 0.5, c - 0.5],
            y=[-0.5, GRID_ROWS - 0.5],
            mode="lines",
            line=dict(color="rgba(255,255,255,0.45)", width=1),
            showlegend=False,
            hoverinfo="skip",
        ))

    for r in range(GRID_ROWS + 1):
        fig.add_trace(go.Scatter(
            x=[-0.5, GRID_COLS - 0.5],
            y=[r - 0.5, r - 0.5],
            mode="lines",
            line=dict(color="rgba(255,255,255,0.45)", width=1),
            showlegend=False,
            hoverinfo="skip",
        ))


def add_polygon(fig, geom, fill=True):
    xs, ys = geom.exterior.xy

    if fill:
        fig.add_trace(go.Scatter(
            x=list(xs),
            y=list(ys),
            mode="lines",
            fill="toself",
            fillcolor="rgba(255,255,255,0.22)",
            line=dict(color="red", width=3),
            showlegend=False,
            hoverinfo="skip",
            name="POLYGON_FILL",
        ))
    else:
        fig.add_trace(go.Scatter(
            x=list(xs),
            y=list(ys),
            mode="lines",
            line=dict(color="red", width=3),
            showlegend=False,
            hoverinfo="skip",
            name="POLYGON",
        ))


def add_polygon_cell_mask(fig, geom):
    mask = np.full((GRID_ROWS, GRID_COLS), np.nan)

    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            x = c
            y = r
            if geom.contains(gpd.points_from_xy([x], [y])[0]):
                mask[r, c] = 1

    fig.add_trace(go.Heatmap(
        z=mask,
        colorscale=[[0, "rgba(255,255,255,0)"], [1, "rgba(255,0,0,0.35)"]],
        showscale=False,
        opacity=0.45,
        hoverinfo="skip",
        name="POLYGON_CELL_MASK",
    ))


def make_fig(layers, dx, dy, sx, sy, angle):
    poly_t = transform_polygon(POLY_GRID, dx, dy, sx, sy, angle)

    fig = go.Figure()

    if "base" in layers:
        add_watermark(fig, PNG)

    if "pinos" in layers:
        fig.add_trace(go.Heatmap(
            z=Z_TOTAL_CM,
            colorscale="Viridis",
            showscale=True,
            colorbar=dict(title="Pino<br>(cm)"),
            opacity=GRID_OPACITY,
            xgap=0,
            ygap=0,
            hovertemplate="col=%{x}<br>row=%{y}<br>pino=%{z:.1f} cm<extra></extra>",
            name="PINO_Z_TOTAL_CM",
        ))

    if "polygon_mask" in layers:
        add_polygon_cell_mask(fig, poly_t)

    if "polygon" in layers:
        add_polygon(fig, poly_t, fill=("polygon_fill" in layers))

    if "grid" in layers:
        add_grid_lines(fig)

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False, range=[-0.5, GRID_COLS - 0.5], constrain="domain"),
        yaxis=dict(visible=False, range=[GRID_ROWS - 0.5, -0.5], scaleanchor="x", scaleratio=1),
        plot_bgcolor="white",
        paper_bgcolor="white",
        autosize=True,
    )

    return fig


PNG_PATH = first_existing(PNG_CANDIDATES)
POLYGON_PATH = first_existing(POLYGON_CANDIDATES)

df = pd.read_csv(CSV_PATH)
Z_TOTAL_CM = fix_like_v42(build_grid(df))
PNG = load_png(PNG_PATH)

POLY_RAW = load_polygon(POLYGON_PATH)
POLY_GRID = polygon_to_grid_space(POLY_RAW)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Div("V125 — Polygon Alignment", style={"fontWeight": "bold", "marginBottom": "6px"}),

        dcc.Checklist(
            id="layers",
            options=[
                {"label": "Base IPT", "value": "base"},
                {"label": "Pinos z_total_cm", "value": "pinos"},
                {"label": "Polígono", "value": "polygon"},
                {"label": "Preencher polígono", "value": "polygon_fill"},
                {"label": "Máscara por célula", "value": "polygon_mask"},
                {"label": "Grid 16x8", "value": "grid"},
            ],
            value=["base", "pinos", "polygon", "polygon_fill", "polygon_mask", "grid"],
        ),

        html.Br(),

        html.Label("dx"),
        dcc.Slider(-8, 8, 0.05, value=0, id="dx", marks={-8: "-8", 0: "0", 8: "8"}),

        html.Label("dy"),
        dcc.Slider(-8, 8, 0.05, value=0, id="dy", marks={-8: "-8", 0: "0", 8: "8"}),

        html.Label("scale_x"),
        dcc.Slider(0.2, 2.5, 0.01, value=1, id="sx", marks={0.2: "0.2", 1: "1", 2.5: "2.5"}),

        html.Label("scale_y"),
        dcc.Slider(0.2, 2.5, 0.01, value=1, id="sy", marks={0.2: "0.2", 1: "1", 2.5: "2.5"}),

        html.Label("angle"),
        dcc.Slider(-180, 180, 1, value=0, id="angle", marks={-180: "-180", 0: "0", 180: "180"}),

        html.Pre(id="params", style={"fontSize": "12px", "whiteSpace": "pre-wrap"}),
    ], style={
        "position": "fixed",
        "left": "8px",
        "top": "8px",
        "zIndex": 10,
        "width": "350px",
        "background": "rgba(255,255,255,0.90)",
        "padding": "10px",
        "border": "1px solid #ccc",
        "borderRadius": "8px",
        "fontFamily": "Arial",
        "fontSize": "13px",
    }),

    dcc.Graph(
        id="cityspace-v125",
        config={"displayModeBar": False, "scrollZoom": False, "responsive": True},
        style={"width": "100vw", "height": "100vh"},
    )
], style={"margin": 0, "padding": 0, "width": "100vw", "height": "100vh", "overflow": "hidden"})


@app.callback(
    Output("cityspace-v125", "figure"),
    Output("params", "children"),
    Input("layers", "value"),
    Input("dx", "value"),
    Input("dy", "value"),
    Input("sx", "value"),
    Input("sy", "value"),
    Input("angle", "value"),
)
def update(layers, dx, dy, sx, sy, angle):
    txt = (
        f"DX = {dx:.2f}\n"
        f"DY = {dy:.2f}\n"
        f"SCALE_X = {sx:.2f}\n"
        f"SCALE_Y = {sy:.2f}\n"
        f"ANGLE = {angle:.1f}\n"
        f"POLYGON = {POLYGON_PATH.name}"
    )
    return make_fig(layers or [], dx, dy, sx, sy, angle), txt


if __name__ == "__main__":
    print("========================================")
    print("V125 — POLYGON ALIGNMENT CALIBRATOR")
    print("========================================")
    print("CSV:", CSV_PATH)
    print("PNG:", PNG_PATH)
    print("POLYGON:", POLYGON_PATH)
    print("Pino cm min/max:", float(np.nanmin(Z_TOTAL_CM)), float(np.nanmax(Z_TOTAL_CM)))
    print("========================================")
    app.run(debug=True)
