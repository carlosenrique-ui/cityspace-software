from pathlib import Path

file = Path("online/ui/dash_v50_temporal_truth.py")
text = file.read_text()

# força uso do build_grid dentro do callback
if "build_grid(" in text and "z =" not in text:
    text = text.replace(
        "fig = go.Figure(",
        "z = build_grid(ACTUATOR_PLAN, len(ACTUATOR_PLAN))\n    fig = go.Figure("
    )

file.write_text(text)

print("✔ CALLBACK agora usa build_grid")
