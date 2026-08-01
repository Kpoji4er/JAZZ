# -*- coding: utf-8 -*-
"""Union magazine AvailableComponents within each mag family.

After _split_mag_families: family-suffixed ids are shared inside a family.
AK is further split by caliber (7.62 vs 5.45) — do NOT union 40↔45.
"""
from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

from _split_mag_families import FAMILY_MEMBERS, WEAPON_TO_FAMILY

ROOT = Path(__file__).resolve().parents[2]
INV = ROOT / "InventoryItem"

FAM_SUFFIXES = set(FAMILY_MEMBERS) | {"AK"}

# Caliber wells inside AK family (mag well ≈ same platform shape, different cartridge).
AK762 = frozenset({"AK47", "AKM", "Type56", "RPK", "Zastava_M70", "ZastavaM92"})
AK545 = frozenset({"AK74", "AKSU", "RPK74", "AN94"})

AK762_MAGS = frozenset({
    "JAZZ_MagLarge_30_40",
    "JAZZ_MagDrum_30_75",
    "JAZZ_MagQuick_AK",
})
AK545_MAGS = frozenset({
    "JAZZ_MagLarge_30_45",
    "JAZZ_MagQuick_AK",
})

# Non-AK legacy shared (none currently beyond caliber sets).
LEGACY_FAMILY_SHARED: dict[str, set[str]] = {}


def extract_mag_options(text: str) -> tuple[int, int, list[str]] | None:
    m = re.search(
        r"'SlotType',\s*\"Magazine\",.*?AvailableComponents',\s*\{(.*?)\}",
        text,
        flags=re.S,
    )
    if not m:
        return None
    opts = re.findall(r"\"([^\"]+)\"", m.group(1))
    return m.start(1), m.end(1), opts


def replace_mag_options(text: str, ordered: list[str]) -> str | None:
    m = re.search(
        r"('SlotType',\s*\"Magazine\",.*?AvailableComponents',\s*\{)(.*?)(\})",
        text,
        flags=re.S,
    )
    if not m:
        return None
    body = "\n" + "\n".join(f'\t\t\t\t"{o}",' for o in ordered) + "\n\t\t\t"
    return text[: m.start(2)] + body + text[m.end(2) :]


def allowed_for_weapon(weapon: str, fam: str) -> set[str] | None:
    """Return restricted mag set for weapons that need caliber wells; else None."""
    if fam != "AK":
        return None
    if weapon in AK762:
        return set(AK762_MAGS)
    if weapon in AK545:
        return set(AK545_MAGS)
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    fam_opts: dict[str, set[str]] = defaultdict(set)
    weapon_texts: dict[str, tuple[Path, str]] = {}
    for fam, members in FAMILY_MEMBERS.items():
        for w in members:
            path = INV / f"{w}.lua"
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            weapon_texts[w] = (path, text)
            extracted = extract_mag_options(text)
            if not extracted:
                continue
            _, _, opts = extracted
            for o in opts:
                if o.startswith("JAZZ_MagNormal"):
                    continue
                if o.endswith(f"_{fam}") or o in LEGACY_FAMILY_SHARED.get(fam, ()):
                    fam_opts[fam].add(o)
                # Collect caliber-tagged AK mags into fam_opts only via allowed sets at merge

    # Seed AK caliber mags into fam_opts["AK"] for reporting; merge uses allowed_for_weapon.
    fam_opts["AK"] |= AK762_MAGS | AK545_MAGS

    print("Family option unions:")
    for fam in sorted(fam_opts):
        print(f"  {fam}: {sorted(fam_opts[fam])}")

    if not args.apply:
        print("dry-run")
        return 0

    changed = 0
    for w, (path, text) in weapon_texts.items():
        fam = WEAPON_TO_FAMILY.get(w)
        if not fam or fam not in fam_opts:
            continue
        extracted = extract_mag_options(text)
        if not extracted:
            continue
        _, _, opts = extracted
        normals = [o for o in opts if o.startswith("JAZZ_MagNormal")]
        caliber = allowed_for_weapon(w, fam)
        if caliber is not None:
            # Keep only normals + caliber-allowed (+ any non-family extras)
            others_keep = [
                o
                for o in opts
                if o not in normals
                and o not in AK762_MAGS
                and o not in AK545_MAGS
                and not o.endswith(f"_{fam}")
                and not any(o.endswith(f"_{s}") for s in FAMILY_MEMBERS)
            ]
            merged = normals + sorted(set(others_keep) | caliber)
        else:
            others_keep = [
                o
                for o in opts
                if o not in normals
                and not o.endswith(f"_{fam}")
                and o not in LEGACY_FAMILY_SHARED.get(fam, ())
                and not any(o.endswith(f"_{s}") for s in FAMILY_MEMBERS)
            ]
            merged = normals + sorted(set(others_keep) | fam_opts[fam])
        seen: set[str] = set()
        ordered: list[str] = []
        for o in merged:
            if o not in seen:
                seen.add(o)
                ordered.append(o)
        if ordered == opts:
            continue
        new_text = replace_mag_options(text, ordered)
        if not new_text:
            continue
        path.write_text(new_text, encoding="utf-8", newline="\n")
        changed += 1
        print("updated", w, "->", ordered)

    print("weapons updated", changed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
