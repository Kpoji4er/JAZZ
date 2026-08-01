"""After salary commit: restore WIP overlays and re-apply temporarily reverted AUG rename."""
from __future__ import annotations

import re
from pathlib import Path

JAZZ = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")


def ensure_bullet_and_version(path: Path, min_ver: int, bullet: str) -> None:
    t = path.read_text(encoding="utf-8")
    m = re.search(r"'version',\s*(\d+)", t)
    if not m:
        raise SystemExit(f"no version in {path}")
    ver = int(m.group(1))
    if ver < min_ver:
        t = re.sub(r"'version',\s*\d+", f"'version', {min_ver}", t, count=1)
        print(f"{path.parent.name}: version -> {min_ver}")
    else:
        print(f"{path.parent.name}: version {ver}")
    if bullet not in t:
        t = t.replace("'last_changes', '", f"'last_changes', '- {bullet}\\n", 1)
        print(f"{path.parent.name}: appended last_changes bullet")
    else:
        print(f"{path.parent.name}: last_changes already has bullet")
    path.write_text(t, encoding="utf-8")


def restore(src: Path, dst: Path) -> bool:
    if not src.exists():
        print(f"no backup {src.name}")
        return False
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    src.unlink()
    print(f"restored {dst}")
    return True


def main() -> None:
    # jazz backups may already be restored
    restore(JAZZ / "Russian.csv.wip_salary_commit", JAZZ / "Russian.csv")
    restore(JAZZ / "docs" / "tools" / "README.md.wip_salary_commit", JAZZ / "docs" / "tools" / "README.md")
    if restore(JAZZ / "metadata.lua.wip_salary_commit", JAZZ / "metadata.lua"):
        ensure_bullet_and_version(
            JAZZ / "metadata.lua",
            5949,
            "Docs/loc: Madman/Grom/Hitman paid hire; AIM chat no longer claims free",
        )
    else:
        ensure_bullet_and_version(
            JAZZ / "metadata.lua",
            5949,
            "Docs/loc: Madman/Grom/Hitman paid hire; AIM chat no longer claims free",
        )

    if restore(UNITS / "metadata.lua.wip_salary_commit", UNITS / "metadata.lua"):
        ensure_bullet_and_version(
            UNITS / "metadata.lua",
            2250,
            "Paid hire for Madman/Grom/Hitman (fix StartingSalary=0 div0 on AIM)",
        )
    else:
        ensure_bullet_and_version(
            UNITS / "metadata.lua",
            2250,
            "Paid hire for Madman/Grom/Hitman (fix StartingSalary=0 div0 on AIM)",
        )

    # Re-apply AUG rename that was temporarily reverted for a clean commit.
    items = UNITS / "items.lua"
    t = items.read_text(encoding="utf-8")
    plain = t.count('"AUGCompensator_03"')
    jazzed = t.count('"JAZZ_AUGCompensator_03"')
    print(f"AUG counts plain={plain} jazz={jazzed}")
    if plain > 0:
        # Restore the first plain occurrence (the one we reverted).
        t2 = t.replace('"AUGCompensator_03"', '"JAZZ_AUGCompensator_03"', 1)
        items.write_text(t2, encoding="utf-8")
        print("re-applied JAZZ_AUGCompensator_03 rename (1)")
    else:
        print("no plain AUGCompensator_03 to restore")


if __name__ == "__main__":
    main()
