# JAZZ-WEAPON-RAIL-001: slots, paid mount components, mount-mesh move, FAL merge.
# Idempotent. Run from the jazz repo: python docs/tools/_apply_weapon_rails.py
from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
COMPANION = ROOT / "InventoryItem"
UNITS = ROOT.parent / "jazz-units" / "items.lua"
MARKER_BEGIN = "-- JAZZ-WEAPON-RAIL-001 components begin"
MARKER_END = "-- JAZZ-WEAPON-RAIL-001 components end"

WESTERN = [
    "JAZZ_Reflex_Aimpoint5000",
    "JAZZ_Reflex_M68",
    "JAZZ_Reflex_Eotech",
    "JAZZ_Reflex_Closed",
    "JAZZ_Reflex_Open",
    "JAZZ_CombatScope_ACOG",
    "JAZZ_CombatScope_2x",
    "JAZZ_Scope_12x",
    "JAZZ_Scope_6x",
    "JAZZ_Scope_Scout",
    "JAZZ_NightScope",
]

# class -> list of (slot, component, is_default)
SLOTS: dict[str, list[tuple[str, str, bool]]] = {
    "AKM": [("Dovetail", "JAZZ_Dovetail_AK", False), ("Rail", "JAZZ_Rail_NATO_AK", False)],
    "AK74": [("Dovetail", "JAZZ_Dovetail_AK", False)],
    "AK74M": [("Rail", "JAZZ_Rail_NATO_AK", False)],
    "AK105": [("Rail", "JAZZ_Rail_NATO_AK", False)],
    "AEK971": [("Dovetail", "JAZZ_Dovetail_AK", False), ("Rail", "JAZZ_Rail_NATO_AK", False)],
    "AKSU": [("Dovetail", "JAZZ_Dovetail_AKSU", False)],
    "DragunovSVD": [("Dovetail", "JAZZ_Dovetail_SVD", True), ("Rail", "JAZZ_Rail_NATO_SVD", False)],
    "AS_Val": [("Dovetail", "JAZZ_Dovetail_Val", False), ("Rail", "JAZZ_Rail_NATO_Val", False)],
    "VSS": [("Dovetail", "JAZZ_Dovetail_Val", False), ("Rail", "JAZZ_Rail_NATO_Val", False)],
    "PP19Bizon": [("Dovetail", "JAZZ_Dovetail_AK", False)],
    "AR10": [("Rail", "JAZZ_Rail_AR", False)],
    "CAR15": [("Rail", "JAZZ_Rail_AR", False)],
    "M16A1": [("Rail", "JAZZ_Rail_AR", False)],
    "M16A2": [("Rail", "JAZZ_Rail_M16A2", False), ("RailSide", "JAZZ_Rail_M16A2_Side", False)],
    "AUG": [("Rail", "JAZZ_Rail_AUG", False), ("RailSide", "JAZZ_Rail_AUG_Side", False)],
    "FAMAS": [("Rail", "JAZZ_Rail_FAMAS", False)],
    "FNFAL": [("Rail", "JAZZ_Rail_FAL", False)],
    "G3A3": [("Rail", "JAZZ_Rail_G3", False)],
    "G3A4": [("Rail", "JAZZ_Rail_G3", False)],
    "G3SniperV1": [("Rail", "JAZZ_Rail_G3", True)],
    "G36": [("Rail", "JAZZ_Rail_G36", False)],
    "HK21": [("Rail", "JAZZ_Rail_HK21", False)],
    "HK33": [("Rail", "JAZZ_Rail_HK33", False)],
    "Galil": [("Rail", "JAZZ_Rail_Galil", False)],
    "M24Sniper": [("Rail", "JAZZ_Rail_M24", True)],
    "Winchester1894": [("Rail", "JAZZ_Rail_Winchester", False)],
    "AA12": [("Rail", "JAZZ_Rail_AA12", False)],
    "Ithaca": [("Rail", "JAZZ_Rail_Ithaca", False)],
    "R870": [("Rail", "JAZZ_Rail_R870", False)],
    "UMP45": [("Rail", "JAZZ_Rail_UMP", False)],
    "MP5K": [("Rail", "JAZZ_Rail_MP5K", False)],
    "UZI": [("Rail", "JAZZ_Rail_UZI", False)],
    "MicroUZI": [("Rail", "JAZZ_Rail_MicroUZI", False)],
    "M14SAW": [("Rail", "JAZZ_Rail_M14", False)],
    "M21": [("Rail", "JAZZ_Rail_M21", True)],
    "JAZZ_M14_MkIII": [("Rail", "JAZZ_Rail_MkIII", True)],
    "M1A": [("Rail", "JAZZ_Rail_M1A", False)],
    "M4Commando": [("Rail", "JAZZ_Rail_Commando", False)],
    "PSG1": [("Rail", "JAZZ_Rail_PSG", False)],
    "Bereta92": [("Rail", "JAZZ_Rail_Beretta", False)],
    "CZ52": [("Rail", "JAZZ_Rail_PistolUnder", False)],
    "MAC1950": [("Rail", "JAZZ_Rail_PistolUnder", False)],
    "P220": [("Rail", "JAZZ_Rail_P220", False)],
    "ColtAnaconda": [("Rail", "JAZZ_Rail_Anaconda", False)],
    "Mosin": [("Conversion", "JAZZ_Conversion_Mosin", False)],
    "SVT40": [("Conversion", "JAZZ_Conversion_SVT", False)],
    "G43": [("Conversion", "JAZZ_Conversion_G43", False)],
    "Springfield": [("Conversion", "JAZZ_Conversion_Springfield", False)],
    "Gewehr98": [("Conversion", "JAZZ_Conversion_Gewehr", False)],
    "STG44": [("Conversion", "JAZZ_Conversion_STG", False)],
    "M1Garand": [("Conversion", "JAZZ_Conversion_Garand", False)],
}

# (ApplyTo, Entity, component that now owns the mesh)
MOVES = [
    ("AKM", "AKSeriaMount", "JAZZ_Dovetail_AK"),
    ("AK74", "AKSeriaMount", "JAZZ_Dovetail_AK"),
    ("AEK971", "AKSeriaMount", "JAZZ_Dovetail_AK"),
    ("PP19Bizon", "AKSeriaMount", "JAZZ_Dovetail_AK"),
    ("AKSU", "WeaponAttA_MountAKS74U_01", "JAZZ_Dovetail_AKSU"),
    ("DragunovSVD", "WeaponAttA_MountDragunov_01", "JAZZ_Dovetail_SVD"),
    ("AS_Val", "ValVSSMount", "JAZZ_Dovetail_Val"),
    ("VSS", "ValVSSMount", "JAZZ_Dovetail_Val"),
    ("AKM", "WeaponAttA_MountAK47", "JAZZ_Rail_NATO_AK"),
    ("AEK971", "WeaponAttA_MountAK47", "JAZZ_Rail_NATO_AK"),
    ("AK74M", "WeaponAttA_MountAK47", "JAZZ_Rail_NATO_AK"),
    ("AK105", "WeaponAttA_MountAK47", "JAZZ_Rail_NATO_AK"),
    ("AR10", "CAR15Mount", "JAZZ_Rail_AR"),
    ("CAR15", "CAR15Mount", "JAZZ_Rail_AR"),
    ("M16A1", "CAR15Mount", "JAZZ_Rail_AR"),
    ("M16A2", "CAR15Mount", "JAZZ_Rail_M16A2"),
    ("M16A2", "WeaponAttA_MountFrontCAR15", "JAZZ_Rail_M16A2_Side"),
    ("AUG", "WeaponAttA_MountSteyr", "JAZZ_Rail_AUG"),
    ("AUG", "WeaponAttA_SideMountSteyr", "JAZZ_Rail_AUG_Side"),
    ("FAMAS", "WeaponAttA_MountAnaconda", "JAZZ_Rail_FAMAS"),
    ("FNFAL", "WeaponAttA_MountFNFal_01", "JAZZ_Rail_FAL"),
    ("JAZZ_FNFAL_Tactical", "WeaponAttA_MountFNFal_01", "JAZZ_Rail_FAL"),
    ("G3A3", "G3Mount", "JAZZ_Rail_G3"),
    ("G3A4", "G3Mount", "JAZZ_Rail_G3"),
    ("G3SniperV1", "G3Mount", "JAZZ_Rail_G3"),
    ("G36", "WeaponAttA_MountHKG36_01", "JAZZ_Rail_G36"),
    ("HK21", "WeaponAttA_MountHK21_01", "JAZZ_Rail_HK21"),
    ("HK33", "HK33__Mount", "JAZZ_Rail_HK33"),
    ("Galil", "WeaponAttA_MountGalil", "JAZZ_Rail_Galil"),
    ("M24Sniper", "WeaponAttA_MountM24", "JAZZ_Rail_M24"),
    ("Winchester1894", "WeaponAttA_MountWinchester", "JAZZ_Rail_Winchester"),
    ("AA12", "WeaponAttA_MountAA12_02", "JAZZ_Rail_AA12"),
    ("Ithaca", "Ithaca_Rail", "JAZZ_Rail_Ithaca"),
    ("R870", "UMPScopeRail", "JAZZ_Rail_R870"),
    ("UMP45", "UMPScopeRail", "JAZZ_Rail_UMP"),
    ("MP5K", "WeaponAttA_MountMP5", "JAZZ_Rail_MP5K"),
    ("UZI", "WeaponAttA_MountUzi_02", "JAZZ_Rail_UZI"),
    ("MicroUZI", "WeaponAttA_MountUzi_01", "JAZZ_Rail_MicroUZI"),
    ("M14SAW", "JAZZ_M14_OpticsMount", "JAZZ_Rail_M14"),
    ("M21", "JAZZ_M14_OpticsMount", "JAZZ_Rail_M21"),
    ("JAZZ_M14_MkIII", "WeaponAttA_SideMountM14", "JAZZ_Rail_MkIII"),
    ("M1A", "JAZZ_M14_OpticsMount", "JAZZ_Rail_M1A"),
    ("M4Commando", "WeaponAttA_MountFrontCAR15", "JAZZ_Rail_Commando"),
    ("PSG1", "WeaponAttA_FrontMountM24", "JAZZ_Rail_PSG"),
    ("Bereta92", "WeaponAttA_MountBeretta", "JAZZ_Rail_Beretta"),
    ("CZ52", "WeaponAttA_MountBottomCAR15", "JAZZ_Rail_PistolUnder"),
    ("MAC1950", "WeaponAttA_MountBottomCAR15", "JAZZ_Rail_PistolUnder"),
    ("P220", "P220RailUnder", "JAZZ_Rail_P220"),
    ("ColtAnaconda", "WeaponAttA_MountAnaconda", "JAZZ_Rail_Anaconda"),
]

COMPONENTS = [
    ("JAZZ_Dovetail_AK", "Dovetail", 300, 990003101, "Ласточкин хвост"),
    ("JAZZ_Dovetail_AKSU", "Dovetail", 300, 990003101, "Ласточкин хвост"),
    ("JAZZ_Dovetail_SVD", "Dovetail", 300, 990003101, "Ласточкин хвост"),
    ("JAZZ_Dovetail_Val", "Dovetail", 300, 990003101, "Ласточкин хвост"),
    ("JAZZ_Rail_NATO_AK", "Rail", 100, 990003105, "Переходник НАТО"),
    ("JAZZ_Rail_NATO_SVD", "Rail", 100, 990003105, "Переходник НАТО"),
    ("JAZZ_Rail_NATO_Val", "Rail", 100, 990003105, "Переходник НАТО"),
    ("JAZZ_Rail_AR", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_M16A2", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_M16A2_Side", "RailSide", 100, 990003102, "Планка"),
    ("JAZZ_Rail_AUG", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_AUG_Side", "RailSide", 100, 990003102, "Планка"),
    ("JAZZ_Rail_FAMAS", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_FAL", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_G3", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_G36", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_HK21", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_HK33", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_Galil", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_M24", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_Winchester", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_AA12", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_Ithaca", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_R870", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_UMP", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_MP5K", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_UZI", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_MicroUZI", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_M14", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_M21", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_MkIII", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_M1A", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_Commando", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_PSG", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_Beretta", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_PistolUnder", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_P220", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Rail_Anaconda", "Rail", 100, 990003102, "Планка"),
    ("JAZZ_Conversion_Mosin", "Conversion", 1000, 990003111, "Снайперская винтовка Мосина"),
    ("JAZZ_Conversion_SVT", "Conversion", 1000, 990003112, "СВТ-40 с ПУ"),
    ("JAZZ_Conversion_G43", "Conversion", 1000, 990003113, "G43 с ZF4"),
    ("JAZZ_Conversion_Springfield", "Conversion", 1000, 990003114, "Springfield M1903A4"),
    ("JAZZ_Conversion_Gewehr", "Conversion", 1000, 990003115, "Gewehr 98 с ZF"),
    ("JAZZ_Conversion_STG", "Conversion", 1000, 990003116, "StG-44 с ZF4"),
    ("JAZZ_Conversion_Garand", "Conversion", 1000, 990003117, "Снайперский М1 Гаранд"),
]

HANDGUARD_PARTS = (
    "JAZZ_Handguard_RIS",
    "JAZZ_HK33HandguardMod",
    "JAZZ_HandguardM1ARail",
    "JAZZ_FNFAL_TacHandguard",
)


def brace_end(text: str, open_at: int) -> int:
    depth = 0
    for i in range(open_at, len(text)):
        char = text[i]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return i
    raise RuntimeError("unbalanced brace")


def visual_spans(text: str) -> list[tuple[int, int, str]]:
    key = "PlaceObj('WeaponComponentVisual'"
    spans = []
    cursor = 0
    while True:
        start = text.find(key, cursor)
        if start < 0:
            break
        paren = text.find("(", start)
        depth = 0
        end = None
        for i in range(paren, len(text)):
            if text[i] == "(":
                depth += 1
            elif text[i] == ")":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        if end is None:
            raise RuntimeError("unbalanced visual")
        spans.append((start, end, text[start:end]))
        cursor = end
    return spans


def field(block: str, name: str) -> str | None:
    match = re.search(rf'{name}\s*=\s*"([^"]*)"', block)
    return match.group(1) if match else None


def slot_block(slot: str, component: str, default: bool) -> str:
    lines = [
        "\t\tPlaceObj('WeaponComponentSlot', {",
        f"\t\t\t'SlotType', \"{slot}\",",
        "\t\t\t'CanBeEmpty', true,",
        "\t\t\t'AvailableComponents', {",
        f"\t\t\t\t\"{component}\",",
        "\t\t\t},",
    ]
    if default:
        lines.append(f"\t\t\t'DefaultComponent', \"{component}\",")
    lines.append("\t\t}),")
    return "\n".join(lines)


def weapon_region(text: str, class_id: str, companion: bool = False) -> tuple[int, int] | None:
    if companion:
        start = 0
    else:
        token = f"'Id', \"{class_id}\""
        start = text.find(token)
        if start < 0:
            return None
    slots_at = text.find("ComponentSlots", start)
    if slots_at < 0 or slots_at - start > 80000:
        return None
    brace = text.find("{", slots_at)
    end = brace_end(text, brace)
    return brace, end


def insert_slots(text: str, class_id: str, companion: bool = False) -> str:
    region = weapon_region(text, class_id, companion)
    if region is None:
        print(f"MISSING weapon {class_id}")
        return text
    brace, end = region
    body = text[brace:end]
    extra = []
    for slot, component, default in SLOTS[class_id]:
        if f"'SlotType', \"{slot}\"" in body or f"SlotType', \"{slot}\"" in body:
            continue
        extra.append(slot_block(slot, component, default))
    if not extra:
        return text
    insertion = "\n" + "\n".join(extra) + "\n"
    return text[:end] + insertion + text[end:]


def add_ids_to_scope(text: str, class_id: str, ids: list[str], companion: bool = False) -> str:
    region = weapon_region(text, class_id, companion)
    if region is None:
        return text
    brace, end = region
    body = text[brace:end]
    scope = body.find("'SlotType', \"Scope\"")
    if scope < 0:
        print(f"MISSING scope {class_id}")
        return text
    avail = body.find("'AvailableComponents'", scope)
    open_brace = body.find("{", avail)
    close = brace_end(body, open_brace)
    block = body[open_brace:close]
    missing = [item for item in ids if f'"{item}"' not in block]
    if not missing:
        return text
    addition = "".join(f'\n\t\t\t\t"{item}",' for item in missing)
    abs_close = brace + close
    return text[:abs_close] + addition + "\n" + text[abs_close:]


def patch_fal(text: str, companion: bool = False) -> str:
    region = weapon_region(text, "FNFAL", companion)
    if region is None:
        print("MISSING FNFAL")
        return text
    brace, end = region
    body = text[brace:end]
    body2, count = re.subn(
        r"('SlotType', \"Handguard\",\s*)'Modifiable', false,",
        r"\1'Modifiable', true,",
        body,
        count=1,
    )
    body = body2 if count else body
    if '"JAZZ_FNFAL_TacHandguard"' not in body.split("'SlotType', \"Barrel\"")[0]:
        body = body.replace(
            '"FNFAL_Handguard",',
            '"FNFAL_Handguard",\n\t\t\t\t"JAZZ_FNFAL_TacHandguard",',
            1,
        )
    if '"JAZZ_BarrelLong"' not in body:
        body = body.replace(
            '"JAZZ_BarrelShortImproved",',
            '"JAZZ_BarrelShortImproved",\n\t\t\t\t"JAZZ_BarrelLong",\n\t\t\t\t"JAZZ_BarrelLongImproved",',
            1,
        )
    if '"JAZZ_StockHeavy"' not in body:
        body = body.replace(
            '"JAZZ_StockLightFolded",',
            '"JAZZ_StockLightFolded",\n\t\t\t\t"JAZZ_StockHeavy",',
            1,
        )
    return text[:brace] + body + text[end:]


def hide_tactical(text: str) -> str:
    token = "'Id', \"JAZZ_FNFAL_Tactical\""
    start = text.find(token)
    if start < 0:
        return text
    window_end = start + 2500
    window = text[start:window_end]
    window2 = window.replace("'CanAppearInShop', true,", "'CanAppearInShop', false,", 1)
    return text[:start] + window2 + text[window_end:]


def component_block(slots_by_component: dict[str, list[tuple[str, str, str]]]) -> str:
    parts = [MARKER_BEGIN]
    for comp_id, slot, amount, text_id, label in COMPONENTS:
        visuals = slots_by_component.get(comp_id, [])
        if not visuals:
            visuals = []
        visual_lines = []
        seen = set()
        for apply_to, entity, visual_slot in visuals:
            key = (apply_to, entity)
            if key in seen:
                continue
            seen.add(key)
            visual_lines.append(
                "\t\t\tPlaceObj('WeaponComponentVisual', {\n"
                f'\t\t\t\tApplyTo = "{apply_to}",\n'
                f'\t\t\t\tEntity = "{entity}",\n'
                f'\t\t\t\tSlot = "{visual_slot}",\n'
                "\t\t\t\tparam_bindings = false,\n"
                "\t\t\t}),"
            )
        visual_body = "\n".join(visual_lines) if visual_lines else ""
        parts.append(
            "PlaceObj('ModItemWeaponComponent', {\n"
            "\tAdditionalCosts = {\n"
            "\t\tPlaceObj('WeaponComponentCost', {\n"
            f"\t\t\t'Amount', {amount},\n"
            "\t\t\t'Type', \"Parts\",\n"
            "\t\t}),\n"
            "\t},\n"
            "\tCost = 0,\n"
            f"\tDisplayName = T({text_id}, --[[ModItemWeaponComponent {comp_id} DisplayName]] \"{label}\"),\n"
            f"\tDisplayNamePlural = T({text_id}, --[[ModItemWeaponComponent {comp_id} DisplayNamePlural]] \"{label}\"),\n"
            "\tIcon = \"UI/Icons/Upgrades/default_handguard\",\n"
            "\tModificationDifficulty = 0,\n"
            f"\tSlot = \"{slot}\",\n"
            "\tVisuals = {\n"
            f"{visual_body}\n"
            "\t},\n"
            "\tcomment = \"JAZZ-WEAPON-RAIL-001\",\n"
            "\tgroup = \"JAZZ Rails\",\n"
            f"\tid = \"{comp_id}\",\n"
            "}),"
        )
    parts.append(MARKER_END)
    return "\n".join(parts) + "\n"


def move_visuals(text: str) -> tuple[str, dict[str, list[tuple[str, str, str]]]]:
    wanted = {(apply_to, entity): comp for apply_to, entity, comp in MOVES}
    owned: dict[str, list[tuple[str, str, str]]] = {}
    spans = visual_spans(text)
    remove = []
    for start, end, block in spans:
        apply_to = field(block, "ApplyTo")
        entity = field(block, "Entity")
        comp = wanted.get((apply_to, entity))
        if not comp:
            continue
        visual_slot = field(block, "Slot") or "Mount"
        owned.setdefault(comp, [])
        if (apply_to, entity, visual_slot) not in owned[comp]:
            owned[comp].append((apply_to, entity, visual_slot))
        remove.append((start, end))
    for start, end in reversed(remove):
        tail = end
        if tail < len(text) and text[tail] == ",":
            tail += 1
        if tail < len(text) and text[tail] == "\r":
            tail += 1
        if tail < len(text) and text[tail] == "\n":
            tail += 1
        text = text[:start] + text[tail:]
    for apply_to, entity, comp in MOVES:
        have = {(a, e) for a, e, _s in owned.get(comp, [])}
        if (apply_to, entity) not in have:
            owned.setdefault(comp, []).append((apply_to, entity, "Mount"))
    return text, owned


def patch_handguard_cost(text: str, comp_id: str) -> str:
    token = f'id = "{comp_id}"'
    at = text.find(token)
    if at < 0:
        print(f"MISSING component {comp_id}")
        return text
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, at)
    if start < 0:
        return text
    end = text.find("id = \"" + comp_id + "\"", start)
    # block continues a few lines after id
    close = text.find("}),", end)
    block = text[start:close]
    if "'Amount', 500" in block and "'Type', \"Parts\"" in block:
        block2 = re.sub(r"Cost = \d+,", "Cost = 0,", block, count=1)
        block2 = re.sub(r"ModificationDifficulty = -?\d+,", "ModificationDifficulty = 0,", block2, count=1)
        if "Cost = 0" not in block2:
            block2 = block2.replace(
                "PlaceObj('ModItemWeaponComponent', {",
                "PlaceObj('ModItemWeaponComponent', {\n\t\t\t\t\t\tCost = 0,",
                1,
            )
        return text[:start] + block2 + text[close:]
    addition = (
        "\n\t\t\t\t\tAdditionalCosts = {\n"
        "\t\t\t\t\t\tPlaceObj('WeaponComponentCost', {\n"
        "\t\t\t\t\t\t\t'Amount', 500,\n"
        "\t\t\t\t\t\t\t'Type', \"Parts\",\n"
        "\t\t\t\t\t\t}),\n"
        "\t\t\t\t\t},"
    )
    block2 = block.replace("PlaceObj('ModItemWeaponComponent', {", "PlaceObj('ModItemWeaponComponent', {" + addition, 1)
    block2 = re.sub(r"Cost = \d+,", "Cost = 0,", block2, count=1)
    block2 = re.sub(r"ModificationDifficulty = -?\d+,", "ModificationDifficulty = 0,", block2, count=1)
    if "Cost = 0" not in block2:
        block2 = block2.replace(addition, addition + "\n\t\t\t\t\tCost = 0,", 1)
    return text[:start] + block2 + text[close:]


def add_fal_visual(text: str) -> str:
    token = 'id = "JAZZ_FNFAL_TacHandguard"'
    at = text.find(token)
    if at < 0 or 'ApplyTo = "FNFAL"' in text[max(0, at - 800):at]:
        return text
    needle = 'ApplyTo = "JAZZ_FNFAL_Tactical",\n\t\t\t\t\t\t\t\t\t\tEntity = "JAZZ_FNFAL_TacHandguard",'
    if needle not in text:
        # single-line or different indent: append before the component id if the entity visual exists
        entity = 'Entity = "JAZZ_FNFAL_TacHandguard"'
        pos = text.rfind(entity, 0, at)
        if pos < 0:
            return text
        line_end = text.find("\n", pos)
        insert = (
            "\n\t\t\t\t\t\t\t\t\tPlaceObj('WeaponComponentVisual', {\n"
            '\t\t\t\t\t\t\t\t\t\tApplyTo = "FNFAL",\n'
            '\t\t\t\t\t\t\t\t\t\tEntity = "JAZZ_FNFAL_TacHandguard",\n'
            '\t\t\t\t\t\t\t\t\t\tSlot = "Handguard",\n'
            "\t\t\t\t\t\t\t\t\t\tparam_bindings = false,\n"
            "\t\t\t\t\t\t\t\t\t}),"
        )
        return text[:line_end] + insert + text[line_end:]
    return text


def insert_components(text: str, block: str) -> str:
    if MARKER_BEGIN in text:
        start = text.find(MARKER_BEGIN)
        end = text.find(MARKER_END, start)
        end = text.find("\n", end) + 1
        return text[:start] + block + text[end:]
    anchor = "PlaceObj('ModItemLocTable'"
    at = text.find(anchor)
    if at < 0:
        raise RuntimeError("no loctable anchor")
    return text[:at] + block + "\n\t" + text[at:]


def insert_upgrade_slots(text: str) -> str:
    if 'id = "Dovetail"' in text and 'id = "RailSide"' in text and 'id = "Conversion"' in text:
        return text
    anchor = 'id = "Freeswap"'
    at = text.find(anchor)
    if at < 0:
        raise RuntimeError("no Freeswap slot")
    # insert after the PlaceObj that contains Freeswap, i.e. after the next "}),"
    close = text.find("}),", at)
    insert = """
			PlaceObj('ModItemWeaponUpgradeSlot', {
				DisplayName = T(990003101, --[[ModItemWeaponUpgradeSlot Default Dovetail DisplayName]] "Ласточкин хвост"),
				group = "Default",
				id = "Dovetail",
			}),
			PlaceObj('ModItemWeaponUpgradeSlot', {
				DisplayName = T(990003102, --[[ModItemWeaponUpgradeSlot Default Rail DisplayName]] "Планка"),
				group = "Default",
				id = "Rail",
			}),
			PlaceObj('ModItemWeaponUpgradeSlot', {
				DisplayName = T(990003103, --[[ModItemWeaponUpgradeSlot Default RailSide DisplayName]] "Боковая планка"),
				group = "Default",
				id = "RailSide",
			}),
			PlaceObj('ModItemWeaponUpgradeSlot', {
				DisplayName = T(990003104, --[[ModItemWeaponUpgradeSlot Default Conversion DisplayName]] "Переделка"),
				group = "Default",
				id = "Conversion",
			}),
"""
    return text[: close + 3] + insert + text[close + 3 :]


def patch_companion(class_id: str) -> None:
    path = COMPANION / f"{class_id}.lua"
    if not path.exists():
        print(f"MISSING companion {class_id}")
        return
    text = path.read_text(encoding="utf-8")
    original = text
    text = insert_slots(text, class_id, companion=True)
    if class_id in ("AK74M", "AK105"):
        text = add_ids_to_scope(text, class_id, WESTERN, companion=True)
    if class_id == "FNFAL":
        text = patch_fal(text, companion=True)
    if class_id == "JAZZ_FNFAL_Tactical":
        text = text.replace("CanAppearInShop = true,", "CanAppearInShop = false,", 1)
    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
        print(f"companion {class_id}")


def patch_units(text: str) -> str:
    text = text.replace(
        'weapon = "JAZZ_FNFAL_Tactical",',
        'weapon = "FNFAL",',
    )
    # Ensure the tactical handguard is in each of the five upgraded entries.
    pattern = re.compile(
        r"PlaceObj\('LootEntryUpgradedWeapon', \{\n(?P<body>.*?)\n(?P<indent>\t*)\}\),",
        re.S,
    )

    def repl(match: re.Match) -> str:
        body = match.group("body")
        if 'weapon = "FNFAL"' not in body or "FNFAL_Tactical" in body:
            return match.group(0)
        # Only the defs that used to be the tactical gun: they now say FNFAL and
        # sit next to a tactical loot id. Handled below more narrowly.
        return match.group(0)

    _ = repl
    for loot_id in (
        "BattleRifles_FNFAL_Tactical",
        "BattleRifles_FNFAL_Tactical_AP",
        "BattleRifles_FNFAL_Tactical_Scope",
        "Adonis_FNFAL_Tactical",
        "Adonis_FNFAL_Tactical_Reflex",
    ):
        at = text.find(f'id = "{loot_id}"')
        if at < 0:
            print(f"MISSING loot {loot_id}")
            continue
        window_end = text.find("PlaceObj('ModItemLootDef'", at + 10)
        if window_end < 0:
            window_end = at + 1200
        window = text[at:window_end]
        if "JAZZ_FNFAL_TacHandguard" in window:
            continue
        if "upgrades = {" in window:
            window = window.replace(
                "upgrades = {",
                'upgrades = {\n\t\t\t\t\t\t\t"JAZZ_FNFAL_TacHandguard",',
                1,
            )
        else:
            window = window.replace(
                'weapon = "FNFAL",',
                'upgrades = {\n\t\t\t\t\t\t"JAZZ_FNFAL_TacHandguard",\n\t\t\t\t\t},\n\t\t\t\t\tweapon = "FNFAL",',
                1,
            )
        text = text[:at] + window + text[window_end:]
    return text


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    text, owned = move_visuals(text)
    print(f"moved meshes onto {len(owned)} components")
    for class_id in SLOTS:
        text = insert_slots(text, class_id)
    text = add_ids_to_scope(text, "AK74M", WESTERN)
    text = add_ids_to_scope(text, "AK105", WESTERN)
    text = patch_fal(text)
    text = hide_tactical(text)
    for comp_id in HANDGUARD_PARTS:
        text = patch_handguard_cost(text, comp_id)
    text = add_fal_visual(text)
    text = insert_upgrade_slots(text)
    text = insert_components(text, component_block(owned))
    ITEMS.write_text(text, encoding="utf-8", newline="\n")
    print("items.lua written")
    for class_id in SLOTS:
        patch_companion(class_id)
    tactical = COMPANION / "JAZZ_FNFAL_Tactical.lua"
    if tactical.exists():
        body = tactical.read_text(encoding="utf-8")
        body2 = body.replace("CanAppearInShop = true,", "CanAppearInShop = false,", 1)
        if body2 != body:
            tactical.write_text(body2, encoding="utf-8", newline="\n")
            print("companion JAZZ_FNFAL_Tactical")
    units = UNITS.read_text(encoding="utf-8")
    units2 = patch_units(units)
    if units2 != units:
        UNITS.write_text(units2, encoding="utf-8", newline="\n")
        print("jazz-units loot")
    print("done")


if __name__ == "__main__":
    main()
