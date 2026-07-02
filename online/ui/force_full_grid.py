from pathlib import Path

file = Path("online/ui/dash_v50_temporal_truth.py")
text = file.read_text()

text = text.replace(
    "build_grid(ACTUATOR_PLAN, step)",
    "build_grid(ACTUATOR_PLAN, len(ACTUATOR_PLAN))"
)

file.write_text(text)

print("✔ GRID FORÇADO COM TODOS OS EVENTOS")
