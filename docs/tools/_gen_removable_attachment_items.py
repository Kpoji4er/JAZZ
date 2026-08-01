# -*- coding: utf-8 -*-
"""Generate per-component JAZZ_RemovableAttachment InventoryItems for editor spawn.

Canon: docs/design/weapon-repair-parts.md + JAZZ-WEAPONS-002 AC-002 catalog gap.
Each live remountable WeaponComponent gets InventoryItem Id == component id
(object_class JAZZ_RemovableAttachment, RemovableComponentId = id).

Usage:
  python docs/tools/_gen_removable_attachment_items.py           # dry-run
  python docs/tools/_gen_removable_attachment_items.py --apply
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _apply_attach_001 import placeobj_blocks, prop


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        backup = path.with_suffix(path.suffix + ".bak_removable_items")
        backup.write_bytes(path.read_bytes())
    path.write_text(content, encoding="utf-8", newline="\n")

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"
CSV = ROOT / "docs" / "technical" / "weapons" / "data" / "weapon-components.csv"
INV_DIR = ROOT / "InventoryItem"

REMOVABLE_SLOTS = {
    "Scope",
    "Muzzle",
    "Side",
    "Under",
    "Bipod",
    "Magazine",
    "GrenadeLauncher",
    "Grenadelauncher",  # CSV spelling variant
}

SKIP_IDS = {
    "JAZZ_Compensator_cosmetic",
    "JAZZ_DefMuzzle",
    "JAZZ_DefaultMuzzle_HK21",
    "JAZZ_M14_Default_Muzzle",
    "JAZZ_Galil_Handguard_Default",
    "JAZZ_AUGScope_Default",
    "JAZZ_FlashlightOff",
    "JAZZ_VerticalGripFld",
    "JAZZ_MagNormal",
    "MagNormal",
    "JAZZ_SuppressorIntegrated",
    "SuppressorIntegrated",
}

SKIP_SUBSTRINGS = ("Iron", "Ironsight", "SuppressorIntegrated")

FOLDER_MARKER_BEGIN = "-- JAZZ-WEAPONS-002-REMOVABLE-ITEMS-BEGIN"
FOLDER_MARKER_END = "-- JAZZ-WEAPONS-002-REMOVABLE-ITEMS-END"

LOC_BASE = 990002100  # reserved block for generated remountable item T-ids (RU/EN shared)


def slot_norm(slot: str) -> str:
    if slot.lower() == "grenadelauncher":
        return "GrenadeLauncher"
    return slot


def is_removable_row(row: dict) -> bool:
    cid = (row.get("id") or "").strip()
    if not cid.startswith("JAZZ_"):
        return False
    if (row.get("source") or "").strip() not in ("jazz", "working-tree", ""):
        # CSV uses source=jazz
        pass
    source = (row.get("source") or "").strip()
    if source and source not in ("jazz",):
        return False
    slot = slot_norm((row.get("slot") or "").strip())
    if slot not in REMOVABLE_SLOTS and slot_norm(slot) not in REMOVABLE_SLOTS:
        # allow CSV Slot column name variants
        if slot not in REMOVABLE_SLOTS:
            return False
    if cid in SKIP_IDS:
        return False
    for sub in SKIP_SUBSTRINGS:
        if sub in cid:
            return False
    return True


def load_csv_ids() -> list[dict]:
    rows: list[dict] = []
    with CSV.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            # normalize keys
            r = {k.strip(): (v or "").strip() for k, v in row.items()}
            # expect columns: id, name, slot, cost, ...
            if "id" not in r and "component_id" in r:
                r["id"] = r["component_id"]
            if not is_removable_row(r):
                continue
            rows.append(r)
    # dedupe by id
    seen = {}
    for r in rows:
        seen[r["id"]] = r
    return [seen[k] for k in sorted(seen)]


def load_component_presentation(items_text: str) -> dict[str, dict]:
    """id -> {display_t, icon, cost, slot} from ModItemWeaponComponent blocks."""
    out: dict[str, dict] = {}
    for block in placeobj_blocks(items_text, "ModItemWeaponComponent"):
        cid = prop(block.text, "id")
        if not cid or not cid.startswith("JAZZ_"):
            continue
        dn = re.search(
            r"DisplayName = (T\(\d+,\s*--\[\[[^\]]*\]\]\s*\"(?:\\.|[^\"\\])*\"\))",
            block.text,
        )
        icon_m = re.search(r'(?m)^\s*Icon = \"([^\"]+)\",', block.text)
        # prefer first Visuals Icon if present
        vis_icon = re.search(r"PlaceObj\('WeaponComponentVisual'[\s\S]*?Icon = \"([^\"]+)\"", block.text)
        cost_m = re.search(r"(?m)^\s*Cost = (-?\d+),", block.text)
        slot = prop(block.text, "Slot") or ""
        out[cid] = {
            "display_expr": dn.group(1) if dn else None,
            "icon": (vis_icon.group(1) if vis_icon else None)
            or (icon_m.group(1) if icon_m else "UI/Icons/Upgrades/parts_placeholder"),
            "cost": int(cost_m.group(1)) if cost_m else 0,
            "slot": slot,
        }
    return out


def escape_lua_str(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def is_lua_identifier(name: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name))


def companion_lua(cid: str, display_name: str, icon: str, cost: int, t_name: int, t_plural: int, t_hint: int) -> str:
    # Public ids must be Lua identifiers (`_` not `-`). Hyphen in DefineClass.Name
    # parses as subtraction → "syntax error near '-'".
    if not is_lua_identifier(cid):
        raise ValueError(f"companion id not a Lua identifier (use _ not -): {cid}")
    define_open = f"DefineClass.{cid} = {{"
    define_close = "}"
    return (
        f"UndefineClass('{cid}')\n"
        f"{define_open}\n"
        f"\t__parents = {{ \"JAZZ_RemovableAttachment\" }},\n"
        f"\t__generated_by_class = \"ModItemInventoryItemCompositeDef\",\n"
        f"\n"
        f"\tobject_class = \"JAZZ_RemovableAttachment\",\n"
        f"\tRepairable = false,\n"
        f"\tIcon = \"{escape_lua_str(icon)}\",\n"
        f"\tDisplayName = T({t_name}, --[[ModItemInventoryItemCompositeDef {cid} DisplayName]] \"{escape_lua_str(display_name)}\"),\n"
        f"\tDisplayNamePlural = T({t_plural}, --[[ModItemInventoryItemCompositeDef {cid} DisplayNamePlural]] \"{escape_lua_str(display_name)}\"),\n"
        f"\tAdditionalHint = T({t_hint}, --[[ModItemInventoryItemCompositeDef {cid} AdditionalHint]] \"Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации.\"),\n"
        f"\tCost = {max(0, cost) * 100 if cost and cost < 100 else max(0, cost)},\n"
        f"\tCanAppearInShop = true,\n"
        f"\tTier = 1,\n"
        f"\tMaxStock = 1,\n"
        f"\tRestockWeight = 10,\n"
        f"\tCategoryPair = \"Components\",\n"
        f"\tMaxStacks = 1,\n"
        f"\tRemovableComponentId = \"{cid}\",\n"
        f"{define_close}\n"
    )


def moditem_block(cid: str, display_name: str, icon: str, cost: int, t_name: int, t_plural: int, t_hint: int) -> str:
    # Shop Cost on MiscItem is often in money units; WeaponComponent.Cost is Parts.
    # Keep Parts-like number * 100 for rough money, matching legacy Compensator ~2900.
    money = max(0, cost) * 100 if cost else 0
    return (
        "\t\t\t\tPlaceObj('ModItemInventoryItemCompositeDef', {\n"
        f"\t\t\t\t\t'Group', \"RemovableAttachments\",\n"
        f"\t\t\t\t\t'Id', \"{cid}\",\n"
        f"\t\t\t\t\t'comment', \"WEAPONS-002 remountable → component {cid}\",\n"
        f"\t\t\t\t\t'object_class', \"JAZZ_RemovableAttachment\",\n"
        f"\t\t\t\t\t'Repairable', false,\n"
        f"\t\t\t\t\t'Icon', \"{escape_lua_str(icon)}\",\n"
        f"\t\t\t\t\t'DisplayName', T({t_name}, --[[ModItemInventoryItemCompositeDef {cid} DisplayName]] \"{escape_lua_str(display_name)}\"),\n"
        f"\t\t\t\t\t'DisplayNamePlural', T({t_plural}, --[[ModItemInventoryItemCompositeDef {cid} DisplayNamePlural]] \"{escape_lua_str(display_name)}\"),\n"
        f"\t\t\t\t\t'AdditionalHint', T({t_hint}, --[[ModItemInventoryItemCompositeDef {cid} AdditionalHint]] \"Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации.\"),\n"
        f"\t\t\t\t\t'Cost', {money},\n"
        f"\t\t\t\t\t'CanAppearInShop', true,\n"
        f"\t\t\t\t\t'Tier', 1,\n"
        f"\t\t\t\t\t'MaxStock', 1,\n"
        f"\t\t\t\t\t'RestockWeight', 10,\n"
        f"\t\t\t\t\t'CategoryPair', \"Components\",\n"
        f"\t\t\t\t\t'MaxStacks', 1,\n"
        f"\t\t\t\t\t'RemovableComponentId', \"{cid}\",\n"
        "\t\t\t\t}),\n"
    )


def folder_block(moditems: str) -> str:
    return (
        f"\t\t\t{FOLDER_MARKER_BEGIN}\n"
        "\t\t\tPlaceObj('ModItemFolder', {\n"
        "\t\t\t\t'name', \"RemovableAttachments\",\n"
        "\t\t\t}, {\n"
        f"{moditems}"
        "\t\t\t\t}),\n"
        f"\t\t\t{FOLDER_MARKER_END}\n"
    )


def patch_items_lua(text: str, folder: str) -> str:
    begin = text.find(FOLDER_MARKER_BEGIN)
    end = text.find(FOLDER_MARKER_END)
    if begin != -1 and end != -1:
        end = text.find("\n", end)
        if end == -1:
            end = len(text)
        else:
            end += 1
        # include leading tabs/newline before BEGIN
        line_start = text.rfind("\n", 0, begin) + 1
        return text[:line_start] + folder + text[end:]

    # Insert after Resources folder that contains JAZZ_RemovableAttachment
    anchor = "'Id', \"JAZZ_RemovableAttachment\""
    pos = text.find(anchor)
    if pos == -1:
        raise SystemExit("JAZZ_RemovableAttachment ModItem not found in items.lua")
    # Find closing of Resources folder: after RemovableAttachment's `}),` then `}),` of folder children
    # Simpler: insert right BEFORE the Resources folder closer that follows RemovableAttachment.
    # Locate the PlaceObj ModItemFolder Resources start, then find matching end after RemovableAttachment.
    res_folder = text.rfind("PlaceObj('ModItemFolder'", 0, pos)
    if res_folder == -1:
        raise SystemExit("Resources folder not found")
    # After RemovableAttachment block ends with `}),` then folder closes with `}),`
    after = text.find("}),", pos)
    if after == -1:
        raise SystemExit("cannot find end of RemovableAttachment")
    # skip this }), (item) and the next }), (folder children end)
    item_end = after + 3
    # next non-ws should be `}),` closing folder
    m = re.search(r"\n\t\t\t\t\}\),\n", text[item_end:])
    if not m:
        # try `}),` with three tabs
        m = re.search(r"\n\t\t\t\}\),\n", text[item_end:])
    if not m:
        raise SystemExit("cannot find Resources folder close after RemovableAttachment")
    insert_at = item_end + m.end()
    return text[:insert_at] + folder + text[insert_at:]


def patch_metadata(meta: str, ids: list[str]) -> str:
    # 1) code array: InventoryItem/<id>.lua after JAZZ_RemovableAttachment.lua
    code_anchor = '"InventoryItem/JAZZ_RemovableAttachment.lua",'
    if code_anchor not in meta:
        raise SystemExit("metadata.lua missing InventoryItem/JAZZ_RemovableAttachment.lua")
    # remove previous generated block if any
    meta = re.sub(
        r"\n\t\t-- JAZZ-WEAPONS-002-REMOVABLE-ITEMS-BEGIN\n.*?\n\t\t-- JAZZ-WEAPONS-002-REMOVABLE-ITEMS-END\n",
        "\n",
        meta,
        count=1,
        flags=re.S,
    )
    lines = [f'\t\t"InventoryItem/{cid}.lua",' for cid in ids]
    block = (
        "\n\t\t-- JAZZ-WEAPONS-002-REMOVABLE-ITEMS-BEGIN\n"
        + "\n".join(lines)
        + "\n\t\t-- JAZZ-WEAPONS-002-REMOVABLE-ITEMS-END\n"
    )
    meta = meta.replace(code_anchor, code_anchor + block, 1)

    # 2) items {} resources: Id entries near JAZZ_RemovableAttachment
    item_anchor = "'Id', \"JAZZ_RemovableAttachment\","
    if item_anchor not in meta:
        # try alternate formatting
        pass
    meta = re.sub(
        r"\n\t\t\t-- JAZZ-WEAPONS-002-REMOVABLE-ITEMS-BEGIN\n.*?\n\t\t\t-- JAZZ-WEAPONS-002-REMOVABLE-ITEMS-END\n",
        "\n",
        meta,
        count=1,
        flags=re.S,
    )
    # Find PlaceObj that contains JAZZ_RemovableAttachment Id and append siblings after that PlaceObj
    m = re.search(
        r"PlaceObj\('ModItemInventoryItemCompositeDef',\s*\{[^}]*'Id',\s*\"JAZZ_RemovableAttachment\"[^}]*\}\),",
        meta,
        flags=re.S,
    )
    if not m:
        # looser: line with Id then later }),
        idx = meta.find("'Id', \"JAZZ_RemovableAttachment\"")
        if idx == -1:
            raise SystemExit("metadata items entry for JAZZ_RemovableAttachment not found")
        end = meta.find("}),", idx)
        if end == -1:
            raise SystemExit("metadata items entry close not found")
        end += 3
    else:
        end = m.end()

    item_lines = []
    for cid in ids:
        item_lines.append(
            "\t\tPlaceObj('ModResourcePreset', {\n"
            '\t\t\t\'Class\', "InventoryItemCompositeDef",\n'
            f'\t\t\t\'Id\', "{cid}",\n'
            '\t\t\t\'ClassDisplayName\', "Inventory item",\n'
            "\t\t}),"
        )
    item_block = (
        "\n\t\t-- JAZZ-WEAPONS-002-REMOVABLE-ITEMS-BEGIN\n"
        + "\n".join(item_lines)
        + "\n\t\t-- JAZZ-WEAPONS-002-REMOVABLE-ITEMS-END"
    )
    meta = meta[:end] + item_block + meta[end:]
    return meta


def upsert_loc_csv(path: Path, rows: list[tuple[int, str, str]]) -> None:
    """Append missing T-ids to Russian.csv / English.csv (id,text)."""
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    existing = set(re.findall(r"(?m)^(\d+),", text))
    add = []
    for tid, _ru_or_en, val in rows:
        if str(tid) in existing:
            continue
        # CSV escape
        safe = '"' + val.replace('"', '""') + '"' if ("," in val or '"' in val or "\n" in val) else val
        add.append(f"{tid},{safe}")
    if not add:
        return
    if not text.endswith("\n"):
        text += "\n"
    write_text(path, text + "\n".join(add) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    # Fix CSV column names from actual file
    with CSV.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        raw_rows = list(reader)

    # Map flexible headers
    def norm_row(row: dict) -> dict:
        lower = { (k or "").strip().lower(): (v or "").strip() for k, v in row.items() }
        return {
            "id": lower.get("id") or lower.get("component_id") or "",
            "name": lower.get("display_name")
            or lower.get("name")
            or lower.get("component_name")
            or "",
            "slot": lower.get("slot") or lower.get("slot_type") or "",
            "cost": lower.get("cost") or "0",
            "source": lower.get("source") or lower.get("component_source") or "",
        }

    candidates = []
    for raw in raw_rows:
        r = norm_row(raw)
        if not r["id"].startswith("JAZZ_"):
            continue
        if r["source"] and r["source"] != "jazz":
            continue
        slot = slot_norm(r["slot"])
        if slot not in REMOVABLE_SLOTS:
            continue
        if r["id"] in SKIP_IDS:
            continue
        if any(sub in r["id"] for sub in SKIP_SUBSTRINGS):
            continue
        r["slot"] = slot
        candidates.append(r)

    by_id = {r["id"]: r for r in candidates}
    ids = sorted(by_id)

    items_text = ITEMS.read_text(encoding="utf-8")
    pres = load_component_presentation(items_text)

    # Drop ids that would collide with existing InventoryItem companions (except regenerating our own)
    existing_inv = {p.stem for p in INV_DIR.glob("*.lua")}
    # Allow overwrite of previously generated remountables; refuse weapons/ammo etc.
    forbidden = existing_inv - set(ids) - {"JAZZ_RemovableAttachment"}
    collide = [cid for cid in ids if cid in forbidden]
    # Also collision with non-removable inventory that shares name
    hard_collide = []
    for cid in ids:
        if cid in existing_inv and cid not in ids:
            hard_collide.append(cid)
        companion = INV_DIR / f"{cid}.lua"
        if companion.exists():
            body = companion.read_text(encoding="utf-8", errors="replace")
            if "JAZZ_RemovableAttachment" not in body and "RemovableComponentId" not in body:
                # existing non-removable item (e.g. weapon) — skip
                hard_collide.append(cid)
    if hard_collide:
        print("SKIP colliding InventoryItem ids:", ", ".join(hard_collide[:20]), f"... ({len(hard_collide)})")
        ids = [c for c in ids if c not in set(hard_collide)]

    print(f"remountable inventory items: {len(ids)}")
    for cid in ids[:8]:
        print(" ", cid, by_id[cid]["slot"], by_id[cid]["name"])
    if len(ids) > 8:
        print("  ...")

    if not args.apply:
        print("dry-run; pass --apply to write items.lua / metadata.lua / companions / loc")
        return 0

    moditem_parts = []
    loc_ru: list[tuple[int, str, str]] = []
    loc_en: list[tuple[int, str, str]] = []
    for i, cid in enumerate(ids):
        info = by_id[cid]
        p = pres.get(cid, {})
        display = info["name"] or cid
        icon = p.get("icon") or "UI/Icons/Upgrades/parts_placeholder"
        try:
            cost = int(p.get("cost") or info.get("cost") or 0)
        except ValueError:
            cost = 0
        t_name = LOC_BASE + i * 3
        t_plural = t_name + 1
        t_hint = t_name + 2
        # Prefer component DisplayName text from CSV name; EN = same for now (editor spawn)
        loc_ru.append((t_name, "ru", display))
        loc_ru.append((t_plural, "ru", display))
        loc_ru.append(
            (
                t_hint,
                "ru",
                "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации.",
            )
        )
        loc_en.append((t_name, "en", display))
        loc_en.append((t_plural, "en", display))
        loc_en.append(
            (
                t_hint,
                "en",
                "Removable module. Drag onto a compatible firearm or install in the weapon modification screen.",
            )
        )
        moditem_parts.append(moditem_block(cid, display, icon, cost, t_name, t_plural, t_hint))
        companion = companion_lua(cid, display, icon, cost, t_name, t_plural, t_hint)
        write_text(INV_DIR / f"{cid}.lua", companion)

    folder = folder_block("".join(moditem_parts))
    new_items = patch_items_lua(items_text, folder)
    write_text(ITEMS, new_items)

    meta = META.read_text(encoding="utf-8")
    write_text(META, patch_metadata(meta, ids))

    upsert_loc_csv(ROOT / "Russian.csv", loc_ru)
    upsert_loc_csv(ROOT / "English.csv", loc_en)

    strings = ROOT / "Localization" / "Strings.csv"
    if strings.exists():
        upsert_loc_csv(strings, loc_ru)

    print(f"applied {len(ids)} remountable InventoryItems")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
