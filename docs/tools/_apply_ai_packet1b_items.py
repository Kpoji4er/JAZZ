# -*- coding: utf-8 -*-
"""Packet 1B: sync ROLE items.lua to companions; wire POL-002 OptLoc; leave TakeCover weights live."""
from __future__ import annotations

import re
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
UNITS = JAZZ.parent / "jazz-units"
ITEMS = UNITS / "items.lua"
UD = UNITS / "UnitData"

ASSAULT_NEEDLE = """\t\t\t\t\tPlaceObj('AIPolicyTakeCover', {
\t\t\t\t\t\t'Weight', 10,
\t\t\t\t\t\t'visibility_mode', "team",
\t\t\t\t\t}),
\t\t\t\t},
\t\t\t\tOptLocSearchRadius = 80,"""

ASSAULT_INSERT = """\t\t\t\t\tPlaceObj('AIPolicyTakeCover', {
\t\t\t\t\t\t'Weight', 10,
\t\t\t\t\t\t'visibility_mode', "team",
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('AIPolicyAllyRoleAnchor', {
\t\t\t\t\t\t'Weight', 35,
\t\t\t\t\t\t'Mode', "screen",
\t\t\t\t\t\t'AnchorKeyword', "Sniper",
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('AIPolicyAllyRoleAnchor', {
\t\t\t\t\t\t'Weight', 25,
\t\t\t\t\t\t'Mode', "retinue",
\t\t\t\t\t\t'AnchorKeyword', "Leader",
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('AIPolicyAvoidPeekVoxel', {
\t\t\t\t\t\t'Weight', 40,
\t\t\t\t\t\t'Penalty', 80,
\t\t\t\t\t\t'Radius', 1,
\t\t\t\t\t}),
\t\t\t\t},
\t\t\t\tOptLocSearchRadius = 80,"""

FRONT_NEEDLE = """\t\t\t\t\tPlaceObj('AIPolicyTakeCover', {
\t\t\t\t\t\t'Weight', 20,
\t\t\t\t\t\t'visibility_mode', "team",
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('AIPolicyTakeCover', {
\t\t\t\t\t\t'Weight', 40,
\t\t\t\t\t}),
\t\t\t\t},
\t\t\t\tOptLocSearchRadius = 80,"""

FRONT_INSERT = """\t\t\t\t\tPlaceObj('AIPolicyTakeCover', {
\t\t\t\t\t\t'Weight', 20,
\t\t\t\t\t\t'visibility_mode', "team",
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('AIPolicyTakeCover', {
\t\t\t\t\t\t'Weight', 40,
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('AIPolicyAllyRoleAnchor', {
\t\t\t\t\t\t'Weight', 35,
\t\t\t\t\t\t'Mode', "screen",
\t\t\t\t\t\t'AnchorKeyword', "Sniper",
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('AIPolicyAllyRoleAnchor', {
\t\t\t\t\t\t'Weight', 25,
\t\t\t\t\t\t'Mode', "retinue",
\t\t\t\t\t\t'AnchorKeyword', "Leader",
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('AIPolicyAvoidPeekVoxel', {
\t\t\t\t\t\t'Weight', 40,
\t\t\t\t\t\t'Penalty', 80,
\t\t\t\t\t\t'Radius', 1,
\t\t\t\t\t}),
\t\t\t\t},
\t\t\t\tOptLocSearchRadius = 80,"""


def companion_files():
    files = list(UD.glob("JAZZ_Legion_*.lua"))
    files += list(UD.glob("Rebel*.lua"))
    return sorted(files)


def parse_companion(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    cid = path.stem
    arch = re.search(r'^\tarchetype = "([^"]+)"', text, re.M)
    repos = re.search(r'^\tRepositionArchetype = "([^"]+)"', text, re.M)
    m = re.search(
        r"^\tPickCustomArchetype = function \(self, proto_context\)\r?\n(.*?)^\tend,",
        text,
        re.M | re.S,
    )
    body = m.group(1).strip() if m else None
    return {
        "id": cid,
        "archetype": arch.group(1) if arch else None,
        "reposition": repos.group(1) if repos else None,
        "pick_body": body,
    }


def read_items() -> tuple[str, bytes]:
    raw = ITEMS.read_bytes()
    nl = b"\r\n" if b"\r\n" in raw else b"\n"
    text = raw.decode("utf-8")
    if nl == b"\r\n":
        text = text.replace("\r\n", "\n")
    return text, nl


def write_items(text: str, nl: bytes) -> None:
    if nl == b"\r\n":
        payload = text.replace("\n", "\r\n").encode("utf-8")
    else:
        payload = text.encode("utf-8")
    ITEMS.write_bytes(payload)


def unit_span(text: str, uid: str) -> tuple[int, int] | None:
    needle = f"'Id', \"{uid}\""
    start = text.find(needle)
    if start < 0:
        return None
    nxt = text.find("'Id', \"", start + len(needle))
    end = nxt if nxt >= 0 else len(text)
    return start, end


def replace_pickcustom(block: str, items_body: str, uid: str) -> str:
    m1 = re.search(
        r"^(\t+)'PickCustomArchetype', function \(self, proto_context\)  end,",
        block,
        re.M,
    )
    if m1:
        indent = m1.group(1)
        new = (
            f"{indent}'PickCustomArchetype', function (self, proto_context)\n"
            f"{items_body}\n"
            f"{indent}end,"
        )
        return block[: m1.start()] + new + block[m1.end() :]

    m = re.search(
        r"^(\t+)'PickCustomArchetype', function \(self, proto_context\)\r?\n",
        block,
        re.M,
    )
    if not m:
        return block
    indent = m.group(1)
    start = m.start()
    closer_re = re.compile(rf"\r?\n{re.escape(indent)}end,")
    cm = closer_re.search(block, m.end())
    if not cm:
        raise SystemExit(f"PickCustom closer not found for {uid} (indent tabs={indent.count(chr(9))})")
    new = (
        f"{indent}'PickCustomArchetype', function (self, proto_context)\n"
        f"{items_body}\n"
        f"{indent}end,"
    )
    return block[:start] + new + block[cm.end() :]


def companion_body_to_items(body: str, indent: str) -> str:
    inner = indent + "\t"
    lines = []
    for line in body.splitlines():
        stripped = line.lstrip("\t")
        if stripped:
            lines.append(inner + stripped)
        else:
            lines.append("")
    return "\n".join(lines)


def patch_field(block: str, key: str, value: str | None) -> str:
    if not value:
        return block
    pat = re.compile(rf"('{re.escape(key)}', )\"[^\"]+\"")
    m = pat.search(block)
    if not m:
        return block
    return block[: m.start()] + m.group(1) + '"' + value + '"' + block[m.end() :]


def wire_pol002(text: str) -> str:
    if "AIPolicyAllyRoleAnchor" in text:
        print("POL-002 already wired, skip insert")
        return text
    ac = text.count(ASSAULT_NEEDLE)
    fc = text.count(FRONT_NEEDLE)
    print(f"POL-002 needles assault={ac} front={fc}")
    if ac != 2 or fc != 2:
        raise SystemExit("unexpected POL-002 needle counts")
    text = text.replace(ASSAULT_NEEDLE, ASSAULT_INSERT)
    text = text.replace(FRONT_NEEDLE, FRONT_INSERT)
    return text


def main() -> None:
    text, nl = read_items()
    original = text
    comps = [parse_companion(p) for p in companion_files()]
    n_pick = n_arch = n_repos = 0
    missing = []
    for c in comps:
        span = unit_span(text, c["id"])
        if not span:
            missing.append(c["id"])
            continue
        start, end = span
        block = text[start:end]
        if end - start > 40000:
            raise SystemExit(f"unit span too large for {c['id']}: {end - start} bytes")
        if block.count(f"'Id', \"{c['id']}\"") != 1:
            raise SystemExit(f"non-unique Id span for {c['id']}")
        if c["archetype"]:
            before = block
            old_arch = re.search(r"'archetype', \"([^\"]+)\"", block)
            block = patch_field(block, "archetype", c["archetype"])
            if block != before:
                n_arch += 1
                src = old_arch.group(1) if old_arch else "?"
                if src != c["archetype"]:
                    print(f"  archetype {c['id']}: {src} -> {c['archetype']}")
        if c["reposition"]:
            before = block
            block = patch_field(block, "RepositionArchetype", c["reposition"])
            if block != before:
                n_repos += 1
        if c["pick_body"] and "JazzAI_PickCombatStance" in c["pick_body"]:
            m = re.search(r"^(\t+)'PickCustomArchetype'", block, re.M)
            indent = m.group(1) if m else "\t\t\t\t"
            items_body = companion_body_to_items(c["pick_body"], indent)
            new_block = replace_pickcustom(block, items_body, c["id"])
            if new_block != block:
                n_pick += 1
                block = new_block
        text = text[:start] + block + text[end:]

    if missing:
        print("WARN missing in items.lua:", ", ".join(missing))

    text = wire_pol002(text)

    if text == original:
        raise SystemExit("no changes")
    write_items(text, nl)
    print(f"OK items.lua pick={n_pick} archetype={n_arch} reposition={n_repos} pol002 wired")


if __name__ == "__main__":
    main()
