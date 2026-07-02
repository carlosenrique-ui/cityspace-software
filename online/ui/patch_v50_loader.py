from pathlib import Path

file = Path("online/ui/dash_v50_temporal_truth.py")
text = file.read_text()

inject = """
# =========================================
# LOAD ACTUATOR PLAN (REAL PIPELINE)
# =========================================
import json

PLAN_PATH = "products/latest/actuator_plan.json"

try:
    with open(PLAN_PATH, "r") as f:
        ACTUATOR_PLAN = json.load(f)
    print(f"[UI] Loaded plan: {len(ACTUATOR_PLAN)} events")
except Exception as e:
    print(f"[UI] ERROR loading plan: {e}")
    ACTUATOR_PLAN = []
"""

if "ACTUATOR_PLAN" not in text:
    text = inject + "\n\n" + text
    file.write_text(text)
    print("✔ PATCH aplicado na V50")
else:
    print("✔ PATCH já existe")
