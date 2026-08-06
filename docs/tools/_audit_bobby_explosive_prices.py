# -*- coding: utf-8 -*-
"""Audit explosives / grenades / demo for Bobby Ray ECON-004.

Usage:
  python docs/tools/_audit_bobby_explosive_prices.py
  python docs/tools/_audit_bobby_explosive_prices.py --json .tmp/bobby_explosive_prices.json

Restock: soft-tail like guns (RW × 0.1^|T−U|); price Cost × (3^Δ|0.3^|Δ|) × jitter.
BlackPowder stays consumables flat staple (listed here as cross-ref).
40mm packs / mortar shells → ammo audit (cross-ref out).
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INV = ROOT / "InventoryItem"

COST_RE = re.compile(r"(?<![A-Za-z])Cost\s*=\s*(\d+)")
TIER_RE = re.compile(r'(?<![A-Za-z])Tier\s*=\s*(?:"?(\d+)"?)')
RW_RE = re.compile(r"RestockWeight\s*=\s*(\d+)")
MS_RE = re.compile(r"MaxStock\s*=\s*(\d+)")
SHOP_RE = re.compile(r"CanAppearInShop\s*=\s*(true|false)")
DN_RE = re.compile(
    r'DisplayName\s*=\s*T\(\s*\d+\s*,\s*(?:--\[\[[^\]]*\]\]\s*)?"((?:\\.|[^"\\])*)"',
    re.S,
)
OC_RE = re.compile(r'object_class\s*=\s*"([^"]+)"')
CAT_RE = re.compile(r'CategoryPair\s*=\s*"([^"]+)"')

# id → (family, prop_cost|None, prop_rw, prop_tier, max_stock|None, note, shop, rule, category_pair)
# shop: bobby | rare | cross_consumable | out_*
CATALOG: dict[str, tuple[str, int | None, int, int | None, int | None, str, str, str, str]] = {
    # --- substances ---
    "TNT": ("substance", 150, 50, 1, 5, "TNT brick BR1", "bobby", "soft_tail", "Components"),
    "C4": ("substance", 350, 35, 2, 4, "C4 BR2", "bobby", "soft_tail", "Components"),
    "PETN": ("substance", 450, 25, 3, 3, "PETN BR3", "bobby", "soft_tail", "Components"),
    # --- fused products (rare, MaxStock1) ---
    "TimedTNT": ("fused", 600, 12, 2, 1, "Timed TNT", "bobby", "soft_tail", "Components"),
    "RemoteTNT": ("fused", 650, 10, 2, 1, "Remote TNT", "bobby", "soft_tail", "Components"),
    "ProximityTNT": ("fused", 650, 10, 2, 1, "Proximity TNT", "bobby", "soft_tail", "Components"),
    "TimedC4": ("fused", 900, 10, 3, 1, "Timed C4", "bobby", "soft_tail", "Components"),
    "RemoteC4": ("fused", 950, 8, 3, 1, "Remote C4", "bobby", "soft_tail", "Components"),
    "ProximityC4": ("fused", 950, 8, 3, 1, "Proximity C4", "bobby", "soft_tail", "Components"),
    "TimedPETN": ("fused", 1100, 6, 4, 1, "Timed PETN", "bobby", "soft_tail", "Components"),
    "RemotePETN": ("fused", 1200, 5, 4, 1, "Remote PETN", "bobby", "soft_tail", "Components"),
    "ProximityPETN": ("fused", 1200, 5, 4, 1, "Proximity PETN", "bobby", "soft_tail", "Components"),
    # --- throwables ---
    "Molotov": ("grenade", 150, 60, 1, 8, "Molotov BR1", "bobby", "soft_tail", "Grenade"),
    "PipeBomb": ("grenade", 120, 0, 1, None, "Pipe Bomb — out (owner)", "out_pipe", "out", "Grenade"),
    "FragGrenade": ("grenade", 300, 70, 1, 8, "Frag M24 BR1", "bobby", "soft_tail", "Grenade"),
    "HE_Grenade": ("grenade", 400, 45, 2, 6, "Mk2 HE BR2", "bobby", "soft_tail", "Grenade"),
    "SmokeGrenade": ("grenade", 300, 50, 1, 8, "Smoke BR1 (owner)", "bobby", "soft_tail", "Grenade"),
    "ConcussiveGrenade": ("grenade", 400, 35, 2, 5, "Flashbang BR2", "bobby", "soft_tail", "Grenade"),
    "TearGasGrenade": ("grenade", 450, 30, 2, 5, "Tear gas BR2", "bobby", "soft_tail", "Grenade"),
    "FlareStick": ("utility", 200, 40, 2, 8, "Flare stick BR2", "bobby", "soft_tail", "Grenade"),
    "GlowStick": ("utility", 100, 50, 1, 10, "Glow stick BR1", "bobby", "soft_tail", "Grenade"),
    "ShapedCharge": ("demo", 1500, 0, 3, None, "Shaped charge — out (owner)", "out_shaped", "out", "Components"),
    # --- RPG warhead ---
    "Warhead_Frag": ("ordnance", 900, 30, 2, 6, "PG-7V — with RPG7 BR2", "bobby", "soft_tail", "Ordnance"),
    # --- cross / out ---
    "BlackPowder": (
        "substance",
        200,
        80,
        1,
        10,
        "Gunpowder — consumables flat staple (not soft-tail here)",
        "cross_consumable",
        "flat",
        "Components",
    ),
    "ToxicGasGrenade": ("grenade", 800, 0, 3, None, "Mustard gas — chem out", "out_chem", "out", "Grenade"),
    "JAZZ_AMMO_40mmFragGrenade": (
        "ordnance",
        2400,
        35,
        2,
        5,
        "40mm frag — ammo audit",
        "cross_ammo",
        "out",
        "Ordnance",
    ),
    "JAZZ_AMMO_40mmFlashbangGrenade": (
        "ordnance",
        1800,
        30,
        2,
        5,
        "40mm flash — ammo audit",
        "cross_ammo",
        "out",
        "Ordnance",
    ),
    "FlareAmmo": (
        "ordnance",
        150,
        40,
        1,
        8,
        "Flare cartridge — ammo audit",
        "cross_ammo",
        "out",
        "UtilityAmmo",
    ),
    "JAZZ_AMMO_MortarShell_HE": (
        "ordnance",
        350,
        0,
        2,
        None,
        "mortar — out_mortar (ammo)",
        "out_mortar",
        "out",
        "Ordnance",
    ),
    "JAZZ_AMMO_MortarShell_Smoke": (
        "ordnance",
        350,
        0,
        2,
        None,
        "mortar smoke — out",
        "out_mortar",
        "out",
        "Ordnance",
    ),
    "JAZZ_AMMO_MortarShell_Gas": (
        "ordnance",
        350,
        0,
        3,
        None,
        "mortar gas — out",
        "out_mortar",
        "out",
        "Ordnance",
    ),
}


def parse_item(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    return {
        "cost_cur": int(COST_RE.search(text).group(1)) if COST_RE.search(text) else None,
        "tier_cur": int(TIER_RE.search(text).group(1)) if TIER_RE.search(text) else None,
        "rw_cur": int(RW_RE.search(text).group(1)) if RW_RE.search(text) else None,
        "max_cur": int(MS_RE.search(text).group(1)) if MS_RE.search(text) else None,
        "shop_cur": SHOP_RE.search(text).group(1) if SHOP_RE.search(text) else None,
        "display": (
            DN_RE.search(text).group(1).replace('\\"', '"') if DN_RE.search(text) else path.stem
        ),
        "object_class": OC_RE.search(text).group(1) if OC_RE.search(text) else None,
        "category_pair": CAT_RE.search(text).group(1) if CAT_RE.search(text) else None,
    }


def build_rows() -> list[dict]:
    rows: list[dict] = []
    for item_id, (
        family,
        prop_cost,
        prop_rw,
        prop_tier,
        prop_ms,
        note,
        shop,
        rule,
        cat_pair,
    ) in CATALOG.items():
        path = INV / f"{item_id}.lua"
        in_bobby = shop == "bobby"
        if not path.exists():
            rows.append(
                {
                    "id": item_id,
                    "display": item_id,
                    "family": family,
                    "shop": shop,
                    "missing": True,
                    "note": f"MISSING — {note}",
                    "Cost_cur": None,
                    "Cost": prop_cost,
                    "Tier_cur": None,
                    "Tier": prop_tier,
                    "RestockWeight_cur": None,
                    "RestockWeight": prop_rw,
                    "MaxStock": prop_ms,
                    "CategoryPair": cat_pair,
                    "action": "SKIP",
                    "rule": rule,
                }
            )
            continue
        cur = parse_item(path)
        cost = prop_cost if prop_cost is not None else cur["cost_cur"]
        action = "KEEP"
        if shop.startswith("out_") or shop.startswith("cross_"):
            if shop.startswith("out_") and cur["shop_cur"] != "false":
                action = "SET_FALSE" if shop.startswith("out_") else "CROSS"
            else:
                action = "CROSS" if shop.startswith("cross_") else "KEEP_OUT"
        elif cur["shop_cur"] == "false":
            action = "SET_TRUE"

        rows.append(
            {
                "id": item_id,
                "display": cur["display"],
                "family": family,
                "shop": shop,
                "missing": False,
                "note": note,
                "Cost_cur": cur["cost_cur"],
                "Cost": cost,
                "Tier_cur": cur["tier_cur"],
                "Tier": prop_tier if in_bobby or shop == "cross_consumable" else cur["tier_cur"],
                "RestockWeight_cur": cur["rw_cur"],
                "RestockWeight": prop_rw if in_bobby or shop == "cross_consumable" else cur["rw_cur"],
                "MaxStock_cur": cur["max_cur"],
                "MaxStock": prop_ms if in_bobby else cur["max_cur"],
                "CanAppearInShop_cur": cur["shop_cur"],
                "CategoryPair_cur": cur["category_pair"],
                "CategoryPair": cat_pair if in_bobby else cur["category_pair"],
                "object_class": cur["object_class"],
                "delta_cost": (cost or 0) - (cur["cost_cur"] or 0) if cost is not None else 0,
                "action": action,
                "rule": rule,
            }
        )

    order = {"bobby": 0, "cross_consumable": 1, "cross_ammo": 2, "rare": 3}
    rows.sort(
        key=lambda r: (
            order.get(r["shop"], 9),
            r.get("Tier") or 99,
            r["family"],
            r["id"],
        )
    )
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=Path, default=ROOT / ".tmp" / "bobby_explosive_prices.json")
    ap.add_argument("--tsv", type=Path, default=ROOT / ".tmp" / "bobby_explosive_prices.tsv")
    args = ap.parse_args()

    rows = build_rows()
    by_shop: dict[str, int] = {}
    by_fam: dict[str, int] = {}
    for r in rows:
        by_shop[r["shop"]] = by_shop.get(r["shop"], 0) + 1
        by_fam[r["family"]] = by_fam.get(r["family"], 0) + 1

    payload = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "rule": (
            "explosives soft-tail like guns; TNT BR1 / C4 BR2 / PETN BR3; "
            "fused MaxStock1; grenades BR1–2 (Smoke BR1); out PipeBomb/ShapedCharge; "
            "BlackPowder→consumables flat; 40mm/mortar→ammo audit; owner OK catalog 2026-08-07"
        ),
        "counts": {
            "total": len(rows),
            "bobby": sum(1 for r in rows if r["shop"] == "bobby"),
            "by_shop": by_shop,
            "by_family": by_fam,
        },
        "rows": rows,
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    cols = [
        "id",
        "display",
        "family",
        "shop",
        "Cost_cur",
        "Cost",
        "Tier_cur",
        "Tier",
        "RestockWeight_cur",
        "RestockWeight",
        "MaxStock",
        "action",
        "note",
    ]
    lines = ["\t".join(cols)]
    for r in rows:
        lines.append("\t".join("" if r.get(c) is None else str(r.get(c)) for c in cols))
    args.tsv.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"bobby={payload['counts']['bobby']} total={len(rows)}")
    print("by_shop", by_shop)
    print(f"wrote {args.json}")


if __name__ == "__main__":
    main()
