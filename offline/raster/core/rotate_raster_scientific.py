import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling
from rasterio.transform import Affine

def rotate_raster_scientific(input_path, output_path, rigid_affine):


print("\n=================================================")
print(f"[ROTATE] {input_path.name}")
print("=================================================")

with rasterio.open(input_path) as src:

    data = src.read(1)
    transform = src.transform
    meta = src.meta.copy()

    height, width = data.shape

    print(f"Shape original: {data.shape}")
    print(f"CRS: {src.crs}")

    # ---------------------------------------
    # Bounding box original
    # ---------------------------------------

    left, bottom, right, top = rasterio.transform.array_bounds(
        height,
        width,
        transform
    )

    # ---------------------------------------
    # Rotacionar cantos
    # ---------------------------------------

    corners = [
        rigid_affine * (left, top),
        rigid_affine * (right, top),
        rigid_affine * (right, bottom),
        rigid_affine * (left, bottom),
    ]

    xs = [c[0] for c in corners]
    ys = [c[1] for c in corners]

    new_left = min(xs)
    new_right = max(xs)
    new_bottom = min(ys)
    new_top = max(ys)

    # ---------------------------------------
    # resolução original
    # ---------------------------------------

    res_x = transform.a
    res_y = -transform.e

    new_width = int((new_right - new_left) / res_x)
    new_height = int((new_top - new_bottom) / res_y)

    # ---------------------------------------
    # novo transform
    # ---------------------------------------

    new_transform = Affine(
        res_x, 0, new_left,
        0, -res_y, new_top
    )

    # ---------------------------------------
    # array destino
    # ---------------------------------------

    dst_array = np.zeros(
        (new_height, new_width),
        dtype=data.dtype
    )

    # ---------------------------------------
    # reprojeção (warp real)
    # ---------------------------------------

    reproject(
        source=data,
        destination=dst_array,
        src_transform=transform,
        src_crs=src.crs,
        dst_transform=new_transform,
        dst_crs=src.crs,
        resampling=Resampling.bilinear
    )

    meta.update({
        "height": new_height,
        "width": new_width,
        "transform": new_transform
    })

    with rasterio.open(output_path, "w", **meta) as dst:
        dst.write(dst_array, 1)

print(f"[OK] Rotacionado corretamente: {output_path.name}")
