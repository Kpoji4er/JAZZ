# -*- coding: utf-8 -*-
"""Apply focused high-tier accuracy package buffs + AR10DMR -> sniper."""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

UPDATES = {
    "Glock18": {"AimAccuracy": 3, "BulletDropRange": 8, "Grouping": 72},
    "MAC10": {"BulletDropRange": 6, "WeaponRange": 18, "Grouping": 72, "AimAccuracy": 8},
    "Agram2000": {"AimAccuracy": 7, "BulletDropRange": 9, "WeaponRange": 24, "Grouping": 70},
    "HiPower": {"AimAccuracy": 9, "BulletDropRange": 7},
    "VectorCP1": {"AimAccuracy": 6, "BulletDropRange": 7},
    "PP19Bizon": {"BulletDropRange": 9},
    "SpectreM4": {"AimAccuracy": 9, "BulletDropRange": 10, "WeaponRange": 25},
    "AS_Val": {"WeaponRange": 36, "BulletDropRange": 15},
    "M1A": {"AimAccuracy": 14, "WeaponRange": 65, "BulletDropRange": 19},
    "SVU": {"AimAccuracy": 15, "WeaponRange": 75, "BulletDropRange": 19},
    "MP7": {"AimAccuracy": 11},
    "Striker": {"AimAccuracy": 10, "BulletDropRange": 8, "WeaponRange": 21},
    "MAS49": {"AimAccuracy": 12, "WeaponRange": 58},
    "AR10": {"WeaponRange": 58, "BulletDropRange": 18},
}

CSV_MAP = {
    "AimAccuracy": "aim_accuracy",
    "BulletDropRange": "bullet_drop_range",
    "WeaponRange": "weapon_range",
    "Grouping": "grouping",
}


def set_lua_field(text: str, key: str, value: int) -> str:
    pattern = rf"^(\t{key} = )-?\d+,"
    if re.search(pattern, text, flags=re.M):
        return re.sub(pattern, rf"\g<1>{value},", text, count=1, flags=re.M)
    # Insert after Damage line if possible, else after object_class block MagazineSize/WeaponRange
    for anchor in ("Damage = ", "ObjDamageMod = ", "MagazineSize = ", "WeaponRange = "):
        m = re.search(rf"^(\t{re.escape(anchor)}\d+,\n)", text, flags=re.M)
        if m:
            return text[: m.end()] + f"\t{key} = {value},\n" + text[m.end() :]
    raise SystemExit(f"cannot insert {key}")


def patch_lua_file(path: Path, fields: dict) -> None:
    text = path.read_text(encoding="utf-8")
    for k, v in fields.items():
        text = set_lua_field(text, k, v)
    path.write_text(text, encoding="utf-8")


def set_items_field(window: str, key: str, value: int) -> str:
    pattern = rf"('{key}', )-?\d+"
    if re.search(pattern, window):
        return re.sub(pattern, rf"\g<1>{value}", window, count=1)
    # insert after Damage or MagazineSize
    for anchor in ("'Damage', ", "'ObjDamageMod', ", "'MagazineSize', ", "'WeaponRange', "):
        m = re.search(rf"({re.escape(anchor)}\d+,\n)", window)
        if m:
            indent = "\t\t\t\t\t"
            return window[: m.end()] + f"{indent}'{key}', {value},\n" + window[m.end() :]
    raise SystemExit(f"items cannot insert {key}")


def patch_items(fields_by_id: dict) -> None:
    path = ROOT / "items.lua"
    text = path.read_text(encoding="utf-8")
    for wid, fields in fields_by_id.items():
        m = re.search(rf"'Id', \"{re.escape(wid)}\"", text)
        if not m:
            raise SystemExit(f"items.lua: Id {wid} not found")
        start = m.start()
        window = text[start : start + 4000]
        new_window = window
        for k, v in fields.items():
            new_window = set_items_field(new_window, k, v)
        text = text[:start] + new_window + text[start + len(window) :]
    path.write_text(text, encoding="utf-8")


def patch_csv(fields_by_id: dict) -> None:
    path = ROOT / "docs/technical/weapons/data/weapons.csv"
    rows = []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            upd = fields_by_id.get(row["id"])
            if upd:
                for k, v in upd.items():
                    row[CSV_MAP[k]] = str(v)
                # if AimAccuracy was defaulted, drop from defaulted_fields list optionally — skip
            rows.append(row)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def move_ar10dmr_to_sniper() -> None:
    p = ROOT / "InventoryItem/AR10DMR.lua"
    t = p.read_text(encoding="utf-8")
    t = t.replace('__parents = { "AssaultRifle" }', '__parents = { "SniperRifle" }')
    t = t.replace('object_class = "AssaultRifle"', 'object_class = "SniperRifle"')
    t = t.replace('CategoryPair = "AssaultRifles"', 'CategoryPair = "Rifles"')
    p.write_text(t, encoding="utf-8")

    items = ROOT / "items.lua"
    text = items.read_text(encoding="utf-8")
    idx = text.find("'Id', \"AR10DMR\"")
    if idx < 0:
        raise SystemExit("AR10DMR missing")
    chunk = text[idx : idx + 2500]
    chunk2 = chunk.replace("'object_class', \"AssaultRifle\"", "'object_class', \"SniperRifle\"", 1)
    chunk2 = chunk2.replace("'CategoryPair', \"AssaultRifles\"", "'CategoryPair', \"Rifles\"", 1)
    # Keep Group Rifles-Semi (same as M1A)
    text = text[:idx] + chunk2 + text[idx + len(chunk) :]
    items.write_text(text, encoding="utf-8")

    path = ROOT / "docs/technical/weapons/data/weapons.csv"
    rows = []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row["id"] == "AR10DMR":
                row["family_id"] = "sniper-rifle"
                row["family_name_ru"] = "Снайперские винтовки"
                row["object_class"] = "SniperRifle"
            rows.append(row)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print("AR10DMR -> SniperRifle / Rifles / sniper-rifle family")


def main():
    for wid, fields in UPDATES.items():
        path = ROOT / "InventoryItem" / f"{wid}.lua"
        if not path.exists():
            raise SystemExit(f"missing {path}")
        patch_lua_file(path, fields)
        print("ok", wid, fields)
    patch_items(UPDATES)
    print("items.lua ok")
    patch_csv(UPDATES)
    print("csv ok")
    move_ar10dmr_to_sniper()


if __name__ == "__main__":
    main()
