import json
from pathlib import Path


def export_timeline(frame_times, version="v41"):

    output_path = Path(f"visualization/mesa_virtual_{version}_timeline.json")

    data = {
        "version": version,
        "total_frames": len(frame_times),
        "frame_times_ms": frame_times,
    }

    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[TIMELINE] Exportada: {output_path}")
