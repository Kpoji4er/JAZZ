"""Audit JA12 Jazz merc AppearancesList vs shipped/vanilla presets + gender lock."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")
JAZZ = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
MAP = JAZZ / "docs" / "design" / "mercs-ja12" / "ja12-appearance-map.json"
VANILLA_AP = Path(
    r"F:\SteamLibrary\steamapps\common\Jagged Alliance 3"
    r"\ModTools\Src\Data\AppearancePreset.lua"
)

VANILLA_OK = {"Biff", "Hitman", "Shadow"}


def preset_ids(text: str) -> set[str]:
    return set(re.findall(r'\bid\s*=\s*"([^"]+)"', text))


def gender_of_mesh(name: str) -> str | None:
    n = name or ""
    if not n:
        return None
    if re.search(
        r"(?i)(_F_|Female|Buns|Fox|Vicki|Meltdown|Mouse|Livewire|Kalyna|Raven|Scope|"
        r"Fauda|Corazon|Emma|DrMangel|IMP_Female|Head_F_|Equipment(Buns|Fox|Vicki|"
        r"Meltdown|Mouse|Livewire|Kalyna|Raven|Scope|Fauda|Corazon))",
        n,
    ):
        return "Female"
    if re.search(r"(?i)(_M_|Male_|IMP_Male|Head_M_|Equipment)", n):
        return "Male"
    if n.startswith("Head_"):
        return "Female" if n.startswith("Head_F_") else "Male"
    return None


def block_for_id(section: str, pid: str) -> str | None:
    im = re.search(rf'\tid = "{re.escape(pid)}",', section)
    if not im:
        return None
    needle = "PlaceObj('ModItemAppearancePreset'"
    start = section.rfind(needle, 0, im.start())
    if start < 0:
        return None
    return section[start : im.end()]


def main() -> int:
    items = (UNITS / "items.lua").read_text(encoding="utf-8")
    m = re.search(
        r"-- JAZZ-UNITS-002-JA12-APP-BEGIN([\s\S]*?)-- JAZZ-UNITS-002-JA12-APP-END",
        items,
    )
    section = m.group(1) if m else ""
    shipped = preset_ids(section)
    all_mod = preset_ids(items)
    vanilla = preset_ids(VANILLA_AP.read_text(encoding="utf-8")) if VANILLA_AP.exists() else set()
    known = all_mod | vanilla | VANILLA_OK

    recipes = json.loads(MAP.read_text(encoding="utf-8")) if MAP.exists() else {}

    gender_bad = []
    for pid in sorted(shipped):
        block = block_for_id(section, pid)
        if not block:
            gender_bad.append((pid, "block not found"))
            continue
        body = re.search(r'Body\s*=\s*"([^"]*)"', block)
        head = re.search(r'Head\s*=\s*"([^"]*)"', block)
        expect = (recipes.get(pid) or {}).get("gender")
        bg = gender_of_mesh(body.group(1) if body else "")
        hg = gender_of_mesh(head.group(1) if head else "")
        if expect and bg and bg != expect:
            gender_bad.append((pid, f"Body {body.group(1)}={bg} expect {expect}"))
        if expect and hg and hg != expect:
            gender_bad.append((pid, f"Head {head.group(1)}={hg} expect {expect}"))
        if bg and hg and bg != hg:
            gender_bad.append((pid, f"mixed {bg}/{hg}"))

    link_bad = []
    link_ok = []
    for path in sorted((UNITS / "UnitData").glob("Jazz_*.lua")):
        if path.name.startswith(("JAZZ_AME", "JAZZ_Legion")) or path.stem.startswith(
            "Jazz_Recruter"
        ):
            continue
        text = path.read_text(encoding="utf-8")
        presets = re.findall(r"'Preset',\s*\"([^\"]+)\"", text)
        if not presets:
            if "AppearancesList" not in text:
                link_bad.append((path.name, "<no AppearancesList>"))
            continue
        for p in presets:
            if p in known:
                link_ok.append((path.stem, p))
            else:
                link_bad.append((path.name, p))

    print(
        f"shipped_ja12={len(shipped)} link_ok={len(link_ok)} "
        f"link_bad={len(link_bad)} gender_bad={len(gender_bad)}"
    )
    for x in link_bad:
        print("LINK_BAD", x)
    for x in gender_bad:
        print("GENDER_BAD", x)
    combos = [
        k
        for k, v in recipes.items()
        if not v.get("handcrafted_kept") and v.get("body_donor") != v.get("head_donor")
    ]
    print("combos", len(combos), combos)
    return 1 if link_bad or gender_bad else 0


if __name__ == "__main__":
    sys.exit(main())
