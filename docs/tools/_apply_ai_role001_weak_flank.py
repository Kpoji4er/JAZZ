# -*- coding: utf-8 -*-
"""ROLE-001 REQ-005: weaken Flanker AI branches on Assaulter/Frontliner; keep Flanker presets strong."""
from __future__ import annotations

import re
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
ITEMS = JAZZ.parent / "jazz-units" / "items.lua"

WEAK_ARCH = (
    "Legion_Assaulter",
    "Legion_Frontliner",
    "Rebels_Assaulter",
    "Rebels_Frontliner",
)
BEHAVIOR_WEIGHT = 80
FLANK_POLICY_WEIGHT = 150


def read_items() -> tuple[str, bytes]:
    raw = ITEMS.read_bytes()
    nl = b"\r\n" if b"\r\n" in raw else b"\n"
    text = raw.decode("utf-8")
    if nl == b"\r\n":
        text = text.replace("\r\n", "\n")
    return text, nl


def write_items(text: str, nl: bytes) -> None:
    payload = text.replace("\n", "\r\n").encode("utf-8") if nl == b"\r\n" else text.encode("utf-8")
    ITEMS.write_bytes(payload)


def archetype_span(text: str, arch_id: str) -> tuple[int, int]:
    needle = f'id = "{arch_id}"'
    pos = text.find(needle)
    if pos < 0:
        raise SystemExit(f"missing id {arch_id}")
    start = text.rfind("PlaceObj('ModItemAIArchetype'", 0, pos)
    if start < 0:
        raise SystemExit(f"missing PlaceObj for {arch_id}")
    end = pos + len(needle)
    return start, end


def close_placeobj(block: str, start: int) -> int:
    brace = block.find("{", start)
    depth = 0
    for j in range(brace, len(block)):
        if block[j] == "{":
            depth += 1
        elif block[j] == "}":
            depth -= 1
            if depth == 0:
                return j + 1
    raise SystemExit("unclosed PlaceObj")


def weaken_chunk(chunk: str, arch_id: str) -> str:
    out = chunk
    n_beh = n_pol = n_typo = 0
    for m in list(
        re.finditer(
            r"PlaceObj\('(?:StandardAI|PositioningAI)', \{",
            chunk,
        )
    ):
        end = close_placeobj(chunk, m.start())
        body = chunk[m.start() : end]
        if "'Label', \"Flanker AI\"" not in body and "'Label', \"Flanker AI POS\"" not in body:
            continue
        new = body
        new, c = re.subn(
            r"^(\t+)'Weight', 500,$",
            rf"\1'Weight', {BEHAVIOR_WEIGHT},",
            new,
            count=1,
            flags=re.M,
        )
        if c == 0:
            new, c = re.subn(
                r"^(\t+)'Weight', 1000,$",
                rf"\1'Weight', {BEHAVIOR_WEIGHT},",
                new,
                count=1,
                flags=re.M,
            )
        n_beh += c
        new, c2 = re.subn(
            r"(PlaceObj\('AIPolicyFlanking', \{\s*'Weight', )1000,",
            rf"\g<1>{FLANK_POLICY_WEIGHT},",
            new,
            count=1,
        )
        n_pol += c2
        if "Flanks" in new:
            new = new.replace('"Flanks"', '"Flank"', 1)
            n_typo += 1
        if new != body:
            out = out.replace(body, new, 1)
    print(f"  {arch_id}: behavior={n_beh} flanking={n_pol} Flanks-to-Flank={n_typo}")
    if n_beh < 1 or n_pol < 1:
        raise SystemExit(f"{arch_id}: expected Flanker AI branches to weaken")
    return out


def main() -> None:
    text, nl = read_items()
    original = text
    for arch_id in WEAK_ARCH:
        start, end = archetype_span(text, arch_id)
        chunk = text[start:end]
        new_chunk = weaken_chunk(chunk, arch_id)
        text = text[:start] + new_chunk + text[end:]
    if text == original:
        raise SystemExit("no changes")
    write_items(text, nl)
    print("OK ROLE-001 weak Flanker AI on Assaulter/Frontliner")


if __name__ == "__main__":
    main()
