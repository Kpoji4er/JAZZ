from pathlib import Path

t = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua").read_text(encoding="utf-8")
for needle in ['id = "Loot_JAZZ_Grom"', 'id = "JAZZ_Grom50"', 'id = "JAZZ_Grom20"', "'name', \"Jazz_Grom\""]:
    idx = t.find(needle)
    print("===", needle, "at", idx)
    if idx >= 0:
        print(t[max(0, idx - 100) : idx + 450])
        print()
