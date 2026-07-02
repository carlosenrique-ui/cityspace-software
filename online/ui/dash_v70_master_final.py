# ==========================================================
# IPT-CitySpace – V70 MASTER FINAL (AUTO DIAGNÓSTICO + FASES)
# ==========================================================

import json
import numpy as np
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from pathlib import Path
import time
import base64

# =========================================
# CONFIG
# =========================================

ROWS = 8
COLS = 16
PIN_MAX_CM = 10.0
SPEED_CM_S = 2.0

PLAN_PATH = Path("products/final/actuator_plan.json")
CSV_PATH = Path("products/final/grid_height.csv")
BG_PATH = Path("products/final/grid_height.bmp")

START_YEAR = 1940
END_YEAR = 2020

# =========================================
# FASE 1 – AUTOSCAN FILESYSTEM
# =========================================

print("\n==============================")
print("🔍 FASE 1 – AUTOSCAN FILESYSTEM")
print("==============================")

def check(path, name):
    if path.exists():
        print(f"✅ {name}: OK")
        return True
    else:
        print(f"❌ {name}: NÃO ENCONTRADO")
        return False

check(PLAN_PATH, "actuator_plan")
check(CSV_PATH, "grid_height.csv")
check(BG_PATH, "urbanização BMP")

# =========================================
# FASE 2 – LOAD DATA
# =========================================

print("\n==============================")
print("📥 FASE 2 – LOAD DATA")
print("==============================")

EVENTS = []
try:
    with open(PLAN_PATH) as f:
        raw = json.load(f)
        EVENTS = raw.get("events", raw)
    print(f"✅ Eventos carregados: {len(EVENTS)}")
except Exception as e:
    print(f"❌ Erro actuator_plan: {e}")

try:
    df = pd.read_csv(CSV_PATH)
    print(f"✅ CSV carregado: {len(df)} registros")
except Exception as e:
    print(f"❌ Erro CSV: {e}")
    df = pd.DataFrame()

# grids
grid_total = np.zeros((ROWS, COLS))
grid_terrain = np.zeros((ROWS, COLS))
grid_building = np.zeros((ROWS, COLS))

if not df.empty:
    grid_total = df.pivot(index="row", columns="col", values="z_total_m").values
    grid_terrain = df.pivot(index="row", columns="col", values="z_terrain_m").values
    grid_building = df.pivot(index="row", columns="col", values="z_building_m").values

# =========================================
# FASE 3 – AUTOSCAN CIENTÍFICO
# =========================================

print("\n==============================")
print("🧠 FASE 3 – AUTOSCAN CIENTÍFICO")
print("==============================")

def autoscan(df, grid_total, grid_terrain, grid_building):

    # integridade
    if not df.empty:
        diff = np.abs(
            df["z_total_m"] - (df["z_terrain_m"] + df["z_building_m"])
        ).mean()

        if diff < 0.01:
            print("✅ Integridade: total = terrain + building")
        else:
            print(f"❌ ERRO: inconsistência (diff médio = {diff:.4f})")

    # variação
    max_val = np.max(grid_total)
    min_val = np.min(grid_total)

    print(f"📊 Range altura: {min_val:.2f} → {max_val:.2f}")

    if max_val < 1:
        print("⚠️ Alturas muito baixas")

    # camadas
    if np.allclose(grid_total, grid_terrain):
        print("⚠️ Terrain == Total (building perdido)")

    if np.allclose(grid_building, 0):
        print("⚠️ Sem edifícios detectados")

    # grid
    if grid_total.shape == (ROWS, COLS):
        print("✅ Grid OK (8x16)")
    else:
        print(f"❌ Grid incorreto: {grid_total.shape}")

autoscan(df, grid_total, grid_terrain, grid_building)

# =========================================
# FASE 4 – NORMALIZAÇÃO
# =========================================

print("\n==============================")
print("📏 FASE 4 – NORMALIZAÇÃO")
print("==============================")

max_m = np.max(grid_total) if np.max(grid_total) > 0 else 1
grid_cm = (grid_total / max_m) * PIN_MAX_CM

print(f"📐 max_m: {max_m:.2f} m")
print(f"📐 escala → PIN_MAX_CM: {PIN_MAX_CM} cm")

# =========================================
# FASE 5 – BACKGROUND
# ====