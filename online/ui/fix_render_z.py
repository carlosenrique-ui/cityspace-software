from pathlib import Path

file = Path("online/ui/dash_v50_temporal_truth.py")
text = file.read_text()

# força uso do z correto no heatmap
text = text.replace(
    "go.Heatmap(",
    "go.Heatmap(z=z,"
)

file.write_text(text)

print("✔ HEATMAP agora usa o grid correto")
