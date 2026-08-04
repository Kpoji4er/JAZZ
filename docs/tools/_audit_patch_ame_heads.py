#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit/repair AME AppearancePresets: gender heads/hats, pale heads, skin, Legion war-paint.

Disk source of truth: jazz-units/items.lua ModItemAppearancePreset id=JAZZ_AME_NN.
Asset policy: docs/design/ame-appearance-assets.md

After repair, next mod load / game launch picks up correct Body/Head/Hat/BodyColor.
Optional: --sync-map updates docs/design/ame-appearance-map.json head_swap from items.

Usage:
  python docs/tools/_audit_patch_ame_heads.py --dry-run
  python docs/tools/_audit_patch_ame_heads.py
  python docs/tools/_audit_patch_ame_heads.py --sync-map
  python docs/tools/_audit_patch_ame_heads.py --verbose
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
ITEMS = JAZZ.parent / "jazz-units" / "items.lua"
MAP_PATH = JAZZ / "docs" / "design" / "ame-appearance-map.json"

# Narrow Af male bank — player-verified dark African meshes only.
# NEVER: Flay/Fidel/Magic/Blood (AIM, read Caucasian), Fauda/Lami (female), Omryn (Asian).
MALE_HEADS = [
    "Head_Chimurenga",
    "Head_Pierre",
    "Head_Jackhammer",
    "Head_M_IMP_01",
    "Faction_Rebels_M_HeadMedic",
]

# AIM / named heads that look pale/Caucasian/wrong on AME (even if historically banked).
REJECTED_MALE_HEADS = {
    "Head_Flay",
    "Head_Fidel",
    "Head_Magic",
    "Head_Blood",
    "Head_Omryn",
    "Head_Fauda",
    "Head_Lami",
}

FEMALE_HEADS = {
    "Head_Fauda",
    "Head_Lami",
    "Head_Buns",
    "Head_Fox",
    "Head_Meltdown",
    "Head_Mouse",
    "Head_Livewire",
    "Head_Kalyna",
    "Head_Scope",
    "Head_Vicki",
    "Head_Raven",
}

FEMALE_HEAD_BANK = [f"Head_F_Af_NPC_{i:02d}" for i in range(1, 11)]
FEMALE_HAT = "NPCCostumeFemale_Hat_01"

SAFE_MALE_PANTS = [
    "Faction_Militia_Bottom_01",
    "Faction_Rebels_Bottom_01",
    "Faction_GrandChien_Bottom_03",
]
FEMALE_PANTS = "Female_Pants_01"

# Dark African skin (BodyColor EditableColor1). Same bank as _gen_ame_appearances.py.
SKIN_BANK = [
    (6, 2, 1),
    (8, 3, 1),
    (10, 4, 2),
    (12, 5, 2),
    (14, 5, 3),
    (16, 5, 5),
    (17, 6, 3),
    (18, 7, 4),
    (19, 8, 4),
    (20, 7, 3),
]

# Bodies whose exposed arms/hands stay pale despite dark BodyColor C1 (player reports).
PALE_HAND_BODIES = {
    "Faction_GrandChien_Top_05",
}

# Pale / Caucasian / Asian / generic heads that must be swapped on AME.
PALE_HEAD_RE = re.compile(
    r"^Head_(M|F)_(Ca|As|Senior)_"
    r"|^Male_Head_"
    r"|^Female_Head_"
    r"|^Head_(Barry|Ivan|MD|Ice|Grizzly|Igor|Tex|Scully|Steroid|DrQ|Gus|Len|Larry|"
    r"Red|Thor|Wolf|Sidney|Nails|Hitman|Grunty|Spike|Raider|Razor|Reaper|Biff|Lynx|"
    r"Shadow|Faucheux|Major|Livewire|Kalyna|Scope|Vicki|Buns|Fox|Meltdown|Mouse)$",
    re.I,
)

WARPAINT_BODY_RE = re.compile(
    r"Faction_Legion_Top_"
    r"|Faction_Legion_.*Paint"
    r"|_WarPaint"
    r"|Legion_Top_0[1-9]",
    re.I,
)

BAD_GEAR_RE = re.compile(r"Omryn|Fauda|Lami", re.I)

SAFE_MALE_BODIES = [
    "Faction_Militia_Top_02",
    "Faction_Militia_Top_03",
    "Faction_Rebels_Top_Comander",
    "Faction_GrandChien_Top_02",
    "Faction_GrandChien_Top_03",
    "Faction_Adonis_Top_01",
]

# Reported mercs — always print in summary.
FOCUS = {
    "JAZZ_AME_03",  # Ibrahim
    "JAZZ_AME_04",
    "JAZZ_AME_06",  # Moussa
    "JAZZ_AME_08",  # Thabo
    "JAZZ_AME_16",  # João
    "JAZZ_AME_20",  # Idrissa
    "JAZZ_AME_23",
    "JAZZ_AME_27",  # Sekou
    "JAZZ_AME_28",
    "JAZZ_AME_31",
    "JAZZ_AME_33",  # Claude (hands)
    "JAZZ_AME_34",  # Emeka
    "JAZZ_AME_38",
    "JAZZ_AME_40",  # Abraham
}


def slot_num(aid: str) -> int:
    m = re.search(r"(\d+)$", aid)
    return int(m.group(1)) if m else 1


def skin_for(aid: str) -> tuple[int, int, int]:
    return SKIN_BANK[(slot_num(aid) - 1) % len(SKIN_BANK)]


def is_female_body(bod: str) -> bool:
    return "Female" in (bod or "")


def is_female_head(head: str) -> bool:
    return head.startswith("Head_F_") or head in FEMALE_HEADS


def is_male_hat(hat: str) -> bool:
    return bool(hat) and ("Male" in hat or hat.startswith("FactionMale"))


def is_warpaint_body(bod: str) -> bool:
    if not bod:
        return False
    if "Legion" in bod and "Top" in bod:
        return True
    return bool(WARPAINT_BODY_RE.search(bod))


def is_pale_head(head: str) -> bool:
    if not head:
        return True
    if head in REJECTED_MALE_HEADS:
        return True
    if head.startswith("Head_F_Af_NPC_"):
        return False
    if head in set(MALE_HEADS):
        return False
    if head.startswith("Faction_Legion_Head_"):
        return True
    return bool(PALE_HEAD_RE.match(head))


def parse_ame_chunks(text: str) -> list[tuple[str, str]]:
    parts = text.split("PlaceObj('ModItemAppearancePreset', {")
    out = []
    for chunk in parts[1:]:
        id_m = re.search(r'\bid = "(JAZZ_AME_\d+)"', chunk)
        if id_m:
            out.append((id_m.group(1), chunk))
    return out


def fields(chunk: str, aid: str) -> dict[str, str]:
    id_m = re.search(rf'\bid = "{re.escape(aid)}"', chunk)
    head_part = chunk[: id_m.start()] if id_m else chunk

    def g(key: str) -> str:
        m = re.search(rf'\b{key} = "([^"]*)"', head_part)
        return m.group(1) if m else ""

    bc1 = ""
    bcm = re.search(
        r"BodyColor = PlaceObj\('ColorizationPropSet',\s*\{"
        r"\s*'EditableColor1',\s*RGBA\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)",
        head_part,
    )
    if bcm:
        bc1 = f"RGBA({bcm.group(1)}, {bcm.group(2)}, {bcm.group(3)}, {bcm.group(4)})"

    return {
        "Head": g("Head"),
        "Hat": g("Hat"),
        "Hat2": g("Hat2"),
        "Body": g("Body"),
        "Pants": g("Pants"),
        "Shirt": g("Shirt"),
        "BodyC1": bc1,
        "BodyC1_rgb": (
            (int(bcm.group(1)), int(bcm.group(2)), int(bcm.group(3))) if bcm else None
        ),
    }


def body_c1_too_pale(rgb: tuple[int, int, int] | None) -> bool:
    """True if BodyColor C1 missing or brighter than darkest SKIN_BANK entry."""
    if not rgb:
        return True
    r, g, b = rgb
    # SKIN_BANK max channel is 20 — anything clearly above is not forced dark African.
    return r > 28 or g > 16 or b > 12


def collect_issues(f: dict[str, str]) -> list[str]:
    head, hat, bod, pants = f["Head"], f["Hat"], f["Body"], f["Pants"]
    issues: list[str] = []
    if not is_female_body(bod) and is_female_head(head):
        issues.append("female_head_on_male")
    if is_female_body(bod) and is_male_hat(hat):
        issues.append("male_hat_on_female")
    if is_pale_head(head) and not is_female_head(head):
        if is_female_body(bod):
            if not head.startswith("Head_F_Af_NPC_"):
                issues.append("pale_or_bad_female_head")
        else:
            issues.append("pale_or_bad_male_head")
    if is_female_body(bod) and head and not head.startswith("Head_F_Af_NPC_") and head not in FEMALE_HEADS:
        if is_pale_head(head) or head.startswith("Head_M_") or head.startswith("Male_"):
            issues.append("pale_or_bad_female_head")
    if not is_female_body(bod) and is_warpaint_body(bod):
        issues.append("warpaint_body")
    if head.startswith("Faction_Legion_Head_"):
        issues.append("warpaint_head")
    if hat and BAD_GEAR_RE.search(hat):
        issues.append("bad_hat_gear")
    if pants and BAD_GEAR_RE.search(pants):
        issues.append("bad_pants_gear")
    if not is_female_body(bod) and bod in PALE_HAND_BODIES:
        issues.append("pale_hand_body")
    if not is_female_body(bod) and body_c1_too_pale(f.get("BodyC1_rgb")):
        issues.append("pale_body_skin")
    # Gloves that hide/fake pale hands — strip so Body skin shows.
    shirt = f.get("Shirt") or ""
    if not is_female_body(bod) and shirt and re.search(r"Glove", shirt, re.I):
        issues.append("gloves_shirt")
    return issues


def reaudit_issues(f: dict[str, str]) -> list[str]:
    """Stricter post-write checks."""
    head, hat, bod, pants = f["Head"], f["Hat"], f["Body"], f["Pants"]
    issues: list[str] = []
    if not is_female_body(bod) and is_female_head(head):
        issues.append("female_head_on_male")
    if is_female_body(bod) and is_male_hat(hat):
        issues.append("male_hat_on_female")
    if not is_female_body(bod) and (
        is_pale_head(head) or head.startswith("Faction_Legion_Head_") or head in REJECTED_MALE_HEADS
    ):
        issues.append("pale_or_bad_male_head")
    if is_female_body(bod) and not head.startswith("Head_F_Af_NPC_"):
        issues.append("non_af_female_head")
    if not is_female_body(bod) and is_warpaint_body(bod):
        issues.append("warpaint_body")
    if not is_female_body(bod) and bod in PALE_HAND_BODIES:
        issues.append("pale_hand_body")
    if not is_female_body(bod) and body_c1_too_pale(f.get("BodyC1_rgb")):
        issues.append("pale_body_skin")
    if hat and BAD_GEAR_RE.search(hat):
        issues.append("bad_hat_gear")
    if pants and BAD_GEAR_RE.search(pants):
        issues.append("bad_pants_gear")
    return issues


def force_body_c1(chunk: str, aid: str) -> str:
    sr, sg, sb = skin_for(aid)
    new, n = re.subn(
        r"(BodyColor = PlaceObj\('ColorizationPropSet',\s*\{\s*'EditableColor1',\s*)"
        r"RGBA\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)",
        rf"\1RGBA({sr}, {sg}, {sb}, 255)",
        chunk,
        count=1,
    )
    if n:
        return new
    # Insert BodyColor after Body = "..." if missing.
    id_pos = chunk.find(f'id = "{aid}"')
    head = chunk[:id_pos] if id_pos >= 0 else chunk
    if re.search(r'\bBody = "[^"]*"', head) and "BodyColor" not in head:
        return re.sub(
            r'(\bBody = "[^"]*"\s*,)',
            rf"\1\n\t\t\tBodyColor = PlaceObj('ColorizationPropSet', {{\n"
            rf"\t\t\t'EditableColor1', RGBA({sr}, {sg}, {sb}, 255),\n"
            rf"\t\t\t'EditableColor2', RGBA(34, 38, 44, 255),\n"
            rf"\t\t\t'EditableColor3', RGBA(0, 0, 0, 255),\n"
            rf"\t\t\t}}),",
            chunk,
            count=1,
        )
    return chunk


def force_head_color_black(chunk: str, aid: str) -> str:
    id_m = re.search(rf'\bid = "{re.escape(aid)}"', chunk)
    hp = chunk[: id_m.start()] if id_m else chunk
    if "HeadColor" not in hp:
        return chunk
    return re.sub(
        r"(HeadColor = PlaceObj\('ColorizationPropSet',\s*\{\s*'EditableColor1',\s*)"
        r"RGBA\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)",
        r"\1RGBA(0, 0, 0, 255)",
        chunk,
        count=1,
    )


def sync_map(presets: dict[str, str]) -> None:
    raw = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    slots = raw["slots"] if isinstance(raw, dict) and "slots" in raw else raw
    changed = 0
    for s in slots:
        aid = s.get("id")
        if not aid or aid not in presets:
            continue
        new_h = presets[aid]
        if s.get("head_swap") != new_h:
            s["head_swap"] = new_h
            changed += 1
    if isinstance(raw, dict) and "slots" in raw:
        MAP_PATH.write_text(json.dumps(raw, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    else:
        MAP_PATH.write_text(json.dumps(slots, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"map_head_swap_updated={changed} -> {MAP_PATH}")


def main() -> int:
    dry = "--dry-run" in sys.argv
    verbose = "--verbose" in sys.argv
    do_sync = "--sync-map" in sys.argv
    text = ITEMS.read_text(encoding="utf-8")
    parts = text.split("PlaceObj('ModItemAppearancePreset', {")
    male_i = female_i = body_i = pants_i = 0
    bad_before: list[tuple] = []
    focus_rows: list[tuple] = []
    changes: list[str] = []
    out = [parts[0]]
    ame_count = 0
    for chunk in parts[1:]:
        id_m = re.search(r'\bid = "(JAZZ_AME_\d+)"', chunk)
        if not id_m:
            out.append("PlaceObj('ModItemAppearancePreset', {" + chunk)
            continue
        aid = id_m.group(1)
        ame_count += 1
        f = fields(chunk, aid)
        head, hat, bod, pants = f["Head"], f["Hat"], f["Body"], f["Pants"]
        issues = collect_issues(f)

        if issues:
            bad_before.append((aid, head, hat, bod, pants, list(issues)))

        if aid in FOCUS or verbose:
            focus_rows.append((aid, bod, head, hat, f.get("BodyC1", ""), list(issues)))

        if not dry and issues:
            if "female_head_on_male" in issues or "pale_or_bad_male_head" in issues or "warpaint_head" in issues:
                if not is_female_body(bod):
                    new_h = MALE_HEADS[male_i % len(MALE_HEADS)]
                    male_i += 1
                    chunk = re.sub(r'\bHead = "[^"]*"', f'Head = "{new_h}"', chunk, count=1)
                    msg = f"{aid}: Head {head} -> {new_h} ({issues})"
                    print(msg)
                    changes.append(msg)
                    head = new_h
            if "pale_or_bad_female_head" in issues or (
                is_female_body(bod) and is_female_head(head) and head in ("Head_Fauda", "Head_Lami")
            ):
                if is_female_body(bod):
                    new_h = FEMALE_HEAD_BANK[female_i % len(FEMALE_HEAD_BANK)]
                    female_i += 1
                    chunk = re.sub(r'\bHead = "[^"]*"', f'Head = "{new_h}"', chunk, count=1)
                    msg = f"{aid}: Head {head} -> {new_h} (female)"
                    print(msg)
                    changes.append(msg)
            if "male_hat_on_female" in issues or "bad_hat_gear" in issues:
                if is_female_body(bod):
                    chunk = re.sub(r'\bHat = "[^"]*"', f'Hat = "{FEMALE_HAT}"', chunk, count=1)
                    print(f"{aid}: Hat {hat} -> {FEMALE_HAT}")
                elif "bad_hat_gear" in issues:
                    chunk = re.sub(r'\bHat = "[^"]*"\s*,?\s*\n', "", chunk, count=1)
                    print(f"{aid}: Hat {hat} -> (removed)")
            if "warpaint_body" in issues or "pale_hand_body" in issues:
                new_b = SAFE_MALE_BODIES[body_i % len(SAFE_MALE_BODIES)]
                body_i += 1
                chunk = re.sub(r'\bBody = "[^"]*"', f'Body = "{new_b}"', chunk, count=1)
                msg = f"{aid}: Body {bod} -> {new_b}"
                print(msg)
                changes.append(msg)
                bod = new_b
            if "bad_pants_gear" in issues:
                new_p = FEMALE_PANTS if is_female_body(bod) else SAFE_MALE_PANTS[pants_i % len(SAFE_MALE_PANTS)]
                pants_i += 1
                chunk = re.sub(r'\bPants = "[^"]*"', f'Pants = "{new_p}"', chunk, count=1)
                print(f"{aid}: Pants {pants} -> {new_p}")
            if "gloves_shirt" in issues:
                chunk = re.sub(r'\bShirt = "[^"]*"', 'Shirt = ""', chunk, count=1)
                print(f"{aid}: Shirt gloves -> (cleared)")
            if "pale_body_skin" in issues or "pale_hand_body" in issues or "warpaint_body" in issues:
                before = f.get("BodyC1")
                chunk = force_body_c1(chunk, aid)
                sr, sg, sb = skin_for(aid)
                msg = f"{aid}: BodyColor C1 {before} -> RGBA({sr}, {sg}, {sb}, 255)"
                print(msg)
                changes.append(msg)
            chunk = force_head_color_black(chunk, aid)

        # Always enforce dark Body C1 + black HeadColor on write pass for males
        # that were otherwise clean but may drift — only when not dry and had issues
        # (full-roster force is intentional for pale_body_skin coverage above).

        out.append("PlaceObj('ModItemAppearancePreset', {" + chunk)

    print(f"ame_count={ame_count}")
    print(f"bad_before={len(bad_before)}")
    for row in bad_before:
        print(row)

    print("--- focus ---")
    for aid, bod, head, hat, bc1, issues in focus_rows:
        if aid in FOCUS or issues:
            print(f"{aid}: Body={bod} Head={head} Hat={hat or '-'} BodyC1={bc1 or '-'} issues={issues or []}")

    if dry:
        return 1 if bad_before else 0

    ITEMS.write_text("".join(out), encoding="utf-8")
    # re-audit
    text2 = ITEMS.read_text(encoding="utf-8")
    bad2 = []
    head_by_id: dict[str, str] = {}
    for aid, chunk in parse_ame_chunks(text2):
        f = fields(chunk, aid)
        head_by_id[aid] = f["Head"]
        issues = reaudit_issues(f)
        if issues:
            bad2.append((aid, f["Head"], f["Hat"], f["Body"], f["Pants"], issues))
    print(f"bad_after={len(bad2)}")
    for row in bad2:
        print(row)

    if do_sync and not bad2:
        sync_map(head_by_id)
    elif do_sync and bad2:
        print("skip --sync-map: bad_after != 0")

    return 1 if bad2 else 0


if __name__ == "__main__":
    raise SystemExit(main())
