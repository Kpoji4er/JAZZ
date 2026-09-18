# jazz Code must not bare-read jazz-units JazzAI_* exports.
# Those names live in Mods.Dv3mFVN.env; jazz env asserts "undefined global".
# Bind via JazzAI_BindUnitsExport / rawget(_G, "Name") / JazzAI_UnitsExportNames.
from __future__ import annotations

import re
import sys
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
UNITS = JAZZ.parent / "jazz-units"
COMBAT = JAZZ / "Code" / "CombatAI.lua"
CODE = JAZZ / "Code"


def units_exports() -> list[str]:
    names: list[str] = []
    stance = UNITS / "Code" / "AICombatStance.lua"
    if not stance.is_file():
        return names
    text = stance.read_text(encoding="utf-8")
    for m in re.finditer(r"^function (JazzAI_[A-Za-z0-9_]+)\b", text, re.M):
        names.append(m.group(1))
    return names


def listed_in_combat(combat: str) -> set[str]:
    block = re.search(r"JazzAI_UnitsExportNames\s*=\s*\{(.*?)\n\}", combat, re.S)
    if not block:
        return set()
    return set(re.findall(r'"(JazzAI_[A-Za-z0-9_]+)"', block.group(1)))


def bare_reads(text: str, name: str) -> list[int]:
    safe = {
        f'rawget(_G, "{name}")',
        f"JazzAI_BindUnitsExport(\"{name}\")",
        f'"{name}"',
        f"function {name}",
    }
    hits: list[int] = []
    for i, line in enumerate(text.splitlines(), 1):
        if name not in line:
            continue
        if any(tok in line for tok in safe):
            continue
        if line.lstrip().startswith("--"):
            continue
        if re.search(rf"\b{re.escape(name)}\b", line):
            hits.append(i)
    return hits


def main() -> int:
    combat = COMBAT.read_text(encoding="utf-8")
    failed: list[str] = []
    exports = units_exports()
    if not exports:
        failed.append("no JazzAI_* functions in jazz-units AICombatStance.lua")
    listed = listed_in_combat(combat)
    for name in exports:
        if name not in listed:
            failed.append(f"JazzAI_UnitsExportNames missing {name}")
    if "function JazzAI_BindUnitsExport" not in combat:
        failed.append("JazzAI_BindUnitsExport missing")
    if "function JazzAI_BindAllUnitsExports" not in combat:
        failed.append("JazzAI_BindAllUnitsExports missing")

    for path in CODE.glob("*.lua"):
        text = path.read_text(encoding="utf-8")
        for name in exports:
            for line_no in bare_reads(text, name):
                failed.append(f"{path.name}:{line_no} bare-read {name}")

    if failed:
        print("FAIL: jazz-units export bind")
        for e in failed:
            print(" -", e)
        return 1
    print(f"PASS: {len(exports)} jazz-units JazzAI_* bound, no bare reads")
    return 0


if __name__ == "__main__":
    sys.exit(main())
