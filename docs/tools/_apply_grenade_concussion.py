# Playtest fix: Concussion CharacterEffect + generated transaction (items/metadata/companion).
# Runtime wiring lives in Code/Systems_Medicine.lua + Code/System_ArmorRating.lua.
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DN_ID = 890000000010277
DESC_ID = 890000000010278
ADD_ID = 890000000010279
REM_ID = 890000000010280

COMPANION = f'''UndefineClass('Concussion')
DefineClass.Concussion = {{
\t__parents = {{ "StatusEffect" }},
\t__generated_by_class = "ModItemCharacterEffectCompositeDef",


\tobject_class = "StatusEffect",
\tParameters = {{
\t\tPlaceObj('PresetParamNumber', {{
\t\t\t'Name', "APLoss",
\t\t\t'Value', 2,
\t\t\t'Tag', "<APLoss>",
\t\t}}),
\t\tPlaceObj('PresetParamPercent', {{
\t\t\t'Name', "cth_penalty",
\t\t\t'Value', 15,
\t\t\t'Tag', "<cth_penalty>%",
\t\t}}),
\t\tPlaceObj('PresetParamNumber', {{
\t\t\t'Name', "move_ap_modifier",
\t\t\t'Value', 30,
\t\t\t'Tag', "<move_ap_modifier>",
\t\t}}),
\t}},
\tunit_reactions = {{
\t\tPlaceObj('UnitReaction', {{
\t\t\tEvent = "OnCalcStartTurnAP",
\t\t\tHandler = function (self, target, value)
\t\t\t\treturn value - self:ResolveValue("APLoss") * const.Scale.AP
\t\t\tend,
\t\t}}),
\t\tPlaceObj('UnitReaction', {{
\t\t\tEvent = "OnCalcChanceToHit",
\t\t\tHandler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
\t\t\t\tif target == attacker then
\t\t\t\t\tApplyCthModifier_Add(self, data, -self:ResolveValue("cth_penalty"))
\t\t\t\tend
\t\t\tend,
\t\t}}),
\t\tPlaceObj('UnitReaction', {{
\t\t\tEvent = "OnCalcMoveModifier",
\t\t\tHandler = function (self, target, value, action)
\t\t\t\treturn value + self:ResolveValue("move_ap_modifier")
\t\t\tend,
\t\t}}),
\t\tPlaceObj('UnitReaction', {{
\t\t\tEvent = "OnCalcFreeMove",
\t\t\tHandler = function (self, target, data)
\t\t\t\tdata.add = 0
\t\t\t\tdata.mul = 0
\t\t\tend,
\t\t}}),
\t\tPlaceObj('UnitReaction', {{
\t\t\tEvent = "OnBeginTurn",
\t\t\tHandler = function (self, target)
\t\t\t\ttarget:RemoveStatusEffect("FreeMove")
\t\t\tend,
\t\t}}),
\t\tPlaceObj('UnitReaction', {{
\t\t\tEvent = "OnEndTurn",
\t\t\tHandler = function (self, target)
\t\t\t\tlocal left = self:ResolveValue("jazz_conc_turns") or 1
\t\t\t\tleft = left - 1
\t\t\t\tif left <= 0 then
\t\t\t\t\ttarget:RemoveStatusEffect("Concussion", "all")
\t\t\t\telse
\t\t\t\t\tself:SetParameter("jazz_conc_turns", left)
\t\t\t\tend
\t\t\tend,
\t\t}}),
\t}},
\tDisplayName = T({DN_ID}, --[[ModItemCharacterEffectCompositeDef Concussion DisplayName]] "Concussion"),
\tDescription = T({DESC_ID}, --[[ModItemCharacterEffectCompositeDef Concussion Description]] "Disoriented by blast: <color EmStyle>−<APLoss> AP</color>, <color EmStyle>−<cth_penalty>% chance to hit</color>, move cost <color EmStyle>+<move_ap_modifier>%</color>, no Free Move. Lasts about 1–2 turns."),
\tAddEffectText = T({ADD_ID}, --[[ModItemCharacterEffectCompositeDef Concussion AddEffectText]] "<color EmStyle><DisplayName></color> is concussed"),
\tRemoveEffectText = T({REM_ID}, --[[ModItemCharacterEffectCompositeDef Concussion RemoveEffectText]] "<color EmStyle><DisplayName></color> clears concussion"),
\tOnAdded = function (self, obj)
\t\tself:SetParameter("jazz_conc_turns", 2)
\t\tMsg("UnitAPChanged", obj)
\tend,
\tOnRemoved = function (self, obj)
\t\tMsg("UnitAPChanged", obj)
\tend,
\ttype = "Debuff",
\tIcon = "Mod/e6L4ECj/Icons/StatusEffects/Concussion.png",
\tRemoveOnEndCombat = true,
\tShown = true,
\tHasFloatingText = true,
}}
'''

ITEMS_BLOCK = f'''\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {{
\t\t\t\t'Id', "Concussion",
\t\t\t\t'Parameters', {{
\t\t\t\t\tPlaceObj('PresetParamNumber', {{
\t\t\t\t\t\t'Name', "APLoss",
\t\t\t\t\t\t'Value', 2,
\t\t\t\t\t\t'Tag', "<APLoss>",
\t\t\t\t\t}}),
\t\t\t\t\tPlaceObj('PresetParamPercent', {{
\t\t\t\t\t\t'Name', "cth_penalty",
\t\t\t\t\t\t'Value', 15,
\t\t\t\t\t\t'Tag', "<cth_penalty>%",
\t\t\t\t\t}}),
\t\t\t\t\tPlaceObj('PresetParamNumber', {{
\t\t\t\t\t\t'Name', "move_ap_modifier",
\t\t\t\t\t\t'Value', 30,
\t\t\t\t\t\t'Tag', "<move_ap_modifier>",
\t\t\t\t\t}}),
\t\t\t\t}},
\t\t\t\t'object_class', "StatusEffect",
\t\t\t\t'unit_reactions', {{
\t\t\t\t\tPlaceObj('UnitReaction', {{
\t\t\t\t\t\tEvent = "OnCalcStartTurnAP",
\t\t\t\t\t\tHandler = function (self, target, value)
\t\t\t\t\t\t\treturn value - self:ResolveValue("APLoss") * const.Scale.AP
\t\t\t\t\t\tend,
\t\t\t\t\t}}),
\t\t\t\t\tPlaceObj('UnitReaction', {{
\t\t\t\t\t\tEvent = "OnCalcChanceToHit",
\t\t\t\t\t\tHandler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
\t\t\t\t\t\t\tif target == attacker then
\t\t\t\t\t\t\t\tApplyCthModifier_Add(self, data, -self:ResolveValue("cth_penalty"))
\t\t\t\t\t\t\tend
\t\t\t\t\t\tend,
\t\t\t\t\t}}),
\t\t\t\t\tPlaceObj('UnitReaction', {{
\t\t\t\t\t\tEvent = "OnCalcMoveModifier",
\t\t\t\t\t\tHandler = function (self, target, value, action)
\t\t\t\t\t\t\treturn value + self:ResolveValue("move_ap_modifier")
\t\t\t\t\t\tend,
\t\t\t\t\t}}),
\t\t\t\t\tPlaceObj('UnitReaction', {{
\t\t\t\t\t\tEvent = "OnCalcFreeMove",
\t\t\t\t\t\tHandler = function (self, target, data)
\t\t\t\t\t\t\tdata.add = 0
\t\t\t\t\t\t\tdata.mul = 0
\t\t\t\t\t\tend,
\t\t\t\t\t}}),
\t\t\t\t\tPlaceObj('UnitReaction', {{
\t\t\t\t\t\tEvent = "OnBeginTurn",
\t\t\t\t\t\tHandler = function (self, target)
\t\t\t\t\t\t\ttarget:RemoveStatusEffect("FreeMove")
\t\t\t\t\t\tend,
\t\t\t\t\t}}),
\t\t\t\t\tPlaceObj('UnitReaction', {{
\t\t\t\t\t\tEvent = "OnEndTurn",
\t\t\t\t\t\tHandler = function (self, target)
\t\t\t\t\t\t\tlocal left = self:ResolveValue("jazz_conc_turns") or 1
\t\t\t\t\t\t\tleft = left - 1
\t\t\t\t\t\t\tif left <= 0 then
\t\t\t\t\t\t\t\ttarget:RemoveStatusEffect("Concussion", "all")
\t\t\t\t\t\t\telse
\t\t\t\t\t\t\t\tself:SetParameter("jazz_conc_turns", left)
\t\t\t\t\t\t\tend
\t\t\t\t\t\tend,
\t\t\t\t\t}}),
\t\t\t\t}},
\t\t\t\t'DisplayName', T({DN_ID}, --[[ModItemCharacterEffectCompositeDef Concussion DisplayName]] "Concussion"),
\t\t\t\t'Description', T({DESC_ID}, --[[ModItemCharacterEffectCompositeDef Concussion Description]] "Disoriented by blast: <color EmStyle>−<APLoss> AP</color>, <color EmStyle>−<cth_penalty>% chance to hit</color>, move cost <color EmStyle>+<move_ap_modifier>%</color>, no Free Move. Lasts about 1–2 turns."),
\t\t\t\t'AddEffectText', T({ADD_ID}, --[[ModItemCharacterEffectCompositeDef Concussion AddEffectText]] "<color EmStyle><DisplayName></color> is concussed"),
\t\t\t\t'RemoveEffectText', T({REM_ID}, --[[ModItemCharacterEffectCompositeDef Concussion RemoveEffectText]] "<color EmStyle><DisplayName></color> clears concussion"),
\t\t\t\t'OnAdded', function (self, obj)
\t\t\t\t\tself:SetParameter("jazz_conc_turns", 2)
\t\t\t\t\tMsg("UnitAPChanged", obj)
\t\t\t\tend,
\t\t\t\t'OnRemoved', function (self, obj)
\t\t\t\t\tMsg("UnitAPChanged", obj)
\t\t\t\tend,
\t\t\t\t'type', "Debuff",
\t\t\t\t'Icon', "Mod/e6L4ECj/Icons/StatusEffects/Concussion.png",
\t\t\t\t'RemoveOnEndCombat', true,
\t\t\t\t'Shown', true,
\t\t\t\t'HasFloatingText', true,
\t\t\t}}),
'''

META_CODE = '\t\t"CharacterEffect/Concussion.lua",\n'
META_RES = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "CharacterEffectCompositeDef",
\t\t\t'Id', "Concussion",
\t\t\t'ClassDisplayName', "Character effect",
\t\t}),
"""


def main() -> None:
    companion = ROOT / "CharacterEffect" / "Concussion.lua"
    companion.write_text(COMPANION, encoding="utf-8")
    print("wrote", companion.relative_to(ROOT))

    items = ROOT / "items.lua"
    text = items.read_text(encoding="utf-8")
    if "'Id', \"Concussion\"" in text:
        print("items.lua already has Concussion")
    else:
        marker = "\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {\n\t\t\t\t'Group', \"System\",\n\t\t\t\t'Id', \"SuppressStunGrenade\","
        if marker not in text:
            raise SystemExit("SuppressStunGrenade marker missing in items.lua")
        text = text.replace(marker, ITEMS_BLOCK + marker, 1)
        items.write_text(text, encoding="utf-8")
        print("inserted Concussion ModItem before SuppressStunGrenade")

    meta = ROOT / "metadata.lua"
    mtext = meta.read_text(encoding="utf-8")
    if "CharacterEffect/Concussion.lua" not in mtext:
        m_marker = '\t\t"CharacterEffect/SuppressStunGrenade.lua",\n'
        if m_marker not in mtext:
            raise SystemExit("metadata code marker missing")
        mtext = mtext.replace(m_marker, META_CODE + m_marker, 1)
        print("metadata.code: Concussion.lua")
    if "'Id', \"Concussion\"" not in mtext:
        r_marker = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "CharacterEffectCompositeDef",
\t\t\t'Id', "SuppressStunGrenade",
\t\t\t'ClassDisplayName', "Character effect",
\t\t}),
"""
        if r_marker not in mtext:
            raise SystemExit("metadata resources marker missing")
        mtext = mtext.replace(r_marker, META_RES + r_marker, 1)
        print("metadata.resources: Concussion")
    meta.write_text(mtext, encoding="utf-8")

    # Loc append helper lines for manual/CSV merge (audit will sync).
    loc_snip = ROOT / "docs" / "tools" / "_grenade_concussion_loc.txt"
    loc_snip.write_text(
        "\n".join(
            [
                f"{DN_ID},Контузия,Concussion",
                f"{DESC_ID},"
                "Дезориентация от взрыва: <color EmStyle>−<APLoss> ОД</color>, "
                "<color EmStyle>−<cth_penalty>% к точности</color>, стоимость хода "
                "<color EmStyle>+<move_ap_modifier>%</color>, без Free Move. Около 1–2 ходов.,"
                "Disoriented by blast: <color EmStyle>−<APLoss> AP</color>, "
                "<color EmStyle>−<cth_penalty>% chance to hit</color>, move cost "
                "<color EmStyle>+<move_ap_modifier>%</color>, no Free Move. Lasts about 1–2 turns.",
                f"{ADD_ID},<color EmStyle><DisplayName></color> контужен,"
                "<color EmStyle><DisplayName></color> is concussed",
                f"{REM_ID},<color EmStyle><DisplayName></color> приходит в себя после контузии,"
                "<color EmStyle><DisplayName></color> clears concussion",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print("wrote", loc_snip.relative_to(ROOT))


if __name__ == "__main__":
    main()
