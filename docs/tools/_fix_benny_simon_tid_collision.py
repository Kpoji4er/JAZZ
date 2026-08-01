# -*- coding: utf-8 -*-
"""Remap Jazz_Benny / Jazz_Simon VR T-ids that collided with expand batch.

Usage (jazz/):
  python docs/tools/_fix_benny_simon_tid_collision.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
JU = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")
ITEMS = JU / "items.lua"
RU = JAZZ / "Russian.csv"
EN = JAZZ / "English.csv"


def max_tid(*texts: str) -> int:
    ids = [int(x) for t in texts for x in re.findall(r"\b(8900\d+)\b", t)]
    return max(ids) if ids else 890000000009100


def remap_block(block: str, uid: str, start_tid: int) -> tuple[str, dict[int, int], int]:
    """Replace T(old, ... voice:uid) in order with new sequential tids."""
    mapping: dict[int, int] = {}
    tid = start_tid

    def repl(m: re.Match) -> str:
        nonlocal tid
        old = int(m.group(1))
        # only remap if comment mentions this uid
        tail = m.group(0)
        if f"voice:{uid}" not in tail and uid not in tail:
            return tail
        if old not in mapping:
            mapping[old] = tid
            tid += 1
        return f"T({mapping[old]},"

    # Match T(id, with following context up to voice:uid in same T( call — do line-wise
    lines = block.splitlines(keepends=True)
    out = []
    for line in lines:
        if f"voice:{uid}" in line or (f"ModItemVoiceResponse {uid}" in line):
            line2 = re.sub(r"T\((\d+),", lambda m: _map(m, mapping, uid, locals_tid := None), line)
            # simpler:
            m = re.search(r"T\((\d+),", line)
            if m:
                old = int(m.group(1))
                if old not in mapping:
                    mapping[old] = tid
                    tid += 1
                line = re.sub(r"T\(\d+,", f"T({mapping[old]},", line, count=1)
        out.append(line)
    return "".join(out), mapping, tid


def _map(m, mapping, uid, locals_tid):
    return m.group(0)  # unused


def patch_csv(path: Path, mapping: dict[int, int], uid: str) -> int:
    """Rewrite colliding ID rows that were appended for uid; add new ID rows."""
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    # Build text by old tid from lines that mention VoiceResponse and were last-appended
    # Safer: for each old->new, if a line starts with old, and Translation looks like placeholder
    # belonging to expand, DUPLICATE as new id with same text for Benny/Simon.
    # Also: remove trailing duplicate rows for old ids that were added in Benny pass
    # (same ID appearing twice — keep first, drop later duplicates that match placeholder).

    from collections import defaultdict

    by_id_idxs = defaultdict(list)
    for i, line in enumerate(lines):
        if not line or line.startswith("sep=") or line.startswith("ID"):
            continue
        mid = re.match(r"^(\d+),", line)
        if mid:
            by_id_idxs[int(mid.group(1))].append(i)

    remove = set()
    additions = []
    for old, new in mapping.items():
        idxs = by_id_idxs.get(old, [])
        if not idxs:
            # synthesize
            additions.append(
                f"{new},…,…,,jazz-units:items.lua:VoiceResponse"
            )
            continue
        # Keep first occurrence (Biff/etc.); if duplicates, drop extras
        keep_line = lines[idxs[0]]
        for j in idxs[1:]:
            remove.add(j)
        # New row for Benny/Simon with same text body as the DUPLICATE if any, else placeholder
        src = lines[idxs[-1]] if len(idxs) > 1 else keep_line
        # replace leading id
        additions.append(re.sub(r"^\d+,", f"{new},", src, count=1))

    new_lines = [ln for i, ln in enumerate(lines) if i not in remove]
    if new_lines and new_lines[-1] != "":
        new_lines.append("")
    new_lines.extend(additions)
    path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    return len(mapping)


def main() -> int:
    items = ITEMS.read_text(encoding="utf-8")
    ru = RU.read_text(encoding="utf-8-sig")
    en = EN.read_text(encoding="utf-8-sig")
    tid = max_tid(items, ru, en) + 1
    print(f"start remap tid={tid}")

    total_map: dict[int, int] = {}
    for uid in ("Jazz_Benny", "Jazz_Simon"):
        # isolate VR block
        m = re.search(
            rf"PlaceObj\('ModItemVoiceResponse',\s*\{{[\s\S]*?\bid\s*=\s*\"{uid}\",\s*\}}\),?",
            items,
        )
        if not m:
            print(f"FAIL: no VR for {uid}")
            return 1
        block = m.group(0)
        new_block, mapping, tid = remap_block(block, uid, tid)
        items = items[: m.start()] + new_block + items[m.end() :]
        total_map.update(mapping)
        print(f"{uid}: remapped {len(mapping)} tids -> {min(mapping.values())}-{max(mapping.values())}")

    ITEMS.write_text(items, encoding="utf-8")
    nru = patch_csv(RU, total_map, "Jazz_Benny")
    nen = patch_csv(EN, total_map, "Jazz_Simon")
    print(f"loc rows written ru={nru} en={nen}")

    # verify no collisions for Benny/Simon
    own = {}
    for m in re.finditer(r"T\((\d+),[^\n]*voice:(Jazz_Benny|Jazz_Simon|Jazz_Biff)", items):
        own.setdefault(m.group(1), set()).add(m.group(2))
    coll = {k: v for k, v in own.items() if len(v) > 1}
    print(f"remaining Benny/Simon/Biff collisions: {len(coll)}")
    return 0 if not coll else 1


if __name__ == "__main__":
    raise SystemExit(main())
