# -*- coding: utf-8 -*-
"""Apply ECON-004 Bobby Ray catalog fields from .tmp/bobby_*_prices.json.

Patches InventoryItem companions + matching ModItem blocks in items.lua:
  Cost, Tier, RestockWeight, MaxStock (when set), CanAppearInShop, CategoryPair (attach).

Usage:
  python docs/tools/_apply_bobby_catalog.py           # dry-run
  python docs/tools/_apply_bobby_catalog.py --apply
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INV = ROOT / "InventoryItem"
ITEMS = ROOT / "items.lua"
TMP = ROOT / ".tmp"

COST_RE = re.compile(r"(?<![A-Za-z])Cost\s*=\s*[^,\n]+")
TIER_RE = re.compile(r"(?<![A-Za-z])Tier\s*=\s*[^,\n]+")
RW_RE = re.compile(r"RestockWeight\s*=\s*[^,\n]+")
MS_RE = re.compile(r"MaxStock\s*=\s*[^,\n]+")
CAS_RE = re.compile(r"CanAppearInShop\s*=\s*(true|false)")
CAT_RE = re.compile(r'CategoryPair\s*=\s*"[^"]*"')


def load_rows() -> list[dict]:
    """Normalize all audit JSONs into apply rows."""
    out: list[dict] = []

    def add(row: dict, *, cost_key: str, tier_key: str, rw_key: str) -> None:
        item_id = row.get("id")
        if not item_id:
            return
        shop = row.get("shop") or ""
        cost = row.get(cost_key)
        tier = row.get(tier_key)
        rw = row.get(rw_key)
        ms = row.get("MaxStock") if "MaxStock" in row else row.get("maxstock")
        cat = row.get("CategoryPair")
        rule = row.get("rule")

        in_shop = shop in ("bobby", "specialty", "rare") or (
            shop == "cross_consumable"
        )
        # weapons/armor/ammo use shop=bobby or out_*
        if shop == "bobby":
            in_shop = True
        if isinstance(shop, str) and shop.startswith("out"):
            in_shop = False
        if shop.startswith("cross_ammo") or shop.startswith("cross_") and shop != "cross_consumable":
            # ammo/mortar handled in their primary audit; skip cross to avoid double
            if shop != "cross_consumable":
                return

        if shop == "cross_consumable":
            # BlackPowder applied via consumables flat — keep
            in_shop = True

        cas = True if in_shop else False
        # specialty/rare still in shop
        if shop in ("specialty", "rare"):
            cas = True
            in_shop = True

        out.append(
            {
                "id": item_id,
                "shop": shop,
                "Cost": int(cost) if cost is not None else None,
                "Tier": int(tier) if tier is not None else None,
                "RestockWeight": int(rw) if rw is not None else None,
                "MaxStock": int(ms) if ms is not None else None,
                "CategoryPair": cat if in_shop and cat else None,
                "CanAppearInShop": cas,
                "rule": rule,
                "source": row.get("_src"),
            }
        )

    # weapons
    weapons = json.loads((TMP / "bobby_weapon_prices.json").read_text(encoding="utf-8"))
    if isinstance(weapons, dict):
        weapons = weapons.get("rows") or []
    for r in weapons:
        r["_src"] = "weapon"
        add(r, cost_key="proposed", tier_key="br_tier", rw_key="rw")

    armor = json.loads((TMP / "bobby_armor_prices.json").read_text(encoding="utf-8"))
    if isinstance(armor, dict):
        armor = armor.get("rows") or []
    for r in armor:
        r["_src"] = "armor"
        add(r, cost_key="proposed", tier_key="br_tier", rw_key="rw")

    ammo = json.loads((TMP / "bobby_ammo_prices.json").read_text(encoding="utf-8"))
    if isinstance(ammo, dict):
        ammo = ammo.get("rows") or []
    for r in ammo:
        r["_src"] = "ammo"
        add(r, cost_key="proposed", tier_key="br_tier", rw_key="rw")

    for name, cost_k, tier_k, rw_k in (
        ("bobby_consumables_prices.json", "Cost", "Tier", "RestockWeight"),
        ("bobby_attach_prices.json", "Cost", "Tier", "RestockWeight"),
        ("bobby_explosive_prices.json", "Cost", "Tier", "RestockWeight"),
    ):
        raw = json.loads((TMP / name).read_text(encoding="utf-8"))
        rows = raw.get("rows") if isinstance(raw, dict) else raw
        for r in rows or []:
            r["_src"] = name
            add(r, cost_key=cost_k, tier_key=tier_k, rw_key=rw_k)

    # last wins for same id (explosives override consumables TNT etc.)
    by_id: dict[str, dict] = {}
    for r in out:
        by_id[r["id"]] = r
    return list(by_id.values())


def ensure_companion_prop(text: str, name: str, value: str, after: str | None = None) -> tuple[str, bool]:
    pat = re.compile(rf"(?<![A-Za-z]){name}\s*=\s*[^,\n]+")
    if pat.search(text):
        new, n = pat.subn(f"{name} = {value}", text, count=1)
        return new, n > 0 and new != text
    # insert
    anchors = [
        after,
        "CanAppearInShop",
        "Cost",
        "CategoryPair",
        "object_class",
    ]
    for a in anchors:
        if not a:
            continue
        m = re.search(rf"({a}\s*=\s*[^,\n]+,)", text)
        if m:
            insert = f"{m.group(1)}\n\t{name} = {value},"
            return text.replace(m.group(1), insert, 1), True
    # before closing
    if "\n}" in text:
        return text.replace("\n}", f"\n\t{name} = {value},\n}}", 1), True
    return text, False


def patch_companion(path: Path, row: dict) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text
    cas = "true" if row["CanAppearInShop"] else "false"
    if CAS_RE.search(text):
        text = CAS_RE.sub(f"CanAppearInShop = {cas}", text, count=1)
    else:
        text, _ = ensure_companion_prop(text, "CanAppearInShop", cas, after="Cost")

    if row["Cost"] is not None:
        if COST_RE.search(text):
            text = COST_RE.sub(f"Cost = {row['Cost']}", text, count=1)
        else:
            text, _ = ensure_companion_prop(text, "Cost", str(row["Cost"]))

    if row["CanAppearInShop"]:
        if row["Tier"] is not None:
            if TIER_RE.search(text):
                text = TIER_RE.sub(f"Tier = {row['Tier']}", text, count=1)
            else:
                text, _ = ensure_companion_prop(text, "Tier", str(row["Tier"]), after="CanAppearInShop")
        if row["RestockWeight"] is not None:
            if RW_RE.search(text):
                text = RW_RE.sub(f"RestockWeight = {row['RestockWeight']}", text, count=1)
            else:
                text, _ = ensure_companion_prop(
                    text, "RestockWeight", str(row["RestockWeight"]), after="Tier"
                )
        if row["MaxStock"] is not None:
            if MS_RE.search(text):
                text = MS_RE.sub(f"MaxStock = {row['MaxStock']}", text, count=1)
            else:
                text, _ = ensure_companion_prop(
                    text, "MaxStock", str(row["MaxStock"]), after="RestockWeight"
                )
        if row.get("CategoryPair"):
            if CAT_RE.search(text):
                text = CAT_RE.sub(f'CategoryPair = "{row["CategoryPair"]}"', text, count=1)
            else:
                text, _ = ensure_companion_prop(
                    text, "CategoryPair", f'"{row["CategoryPair"]}"', after="CanAppearInShop"
                )
    return text != orig, text


def patch_items_block(block: str, row: dict) -> tuple[str, bool]:
    changed = False
    cas = "true" if row["CanAppearInShop"] else "false"
    if "'CanAppearInShop'," in block:
        block2, n = re.subn(
            r"'CanAppearInShop',\s*(true|false)",
            f"'CanAppearInShop', {cas}",
            block,
            count=1,
        )
        if n:
            block, changed = block2, True
    else:
        # insert after Id or Cost
        block2, n = re.subn(
            r"('Cost',\s*[^,\n]+,)",
            rf"\1\n\t\t\t\t\t'CanAppearInShop', {cas},",
            block,
            count=1,
        )
        if n:
            block, changed = block2, True

    def ensure(key: str, value: str) -> None:
        nonlocal block, changed
        q = f"'{key}',"
        if q in block:
            block2, n = re.subn(rf"'{key}',\s*[^,\n]+", f"'{key}', {value}", block, count=1)
            if n and block2 != block:
                block = block2
                changed = True
        else:
            block2, n = re.subn(
                rf"('CanAppearInShop',\s*{cas},)",
                rf"\1\n\t\t\t\t\t'{key}', {value},",
                block,
                count=1,
            )
            if n:
                block = block2
                changed = True

    if row["Cost"] is not None:
        ensure("Cost", str(row["Cost"]))
    if row["CanAppearInShop"]:
        if row["Tier"] is not None:
            ensure("Tier", str(row["Tier"]))
        if row["RestockWeight"] is not None:
            ensure("RestockWeight", str(row["RestockWeight"]))
        if row["MaxStock"] is not None:
            ensure("MaxStock", str(row["MaxStock"]))
        if row.get("CategoryPair"):
            ensure("CategoryPair", f'"{row["CategoryPair"]}"')
    return block, changed


def patch_items_lua(text: str, by_id: dict[str, dict]) -> tuple[str, int]:
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        block = m.group(0)
        idm = re.search(r"'Id',\s*\"([^\"]+)\"", block)
        if not idm:
            return block
        item_id = idm.group(1)
        row = by_id.get(item_id)
        if not row:
            return block
        new_block, ch = patch_items_block(block, row)
        if ch:
            count += 1
        return new_block

    new_text = re.sub(
        r"PlaceObj\('ModItemInventoryItemCompositeDef',\s*\{.*?\}\),",
        repl,
        text,
        flags=re.S,
    )
    return new_text, count


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    rows = load_rows()
    by_id = {r["id"]: r for r in rows}
    print(f"rows={len(rows)} bobby={sum(1 for r in rows if r['CanAppearInShop'])} out={sum(1 for r in rows if not r['CanAppearInShop'])}")

    companion_n = 0
    missing = []
    for item_id, row in sorted(by_id.items()):
        paths = list(INV.rglob(f"{item_id}.lua"))
        if not paths:
            missing.append(item_id)
            continue
        path = paths[0]
        changed, new_text = patch_companion(path, row)
        if changed:
            companion_n += 1
            if args.apply:
                path.write_text(new_text, encoding="utf-8", newline="\n")

    items_text = ITEMS.read_text(encoding="utf-8")
    new_items, items_n = patch_items_lua(items_text, by_id)
    if args.apply and items_n:
        ITEMS.write_text(new_items, encoding="utf-8", newline="\n")

    print(f"companions would_patch/patched={companion_n}")
    print(f"items.lua blocks={items_n}")
    print(f"missing companions={len(missing)}")
    if missing[:20]:
        print("  sample missing:", ", ".join(missing[:20]))
    if not args.apply:
        print("dry-run; pass --apply to write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
