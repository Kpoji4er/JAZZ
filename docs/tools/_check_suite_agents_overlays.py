# -*- coding: utf-8 -*-
"""Check sibling package AGENTS.md overlays against the jazz routing contract."""
from __future__ import annotations

import sys
from pathlib import Path

REQUIRED_NEEDLES = (
    "../jazz/AGENTS.md",
    "../jazz/docs/specs/active/",
    "../jazz/.agents/skills/work-on-jazz-mod/SKILL.md",
    "../jazz/.cursor/rules/jazz-docs-sync.mdc",
)
FORBIDDEN_PATTERNS = (
    ("docs/wiki/", "overlay must not point at docs/wiki/; use jazz-docs-sync.mdc"),
    ("не вед", "overlay still claims wiki/docs are disabled"),
)
PACKAGES = ("jazz_assets", "jazz-units", "jazz-maps", "jazz-nomaps")


def check_overlay(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for needle in REQUIRED_NEEDLES:
        if needle not in text:
            errors.append(f"{path}: missing {needle}")
    lowered = text.lower()
    if "docs/wiki/" in lowered:
        errors.append(f"{path}: {FORBIDDEN_PATTERNS[0][1]}")
    if "не вед" in lowered:
        errors.append(f"{path}: {FORBIDDEN_PATTERNS[1][1]}")
    return errors


def main() -> int:
    jazz_root = Path(__file__).resolve().parents[2]
    mods_root = jazz_root.parent
    errors: list[str] = []
    checked = 0
    for name in PACKAGES:
        overlay = mods_root / name / "AGENTS.md"
        if not overlay.is_file():
            print(f"SKIP {name}: no checkout")
            continue
        checked += 1
        errors.extend(check_overlay(overlay))
    if errors:
        for err in errors:
            print(f"FAIL {err}")
        return 1
    print(f"OK {checked} overlay AGENTS.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
