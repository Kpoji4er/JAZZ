# -*- coding: utf-8 -*-
"""Audit ammo InventoryItem.Cost / Bobby Tier for ECON-004.

Usage:
  python docs/tools/_audit_bobby_ammo_prices.py
  python docs/tools/_audit_bobby_ammo_prices.py --json .tmp/bobby_ammo_prices.json

`proposed` = stack Cost (ShopStackSize pack) for Bobby + world sell/buy.
Crafted / mortar / dupe / antique-only calibers → out_*; Cost still set.

Runtime restock (ECON-004, not encoded in companion RW alone):
  ammo T < U → weight × 2^(U−T) (cap 8); Poor fades out by U (0 at U≥4).
  Authored RW/MaxStock = base at T==U; below-U boost is code-side.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INV = ROOT / "InventoryItem"
BOBBY_TIER_TOTAL = 5

# Antique calibers whose guns are out of Bobby (~2005 / WW2).
OUT_OLD_CALIBERS = {
    "JAZZ_Caliber_792",
    "JAZZ_Caliber_792x33",
    "JAZZ_Caliber_75French",
}

DISPLAY_RE = re.compile(
    r'DisplayName\s*=\s*T\(\s*\d+\s*,\s*--\[\[[^\]]*\]\]\s*"((?:\\.|[^"\\])*)"',
    re.S,
)
COST_RE = re.compile(r"(?<![A-Za-z])Cost\s*=\s*(\d+)")
TIER_RE = re.compile(r'(?<![A-Za-z])Tier\s*=\s*(?:"?(\d+)"?)')
RW_RE = re.compile(r"RestockWeight\s*=\s*(\d+)")
SHOP_RE = re.compile(r"CanAppearInShop\s*=\s*(true|false)")
SSS_RE = re.compile(r"ShopStackSize\s*=\s*(\d+)")
CAL_RE = re.compile(r'Caliber\s*=\s*"([^"]+)"')
OC_RE = re.compile(r'object_class\s*=\s*"([^"]+)"')
CAT_RE = re.compile(r'CategoryPair\s*=\s*"([^"]+)"')

# Grade → base BR (before caliber bumps).
GRADE_BR = {
    "Poor": 1,
    "Saltshot": 1,
    "Birdshot": 1,
    "US": 1,
    "FMJ": 2,
    "JHP": 2,
    "P": 2,
    "Buckshot": 2,
    "Basic": 3,  # 50BMG basic
    "Army": 3,
    "Tracer": 3,
    "Slug": 3,
    "Subsonic": 3,
    "Match": 4,
    "EPR": 4,
    "APP": 4,
    "APSlug": 4,
    "API_HEI": 4,
    "AP": 5,
    "APIT": 5,
    "Frag": 2,
    "Flashbang": 2,
    "Crafted": None,  # out
}

# Soft per-round game-$ targets by grade (before caliber mult).
GRADE_PER_RD = {
    "Poor": 4,
    "Saltshot": 3,
    "Birdshot": 5,
    "US": 6,
    "FMJ": 10,
    "JHP": 12,
    "P": 11,
    "Buckshot": 14,
    "Basic": 400,  # .50 BMG
    "Army": 18,
    "Tracer": 16,
    "Slug": 20,
    "Subsonic": 22,
    "Match": 35,
    "EPR": 28,
    "APP": 40,
    "APSlug": 45,
    "API_HEI": 900,
    "AP": 42,
    "APIT": 55,  # rifle APIT; 50BMG overridden
    "Frag": 80,
    "Flashbang": 70,
    "Crafted": 2,
}

# Caliber relative cost / BR bump.
CAL_MULT = {
    "JAZZ_Caliber_9x18": 0.85,
    "JAZZ_Caliber_9x19": 1.0,
    "JAZZ_Caliber_45ACP": 1.05,
    "JAZZ_Caliber_38special": 0.9,
    "JAZZ_Caliber_44CAL": 1.15,
    "JAZZ_Caliber_762x25": 0.9,
    "JAZZ_Caliber_556": 1.0,
    "JAZZ_Caliber_545": 0.95,
    "JAZZ_Caliber_762x39": 0.95,
    "JAZZ_Caliber_762x51": 1.25,
    "JAZZ_Caliber_762x54": 1.2,
    "JAZZ_Caliber_3006": 1.15,
    "JAZZ_Caliber_30": 0.9,
    "JAZZ_Caliber_12gauge": 1.1,
    "JAZZ_Caliber_9x39": 1.35,
    "JAZZ_Caliber_46": 1.4,
    "JAZZ_Caliber_57": 1.45,
    "JAZZ_Caliber_50AE": 1.5,
    "JAZZ_Caliber_50BMG": 1.0,  # already in grade
    "JAZZ_Caliber_40mmGrenade": 1.0,
    "JAZZ_Caliber_Warhead": 1.0,
}

CAL_BR_BUMP = {
    "JAZZ_Caliber_9x39": 1,
    "JAZZ_Caliber_46": 1,
    "JAZZ_Caliber_57": 1,
    # 50AE: no bump — pistol family stays early (owner)
}

# Handgun / revolver: BR1–3 when Bobby has matching guns there; else match gun BR.
PISTOL_CALIBERS = {
    "JAZZ_Caliber_9x19",
    "JAZZ_Caliber_9x18",
    "JAZZ_Caliber_45ACP",
    "JAZZ_Caliber_38",
    "JAZZ_Caliber_357",
    "JAZZ_Caliber_44CAL",
    "JAZZ_Caliber_762x25",
    "JAZZ_Caliber_50AE",
    "JAZZ_Caliber_57",
}

# Caliber → Bobby handgun BR tiers (weapon price audit).
PISTOL_GUN_BR: dict[str, list[int]] = {
    "JAZZ_Caliber_762x25": [1],
    "JAZZ_Caliber_38": [1],
    "JAZZ_Caliber_9x18": [1, 3],
    "JAZZ_Caliber_9x19": [1, 2, 3, 4, 5],
    "JAZZ_Caliber_45ACP": [1, 2, 3, 4],
    "JAZZ_Caliber_357": [1, 3, 4],
    "JAZZ_Caliber_44CAL": [3, 4],
    "JAZZ_Caliber_50AE": [4],
    "JAZZ_Caliber_57": [5],
}

# Grade → index into T1–T3 span for that caliber.
PISTOL_GRADE_BAND = {
    "Poor": 0,
    "FMJ": 0,
    "P": 0,
    "JHP": 1,
    "Match": 2,
    "APP": 2,
    "AP": 2,
}


def round_price(n: float) -> int:
    n = max(20, int(round(n)))
    if n < 200:
        return int(round(n / 10.0) * 10)
    if n < 2000:
        return int(round(n / 50.0) * 50)
    if n < 20000:
        return int(round(n / 100.0) * 100)
    return int(round(n / 500.0) * 500)


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


def parse_id_parts(wid: str) -> tuple[str, str]:
    """Return (caliber_key, grade) from JAZZ_AMMO_<cal>_<grade>."""
    if not wid.startswith("JAZZ_AMMO_"):
        return "", ""
    rest = wid[len("JAZZ_AMMO_") :]
    # Ordnance names
    if rest.startswith("40mm"):
        if "Flashbang" in rest:
            return "40mm", "Flashbang"
        if "Frag" in rest:
            return "40mm", "Frag"
        return "40mm", rest
    if rest.startswith("MortarShell_"):
        return "mortar", rest.split("_", 1)[-1]
    # Known multi-part grades first
    for grade in (
        "API_HEI",
        "APSlug",
        "Saltshot",
        "Birdshot",
        "Buckshot",
        "Subsonic",
        "Flashbang",
        "Crafted",
        "Tracer",
        "Match",
        "Army",
        "Basic",
        "Poor",
        "APIT",
        "APP",
        "EPR",
        "JHP",
        "FMJ",
        "Slug",
        "AP",
        "US",
        "P",
    ):
        suf = "_" + grade
        if rest.endswith(suf):
            return rest[: -len(suf)], grade
    if "_" in rest:
        a, b = rest.rsplit("_", 1)
        return a, b
    return rest, ""


def parse_file(path: Path) -> dict | None:
    wid = path.stem
    if wid.endswith(".bak") or not (
        wid.startswith("JAZZ_AMMO_") or wid == "FlareAmmo"
    ):
        return None
    t = path.read_text(encoding="utf-8", errors="replace")
    m_dn = DISPLAY_RE.search(t)
    name = m_dn.group(1).replace('\\"', '"') if m_dn else wid
    cost_m = COST_RE.search(t)
    tier_m = TIER_RE.search(t)
    rw_m = RW_RE.search(t)
    shop_m = SHOP_RE.search(t)
    sss_m = SSS_RE.search(t)
    cal = (CAL_RE.search(t) or [None, ""])[1]
    oc = (OC_RE.search(t) or [None, "Ammo"])[1]
    cat = (CAT_RE.search(t) or [None, ""])[1]
    cal_key, grade = parse_id_parts(wid)
    if wid == "FlareAmmo":
        cal_key, grade = "flare", "FMJ"
    return {
        "id": wid,
        "name": name,
        "cost_now": int(cost_m.group(1)) if cost_m else 0,
        "tier_now": int(tier_m.group(1)) if tier_m else None,
        "rw_now": int(rw_m.group(1)) if rw_m else None,
        "shop_now": shop_m.group(1) if shop_m else "unset",
        "sss": int(sss_m.group(1)) if sss_m else 30,
        "caliber": cal,
        "cal_key": cal_key,
        "grade": grade,
        "object_class": oc,
        "category": cat,
    }


def shop_bucket(row: dict) -> tuple[str, str]:
    wid = row["id"]
    if wid.endswith("_copy") or wid == "JAZZ_AMMO_9x19_JHP_copy":
        return "out_dupe", "вне Bobby: дубликат"
    if row["grade"] == "Crafted" or wid.endswith("_Crafted"):
        return "out_craft", "вне Bobby: крафт игрока"
    if row["cal_key"] == "mortar" or "MortarShell" in wid:
        return "out_mortar", "вне Bobby: миномётные снаряды"
    if row.get("caliber") in OUT_OLD_CALIBERS:
        return "out_old", "вне Bobby: antique caliber (оружие out_old)"
    return "bobby", ""


def pistol_br_for(row: dict) -> int | None:
    """Handgun ammo: T1–T3 if Bobby has that caliber there; else match gun BR."""
    cal = row.get("caliber") or ""
    if cal not in PISTOL_CALIBERS:
        return None
    guns = PISTOL_GUN_BR.get(cal) or []
    in_13 = [b for b in guns if 1 <= b <= 3]
    grade = row.get("grade") or "FMJ"
    if in_13:
        # Spread grades across available T1–T3 slots for this caliber.
        band = PISTOL_GRADE_BAND.get(grade, 1)
        # Pick from sorted unique in_13 by band index (clamp).
        slots = sorted(set(in_13))
        # Ensure at least early/mid/late within 1..3 even if only one gun tier:
        # expand to fill 1..max(in_13) capped at 3.
        hi = min(3, max(slots))
        lo = min(slots)
        span = [t for t in range(lo, hi + 1)]
        if not span:
            span = slots
        idx = min(band, len(span) - 1)
        return span[idx]
    # No T1–T3 gun — equalize with earliest Bobby gun of this caliber.
    if guns:
        return min(guns)
    return 2


def proposed_bobby_tier(row: dict) -> int | None:
    if shop_bucket(row)[0] != "bobby":
        return None
    wid = row["id"]
    overrides = {
        "FlareAmmo": 1,
        "JAZZ_AMMO_50BMG_Basic": 3,
        "JAZZ_AMMO_50BMG_API_HEI": 4,
        "JAZZ_AMMO_50BMG_APIT": 5,
        "JAZZ_AMMO_9x39_JHP": 3,
        "JAZZ_AMMO_9x39_AP": 5,
        "JAZZ_AMMO_12gauge_APSlug": 4,
        "JAZZ_AMMO_762x39_APP": 5,
        "JAZZ_AMMO_40mmFragGrenade": 2,
        "JAZZ_AMMO_40mmFlashbangGrenade": 2,
    }
    if wid in overrides:
        return overrides[wid]

    pistol = pistol_br_for(row)
    if pistol is not None:
        return pistol

    grade = row["grade"]
    base = GRADE_BR.get(grade)
    if base is None:
        return 2
    bump = CAL_BR_BUMP.get(row.get("caliber") or "", 0)
    return min(5, max(1, base + bump))

PROPOSED_OVERRIDE: dict[str, tuple[int, str]] = {
    "JAZZ_AMMO_50BMG_APIT": (22000, "APIT .50 pack; срезали 72k; BR5 RW1"),
    "JAZZ_AMMO_50BMG_API_HEI": (9000, "API-HEI .50; срезали 13.5k"),
    "JAZZ_AMMO_50BMG_Basic": (4500, "Basic .50 pack BR3"),
    "JAZZ_AMMO_762x39_APP": (2200, "APP 7.62×39 BR5; был 400"),
    "JAZZ_AMMO_12gauge_APSlug": (1800, "AP slug BR4; был 3000@T2"),
    "JAZZ_AMMO_556_FMJ": (1200, "keep FMJ 5.56 pack"),
    "JAZZ_AMMO_9x19_FMJ": (500, "FMJ 9×19 pack"),
    "JAZZ_AMMO_40mmFragGrenade": (2400, "40mm frag pack BR2"),
    "JAZZ_AMMO_40mmFlashbangGrenade": (1800, "40mm flash BR2"),
    "JAZZ_AMMO_762x54_APIT": (2800, "APIT 7.62x54 pack BR5; formula was BMG-scaled"),
    "JAZZ_AMMO_545_AP": (4500, "AP 5.45 pack BR5; between now 2700 and band"),
    "JAZZ_AMMO_556_AP": (4800, "AP 5.56 pack BR5"),
    "JAZZ_AMMO_762x51_AP": (3200, "AP 7.62x51 pack BR5 @SSS20"),
    "JAZZ_AMMO_762x51_Match": (2800, "Match 7.62x51; срезали 6k"),
    "JAZZ_AMMO_762x54_Match": (2400, "Match 7.62x54; срезали 4.5k"),
    "JAZZ_AMMO_556_Match": (2800, "Match 5.56 pack"),
    "FlareAmmo": (150, "flare BR1"),
}


def propose_cost(row: dict, br: int | None) -> tuple[int, str]:
    wid = row["id"]
    if wid in PROPOSED_OVERRIDE:
        return PROPOSED_OVERRIDE[wid]
    grade = row["grade"] or "FMJ"
    sss = max(1, row["sss"])
    per = GRADE_PER_RD.get(grade, 12)
    mult = CAL_MULT.get(row.get("caliber") or "", 1.0)
    # BR soft pull
    br_f = {1: 0.85, 2: 1.0, 3: 1.1, 4: 1.25, 5: 1.4}.get(br or 2, 1.0)
    proposed = round_price(per * mult * sss * br_f)
    now = row["cost_now"]
    bits = [f"grade {grade} ${per}/rd ×{sss} ×cal {mult:.2f} ×BR{br_f}→{proposed}"]
    if now and abs(proposed - now) < max(80, now * 0.2):
        proposed = now
        bits.append("keep near now")
    elif now and abs(proposed - now) >= max(200, now * 0.4):
        bits.append(f"vs now {now}")
    return proposed, "; ".join(bits)


def propose_rw(row: dict, br: int | None, proposed: int) -> int | None:
    if shop_bucket(row)[0] != "bobby":
        return None
    wid = row["id"]
    overrides = {
        "JAZZ_AMMO_50BMG_APIT": 1,
        "JAZZ_AMMO_50BMG_API_HEI": 3,
        "JAZZ_AMMO_50BMG_Basic": 12,
        "JAZZ_AMMO_46_JHP": 15,  # was 1005 typo
        "JAZZ_AMMO_556_AP": 8,
        "JAZZ_AMMO_545_AP": 8,
        "JAZZ_AMMO_762x51_AP": 8,
        "JAZZ_AMMO_762x51_Match": 6,
        "JAZZ_AMMO_9x39_AP": 8,
        "FlareAmmo": 40,
    }
    if wid in overrides:
        return overrides[wid]
    grade = row["grade"]
    base = {
        "Poor": 90,  # high early; runtime fade when U rises
        "Saltshot": 80,
        "Birdshot": 90,
        "US": 100,
        "FMJ": 100,  # bulk resupply when T < U (runtime ×2^Δ)
        "JHP": 75,
        "P": 80,
        "Buckshot": 85,
        "Basic": 20,
        "Army": 50,
        "Tracer": 45,
        "Slug": 40,
        "Subsonic": 30,
        "Match": 18,
        "EPR": 22,
        "APP": 16,
        "APSlug": 14,
        "API_HEI": 5,
        "AP": 10,
        "APIT": 4,
        "Frag": 35,
        "Flashbang": 30,
    }.get(grade, 50)
    if (br or 3) >= 5:
        base = min(base, 12)
    elif (br or 3) >= 4:
        base = min(base, 25)
    if proposed >= 15000:
        base = min(base, 8)
    return int(base)


def propose_maxstock(row: dict, br: int | None) -> int | None:
    """Authored MaxStock at match tier; runtime may boost when T < U."""
    if shop_bucket(row)[0] != "bobby":
        return None
    grade = row.get("grade") or ""
    if grade == "Poor":
        return 3  # early only; fade removes later
    if grade in ("FMJ", "US", "Buckshot", "Birdshot", "P"):
        return 8
    if grade in ("JHP", "Army", "Tracer", "Slug"):
        return 5
    if grade in ("Match", "EPR", "APP", "APSlug"):
        return 3
    if grade in ("AP", "APIT", "API_HEI", "Basic"):
        return 2
    return 5


def load_rows() -> list[dict]:
    rows: list[dict] = []
    paths = list(INV.glob("JAZZ_AMMO_*.lua")) + list(INV.glob("FlareAmmo.lua"))
    for path in sorted(paths):
        if path.name.endswith(".bak"):
            continue
        parsed = parse_file(path)
        if not parsed:
            continue
        shop, shop_why = shop_bucket(parsed)
        br = proposed_bobby_tier(parsed)
        proposed, why = propose_cost(parsed, br)
        rw = propose_rw(parsed, br, proposed)
        maxstock = propose_maxstock(parsed, br)
        per_now = (parsed["cost_now"] / parsed["sss"]) if parsed["sss"] else 0
        per_prop = (proposed / parsed["sss"]) if parsed["sss"] else 0
        fade_note = ""
        if shop == "bobby" and parsed.get("grade") == "Poor":
            fade_note = "; Poor fade U2×0.35 U3×0.08 U4+=0"
        elif shop == "bobby":
            fade_note = "; ammo T<U → RW×2^(U-T) cap8 (+MaxStock boost)"
        row = {
            **parsed,
            "shop": shop,
            "br_tier": br,
            "proposed": proposed,
            "delta": proposed - parsed["cost_now"],
            "rw": rw,
            "maxstock": maxstock,
            "rarity": rarity_label(rw) if rw is not None else "—",
            "per_now": round(per_now, 1),
            "per_prop": round(per_prop, 1),
            "family": parsed["cal_key"] or parsed.get("category") or "misc",
            "why": (
                f"{shop_why}. Cost (мир): {why}"
                if shop != "bobby"
                else f"{why}; BR{br}/{BOBBY_TIER_TOTAL}; {rarity_label(rw)} RW{rw} MaxStock{maxstock}{fade_note}"
                + (
                    f" (now Tier={parsed['tier_now']})"
                    if parsed["tier_now"] is not None and br is not None and parsed["tier_now"] != br
                    else (" (Tier unset)" if parsed["tier_now"] is None and br is not None else "")
                )
                + (
                    f" (RW now {parsed['rw_now']})"
                    if parsed["rw_now"] is not None and rw is not None and parsed["rw_now"] != rw
                    else (" (RW unset)" if parsed["rw_now"] is None and rw is not None else "")
                )
            ),
            "cas_action": (
                "SET_FALSE"
                if shop != "bobby" and parsed.get("shop_now") != "false"
                else "KEEP"
            ),
        }
        rows.append(row)

    rows.sort(
        key=lambda r: (
            0 if r["shop"] == "bobby" else 1,
            r.get("br_tier") or 99,
            r.get("family") or "",
            {"Poor": 0, "FMJ": 1, "JHP": 2, "Army": 3, "Tracer": 4, "Match": 5, "EPR": 6, "AP": 7}.get(
                r.get("grade") or "", 9
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

    print(f"ammo rows: {len(rows)}")
    print(f"  bobby: {len(bobby)}")
    for k, v in sorted(Counter(r["shop"] for r in rows).items()):
        print(f"  {k}: {v}")
    brc = Counter(r.get("br_tier") for r in bobby)
    print(f"  BR dist={dict(sorted((k, v) for k, v in brc.items() if k))}")
    huge = [r for r in bobby if abs(r["delta"]) >= 5000]
    print(f"  |delta|>=5k bobby: {len(huge)}")
    for r in huge[:12]:
        print(f"    {r['id']:36} now={r['cost_now']:7} -> {r['proposed']:7} /rd {r['per_prop']}")

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        payload = [
            {
                "family": r["family"],
                "grade": r["grade"],
                "tier": f"{r['family']}/{r['grade']}" if r["grade"] else r["family"],
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
                "maxstock": r.get("maxstock"),
                "rarity": r.get("rarity"),
                "sss": r["sss"],
                "per_now": r["per_now"],
                "per_prop": r["per_prop"],
                "cas_action": r["cas_action"],
            }
            for r in rows
        ]
        args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print("wrote", args.json)

    if args.tsv:
        args.tsv.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "family\tgrade\tid\tname\tnow\tproposed\tdelta\tper_now\tper_prop\tsss\tbr_tier\tbr_now\trarity\trw\trw_now\tshop\twhy"
        ]
        for r in rows:
            lines.append(
                "\t".join(
                    map(
                        str,
                        [
                            r["family"],
                            r["grade"],
                            r["id"],
                            r["name"].replace("\t", " "),
                            r["cost_now"],
                            r["proposed"],
                            r["delta"],
                            r["per_now"],
                            r["per_prop"],
                            r["sss"],
                            r.get("br_tier") if r.get("br_tier") is not None else "",
                            r.get("tier_now") if r.get("tier_now") is not None else "",
                            r.get("rarity") or "",
                            r.get("rw") if r.get("rw") is not None else "",
                            r.get("rw_now") if r.get("rw_now") is not None else "",
                            r["shop"],
                            r["why"].replace("\t", " "),
                        ],
                    )
                )
            )
        args.tsv.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("wrote", args.tsv)


if __name__ == "__main__":
    main()
