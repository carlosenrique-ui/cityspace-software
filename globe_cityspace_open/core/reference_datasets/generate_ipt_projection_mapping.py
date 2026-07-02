from __future__ import annotations

from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROWS = 8
COLS = 16
PX_PER_CM = 100
DPI = 254

BASE = Path(".")
PROJECT = BASE / "globe_cityspace_open/projects/ipt_north_5000"


def load_grid(name: str) -> np.ndarray:
    return np.loadtxt(PROJECT / name, delimiter=";")


def viridis(t: float) -> tuple[int, int, int]:
    stops = [
        (68, 1, 84),
        (49, 104, 142),
        (53, 183, 121),
        (253, 231, 37),
    ]
    t = max(0.0, min(1.0, t))
    i = min(len(stops) - 2, int(t * (len(stops) - 1)))
    f = t * (len(stops) - 1) - i
    a = stops[i]
    b = stops[i + 1]
    return tuple(round(a[k] + (b[k] - a[k]) * f) for k in range(3))


def pin_id(row: int, col: int) -> int:
    return col * ROWS + row + 1


def draw_projection(
    out_path: Path,
    pin_cm: np.ndarray,
    gray: np.ndarray,
    cell_size_cm: int,
    mode: str,
    labels: bool,
    calibration: bool,
) -> None:
    cell_px = cell_size_cm * PX_PER_CM
    width = COLS * cell_px
    height = ROWS * cell_px

    img = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(img)

    font = ImageFont.load_default()

    for r in range(ROWS):
        for c in range(COLS):
            x0 = c * cell_px
            y0 = r * cell_px
            x1 = x0 + cell_px - 1
            y1 = y0 + cell_px - 1

            z = float(pin_cm[r, c])
            g = int(gray[r, c])

            if mode == "gray":
                color = (g, g, g)
            else:
                color = viridis(z / 10.0)

            draw.rectangle([x0, y0, x1, y1], fill=color)

            if calibration:
                draw.rectangle([x0, y0, x1, y1], outline=(255, 255, 255), width=max(2, cell_px // 40))

            if labels:
                pid = pin_id(r, c)
                text = f"P{pid:03d}\n{z:.1f}cm"
                text_color = (0, 0, 0) if z > 6.0 or g > 160 else (255, 255, 255)
                draw.multiline_text((x0 + 8, y0 + 8), text, fill=text_color, font=font)

    if calibration:
        corner = max(18, cell_px // 4)
        draw.rectangle([0, 0, corner, corner], fill=(255, 0, 0))
        draw.text((corner + 8, 8), "P001", fill=(255, 255, 255), font=font)

        draw.rectangle([0, height - corner, corner, height], fill=(0, 255, 0))
        draw.text((corner + 8, height - corner + 8), "P008", fill=(255, 255, 255), font=font)

        draw.rectangle([width - corner, height - corner, width, height], fill=(0, 0, 255))
        draw.text((width - corner - 48, height - corner + 8), "P121", fill=(255, 255, 255), font=font)

        draw.rectangle([width - corner, 0, width, corner], fill=(255, 255, 0))
        draw.text((width - corner - 48, 8), "P128", fill=(0, 0, 0), font=font)

        draw.text((width // 2 - 45, 8), "NORTE ↑", fill=(255, 255, 255), font=font)

    img.save(out_path, dpi=(DPI, DPI))


def draw_legend(out_path: Path) -> None:
    w, h = 220, 720
    img = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    bar_x0, bar_x1 = 70, 120
    bar_y0, bar_y1 = 60, 660

    for y in range(bar_y0, bar_y1):
        t = 1.0 - ((y - bar_y0) / (bar_y1 - bar_y0))
        draw.line([bar_x0, y, bar_x1, y], fill=viridis(t))

    draw.rectangle([bar_x0, bar_y0, bar_x1, bar_y1], outline=(0, 0, 0), width=2)

    for i in range(11):
        z = 10 - i
        y = bar_y0 + int((i / 10) * (bar_y1 - bar_y0))
        draw.line([bar_x1, y, bar_x1 + 10, y], fill=(0, 0, 0), width=2)
        draw.text((bar_x1 + 18, y - 5), f"{z} cm", fill=(0, 0, 0), font=font)

    draw.text((30, 20), "Altura dos pinos", fill=(0, 0, 0), font=font)
    draw.text((55, 680), "0–10 cm", fill=(0, 0, 0), font=font)

    img.save(out_path, dpi=(DPI, DPI))


def main() -> None:
    pin = load_grid("grid_pino_cm.csv")
    gray = load_grid("grid_uint8.csv").astype(np.uint8)

    products = []

    for cell_size_cm in [1, 2]:
        for mode in ["viridis", "gray"]:
            path = PROJECT / f"projection_mapping_{mode}_{cell_size_cm}cm.png"
            draw_projection(path, pin, gray, cell_size_cm, mode, labels=False, calibration=False)
            products.append(path.name)

        path = PROJECT / f"projection_mapping_calibration_{cell_size_cm}cm.png"
        draw_projection(path, pin, gray, cell_size_cm, "viridis", labels=True, calibration=True)
        products.append(path.name)

    legend_path = PROJECT / "projection_mapping_legend_cm.png"
    draw_legend(legend_path)
    products.append(legend_path.name)

    manifest_path = PROJECT / "manifest_ipt_north_5000.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["projection_mapping_products"] = {
        "purpose": "Images intended for projection mapping over the tangible 16x8 physical table",
        "north_up": True,
        "rotation_deg": 0.0,
        "cell_modes": ["1cm", "2cm"],
        "products": products,
        "corner_validation": {
            "P001": "upper_left",
            "P008": "lower_left",
            "P121": "lower_right",
            "P128": "upper_right",
        },
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    print("PROJECTION MAPPING PRODUCTS CREATED")
    for p in products:
        print(PROJECT / p)


if __name__ == "__main__":
    main()
