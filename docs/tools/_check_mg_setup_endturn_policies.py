# Legion/Rebels Machinegunner PositioningAI Label MGSetup must have
# EndTurnPolicies with LosToEnemy Required (else Score≈0 → huddle, no deploy).
from __future__ import annotations

import re
import sys
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
UNITS = JAZZ.parent / "jazz-units"
ITEMS = UNITS / "items.lua"
ARCH_IDS = ("Legion_Machinegunner", "Rebels_Machinegunner")


def close_brace(text: str, brace: int) -> int:
    depth = 0
    for j in range(brace, len(text)):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return j + 1
    return -1


def extract_archetype(text: str, arch_id: str) -> str | None:
    needle = f'id = "{arch_id}"'
    pos = text.find(needle)
    if pos < 0:
        return None
    start = text.rfind("PlaceObj('ModItemAIArchetype'", 0, pos)
    if start < 0:
        return None
    return text[start:pos]


def mgsetup_positioning(chunk: str) -> str | None:
    for m in re.finditer(r"PlaceObj\('PositioningAI', \{", chunk):
        end = close_brace(chunk, chunk.find("{", m.start()))
        if end < 0:
            continue
        body = chunk[m.start() : end]
        if "'Label', \"MGSetup\"" in body:
            return body
    return None


def main() -> int:
    if not ITEMS.is_file():
        print(f"FAIL: missing {ITEMS}")
        return 1
    text = ITEMS.read_text(encoding="utf-8")
    errors: list[str] = []
    for arch_id in ARCH_IDS:
        chunk = extract_archetype(text, arch_id)
        if not chunk:
            errors.append(f"{arch_id}: archetype block not found")
            continue
        body = mgsetup_positioning(chunk)
        if not body:
            errors.append(f"{arch_id}: PositioningAI Label MGSetup missing")
            continue
        if "'EndTurnPolicies'" not in body:
            errors.append(f"{arch_id}: MGSetup PositioningAI has no EndTurnPolicies")
            continue
        if "AIPolicyLosToEnemy" not in body:
            errors.append(f"{arch_id}: MGSetup EndTurn missing AIPolicyLosToEnemy")
        elif not re.search(
            r"PlaceObj\('AIPolicyLosToEnemy',\s*\{[^}]*'Required',\s*true",
            body,
            re.S,
        ):
            errors.append(f"{arch_id}: LosToEnemy on MGSetup EndTurn is not Required")
    if errors:
        print("FAIL: MGSetup EndTurn policies")
        for e in errors:
            print(" -", e)
        return 1
    print("PASS: Legion/Rebels MGSetup PositioningAI EndTurn LosToEnemy Required")
    return 0


if __name__ == "__main__":
    sys.exit(main())
