# -*- coding: utf-8 -*-
from pathlib import Path
import re

root = Path(r"F:/SteamLibrary/steamapps/common/Jagged Alliance 3/ModTools/Src/Data/CharacterEffectCompositeDef")
for p in sorted(root.glob("*.lua")):
    t = p.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"'Icon',\s*\"([^\"]+)\"", t)
    if m:
        print(f"{p.stem}: {m.group(1)}")
