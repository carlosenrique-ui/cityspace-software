from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROWS = 8
COLS = 16
CELL = 80

GRID = Path("globe_cityspace_open/projects/ipt_north_5000/grid_pino_cm.csv")
OUT = Path(__file__).parent

pin = np.loadtxt(GRID, delimiter=";")

def viridis(t):
    stops = [(68,1,84),(49,104,142),(53,183,121),(253,231,37)]
    t = max(0, min(1, float(t)))
    i = min(len(stops)-2, int(t*(len(stops)-1)))
    f = t*(len(stops)-1)-i
    a,b = stops[i], stops[i+1]
    return tuple(round(a[k]+(b[k]-a[k])*f) for k in range(3))

def render_matrix(arr, name):
    h, w = arr.shape
    img = Image.new("RGB", (w*CELL, h*CELL), "white")
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    for r in range(h):
        for c in range(w):
            z = float(arr[r,c])
            color = viridis(z/10.0)
            x0, y0 = c*CELL, r*CELL
            d.rectangle([x0,y0,x0+CELL-1,y0+CELL-1], fill=color, outline=(255,255,255), width=2)
            d.text((x0+5,y0+5), f"{z:.1f}", fill=(0,0,0) if z>6 else (255,255,255), font=font)

    d.text((10,10), name, fill=(255,0,0), font=font)
    img.save(OUT / f"{name}.png")

def rotate_pil(arr, angle, name):
    # renderiza North-Up e rotaciona a imagem visualmente
    h, w = arr.shape
    img = Image.new("RGB", (w*CELL, h*CELL), "white")
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    for r in range(h):
        for c in range(w):
            z = float(arr[r,c])
            color = viridis(z/10.0)
            x0, y0 = c*CELL, r*CELL
            d.rectangle([x0,y0,x0+CELL-1,y0+CELL-1], fill=color, outline=(255,255,255), width=2)
            d.text((x0+5,y0+5), f"{z:.1f}", fill=(0,0,0) if z>6 else (255,255,255), font=font)

    rot = img.rotate(angle, expand=True, fillcolor=(255,255,255))
    d2 = ImageDraw.Draw(rot)
    d2.text((10,10), name, fill=(255,0,0), font=font)
    rot.save(OUT / f"{name}.png")

render_matrix(pin, "north_up")
render_matrix(np.flipud(pin), "flipud")
render_matrix(np.fliplr(pin), "fliplr")
render_matrix(np.rot90(pin, 2), "rot180")

rotate_pil(pin, 146.815825, "rot_visual_146_815825")
rotate_pil(pin, 154.63, "rot_visual_154_63")
rotate_pil(pin, -146.815825, "rot_visual_minus_146_815825")
rotate_pil(pin, -154.63, "rot_visual_minus_154_63")

report = {
    "source": str(GRID),
    "tested": [
        "north_up",
        "flipud",
        "fliplr",
        "rot180",
        "rot_visual_146_815825",
        "rot_visual_154_63",
        "rot_visual_minus_146_815825",
        "rot_visual_minus_154_63"
    ],
    "purpose": "Visual forensic comparison between Globe North-Up grid and IPT-CitySpace temporal orientation."
}

(OUT / "rotation_test_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print("ROTATION TEST CREATED")
print(OUT)
