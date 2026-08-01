"""Wire M72LAW InventoryItem Icon → WeaponIcons/M72LAW.png."""
from __future__ import annotations

import os
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
COMPANION = ROOT / "InventoryItem" / "M72LAW.lua"
ICON = 'Icon = "Mod/e6L4ECj/WeaponIcons/M72LAW.png",'
ICON_LINE = f"\t{ICON}\n"


def patch_items(text: str) -> str:
    needle = "'Id', \"M72LAW\","
    i = text.find(needle)
    if i < 0:
        raise SystemExit("M72LAW missing in items.lua")
    # find end of this PlaceObj props (before next }),)
    # insert Icon after Entity if absent
    chunk_end = text.find("}),", i)
    chunk = text[i:chunk_end]
    if "WeaponIcons/M72LAW" in chunk:
        print("items: already")
        return text
    ent = "'Entity', \"M72LAW2\","
    if ent not in chunk:
        raise SystemExit("Entity needle missing")
    new_chunk = chunk.replace(ent, ent + "\n\t\t\t\t\t" + ICON, 1)
    print("items: ok")
    return text[:i] + new_chunk + text[chunk_end:]


def patch_companion(text: str) -> str:
    if "WeaponIcons/M72LAW" in text:
        print("companion: already")
        return text
    # after Entity line
    old = '\tEntity = "M72LAW2",\n'
    if old not in text:
        raise SystemExit("companion Entity missing")
    print("companion: ok")
    return text.replace(old, old + ICON_LINE, 1)


def atomic_write(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    for _ in range(25):
        try:
            os.replace(tmp, path)
            return
        except OSError:
            time.sleep(0.3)
    raise SystemExit(f"locked {path}")


def main() -> None:
    atomic_write(ITEMS, patch_items(ITEMS.read_text(encoding="utf-8")))
    atomic_write(COMPANION, patch_companion(COMPANION.read_text(encoding="utf-8")))
    print("done")


if __name__ == "__main__":
    main()
