from pathlib import Path

roots = [
    Path(r"F:\SteamLibrary\steamapps\workshop\content"),
    Path(r"D:\SteamLib\steamapps\workshop\content"),
    Path(r"E:\SteamLibrary\steamapps\workshop\content"),
    Path(r"C:\Program Files (x86)\Steam\steamapps\workshop\content"),
]

for root in roots:
    if not root.exists():
        continue
    print("ROOT", root)
    for app in sorted(root.iterdir()):
        if not app.is_dir():
            continue
        mods = []
        for mod in app.iterdir():
            if not mod.is_dir():
                continue
            if (mod / "metadata.lua").exists() or (mod / "items.lua").exists():
                mods.append(mod)
        if mods:
            print(f"  app {app.name}: {len(mods)} mods")
            for mod in mods[:20]:
                meta = mod / "metadata.lua"
                title = "?"
                if meta.exists():
                    text = meta.read_text(encoding="utf-8", errors="replace")[:2000]
                    for key in ("id", "title", "version"):
                        import re

                        m = re.search(rf"'{key}',\s*\"([^\"]+)\"", text)
                        if m:
                            title += f" {key}={m.group(1)}"
                bandage = (mod / "InventoryItem" / "JAZZ_Bandage.lua").exists()
                print(f"    {mod.name} bandage={bandage} {title}")
