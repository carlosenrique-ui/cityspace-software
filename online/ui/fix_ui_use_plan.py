from pathlib import Path

UI_FILE = Path("online/ui/dash_eventbus_grid_app.py")

content = UI_FILE.read_text()

# REMOVE dependência de snapshot antigo
content = content.replace(
    "OfflineProduct(",
    "# OfflineProduct REMOVIDO (snapshot antigo)\n# OfflineProduct("
)

# INJETAR caminho do plano
inject = """
import json

PLAN_PATH = "products/latest/actuator_plan.json"

with open(PLAN_PATH, "r") as f:
    PLAN = json.load(f)
"""

if "PLAN_PATH" not in content:
    content = inject + "\n\n" + content

UI_FILE.write_text(content)

print("✔ UI agora usa actuator_plan.json")
