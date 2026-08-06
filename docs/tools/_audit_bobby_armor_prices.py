# -*- coding: utf-8 -*-
"""Audit armor InventoryItem.Cost / Bobby Tier for ECON-004 companion pass.

Usage:
  python docs/tools/_audit_bobby_armor_prices.py
  python docs/tools/_audit_bobby_armor_prices.py --json .tmp/bobby_armor_prices.json

`proposed` = InventoryItem.Cost for Bobby buy + world sell/buy (same contract as weapons).
Legion-style improvised/raider kit → shop=out_legion (CanAppearInShop=false), Cost still set.
Vanilla Flak/Kevlar stubs → out_stub. Quest/broken compositum → out_special.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INV = ROOT / "InventoryItem"
BOBBY_TIER_TOTAL = 5

# Early Legion flavor — not Bobby catalog (owner 2026-08-07).
OUT_LEGION = {
    "JazzArmor_TireArmor",
    "JazzArmor_TireBrigantine",
    "JazzArmor_Chainmail",
    "JazzArmor_ImprovisedCuirass",
    "JazzArmor_AssaultCuirass",
    "JazzArmor_SovietAssaultArmor",
    "JazzArmor_LeatherArmor",
    "JazzArmor_RaiderKneePads",
    "JazzArmor_RaiderMetalLeggins",
    "JazzArmor_MetalHelm",
    "JazzArmor_WieldingHelm",
    "JazzArmor_AdrianHelmet",
    "JazzArmor_Stahlhelm",
    "JazzArmorPlates_Scrap",  # самодельная плита — не Bobby (owner 2026-08-07)
}

OUT_SPECIAL = {
    "JazzArmor_SpectraCompositum",
    "JazzArmor_SpectraFullCompositum",
    "ShamanHelmet",
    "ShamanArmor",
    "ShamanLeggings",
    "PostApoHelmet",
    "Infected_HardenedSkin",
    "NailsLeatherVest",
    "IvanUshanka",
    "CrocodileHide",
    "Gasmaskenhelm",
    "Vest_test",
}

# Soft civ / utility still sold (early BR) or accessories.
SOFT_GEAR = {
    "JazzArmor_LeatherJacketBlk",
    "JazzArmor_LeatherJacketBrn",
    "JazzArmor_LeatherVest",
    "JazzArmor_LeatherPants",
    "JazzArmor_Uniform",
    "JazzArmor_UniformCap",
    "JazzArmor_UniformPants",
    "JazzArmor_ConstructionHelmet",
    "JazzArmor_MotoKneePads",
    "JazzArmor_ESS",
    "JazzArmor_Sunglasses",
    "JazzArmor_BallisticMask",
    "JazzArmor_CamoBalaclava",
}

DISPLAY_RE = re.compile(
    r'DisplayName\s*=\s*T\(\s*\d+\s*,\s*--\[\[[^\]]*\]\]\s*"((?:\\.|[^"\\])*)"',
    re.S,
)
COMMENT_RE = re.compile(r'comment\s*=\s*"([^"]*)"')
COST_RE = re.compile(r"(?<![A-Za-z])Cost\s*=\s*(\d+)")
TIER_RE = re.compile(r"(?<![A-Za-z])Tier\s*=\s*(\d+)")
RW_RE = re.compile(r"RestockWeight\s*=\s*(\d+)")
SHOP_RE = re.compile(r"CanAppearInShop\s*=\s*(true|false)")
OC_RE = re.compile(r'object_class\s*=\s*"([^"]+)"')
CAT_RE = re.compile(r'CategoryPair\s*=\s*"([^"]+)"')
CLASS_RE = re.compile(r"Class\s*(\d+)", re.I)
T_RE = re.compile(r"\bT(\d)\b")
BAND_RE = re.compile(r"\b(SH|L|M|H|N)\b")


def round_price(n: float) -> int:
    n = max(50, int(round(n)))
    if n < 1000:
        return int(round(n / 50.0) * 50)
    if n < 10000:
        return int(round(n / 100.0) * 100)
    if n < 50000:
        return int(round(n / 500.0) * 500)
    return int(round(n / 1000.0) * 1000)


def rarity_label(weight: int) -> str:
    if weight <= 8:
        return "очень редко"
    if weight <= 20:
        return "редко"
    if weight <= 45:
        return "нечасто"
    if weight <= 90:
        return "обычно"
    if weight <= 120:
        return "часто"
    return "очень часто"


def parse_file(path: Path) -> dict | None:
    wid = path.stem
    keep = (
        wid.startswith("JazzArmor")
        or wid.startswith("JazzArmorPlates")
        or wid in (
            "GasMask",
            "NightVisionGoggles",
            "JAZZ_ArmorUpgrade",
            "Combination_CeramicPlates",
            "Combination_Kompositum58",
        )
        or wid in OUT_SPECIAL
        or wid.startswith(("Flak", "Kevlar", "HeavyArmor", "LightHelmet", "CamoArmor"))
    )
    if not keep:
        return None
    t = path.read_text(encoding="utf-8", errors="replace")
    m_dn = DISPLAY_RE.search(t)
    name = m_dn.group(1).replace('\\"', '"') if m_dn else wid
    comment = (COMMENT_RE.search(t) or [None, ""])[1] or ""
    cost_m = COST_RE.search(t)
    tier_m = TIER_RE.search(t)
    rw_m = RW_RE.search(t)
    shop_m = SHOP_RE.search(t)
    oc = (OC_RE.search(t) or [None, "Armor"])[1]
    cat = (CAT_RE.search(t) or [None, ""])[1]

    cm = CLASS_RE.search(comment)
    pen_class = int(cm.group(1)) if cm else None
    tm = T_RE.search(comment)
    design_t = int(tm.group(1)) if tm else None
    # weight band letter after ClassN
    band = ""
    bm = re.search(r"Class\s*\d+\s*([A-Z]+)", comment, re.I)
    if bm:
        band = bm.group(1)
        if band not in ("L", "M", "H", "N", "SH"):
            band = band[:1] if band[:1] in ("L", "M", "H", "N") else ""

    return {
        "id": wid,
        "name": name,
        "comment": comment,
        "cost_now": int(cost_m.group(1)) if cost_m else 0,
        "tier_now": int(tier_m.group(1)) if tier_m else None,
        "rw_now": int(rw_m.group(1)) if rw_m else None,
        "shop_now": shop_m.group(1) if shop_m else "unset",
        "object_class": oc,
        "category": cat,
        "pen_class": pen_class,
        "design_t": design_t,
        "band": band,
    }


def slot_of(row: dict) -> str:
    wid = row["id"]
    oc = row.get("object_class") or ""
    if "Plates" in wid or oc == "ArmorPlates":
        return "plates"
    if wid in ("GasMask",) or "Mask" in wid or wid.endswith("Balaclava"):
        return "face"
    if "NVG" in wid or wid == "NightVisionGoggles":
        return "nvg"
    if wid == "JAZZ_ArmorUpgrade":
        return "upgrade"
    low = wid.lower()
    if any(x in low for x in ("helm", "helmet", "cap", "ushanka", "altyn", "stsh", "mich", "protec", "stahl", "adrian")):
        return "helm"
    if any(x in low for x in ("leg", "pad", "pants", "legging")):
        return "legs"
    if wid in SOFT_GEAR or "Leather" in wid or "Uniform" in wid or "Jacket" in wid:
        if "Pants" in wid or "Pad" in wid:
            return "legs"
        if "Cap" in wid or "Helmet" in wid:
            return "helm"
        return "soft"
    return "torso"


def shop_bucket(row: dict) -> tuple[str, str]:
    wid = row["id"]
    if wid in OUT_LEGION:
        return "out_legion", "вне Bobby: legion-style / импровиз"
    if wid in OUT_SPECIAL:
        return "out_special", "вне Bobby: спец/квест/битый def"
    if wid.startswith(("Flak", "Kevlar", "HeavyArmor", "LightHelmet", "CamoArmor")):
        return "out_stub", "вне Bobby: vanilla stub → JazzArmor remap"
    if wid in ("Combination_CeramicPlates", "Combination_Kompositum58"):
        return "out_special", "вне Bobby: craft/combination"
    return "bobby", ""


def proposed_bobby_tier(row: dict) -> int | None:
    if shop_bucket(row)[0] != "bobby":
        return None
    wid = row["id"]
    slot = slot_of(row)
    pen = row.get("pen_class") or 1
    design_t = row.get("design_t")

    overrides = {
        "JazzArmor_Spectra": 5,
        "JazzArmor_SpectraFull": 5,
        "JazzArmor_SpectraHelm": 5,
        "JazzArmor_SpectraLegs": 5,
        "JazzArmor_UHMWPE": 5,
        "JazzArmor_UHMWPEFull": 5,
        "JazzArmor_UHMWPEHelm": 5,
        "JazzArmor_UHMWPELegs": 5,
        "JazzArmor_IBA": 4,
        "JazzArmor_IBAFull": 4,
        "JazzArmor_IBALight": 4,
        "JazzArmor_AltynHelm": 4,
        "JazzArmor_Mich2000": 4,
        "JazzArmor_Mich2001": 4,
        "JazzArmor_EOD": 3,
        "JazzArmor_NVG1": 3,
        "JazzArmor_NVG2": 4,
        "JazzArmor_NVG3": 5,
        "JazzArmor_BallisticMask": 2,
        "NightVisionGoggles": 3,
        "GasMask": 2,
        "JAZZ_ArmorUpgrade": 2,
        "JazzArmorPlates_Twaron": 1,
        "JazzArmorPlates_Kevlar": 1,
        "JazzArmorPlates_Steel3": 2,
        "JazzArmorPlates_Ceramics3": 2,
        "JazzArmorPlates_Titan3": 2,
        "JazzArmorPlates_Steel4": 3,
        "JazzArmorPlates_Ceramics4": 3,
        "JazzArmorPlates_Titan4": 3,
        "JazzArmorPlates_Steel5": 4,
        "JazzArmorPlates_Ceramics5": 4,
        "JazzArmorPlates_Titan5": 4,
    }
    if wid in overrides:
        return overrides[wid]
    if wid in SOFT_GEAR:
        return 1

    # comment T* is design ladder hint (T2 early … T5 endgame)
    if design_t is not None:
        # map design T → BR: T1→1, T2→1-2, T3→2-3, T4→3-4, T5→5
        if design_t <= 1:
            return 1
        if design_t == 2:
            return 1 if pen <= 1 else 2
        if design_t == 3:
            return 2 if pen <= 2 else 3
        if design_t == 4:
            return 3 if pen <= 2 else 4
        return 5

    # plates / helms / legs by penetration class
    if slot == "plates":
        return min(5, max(1, pen))
    if pen <= 1:
        return 1
    if pen == 2:
        return 2
    if pen == 3:
        return 3
    if pen == 4:
        return 4
    return 5


# Family bands: BR tier → (lo, hi) game $ for torso baseline.
TORSO_BAND = {
    1: (700, 2200),
    2: (3000, 6500),
    3: (5500, 12000),
    4: (12000, 28000),
    5: (32000, 55000),
}
SLOT_MULT = {
    "torso": 1.0,
    "soft": 0.35,
    "helm": 0.55,
    "legs": 0.40,
    "plates": 0.45,
    "nvg": 0.90,
    "face": 0.25,
    "upgrade": 0.50,
}

PROPOSED_OVERRIDE: dict[str, tuple[int, str]] = {
    # Spectra — cut absurd 100k–250k; BR5 jackpot-friendly Cost
    "JazzArmor_Spectra": (42000, "Spectra mid BR5; срезали 100k"),
    "JazzArmor_SpectraFull": (52000, "Spectra heavy BR5; срезали 250k"),
    "JazzArmor_SpectraHelm": (28000, "Spectra helm BR5; срезали 100k"),
    "JazzArmor_SpectraLegs": (22000, "Spectra legs BR5; срезали 150k"),
    "JazzArmor_UHMWPE": (24000, "UHMWPE torso BR5; срезали 50k"),
    "JazzArmor_UHMWPEFull": (30000, "UHMWPE full BR5; срезали 75k"),
    "JazzArmor_UHMWPEHelm": (14000, "UHMWPE helm BR5; срезали 25k"),
    "JazzArmor_UHMWPELegs": (11000, "UHMWPE legs BR5; срезали 40k"),
    "JazzArmor_IBA": (16000, "IBA mid BR4"),
    "JazzArmor_IBAFull": (19000, "IBA full BR4"),
    "JazzArmor_IBALight": (13000, "IBA light BR4"),
    "JazzArmor_GuardianFull": (11000, "Guardian heavy BR3–4"),
    "JazzArmor_GuardianMedium": (9000, "Guardian mid"),
    "JazzArmor_GuardianLight": (7500, "Guardian light"),
    "JazzArmor_FlakM1955": (900, "early flak BR1"),
    "JazzArmor_FlakM69": (1400, "flak M69 BR1"),
    "JazzArmor_PoliceVest": (2800, "police BR2"),
    "JazzArmor_PASGT": (4200, "PASGT BR2"),
    "JazzArmor_SWAT": (4800, "SWAT BR2"),
    "JazzArmor_6B3": (5000, "6Б3 BR2"),
    "JazzArmor_6B13": (9500, "6Б13 BR3"),
    "JazzArmor_AltynHelm": (12000, "Алтын rare heavy helm BR4"),
    "JazzArmor_Mich2000": (8500, "MICH 2000 BR4"),
    "JazzArmor_Mich2001": (10000, "MICH 2001 BR4"),
    "JazzArmor_NVG1": (4500, "NVG gen1 BR3"),
    "JazzArmor_NVG2": (12000, "NVG gen2 BR4"),
    "JazzArmor_NVG3": (28000, "NVG gen3 BR5; late jackpot-ish"),
    "NightVisionGoggles": (4000, "vanilla NVG → рядом NVG1; BR3"),
    "GasMask": (1800, "gas mask BR2"),
    "JAZZ_ArmorUpgrade": (4500, "plate/upgrade kit BR2"),
    "JazzArmor_EOD": (8500, "EOD heavy; DisplayName buggy — Cost ок"),
    "JazzArmor_LeatherJacketBlk": (400, "civ soft BR1"),
    "JazzArmor_LeatherJacketBrn": (400, "civ soft BR1"),
    "JazzArmor_LeatherVest": (250, "civ soft BR1"),
    "JazzArmor_LeatherPants": (350, "civ soft BR1"),
    "JazzArmor_Uniform": (500, "uniform BR1"),
    "JazzArmor_UniformCap": (200, "cap BR1"),
    "JazzArmor_UniformPants": (400, "pants BR1"),
    "JazzArmor_ConstructionHelmet": (150, "scrap helm BR1"),
    "JazzArmor_MotoKneePads": (200, "moto pads BR1"),
    "JazzArmor_BallisticMask": (3500, "ballistic face mask BR2; срезали 10k"),
    "JazzArmor_ESS": (1200, "ballistic glasses BR1"),
    "JazzArmor_M1Helm": (1200, "M1 helmet BR2; Cost был unset"),
    # legion-style world Cost (loot/sell), not Bobby
    "JazzArmor_TireArmor": (800, "legion scrap Cost (мир)"),
    "JazzArmor_TireBrigantine": (900, "legion scrap Cost (мир)"),
    "JazzArmor_Chainmail": (1000, "legion scrap Cost (мир)"),
    "JazzArmor_ImprovisedCuirass": (1100, "legion scrap Cost (мир)"),
    "JazzArmor_AssaultCuirass": (1400, "legion scrap Cost (мир)"),
    "JazzArmor_SovietAssaultArmor": (1600, "legion scrap Cost (мир)"),
    "JazzArmor_LeatherArmor": (1200, "legion/merc leather Cost (мир)"),
    "JazzArmor_RaiderKneePads": (300, "legion scrap Cost (мир)"),
    "JazzArmor_RaiderMetalLeggins": (600, "legion scrap Cost (мир)"),
    "JazzArmor_MetalHelm": (400, "legion scrap Cost (мир)"),
    "JazzArmor_WieldingHelm": (500, "legion scrap Cost (мир)"),
    "JazzArmor_AdrianHelmet": (350, "antique helm Cost (мир)"),
    "JazzArmor_Stahlhelm": (450, "antique helm Cost (мир)"),
    "JazzArmorPlates_Scrap": (800, "самодельная плита Cost (мир); вне Bobby"),
    "JazzArmorPlates_Twaron": (1600, "twaron plate BR1"),
    "JazzArmorPlates_Kevlar": (2800, "kevlar plate BR1"),
    "JazzArmorPlates_Steel3": (2800, "steel3 plate BR2"),
    "JazzArmorPlates_Ceramics3": (3200, "ceram3 plate BR2"),
    "JazzArmorPlates_Titan3": (5500, "titan3 rare BR2"),
    "JazzArmorPlates_Steel4": (4800, "steel4 plate BR3"),
    "JazzArmorPlates_Ceramics4": (5500, "ceram4 plate BR3"),
    "JazzArmorPlates_Titan4": (11000, "titan4 rare BR3"),
    "JazzArmorPlates_Steel5": (8000, "steel5 plate BR4"),
    "JazzArmorPlates_Ceramics5": (9000, "ceram5 plate BR4"),
    "JazzArmorPlates_Titan5": (16000, "titan5 rare BR4"),
}


def propose_cost(row: dict, br: int | None) -> tuple[int, str]:
    wid = row["id"]
    if wid in PROPOSED_OVERRIDE:
        p, why = PROPOSED_OVERRIDE[wid]
        return p, why
    slot = slot_of(row)
    tier = br or 2
    lo, hi = TORSO_BAND.get(tier, TORSO_BAND[2])
    mid = (lo + hi) / 2
    # band within slot: L cheaper, H/SH pricier
    band = row.get("band") or "M"
    band_f = {"L": 0.85, "N": 0.9, "M": 1.0, "H": 1.15, "SH": 1.35}.get(band, 1.0)
    mult = SLOT_MULT.get(slot, 1.0)
    proposed = round_price(mid * mult * band_f)
    # pull toward current if within 25%
    now = row["cost_now"]
    bits = [f"band BR{tier} torso {lo}–{hi} ×slot {mult} ×{band}→{proposed}"]
    if now and abs(proposed - now) < max(400, now * 0.2):
        proposed = now
        bits.append("keep near now")
    elif now and abs(proposed - now) >= max(1000, now * 0.35):
        bits.append(f"vs now {now}")
    return proposed, "; ".join(bits)


def propose_rw(row: dict, br: int | None, proposed: int) -> int | None:
    shop, _ = shop_bucket(row)
    if shop != "bobby":
        return None
    wid = row["id"]
    overrides = {
        "JazzArmor_Spectra": 6,
        "JazzArmor_SpectraFull": 5,
        "JazzArmor_SpectraHelm": 5,
        "JazzArmor_SpectraLegs": 5,
        "JazzArmor_UHMWPE": 10,
        "JazzArmor_UHMWPEFull": 8,
        "JazzArmor_AltynHelm": 8,
        "JazzArmor_NVG1": 40,
        "JazzArmor_NVG2": 18,
        "JazzArmor_NVG3": 8,
        "NightVisionGoggles": 35,
        "JazzArmorPlates_Titan5": 10,
        "JazzArmorPlates_Titan4": 14,
        "JazzArmorPlates_Titan3": 22,
        "JazzArmor_GuardianLegs": 25,  # was RW=0 bug
        "JazzArmor_UHMWPEHelm": 10,  # was RW=0
        "JazzArmor_UHMWPELegs": 12,    }
    if wid in overrides:
        return overrides[wid]
    base = {1: 100, 2: 80, 3: 55, 4: 35, 5: 18}.get(br or 3, 55)
    if proposed >= 40000:
        base = min(base, 12)
    elif proposed >= 20000:
        base = min(base, 22)
    elif proposed >= 10000:
        base = min(base, 40)
    slot = slot_of(row)
    if slot == "soft":
        base = min(120, base + 20)
    if slot == "plates" and (br or 3) >= 4:
        base = max(6, base - 10)
    if slot == "nvg":
        base = max(8, base - 15)
    return int(base)


def load_rows() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(INV.glob("*.lua")):
        parsed = parse_file(path)
        if not parsed:
            continue
        # skip empty stubs without jazz armor name that aren't in lists
        wid = parsed["id"]
        shop, shop_why = shop_bucket(parsed)
        # Only keep jazz armor family + listed extras + stubs we mark out
        if not (
            wid.startswith("JazzArmor")
            or wid.startswith("JazzArmorPlates")
            or wid in ("GasMask", "NightVisionGoggles", "JAZZ_ArmorUpgrade")
            or shop in ("out_stub", "out_special", "out_legion")
        ):
            continue
        if shop == "out_stub" and not wid.startswith(("Flak", "Kevlar", "HeavyArmor", "LightHelmet", "CamoArmor")):
            continue

        br = proposed_bobby_tier(parsed)
        proposed, why = propose_cost(parsed, br)
        rw = propose_rw(parsed, br, proposed)
        slot = slot_of(parsed)
        row = {
            **parsed,
            "slot": slot,
            "shop": shop,
            "br_tier": br,
            "proposed": proposed,
            "delta": proposed - parsed["cost_now"],
            "rw": rw,
            "rarity": rarity_label(rw) if rw is not None else "—",
            "why": (
                f"{shop_why}. Cost (мир): {why}"
                if shop != "bobby"
                else f"{why}; BR{br}/{BOBBY_TIER_TOTAL}; {rarity_label(rw)} RW{rw}"
                + (
                    f" (now Tier={parsed['tier_now']})"
                    if parsed["tier_now"] is not None and br is not None and parsed["tier_now"] != br
                    else ""
                )
                + (
                    f" (RW now {parsed['rw_now']})"
                    if parsed["rw_now"] is not None and rw is not None and parsed["rw_now"] != rw
                    else (" (RW unset)" if parsed["rw_now"] is None and rw is not None else "")
                )
            ),
        }
        rows.append(row)

    rows.sort(
        key=lambda r: (
            0 if r["shop"] == "bobby" else 1,
            r.get("br_tier") or 99,
            {"torso": 0, "soft": 1, "helm": 2, "legs": 3, "plates": 4, "nvg": 5, "face": 6, "upgrade": 7}.get(
                r["slot"], 9
            ),
            r["id"],
        )
    )
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=Path)
    ap.add_argument("--tsv", type=Path)
    args = ap.parse_args()
    rows = load_rows()
    bobby = [r for r in rows if r["shop"] == "bobby"]
    from collections import Counter

    print(f"armor rows: {len(rows)}")
    print(f"  bobby: {len(bobby)}")
    for k, v in sorted(Counter(r["shop"] for r in rows).items()):
        print(f"  {k}: {v}")
    brc = Counter(r.get("br_tier") for r in bobby)
    print(f"  BR dist={dict(sorted((k, v) for k, v in brc.items() if k))}")
    huge = [r for r in bobby if abs(r["delta"]) >= 20000]
    print(f"  |delta|>=20k bobby: {len(huge)}")
    for r in huge[:12]:
        print(f"    {r['id']:32} now={r['cost_now']:7} -> {r['proposed']:7}")

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        payload = [
            {
                "slot": r["slot"],
                "family": r["slot"],
                "tier": r.get("comment") or "—",
                "id": r["id"],
                "name": r["name"],
                "now": r["cost_now"],
                "proposed": r["proposed"],
                "delta": r["delta"],
                "shop": r["shop"],
                "why": r["why"],
                "br_tier": r.get("br_tier"),
                "br_tier_now": r.get("tier_now"),
                "br_tier_total": BOBBY_TIER_TOTAL,
                "rw": r.get("rw"),
                "rw_now": r.get("rw_now"),
                "rarity": r.get("rarity"),
                "pen_class": r.get("pen_class"),
                "cas_action": (
                    "SET_FALSE"
                    if r["shop"] in ("out_legion", "out_special", "out_stub")
                    and r.get("shop_now") != "false"
                    else "KEEP"
                ),
            }
            for r in rows
            if r["shop"] != "out_stub"  # stubs noisy; still in tsv
        ]
        # include stubs in json lightly? skip for canvas clarity
        args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print("wrote", args.json, "canvas-rows", len(payload))

    if args.tsv:
        args.tsv.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "slot\tshop\tid\tname\tnow\tproposed\tdelta\tbr_tier\tbr_now\trarity\trw\trw_now\tpen\tcomment\twhy"
        ]
        for r in rows:
            lines.append(
                "\t".join(
                    map(
                        str,
                        [
                            r["slot"],
                            r["shop"],
                            r["id"],
                            r["name"].replace("\t", " "),
                            r["cost_now"],
                            r["proposed"],
                            r["delta"],
                            r.get("br_tier") if r.get("br_tier") is not None else "",
                            r.get("tier_now") if r.get("tier_now") is not None else "",
                            r.get("rarity") or "",
                            r.get("rw") if r.get("rw") is not None else "",
                            r.get("rw_now") if r.get("rw_now") is not None else "",
                            r.get("pen_class") if r.get("pen_class") is not None else "",
                            (r.get("comment") or "").replace("\t", " "),
                            r["why"].replace("\t", " "),
                        ],
                    )
                )
            )
        args.tsv.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("wrote", args.tsv)


if __name__ == "__main__":
    main()
