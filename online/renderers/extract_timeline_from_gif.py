from pathlib import Path
import json
from PIL import Image

GIF_PATH = Path("visualization/mesa_virtual_v41.gif")
OUT_PATH = Path("visualization/mesa_virtual_v41_timeline.json")

if not GIF_PATH.exists():
    raise RuntimeError(f"GIF não encontrado: {GIF_PATH}")

gif = Image.open(GIF_PATH)

frame_times = []
tempo = 0

try:
    while True:

        duration = gif.info.get("duration", 100)  # ms

        tempo += duration
        frame_times.append(tempo)

        gif.seek(gif.tell() + 1)

except EOFError:
    pass

with open(OUT_PATH, "w") as f:
    json.dump(
        {
            "version": "v41",
            "total_frames": len(frame_times),
            "frame_times_ms": frame_times,
        },
        f,
        indent=4,
    )

print("Timeline criada:", OUT_PATH)
print("Frames:", len(frame_times))
