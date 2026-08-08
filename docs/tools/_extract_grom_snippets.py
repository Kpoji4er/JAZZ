from pathlib import Path
import re

t = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua").read_text(encoding="utf-8")
out = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz\docs\tools\_grom_snippets")
out.mkdir(exist_ok=True)

pat_loot = (
    r"PlaceObj\('ModItemLootDef', \{\s*"
    r"Comment = \"merc\",\s*"
    r"group = \"Mercs\",\s*"
    r"id = \"%s\",.*?\n\t\t\t\t\}\),"
)

for tid in ("Loot_JAZZ_Grom", "JAZZ_Grom50", "JAZZ_Grom35", "JAZZ_Grom25", "JAZZ_Grom20"):
    m = re.search(pat_loot % tid, t, flags=re.S)
    (out / ("%s.lua.txt" % tid)).write_text(m.group(0) if m else "FAIL", encoding="utf-8")
    print(tid, bool(m), "len", len(m.group(0)) if m else 0)

idx = t.find("PlaceObj('ModItemFolder', {\n\t\t\t\t'name', \"Jazz_Grom\",")
print("folder idx", idx)
rest = t[idx + 10 :]
nxt = rest.find("\n\t\t\tPlaceObj('ModItemFolder', {")
print("next folder relative", nxt)
block = t[idx : idx + 10 + nxt]
(out / "Jazz_Grom_folder.lua.txt").write_text(block, encoding="utf-8")
print("folder len", len(block))

m = re.search(
    r"PlaceObj\('ModItemAppearancePreset', \{.*?^\t\tid = \"Grom\",\n\t\}\),",
    t,
    flags=re.M | re.S,
)
(out / "Appearance_Grom.lua.txt").write_text(m.group(0) if m else "FAIL", encoding="utf-8")
print("appearance", bool(m), "len", len(m.group(0)) if m else 0)
