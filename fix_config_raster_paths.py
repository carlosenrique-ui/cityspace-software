from pathlib import Path
import re

file = Path("config/system_paths.py")
code = file.read_text()

code = re.sub(
    r'DSM_LOCAL\s*=.*',
    'DSM_LOCAL = "offline/data/processed/dsm/IPT_2018_DSM_CLIP.tif"',
    code
)

code = re.sub(
    r'DTM_LOCAL\s*=.*',
    'DTM_LOCAL = "offline/data/processed/dtm/IPT_2018_DTM_CLIP.tif"',
    code
)

file.write_text(code)

print("✅ config.system_paths corrigido")
