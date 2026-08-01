# -*- coding: utf-8 -*-
"""Split cross-family shared JAZZ_Mag* into platform-family component IDs.

Example: JAZZ_MagLarge_50 on AK47 + M16 → JAZZ_MagLarge_50_AK / _AR15 / _MP5 / …
AK family includes RPK/RPK74 (same mag well). MagNormal stays universal.

Also writes InventoryItem companions (JAZZ_RemovableAttachment) for every new id.

Usage:
  python docs/tools/_split_mag_families.py           # dry-run
  python docs/tools/_split_mag_families.py --apply
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _apply_attach_001 import placeobj_blocks, prop
from _gen_removable_attachment_items import (
    companion_lua,
    escape_lua_str,
    is_lua_identifier,
    moditem_block,
)

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"
INV = ROOT / "InventoryItem"
OPT_CSV = ROOT / "docs/technical/weapons/data/weapon-component-options.csv"
COMP_CSV = ROOT / "docs/technical/weapons/data/weapon-components.csv"

# Weapon id → magazine family (mag well / feed geometry).
FAMILY_MEMBERS: dict[str, tuple[str, ...]] = {
    "AK": (
        "AK47", "AK74", "AKM", "AKSU", "Type56", "AN94",
        "RPK", "RPK74", "Zastava_M70", "ZastavaM92",
    ),
    "VAL": ("AS_Val", "VSS"),
    "AR15": (
        "AR15", "M16A1", "M16A2", "M16A4", "M4A1", "M4Commando", "CAR15",
    ),
    "SIG": ("Sig550", "Sig550Custom", "Sig552", "Sig552SWAT"),
    "FAL": ("FNFAL",),
    "GALIL": ("Galil", "Galil_FlagHill"),
    "G36": ("G36", "G36c"),
    "AUG": ("AUG",),
    "HK33": ("HK33",),
    "G3": ("G3A3", "G3A4", "G3SniperV1", "HK21", "HK23e", "U100"),
    "MP5": ("MP5", "MP5A2", "MP5A4", "MP5K", "MP5SD"),
    "MP40": ("MP40",),
    "UZI": ("UZI", "MicroUZI"),
    "UMP": ("UMP45",),
    "TMP": ("TMP",),
    "THOMPSON": ("Thompson",),
    "SVD": ("DragunovSVD", "DragunovSVD_Custom", "SVU", "ZastavaM76"),
    "M14": ("M14SAW", "M1A", "M21"),
    "MINI14": ("Mini14",),
    "BARRET": ("BarretM82",),
    "PSG1": ("PSG1",),
    "AA12": ("AA12",),
    "USAS": ("USAS12",),
    "PISTOL_9": (
        "Glock17", "Glock18", "Bereta92", "Beretta93r", "CZ75", "P226",
        "HiPower", "MP446VIKING", "SWModel5906", "VectorCP1",
    ),
    "PISTOL_45": ("USP45", "Colt1911", "Kimber"),
    "PISTOL_DE": ("DesertEagle",),
    "PISTOL_52": ("SWModel52", "CZ52", "MAC1950", "P38"),
    "M2CARBINE": ("M2Carbine",),
}

SKIP_SPLIT = {
    "JAZZ_MagNormal",  # factory placeholder, not remountable catalog
}

# Bases that must not create an _AK family clone (AK uses MagLarge_30_40 = 40).
SKIP_FAMILY_CLONE = {
    ("JAZZ_MagLarge_50", "AK"),
}

# Loc block for new InventoryItems (after FreeParts/ScopeParts range).
LOC_BASE = 990002520

WEAPON_TO_FAMILY: dict[str, str] = {}
for fam, members in FAMILY_MEMBERS.items():
    for w in members:
        WEAPON_TO_FAMILY[w] = fam


def family_of(weapon: str) -> str:
    return WEAPON_TO_FAMILY.get(weapon, f"OTHER_{weapon}")


def new_id(old: str, fam: str) -> str:
    return f"{old}_{fam}"


def load_usage() -> dict[str, list[str]]:
    """Prefer live InventoryItem companions; fall back to options CSV."""
    usage: dict[str, list[str]] = defaultdict(list)
    for path in INV.glob("*.lua"):
        text = path.read_text(encoding="utf-8")
        if "SlotType\", \"Magazine\"" not in text and "SlotType', \"Magazine\"" not in text:
            # also accept 'SlotType', "Magazine"
            if "'SlotType', \"Magazine\"" not in text:
                continue
        m = re.search(
            r"'SlotType',\s*\"Magazine\",.*?AvailableComponents',\s*\{(.*?)\}",
            text,
            flags=re.S,
        )
        if not m:
            continue
        for cid in re.findall(r"\"(JAZZ_Mag[^\"]+)\"", m.group(1)):
            usage[cid].append(path.stem)
    if usage:
        return {k: sorted(set(v)) for k, v in usage.items()}
    with OPT_CSV.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row["slot_type"] != "Magazine":
                continue
            cid = row["component_id"]
            if not cid.startswith("JAZZ_Mag"):
                continue
            usage[cid].append(row["weapon_id"])
    return {k: sorted(set(v)) for k, v in usage.items()}


def split_plan(usage: dict[str, list[str]]) -> dict[str, dict[str, list[str]]]:
    """old_id → { family → [weapons] }.

    Handles both pre-split shared ids and already-suffixed ids (re-apply safe).
    """
    fam_names = sorted(FAMILY_MEMBERS, key=len, reverse=True)
    plan: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))

    for cid, weapons in usage.items():
        if cid in SKIP_SPLIT:
            continue
        base, fam = cid, None
        for name in fam_names:
            suf = f"_{name}"
            if cid.endswith(suf):
                base, fam = cid[: -len(suf)], name
                break
        if fam:
            plan[base][fam].extend(weapons)
            continue
        by_fam: dict[str, list[str]] = defaultdict(list)
        for w in weapons:
            by_fam[family_of(w)].append(w)
        if len(by_fam) <= 1:
            continue
        for f, ws in by_fam.items():
            plan[base][f].extend(ws)

    out: dict[str, dict[str, list[str]]] = {}
    for base, fams in plan.items():
        cleaned = {f: sorted(set(ws)) for f, ws in fams.items() if ws}
        if len(cleaned) >= 1:
            out[base] = cleaned
    return out


def filter_visuals(block: str, family_weapons: set[str]) -> str:
    """Keep Visuals without ApplyTo, or ApplyTo in family_weapons."""
    # Split Visuals list entries
    m = re.search(r"Visuals\s*=\s*\{", block)
    if not m:
        return block
    start = m.end() - 1
    # find matching brace for Visuals table
    depth, i = 0, start
    while i < len(block):
        ch = block[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i
                break
        i += 1
    else:
        return block
    visuals_body = block[start + 1 : end]
    kept = []
    for vm in re.finditer(
        r"PlaceObj\('WeaponComponentVisual',\s*\{(.*?)\}\),",
        visuals_body,
        flags=re.S,
    ):
        entry = vm.group(0)
        am = re.search(r"ApplyTo\s*=\s*\"([^\"]+)\"", entry)
        if not am or am.group(1) in family_weapons:
            kept.append(entry)
    new_visuals = "Visuals = {\n" + ("\n".join(kept) + ("\n" if kept else "")) + "\t\t\t\t\t\t\t}"
    return block[: m.start()] + new_visuals + block[end + 1 :]


def clone_component_block(block: str, old_id: str, new_cid: str, fam: str, weapons: list[str]) -> str:
    text = block
    text = text.replace(f'id = "{old_id}"', f'id = "{new_cid}"')
    text = text.replace(f"id = '{old_id}'", f"id = '{new_cid}'")
    # comment tag
    text = re.sub(
        r'comment\s*=\s*"[^"]*"',
        f'comment = "Mag family {fam} — split from {old_id}"',
        text,
        count=1,
    )
    if "comment =" not in text:
        text = text.replace(
            f'id = "{new_cid}"',
            f'comment = "Mag family {fam} — split from {old_id}",\n\t\t\t\t\t\t\tid = "{new_cid}"',
        )
    text = filter_visuals(text, set(weapons))
    return text


def replace_in_weapon_files(old: str, mapping: dict[str, str], weapon_files: dict[str, Path]) -> int:
    """mapping: weapon_id → new component id."""
    n = 0
    for weapon, new_cid in mapping.items():
        path = weapon_files.get(weapon)
        if not path or not path.exists():
            # try InventoryItem/<weapon>.lua
            path = INV / f"{weapon}.lua"
        if not path.exists():
            print("WARN missing weapon file", weapon)
            continue
        text = path.read_text(encoding="utf-8")
        if f'"{old}"' not in text and f"'{old}'" not in text:
            continue
        new_text = text.replace(f'"{old}"', f'"{new_cid}"').replace(f"'{old}'", f"'{new_cid}'")
        if new_text != text:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            n += 1
    return n


def replace_in_items_weapon_blocks(items: str, old: str, weapon_to_new: dict[str, str]) -> str:
    """Replace AvailableComponents string in ModItemInventoryItemCompositeDef per weapon Id."""
    out = []
    last = 0
    for block in placeobj_blocks(items, "ModItemInventoryItemCompositeDef"):
        wid = prop(block.text, "Id")
        if not wid or wid not in weapon_to_new:
            continue
        new_cid = weapon_to_new[wid]
        chunk = block.text
        if f'"{old}"' not in chunk:
            continue
        chunk2 = chunk.replace(f'"{old}"', f'"{new_cid}"')
        out.append((block.start, block.end, chunk2))
    if not out:
        return items
    parts = []
    cursor = 0
    for start, end, repl in sorted(out):
        parts.append(items[cursor:start])
        parts.append(repl)
        cursor = end
    parts.append(items[cursor:])
    return "".join(parts)


def upsert_loc(path: Path, rows: list[tuple[int, str, str]]) -> None:
    """rows: (id, ru_or_en_text_for_col, lang) — simplified: write id,en,ru style."""
    # Actually Russian.csv: id, english?, russian?, ...
    # Match existing: id, Text, Translation, ...
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    by_id = {}
    for i, line in enumerate(lines):
        if line.startswith("id,") or not line.strip():
            continue
        parts = line.split(",", 1)
        if parts and parts[0].isdigit():
            by_id[int(parts[0])] = i
    # append missing
    append = []
    for tid, en, ru in rows:
        if tid in by_id:
            continue
        if path.name.startswith("Russian"):
            append.append(f"{tid},{en},{ru},,jazz:InventoryItem/mag-family\n")
        else:
            append.append(f"{tid},{en},,,jazz:InventoryItem/mag-family\n")
    if append:
        if not text.endswith("\n"):
            text += "\n"
        path.write_text(text + "".join(append), encoding="utf-8", newline="\n")


def write_inventory_item(cid: str, display: str, icon: str, cost: int, t0: int, fam: str) -> None:
    hint_ru = (
        f"Семья магазинов: {fam}. Съёмный модуль. "
        "Перетащите на совместимое оружие или установите в кабинете модификации."
    )
    # companion_lua uses fixed hint — write custom
    if is_lua_identifier(cid):
        define_open = f"DefineClass.{cid} = {{"
        define_close = "}"
    else:
        define_open = f'DefineClass("{cid}", {{'
        define_close = "})"
    body = (
        f"UndefineClass('{cid}')\n"
        f"{define_open}\n"
        f'\t__parents = {{ "JAZZ_RemovableAttachment" }},\n'
        f'\t__generated_by_class = "ModItemInventoryItemCompositeDef",\n'
        f"\n"
        f'\tobject_class = "JAZZ_RemovableAttachment",\n'
        f"\tRepairable = false,\n"
        f'\tIcon = "{escape_lua_str(icon)}",\n'
        f'\tDisplayName = T({t0}, --[[ModItemInventoryItemCompositeDef {cid} DisplayName]] "{escape_lua_str(display)}"),\n'
        f'\tDisplayNamePlural = T({t0+1}, --[[ModItemInventoryItemCompositeDef {cid} DisplayNamePlural]] "{escape_lua_str(display)}"),\n'
        f'\tAdditionalHint = T({t0+2}, --[[ModItemInventoryItemCompositeDef {cid} AdditionalHint]] "{escape_lua_str(hint_ru)}"),\n'
        f"\tCost = {max(0, cost) * 100 if cost and cost < 100 else max(0, cost)},\n"
        f"\tCanAppearInShop = false,\n"
        f'\tCategoryPair = "Components",\n'
        f"\tMaxStacks = 1,\n"
        f'\tRemovableComponentId = "{cid}",\n'
        f"{define_close}\n"
    )
    (INV / f"{cid}.lua").write_text(body, encoding="utf-8", newline="\n")


def patch_metadata_code_and_items(meta: str, new_ids: list[str]) -> str:
    # Insert code paths after RemovableAttachment.lua or MagLarge_50 if present
    anchor = '"InventoryItem/JAZZ_RemovableAttachment.lua",'
    if anchor not in meta:
        anchor = '"InventoryItem/JAZZ_MagLarge_50.lua",'
    if anchor not in meta:
        raise SystemExit("metadata code anchor not found")
    insert_code = "".join(f'\t\t"InventoryItem/{cid}.lua",\n' for cid in new_ids)
    # avoid dup
    for cid in new_ids:
        meta = re.sub(rf'\s*"InventoryItem/{re.escape(cid)}\.lua",\n', "\n", meta)
    meta = meta.replace(anchor, anchor + "\n" + insert_code, 1)

    # ModResourcePreset entries
    res_chunks = []
    for cid in new_ids:
        res_chunks.append(
            "\t\tPlaceObj('ModResourcePreset', {\n"
            f'\t\t\t\'Class\', "InventoryItemCompositeDef",\n'
            f'\t\t\t\'Id\', "{cid}",\n'
            f'\t\t\t\'ClassDisplayName\', "Inventory item",\n'
            "\t\t}),\n"
        )
    marker = "'Id', \"JAZZ_RemovableAttachment\""
    idx = meta.find(marker)
    if idx < 0:
        raise SystemExit("metadata items RemovableAttachment not found")
    # find end of that PlaceObj
    from _apply_attach_001 import matching_paren
    p0 = meta.rfind("PlaceObj(", 0, idx)
    end = matching_paren(meta, meta.find("(", p0))
    meta = meta[: end + 1] + ",\n" + "".join(res_chunks) + meta[end + 1 :]
    # clean double commas messy — ok if PlaceObj ends with }),
    return meta


def insert_moditems_folder(items: str, blocks: list[str]) -> str:
    begin = "-- JAZZ-WEAPONS-002-REMOVABLE-ITEMS-BEGIN"
    end = "-- JAZZ-WEAPONS-002-REMOVABLE-ITEMS-END"
    chunk = "\n".join(blocks) + "\n"
    if begin in items and end in items:
        a = items.find(begin)
        b = items.find(end)
        # insert before END
        return items[:b] + chunk + items[b:]
    # fallback: before Handgrip WeaponUpgradeSlot
    needle = "PlaceObj('ModItemWeaponUpgradeSlot', {\n\t\t\t\tDisplayName = T(186293445167"
    pos = items.find(needle)
    if pos < 0:
        raise SystemExit("cannot find remountable folder or Handgrip anchor")
    return items[:pos] + chunk + items[pos:]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    usage = load_usage()
    plan = split_plan(usage)
    print(f"components to split: {len(plan)}")
    for cid, fams in sorted(plan.items()):
        print(f"  {cid}: { {f: len(ws) for f, ws in fams.items()} }")

    if not args.apply:
        print("dry-run; pass --apply to write")
        return 0

    items = ITEMS.read_text(encoding="utf-8")
    # index weapon components
    comp_blocks = {
        prop(b.text, "id") or prop(b.text, "Id"): b
        for b in placeobj_blocks(items, "ModItemWeaponComponent")
    }

    new_component_inserts: list[str] = []
    inventory_moditems: list[str] = []
    loc_rows: list[tuple[int, str, str]] = []
    new_ids: list[str] = []
    loc_i = 0
    retired: list[str] = []

    for old_id, fams in sorted(plan.items()):
        src = comp_blocks.get(old_id)
        if not src:
            print("WARN no component block", old_id)
            continue
        display_m = re.search(
            r'DisplayName\s*=\s*T\([^)]*?"([^"]*)"',
            src.text,
            flags=re.S,
        )
        display = display_m.group(1) if display_m else old_id
        icon_m = re.search(r'Icon\s*=\s*"([^"]+)"', src.text)
        icon = icon_m.group(1) if icon_m else "UI/Icons/Upgrades/galil_magazine_large"
        cost_m = re.search(r"Cost\s*=\s*(\d+)", src.text)
        cost = int(cost_m.group(1)) if cost_m else 25

        weapon_to_new: dict[str, str] = {}
        for fam, weapons in sorted(fams.items()):
            if (old_id, fam) in SKIP_FAMILY_CLONE:
                print("skip family clone", old_id, fam)
                continue
            nid = new_id(old_id, fam)
            new_ids.append(nid)
            weapon_to_new.update({w: nid for w in weapons})
            if nid not in comp_blocks and old_id in comp_blocks:
                cloned = clone_component_block(src.text, old_id, nid, fam, weapons)
                new_component_inserts.append(cloned + ",")
            elif nid not in comp_blocks and old_id not in comp_blocks:
                print("WARN cannot clone", old_id, "->", nid)

            already_moditem = f"'Id', \"{nid}\"" in items
            if not (INV / f"{nid}.lua").exists() or not already_moditem:
                t0 = LOC_BASE + loc_i
                loc_i += 3
                loc_rows.append((t0, display, display))
                loc_rows.append((t0 + 1, display, display))
                loc_rows.append(
                    (
                        t0 + 2,
                        f"Magazine family: {fam}. Removable module. Drag onto a compatible firearm or install in the weapon modification screen.",
                        f"Семья магазинов: {fam}. Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации.",
                    )
                )
                if not (INV / f"{nid}.lua").exists():
                    write_inventory_item(nid, display, icon, cost, t0, fam)
                if not already_moditem:
                    inventory_moditems.append(
                        moditem_block(nid, display, icon, cost, t0, t0 + 1, t0 + 2)
                    )

        for weapon, nid in weapon_to_new.items():
            path = INV / f"{weapon}.lua"
            if path.exists():
                t = path.read_text(encoding="utf-8")
                if f'"{old_id}"' in t:
                    path.write_text(
                        t.replace(f'"{old_id}"', f'"{nid}"'),
                        encoding="utf-8",
                        newline="\n",
                    )
        items = replace_in_items_weapon_blocks(items, old_id, weapon_to_new)

        # Retire old component id string from any leftover options (defaults etc.)
        retired.append(old_id)

    # Insert clones into CURRENT items text (offsets from initial parse are stale
    # after replace_in_items_weapon_blocks).
    if new_component_inserts:
        live_blocks = {
            prop(b.text, "id") or prop(b.text, "Id"): b
            for b in placeobj_blocks(items, "ModItemWeaponComponent")
        }
        anchor = live_blocks.get("JAZZ_MagLarge_50") or live_blocks.get(retired[0] if retired else "")
        if not anchor:
            # fallback: first retired still present
            for rid in retired:
                if rid in live_blocks:
                    anchor = live_blocks[rid]
                    break
        if not anchor:
            raise SystemExit("cannot find insert anchor for new mag components")
        blob = "\n" + "\n".join(new_component_inserts) + "\n"
        items = items[: anchor.end] + blob + items[anchor.end :]

    items = insert_moditems_folder(items, inventory_moditems)

    # backup + write
    bak = ITEMS.with_suffix(".lua.bak_mag_families")
    bak.write_bytes(ITEMS.read_bytes())
    ITEMS.write_text(items, encoding="utf-8", newline="\n")

    meta = META.read_text(encoding="utf-8")
    META.write_text(patch_metadata_code_and_items(meta, new_ids), encoding="utf-8", newline="\n")

    upsert_loc(ROOT / "Russian.csv", loc_rows)
    upsert_loc(ROOT / "English.csv", [(a, b, "") for a, b, c in loc_rows])

    # Fix inventory AdditionalHint T ids already baked in write_inventory_item —
    # moditem_block still uses generic hint; patch RemovableComponent hints in items for family.
    print(f"created {len(new_ids)} family mag components + InventoryItems")
    print("retired shared ids (no longer on weapons):", ", ".join(retired))
    print("NOTE: re-export CSV via docs tools; old shared comps may remain as unused defs until purge.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
