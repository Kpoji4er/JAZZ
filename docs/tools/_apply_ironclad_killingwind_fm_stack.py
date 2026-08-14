# -*- coding: utf-8 -*-
"""Ironclad −50% armor FM tax + KillingWind another −50% (stack to 0). Sync items/metadata/CSV.

Does not bump metadata Revision. Does not change BeginTurn cumbersome FreeMove.
"""
from __future__ import annotations

import csv
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"
RU = ROOT / "Russian.csv"
EN = ROOT / "English.csv"

KW_DESC_ID = "890000000009876"
IR_DESC_ID = "890000000013124"

KW_RU = (
    "При попадании по ≥2 врагам: +<gritPerEnemyHit> Grit за каждого. "
    "Ещё −50% штрафа Free Move от брони (вместе с Железной кожей — без штрафа FM от брони). "
    "Громоздкое оружие не лишает Free Move."
)
KW_EN = (
    "On hitting ≥2 enemies: +<gritPerEnemyHit> Grit per enemy. "
    "Another −50% armor Free Move penalty (with Ironclad: no armor FM tax). "
    "Cumbersome weapons keep Free Move."
)
IR_RU = (
    "Штраф <GameTerm('FreeMove')> от тяжёлой брони снижен на <em>50%</em>. "
    "Также вдвое снижает штраф стартовых ОД от веса брони."
)
IR_EN = (
    "Heavy armor <GameTerm('FreeMove')> penalty reduced by <em>50%</em>. "
    "Also halves the start-of-turn AP penalty from armor weight."
)

LOC = {
    KW_DESC_ID: (KW_RU, KW_EN, "jazz:CharacterEffect/KillingWind.lua"),
    IR_DESC_ID: (IR_RU, IR_EN, "jazz:CharacterEffect/Ironclad.lua"),
}

IR_ITEM = (
    "\t\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {\n"
    "\t\t\t\t\t'Group', \"Strength\",\n"
    "\t\t\t\t\t'Id', \"Ironclad\",\n"
    "\t\t\t\t\t'SortKey', 5,\n"
    "\t\t\t\t\t'object_class', \"Perk\",\n"
    f"\t\t\t\t\t'DisplayName', T(103856163842, --[[ModItemCharacterEffectCompositeDef Ironclad DisplayName]] \"Ironclad\"),\n"
    f"\t\t\t\t\t'Description', T({IR_DESC_ID}, --[[ModItemCharacterEffectCompositeDef Ironclad Description]] \"{IR_RU}\"),\n"
    "\t\t\t\t\t'Icon', \"UI/Icons/Perks/OverwatchExpert\",\n"
    "\t\t\t\t\t'Tier', \"Silver\",\n"
    "\t\t\t\t\t'Stat', \"Strength\",\n"
    "\t\t\t\t\t'StatValue', 80,\n"
    "\t\t\t\t}),\n"
)


def upsert_csv(path: Path, lang: str) -> None:
    # Line-based upsert: keep BOM and quoting of untouched rows.
    raw = path.read_text(encoding="utf-8-sig")
    newline = "\r\n" if "\r\n" in raw else "\n"
    lines = raw.splitlines()
    by_id = {}
    for lid, (ru, en, ctx) in LOC.items():
        translation = ru if lang == "ru" else en
        fields = [lid, ru, translation, "", ctx]
        buf = io.StringIO()
        writer = csv.writer(buf, lineterminator="", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(fields)
        by_id[lid] = buf.getvalue()
    out = []
    seen = set()
    for line in lines:
        rid = line.split(",", 1)[0] if line else ""
        if rid in by_id:
            out.append(by_id[rid])
            seen.add(rid)
            print(f"{path.name} updated {rid}")
        else:
            out.append(line)
    for lid, row in by_id.items():
        if lid not in seen:
            out.append(row)
            print(f"{path.name} inserted {lid}")
    text = newline.join(out)
    if not text.endswith(newline):
        text += newline
    path.write_text(text, encoding="utf-8-sig")


def patch_items() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    old_kw = (
        "'Description', T(890000000009876, --[[ModItemCharacterEffectCompositeDef KillingWind Description]] "
        '"При попадании по ≥2 врагам: +<gritPerEnemyHit> Grit за каждого. '
        'Штраф Free Move от тяжёлой брони −50%; громоздкое оружие не лишает Free Move.")'
    )
    new_kw = (
        f"'Description', T({KW_DESC_ID}, --[[ModItemCharacterEffectCompositeDef KillingWind Description]] "
        f'"{KW_RU}")'
    )
    if old_kw in text:
        text = text.replace(old_kw, new_kw, 1)
        print("items.lua: KillingWind Description updated")
    elif KW_RU in text:
        print("items.lua: KillingWind Description already new")
    else:
        raise SystemExit("items.lua: KillingWind Description not found")

    if "'Id', \"Ironclad\"" in text:
        print("items.lua: Ironclad ModItem already present")
    else:
        needle = "\t\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {\n\t\t\t\t\t'Group', \"Perk-Personal\",\n\t\t\t\t\t'Id', \"KillingWind\","
        if needle not in text:
            raise SystemExit("items.lua: KillingWind ModItem anchor missing")
        text = text.replace(needle, IR_ITEM + needle, 1)
        print("items.lua: Ironclad ModItem inserted before KillingWind")

    ITEMS.write_text(text, encoding="utf-8")


def patch_metadata() -> None:
    text = META.read_text(encoding="utf-8")
    entry = '"CharacterEffect/Ironclad.lua",'
    if entry in text:
        print("metadata.lua: Ironclad already in code")
        return
    anchor = '\t\t"CharacterEffect/KillingWind.lua",'
    if anchor not in text:
        raise SystemExit("metadata.lua: KillingWind.lua missing from code")
    text = text.replace(anchor, f'\t\t{entry}\n{anchor}', 1)
    META.write_text(text, encoding="utf-8")
    print("metadata.lua: inserted CharacterEffect/Ironclad.lua")


def main() -> None:
    patch_items()
    patch_metadata()
    upsert_csv(RU, "ru")
    upsert_csv(EN, "en")
    print("ironclad/killingwind FM stack apply done")


if __name__ == "__main__":
    main()
