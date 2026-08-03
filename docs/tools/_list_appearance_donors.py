"""List appearance donor ids by rough kit category + gender."""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

VAN = Path(
    r"F:\SteamLibrary\steamapps\common\Jagged Alliance 3"
    r"\ModTools\Src\Data\AppearancePreset.lua"
)
JU = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")


def extract_blocks(src: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for needle in ("PlaceObj('AppearancePreset'", "PlaceObj('ModItemAppearancePreset'"):
        i = 0
        while True:
            start = src.find(needle, i)
            if start < 0:
                break
            brace = src.find("{", start)
            depth = 0
            j = brace
            while j < len(src):
                c = src[j]
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        block = src[start : j + 1]
                        m = re.search(r'\bid\s*=\s*"([^"]+)"', block)
                        if m:
                            out[m.group(1)] = block
                        i = j + 1
                        break
                j += 1
            else:
                break
    return out


def field(block: str, key: str) -> str:
    m = re.search(rf'{key}\s*=\s*"([^"]*)"', block)
    return m.group(1) if m else ""


FEMALE_MARK = re.compile(
    r"(?i)(_F_|Female|Buns|Fox|Vicki|Meltdown|Mouse|Livewire|Kalyna|Raven|Scope|"
    r"Fauda|Corazon|Emma|DrMangel|IMP_Female|Head_F_|Equipment(Buns|Fox|Vicki|"
    r"Meltdown|Mouse|Livewire|Kalyna|Raven|Scope|Fauda|Corazon))"
)


def gender(block: str, pid: str) -> str:
    body = field(block, "Body")
    head = field(block, "Head")
    blob = f"{pid}|{body}|{head}"
    if FEMALE_MARK.search(blob):
        return "F"
    return "M"


def category(pid: str, body: str) -> str:
    b = body or ""
    if "Equipment" in b and not any(
        x in b
        for x in (
            "Buns",
            "Fox",
            "Vicki",
            "Meltdown",
            "Mouse",
            "Livewire",
            "Kalyna",
            "Raven",
            "Scope",
            "Fauda",
        )
    ):
        # male AIM or female AIM already caught
        if FEMALE_MARK.search(b):
            return "AIM_F"
        return "AIM_M"
    if FEMALE_MARK.search(b) and "Equipment" in b:
        return "AIM_F"
    if "Faction_Legion" in b or pid.startswith("Legion"):
        return "Legion"
    if "Militia" in b or "Militia" in pid:
        return "Militia"
    if "Rebel" in b or "Rebel" in pid or "Rebels" in pid:
        return "Rebels"
    if "Adonis" in b or "Adonis" in pid:
        return "Adonis"
    if "Army" in b or "Army" in pid or "GrandChien" in pid:
        return "Army"
    if "Thug" in b or "Thug" in pid:
        return "Thugs"
    if "Civ" in b or "Civilian" in pid or "Villager" in pid:
        return "Civ"
    if "IMP" in b or "IMP" in pid:
        return "IMP"
    if b.startswith("Male_") or b.startswith("Female_"):
        return "Generic"
    if "Infected" in b or "Infected" in pid:
        return "Infected"
    return "Other"


def main() -> None:
    blocks = extract_blocks(VAN.read_text(encoding="utf-8"))
    # Prefer vanilla for catalog; still merge jazz for named extras but skip JA12/AME clones
    ju = extract_blocks(JU.read_text(encoding="utf-8"))
    for k, v in ju.items():
        if k.startswith(("JAZZ_AME_", "JAZZ_JA12")) or k in blocks:
            continue
        if re.search(r'group = "JAZZ_JA12"', v):
            continue
        blocks[k] = v

    cats: dict[str, list[str]] = defaultdict(list)
    for pid, b in sorted(blocks.items()):
        body = field(b, "Body")
        g = gender(b, pid)
        cat = category(pid, body)
        cats[f"{cat}/{g}"].append(pid)

    for k in sorted(cats):
        ids = cats[k]
        sample = ", ".join(ids[:20])
        more = f" ...(+{len(ids)-20})" if len(ids) > 20 else ""
        print(f"{k}\t{len(ids)}\t{sample}{more}")


if __name__ == "__main__":
    main()
