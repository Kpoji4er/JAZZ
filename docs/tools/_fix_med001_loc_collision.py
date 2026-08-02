# -*- coding: utf-8 -*-
"""Fix MED-001 loc ID collision with JA2 voice remesh duplicates.

Voice ship appended VR lines onto IDs already used by medicine (890000000009195+).
Engine last-wins → tooltips show 'Engage!' / 'Есть цель!' on Bandage/Medkit.

Remap all T(890000000009195..9255) medicine/trauma strings to 890000000010000+.
Keep VR on the old IDs (drop the earlier medicine duplicate rows).
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
OLD_LO = 890000000009195
OLD_HI = 890000000009400  # trauma block + actions
NEW_BASE = 890000000010000

# Collect first (medicine) text for each id from English/Russian, then drop first when writing.
def load_csv(path: Path):
    rows = []
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.reader(f):
            rows.append(row)
    return rows


def first_texts(rows):
    """id -> (col1, col2) from FIRST occurrence."""
    out = {}
    for row in rows:
        if not row:
            continue
        try:
            i = int(row[0])
        except ValueError:
            continue
        if OLD_LO <= i <= OLD_HI and i not in out:
            c1 = row[1] if len(row) > 1 else ""
            c2 = row[2] if len(row) > 2 else c1
            out[i] = (c1, c2, row)
    return out


en_rows = load_csv(ROOT / "English.csv")
ru_rows = load_csv(ROOT / "Russian.csv")
en_first = first_texts(en_rows)
ru_first = first_texts(ru_rows)

# IDs that have medicine-looking first text (not already VR)
def is_med_text(t: str) -> bool:
    tl = (t or "").lower()
    if any(x in tl for x in ("bleed", "pain", "bandage", "morphine", "trauma", "med kit", "ifak", "surgical", "analges", "inject morphine", "bleeding reduced")):
        return True
    if "DamagePerTurn" in (t or "") or "APLoss" in (t or "") or "cth_penalty" in (t or ""):
        return True
    if (t or "").startswith("<image UI/Conversation"):
        return True
    if (t or "").startswith("<color EmStyle>"):
        return True
    if t in ("USE", "MORPHINE", "Bandages", "Surgical Kits", "IFAKs", "Med Kits", "Pain", "Analgesia"):
        return True
    return False

med_ids = sorted(i for i, (c1, _, _) in en_first.items() if is_med_text(c1))
print("medicine ids to remap:", len(med_ids), "range", med_ids[0] if med_ids else None, "..", med_ids[-1] if med_ids else None)

id_map = {old: NEW_BASE + n for n, old in enumerate(med_ids)}

# Rewrite lua files
lua_paths = list((ROOT / "CharacterEffect").glob("*.lua"))
lua_paths += list((ROOT / "InventoryItem").glob("JAZZ_*.lua"))
lua_paths += list((ROOT / "InventoryItem").glob("FirstAidKit.lua"))
lua_paths += list((ROOT / "InventoryItem").glob("Medkit.lua"))
lua_paths += [ROOT / "items.lua"]
# CombatAction if any
for p in (ROOT / "Code").glob("*.lua"):
    lua_paths.append(p)

pat = re.compile(r"T\((\d{10,})")
changed_files = []
for path in lua_paths:
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    orig = text

    def repl(m):
        i = int(m.group(1))
        if i in id_map:
            return f"T({id_map[i]}"
        return m.group(0)

    text = pat.sub(repl, text)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        changed_files.append(path.name)

print("lua files updated:", len(changed_files))


def rewrite_csv(path: Path, first: dict, lang: str):
    rows = load_csv(path)
    seen = set()
    out = []
    removed_first = 0
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
            if i not in seen:
                # drop first (medicine) occurrence — VR duplicate kept
                seen.add(i)
                removed_first += 1
                continue
            # keep subsequent (VR)
            out.append(row)
            continue
        out.append(row)

    # append new medicine rows
    for old in med_ids:
        new = id_map[old]
        c1, c2, _ = first[old]
        # RU file: prefer Russian first-occurrence col1/col2
        out.append([str(new), c1, c2, "", f"jazz:MED-001-remap-from-{old}"])
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerows(out)
    print(path.name, "removed first dups", removed_first, "appended", len(med_ids))


# For Russian use ru_first texts when available
def merge_first():
    merged = {}
    for i in med_ids:
        en = en_first[i]
        ru = ru_first.get(i, en)
        # Russian.csv typically: id, russian, english_or_same
        # Prefer ru col1 as russian, en col1 as english fallback in col2
        merged[i] = (ru[0], en[0], ru[2] if len(ru) > 2 else None)
    return merged


merged = merge_first()

# English.csv: col1=english, col2=english
en_out_first = {i: (en_first[i][0], en_first[i][0], None) for i in med_ids}
# Russian.csv: Text=english source, Translation=russian (JA3 engine contract)
ru_out_first = {i: (en_first[i][0], ru_first[i][0], None) for i in med_ids}


def rewrite_csv2(path: Path, texts: dict):
    rows = load_csv(path)
    seen = set()
    out = []
    removed_first = 0
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
            if i not in seen:
                seen.add(i)
                removed_first += 1
                continue
            out.append(row)
            continue
        out.append(row)
    for old in med_ids:
        new = id_map[old]
        c1, c2, _ = texts[old]
        out.append([str(new), c1, c2, "", f"jazz:MED-001-remap-from-{old}"])
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerows(out)
    print(path.name, "removed_first", removed_first, "appended", len(med_ids))


rewrite_csv2(ROOT / "English.csv", en_out_first)
rewrite_csv2(ROOT / "Russian.csv", ru_out_first)

# write map for docs
map_path = ROOT / "docs/tools/_med001_loc_remap.txt"
map_path.write_text("\n".join(f"{o}->{n}" for o, n in id_map.items()), encoding="utf-8")
print("map", map_path)
print("sample", list(id_map.items())[:5])
