from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROWS = 8
COLS = 16
PX_PER_CM = 100


VIRIDIS = [
    (68, 1, 84),
    (72, 35, 116),
    (64, 67, 135),
    (52, 94, 141),
    (41, 120, 142),
    (32, 144, 140),
    (34, 167, 132),
    (68, 190, 112),
    (121, 209, 81),
    (189, 223, 38),
    (253, 231, 37),
]


def viridis_color(value: int) -> tuple[int, int, int]:
    value = max(0, min(255, int(value)))
    idx = round((value / 255) * (len(VIRIDIS) - 1))
    return VIRIDIS[idx]


def load_height_contract(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_matrix(cells: list[dict]) -> list[list[dict]]:
    matrix = [[None for _ in range(COLS)] for _ in range(ROWS)]

    for cell in cells:
        r = int(cell["row"]) - 1
        c = int(cell["col"]) - 1
        matrix[r][c] = cell

    return matrix


def write_viridis_layer(path: Path, matrix: list[list[dict]], cell_size_cm: int) -> None:
    cell_px = cell_size_cm * PX_PER_CM
    width = COLS * cell_px
    height = ROWS * cell_px

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    for r in range(ROWS):
        for c in range(COLS):
            cell = matrix[r][c]
            color = viridis_color(cell["gray_value"])

            x0 = c * cell_px
            y0 = r * cell_px
            x1 = x0 + cell_px
            y1 = y0 + cell_px

            draw.rectangle(
                [x0, y0, x1, y1],
                fill=color,
                outline=(255, 255, 255),
                width=2
            )

    img.save(path)


def write_pin_preview(path: Path, matrix: list[list[dict]], cell_size_cm: int) -> None:
    cell_px = cell_size_cm * PX_PER_CM
    width = COLS * cell_px
    height = ROWS * cell_px

    img = Image.new("RGB", (width, height), (15, 23, 42))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.load_default()
    except Exception:
        font = None

    for r in range(ROWS):
        for c in range(COLS):
            cell = matrix[r][c]

            x0 = c * cell_px
            y0 = r * cell_px
            x1 = x0 + cell_px
            y1 = y0 + cell_px

            gray = int(cell["gray_value"])
            color = viridis_color(gray)

            pin_cm = float(cell["pin_height_cm"])
            bar_h = int((pin_cm / 10.0) * (cell_px - 12))

            draw.rectangle(
                [x0, y0, x1, y1],
                fill=(30, 41, 59),
                outline=(148, 163, 184),
                width=1
            )

            bx0 = x0 + int(cell_px * 0.30)
            bx1 = x0 + int(cell_px * 0.70)
            by1 = y1 - 6
            by0 = by1 - bar_h

            draw.rectangle(
                [bx0, by0, bx1, by1],
                fill=color,
                outline=(255, 255, 255),
                width=1
            )

            text = f'{cell["cell_id"]}\n{pin_cm:.1f}cm'
            draw.multiline_text(
                (x0 + 5, y0 + 5),
                text,
                fill=(255, 255, 255),
                font=font
            )

    img.save(path)


def write_layer_manifest(path: Path, products: list[str]) -> None:
    manifest = {
        "contract_type": "layer_products",
        "contract_version": "G5.7",
        "description": "Layer Engine MVP generated from Height Contract",
        "layers": [
            {
                "name": "Viridis Height Layer",
                "source": "gray_value",
                "purpose": "analytical visual layer for presentation"
            },
            {
                "name": "Pin Preview Layer",
                "source": "pin_height_cm",
                "purpose": "virtual table preview without hardware"
            }
        ],
        "products": products
    }

    path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--height-contract", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    height_contract = load_height_contract(Path(args.height_contract))
    matrix = build_matrix(height_contract["cells"])

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    products = []

    for cell_size_cm in [1, 2]:
        suffix = f"{cell_size_cm}cm"

        viridis_path = out_dir / f"viridis_layer_{suffix}.png"
        pin_path = out_dir / f"pin_preview_{suffix}.png"

        write_viridis_layer(viridis_path, matrix, cell_size_cm)
        write_pin_preview(pin_path, matrix, cell_size_cm)

        products.append(viridis_path.name)
        products.append(pin_path.name)

    write_layer_manifest(out_dir / "layer_manifest_G57.json", products)

    print("LAYER PRODUCTS CREATED")
    print(out_dir)


if __name__ == "__main__":
    main()
