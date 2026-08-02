# -*- coding: utf-8 -*-
from pathlib import Path

t = Path(r"C:/Users/SsAnd/AppData/Roaming/Jagged Alliance 3/Mods/jazz/items.lua").read_text(encoding="utf-8")
for i in ("Jazz_Perk_Mimicry", "Jazz_Perk_Veteran", "Jazz_Perk_Sniper"):
    key = f"'Id', \"{i}\""
    idx = t.find(key)
    print(i, "MISSING" if idx < 0 else "OK")
    if idx >= 0:
        chunk = t[idx : idx + 550]
        for icon in ("Bond", "Teacher", "Deadeye", "DeathFromAbove"):
            if f"UI/Icons/Perks/{icon}" in chunk:
                print("  icon:", icon)
