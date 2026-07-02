from pathlib import Path
import ezdxf
from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely.validation import make_valid
from osgeo import ogr, gdal

print("\n====================================================")
print("=== DXF HATCH → SCIENTIFIC (BUILDINGS + ENVELOPE) ===")
print("====================================================\n")

gdal.UseExceptions()

ENGINE_ROOT = Path(__file__).resolve().parents[2]

DXF_PATH = ENGINE_ROOT / "offline/data/raw/dxf/IPT-2018-DXF.dxf"

OUTPUT_BUILDINGS = ENGINE_ROOT / "offline/products/scientific/buildings_scientific.gpkg"
OUTPUT_ENVELOPE = ENGINE_ROOT / "offline/products/scientific/urban_envelope_scientific.gpkg"


from ezdxf.entities.boundary_paths import LineEdge, SplineEdge


def hatch_to_polygon(hatch):

    polygons = []

    for path in hatch.paths:
        if hasattr(path, "edges"):

            coords = []

            for edge in path.edges:

                if isinstance(edge, LineEdge):
                    coords.append((edge.start[0], edge.start[1]))

                elif isinstance(edge, SplineEdge):
                    for p in edge.control_points:
                        coords.append((p[0], p[1]))

            if len(coords) > 2:
                poly = Polygon(coords)
                if poly.is_valid and poly.area > 1:
                    polygons.append(poly)

    if polygons:
        return unary_union(polygons)

    return None

def save_gpkg(geoms, output_path, layer_name):

    driver = ogr.GetDriverByName("GPKG")

    if output_path.exists():
        driver.DeleteDataSource(str(output_path))

    ds = driver.CreateDataSource(str(output_path))
    layer = ds.CreateLayer(layer_name, None, ogr.wkbPolygon)

    feature_def = layer.GetLayerDefn()

    for geom in geoms:
        feature = ogr.Feature(feature_def)
        ogr_geom = ogr.CreateGeometryFromWkb(geom.wkb)
        feature.SetGeometry(ogr_geom)
        layer.CreateFeature(feature)

    ds = None


def main():

    if not DXF_PATH.exists():
        raise FileNotFoundError(f"DXF não encontrado:\n{DXF_PATH}")

    print("Lendo DXF...")
    doc = ezdxf.readfile(DXF_PATH)
    msp = doc.modelspace()

    geometries = []

    print("Convertendo HATCH para polígonos...")

    for hatch in msp.query("HATCH"):
        geom = hatch_to_polygon(hatch)
        if geom:
            if not geom.is_valid:
                geom = make_valid(geom)
            geometries.append(geom)

    print("Total HATCH convertidos:", len(geometries))

    if len(geometries) == 0:
        raise RuntimeError("Nenhuma geometria válida encontrada.")

    print("Calculando áreas...")

    geometries_sorted = sorted(geometries, key=lambda g: g.area, reverse=True)

    envelope = geometries_sorted[0]
    buildings = geometries_sorted[1:]

    print("Área envelope:", envelope.area)
    print("Total edifícios:", len(buildings))

    print("Salvando envelope científico...")
    save_gpkg([envelope], OUTPUT_ENVELOPE, "urban_envelope")

    print("Salvando edifícios científicos...")
    save_gpkg(buildings, OUTPUT_BUILDINGS, "buildings")

    print("\n✔ Processamento concluído com sucesso.")
    print("\nArquivos gerados:")
    print(OUTPUT_ENVELOPE)
    print(OUTPUT_BUILDINGS)


if __name__ == "__main__":
    main()