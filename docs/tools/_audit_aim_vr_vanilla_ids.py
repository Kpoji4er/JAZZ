# -*- coding: utf-8 -*-
"""Report ModItemVoiceResponse T-IDs: vanilla mercs must not use 8900* IDs.

Vanilla AIM/IME VoiceResponses keep Game.csv T-IDs so opus + subtitles resolve.
Jazz_* / JAZZ_* mercs may use 8900* mod-only IDs.

Usage (from jazz/):
  python docs/tools/_audit_aim_vr_vanilla_ids.py
"""
from __future__ import annotations

import re
from pathlib import Path

UNITS = Path(__file__).resolve().parents[2].parent / "jazz-units"
VR_START = re.compile(r"PlaceObj\('ModItemVoiceResponse',\s*\{")
GROUP_ID = re.compile(r'group = "([^"]+)",\s*id = "([^"]+)"')
T_RE = re.compile(r"T\((\d+),")


def vr_blocks(text: str) -> list[tuple[str, str, str]]:
    """Return (id, group, block) for each ModItemVoiceResponse with group+id."""
    out: list[tuple[str, str, str]] = []
    for m in VR_START.finditer(text):
        start = m.start()
        window = text[start : start + 400000]
        gm = GROUP_ID.search(window)
        if not gm:
            continue
        group, vid = gm.group(1), gm.group(2)
        close = text.find("}),", start + gm.end())
        if close < 0:
            continue
        out.append((vid, group, text[start : close + 3]))
    return out


def main() -> int:
    text = (UNITS / "items.lua").read_text(encoding="utf-8")
    print(f"VR scan {UNITS / 'items.lua'}")
    vanilla_8900: list[tuple[str, str, int, int, int]] = []
    jazz_vanilla: list[tuple[str, str, int, int, int]] = []
    aim_four: list[tuple[str, str, int, int, int]] = []
    blocks = vr_blocks(text)
    n_blocks = len(blocks)
    for vid, group, block in blocks:
        tids = T_RE.findall(block)
        n8900 = sum(1 for t in tids if t.startswith("8900"))
        nvan = len(tids) - n8900
        row = (vid, group, len(tids), n8900, nvan)
        if vid in ("Raven", "Thor", "Vicki", "Wolf"):
            aim_four.append(row)
        jazz = vid.startswith("Jazz_") or vid.startswith("JAZZ_")
        if n8900 and not jazz:
            vanilla_8900.append(row)
        elif jazz and nvan > n8900 and len(tids) > 20:
            jazz_vanilla.append(row)

    print(f"VR blocks with group+id: {n_blocks}")
    print("--- AIM four (must be 8900=0) ---")
    for vid, group, n, n8, nv in aim_four:
        print(f"{vid:30} group={group:20} T={n:4} 8900={n8:4} other={nv:4}")
    print("--- vanilla-looking ids with 8900 (FAIL if any) ---")
    if not vanilla_8900:
        print("(none)")
    for vid, group, n, n8, nv in vanilla_8900:
        print(f"{vid:30} group={group:20} T={n:4} 8900={n8:4} other={nv:4}")
    print("--- Jazz_* with mostly vanilla ids (info) ---")
    for vid, group, n, n8, nv in jazz_vanilla:
        print(f"{vid:30} group={group:20} T={n:4} 8900={n8:4} other={nv:4}")
    bad = [r for r in aim_four if r[3]] + vanilla_8900
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
