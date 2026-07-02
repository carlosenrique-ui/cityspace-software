import numpy as np
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
ROWS=8
COLS=16
BASE=Path(".")
OUT_DIR=BASE/"diagnostics"
OUT_DIR.mkdir(exist_ok=True)
timestamp=datetime.now().strftime("%Y%m%d_%H%M%S")
OUT_FILE=OUT_DIR/f"autoscan_{timestamp}.txt"
PLAN_PATH=BASE/"products/final/actuator_plan.json"
CSV_PATH=BASE/"products/final/grid_height.csv"
BMP_PATH=BASE/"products/final/grid_height.bmp"
log_lines=[]
def log(msg):
 print(msg)
 log_lines.append(msg)
log("==============================")
log("FASE 1 – FILESYSTEM")
log("==============================")
def check(path,name):
 if path.exists():
  log(f"[OK] {name}")
  return True
 else:
  log(f"[ERRO] {name} não encontrado")
  return False
ok_plan=check(PLAN_PATH,"actuator_plan")
ok_csv=check(CSV_PATH,"grid_height.csv")
ok_bmp=check(BMP_PATH,"grid_height.bmp")
log("==============================")
log("FASE 2 – LOAD DATA")
log("==============================")
EVENTS=[]
if ok_plan:
 try:
  with open(PLAN_PATH) as f:
   raw=json.load(f)
   EVENTS=raw.get("events",raw)
  log(f"[OK] Eventos: {len(EVENTS)}")
 except Exception as e:
  log(f"[ERRO] actuator_plan: {e}")
df=pd.DataFrame()
if ok_csv:
 try:
  df=pd.read_csv(CSV_PATH)
  log(f"[OK] CSV carregado: {len(df)} linhas")
 except Exception as e:
  log(f"[ERRO] CSV: {e}")
log("==============================")
log("FASE 3 – GRID")
log("==============================")
grid_total=np.zeros((ROWS,COLS))
grid_terrain=np.zeros((ROWS,COLS))
grid_building=np.zeros((ROWS,COLS))
if not df.empty:
 try:
  grid_total=df.pivot(index="row",columns="col",values="z_total_m").values
  grid_terrain=df.pivot(index="row",columns="col",values="z_terrain_m").values
  grid_building=df.pivot(index="row",columns="col",values="z_building_m").values
  log(f"[OK] Grid shape: {grid_total.shape}")
 except Exception as e:
  log(f"[ERRO] Pivot: {e}")
log("==============================")
log("FASE 4 – INTEGRIDADE")
log("==============================")
if not df.empty:
 if all(col in df.columns for col in ["z_total_m","z_terrain_m","z_building_m"]):
  diff=np.abs(df["z_total_m"]-(df["z_terrain_m"]+df["z_building_m"])).mean()
  if diff<0.01:
   log("[OK] total = terrain + building")
  else:
   log(f"[ERRO] inconsistência média: {diff:.4f}")
log("==============================")
log("FASE 5 – VARIAÇÃO")
log("==============================")
if not df.empty:
 max_val=np.max(grid_total)
 min_val=np.min(grid_total)
 log(f"Range: {min_val:.2f} → {max_val:.2f}")
 if max_val<1:
  log("[ALERTA] relevo muito baixo")
log("==============================")
log("FASE 6 – CAMADAS")
log("==============================")
if not df.empty:
 if np.allclose(grid_total,grid_terrain):
  log("[ALERTA] terrain == total")
 if np.allclose(grid_building,0):
  log("[ALERTA] building = 0")
log("==============================")
log("FASE 7 – TEMPO")
log("==============================")
if not df.empty:
 avg_h=np.mean(grid_total)
 tempo=(avg_h*100)/2.0
 log(f"Tempo médio estimado: {tempo:.2f}s")
log("==============================")
log("SALVANDO RELATÓRIO")
log("==============================")
with open(OUT_FILE,"w",encoding="utf-8") as f:
 f.write("\n".join(log_lines))
log(f"Arquivo gerado: {OUT_FILE}")
log("AUTOSCAN FINALIZADO")