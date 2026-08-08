# -*- coding: utf-8 -*-
"""Add ModItem Parameters to UNITS-006 perks and wire Code to ResolveValue.

Companions are source of truth; syncs items.lua ModItems.
Run from jazz root:
  python docs/tools/_units006_perk_moditem_params.py
  python docs/tools/_validate_items_quick.py

Cyrillic in this file must use \\u escapes.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _apply_units006_batch2_items_loc import (  # type: ignore
    companion_props_to_items,
    extract_define_props,
    find_moditem_span,
    build_moditem,
)

CE = ROOT / "CharacterEffect"
ITEMS = ROOT / "items.lua"
CODE = ROOT / "Code" / "System_NamedPerks_006.lua"

# class_id -> list of (Name, Value, Tag, kind) kind in {Number, Percent}
PARAMS: dict[str, list[tuple[str, int, str, str]]] = {
    "Jazz_Perk_Henning": [
        ("radius", 10, "<radius>", "Number"),
    ],
    "Jazz_OrderAP": [
        ("ap_bonus", 3, "<ap_bonus>", "Number"),
    ],
    "Jazz_Perk_Miguel": [
        ("aura_radius", 30, "<aura_radius>", "Number"),
    ],
    "Jazz_MiguelAuraUp": [
        ("cth_bonus", 15, "<cth_bonus>", "Number"),
        ("will_bonus", 30, "<will_bonus>", "Number"),
    ],
    "Jazz_MiguelAuraDown": [
        ("cth_penalty", 15, "<cth_penalty>", "Number"),
        ("will_penalty", 30, "<will_penalty>", "Number"),
    ],
    "Jazz_Perk_Rothman": [
        ("mine_bonus_base", 10, "<mine_bonus_base>", "Number"),
        ("mine_bonus_loyalty_span", 30, "<mine_bonus_loyalty_span>", "Number"),
    ],
    "Jazz_Perk_Flo": [
        ("buy_discount", 12, "<buy_discount>", "Percent"),
        ("sell_bonus", 12, "<sell_bonus>", "Percent"),
    ],
    "Jazz_Perk_Static": [
        ("parts_per_level", 5, "<parts_per_level>", "Number"),
        ("parts_cap", 25, "<parts_cap>", "Number"),
    ],
    "DesignerExplosives": [
        ("craft_discount", 30, "<craft_discount>", "Percent"),
    ],
    "Jazz_Perk_Cord": [
        ("repair_parts_discount", 10, "<repair_parts_discount>", "Percent"),
        ("repair_time_discount", 15, "<repair_time_discount>", "Percent"),
    ],
    "Jazz_Perk_Conrad": [
        ("leadership_floor", 90, "<leadership_floor>", "Number"),
    ],
    "Jazz_Perk_Carlos": [
        ("detection_reduction", 33, "<detection_reduction>", "Percent"),
        ("keep_hidden_chance", 50, "<keep_hidden_chance>", "Percent"),
    ],
    "Jazz_Perk_Vince": [
        ("med_skip_chance", 25, "<med_skip_chance>", "Percent"),
        ("med_amount_mul", 75, "<med_amount_mul>", "Percent"),
    ],
    "Jazz_Perk_Ira": [
        ("primary_bonus", 20, "<primary_bonus>", "Number"),
    ],
    "Jazz_Perk_Cougar": [
        ("noise_mul", 67, "<noise_mul>", "Percent"),
    ],
    "Jazz_Perk_Grace": [
        ("knife_range", 12, "<knife_range>", "Number"),
    ],
    "Jazz_Perk_Benny": [
        ("lure_range", 8, "<lure_range>", "Number"),
    ],
    "Jazz_Perk_Nervous": [
        ("stack_cap", 10, "<stack_cap>", "Number"),
    ],
    "Jazz_Perk_Madman": [
        ("will_drain", 10, "<will_drain>", "Number"),
        ("radius", 5, "<radius>", "Number"),
    ],
    "Jazz_Perk_Steiger": [
        ("radius", 10, "<radius>", "Number"),
        ("cth_bonus", 5, "<cth_bonus>", "Number"),
    ],
    "DangerClose": [
        ("minRange", 8, "<minRange>", "Number"),
        ("damageBonus", 40, "<damageBonus>", "Percent"),
        ("bleed_stacks", 2, "<bleed_stacks>", "Number"),
    ],
    "Jazz_Perk_Kulba": [
        ("recoil_mul", 50, "<recoil_mul>", "Percent"),
    ],
    "Jazz_Perk_Ricochet": [
        ("splash_percent", 35, "<splash_percent>", "Percent"),
        ("splash_range", 1, "<splash_range>", "Number"),
    ],
}


def params_block(entries: list[tuple[str, int, str, str]]) -> str:
    lines = ["\tParameters = {\n"]
    for name, value, tag, kind in entries:
        cls = "PresetParamPercent" if kind == "Percent" else "PresetParamNumber"
        lines.append("\t\tPlaceObj('%s', {\n" % cls)
        lines.append("\t\t\t'Name', \"%s\",\n" % name)
        lines.append("\t\t\t'Value', %d,\n" % value)
        lines.append("\t\t\t'Tag', \"%s\",\n" % tag)
        lines.append("\t\t}),\n")
    lines.append("\t},\n")
    return "".join(lines)


def upsert_parameters(path: Path, entries: list[tuple[str, int, str, str]]) -> None:
    text = path.read_text(encoding="utf-8")
    block = params_block(entries)
    # Remove existing Parameters = { ... }, at top level of DefineClass
    text2 = re.sub(
        r"\tParameters = \{.*?\n\t\},\n",
        block,
        text,
        count=1,
        flags=re.S,
    )
    if text2 == text:
        # Insert after object_class line
        m = re.search(r"(\tobject_class = \"[^\"]+\",\n)", text)
        if not m:
            raise SystemExit(f"object_class missing in {path.name}")
        text2 = text[: m.end()] + block + text[m.end() :]
    path.write_text(text2, encoding="utf-8", newline="\n")
    print("params", path.name)


def patch_reactions_resolve(path: Path, class_id: str) -> None:
    """Best-effort: replace known hardcodes inside unit_reactions with ResolveValue."""
    text = path.read_text(encoding="utf-8")
    orig = text
    if class_id == "Jazz_Perk_Henning":
        text = text.replace(
            "DivRound(target:GetDist(ally), const.SlabSizeX) <= 10",
            "DivRound(target:GetDist(ally), const.SlabSizeX) <= (self:ResolveValue(\"radius\") or 10)",
        )
    elif class_id == "Jazz_OrderAP":
        text = text.replace(
            "target:GainAP(3 * const.Scale.AP)",
            "target:GainAP((self:ResolveValue(\"ap_bonus\") or 3) * const.Scale.AP)",
        )
        text = text.replace(
            "obj:GainAP(3 * const.Scale.AP)",
            "obj:GainAP((self:ResolveValue(\"ap_bonus\") or 3) * const.Scale.AP)",
        )
    elif class_id == "Jazz_MiguelAuraUp":
        text = text.replace(
            "ApplyCthModifier_Add(self, data, 15)",
            "ApplyCthModifier_Add(self, data, self:ResolveValue(\"cth_bonus\") or 15)",
        )
        text = text.replace(
            "target.WillPoints = Min(target.MaxWillPoints, target.WillPoints + 30)",
            "target.WillPoints = Min(target.MaxWillPoints, target.WillPoints + (self:ResolveValue(\"will_bonus\") or 30))",
        )
    elif class_id == "Jazz_MiguelAuraDown":
        text = text.replace(
            "ApplyCthModifier_Add(self, data, -15)",
            "ApplyCthModifier_Add(self, data, -(self:ResolveValue(\"cth_penalty\") or 15))",
        )
        text = text.replace(
            "target.WillPoints = Max(0, target.WillPoints - 30)",
            "target.WillPoints = Max(0, target.WillPoints - (self:ResolveValue(\"will_penalty\") or 30))",
        )
    elif class_id == "Jazz_Perk_Grace":
        text = text.replace(
            "if dist <= 12 then",
            "if dist <= (self:ResolveValue(\"knife_range\") or 12) then",
        )
    elif class_id == "Jazz_Perk_Steiger":
        # night aura radius / CTH if present in companion
        text = text.replace(
            "DivRound(target:GetDist(ally), const.SlabSizeX) <= 10",
            "DivRound(target:GetDist(ally), const.SlabSizeX) <= (self:ResolveValue(\"radius\") or 10)",
        )
    elif class_id == "Jazz_Perk_Ricochet":
        text = text.replace(
            "MulDivRound(dmg, 35, 100)",
            "MulDivRound(dmg, self:ResolveValue(\"splash_percent\") or 35, 100)",
        )
        text = text.replace(
            "DivRound(attack_target:GetDist(u), slab) <= 1",
            "DivRound(attack_target:GetDist(u), slab) <= (self:ResolveValue(\"splash_range\") or 1)",
        )
    if text != orig:
        path.write_text(text, encoding="utf-8", newline="\n")
        print("reactions", path.name)


def ensure_helper_and_wire_code() -> None:
    text = CODE.read_text(encoding="utf-8")
    helper = '''
--- Read a Named Perk Parameter from unit effect or CharacterEffectDefs (ModItem-tunable).
function Jazz_NamedPerkParam(unit, perk_id, key, default)
\tlocal effect
\tif unit and unit.GetStatusEffect then
\t\teffect = unit:GetStatusEffect(perk_id)
\tend
\tif (not effect or not effect.ResolveValue) and CharacterEffectDefs then
\t\teffect = CharacterEffectDefs[perk_id]
\tend
\tif effect and effect.ResolveValue then
\t\tlocal v = effect:ResolveValue(key)
\t\tif v ~= nil then
\t\t\treturn v
\t\tend
\tend
\treturn default
end

'''
    if "function Jazz_NamedPerkParam" not in text:
        # insert after first header comment block / before first g_JAZZ_
        m = re.search(r"^g_JAZZ_NamedPerks006Wrapped", text, re.M)
        if not m:
            raise SystemExit("hub marker missing")
        text = text[: m.start()] + helper + text[m.start() :]
        print("inserted Jazz_NamedPerkParam")

    replacements = [
        (
            "return InteractionRand(100, \"Jazz_Perk_Vince\") < 25",
            'return InteractionRand(100, "Jazz_Perk_Vince") < Jazz_NamedPerkParam(healer, "Jazz_Perk_Vince", "med_skip_chance", 25)',
        ),
        (
            "return Max(1, MulDivRound(amount, 75, 100))",
            'return Max(1, MulDivRound(amount, Jazz_NamedPerkParam(healer, "Jazz_Perk_Vince", "med_amount_mul", 75), 100))',
        ),
        (
            "return Clamp(tonumber(unit:GetEffectValue(\"Jazz_NervousBonusShots\")) or 0, 0, 10)",
            'return Clamp(tonumber(unit:GetEffectValue("Jazz_NervousBonusShots")) or 0, 0, Jazz_NamedPerkParam(unit, "Jazz_Perk_Nervous", "stack_cap", 10))',
        ),
        (
            "unit:SetEffectValue(\"Jazz_NervousBonusShots\", Clamp(cur + hits, 0, 10))",
            'unit:SetEffectValue("Jazz_NervousBonusShots", Clamp(cur + hits, 0, Jazz_NamedPerkParam(unit, "Jazz_Perk_Nervous", "stack_cap", 10)))',
        ),
        (
            "u.WillPoints = Max(0, wp - 10)",
            'u.WillPoints = Max(0, wp - Jazz_NamedPerkParam(center_unit, "Jazz_Perk_Madman", "will_drain", 10))',
        ),
        (
            "if DivRound(center_unit:GetDist(u), slab) <= 5 then",
            'if DivRound(center_unit:GetDist(u), slab) <= Jazz_NamedPerkParam(center_unit, "Jazz_Perk_Madman", "radius", 5) then',
        ),
        (
            "return Clamp((tonumber(lvl) or 1) * 5, 0, 25)",
            'return Clamp((tonumber(lvl) or 1) * Jazz_NamedPerkParam(unit, "Jazz_Perk_Static", "parts_per_level", 5), 0, Jazz_NamedPerkParam(unit, "Jazz_Perk_Static", "parts_cap", 25))',
        ),
        (
            "cost = MulDivRound(cost, 88, 100)",
            'local disc = Jazz_NamedPerkParam(nil, "Jazz_Perk_Flo", "buy_discount", 12)\n\t\t\t\tcost = MulDivRound(cost, 100 - disc, 100)',
        ),
        (
            "item.Cost = MulDivRound(old, 112, 100)",
            'local bonus = Jazz_NamedPerkParam(nil, "Jazz_Perk_Flo", "sell_bonus", 12)\n\t\t\t\titem.Cost = MulDivRound(old, 100 + bonus, 100)',
        ),
        (
            "radius = MulDivRound(radius, 67, 100)",
            'radius = MulDivRound(radius, Jazz_NamedPerkParam(attacker, "Jazz_Perk_Cougar", "noise_mul", 67), 100)',
        ),
        (
            "return 10 + MulDivRound(Max(0, 100 - loyalty), 30, 100)",
            'local base = Jazz_NamedPerkParam(nil, "Jazz_Perk_Rothman", "mine_bonus_base", 10)\n\tlocal span = Jazz_NamedPerkParam(nil, "Jazz_Perk_Rothman", "mine_bonus_loyalty_span", 30)\n\treturn base + MulDivRound(Max(0, 100 - loyalty), span, 100)',
        ),
        (
            "if DivRound(miguel:GetDist(u), slab) <= 30 then",
            'if DivRound(miguel:GetDist(u), slab) <= Jazz_NamedPerkParam(miguel, "Jazz_Perk_Miguel", "aura_radius", 30) then',
        ),
        (
            "return 30",
            # Barry craft — only the DesignerExplosives return 30 function body
            None,  # handled specially below
        ),
        (
            "return Max(ldr, 90)",
            'return Max(ldr, Jazz_NamedPerkParam(merc, "Jazz_Perk_Conrad", "leadership_floor", 90))',
        ),
        (
            "parts = Max(0, MulDivRound(parts, 90, 100))",
            'local disc = Jazz_NamedPerkParam(merc, "Jazz_Perk_Cord", "repair_parts_discount", 10)\n\t\t\t\t\t\tparts = Max(0, MulDivRound(parts, 100 - disc, 100))',
        ),
        (
            "t = MulDivRound(t, 85, 100)",
            'local td = Jazz_NamedPerkParam(merc, "Jazz_Perk_Cord", "repair_time_discount", 15)\n\t\t\t\tt = MulDivRound(t, 100 - td, 100)',
        ),
        (
            "if ldr < 90 and ldr > 0 then",
            'local floor = Jazz_NamedPerkParam(merc, "Jazz_Perk_Conrad", "leadership_floor", 90)\n\t\t\t\tif ldr < floor and ldr > 0 then',
        ),
        (
            "t = MulDivRound(t, ldr, 90)",
            "t = MulDivRound(t, ldr, floor)",
        ),
        (
            "if InteractionRand(100, \"Jazz_Perk_Carlos\") < 50 then",
            'if InteractionRand(100, "Jazz_Perk_Carlos") < Jazz_NamedPerkParam(self, "Jazz_Perk_Carlos", "keep_hidden_chance", 50) then',
        ),
        (
            "if DivRound(unit:GetDist(enemy), slab) <= 8 then",
            'if DivRound(unit:GetDist(enemy), slab) <= Jazz_NamedPerkParam(unit, "Jazz_Perk_Benny", "lure_range", 8) then',
        ),
        (
            "unit[stat] = Clamp(cur + 20, 0, 100)",
            'unit[stat] = Clamp(cur + Jazz_NamedPerkParam(nil, "Jazz_Perk_Ira", "primary_bonus", 20), 0, 100)',
        ),
    ]

    for old, new in replacements:
        if new is None:
            continue
        if old in text:
            text = text.replace(old, new, 1)
            print("wired", old[:48])

    # Barry craft discount function
    text = re.sub(
        r"function Jazz_BarryCraftDiscountPercent\(unit\)\n"
        r"\tif unit and HasPerk\(unit, \"DesignerExplosives\"\) then\n"
        r"\t\treturn 30\n"
        r"\tend\n"
        r"\treturn 0\n"
        r"end",
        "function Jazz_BarryCraftDiscountPercent(unit)\n"
        "\tif unit and HasPerk(unit, \"DesignerExplosives\") then\n"
        "\t\treturn Jazz_NamedPerkParam(unit, \"DesignerExplosives\", \"craft_discount\", 30)\n"
        "\tend\n"
        "\treturn 0\n"
        "end",
        text,
        count=1,
    )

    # DangerClose bleed stacks
    if "Jazz_DangerCloseOnAttack" in text and "bleed_stacks" not in text:
        text = text.replace(
            """\tif CharacterEffectDefs and CharacterEffectDefs.Bleeding and target.AddStatusEffect then
\t\ttarget:AddStatusEffect("Bleeding")
\t\ttarget:AddStatusEffect("Bleeding")
\tend""",
            """\tlocal stacks = Jazz_NamedPerkParam(attacker, "DangerClose", "bleed_stacks", 2)
\tif CharacterEffectDefs and CharacterEffectDefs.Bleeding and target.AddStatusEffect then
\t\tfor _ = 1, stacks do
\t\t\ttarget:AddStatusEffect("Bleeding")
\t\tend
\tend""",
        )
        # also min range in DangerCloseOnAttack
        text = text.replace(
            "if dist < 8 then",
            'if dist < Jazz_NamedPerkParam(attacker, "DangerClose", "minRange", 8) then',
        )

    # Carlos detection in UnitAwareness is separate file
    CODE.write_text(text, encoding="utf-8", newline="\n")
    print("updated", CODE.name)

    aw = ROOT / "Code" / "UnitAwareness.lua"
    awt = aw.read_text(encoding="utf-8")
    old_c = """\t\tif HasPerk(ally, "Jazz_Perk_Carlos") then
\t\t\tallyDetectionModifier = allyDetectionModifier - 33
\t\tend"""
    new_c = """\t\tif HasPerk(ally, "Jazz_Perk_Carlos") then
\t\t\tallyDetectionModifier = allyDetectionModifier - Jazz_NamedPerkParam(ally, "Jazz_Perk_Carlos", "detection_reduction", 33)
\t\tend"""
    if old_c in awt:
        aw.write_text(awt.replace(old_c, new_c, 1), encoding="utf-8", newline="\n")
        print("UnitAwareness Carlos param")


def sync_items_for(class_ids: list[str]) -> None:
    text = ITEMS.read_text(encoding="utf-8")
    for class_id in class_ids:
        path = CE / f"{class_id}.lua"
        if not path.exists():
            print("skip missing companion", class_id)
            continue
        cid, props = extract_define_props(path)
        assert cid == class_id
        # Infer group from existing ModItem or default
        span = find_moditem_span(text, class_id)
        group = "Perk-Personal"
        if span:
            chunk = text[span[0] : span[1]]
            gm = re.search(r"'Group', \"([^\"]+)\"", chunk)
            if gm:
                group = gm.group(1)
        props_items = companion_props_to_items(props)
        block = build_moditem(class_id, group, props_items)
        if not span:
            print("WARN no ModItem for", class_id)
            continue
        text = text[: span[0]] + block + text[span[1] :]
        print("synced ModItem", class_id)
    tmp = ITEMS.with_suffix(".lua.tmp_params")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    tmp.replace(ITEMS)


def main() -> None:
    for class_id, entries in PARAMS.items():
        path = CE / f"{class_id}.lua"
        if not path.exists():
            print("skip missing", class_id)
            continue
        upsert_parameters(path, entries)
        patch_reactions_resolve(path, class_id)
    ensure_helper_and_wire_code()
    sync_items_for(list(PARAMS.keys()))
    print("OK perk ModItem params")


if __name__ == "__main__":
    main()
