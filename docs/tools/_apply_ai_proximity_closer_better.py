"""Set AIPolicyProximity ScoreMode=closer_better on active faction combat archetypes.

POL-001 incomplete: without ScoreMode, EvalDest returns raw distance (farther_better),
so Machinegunners (and Frontliner/Assaulter) score OptLoc higher when far from allies —
gunners chase half-cover MGSetup across OptLocSearchRadius 80 and end up alone.

Usage (from jazz/):
  python docs/tools/_apply_ai_proximity_closer_better.py
"""
from __future__ import annotations

import re
from pathlib import Path

UNITS = Path(__file__).resolve().parents[2].parent / "jazz-units" / "items.lua"

TARGET_IDS = {
    "Legion_Machinegunner",
    "Rebels_Machinegunner",
    "Legion_Frontliner",
    "Rebels_Frontliner",
    "Legion_Assaulter",
    "Rebels_Assaulter",
}

MG_IDS = {"Legion_Machinegunner", "Rebels_Machinegunner"}
MG_PROX_WEIGHT = 80

SCOREMODE_LINE = "\t\t\t\t\t\t'ScoreMode', " + '"closer_better"' + ",\n"


def archetype_span(text: str, aid: str) -> tuple[int, int] | None:
    m = re.search(rf'id = "{re.escape(aid)}"', text)
    if not m:
        return None
    start = text.rfind("PlaceObj('ModItemAIArchetype'", 0, m.start())
    if start < 0:
        return None
    after = m.end()
    candidates = [
        i
        for i in (
            text.find("PlaceObj('ModItemAIArchetype'", after),
            text.find("PlaceObj('ModItemFolder'", after),
            text.find("PlaceObj('ModItemEnemyRole'", after),
            text.find("PlaceObj('ModItemUnitDataCompositeDef'", after),
        )
        if i > 0
    ]
    end = min(candidates) if candidates else len(text)
    return start, end


def patch_proximity_block(body: str, *, mg: bool) -> tuple[str, bool]:
    changed = False
    if "'ScoreMode'" not in body:
        body2 = re.sub(
            r"(PlaceObj\('AIPolicyProximity',\s*\{\s*\n)",
            r"\1" + SCOREMODE_LINE,
            body,
            count=1,
        )
        if body2 == body:
            body2 = re.sub(
                r"(PlaceObj\('AIPolicyProximity',\s*\{)",
                r"\1\n" + SCOREMODE_LINE.rstrip("\n") + ",",
                body,
                count=1,
            )
        if body2 != body:
            body = body2
            changed = True
    elif '"farther_better"' in body:
        body = body.replace('"farther_better"', '"closer_better"', 1)
        changed = True

    if mg and "'TargetUnits', \"allies\"" in body:
        m = re.search(r"'Weight',\s*(\d+)", body)
        if m and int(m.group(1)) < MG_PROX_WEIGHT:
            body = re.sub(r"'Weight',\s*\d+", f"'Weight', {MG_PROX_WEIGHT}", body, count=1)
            changed = True
    return body, changed


def main() -> None:
    text = UNITS.read_text(encoding="utf-8")
    total = 0
    for aid in sorted(TARGET_IDS):
        span = archetype_span(text, aid)
        if not span:
            print("MISSING", aid)
            continue
        a, b = span
        block = text[a:b]
        mg = aid in MG_IDS
        out = []
        last = 0
        n = 0
        for m in re.finditer(r"PlaceObj\('AIPolicyProximity',\s*\{.*?\}\s*\)", block, re.S):
            chunk = m.group(0)
            out.append(block[last : m.start()])
            if "'TargetUnits', \"enemies\"" in chunk:
                out.append(chunk)
            else:
                patched, ch = patch_proximity_block(chunk, mg=mg)
                out.append(patched)
                if ch:
                    n += 1
            last = m.end()
        out.append(block[last:])
        if n:
            text = text[:a] + "".join(out) + text[b:]
            total += n
            print(f"{aid}: patched {n} Proximity")
        else:
            print(f"{aid}: already ok / no ally Proximity")

    endturn_insert = (
        "\n\t\t\t\t\t\tPlaceObj('AIPolicyProximity', {\n"
        "\t\t\t\t\t\t\t'ScoreMode', \"closer_better\",\n"
        "\t\t\t\t\t\t\t'Weight', 100,\n"
        "\t\t\t\t\t\t\t'AllyPlannedPosition', true,\n"
        "\t\t\t\t\t\t\t'TargetUnits', \"allies\",\n"
        "\t\t\t\t\t\t\t'TargetDist', \"average\",\n"
        "\t\t\t\t\t\t\t'MinScore', 0,\n"
        "\t\t\t\t\t\t}),"
    )
    # Fix Python string: use real double quotes for ScoreMode value
    endturn_insert = endturn_insert.replace('\\"', '"') if False else (
        "\n\t\t\t\t\t\tPlaceObj('AIPolicyProximity', {\n"
        "\t\t\t\t\t\t\t'ScoreMode', " + '"closer_better"' + ",\n"
        "\t\t\t\t\t\t\t'Weight', 100,\n"
        "\t\t\t\t\t\t\t'AllyPlannedPosition', true,\n"
        "\t\t\t\t\t\t\t'TargetUnits', " + '"allies"' + ",\n"
        "\t\t\t\t\t\t\t'TargetDist', " + '"average"' + ",\n"
        "\t\t\t\t\t\t\t'MinScore', 0,\n"
        "\t\t\t\t\t\t}),"
    )

    for aid in sorted(MG_IDS):
        span = archetype_span(text, aid)
        if not span:
            continue
        a, b = span
        block = text[a:b]
        m = re.search(
            r"(PlaceObj\('StandardAI',\s*\{.*?\'EndTurnPolicies\',\s*\{)(.*?)(\},)",
            block,
            re.S,
        )
        if not m:
            print(aid, "no StandardAI EndTurn")
            continue
        et = m.group(2)
        if "AIPolicyProximity" in et:
            print(aid, "EndTurn already has Proximity")
            continue
        new_block = block[: m.start(2)] + endturn_insert + et + block[m.end(2) :]
        text = text[:a] + new_block + text[b:]
        total += 1
        print(aid, "added EndTurn ally Proximity")

    UNITS.write_text(text, encoding="utf-8", newline="\n")
    print("done, changes~", total, "->", UNITS)


if __name__ == "__main__":
    main()
