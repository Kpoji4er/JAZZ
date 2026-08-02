#!/usr/bin/env python3
"""JAZZ-WEAPONS-006: migrate pellet count from AutoShots to BuckshotProjectiles.

Usage (jazz/):
  python docs/tools/_apply_buckshot_projectiles.py
  python docs/tools/_apply_buckshot_projectiles.py --apply
"""
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INV = ROOT / "InventoryItem"
ITEMS = ROOT / "items.lua"
CSV = ROOT / "docs/technical/weapons/data/weapons.csv"

SHOTGUN_IDS = (
    "AA12",
    "Auto5",
    "DoubleBarrelShotgun",
    "Ithaca",
    "M1897",
    "M41Shotgun",
    "R870",
    "SPAS12",
    "Stoeger",
    "Striker",
    "USAS12",
    "Auto5_quest",
)


def patch_shotgun_companion(text: str) -> str:
    if re.search(r"^(\tBuckshotProjectiles = )\d+", text, flags=re.M):
        text = re.sub(r"^(?P<p>\tBuckshotProjectiles = )\d+(?P<s>,?\s*)$", r"\g<p>1\g<s>", text, count=1, flags=re.M)
    else:
        m = re.search(r"^(\tBuckshotConeAngle = \d+,?\s*)$", text, flags=re.M)
        if m:
            text = text[: m.end()] + "\n\tBuckshotProjectiles = 1," + text[m.end() :]
        else:
            m = re.search(r"^(\tAutoShots = \d+,?\s*)$", text, flags=re.M)
            if m:
                text = text[: m.start()] + "\tBuckshotProjectiles = 1,\n" + text[m.start() :]
            else:
                text = text.rstrip() + "\n\tBuckshotProjectiles = 1,\n"
    text = re.sub(r"^(?P<p>\tAutoShots = )\d+(?P<s>,?\s*)$", r"\g<p>0\g<s>", text, count=1, flags=re.M)
    text = re.sub(r"^(?P<p>\tBurstShots = )\d+(?P<s>,?\s*)$", r"\g<p>0\g<s>", text, count=1, flags=re.M)
    return text


def patch_items(text: str) -> tuple[str, list[str]]:
    log: list[str] = []
    # CaliberModification target_prop (12g ammo only uses this for pellet count today)
    text2, c = re.subn(r'(target_prop = )"AutoShots"', r'\1"BuckshotProjectiles"', text)
    if c:
        log.append(f"ammo target_prop x{c}")
    text = text2

    for a, b in (
        (
            "local num_shots = weapon.AutoShots",
            "local num_shots = weapon.BuckshotProjectiles",
        ),
        (
            "args.num_shots = args.weapon and args.weapon.AutoShots or 12",
            "args.num_shots = args.weapon and args.weapon.BuckshotProjectiles or 1",
        ),
        (
            "args.num_shots = (args.weapon and args.weapon.AutoShots or 12) * 2",
            "args.num_shots = (args.weapon and args.weapon.BuckshotProjectiles or 1) * 2",
        ),
    ):
        if a in text:
            text = text.replace(a, b)
            log.append(f"combataction {a[:40]}...")

    for wid in SHOTGUN_IDS:
        needle = f"'Id', \"{wid}\""
        idx = text.find(needle)
        if idx < 0:
            log.append(f"items missing Id {wid}")
            continue
        p = text.rfind("PlaceObj('ModItemInventoryItemCompositeDef'", max(0, idx - 500), idx)
        if p < 0:
            log.append(f"items no PlaceObj for {wid}")
            continue
        end = text.find("\n\t\t\t\t\tPlaceObj('ModItemInventoryItemCompositeDef'", idx)
        if end < 0:
            end = text.find("\n\t\t\t\tPlaceObj('ModItemInventoryItemCompositeDef'", idx)
        if end < 0:
            end = min(len(text), idx + 25000)
        block = text[p:end]
        new_block = block
        if "'BuckshotProjectiles'" not in new_block:
            m = re.search(r"(\n)(\t+)'AutoShots',\s*\d+", new_block)
            if m:
                indent = m.group(2)
                new_block = (
                    new_block[: m.start()]
                    + f"\n{indent}'BuckshotProjectiles', 1,"
                    + f"\n{indent}'AutoShots', 0"
                    + new_block[m.end() :]
                )
            else:
                m = re.search(r"(\n)(\t+)'object_class',\s*\"Shotgun\",", new_block)
                if m:
                    indent = m.group(2)
                    new_block = (
                        new_block[: m.end()]
                        + f"\n{indent}'BuckshotProjectiles', 1,"
                        + new_block[m.end() :]
                    )
        else:
            new_block = re.sub(r"('BuckshotProjectiles',\s*)\d+", r"\g<1>1", new_block, count=1)
            new_block = re.sub(r"('AutoShots',\s*)\d+", r"\g<1>0", new_block, count=1)
        new_block = re.sub(r"('BurstShots',\s*)\d+", r"\g<1>0", new_block, count=1)
        if new_block != block:
            text = text[:p] + new_block + text[end:]
            log.append(f"items shotgun {wid}")
    return text, log


def patch_csv(apply: bool) -> int:
    with CSV.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    if "buckshot_projectiles" not in fieldnames:
        if "auto_shots" in fieldnames:
            fieldnames.insert(fieldnames.index("auto_shots") + 1, "buckshot_projectiles")
        else:
            fieldnames.append("buckshot_projectiles")
    n = 0
    for row in rows:
        if "buckshot_projectiles" not in row:
            row["buckshot_projectiles"] = ""
        if (row.get("object_class") or "").lower() != "shotgun":
            continue
        row["buckshot_projectiles"] = "1"
        row["auto_shots"] = "0"
        row["burst_shots"] = "0"
        n += 1
    if apply:
        with CSV.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
    return n


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    sg_n = ammo_n = 0
    for path in sorted(INV.rglob("*.lua")):
        text = path.read_text(encoding="utf-8", errors="replace")
        if re.search(r'object_class = "Shotgun"', text):
            new = patch_shotgun_companion(text)
            if new != text:
                print(("APPLY" if args.apply else "DRY"), "sg", path.relative_to(ROOT).as_posix())
                sg_n += 1
                if args.apply:
                    path.write_text(new, encoding="utf-8", newline="\n")
        elif 'target_prop = "AutoShots"' in text and (
            "12gauge" in path.name or "12g" in text[:500]
        ):
            new = text.replace('target_prop = "AutoShots"', 'target_prop = "BuckshotProjectiles"')
            print(("APPLY" if args.apply else "DRY"), "ammo", path.relative_to(ROOT).as_posix())
            ammo_n += 1
            if args.apply:
                path.write_text(new, encoding="utf-8", newline="\n")

    items = ITEMS.read_text(encoding="utf-8", errors="replace")
    new_items, log = patch_items(items)
    for line in log:
        print(("APPLY" if args.apply else "DRY"), line)
    if args.apply and new_items != items:
        ITEMS.write_text(new_items, encoding="utf-8", newline="\n")

    csv_n = patch_csv(args.apply)
    print(f"done sg={sg_n} ammo={ammo_n} csv_sg={csv_n} items_log={len(log)}")


if __name__ == "__main__":
    main()
