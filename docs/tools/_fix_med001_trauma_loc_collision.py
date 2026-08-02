# -*- coding: utf-8 -*-
"""Remap Trauma* (and any remaining MED) loc IDs away from VR-stomped duplicates.

For IDs where first row is VR and last is trauma text, keep VR on old ID,
move trauma to NEW_BASE continuing from prior remap.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
NEW_BASE = 890000000010100  # after previous 10000+31 block


def load_csv(path: Path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.reader(f))


def occurrences(rows):
    by = {}
    for row in rows:
        if not row:
            continue
        try:
            i = int(row[0])
        except ValueError:
            continue
        by.setdefault(i, []).append(row)
    return by


en = load_csv(ROOT / "English.csv")
ru = load_csv(ROOT / "Russian.csv")
en_occ = occurrences(en)
ru_occ = occurrences(ru)

# Find IDs referenced by Trauma* companions still on 9xxxxx
trauma_ids = set()
for p in (ROOT / "CharacterEffect").glob("Trauma*.lua"):
    for m in re.finditer(r"T\((\d{10,})", p.read_text(encoding="utf-8")):
        trauma_ids.add(int(m.group(1)))

# Also any id with multiple rows where last looks like trauma and first looks like VR
for i, rows in en_occ.items():
    if len(rows) < 2:
        continue
    last = rows[-1][1] if len(rows[-1]) > 1 else ""
    if "Trauma" in last or "trauma" in last or "Burn Trauma" in last:
        trauma_ids.add(i)

trauma_ids = sorted(i for i in trauma_ids if i < NEW_BASE)
print("trauma-related ids", len(trauma_ids), trauma_ids[:5], "...", trauma_ids[-5:])

id_map = {old: NEW_BASE + n for n, old in enumerate(trauma_ids)}

# lua rewrite
pat = re.compile(r"T\((\d{10,})")
changed = []
for path in list((ROOT / "CharacterEffect").glob("*.lua")) + [ROOT / "items.lua"]:
    text = path.read_text(encoding="utf-8")
    orig = text

    def repl(m):
        i = int(m.group(1))
        return f"T({id_map[i]}" if i in id_map else m.group(0)

    text = pat.sub(repl, text)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        changed.append(path.name)
print("lua", changed)


def is_vr(t: str) -> bool:
    return t in {
        "Target!",
        "Engage!",
        "Contact!",
        "Online.",
        "Down.",
        "Waiting.",
        "Learning.",
        "Not this.",
        "Nice work.",
        "Low ammo!",
        "I'm hit!",
        "That's it...",
        "Roger.",
        "Moving.",
        "Quiet.",
    } or t.startswith("I see") or t in {"Argh!", "Clear.", "Cover!", "Done.", "Thanks.", "Jam!"}


def rewrite(path: Path, occ: dict, prefer_lang_en: bool):
    rows = load_csv(path)
    # drop LAST trauma occurrence for remapped ids (keep VR first); append new
    out = []
    skip_last = {i: True for i in id_map}  # skip the last trauma row
    counts = {i: 0 for i in id_map}
    total = {i: len(occ.get(i, [])) for i in id_map}

    for row in rows:
        if not row:
            out.append(row)
            continue
        try:
            i = int(row[0])
        except ValueError:
            out.append(row)
            continue
        if i in id_map:
            counts[i] += 1
            # If multiple: keep all but the last (trauma). If only one and it's trauma, drop and re-add.
            if total[i] >= 2 and counts[i] == total[i]:
                continue  # drop last trauma duplicate
            if total[i] == 1 and not is_vr(row[1] if len(row) > 1 else ""):
                continue  # sole trauma row → move
            out.append(row)
            continue
        out.append(row)

    for old in trauma_ids:
        new = id_map[old]
        rows_i = occ.get(old, [])
        # pick last non-VR text
        pick = None
        for row in reversed(rows_i):
            t = row[1] if len(row) > 1 else ""
            if not is_vr(t):
                pick = row
                break
        if not pick:
            pick = rows_i[-1] if rows_i else [str(old), "?", "?", "", ""]
        c1 = pick[1] if len(pick) > 1 else ""
        c2 = pick[2] if len(pick) > 2 else c1
        if prefer_lang_en:
            # English file: both english
            en_rows = en_occ.get(old, [])
            for row in reversed(en_rows):
                t = row[1] if len(row) > 1 else ""
                if not is_vr(t):
                    c1 = t
                    c2 = t
                    break
        else:
            # Russian: ru text + en text
            en_c = c1
            for row in reversed(en_occ.get(old, [])):
                t = row[1] if len(row) > 1 else ""
                if not is_vr(t):
                    en_c = t
                    break
            ru_c = c1
            for row in reversed(ru_occ.get(old, [])):
                t = row[1] if len(row) > 1 else ""
                if not is_vr(t):
                    ru_c = t
                    break
            c1, c2 = ru_c, en_c
        out.append([str(new), c1, c2, "", f"jazz:MED-001-trauma-remap-from-{old}"])

    with path.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\n").writerows(out)
    print(path.name, "appended", len(trauma_ids))


rewrite(ROOT / "English.csv", en_occ, prefer_lang_en=True)
# reload occ after english? use original occ for texts
rewrite(ROOT / "Russian.csv", ru_occ, prefer_lang_en=False)

(ROOT / "docs/tools/_med001_trauma_loc_remap.txt").write_text(
    "\n".join(f"{o}->{n}" for o, n in id_map.items()), encoding="utf-8"
)
print("done")
