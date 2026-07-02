from pathlib import Path
import re

file = Path("offline/scientific_cell_metrics_utm.py")
code = file.read_text()

# substitui definição de DSM_LOCAL
code = re.sub(
    r'DSM_LOCAL\s*=.*',
    'DSM_LOCAL = "offline/data/processed/dsm/IPT_2018_DSM_CLIP.tif"',
    code
)

# substitui definição de DTM_LOCAL
code = re.sub(
    r'DTM_LOCAL\s*=.*',
    'DTM_LOCAL = "offline/data/processed/dtm/IPT_2018_DTM_CLIP.tif"',
    code
)

file.write_text(code)

print("✅ DSM/DTM paths corrigidos definitivamente")
