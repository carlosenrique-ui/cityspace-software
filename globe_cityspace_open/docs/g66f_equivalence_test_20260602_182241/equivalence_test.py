from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageDraw

GRID = "globe_cityspace_open/projects/ipt_north_5000/grid_z_total_m.csv"

z = np.loadtxt(GRID, delimiter=";")

max_r, max_c = np.unravel_index(np.nanargmax(z), z.shape)
min_r, min_c = np.unravel_index(np.nanargmin(z), z.shape)

report = {
    "grid_shape": list(z.shape),
    "max_value": float(z[max_r, max_c]),
    "max_position": {
        "row": int(max_r),
        "col": int(max_c)
    },
    "min_value": float(z[min_r, min_c]),
    "min_position": {
        "row": int(min_r),
        "col": int(min_c)
    }
}

# versões geométricas
variants = {
    "north_up": z,
    "rot180": np.rot90(z, 2),
    "flipud": np.flipud(z),
    "fliplr": np.fliplr(z),
}

CELL = 80

for name, arr in variants.items():

    h, w = arr.shape

    img = Image.new("RGB", (w*CELL, h*CELL), "white")
    draw = ImageDraw.Draw(img)

    vmax = np.nanmax(arr)

    for r in range(h):
        for c in range(w):
            v = float(arr[r,c])

            g = int(255 * (v / vmax))

            x0 = c * CELL
            y0 = r * CELL

            draw.rectangle(
                [x0,y0,x0+CELL,y0+CELL],
                fill=(g,g,g),
                outline=(255,255,255)
            )

    img.save(f"{OUT}/{name}.png")

with open(f"{OUT}/equivalence_report.json","w") as f:
    json.dump(report,f,indent=2)

print(json.dumps(report,indent=2))
print()
print("OUTPUT =", OUT)
