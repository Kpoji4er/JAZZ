# -*- coding: utf-8 -*-
"""Export JAZZ Ammo CaliberModification stats to JSON/CSV for analysis.

  python docs/tools/_export_ammo_stats.py
  python docs/tools/_export_ammo_stats.py --json Ammopics/_gen/ammo_stats.json
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INV = ROOT / "InventoryItem"

MOD_RE = re.compile(
    r"PlaceObj\(\s*'CaliberModification'\s*,\s*\{(?P<body>.*?)\}\s*\)",
    re.S,
)
FIELD_RE = re.compile(r"(mod_mul|mod_add|target_prop)\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|(-?\d+))")
KV_RE = re.compile(
    r"^\s*(Caliber|Cost|Tier|RestockWeight|MaxStock|CanAppearInShop|colorStyle|"
    r"CategoryPair|ShopStackSize|MaxStacks|Icon)\s*=\s*(.+?),\s*$",
    re.M,
)
NAME_RE = re.compile(
    r'DisplayName\s*=\s*T\(\s*\d+\s*,.*?\]\]\s*"((?:\\.|[^"\\])*)"\s*\)',
    re.S,
)
EFFECTS_RE = re.compile(r"AppliedEffects\s*=\s*\{([^}]*)\}", re.S)
ID_RE = re.compile(r"DefineClass\.(JAZZ_AMMO_\w+)\s*=")


def parse_display_name(text: str) -> str:
    m = NAME_RE.search(text)
    return m.group(1) if m else ""


def parse_mods(block: str) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for m in MOD_RE.finditer(block):
        body = m.group("body")
        fields: dict[str, object] = {}
        for fm in FIELD_RE.finditer(body):
            key = fm.group(1)
            val = fm.group(2) or fm.group(3) or fm.group(4)
            if key == "target_prop":
                fields["prop"] = val
            elif key in ("mod_mul", "mod_add"):
                fields[key] = int(val)
        prop = fields.get("prop")
        if not prop:
            continue
        out[str(prop)] = {
            "mod_mul": fields.get("mod_mul"),
            "mod_add": fields.get("mod_add"),
        }
    return out


def mul_or(default: int, v) -> int:
    return default if v is None else int(v)


def pen_display(mods: dict) -> str:
    """UI formula (AmmoRolloverHint): mul defaults 1000; only PenetrationBonus add."""
    pc = mods.get("PenetrationClass", {})
    pb = mods.get("PenetrationBonus", {})
    mul = mul_or(1000, pc.get("mod_mul"))
    add = 0 if pb.get("mod_add") is None else int(pb["mod_add"])
    tenths = int(round(mul / 100.0)) + add
    sign = "-" if tenths < 0 else ""
    tenths = abs(tenths)
    return f"{sign}{tenths // 10}.{tenths % 10}"


def format_mod(mods: dict, prop: str) -> str | None:
    m = mods.get(prop, {})
    parts: list[str] = []
    mul = m.get("mod_mul")
    add = m.get("mod_add")
    if mul is not None and mul != 1000:
        parts.append(f"{int(mul) / 10:.0f}%")
    if add is not None and add != 0:
        parts.append(f"{int(add):+d}")
    return " ".join(parts) if parts else None


def add_val(mods: dict, prop: str) -> int | None:
    m = mods.get(prop, {})
    if "mod_add" not in m or m["mod_add"] is None:
        return None
    return int(m["mod_add"])


def jam_pct(mods: dict) -> float | None:
    a = add_val(mods, "BaseJamChance")
    if a is None:
        return None
    return a / 10.0


def strip_val(raw: str) -> object:
    raw = raw.strip().rstrip(",")
    if raw in ("true", "false"):
        return raw == "true"
    if raw.startswith('"') or raw.startswith("'"):
        return raw.strip("\"'")
    try:
        return int(raw)
    except ValueError:
        return raw


def parse_file(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    mid = ID_RE.search(text)
    if not mid:
        return None
    mods_m = re.search(r"Modifications\s*=\s*\{(.*)\},\s*\n\s*(?:AppliedEffects|ammo_type)", text, re.S)
    mods_block = mods_m.group(1) if mods_m else ""
    # fallback: from Modifications to end of table before next top-level
    if not mods_block:
        mods_m = re.search(r"Modifications\s*=\s*\{(.*?)\},", text, re.S)
        mods_block = mods_m.group(1) if mods_m else ""
    mods = parse_mods(mods_block)
    meta = {k: strip_val(v) for k, v in KV_RE.findall(text)}
    eff_m = EFFECTS_RE.search(text)
    effects = []
    if eff_m:
        effects = re.findall(r'"([^"]+)"', eff_m.group(1))
    row = {
        "id": mid.group(1),
        "name": parse_display_name(text),
        "caliber": str(meta.get("Caliber", "")).replace("JAZZ_Caliber_", ""),
        "colorStyle": str(meta.get("colorStyle", "")),
        "cost": meta.get("Cost"),
        "tier": meta.get("Tier"),
        "rw": meta.get("RestockWeight"),
        "maxStock": meta.get("MaxStock"),
        "shop": meta.get("CanAppearInShop"),
        "shopStack": meta.get("ShopStackSize"),
        "maxStacks": meta.get("MaxStacks"),
        "icon": str(meta.get("Icon", "")).split("/")[-1],
        "effects": effects,
        "pen": pen_display(mods),
        "penClassAdd": add_val(mods, "PenetrationClass"),  # anomaly if set (UI uses mod_mul only)
        "dmg": format_mod(mods, "Damage"),
        "grouping": format_mod(mods, "Grouping"),
        "noise": format_mod(mods, "Noise"),
        "objDmg": format_mod(mods, "ObjDamageMod"),
        "reliability": add_val(mods, "Reliability"),
        "jamPct": jam_pct(mods),
        "crit": add_val(mods, "CritChance"),
        "recoil": add_val(mods, "Recoil"),
        "aimAccuracy": add_val(mods, "AimAccuracy"),
        "weaponRange": add_val(mods, "WeaponRange"),
        "bulletDrop": add_val(mods, "BulletDropRange"),
        "buckshot": format_mod(mods, "BuckshotProjectiles"),
        "overwatch": format_mod(mods, "OverwatchAngle"),
        "mods_raw": {
            k: {kk: vv for kk, vv in v.items() if vv is not None}
            for k, v in mods.items()
        },
    }
    return row


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", type=Path, default=ROOT / "Ammopics" / "_gen" / "ammo_stats.json")
    ap.add_argument("--csv", type=Path, default=ROOT / "Ammopics" / "_gen" / "ammo_stats.csv")
    args = ap.parse_args()

    rows = []
    for p in sorted(INV.glob("JAZZ_AMMO_*.lua")):
        if p.name.endswith("_copy.lua"):
            continue
        # skip mortar/ordnance shells for main small-arms table? include all ammo objects
        row = parse_file(p)
        if row:
            rows.append(row)

    rows.sort(key=lambda r: (r["caliber"], r["id"]))
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    cols = [
        "id", "name", "caliber", "colorStyle", "pen", "dmg", "grouping",
        "reliability", "jamPct", "crit", "recoil", "noise", "aimAccuracy",
        "weaponRange", "bulletDrop", "buckshot", "effects", "cost", "tier", "rw", "shop",
    ]
    with args.csv.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            rr = dict(r)
            rr["effects"] = ";".join(r["effects"])
            w.writerow(rr)

    calibers = sorted({r["caliber"] for r in rows})
    print(f"rows={len(rows)} calibers={len(calibers)}")
    print(f"json={args.json}")
    print(f"csv={args.csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
