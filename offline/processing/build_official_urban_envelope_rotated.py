import json
from pathlib import Path
import ezdxf
import pyogrio
import geopandas as gpd
from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely.affinity import rotate, translate
from shapely.validation import make_valid

# ===================================================
# === BUILD OFFICIAL URBAN ENVELOPE (ROTATED) ===
# ===================================================

BASE = Path(__file__).resolve().parents[2]

DXF_PATH = BASE / "offline/data/raw/dxf/IPT-2018-DXF.dxf"
PARAMS_PATH = BASE / "offline/products/scientific/rigid_transform_params.json"

OUT_PATH = BASE / "offline/products/scientific/urban_envelope_scientific_rotated.gpkg"

CRS = "EPSG:31983"

# Distância para fechar portões (ajustável)
BUFFER_DISTANCE = 6.0


def hatch_to_polygons(hatch):

    polygons = []

    for path in hatch.paths:

        pts = []

        for edge in path.edges:

            # LineEdge
            if hasattr(edge, "start") and hasattr(edge, "end"):
                pts.append((edge.start[0], edge.start[1]))

            # SplineEdge
            elif hasattr(edge, "control_points"):
                for pt in edge.control_points:
                    pts.append((pt[0], pt[1]))

        if len(pts) >= 3:
            try:
                poly = Polygon(pts)

                # Correção topológica robusta
                poly = make_valid(poly)
                poly = poly.buffer(0)

                if poly.is_valid and not poly.is_empty:
                    polygons.append(poly)

            except Exception:
                continue

    return polygons


def main():

    print("\n==============================================")
    print("=== BUILD OFFICIAL URBAN ENVELOPE (REAL) ===")
    print("==============================================\n")

    doc = ezdxf.readfile(DXF_PATH)
    msp = doc.modelspace()

    all_polygons = []

    for hatch in msp.query("HATCH"):
        result = hatch_to_polygons(hatch)
        if result:
            all_polygons.extend(result)

    print(f"Total polígonos válidos extraídos: {len(all_polygons)}")

    if not all_polygons:
        raise RuntimeError("Nenhum polígono válido encontrado.")

    # ------------------------------------------------
    # União total
    # ------------------------------------------------
    print("Unindo geometrias...")
    union = unary_union(all_polygons)

    # ------------------------------------------------
    # Fechamento morfológico (fecha portões)
    # ------------------------------------------------
    print("Aplicando fechamento morfológico...")
    closed = union.buffer(BUFFER_DISTANCE).buffer(-BUFFER_DISTANCE)

    # ------------------------------------------------
    # Selecionar maior polígono
    # ------------------------------------------------
    if closed.geom_type == "MultiPolygon":
        largest = max(closed.geoms, key=lambda g: g.area)
    else:
        largest = closed

    # ------------------------------------------------
    # Manter apenas anel externo (remove buracos)
    # ------------------------------------------------
    envelope = Polygon(largest.exterior)

    print("Área do envelope externo:", envelope.area)

    # ------------------------------------------------
    # Aplicar transformação rígida
    # ------------------------------------------------
    with open(PARAMS_PATH) as f:
        params = json.load(f)

    angle = params["theta_rotation_deg"]
    dx = params["dx"]
    dy = params["dy"]
    cx, cy = params["midpoint_original"]

    print("Aplicando rotação rígida...")

    envelope_rot = rotate(envelope, angle, origin=(cx, cy), use_radians=False)
    envelope_rot = translate(envelope_rot, xoff=dx, yoff=dy)

    # ------------------------------------------------
    # Criar GeoDataFrame com CRS correto
    # ------------------------------------------------
    gdf = gpd.GeoDataFrame(
        {"id": [1]},
        geometry=[envelope_rot],
        crs=CRS
    )

    # ------------------------------------------------
    # Salvar
    # ------------------------------------------------
    pyogrio.write_dataframe(
        gdf,
        OUT_PATH,
        layer="urban_envelope_scientific_rotated",
        driver="GPKG"
    )

    print("\n✔ Envelope oficial rotacionado criado com sucesso.")
    print(OUT_PATH)
    print()


if __name__ == "__main__":
    main()