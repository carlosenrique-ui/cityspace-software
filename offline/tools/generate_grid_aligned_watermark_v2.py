from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely import affinity

ENGINE_ROOT = Path("/mnt/c/workspace/ipt-cityspace-engine")
CORE_ROOT = ENGINE_ROOT / "ipt_core_clean"

SCIENTIFIC_DIR = CORE_ROOT / "offline" / "products" / "scientific"
ONLINE_ASSETS_DIR = CORE_ROOT / "online" / "assets"

OUTPUT_PNG = ONLINE_ASSETS_DIR / "ipt_mask_rotated_grid_aligned_v2.png"

ROWS = 8
COLS = 16

XMIN = -0.5
XMAX = COLS - 0.5
YMIN = -0.5
YMAX = ROWS - 0.5


def print_header(title: str) -> None:
    print("\n" + "=" * 70, flush=True)
    print(title, flush=True)
    print("=" * 70, flush=True)


def resolve_vector_path() -> Path:
    candidates = [
        SCIENTIFIC_DIR / "urbanismo_scientific_rotated.gpkg",
        SCIENTIFIC_DIR / "urbanismo_scientific_clean.gpkg",
        SCIENTIFIC_DIR / "buildings_scientific_rotated.gpkg",
        SCIENTIFIC_DIR / "buildings_scientific.gpkg",
        SCIENTIFIC_DIR / "urban_envelope_scientific_rotated_clean.gpkg",
        SCIENTIFIC_DIR / "urban_envelope_scientific_rotated.gpkg",
        SCIENTIFIC_DIR / "urban_envelope_scientific.gpkg",
    ]

    print_header("RESOLVENDO VETOR FONTE")

    for path in candidates:
        print(f"[CHECK] {path}", flush=True)
        if path.exists():
            print(f"[OK] usando vetor: {path}", flush=True)
            return path

    raise FileNotFoundError(
        "Nenhum vetor candidato encontrado em offline/products/scientific."
    )


def load_vector(path: Path) -> gpd.GeoDataFrame:
    print_header("CARREGANDO VETOR")

    gdf = gpd.read_file(path)

    if gdf.empty:
        raise ValueError(f"Vetor vazio: {path}")

    gdf = gdf[gdf.geometry.notna()].copy()
    gdf = gdf[~gdf.geometry.is_empty].copy()

    if gdf.empty:
        raise ValueError(f"Todas as geometrias são nulas/vazias em: {path}")

    print(f"[OK] feições: {len(gdf)}", flush=True)
    print(f"[OK] CRS: {gdf.crs}", flush=True)
    print(f"[OK] bounds originais: {tuple(gdf.total_bounds)}", flush=True)

    return gdf


def normalize_to_grid_frame(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    print_header("NORMALIZANDO PARA O FRAME 16x8 DO GRID")

    minx, miny, maxx, maxy = gdf.total_bounds

    if maxx <= minx or maxy <= miny:
        raise ValueError("Bounds inválidos para normalização.")

    sx = COLS / (maxx - minx)
    sy = ROWS / (maxy - miny)

    print(f"[INFO] scale_x = {sx}", flush=True)
    print(f"[INFO] scale_y = {sy}", flush=True)

    def _transform(geom):
        g = affinity.translate(geom, xoff=-minx, yoff=-miny)
        g = affinity.scale(g, xfact=sx, yfact=sy, origin=(0, 0))
        return g

    gdf2 = gdf.copy()
    gdf2["geometry"] = gdf2.geometry.apply(_transform)

    print(f"[OK] bounds normalizados: {tuple(gdf2.total_bounds)}", flush=True)
    return gdf2


def render_png(gdf: gpd.GeoDataFrame, output_png: Path) -> None:
    print_header("RENDERIZANDO PNG")

    output_png.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(16, 8), dpi=300)
    fig.patch.set_alpha(0.0)
    ax.set_facecolor((1, 1, 1, 0))

    gdf.plot(
        ax=ax,
        color=(0, 0, 0, 0.25),
        edgecolor=(0, 0, 0, 0.60),
        linewidth=1.0,
    )

    ax.set_xlim(XMIN, XMAX)
    ax.set_ylim(ROWS - 0.5, -0.5)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig(output_png, transparent=True, bbox_inches="tight", pad_inches=0)
    plt.close(fig)

    print(f"[OK] PNG salvo em: {output_png}", flush=True)


def main() -> None:
    print_header("IPT-CITYSPACE | GRID-ALIGNED WATERMARK V2")

    vector_path = resolve_vector_path()
    gdf = load_vector(vector_path)
    gdf_grid = normalize_to_grid_frame(gdf)
    render_png(gdf_grid, OUTPUT_PNG)

    print_header("FINALIZADO")
    print(f"[OK] saída: {OUTPUT_PNG}", flush=True)


if __name__ == "__main__":
    main()
