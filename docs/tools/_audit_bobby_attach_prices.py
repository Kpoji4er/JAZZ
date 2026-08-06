# -*- coding: utf-8 -*-
"""Audit remountable weapon attachments for Bobby Ray ECON-004.

Usage:
  python docs/tools/_audit_bobby_attach_prices.py
  python docs/tools/_audit_bobby_attach_prices.py --json .tmp/bobby_attach_prices.json

Optics BR Tier from design docs (reflex/combat/long); other slots heuristic by Parts cost.
CategoryPair proposed: Optics | Magazines | Muzzle | Side | Under | Bipod | MiscAttach
  (new BobbyRayShopSubCategory under Other / or dedicated Attachments tab — implement later).

Cost proposed = Parts * 100 (fixes companion bug where Parts>=100 stayed as $100).
Restock: soft-tail like weapons (RW * 0.1^|T-U|); MaxStock=1 default.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INV = ROOT / "InventoryItem"
CSV = ROOT / "docs" / "technical" / "weapons" / "data" / "weapon-components.csv"
OPTIONS = ROOT / "docs" / "technical" / "weapons" / "data" / "weapon-component-options.csv"
WEAPON_JSON = ROOT / ".tmp" / "bobby_weapon_prices.json"

COST_RE = re.compile(r"(?<![A-Za-z])Cost\s*=\s*(\d+)")
TIER_RE = re.compile(r'(?<![A-Za-z])Tier\s*=\s*(?:"?(\d+)"?)')
RW_RE = re.compile(r"RestockWeight\s*=\s*(\d+)")
MS_RE = re.compile(r"MaxStock\s*=\s*(\d+)")
SHOP_RE = re.compile(r"CanAppearInShop\s*=\s*(true|false)")
REM_RE = re.compile(r'RemovableComponentId\s*=\s*"([^"]+)"')
DN_RE = re.compile(
    r'DisplayName\s*=\s*T\(\s*\d+\s*,\s*(?:--\[\[[^\]]*\]\]\s*)?"((?:\\.|[^"\\])*)"',
    re.S,
)
CAT_RE = re.compile(r'CategoryPair\s*=\s*"([^"]+)"')

# Design optic → BR tier (docs/design/*-tiers.md). Floor later by earliest Bobby host weapon.
# Owner 2026-08-07: 12× earlier (BR4); Eotech BR4.
OPTIC_BR: dict[str, tuple[int, str, str]] = {
    "JAZZ_Reflex_Garand": (1, "reflex", "Precision T1"),
    "JAZZ_Reflex_Aimpoint5000": (1, "reflex", "Precision T1"),
    "JAZZ_Reflex_Cobra": (1, "reflex", "Overwatch T1"),
    "JAZZ_Reflex_Closed": (2, "reflex", "Precision T2"),
    "JAZZ_Reflex_Open": (2, "reflex", "Overwatch T2"),
    "JAZZ_Reflex_Pistol": (2, "reflex", "Overwatch T2"),
    "JAZZ_Reflex_M68": (3, "reflex", "Precision T3"),
    "JAZZ_Reflex_Eotech": (4, "reflex", "Universal T4 (owner)"),
    "JAZZ_Reflex_PKAS": (4, "reflex", "Precision T4"),
    "JAZZ_CombatScope_2x": (1, "combat", "Combat T1"),
    "JAZZ_CombatScope_3x": (2, "combat", "Combat T2"),
    "JAZZ_G36Scope": (2, "combat", "Combat T2 integral — out"),
    "JAZZ_G36Sight": (1, "combat", "G36 1.5× integral — out"),
    "JAZZ_CombatScope_ACOG": (3, "combat", "Combat T3"),
    "JAZZ_CombatScope_1P29": (3, "combat", "Combat T3"),
    "JAZZ_CombatScope_FeroZ24": (3, "combat", "Combat T3"),
    "JAZZ_Scope_PU": (1, "long", "Long T1"),
    "JAZZ_Scope_Garand": (1, "long", "Long T1"),
    "JAZZ_Scope_Springfield": (1, "long", "Long T1"),
    "JAZZ_Scope_PSO": (2, "long", "Long T2"),
    "JAZZ_Scope_ZF4": (2, "long", "Long T2"),
    "JAZZ_Scope_ZRAK": (2, "long", "Long T2-ish 4×"),
    "JAZZ_Scope_PSG": (3, "long", "Long T3 6× PSG"),
    "JAZZ_Scope_6x": (3, "long", "Long T3"),
    "JAZZ_Scope_DA15_6x": (3, "long", "Long T3"),
    "JAZZ_Scope_Scout": (4, "long", "Long T4"),
    "JAZZ_Scope_8x_SCROME": (4, "long", "Long T4"),
    "JAZZ_Scope_3x_9x": (4, "long", "Long T4"),
    "JAZZ_Scope_12x": (4, "long", "Long T4 earlier (was T5; owner)"),
    "JAZZ_NightScope_NSPU": (3, "night", "Night mid"),
    "JAZZ_NightScope": (4, "night", "Night 5×"),
    "JAZZ_NightScope_M3": (1, "night", "M3 night — M1/M2 carbine (owner BR1)"),
}

# Integral / mis-slot / defaults
OUT_OPTICS = {
    "JAZZ_G36Scope",
    "JAZZ_G36Sight",
    "JAZZ_AUGScope_Default",
    "JAZZ_FlashlightDot_Anaconda",
    "JAZZ_LaserDot_Anaconda",
    "JAZZ_UVDot_Anaconda",
}

# Cold War / WW2–surplus optics — вне Bobby (owner 2026-08-07)
COLD_WAR_OUT = {
    "JAZZ_Reflex_Garand",
    "JAZZ_Scope_Garand",
    "JAZZ_Scope_Springfield",
    "JAZZ_Scope_PU",
    "JAZZ_Scope_ZF4",
    "JAZZ_Scope_ZRAK",
    "JAZZ_Scope_PSO",
    "JAZZ_Scope_PSG",
    "JAZZ_Scope_DA15_6x",
    "JAZZ_CombatScope_1P29",
    "JAZZ_CombatScope_FeroZ24",
    "JAZZ_NightScope_NSPU",
}

SKIP_ALWAYS = {
    "JAZZ_FlashlightOff",
    "JAZZ_SuppressorIntegrated",
    "JAZZ_RemovableAttachment",
}


def slot_to_category(slot: str, cid: str) -> str:
    if cid in OPTIC_BR or slot == "Scope":
        if cid.startswith("JAZZ_Flashlight") or cid.startswith("JAZZ_Laser") or cid.startswith("JAZZ_UV"):
            return "Side"
        if "Iron" in cid or "Ironsight" in cid:
            return "Optics"  # irons not remountable usually
        return "Optics"
    s = (slot or "").lower()
    if s in ("magazine",):
        return "Magazines"
    if s in ("muzzle",):
        return "Muzzle"
    if s in ("side",):
        return "Side"
    if s in ("under", "grenadelauncher"):
        return "Under"
    if s in ("bipod",):
        return "Bipod"
    return "MiscAttach"


def heuristic_br(parts: int | None, category: str) -> int:
    """Fallback BR for non-optic remountables by Parts cost band."""
    p = parts or 20
    if category == "Magazines":
        if p <= 20:
            return 1
        if p <= 35:
            return 2
        if p <= 50:
            return 3
        if p <= 70:
            return 4
        return 5
    if category == "Muzzle":
        if p <= 25:
            return 1
        if p <= 40:
            return 2
        if p <= 60:
            return 3
        if p <= 80:
            return 4
        return 5
    if category == "Side":
        if p <= 30:
            return 1
        if p <= 45:
            return 2
        if p <= 60:
            return 3
        return 4
    if category == "Under":
        if "Grenade" in (category,) or p >= 80:
            return 4
        if p <= 25:
            return 1
        if p <= 45:
            return 2
        if p <= 65:
            return 3
        return 4
    if category == "Bipod":
        return 2 if p <= 40 else 3
    # MiscAttach
    if p <= 25:
        return 1
    if p <= 50:
        return 2
    if p <= 75:
        return 3
    return 4


def rw_for(br: int, category: str) -> int:
    base = {1: 40, 2: 28, 3: 18, 4: 10, 5: 5}.get(br, 15)
    if category == "Optics" and br >= 4:
        return max(3, base - 2)
    if category == "Magazines" and br <= 2:
        return base + 10
    return base


def load_csv() -> dict[str, dict]:
    out: dict[str, dict] = {}
    with CSV.open(encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            cid = (row.get("component_id") or row.get("id") or "").strip()
            if not cid.startswith("JAZZ_"):
                continue
            slot = (row.get("slot") or "").strip()
            parts_s = (row.get("cost") or "").strip()
            name = (row.get("display_name") or cid).strip()
            try:
                parts = int(float(parts_s)) if parts_s not in ("", "-", None) else None
            except ValueError:
                parts = None
            out[cid] = {"slot": slot, "parts": parts, "name": name, "raw": row}
    return out


def parse_companion(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    if "RemovableComponentId" not in text and 'object_class = "JAZZ_RemovableAttachment"' not in text:
        return None
    m_rem = REM_RE.search(text)
    return {
        "cost_cur": int(COST_RE.search(text).group(1)) if COST_RE.search(text) else None,
        "tier_cur": int(TIER_RE.search(text).group(1)) if TIER_RE.search(text) else None,
        "rw_cur": int(RW_RE.search(text).group(1)) if RW_RE.search(text) else None,
        "max_cur": int(MS_RE.search(text).group(1)) if MS_RE.search(text) else None,
        "shop_cur": SHOP_RE.search(text).group(1) if SHOP_RE.search(text) else None,
        "display": (DN_RE.search(text).group(1).replace('\\"', '"') if DN_RE.search(text) else path.stem),
        "category_pair_cur": CAT_RE.search(text).group(1) if CAT_RE.search(text) else None,
        "rem_id": m_rem.group(1) if m_rem else path.stem,
    }


def load_bobby_weapon_br() -> dict[str, int]:
    """weapon_id → proposed Bobby BR tier (shop=bobby only)."""
    if not WEAPON_JSON.exists():
        return {}
    raw = json.loads(WEAPON_JSON.read_text(encoding="utf-8"))
    rows = raw if isinstance(raw, list) else raw.get("rows") or []
    out: dict[str, int] = {}
    for r in rows:
        if r.get("shop") != "bobby":
            continue
        wid = r.get("id")
        br = r.get("br_tier")
        if wid and br is not None:
            out[str(wid)] = int(br)
    return out


def load_component_hosts() -> dict[str, set[str]]:
    """component_id → set of weapon_ids that list it in AvailableComponents."""
    hosts: dict[str, set[str]] = {}
    if not OPTIONS.exists():
        return hosts
    with OPTIONS.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            cid = (row.get("component_id") or "").strip()
            wid = (row.get("weapon_id") or "").strip()
            if not cid or not wid:
                continue
            hosts.setdefault(cid, set()).add(wid)
    return hosts


def earliest_bobby_host(
    cid: str, hosts: dict[str, set[str]], weapon_br: dict[str, int]
) -> tuple[int | None, list[str]]:
    """Return (min BR among Bobby hosts, sample host ids). None if no Bobby host."""
    wids = hosts.get(cid) or set()
    bobby_hosts = sorted((w, weapon_br[w]) for w in wids if w in weapon_br)
    if not bobby_hosts:
        return None, []
    mn = min(br for _, br in bobby_hosts)
    samples = [w for w, br in bobby_hosts if br == mn][:4]
    return mn, samples


def build_rows() -> list[dict]:
    csv_data = load_csv()
    weapon_br = load_bobby_weapon_br()
    hosts = load_component_hosts()
    rows: list[dict] = []
    seen: set[str] = set()

    for path in sorted(INV.glob("JAZZ_*.lua")):
        cur = parse_companion(path)
        if not cur:
            continue
        cid = path.stem
        seen.add(cid)
        if cid in SKIP_ALWAYS:
            continue

        meta = csv_data.get(cid, {})
        slot = meta.get("slot") or "?"
        parts = meta.get("parts")
        category = slot_to_category(slot, cid)

        shop = "bobby"
        note_parts: list[str] = []
        family = category.lower()
        design_br: int

        if cid in OUT_OPTICS or (cid.endswith("_Anaconda") and "Scope" in (slot or "")):
            shop = "out_weapon_locked"
            note_parts.append("weapon-integral / Anaconda mis-slot")
        if "Iron" in cid or "Ironsight" in cid:
            shop = "out_iron"
            note_parts.append("irons not sold as remountable")
        if cid in COLD_WAR_OUT:
            shop = "out_coldwar"
            note_parts.append("Cold War / surplus optic — out (owner)")

        if cid in OPTIC_BR:
            design_br, family, note2 = OPTIC_BR[cid]
            note_parts.append(note2)
            if cid in OUT_OPTICS:
                shop = "out_integral"
        else:
            design_br = heuristic_br(parts, category)
            note_parts.append(f"heuristic Parts={parts}")

        # underslung GL
        if any(x in cid for x in ("GrenadeLauncher", "GP25", "M70_Grenade", "Underbarrel")):
            if "Grenade" in cid or "GP25" in cid:
                shop = "out_gl"
                note_parts.append("underslung GL — вне витрины")

        host_br, host_samples = earliest_bobby_host(cid, hosts, weapon_br)
        if shop == "bobby":
            if host_br is None:
                shop = "out_no_host"
                note_parts.append("no Bobby host weapon")
            else:
                br = max(design_br, host_br)
                if br > design_br:
                    note_parts.append(f"floor BR{design_br}→{br} vs hosts {','.join(host_samples)}")
                else:
                    note_parts.append(f"hosts≥BR{host_br} ({','.join(host_samples)})")
                design_br = br

        cost_prop = (parts * 100) if parts is not None else cur["cost_cur"]
        if parts is not None and parts >= 100 and cur["cost_cur"] is not None and cur["cost_cur"] <= parts + 30:
            cost_prop = parts * 100
            note_parts.append("Cost fix Parts×100")

        note = "; ".join(note_parts)
        if shop.startswith("out_"):
            action = "SET_FALSE"
            rule = "out"
            tier_out = design_br if cid in OPTIC_BR or host_br else cur["tier_cur"]
            rows.append(
                {
                    "id": cid,
                    "display": cur["display"],
                    "slot": slot,
                    "family": family,
                    "category": category,
                    "CategoryPair_cur": cur["category_pair_cur"],
                    "CategoryPair": cur["category_pair_cur"],
                    "shop": shop,
                    "Parts": parts,
                    "Cost_cur": cur["cost_cur"],
                    "Cost": cost_prop,
                    "delta_cost": (cost_prop or 0) - (cur["cost_cur"] or 0) if cost_prop is not None else 0,
                    "Tier_cur": cur["tier_cur"],
                    "Tier": tier_out,
                    "host_br": host_br,
                    "RestockWeight_cur": cur["rw_cur"],
                    "RestockWeight": cur["rw_cur"],
                    "MaxStock": 1,
                    "CanAppearInShop_cur": cur["shop_cur"],
                    "action": action,
                    "rule": rule,
                    "note": note,
                }
            )
            continue

        br = design_br
        rows.append(
            {
                "id": cid,
                "display": cur["display"],
                "slot": slot,
                "family": family,
                "category": category,
                "CategoryPair_cur": cur["category_pair_cur"],
                "CategoryPair": category,
                "shop": shop,
                "Parts": parts,
                "Cost_cur": cur["cost_cur"],
                "Cost": cost_prop,
                "delta_cost": (cost_prop or 0) - (cur["cost_cur"] or 0) if cost_prop is not None else 0,
                "Tier_cur": cur["tier_cur"],
                "Tier": br,
                "host_br": host_br,
                "RestockWeight_cur": cur["rw_cur"],
                "RestockWeight": rw_for(br, category),
                "MaxStock": 1,
                "CanAppearInShop_cur": cur["shop_cur"],
                "action": "KEEP",
                "rule": "soft_tail",
                "note": note,
            }
        )

    for cid, meta in sorted(csv_data.items()):
        if cid in seen or cid in SKIP_ALWAYS:
            continue
        if meta.get("slot") != "Scope":
            continue
        shop = "out_no_inv"
        note = "no remountable INV (iron/default)"
        if cid in COLD_WAR_OUT:
            shop = "out_coldwar"
            note = "Cold War; no INV"
        rows.append(
            {
                "id": cid,
                "display": meta.get("name") or cid,
                "slot": "Scope",
                "family": "iron" if "Iron" in cid else "out",
                "category": "Optics",
                "CategoryPair_cur": None,
                "CategoryPair": None,
                "shop": shop,
                "Parts": meta.get("parts"),
                "Cost_cur": None,
                "Cost": (meta["parts"] * 100) if meta.get("parts") else None,
                "delta_cost": 0,
                "Tier_cur": None,
                "Tier": OPTIC_BR.get(cid, (None, None, None))[0],
                "host_br": None,
                "RestockWeight_cur": None,
                "RestockWeight": None,
                "MaxStock": None,
                "CanAppearInShop_cur": None,
                "action": "SKIP",
                "rule": "out",
                "note": note,
            }
        )

    rows.sort(
        key=lambda r: (
            0 if r["shop"] == "bobby" else 1,
            {"Optics": 0, "Magazines": 1, "Muzzle": 2, "Side": 3, "Under": 4, "Bipod": 5}.get(r["category"], 9),
            r.get("Tier") or 99,
            r["id"],
        )
    )
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=Path, default=ROOT / ".tmp" / "bobby_attach_prices.json")
    ap.add_argument("--tsv", type=Path, default=ROOT / ".tmp" / "bobby_attach_prices.tsv")
    args = ap.parse_args()

    rows = build_rows()
    by_cat: dict[str, int] = {}
    by_shop: dict[str, int] = {}
    for r in rows:
        by_cat[r["category"]] = by_cat.get(r["category"], 0) + 1
        by_shop[r["shop"]] = by_shop.get(r["shop"], 0) + 1

    payload = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "rule": (
            "soft-tail; BR = max(design, earliest Bobby host weapon); "
            "Cold War optics out; 12× BR4; Eotech BR4; Cost=Parts*100; "
            "CategoryPair Optics|Magazines|Muzzle|Side|Under|Bipod"
        ),
        "counts": {"total": len(rows), "by_category": by_cat, "by_shop": by_shop},
        "rows": rows,
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    cols = [
        "id",
        "display",
        "category",
        "family",
        "shop",
        "Parts",
        "Cost_cur",
        "Cost",
        "Tier_cur",
        "Tier",
        "RestockWeight",
        "note",
    ]
    lines = ["\t".join(cols)]
    for r in rows:
        lines.append("\t".join("" if r.get(c) is None else str(r.get(c)) for c in cols))
    args.tsv.write_text("\n".join(lines) + "\n", encoding="utf-8")

    bobby = sum(1 for r in rows if r["shop"] == "bobby")
    optics = sum(1 for r in rows if r["category"] == "Optics" and r["shop"] == "bobby")
    print(f"total={len(rows)} bobby={bobby} optics_bobby={optics}")
    print("by_shop", by_shop)
    print("by_cat", by_cat)
    print(f"wrote {args.json}")


if __name__ == "__main__":
    main()
