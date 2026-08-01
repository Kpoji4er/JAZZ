# -*- coding: utf-8 -*-
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _apply_attach_001 import placeobj_blocks, prop

ROOT = Path(__file__).resolve().parents[2]
t = (ROOT / "items.lua").read_text(encoding="utf-8")

for b in placeobj_blocks(t, "ModItemWeaponComponent"):
    cid = prop(b.text, "id") or ""
    if not cid.startswith("JAZZ_Mag"):
        continue
    cost_m = re.search(r"Cost = (-?\d+)", b.text)
    diff_m = re.search(r"ModificationDifficulty = (-?\d+)", b.text)
    fx_m = re.search(r"ModificationEffects = \{(.*?)\},", b.text, re.S)
    fx = re.findall(r'"([A-Za-z0-9_]+)"', fx_m.group(1) if fx_m else "")
    params = {}
    for m in re.finditer(r"'Name', \"([^\"]+)\"[\s\S]*?'Value', (-?\d+)", b.text):
        params[m.group(1)] = int(m.group(2))
    dn = re.search(r'DisplayName = T\([^,]+,.*?\"([^\"]*)\"\)', b.text, re.S)
    print(
        f"{cid}|{dn.group(1) if dn else ''}|"
        f"cost={cost_m.group(1) if cost_m else ''}|"
        f"diff={diff_m.group(1) if diff_m else ''}|"
        f"fx={';'.join(fx)}|params={params}"
    )
