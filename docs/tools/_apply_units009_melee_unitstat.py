from pathlib import Path

root = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
ids = [
    "Machete",
    "Machete_Balanced",
    "Machete_Sharpened",
    "PierreMachete",
    "Bayonet",
    "Trench_Shovel",
    "Unarmed",
]
old = 'UnitStat = "Dexterity"'
new = 'UnitStat = "Strength"'
for name in ids:
    p = root / "InventoryItem" / f"{name}.lua"
    t = p.read_text(encoding="utf-8")
    if old not in t:
        print("NO COMP", name)
        continue
    p.write_text(t.replace(old, new, 1), encoding="utf-8")
    print("comp", name)

text = (root / "items.lua").read_text(encoding="utf-8")
old_i = "'UnitStat', \"Dexterity\""
new_i = "'UnitStat', \"Strength\""
n = 0
for iid in ids:
    needle = f"'Id', \"{iid}\""
    pos = 0
    found = False
    while True:
        i = text.find(needle, pos)
        if i < 0:
            break
        window = text[i : i + 2500]
        j = window.find(old_i)
        if j >= 0:
            absj = i + j
            text = text[:absj] + new_i + text[absj + len(old_i) :]
            n += 1
            found = True
            break
        pos = i + len(needle)
    if not found:
        print("NO ITEMS", iid)
print("items replacements", n)
(root / "items.lua").write_text(text, encoding="utf-8")
