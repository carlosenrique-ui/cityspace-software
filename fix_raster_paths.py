from pathlib import Path

file = Path("offline/scientific_cell_metrics_utm.py")
code = file.read_text()

# substituir caminhos antigos
code = code.replace(
    "offline/assets/dsm.tif",
    "offline/data/processed/dsm/IPT_2018_DSM_CLIP.tif"
)

code = code.replace(
    "offline/assets/dtm.tif",
    "offline/data/processed/dtm/IPT_2018_DTM_CLIP.tif"
)

file.write_text(code)

print("✅ caminhos de raster corrigidos")
