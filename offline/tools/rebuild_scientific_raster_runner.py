from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
FILE = BASE / "offline/raster/pipeline/scientific_raster_runner.py"

code = '''
"""
IPT CitySpace – SCIENTIFIC RASTER RUNNER (REBUILT)
"""

import json
import numpy as np
from pathlib import Path
import rasterio
from rasterio.warp import reproject, Resampling
from rasterio.mask import mask
from rasterio.transform import Affine
import fiona
from shapely.geometry import shape


BASE = Path(__file__).resolve().parents[3]

PARAMS_PATH = BASE / "offline/products/scientific/rigid_transform_params.json"

DSM_INPUT = BASE / "offline/data/processed/dsm/IPT_2018_DSM_LOCAL.tif"
DTM_INPUT = BASE / "offline/data/processed/dtm/IPT_2018_DTM_LOCAL.tif"

DSM_ROT = BASE / "offline/data/processed/dsm/IPT_2018_DSM_ROT.tif"
DTM_ROT = BASE / "offline/data/processed/dtm/IPT_2018_DTM_ROT.tif"

DSM_CLIP = BASE / "offline/data/processed/dsm/IPT_2018_DSM_CLIP.tif"
DTM_CLIP = BASE / "offline/data/processed/dtm/IPT_2018_DTM_CLIP.tif"

ENVELOPE = BASE / "offline/products/scientific/urban_envelope_scientific_rotated_clean.gpkg"


def load_params():
    with open(PARAMS_PATH) as f:
        return json.load(f)


def load_envelope():

    print("\\n[ENVELOPE] carregando envelope científico")

    with fiona.open(
        ENVELOPE,
        layer="urban_envelope_scientific_rotated_clean"
    ) as src:

        feature = next(iter(src))
        geom = shape(feature["geometry"])

        print("Envelope bounds:", geom.bounds)

        return geom


def rotate_raster(src_path, dst_path, params):

    print("\\n=================================================")
    print("[ROTATE]", src_path.name)
    print("=================================================")

    angle = params["theta_rotation_deg"]
    cx, cy = params["midpoint_original"]
    dx = params["dx"]
    dy = params["dy"]

    with rasterio.open(src_path) as src:

        data = src.read(1)

        print("Shape original:", src.shape)
        print("CRS:", src.crs)

        transform = src.transform

        T1 = Affine.translation(-cx, -cy)
        R  = Affine.rotation(angle)
        T2 = Affine.translation(cx, cy)
        T3 = Affine.translation(dx, dy)

        new_transform = transform * T1 * R * T2 * T3

        dst_array = np.zeros_like(data)

        reproject(
            source=data,
            destination=dst_array,
            src_transform=transform,
            src_crs=src.crs,
            dst_transform=new_transform,
            dst_crs=src.crs,
            resampling=Resampling.bilinear
        )

        meta = src.meta.copy()
        meta.update({"transform": new_transform})

        with rasterio.open(dst_path, "w", **meta) as dst:
            dst.write(dst_array, 1)

    print("[OK] Rotacionado:", dst_path.name)


def clip_raster(src_path, dst_path):

    print("\\n=================================================")
    print("[CLIP]", src_path.name)
    print("=================================================")

    geom = load_envelope()

    with rasterio.open(src_path) as src:

        print("Raster bounds:", src.bounds)

        try:

            out_image, out_transform = mask(src, [geom], crop=True)

        except ValueError:

            print("❌ Envelope não intersecta raster")
            print("Abortando clip")

            return

        meta = src.meta.copy()

        meta.update({
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform,
        })

        with rasterio.open(dst_path, "w", **meta) as dst:
            dst.write(out_image)

    print("[OK] Clip salvo:", dst_path.name)


def main():

    print("\\n=================================================")
    print("IPT-CitySpace – SCIENTIFIC RASTER RUNNER")
    print("=================================================")

    params = load_params()

    print("\\n[TRANSFORMAÇÃO RÍGIDA]")
    print("Ângulo (deg):", params["theta_rotation_deg"])
    print("Centro:", params["midpoint_original"])
    print("dx:", params["dx"])
    print("dy:", params["dy"])

    rotate_raster(DSM_INPUT, DSM_ROT, params)
    rotate_raster(DTM_INPUT, DTM_ROT, params)

    clip_raster(DSM_ROT, DSM_CLIP)
    clip_raster(DTM_ROT, DTM_CLIP)

    print("\\n=================================================")
    print("RUNNER FINALIZADO")
    print("=================================================")


if __name__ == "__main__":
    main()
'''

FILE.write_text(code)

print("Scientific raster runner reconstruído:")
print(FILE)
