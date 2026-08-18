# -*- coding: utf-8 -*-
"""Static packet 1B: live TakeCover weights, POL-002 OptLoc wire, ROLE items.lua vs companions."""
from __future__ import annotations

import re
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
UNITS = JAZZ.parent / "jazz-units"
ITEMS = UNITS / "items.lua"
UD = UNITS / "UnitData"

ARCHETYPES = {
    "Legion_Assaulter": {
        "take": [10],
        "radius": 80,
        "anchors": True,
    },
    "Rebels_Assaulter": {
        "take": [10],
        "radius": 80,
        "anchors": True,
    },
    "Legion_Frontliner": {
        "take": [20, 40],
        "radius": 80,
        "anchors": True,
    },
    "Rebels_Frontliner": {
        "take": [20, 40],
        "radius": 80,
        "anchors": True,
    },
    "Legion_Flanker": {
        "take": [15],
        "radius": 55,
        "anchors": False,
    },
    "Rebels_Flanker": {
        "take": [15],
        "radius": 55,
        "anchors": False,
    },
}

FLANKER_UNITS = {
    "JAZZ_Legion_FlankerT1_Warden": "Legion_Flanker",
    "JAZZ_Legion_FlankerT2_Scout": "Legion_Flanker",
    "JAZZ_Legion_FlankerT2_Skirmisher": "Legion_Flanker",
    "JAZZ_Legion_FlankerT3_Recon": "Legion_Flanker",
    "JAZZ_Legion_FlankerT3_Pathfinder": "Legion_Flanker",
    "JAZZ_Legion_FlankerT4_Ranger": "Legion_Flanker",
    "RebelFlanker": "Rebels_Flanker",
}


def must(cond: bool, msg: str, errors: list[str]) -> None:
    if not cond:
        errors.append(msg)


def extract_optloc(text: str, arch_id: str) -> tuple[str, int] | None:
    needle = f'id = "{arch_id}"'
    pos = text.find(needle)
    if pos < 0:
        return None
    start = text.rfind("OptLocPolicies = {", 0, pos)
    if start < 0:
        return None
    brace = text.find("{", start)
    depth = 0
    end = None
    for j in range(brace, pos):
        ch = text[j]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = j
                break
    if end is None:
        return None
    chunk = text[start : end + 1]
    m = re.search(r"OptLocSearchRadius = (\d+)", text[end : end + 250])
    radius = int(m.group(1)) if m else -1
    return chunk, radius


def take_weights(chunk: str) -> list[int]:
    weights = []
    for m in re.finditer(
        r"PlaceObj\('AIPolicyTakeCover',\s*\{(.*?)\}\s*\)",
        chunk,
        re.S,
    ):
        body = m.group(1)
        wm = re.search(r"'Weight',\s*(\d+)", body)
        weights.append(int(wm.group(1)) if wm else 100)
    return weights


def unit_span(text: str, uid: str) -> str | None:
    needle = f"'Id', \"{uid}\""
    start = text.find(needle)
    if start < 0:
        return None
    nxt = text.find("'Id', \"", start + len(needle))
    end = nxt if nxt >= 0 else len(text)
    return text[start:end]


def pickcustom_body(block: str) -> str:
    m1 = re.search(
        r"'PickCustomArchetype', function \(self, proto_context\)  end,",
        block,
    )
    if m1:
        return ""
    m = re.search(
        r"^(\t+)'PickCustomArchetype', function \(self, proto_context\)\r?\n",
        block,
        re.M,
    )
    if not m:
        return ""
    indent = m.group(1)
    closer = re.compile(rf"\r?\n{re.escape(indent)}end,")
    cm = closer.search(block, m.end())
    if not cm:
        return ""
    return block[m.end() : cm.start()]


def companion_ids() -> list[str]:
    ids = [p.stem for p in sorted(UD.glob("JAZZ_Legion_*.lua"))]
    ids += [p.stem for p in sorted(UD.glob("Rebel*.lua"))]
    return ids


def main() -> int:
    errors: list[str] = []
    text = ITEMS.read_text(encoding="utf-8")

    for arch_id, expect in ARCHETYPES.items():
        extracted = extract_optloc(text, arch_id)
        must(extracted is not None, f"missing OptLoc for {arch_id}", errors)
        if not extracted:
            continue
        chunk, radius = extracted
        got = take_weights(chunk)
        must(
            got == expect["take"],
            f"{arch_id} OptLoc TakeCover {got} != {expect['take']}",
            errors,
        )
        must(
            radius == expect["radius"],
            f"{arch_id} OptLocSearchRadius {radius} != {expect['radius']}",
            errors,
        )
        has_anchor = "AIPolicyAllyRoleAnchor" in chunk
        has_peek = "AIPolicyAvoidPeekVoxel" in chunk
        if expect["anchors"]:
            must(has_anchor, f"{arch_id} missing AllyRoleAnchor", errors)
            must("'Mode', \"screen\"" in chunk and '"Sniper"' in chunk, f"{arch_id} missing screen/Sniper", errors)
            must("'Mode', \"retinue\"" in chunk and '"Leader"' in chunk, f"{arch_id} missing retinue/Leader", errors)
            must(has_peek, f"{arch_id} missing AvoidPeekVoxel", errors)
        else:
            must(not has_anchor, f"{arch_id} should not have AllyRoleAnchor", errors)
            must(not has_peek, f"{arch_id} should not have AvoidPeekVoxel", errors)

    for uid, arch in FLANKER_UNITS.items():
        block = unit_span(text, uid)
        must(block is not None, f"missing UnitData {uid}", errors)
        if not block:
            continue
        must(
            f"'archetype', \"{arch}\"" in block,
            f"{uid} archetype not {arch}",
            errors,
        )
        if uid.startswith("JAZZ_Legion_Flanker"):
            must(
                f"'RepositionArchetype', \"{arch}\"" in block,
                f"{uid} RepositionArchetype not {arch}",
                errors,
            )

    for uid in companion_ids():
        block = unit_span(text, uid)
        must(block is not None, f"missing UnitData {uid}", errors)
        if not block:
            continue
        body = pickcustom_body(block)
        must("JazzAI_PickCombatStance" in body, f"{uid} PickCustom missing helper", errors)
        must("panicshance" not in body, f"{uid} PickCustom still has panicshance", errors)
        must("Hide()" not in body, f"{uid} PickCustom still calls Hide()", errors)
        must("dist < 10*const.SlabSizeX" not in body, f"{uid} PickCustom still Melee@10", errors)
        if uid == "JAZZ_Legion_FrontT1_Bonemaker":
            must("allow_medic" in body, "Bonemaker missing allow_medic", errors)

    if errors:
        print("FAIL packet 1B")
        for e in errors:
            print(" -", e)
        return 1
    print("OK packet 1B: live TakeCover, POL-002 OptLoc, ROLE items.lua")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
