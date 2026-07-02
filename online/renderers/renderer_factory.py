from pathlib import Path

RENDERERS = {

    "v41": {
        "gif": Path("visualization/mesa_virtual_v41.gif"),
        "timeline": Path("visualization/mesa_virtual_v41_timeline.json"),
    },
}


def get_gif_path(version: str):
    if version not in RENDERERS:
        raise ValueError(f"Versão não registrada: {version}")
    return RENDERERS[version]["gif"]


def get_timeline_path(version: str):
    if version not in RENDERERS:
        raise ValueError(f"Versão não registrada: {version}")
    return RENDERERS[version]["timeline"]


def list_versions():
    return list(RENDERERS.keys())
