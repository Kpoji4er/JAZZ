"""Bump metadata version + prepend last_changes with \\n escape only."""
from pathlib import Path
import re

def bump(path: Path, bullet: str) -> None:
    t = path.read_text(encoding="utf-8")
    m = re.search(r"'version',\s*(\d+),", t)
    if not m:
        raise SystemExit(f"no version in {path}")
    new_ver = int(m.group(1)) + 1
    t = t[: m.start(1)] + str(new_ver) + t[m.end(1) :]
    mm = re.search(r"('last_changes',\s*\")", t)
    if not mm:
        raise SystemExit(f"no last_changes in {path}")
    esc = "- " + bullet + "\\n"
    t = t[: mm.end(1)] + esc + t[mm.end(1) :]
    # verify no raw LF inside last_changes value start
    path.write_text(t, encoding="utf-8")
    print(f"{path.parent.name}: version={new_ver}")


if __name__ == "__main__":
    bump(
        Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-maps\metadata.lua"),
        "QUESTS-003: Flag Hill villa counterattack (move Attackers, Ernie30, Wave2) [new game recommended]",
    )
    bump(
        Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\metadata.lua"),
        "QUESTS-003: VillaAttackers_Ernie base 30 for Flag Hill siege [new game recommended]",
    )
