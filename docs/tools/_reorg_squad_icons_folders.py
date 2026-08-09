# Reorganize SquadsIcons/Enemy into faction subfolders.
# Run from jazz/: python docs/tools/_reorg_squad_icons_folders.py

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENEMY = ROOT / "SquadsIcons" / "Enemy"

FACTIONS = ("legion", "army", "adonis", "rebels", "smugglers")

SHIELDS = {
    "legion.png",
    "army.png",
    "army2.png",
    "army3.png",
    "adonis.png",
    "rebels.png",
    "rebels2.png",
    "rebels3.png",
    "smugglers.png",
}

MISC = {
    "enemy_squad.png",
    "enemy_squad.psd",
    "nazi.png",
}


def main() -> int:
    if not ENEMY.is_dir():
        print(f"FAIL: missing {ENEMY}")
        return 1

    shields_dir = ENEMY / "_shields"
    misc_dir = ENEMY / "_misc"
    shields_dir.mkdir(exist_ok=True)
    misc_dir.mkdir(exist_ok=True)
    for fac in FACTIONS:
        (ENEMY / fac).mkdir(exist_ok=True)

    moved = 0
    skipped = 0
    for path in sorted(ENEMY.iterdir()):
        if not path.is_file():
            continue
        name = path.name
        dest = None
        if name in SHIELDS:
            dest = shields_dir / name
        elif name in MISC:
            dest = misc_dir / name
        else:
            for fac in FACTIONS:
                prefix = f"{fac}_"
                if name.startswith(prefix) and name.endswith("_squad.png"):
                    dest = ENEMY / fac / name
                    break
        if dest is None:
            print(f"SKIP unknown: {name}")
            skipped += 1
            continue
        if dest.resolve() == path.resolve():
            continue
        if dest.exists():
            print(f"SKIP exists: {dest.relative_to(ROOT)}")
            skipped += 1
            continue
        shutil.move(str(path), str(dest))
        print(f"MOVE {name} -> {dest.relative_to(ROOT).as_posix()}")
        moved += 1

    print(f"OK moved={moved} skipped={skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
