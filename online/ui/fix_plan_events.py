from pathlib import Path

file = Path("online/ui/dash_v50_temporal_truth.py")
text = file.read_text()

# substituir uso direto do PLAN
text = text.replace(
    "ACTUATOR_PLAN = json.load(f)",
    "RAW_PLAN = json.load(f)\n    ACTUATOR_PLAN = RAW_PLAN.get('events', RAW_PLAN)"
)

file.write_text(text)

print("✔ UI agora usa PLAN['events']")
