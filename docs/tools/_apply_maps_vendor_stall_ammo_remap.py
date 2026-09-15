#!/usr/bin/env python3
"""Copy vanilla vendor stall BanterDefs into jazz-maps and remap vendor LootDef ammo.

Stall labels (Banters_Vendors_Stalls) do not contain InventoryItem IDs. Trader stock
is granted via CustomInteractable → UnitGrantItem(LootTableId=…). This script:

1. Copies vanilla stall BanterDef presets into jazz-maps `Stall Banters` as
   ModItemBanterDef with the same ids (map markers keep working).
2. Overrides vanilla vendor LootDef presets with live JAZZ_AMMO_* / live weapons.

Idempotent. Does not rewrite Maps/*/objects.lua DisplayName prompts.
`--audit-only` also checks I5 `ubRwFgf` custom stall grants: they must use
`JAZZ_AMMO_*` ItemId, not vanilla `Drop_762WP_HP` / `Drop_12gauge_Varied_Legion`.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CORE = Path(__file__).resolve().parents[2]
DEFAULT_MAPS = CORE.parent / "JAZZ Maps"
if not (DEFAULT_MAPS / "items.lua").is_file():
    DEFAULT_MAPS = CORE.parent / "jazz-maps"

VANILLA_DUMP = Path(
    r"C:\Users\23ser\Downloads\JaggedAlliance3Modding-main\JaggedAlliance3Modding-main"
)

STALL_BANTERS_SRC = VANILLA_DUMP / "Data" / "BantersDef" / "BanterDef-Banters_Vendors_Stalls.lua"
LOOTDEF_SRC = VANILLA_DUMP / "Data" / "LootDef.lua"

VENDOR_LOOT_IDS = (
    "Vendor_Ammo",
    "FleatownMarket_Ammo",
    "FleatownMarket_Pistol",
    "FleatownMarket_SMG",
    "FleatownMarket_Shotgun",
    "FosseNoire_Ammo",
    "IlleMorat_Gunpowder",
    "PoacherCamp_Ammo",
    "PoacherCamp_Rifle",
    "PortCacao_AssaultRifle",
    "PortCacao_Shotgun",
    "SmugglerPort_AssaultRifle",
)

# Cut vanilla ammo → live JAZZ family (see docs/technical/weapons/cut-content.md).
AMMO_REMAP: dict[str, str] = {
    "_9mm_Basic": "JAZZ_AMMO_9x19_FMJ",
    "_9mm_AP": "JAZZ_AMMO_9x19_AP",
    "_9mm_HP": "JAZZ_AMMO_9x19_JHP",
    "_9mm_Match": "JAZZ_AMMO_9x19_Match",
    "_9mm_Shock": "JAZZ_AMMO_9x19_FMJ",
    "_9mm_Subsonic": "JAZZ_AMMO_9x19_FMJ",
    "_9mm_Tracer": "JAZZ_AMMO_9x19_FMJ",
    "_44CAL_Basic": "JAZZ_AMMO_44CAL_FMJ",
    "_44CAL_AP": "JAZZ_AMMO_44CAL_FMJ",
    "_44CAL_HP": "JAZZ_AMMO_44CAL_JHP",
    "_44CAL_Match": "JAZZ_AMMO_44CAL_Match",
    "_44CAL_Shock": "JAZZ_AMMO_44CAL_JHP",
    "_762NATO_Basic": "JAZZ_AMMO_762x51_FMJ",
    "_762NATO_AP": "JAZZ_AMMO_762x51_AP",
    "_762NATO_HP": "JAZZ_AMMO_762x51_FMJ",
    "_762NATO_Match": "JAZZ_AMMO_762x51_Match",
    "_762NATO_Tracer": "JAZZ_AMMO_762x51_Tracer",
    "_762WP_Basic": "JAZZ_AMMO_762x39_Army",
    "_762WP_AP": "JAZZ_AMMO_762x39_APP",
    "_762WP_HP": "JAZZ_AMMO_762x39_FMJ",
    "_762WP_Match": "JAZZ_AMMO_762x39_FMJ",
    "_762WP_Subsonic": "JAZZ_AMMO_762x39_US",
    "_762WP_Tracer": "JAZZ_AMMO_762x39_Tracer",
    "_12gauge_Buckshot": "JAZZ_AMMO_12gauge_Buckshot",
    "_12gauge_APSlug": "JAZZ_AMMO_12gauge_APSlug",
    "_12gauge_Breacher": "JAZZ_AMMO_12gauge_Buckshot",
    "_12gauge_Flechette": "JAZZ_AMMO_12gauge_Slug",
    "_12gauge_Saltshot": "JAZZ_AMMO_12gauge_Saltshot",
    "_50BMG_Basic": "JAZZ_AMMO_50BMG_Basic",
    "_50BMG_HE": "JAZZ_AMMO_50BMG_API_HEI",
    "_50BMG_Incendiary": "JAZZ_AMMO_50BMG_APIT",
    "_50BMG_SLAP": "JAZZ_AMMO_50BMG_Basic",
    "_556_Basic": "JAZZ_AMMO_556_FMJ",
    "_556_AP": "JAZZ_AMMO_556_AP",
    "_556_HP": "JAZZ_AMMO_556_Match",
    "_556_Match": "JAZZ_AMMO_556_Match",
    "_556_Tracer": "JAZZ_AMMO_556_Tracer",
    "AR15": "M16A2",
    "M4Commando": "M4A1",
    "MP5": "MP5A2",
}

BANTER_BEGIN = "\t\t-- JAZZ-VANILLA-STALL-BANTERS-BEGIN\n"
BANTER_END = "\t\t-- JAZZ-VANILLA-STALL-BANTERS-END\n"
LOOT_BEGIN = "\t-- JAZZ-VENDOR-LOOT-BEGIN\n"
LOOT_END = "\t-- JAZZ-VENDOR-LOOT-END\n"

ID_RE = re.compile(r"\bid = \"([^\"]+)\"")
RESOURCE_ID_RE = re.compile(r"'Id', \"([^\"]+)\"")


def _extract_placeobjs(src: str, class_name: str) -> list[str]:
    token = f"PlaceObj('{class_name}'"
    out: list[str] = []
    i = 0
    while True:
        start = src.find(token, i)
        if start < 0:
            break
        depth = 0
        j = src.find("(", start)
        if j < 0:
            raise RuntimeError(f"no '(' after {class_name} at {start}")
        k = j
        while k < len(src):
            ch = src[k]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    block = src[start : k + 1]
                    out.append(block)
                    i = k + 1
                    break
            k += 1
        else:
            raise RuntimeError(f"unbalanced {class_name} starting at {start}")
    return out


def _block_id(block: str) -> str | None:
    m = ID_RE.search(block)
    return m.group(1) if m else None


def _indent_block(block: str, extra_tabs: int) -> str:
    pad = "\t" * extra_tabs
    lines = block.splitlines()
    return "\n".join(pad + ln if ln else ln for ln in lines)


def _remap_ammo(block: str) -> tuple[str, list[tuple[str, str]]]:
    changes: list[tuple[str, str]] = []
    out = block
    for old, new in AMMO_REMAP.items():
        pat = re.compile(rf'(item|weapon) = "{re.escape(old)}"')
        if pat.search(out):
            out = pat.sub(rf'\1 = "{new}"', out)
            changes.append((old, new))
    return out, changes


def _to_moditem(block: str, from_class: str, to_class: str) -> str:
    block = block.replace(f"PlaceObj('{from_class}'", f"PlaceObj('{to_class}'", 1)
    block = block.replace(f"--[[{from_class} ", f"--[[{to_class} ")
    if not block.endswith(","):
        block += ","
    return block


def _existing_moditem_ids(items: str, class_name: str) -> set[str]:
    ids: set[str] = set()
    for block in _extract_placeobjs(items, class_name):
        bid = _block_id(block)
        if bid:
            ids.add(bid)
    return ids


def _resource_block(cls: str, oid: str, display: str) -> str:
    return (
        "\t\tPlaceObj('ModResourcePreset', {\n"
        f"\t\t\t'Class', \"{cls}\",\n"
        f"\t\t\t'Id', \"{oid}\",\n"
        f"\t\t\t'ClassDisplayName', \"{display}\",\n"
        "\t\t}),\n"
    )


def _insert_resources(meta: str, cls: str, ids: list[str], display: str, after_id: str) -> str:
    needle = f"'Id', \"{after_id}\""
    pos = meta.find(needle)
    if pos < 0:
        raise RuntimeError(f"metadata.lua: missing resource after-id {after_id}")
    close = meta.find("}),", pos)
    if close < 0:
        raise RuntimeError(f"metadata.lua: cannot find resource closer after {after_id}")
    insert_at = close + 3
    if meta[insert_at : insert_at + 1] == "\n":
        insert_at += 1
    existing = set(RESOURCE_ID_RE.findall(meta))
    chunks = []
    for oid in ids:
        if oid in existing:
            continue
        chunks.append(_resource_block(cls, oid, display))
    if not chunks:
        return meta
    return meta[:insert_at] + "".join(chunks) + meta[insert_at:]


def _replace_marked(src: str, begin: str, end: str, payload: str) -> str:
    start = src.find(begin)
    stop = src.find(end)
    if start >= 0 and stop > start:
        return src[:start] + payload + src[stop + len(end) :]
    return src


def build_stall_banters(items: str, vanilla: str) -> tuple[str, list[str]]:
    existing = _existing_moditem_ids(items, "ModItemBanterDef")
    blocks = _extract_placeobjs(vanilla, "BanterDef")
    converted: list[str] = []
    ids: list[str] = []
    for raw in blocks:
        bid = _block_id(raw)
        if not bid:
            continue
        if bid in existing and BANTER_BEGIN not in items:
            # Already authored (Ernie custom stalls). Skip only if not our marked dump.
            continue
        body = _to_moditem(raw, "BanterDef", "ModItemBanterDef")
        converted.append(_indent_block(body, 2))
        ids.append(bid)
    payload = BANTER_BEGIN + "\n".join(converted) + ("\n" if converted else "") + BANTER_END
    if BANTER_BEGIN in items:
        return _replace_marked(items, BANTER_BEGIN, BANTER_END, payload), ids
    anchor = "\t\t}),\n\tPlaceObj('ModItemFolder', {\n\t\t'name', \"Maps\","
    pos = items.find(anchor)
    if pos < 0:
        raise RuntimeError("items.lua: Stall Banters folder closer before Maps not found")
    return items[:pos] + payload + items[pos:], ids


def build_vendor_loot(items: str, vanilla: str) -> tuple[str, list[str], list[tuple[str, str, str]]]:
    existing = _existing_moditem_ids(items, "ModItemLootDef")
    wanted = set(VENDOR_LOOT_IDS)
    changes: list[tuple[str, str, str]] = []
    converted: list[str] = []
    ids: list[str] = []
    for raw in _extract_placeobjs(vanilla, "LootDef"):
        bid = _block_id(raw)
        if bid not in wanted:
            continue
        remapped, remap_hits = _remap_ammo(raw)
        for old, new in remap_hits:
            changes.append((bid, old, new))
        if bid in existing and LOOT_BEGIN not in items:
            continue
        body = _to_moditem(remapped, "LootDef", "ModItemLootDef")
        converted.append(_indent_block(body, 2))
        ids.append(bid)
    missing = [i for i in VENDOR_LOOT_IDS if i not in ids and i not in existing]
    if missing and LOOT_BEGIN not in items:
        raise RuntimeError(f"vanilla LootDef missing vendor ids: {missing}")
    folder = (
        LOOT_BEGIN
        + "\tPlaceObj('ModItemFolder', {\n"
        + "\t\t'name', \"Vendor Loot\",\n"
        + "\t\t'comment', \"Vanilla vendor LootDef overrides; live JAZZ_AMMO_*\",\n"
        + "\t}, {\n"
        + "\n".join(converted)
        + ("\n" if converted else "")
        + "\t}),\n"
        + LOOT_END
    )
    if LOOT_BEGIN in items:
        return _replace_marked(items, LOOT_BEGIN, LOOT_END, folder), ids, changes
    # Insert after Stall Banters folder (which now contains the marked dump).
    maps_anchor = "\tPlaceObj('ModItemFolder', {\n\t\t'name', \"Maps\","
    pos = items.find(maps_anchor)
    if pos < 0:
        raise RuntimeError("items.lua: Maps folder not found for Vendor Loot insert")
    return items[:pos] + folder + items[pos:], ids, changes


ERNIE_STALL_CUT_LOOT = (
    "Drop_762WP_HP",
    "Drop_12gauge_Varied_Legion",
)

ERNIE_STALL_LIVE_GRANTS = (
    ("Stall_Random_762WPrandom_Parts", "JAZZ_AMMO_762x39_FMJ"),
    ("Stall_Random_12Gauge", "JAZZ_AMMO_12gauge_Buckshot"),
)

UNIT_GRANT_LOOT_RE = re.compile(
    r"PlaceObj\('UnitGrantItem',\s*\{[^}]*LootTableId = \"([^\"]+)\"",
    re.S,
)


def audit_ernie_stall_grants(objects: str) -> list[str]:
    problems: list[str] = []
    for loot_id in UNIT_GRANT_LOOT_RE.findall(objects):
        if loot_id in ERNIE_STALL_CUT_LOOT:
            problems.append(f"ubRwFgf UnitGrantItem still uses {loot_id}")
    for stall_id, item_id in ERNIE_STALL_LIVE_GRANTS:
        if stall_id not in objects:
            problems.append(f"ubRwFgf missing stall {stall_id}")
            continue
        if f'ItemId = "{item_id}"' not in objects:
            problems.append(f"ubRwFgf stall {stall_id} missing grant {item_id}")
    return problems


def audit(items: str, objects: str | None = None) -> list[str]:
    problems: list[str] = []
    loot_ids = _existing_moditem_ids(items, "ModItemLootDef")
    for vid in VENDOR_LOOT_IDS:
        if vid not in loot_ids:
            problems.append(f"missing ModItemLootDef {vid}")
    # Vendor ammo tables must not still grant cut vanilla ammo.
    vendor_ammo_ids = {
        "Vendor_Ammo",
        "FleatownMarket_Ammo",
        "FosseNoire_Ammo",
        "PoacherCamp_Ammo",
    }
    for block in _extract_placeobjs(items, "ModItemLootDef"):
        bid = _block_id(block)
        if bid not in vendor_ammo_ids:
            continue
        for old in AMMO_REMAP:
            if f'item = "{old}"' in block:
                problems.append(f"{bid} still grants cut ammo {old}")
    if objects is not None:
        problems.extend(audit_ernie_stall_grants(objects))
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--maps", type=Path, default=DEFAULT_MAPS)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--audit-only", action="store_true")
    args = ap.parse_args()
    if args.audit_only:
        items = (args.maps / "items.lua").read_text(encoding="utf-8")
        objects_path = args.maps / "Maps" / "ubRwFgf" / "objects.lua"
        objects = objects_path.read_text(encoding="utf-8") if objects_path.is_file() else None
        if objects is None:
            print("AUDIT FAIL: Maps/ubRwFgf/objects.lua missing", file=sys.stderr)
            return 1
        problems = audit(items, objects)
        for p in problems:
            print(f"AUDIT FAIL: {p}", file=sys.stderr)
        if problems:
            return 1
        print("AUDIT OK")
        return 0
    maps = args.maps
    items_path = maps / "items.lua"
    meta_path = maps / "metadata.lua"
    if not items_path.is_file():
        print(f"FAIL: {items_path} missing", file=sys.stderr)
        return 1
    if not STALL_BANTERS_SRC.is_file() or not LOOTDEF_SRC.is_file():
        print(f"FAIL: vanilla dump missing ({STALL_BANTERS_SRC} / {LOOTDEF_SRC})", file=sys.stderr)
        return 1
    items = items_path.read_text(encoding="utf-8")
    meta = meta_path.read_text(encoding="utf-8")
    stall_src = STALL_BANTERS_SRC.read_text(encoding="utf-8")
    loot_src = LOOTDEF_SRC.read_text(encoding="utf-8")
    items2, stall_ids = build_stall_banters(items, stall_src)
    items3, loot_ids, changes = build_vendor_loot(items2, loot_src)
    meta2 = _insert_resources(meta, "BanterDef", stall_ids, "Banter", "Stall_Barter_762x39PS")
    if loot_ids:
        meta2 = _insert_resources(meta2, "LootDef", loot_ids, "LootDef", "IntelSecretStash")
    objects_path = maps / "Maps" / "ubRwFgf" / "objects.lua"
    objects = objects_path.read_text(encoding="utf-8") if objects_path.is_file() else None
    problems = audit(items3, objects)
    print(f"stall banters: {len(stall_ids)}")
    print(f"vendor loot: {len(loot_ids)}")
    print(f"ammo remaps: {len(changes)}")
    for bid, old, new in changes:
        print(f"  {bid}: {old} -> {new}")
    if problems:
        for p in problems:
            print(f"AUDIT FAIL: {p}", file=sys.stderr)
        if args.apply:
            print("refusing --apply with audit failures", file=sys.stderr)
            return 1
        return 1
    print("AUDIT OK")
    if not args.apply:
        print("dry-run (pass --apply to write)")
        return 0
    items_path.write_text(items3, encoding="utf-8", newline="\n")
    meta_path.write_text(meta2, encoding="utf-8", newline="\n")
    print(f"wrote {items_path}")
    print(f"wrote {meta_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
