# -*- coding: utf-8 -*-
"""Audit medicine / tools / Meds·Parts for Bobby Ray ECON-004.

Usage:
  python docs/tools/_audit_bobby_consumables_prices.py
  python docs/tools/_audit_bobby_consumables_prices.py --json .tmp/bobby_consumables_prices.json

Restock:
  staples → effective_weight = RestockWeight (no Δ); available U>=1; price = Cost × jitter
  specialty medicine → soft-tail like guns (SurgicalKit T2, CombatStim/Metaviron T3)
  Medkit stays BR1 flat staple.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INV = ROOT / "InventoryItem"

COST_RE = re.compile(r"(?<![A-Za-z])Cost\s*=\s*(\d+)")
TIER_RE = re.compile(r'(?<![A-Za-z])Tier\s*=\s*(?:"?(\d+)"?)')
RW_RE = re.compile(r"RestockWeight\s*=\s*(\d+)")
SHOP_RE = re.compile(r"CanAppearInShop\s*=\s*(true|false)")
DISPLAY_RE = re.compile(
    r'DisplayName\s*=\s*T\(\s*\d+\s*,\s*(?:--\[\[[^\]]*\]\]\s*)?"((?:\\.|[^"\\])*)"',
    re.S,
)
OC_RE = re.compile(r'object_class\s*=\s*"([^"]+)"')
CAT_RE = re.compile(r'CategoryPair\s*=\s*"([^"]+)"')

# id → (category, proposed_cost|None=keep, proposed_rw, proposed_tier|None, note, shop, rule)
# shop: bobby | specialty | rare | out_*
# rule: flat (no Δ) | soft_tail (weapon-style 0.1^|Δ| + price 3^Δ) | out
CATALOG: dict[str, tuple[str, int | None, int, int | None, str, str, str]] = {
    # --- staples: flat from U=1 ---
    "Meds": ("resource", None, 150, 1, "Meds stack — always", "bobby", "flat"),
    "Parts": ("resource", None, 150, 1, "Parts stack — always", "bobby", "flat"),
    "JAZZ_Bandage": ("medicine", None, 150, 1, "Bandage", "bobby", "flat"),
    "JAZZ_Morphine": ("medicine", None, 75, 1, "Morphine", "bobby", "flat"),
    "FirstAidKit": ("medicine", None, 150, 1, "IFAK", "bobby", "flat"),
    "Medkit": ("medicine", None, 80, 1, "Med Kit BR1 (owner)", "bobby", "flat"),
    "Lockpick": ("tool", None, 100, 1, "Locksmith's Kit", "bobby", "flat"),
    "Wirecutter": ("tool", None, 100, 1, "Wire Cutter", "bobby", "flat"),
    "Crowbar": ("tool", None, 100, 1, "Crowbar", "bobby", "flat"),
    "BlackPowder": ("resource", None, 80, 1, "Gunpowder", "bobby", "flat"),
    "JAZZ_BarrelParts": ("resource", None, 75, 1, "Barrel parts", "bobby", "flat"),
    "JAZZ_ScopeParts": ("resource", None, 60, 1, "Scope parts", "bobby", "flat"),
    # --- specialty medicine: soft-tail by BR tier (owner 2026-08-07) ---
    "JAZZ_SurgicalKit": ("medicine", None, 25, 2, "Surgical Kit BR2", "specialty", "soft_tail"),
    "CombatStim": ("medicine", None, 25, 3, "Combat Stim BR3", "specialty", "soft_tail"),
    "MetaviraShot": ("medicine", None, 2, 3, "Metaviron BR3 MaxStock1", "specialty", "soft_tail"),
    # --- rare flat ---
    "SkillMag_Medical": ("medicine", None, 10, 1, "Medical skill mag — rare flat", "rare", "flat"),
    # TNT/C4/PETN → _audit_bobby_explosive_prices.py (not out here anymore)
    "Personal_Vicki_CustomTools": ("tool", None, 0, None, "unique", "out_unique", "out"),
    "PlasmaGun_Crowbar": ("tool", None, 0, None, "unique gag", "out_unique", "out"),
    "CustomPDA": ("tool", None, 0, None, "unique", "out_unique", "out"),
    "Microchip": ("resource", None, 15, 3, "craft CanAppearInShop=false", "out_craft", "out"),
    "OpticalLens": ("resource", None, 15, 2, "craft out", "out_craft", "out"),
    "FineSteelPipe": ("resource", None, 15, 2, "craft out", "out_craft", "out"),
    "HerbalMedicine": ("medicine", None, 0, None, "world/questish", "out_world", "out"),
    "Reanimationsset": ("medicine", None, 0, None, "no shop fields", "out_world", "out"),
    "MedicalReport": ("quest", None, 0, None, "QuestItem", "out_quest", "out"),
    "OilFilter": ("resource", None, 15, 2, "craft component — not staple", "out_craft", "out"),
    "Combination_WeavePadding": ("resource", None, 15, 2, "combination — later", "out_craft", "out"),
    "Combination_CeramicPlates": ("resource", None, 15, 2, "combination — later", "out_craft", "out"),
}


def parse_item(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    m_cost = COST_RE.search(text)
    m_tier = TIER_RE.search(text)
    m_rw = RW_RE.search(text)
    m_shop = SHOP_RE.search(text)
    m_dn = DISPLAY_RE.search(text)
    m_oc = OC_RE.search(text)
    m_cat = CAT_RE.search(text)
    return {
        "cost_cur": int(m_cost.group(1)) if m_cost else None,
        "tier_cur": int(m_tier.group(1)) if m_tier else None,
        "rw_cur": int(m_rw.group(1)) if m_rw else None,
        "shop_cur": m_shop.group(1) if m_shop else None,
        "display": m_dn.group(1).replace('\\"', '"') if m_dn else path.stem,
        "object_class": m_oc.group(1) if m_oc else None,
        "category_pair": m_cat.group(1) if m_cat else None,
    }


SHOP_ORDER = {"bobby": 0, "specialty": 1, "rare": 2}


def build_rows() -> list[dict]:
    rows: list[dict] = []
    for item_id, (cat, prop_cost, prop_rw, prop_tier, note, shop, rule) in CATALOG.items():
        path = INV / f"{item_id}.lua"
        in_shop = shop in ("bobby", "specialty", "rare")
        if not path.exists():
            rows.append(
                {
                    "id": item_id,
                    "display": item_id,
                    "category": cat,
                    "shop": shop,
                    "missing": True,
                    "note": f"MISSING companion — {note}",
                    "Cost_cur": None,
                    "Cost": prop_cost,
                    "Tier_cur": None,
                    "Tier": prop_tier if in_shop else None,
                    "RestockWeight_cur": None,
                    "RestockWeight": prop_rw,
                    "CanAppearInShop_cur": None,
                    "action": "SKIP",
                    "rule": rule,
                }
            )
            continue
        cur = parse_item(path)
        cost = prop_cost if prop_cost is not None else cur["cost_cur"]
        action = "KEEP"
        if shop.startswith("out_"):
            action = "SET_FALSE" if cur["shop_cur"] != "false" else "KEEP_OUT"
        elif cur["shop_cur"] == "false":
            action = "SET_TRUE"
        tier = prop_tier if in_shop else (prop_tier if prop_tier is not None else cur["tier_cur"])
        rows.append(
            {
                "id": item_id,
                "display": cur["display"],
                "category": cat,
                "shop": shop,
                "missing": False,
                "note": note,
                "Cost_cur": cur["cost_cur"],
                "Cost": cost,
                "Tier_cur": cur["tier_cur"],
                "Tier": tier,
                "RestockWeight_cur": cur["rw_cur"],
                "RestockWeight": prop_rw if in_shop else cur["rw_cur"],
                "CanAppearInShop_cur": cur["shop_cur"],
                "object_class": cur["object_class"],
                "category_pair": cur["category_pair"],
                "delta_cost": (cost or 0) - (cur["cost_cur"] or 0) if cost is not None else 0,
                "action": action,
                "rule": rule,
            }
        )
    rows.sort(
        key=lambda r: (
            SHOP_ORDER.get(r["shop"], 9),
            r.get("Tier") or 99,
            r["category"],
            r["id"],
        )
    )
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=Path, default=ROOT / ".tmp" / "bobby_consumables_prices.json")
    ap.add_argument("--tsv", type=Path, default=ROOT / ".tmp" / "bobby_consumables_prices.tsv")
    args = ap.parse_args()

    rows = build_rows()
    payload = {
        "generated": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
        "rule": (
            "staples flat: RW only, U>=1, price=Cost*jitter; "
            "specialty medicine soft_tail: RW*0.1^|T-U|, price Cost*(3^Δ|0.3^|Δ|)*jitter "
            "(Medkit T1 flat; SurgicalKit T2; CombatStim+Metaviron T3)"
        ),
        "bobby_count": sum(1 for r in rows if r["shop"] == "bobby"),
        "specialty_count": sum(1 for r in rows if r["shop"] == "specialty"),
        "rare_count": sum(1 for r in rows if r["shop"] == "rare"),
        "out_count": sum(1 for r in rows if str(r["shop"]).startswith("out_")),
        "rows": rows,
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    cols = [
        "id",
        "display",
        "category",
        "shop",
        "Cost_cur",
        "Cost",
        "Tier_cur",
        "Tier",
        "RestockWeight_cur",
        "RestockWeight",
        "action",
        "note",
    ]
    lines = ["\t".join(cols)]
    for r in rows:
        lines.append("\t".join("" if r.get(c) is None else str(r.get(c)) for c in cols))
    args.tsv.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(
        f"bobby={payload['bobby_count']} specialty={payload['specialty_count']} "
        f"rare={payload['rare_count']} out={payload['out_count']}"
    )
    print(f"wrote {args.json}")
    print(f"wrote {args.tsv}")


if __name__ == "__main__":
    main()
