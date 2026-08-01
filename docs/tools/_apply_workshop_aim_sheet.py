#!/usr/bin/env python3
"""Apply Otherguy workshop AIM merc sheet targets into jazz-units UnitData + loot.

Source tab gid=1773591798 («Наемники от Otherguy»). Sheet cells use
`current->target` arrows; this script applies the **target** side (and plain
numbers as targets). Personal perk *behavior* gaps are reported, not reinvented.

Usage (from jazz/):
  python docs/tools/_apply_workshop_aim_sheet.py [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
UNITS = JAZZ.parent / "jazz-units"
SNAPSHOT = JAZZ / "docs/design/mercs-ja12/_workshop_otherguy_sheet_targets.md"

# Sheet targets (right of ->, else listed value).
MERCS = {
    "Merc_JerrySinclair": {
        "stats": {
            "Health": 54,
            "Agility": 45,
            "Dexterity": 68,
            "Strength": 85,
            "Wisdom": 76,
            "Leadership": 40,
            "Marksmanship": 67,
            "Mechanical": 84,
            "Explosives": 50,
            "Medical": 8,
        },
        "starting_level": 1,
        "remove_starting_level": True,
        "specialization": "Mechanic",
        "perks": [
            "Merc_JerrySinclair_Perk",
            "MrFixit",
            "Claustrophobic",
            "Optimist",
        ],
        "tier": None,
        "loot_parent_comment": "Gear Jerry Sinclair (sheet 60/30/10)",
        "tiers": {
            "60": [
                ("inv", "ColtPeacemaker", 1),
                ("inv", "JAZZ_AMMO_357_FMJ", 6),
                ("inv", "Parts", 50),
                ("inv", "FineSteelPipe", 1),
                ("inv", "OpticalLens", 1),
            ],
            "30": [
                ("inv", "Parts", 100),
                ("inv", "FineSteelPipe", 2),
                ("inv", "OpticalLens", 4),
            ],
            "10": [
                ("inv", "Parts", 100),
                ("inv", "OpticalLens", 2),
                ("inv", "Microchip", 2),
            ],
        },
        "perk_gap": (
            "Sheet personal perk: repair items to 120% + buff +1 dmg/range/accuracy "
            "while >100% condition. Runtime still crafts 40mm-TB every 7 days "
            "(Merc_JerrySinclair_Perk)."
        ),
    },
    "Merc_MildredPatterson": {
        "stats": {
            "Health": 51,
            "Agility": 48,
            "Dexterity": 74,
            "Strength": 38,
            "Wisdom": 78,
            "Leadership": 50,
            "Marksmanship": 55,
            "Mechanical": 5,
            "Explosives": 2,
            "Medical": 90,
        },
        "starting_level": 1,
        "remove_starting_level": True,
        "specialization": "Doctor",
        "perks": [
            "Merc_MildredPatterson_Bookworm",
            "Teacher",
            "OldDog",
            "Optimist",
        ],
        "tier": None,
        "loot_parent_comment": "Gear Mildred Patterson (sheet 60/30/10)",
        "tiers": {
            "60": [
                ("inv", "HiPower", 1),
                ("inv", "JAZZ_AMMO_9x19_FMJ", 13),
                ("inv", "FirstAidKit", 1),
                ("loot", "Merc_MildredPatterson_SkillMag"),
            ],
            "30": [
                ("inv", "FirstAidKit", 1),
                ("loot", "Merc_MildredPatterson_SkillMag"),
            ],
            "10": [
                ("inv", "Medkit", 1),
                ("loot", "Merc_MildredPatterson_SkillMag"),
            ],
        },
        "extra_loot_defs": {
            "Merc_MildredPatterson_SkillMag": {
                "comment": "Random skill magazine for Mildred starting gear",
                "mode": "first",
                "entries": [
                    ("inv_w", "SkillMag_Health", 1, 10000),
                    ("inv_w", "SkillMag_Agility", 1, 10000),
                    ("inv_w", "SkillMag_Dexterity", 1, 10000),
                    ("inv_w", "SkillMag_Strength", 1, 10000),
                    ("inv_w", "SkillMag_Wisdom", 1, 10000),
                    ("inv_w", "SkillMag_Leadership", 1, 10000),
                    ("inv_w", "SkillMag_Marksmanship", 1, 10000),
                    ("inv_w", "SkillMag_Mechanical", 1, 10000),
                    ("inv_w", "SkillMag_Explosives", 1, 10000),
                    ("inv_w", "SkillMag_Medical", 1, 10000),
                ],
            }
        },
        "notes": [
            "Sheet «Аптечка»→FirstAidKit; «Большая аптечка»→Medkit.",
        ],
        "perk_gap": None,
    },
    "Merc_SamuelNkosi": {
        "stats": {
            "Health": 89,
            "Agility": 78,
            "Dexterity": 62,
            "Strength": 86,
            "Wisdom": 74,
            "Leadership": 14,
            "Marksmanship": 76,
            "Mechanical": 18,
            "Explosives": 21,
            "Medical": 13,
        },
        "starting_level": 1,
        "remove_starting_level": True,
        "specialization": "HeavyWeapons",
        "perks": [
            "Merc_SamuelNkosi_Perk",
            "HeavyWeaponsTraining",
            "AutoWeapons",
        ],
        "tier": None,
        "loot_parent_comment": "Gear Samuel Nkosi (sheet 60/30/10)",
        "tiers": {
            "60": [
                ("inv", "Galil", 1),
                ("inv", "JAZZ_AMMO_762x51_FMJ", 120),
            ],
            "30": [
                ("inv", "HiPower", 1),
                ("inv", "JAZZ_AMMO_9x19_FMJ", 65),
            ],
            "10": [
                ("inv", "Sterling", 1),
                ("inv", "JAZZ_AMMO_9x19_FMJ", 90),
            ],
        },
        "perk_gap": (
            "Sheet personal perk: heavy MGs not bulky for Samuel. Runtime perk "
            "still uses prior OnKill/overwatch-style workshop behavior — verify "
            "Merc_SamuelNkosi_Perk vs sheet."
        ),
    },
    "Merc_AnnieDubois": {
        "stats": {
            "Health": 81,
            "Agility": 74,
            "Dexterity": 86,
            "Strength": 53,
            "Wisdom": 79,
            "Leadership": 16,
            "Marksmanship": 82,
            "Mechanical": 5,
            "Explosives": 4,
            "Medical": 39,
        },
        "starting_level": 1,
        "remove_starting_level": True,
        "specialization": "Marksmen",
        "perks": [
            "Merc_AnnieDubois_Perk",
            "NightOps",
            "Deadeye",
        ],
        "tier": None,
        "loot_parent_comment": "Gear Annie Dubois (sheet 60/30/10)",
        "tiers": {
            "60": [
                ("upg", "M21", ["JAZZ_Scope_6x"]),
                ("inv", "JAZZ_AMMO_762x51_FMJ", 40),
            ],
            "30": [
                ("inv", "HiPower", 1),
                ("inv", "JAZZ_AMMO_9x19_FMJ", 26),
            ],
            "10": [
                ("upg", "M21", ["JAZZ_Reflex_Closed"]),
                ("inv", "JAZZ_AMMO_762x51_FMJ", 20),
            ],
        },
        "notes": [
            "Sheet note «L43 would suit her» left for owner (not applied).",
            "Ammo counts not on sheet — used 40 / 26 / 20 FMJ as reasonable starters.",
        ],
        "perk_gap": (
            "Sheet personal perk: 2 sniper headshots (replacing Inspired-on-kill). "
            "Runtime Merc_AnnieDubois_Perk still grants Inspired on kill."
        ),
    },
    "Merc_HectorSanchez": {
        "stats": {
            "Health": 75,
            "Agility": 68,
            "Dexterity": 70,
            "Strength": 83,
            "Wisdom": 62,
            "Leadership": 70,
            "Marksmanship": 74,
            "Mechanical": 14,
            "Explosives": 28,
            "Medical": 5,
        },
        "starting_level": 1,
        "remove_starting_level": True,
        "specialization": "Leader",
        "perks": [
            "Merc_HectorSanchez_Perk",
            "Teacher",
            "Psycho",
        ],
        "tier": None,
        "loot_parent_comment": "Gear Hector Sanchez (sheet 60/30/10)",
        "tiers": {
            "60": [
                ("upg", "PPSH", ["JAZZ_MagDrum_35_71"]),
                ("inv", "JAZZ_AMMO_762x25_FMJ", 142),
            ],
            "30": [
                ("inv", "Type56", 1),
                ("inv", "JAZZ_AMMO_762x39_FMJ", 60),
            ],
            "10": [
                ("upg", "M21", ["JAZZ_Reflex_Closed"]),
                ("inv", "JAZZ_AMMO_762x51_FMJ", 20),
            ],
        },
        "notes": [
            "Ammo counts not fully on sheet for Type56/M21 — used 60 / 20 FMJ.",
        ],
        "perk_gap": (
            "Sheet personal perk: 10%*level chance to train militia +2 tiers. "
            "Runtime Merc_HectorSanchez_Perk may still use older militia-efficiency "
            "workshop wording — verify behavior."
        ),
    },
    "Merc_CarolThompson": {
        "stats": {
            "Health": 76,
            "Agility": 82,
            "Dexterity": 70,
            "Strength": 61,
            "Wisdom": 83,
            "Leadership": 12,
            "Marksmanship": 76,
            "Mechanical": 89,
            "Explosives": 25,
            "Medical": 13,
        },
        "starting_level": 1,
        "remove_starting_level": True,
        "specialization": "Mechanic",
        "perks": [
            "Merc_CarolThompson_Perk",
            "AutoWeapons",
            "MrFixit",
            "Flanker",
            "RelentlessAdvance",
        ],
        "tier": "Rookie",
        "loot_parent_comment": "Gear Carol Thompson (sheet 60/30/10)",
        "tiers": {
            "60": [
                ("inv", "Sterling", 1),
                ("inv", "JAZZ_AMMO_9x19_FMJ", 90),
                ("inv", "Merc_CarolThompson_Item", 1),
            ],
            "30": [
                ("inv", "Winchester1894", 1),
                ("inv", "JAZZ_AMMO_44CAL_FMJ", 28),
                ("inv", "Merc_CarolThompson_Item", 1),
            ],
            "10": [
                ("inv", "HiPower", 1),
                ("inv", "JAZZ_AMMO_9x19_FMJ", 26),
                ("inv", "Merc_CarolThompson_Item", 1),
            ],
        },
        "notes": [
            "Dropped FlakVest from prior loot (not on sheet presets).",
            "Ammo for Winchester/HiPower not on sheet — used 28 / 26.",
            "Tier Veteran→Rookie with level 1.",
        ],
        "perk_gap": (
            "Sheet personal perk: chance to bring Parts/pipes/lens/chip on ops; "
            "toolbox lockpick. Runtime Merc_CarolThompson_Perk still auto-repairs "
            "equipped gear hourly — verify vs sheet scrap-find rates."
        ),
    },
}


def fmt_inv(item: str, n: int, indent: str = "\t") -> str:
    return (
        f"{indent}PlaceObj('LootEntryInventoryItem', {{\n"
        f"{indent}\tguaranteed = true,\n"
        f"{indent}\titem = \"{item}\",\n"
        f"{indent}\tstack_max = {n},\n"
        f"{indent}\tstack_min = {n},\n"
        f"{indent}}}),\n"
    )


def fmt_inv_w(item: str, n: int, weight: int, indent: str = "\t") -> str:
    return (
        f"{indent}PlaceObj('LootEntryInventoryItem', {{\n"
        f"{indent}\titem = \"{item}\",\n"
        f"{indent}\tstack_max = {n},\n"
        f"{indent}\tstack_min = {n},\n"
        f"{indent}\tweight = {weight},\n"
        f"{indent}}}),\n"
    )


def fmt_upg(weapon: str, upgrades: list[str], indent: str = "\t") -> str:
    ups = ",\n".join(f'{indent}\t\t"{u}"' for u in upgrades)
    return (
        f"{indent}PlaceObj('LootEntryUpgradedWeapon', {{\n"
        f"{indent}\tupgrades = {{\n{ups},\n"
        f"{indent}\t}},\n"
        f"{indent}\tweapon = \"{weapon}\",\n"
        f"{indent}}}),\n"
    )


def fmt_loot_ref(loot_def: str, indent: str = "\t") -> str:
    return (
        f"{indent}PlaceObj('LootEntryLootDef', {{\n"
        f"{indent}\tloot_def = \"{loot_def}\",\n"
        f"{indent}}}),\n"
    )


def entries_to_lua(entries: list, indent: str = "\t") -> str:
    out = []
    for e in entries:
        kind = e[0]
        if kind == "inv":
            out.append(fmt_inv(e[1], e[2], indent))
        elif kind == "inv_w":
            out.append(fmt_inv_w(e[1], e[2], e[3], indent))
        elif kind == "upg":
            out.append(fmt_upg(e[1], e[2], indent))
        elif kind == "loot":
            out.append(fmt_loot_ref(e[1], indent))
        else:
            raise ValueError(e)
    return "".join(out)


def build_loot_block(merc_id: str, cfg: dict) -> str:
    parts = []
    # parent weighted
    parts.append(
        "PlaceObj('ModItemLootDef', {\n"
        f"\tcomment = \"{cfg['loot_parent_comment']}\",\n"
        f"\tid = \"{merc_id}\",\n"
        "\tPlaceObj('LootEntryLootDef', {\n"
        f"\t\tloot_def = \"{merc_id}60\",\n"
        "\t\tweight = 60000,\n"
        "\t}),\n"
        "\tPlaceObj('LootEntryLootDef', {\n"
        f"\t\tloot_def = \"{merc_id}30\",\n"
        "\t\tweight = 30000,\n"
        "\t}),\n"
        "\tPlaceObj('LootEntryLootDef', {\n"
        f"\t\tloot_def = \"{merc_id}10\",\n"
        "\t\tweight = 10000,\n"
        "\t}),\n"
        "}),\n"
    )
    for suffix, entries in cfg["tiers"].items():
        parts.append(
            "PlaceObj('ModItemLootDef', {\n"
            f"\tcomment = \"{merc_id} preset {suffix}%\",\n"
            f"\tid = \"{merc_id}{suffix}\",\n"
            "\tloot = \"all\",\n"
            f"{entries_to_lua(entries)}"
            "}),\n"
        )
    for eid, edef in (cfg.get("extra_loot_defs") or {}).items():
        mode = edef.get("mode", "all")
        parts.append(
            "PlaceObj('ModItemLootDef', {\n"
            f"\tcomment = \"{edef['comment']}\",\n"
            f"\tid = \"{eid}\",\n"
        )
        if mode == "all":
            parts.append("\tloot = \"all\",\n")
        parts.append(f"{entries_to_lua(edef['entries'])}}}),\n")
    return "".join(parts)


def _brace_end(text: str, brace_open: int) -> int | None:
    """End index after PlaceObj('ModItemLootDef', { ... }), including ) and trailing comma."""
    depth = 0
    i = brace_open
    while i < len(text):
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                # PlaceObj( 'ModItemLootDef', { ... } )
                if end < len(text) and text[end] == ")":
                    end += 1
                if end < len(text) and text[end] == ",":
                    end += 1
                while end < len(text) and text[end] in "\r\n":
                    end += 1
                return end
        i += 1
    return None


def _find_moditem_lootdef(text: str, loot_id: str) -> tuple[int, int] | None:
    """Return [start, end) of PlaceObj('ModItemLootDef' with exact id — not Appearance/UnitData."""
    id_re = re.compile(rf'\bid\s*=\s*"{re.escape(loot_id)}"\s*,')
    pos = 0
    while True:
        start = text.find("PlaceObj('ModItemLootDef'", pos)
        if start < 0:
            return None
        brace_open = text.find("{", start)
        if brace_open < 0:
            return None
        end = _brace_end(text, brace_open)
        if end is None:
            return None
        if id_re.search(text, start, end):
            return start, end
        pos = start + 1


def _remove_lootdef(text: str, loot_id: str) -> tuple[str, int]:
    n = 0
    while True:
        span = _find_moditem_lootdef(text, loot_id)
        if not span:
            return text, n
        a, b = span
        text = text[:a] + text[b:]
        n += 1


def replace_loot(text: str) -> tuple[str, list[str]]:
    logs = []
    for merc_id, cfg in MERCS.items():
        for extra_id in list(cfg.get("extra_loot_defs", {})) + [
            f"{merc_id}60",
            f"{merc_id}30",
            f"{merc_id}10",
        ]:
            text, n = _remove_lootdef(text, extra_id)
            if n:
                logs.append(f"removed prior loot {extra_id} x{n}")

        span = _find_moditem_lootdef(text, merc_id)
        if not span:
            raise RuntimeError(f"loot replace failed for {merc_id}: parent not found")
        a, b = span
        block = build_loot_block(merc_id, cfg).rstrip() + "\n"
        text = text[:a] + block + text[b:]
        logs.append(f"replaced loot {merc_id} + tiers")
    # Clean leftover PlaceObj closers from prior bad brace matches inside folders.
    text, n = re.subn(
        r"\}\),\r?\n\),\r?\nPlaceObj\('ModItemUnitDataCompositeDef'",
        "}),\nPlaceObj('ModItemUnitDataCompositeDef'",
        text,
    )
    if n:
        logs.append(f"stripped leftover ), before UnitData x{n}")
    return text, logs


def patch_unitdata_lua(path: Path, merc_id: str, cfg: dict, dry: bool) -> list[str]:
    logs = []
    text = path.read_text(encoding="utf-8")
    orig = text

    for k, v in cfg["stats"].items():
        text2, n = re.subn(
            rf"^(\s*{k}\s*=\s*)\d+",
            rf"\g<1>{v}",
            text,
            count=1,
            flags=re.M,
        )
        if n != 1:
            # Carol uses weird indentation with tabs inside
            text2, n = re.subn(
                rf"({k}\s*=\s*)\d+",
                rf"\g<1>{v}",
                text,
                count=1,
            )
        if n != 1:
            raise RuntimeError(f"{path.name}: failed to set {k}")
        text = text2

    # StartingPerks
    perks_body = ",\n\t\t".join(f'"{p}"' for p in cfg["perks"])
    # Detect indent of StartingPerks block
    m = re.search(r"^([ \t]*)StartingPerks\s*=\s*\{", text, re.M)
    if not m:
        raise RuntimeError(f"{path.name}: StartingPerks not found")
    ind = m.group(1)
    inner = ind + "\t"
    perks_lua = (
        f"{ind}StartingPerks = {{\n"
        + "".join(f'{inner}"{p}",\n' for p in cfg["perks"])
        + f"{ind}}}"
    )
    text2, n = re.subn(
        r"^[ \t]*StartingPerks\s*=\s*\{.*?\n[ \t]*\}",
        perks_lua,
        text,
        count=1,
        flags=re.M | re.S,
    )
    if n != 1:
        raise RuntimeError(f"{path.name}: StartingPerks replace failed")
    text = text2

    # Specialization
    text2, n = re.subn(
        r"(Specialization\s*=\s*)\"[^\"]+\"",
        rf'\g<1>"{cfg["specialization"]}"',
        text,
        count=1,
    )
    if n != 1:
        raise RuntimeError(f"{path.name}: Specialization replace failed")
    text = text2

    # StartingLevel
    if cfg.get("remove_starting_level"):
        text2, n = re.subn(
            r"^[ \t]*StartingLevel\s*=\s*\d+,\n",
            "",
            text,
            count=1,
            flags=re.M,
        )
        if n:
            logs.append(f"{merc_id}: removed StartingLevel")
        text = text2
    elif "starting_level" in cfg:
        if re.search(r"StartingLevel\s*=", text):
            text, n = re.subn(
                r"(StartingLevel\s*=\s*)\d+",
                rf'\g<1>{cfg["starting_level"]}',
                text,
                count=1,
            )
        else:
            # insert before Likes or StartingPerks
            text, n = re.subn(
                r"(^[ \t]*StartingPerks\s*=)",
                f"\tStartingLevel = {cfg['starting_level']},\n\\1",
                text,
                count=1,
                flags=re.M,
            )
        logs.append(f"{merc_id}: StartingLevel={cfg['starting_level']}")

    # Tier
    if cfg.get("tier") is None:
        text2, n = re.subn(r"^[ \t]*Tier\s*=\s*\"[^\"]+\",\n", "", text, count=1, flags=re.M)
        if n:
            logs.append(f"{merc_id}: removed Tier")
        text = text2
    else:
        if re.search(r"Tier\s*=", text):
            text, _ = re.subn(
                r"(Tier\s*=\s*)\"[^\"]+\"",
                rf'\g<1>"{cfg["tier"]}"',
                text,
                count=1,
            )
        else:
            text, _ = re.subn(
                r"(Specialization\s*=)",
                f'\tTier = "{cfg["tier"]}",\n\\1',
                text,
                count=1,
            )
        logs.append(f"{merc_id}: Tier={cfg['tier']}")

    if text != orig:
        logs.append(f"{merc_id}: companion UnitData updated")
        if not dry:
            path.write_text(text, encoding="utf-8")
    else:
        logs.append(f"{merc_id}: companion unchanged")
    return logs


def patch_unitdata_items(text: str, merc_id: str, cfg: dict) -> tuple[str, list[str]]:
    logs = []
    # Find ModItemUnitDataCompositeDef by Id
    m = re.search(
        rf"PlaceObj\('ModItemUnitDataCompositeDef',\s*\{{"
        rf"(?:(?!PlaceObj\('ModItemUnitDataCompositeDef').)*?"
        rf"'Id',\s*\"{re.escape(merc_id)}\"",
        text,
        re.S,
    )
    if not m:
        raise RuntimeError(f"items UnitData not found: {merc_id}")
    start = m.start()
    # End at DaysUntilOnline line closing of this object — find matching close after start
    # Heuristic: next PlaceObj('ModItemVoiceResponse' or folder close after DaysUntilOnline
    m_end = re.search(
        r"'DaysUntilOnline',\s*3,\s*\n\s*\}\),",
        text[start:],
    )
    if not m_end:
        raise RuntimeError(f"items UnitData end not found: {merc_id}")
    end = start + m_end.end()
    block = text[start:end]
    orig_block = block

    for k, v in cfg["stats"].items():
        block2, n = re.subn(rf"('{k}',\s*)\d+", rf"\g<1>{v}", block, count=1)
        if n != 1:
            raise RuntimeError(f"items {merc_id}: failed {k}")
        block = block2

    perks_inner = "".join(f'\t\t"{p}",\n' for p in cfg["perks"])
    # preserve quote style of StartingPerks key
    block2, n = re.subn(
        r"'StartingPerks',\s*\{.*?\n\s*\}",
        "'StartingPerks', {\n" + perks_inner + "\t}",
        block,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise RuntimeError(f"items {merc_id}: StartingPerks failed")
    block = block2

    block2, n = re.subn(
        r"('Specialization',\s*)\"[^\"]+\"",
        rf'\g<1>"{cfg["specialization"]}"',
        block,
        count=1,
    )
    if n != 1:
        raise RuntimeError(f"items {merc_id}: Specialization failed")
    block = block2

    if cfg.get("remove_starting_level"):
        block2, n = re.subn(r"\t*'StartingLevel',\s*\d+,\n", "", block, count=1)
        block = block2
        if n:
            logs.append(f"items {merc_id}: removed StartingLevel")
    elif "starting_level" in cfg:
        if "'StartingLevel'" in block:
            block, _ = re.subn(
                r"('StartingLevel',\s*)\d+",
                rf'\g<1>{cfg["starting_level"]}',
                block,
                count=1,
            )
        else:
            block, _ = re.subn(
                r"('StartingPerks',)",
                f"\t'StartingLevel', {cfg['starting_level']},\n\\1",
                block,
                count=1,
            )

    if cfg.get("tier") is None:
        block2, n = re.subn(r"\t*'Tier',\s*\"[^\"]+\",\n", "", block, count=1)
        block = block2
    else:
        if "'Tier'" in block:
            block, _ = re.subn(
                r"('Tier',\s*)\"[^\"]+\"",
                rf'\g<1>"{cfg["tier"]}"',
                block,
                count=1,
            )
        else:
            block, _ = re.subn(
                r"('Specialization',)",
                f"\t'Tier', \"{cfg['tier']}\",\n\\1",
                block,
                count=1,
            )

    if block != orig_block:
        logs.append(f"items {merc_id}: UnitData ModItem updated")
    text = text[:start] + block + text[end:]
    return text, logs


def patch_metadata(text: str, dry: bool) -> tuple[str, list[str]]:
    logs = []
    needed = []
    for merc_id, cfg in MERCS.items():
        for suffix in ("60", "30", "10"):
            needed.append(f"{merc_id}{suffix}")
        needed.extend(cfg.get("extra_loot_defs", {}).keys())
    insert_after = None
    for nid in needed:
        if re.search(rf"'Id',\s*\"{re.escape(nid)}\"", text):
            continue
        insert_after = nid
        entry = (
            "\t\tPlaceObj('ModResourcePreset', {\n"
            "\t\t\t'Class', \"LootDef\",\n"
            f"\t\t\t'Id', \"{nid}\",\n"
            "\t\t\t'ClassDisplayName', \"Loot definition\",\n"
            "\t\t}),\n"
        )
        # Insert after Merc_SamuelNkosi UnitData resource block cluster — before VoiceResponse Annie
        anchor = (
            "\t\tPlaceObj('ModResourcePreset', {\n"
            "\t\t\t'Class', \"UnitDataCompositeDef\",\n"
            "\t\t\t'Id', \"Merc_SamuelNkosi\",\n"
            "\t\t\t'ClassDisplayName', \"Unit\",\n"
            "\t\t}),\n"
        )
        if anchor not in text:
            raise RuntimeError("metadata anchor Merc_SamuelNkosi missing")
        # accumulate inserts then one replace
        text = text.replace(anchor, anchor + entry, 1)
        logs.append(f"metadata: added LootDef {nid}")
    return text, logs


def write_snapshot() -> None:
    lines = [
        "# Workshop Otherguy AIM — sheet targets applied",
        "",
        "Source: [Google Sheet gid=1773591798](https://docs.google.com/spreadsheets/d/19Je4n5Ju4cYmTLimzw45aFq_Ll8Wxz21RLIETFRsH2g/edit?gid=1773591798#gid=1773591798)",
        "",
        "Parser: `docs/tools/_apply_workshop_aim_sheet.py` (applies **right-hand** of `current->target` arrows).",
        "",
    ]
    for merc_id, cfg in MERCS.items():
        lines.append(f"## {merc_id}")
        lines.append("")
        lines.append("| Stat | Value |")
        lines.append("| --- | ---: |")
        for k, v in cfg["stats"].items():
            lines.append(f"| {k} | {v} |")
        lines.append("")
        lines.append(f"- Specialization: `{cfg['specialization']}`")
        lines.append(f"- StartingLevel: `{cfg['starting_level']}` (field omitted when 1)")
        if cfg.get("tier"):
            lines.append(f"- Tier: `{cfg['tier']}`")
        lines.append("- StartingPerks: " + ", ".join(f"`{p}`" for p in cfg["perks"]))
        lines.append("- Gear presets 60/30/10:")
        for suf, entries in cfg["tiers"].items():
            desc = []
            for e in entries:
                if e[0] == "inv":
                    desc.append(f"{e[1]}×{e[2]}")
                elif e[0] == "upg":
                    desc.append(f"{e[1]}+{'/'.join(e[2])}")
                elif e[0] == "loot":
                    desc.append(f"loot:{e[1]}")
            lines.append(f"  - {suf}%: " + ", ".join(desc))
        if cfg.get("perk_gap"):
            lines.append(f"- Perk gap: {cfg['perk_gap']}")
        for n in cfg.get("notes") or []:
            lines.append(f"- Note: {n}")
        lines.append("")
    SNAPSHOT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not UNITS.is_dir():
        print("jazz-units not found:", UNITS, file=sys.stderr)
        return 1

    items_path = UNITS / "items.lua"
    meta_path = UNITS / "metadata.lua"
    items = items_path.read_text(encoding="utf-8")
    meta = meta_path.read_text(encoding="utf-8")
    all_logs: list[str] = []

    items, logs = replace_loot(items)
    all_logs.extend(logs)

    for merc_id, cfg in MERCS.items():
        companion = UNITS / "UnitData" / f"{merc_id}.lua"
        all_logs.extend(patch_unitdata_lua(companion, merc_id, cfg, args.dry_run))
        items, logs = patch_unitdata_items(items, merc_id, cfg)
        all_logs.extend(logs)

    meta, logs = patch_metadata(meta, args.dry_run)
    all_logs.extend(logs)

    if not args.dry_run:
        items_path.write_text(items, encoding="utf-8")
        meta_path.write_text(meta, encoding="utf-8")
        write_snapshot()
        # README line
        readme = JAZZ / "docs/design/mercs-ja12/README.md"
        tip = (
            "- Workshop Otherguy sheet apply: "
            "[`_workshop_otherguy_sheet_targets.md`](_workshop_otherguy_sheet_targets.md) "
            "+ `docs/tools/_apply_workshop_aim_sheet.py`.\n"
        )
        rtxt = readme.read_text(encoding="utf-8")
        if "_workshop_otherguy_sheet_targets.md" not in rtxt:
            rtxt = rtxt.replace(
                "## Workshop AIM (imported, stubs)\n",
                "## Workshop AIM (imported, stubs)\n\n" + tip,
                1,
            )
            readme.write_text(rtxt, encoding="utf-8")
        tools_readme = JAZZ / "docs/tools/README.md"
        tr = tools_readme.read_text(encoding="utf-8")
        if "_apply_workshop_aim_sheet.py" not in tr:
            tr = tr.rstrip() + (
                "\n\n| `_apply_workshop_aim_sheet.py` | Apply Otherguy workshop AIM sheet "
                "targets (stats/perks/60-30-10 loot) into `jazz-units` UnitData+items+metadata. "
                "`--dry-run` supported. Snapshot: `docs/design/mercs-ja12/_workshop_otherguy_sheet_targets.md`. |\n"
            )
            tools_readme.write_text(tr, encoding="utf-8")

    for line in all_logs:
        print(line)
    print("dry-run" if args.dry_run else "applied", "OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
