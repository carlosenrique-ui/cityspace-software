from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from openpyxl import Workbook


ROWS = 8
COLS = 16
PX_PER_CM = 100
DPI = 254

BASE = Path(".")
OUT = BASE / "globe_cityspace_open/projects/ipt_north_5000"

SRC_TERRAIN = BASE / "offline/products/grid_terrain_m.csv"
SRC_BUILDING = BASE / "offline/products/grid_building_m.csv"
SRC_TOTAL = BASE / "offline/products/grid_z_total_m.csv"


def load_grid(path: Path) -> np.ndarray:
    if not path.exists():
        raise FileNotFoundError(path)
    arr = np.loadtxt(path, delimiter=";")
    if arr.shape != (ROWS, COLS):
        raise ValueError(f"Expected {(ROWS, COLS)}, got {arr.shape}: {path}")
    return arr


def normalize_to_pin_and_gray(total: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    clean = np.nan_to_num(total, nan=0.0, posinf=0.0, neginf=0.0)

    z_min = float(np.nanmin(clean))
    z_max = float(np.nanmax(clean))
    dz = z_max - z_min

    if dz <= 0:
        pin = np.zeros_like(clean)
    else:
        pin = ((clean - z_min) / dz) * 10.0

    gray = np.rint((pin / 10.0) * 255.0).astype(np.uint8)

    return np.round(pin, 3), gray


def write_matrix_csv(path: Path, arr: np.ndarray, fmt: str) -> None:
    np.savetxt(path, arr, delimiter=";", fmt=fmt)


def write_cells_csv(path: Path, terrain, building, total, pin, gray) -> None:
    fields = [
        "cell_id",
        "pin_id",
        "row",
        "col",
        "terrain_height_m",
        "building_height_m",
        "total_height_m",
        "pin_height_cm",
        "gray_value",
        "rotation_deg",
        "north_up",
        "source_policy",
    ]

    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()

        for r in range(ROWS):
            for c in range(COLS):
                pin_id = c * ROWS + (r + 1)

                w.writerow({
                    "cell_id": f"P{pin_id:03d}",
                    "pin_id": pin_id,
                    "row": r + 1,
                    "col": c + 1,
                    "terrain_height_m": round(float(terrain[r, c]), 3),
                    "building_height_m": round(float(building[r, c]), 3),
                    "total_height_m": round(float(total[r, c]), 3),
                    "pin_height_cm": round(float(pin[r, c]), 3),
                    "gray_value": int(gray[r, c]),
                    "rotation_deg": 0.0,
                    "north_up": True,
                    "source_policy": "IPT DTM/DSM/DXF; minimum survey elevation normalized to zero; NaN/outside envelope set to zero",
                })


def write_xlsx(path: Path, terrain, building, total, pin, gray) -> None:
    wb = Workbook()

    ws = wb.active
    ws.title = "cells"
    ws.append([
        "cell_id",
        "pin_id",
        "row",
        "col",
        "terrain_height_m",
        "building_height_m",
        "total_height_m",
        "pin_height_cm",
        "gray_value",
    ])

    for r in range(ROWS):
        for c in range(COLS):
            pin_id = c * ROWS + (r + 1)
            ws.append([
                f"P{pin_id:03d}",
                pin_id,
                r + 1,
                c + 1,
                round(float(terrain[r, c]), 3),
                round(float(building[r, c]), 3),
                round(float(total[r, c]), 3),
                round(float(pin[r, c]), 3),
                int(gray[r, c]),
            ])

    sheets = [
        ("terrain_m_matrix", terrain),
        ("building_m_matrix", building),
        ("total_m_matrix", total),
        ("pin_cm_matrix", pin),
        ("gray_uint8_matrix", gray),
    ]

    for name, arr in sheets:
        wsx = wb.create_sheet(name)
        for r in range(ROWS):
            wsx.append([
                round(float(arr[r, c]), 3)
                if arr.dtype.kind == "f"
                else int(arr[r, c])
                for c in range(COLS)
            ])

    wb.save(path)


def write_gray_image(path: Path, gray: np.ndarray, cell_size_cm: int) -> None:
    cell_px = cell_size_cm * PX_PER_CM
    img = Image.new("L", (COLS * cell_px, ROWS * cell_px), 0)
    draw = ImageDraw.Draw(img)

    for r in range(ROWS):
        for c in range(COLS):
            x0 = c * cell_px
            y0 = r * cell_px
            x1 = x0 + cell_px
            y1 = y0 + cell_px
            draw.rectangle([x0, y0, x1, y1], fill=int(gray[r, c]))

    img.save(path, dpi=(DPI, DPI))


def write_preview(path: Path, pin: np.ndarray, gray: np.ndarray, cell_size_cm: int) -> None:
    cell_px = cell_size_cm * PX_PER_CM
    img = Image.new("RGB", (COLS * cell_px, ROWS * cell_px), "white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.load_default()
    except Exception:
        font = None

    for r in range(ROWS):
        for c in range(COLS):
            g = int(gray[r, c])
            x0 = c * cell_px
            y0 = r * cell_px
            x1 = x0 + cell_px
            y1 = y0 + cell_px

            draw.rectangle(
                [x0, y0, x1, y1],
                fill=(g, g, g),
                outline=(255, 0, 0),
                width=2,
            )

            pin_id = c * ROWS + (r + 1)
            txt = f"P{pin_id:03d}\\nG={g}\\nZ={pin[r,c]:.2f}cm"
            color = (0, 0, 0) if g > 150 else (255, 255, 255)
            draw.multiline_text((x0 + 6, y0 + 6), txt, fill=color, font=font)

    draw.text(
        (10, 10),
        "IPT North 1:5000 | rotation=0 | north up | source: IPT DTM/DSM/DXF",
        fill=(255, 0, 0),
        font=font,
    )

    img.save(path, dpi=(DPI, DPI))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    terrain = load_grid(SRC_TERRAIN)
    building = load_grid(SRC_BUILDING)
    total = load_grid(SRC_TOTAL)

    pin, gray = normalize_to_pin_and_gray(total)

    shutil.copy2(SRC_TERRAIN, OUT / "grid_terrain_m.csv")
    shutil.copy2(SRC_BUILDING, OUT / "grid_building_m.csv")
    shutil.copy2(SRC_TOTAL, OUT / "grid_z_total_m.csv")

    write_matrix_csv(OUT / "grid_pino_cm.csv", pin, "%.3f")
    write_matrix_csv(OUT / "grid_uint8.csv", gray, "%d")
    write_cells_csv(OUT / "ipt_north_5000_cells.csv", terrain, building, total, pin, gray)
    write_xlsx(OUT / "ipt_north_5000_cells.xlsx", terrain, building, total, pin, gray)

    for cell_size_cm in [1, 2]:
        suffix = f"{cell_size_cm}cm"
        write_gray_image(OUT / f"ipt_north_5000_{suffix}.bmp", gray, cell_size_cm)
        write_gray_image(OUT / f"ipt_north_5000_{suffix}.png", gray, cell_size_cm)
        write_preview(OUT / f"preview_{suffix}.png", pin, gray, cell_size_cm)

    manifest = {
        "contract_type": "ipt_reference_dataset_products",
        "contract_version": "G6.0",
        "project_name": "IPT North 1:5000",
        "source_project": "IPT-CitySpace",
        "source_policy": {
            "terrain_provider": "IPT DTM 2018",
            "surface_provider": "IPT DSM 2018",
            "footprint_provider": "IPT DXF",
            "height_reference": "minimum survey elevation normalized to zero",
            "outside_survey_envelope": "NaN or outside survey envelope set to zero",
            "surroundings_policy": "no inference outside IPT survey envelope",
        },
        "spatial_policy": {
            "scale": 5000,
            "rotation_deg": 0.0,
            "north_up": True,
            "grid_rows": ROWS,
            "grid_cols": COLS,
            "pin_layout": "column_zigzag",
            "origin": "upper_left",
            "x_prime": "right",
            "y_prime": "down",
            "z_prime": "up",
        },
        "height_model": {
            "input_total_min_m": round(float(np.nanmin(total)), 3),
            "input_total_max_m": round(float(np.nanmax(total)), 3),
            "pin_height_cm_range": [0, 10],
            "gray_value_range": [0, 255],
        },
        "source_files": {
            "terrain": str(SRC_TERRAIN),
            "building": str(SRC_BUILDING),
            "total": str(SRC_TOTAL),
        },
        "products": [
            "grid_terrain_m.csv",
            "grid_building_m.csv",
            "grid_z_total_m.csv",
            "grid_pino_cm.csv",
            "grid_uint8.csv",
            "ipt_north_5000_cells.csv",
            "ipt_north_5000_cells.xlsx",
            "ipt_north_5000_1cm.bmp",
            "ipt_north_5000_1cm.png",
            "preview_1cm.png",
            "ipt_north_5000_2cm.bmp",
            "ipt_north_5000_2cm.png",
            "preview_2cm.png",
        ],
    }

    (OUT / "manifest_ipt_north_5000.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("IPT NORTH 1:5000 PRODUCTS CREATED")
    print(OUT)
    print("total min/max:", float(np.nanmin(total)), float(np.nanmax(total)))
    print("pin min/max:", float(np.nanmin(pin)), float(np.nanmax(pin)))
    print("gray min/max:", int(np.nanmin(gray)), int(np.nanmax(gray)))


if __name__ == "__main__":
    main()
