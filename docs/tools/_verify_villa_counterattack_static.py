from pathlib import Path
import re
p = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")
t = p.read_text(encoding="utf-8")
idx = t.find('id = "JAZZ_Legion_VillaAttackers_Ernie"')
start = t.rfind("PlaceObj('ModItemEnemySquads'", 0, idx)
block = t[start:idx]
mins = [int(x) for x in re.findall(r"'UnitCountMin', (\d+)", block)]
print("ernie slots", mins, "sum", sum(mins))
o = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-maps\Maps\gsSMikN\objects.lua").read_text(encoding="utf-8")
print("VillaSiege_Wave2 count", o.count("VillaSiege_Wave2"))
# remaining HouseAmbushers AdvanceTo Emma
count = 0
for m in re.finditer(r"PlaceObj\('UnitMarker',", o):
    pass
# crude
ha = 0
i = 0
while True:
    s = o.find("PlaceObj('UnitMarker'", i)
    if s < 0:
        break
    brace = o.find("{", s)
    depth = 0
    j = brace
    while j < len(o):
        if o[j] == "{":
            depth += 1
        elif o[j] == "}":
            depth -= 1
            if depth == 0:
                j += 1
                break
        j += 1
    body = o[s:j]
    if "HouseAmbushers" in body and "AdvanceTo" in body and "EmmaAndCorazon" in body and "Adonis" not in body and "'Legion'" in body:
        ha += 1
    i = j
print("old siege remaining", ha)
