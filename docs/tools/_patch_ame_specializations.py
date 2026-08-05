#!/usr/bin/env python3
"""Patch AME UnitData Specialization from roster generator (no salary/loc regen).

Keeps StartingSalary and other post-apply fields intact.
Source of truth: docs/tools/_gen_ame_roster_60.py ROSTER.
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UNITS = ROOT.parent / "jazz-units"
ROSTER_SCRIPT = Path(__file__).resolve().parent / "_gen_ame_roster_60.py"


def load_roster():
    spec = importlib.util.spec_from_file_location("gen_ame_roster_60", ROSTER_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load roster generator")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.ROSTER


def patch_companion(path: Path, new_spec: str) -> bool:
    text = path.read_text(encoding="utf-8")
    new_text, n = re.subn(
        r'Specialization\s*=\s*"[^"]*"',
        f'Specialization = "{new_spec}"',
        text,
        count=1,
    )
    if n != 1:
        raise RuntimeError(f"{path.name}: Specialization field not found")
    if new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def patch_items(items_path: Path, expected: dict[str, str]) -> int:
    text = items_path.read_text(encoding="utf-8")
    changed = 0
    for uid, new_spec in expected.items():
        # Match Specialization inside that unit's ModItemUnitDataCompositeDef block.
        pattern = re.compile(
            rf"('Id',\s*\"{re.escape(uid)}\".*?'Specialization',\s*\")([^\"]+)(\")",
            re.S,
        )

        def repl(m: re.Match[str], spec: str = new_spec) -> str:
            nonlocal changed
            if m.group(2) != spec:
                changed += 1
            return m.group(1) + spec + m.group(3)

        text, n = pattern.subn(repl, text, count=1)
        if n != 1:
            raise RuntimeError(f"items.lua: could not patch Specialization for {uid}")
    items_path.write_text(text, encoding="utf-8")
    return changed


def main() -> int:
    roster = load_roster()
    expected = {f"JAZZ_AME_{i:02d}": m["spec"] for i, m in enumerate(roster, 1)}
    unit_dir = UNITS / "UnitData"
    companion_changed = 0
    for uid, spec in expected.items():
        path = unit_dir / f"{uid}.lua"
        if not path.is_file():
            raise RuntimeError(f"missing companion {path}")
        if patch_companion(path, spec):
            companion_changed += 1
    items_changed = patch_items(UNITS / "items.lua", expected)
    print(f"companions updated: {companion_changed}/{len(expected)}")
    print(f"items.lua Specialization fields rewritten: {items_changed}")
    # Quick audit
    bad_line = []
    bad_spec = []
    line_ok = {"AllRounder", "Autoriflemen", "HeavyWeapons", "Marksmen"}
    spec_ok = {"Doctor", "Leader", "Marksmen", "ExplosiveExpert", "Mechanic"}
    for i, m in enumerate(roster, 1):
        uid = f"JAZZ_AME_{i:02d}"
        if m["cat"] == "Specialists":
            if m["spec"] not in spec_ok:
                bad_spec.append((uid, m["role"], m["spec"]))
        elif m["spec"] not in line_ok:
            bad_line.append((uid, m["cat"], m["role"], m["spec"]))
    if bad_line or bad_spec:
        print("AUDIT FAIL", bad_line, bad_spec)
        return 1
    print("audit OK: line/specialist specialization sets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
