# -*- coding: utf-8 -*-
"""UNITS-006 Grunty: Passive hotbar CA + fix AdditionalAP double AP grant.

- Insert ModItemCombatAction id=GruntyPerk_JAZZ (Passive, perk_grunty_perk HUD).
- Metadata ModResourcePreset CombatAction.
- Grunty_AdditionalAP: drop OnBeginTurn GainAP (OnCalcStartTurnAP + OnAdded only).
- Bump jazz metadata version + last_changes bullet.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"
CE_BUFF = ROOT / "CharacterEffect" / "Grunty_AdditionalAP.lua"

PLACEHOLDER_T = 115026001164

PASSIVE_CA = f"""\t\t\t\tPlaceObj('ModItemCombatAction', {{
\t\t\t\t\tActionType = "Passive",
\t\t\t\t\tActivePauseBehavior = "instant",
\t\t\t\t\tComment = "Grunty / Юберрашунг passive signature (id must match CE)",
\t\t\t\t\tConfigurableKeybind = false,
\t\t\t\t\tDisplayName = T({PLACEHOLDER_T}, --[[ModItemCombatAction GruntyPerk_JAZZ DisplayName]] "<placeholder>"),
\t\t\t\t\tGetActionDescription = function (self, units)
\t\t\t\t\t\treturn GetSignatureActionDescription(self)
\t\t\t\t\tend,
\t\t\t\t\tGetActionDisplayName = function (self, units)
\t\t\t\t\t\treturn GetSignatureActionDisplayName(self)
\t\t\t\t\tend,
\t\t\t\t\tGetUIState = function (self, units, args)
\t\t\t\t\t\tlocal unit = units[1]
\t\t\t\t\t\tlocal cost = self:GetAPCost(unit, args)
\t\t\t\t\t\tif cost < 0 then return "hidden" end
\t\t\t\t\t\tif not unit:UIHasAP(cost) then return "disabled" end
\t\t\t\t\t\treturn "enabled"
\t\t\t\t\tend,
\t\t\t\t\tIcon = "UI/Icons/Hud/perk_grunty_perk",
\t\t\t\t\tIdDefault = "GruntyPerk_JAZZdefault",
\t\t\t\t\tIsAimableAttack = false,
\t\t\t\t\tKeybindingFromAction = "actionRedirectSignatureAbility",
\t\t\t\t\tRequireState = "any",
\t\t\t\t\tRun = function (self, unit, ap, ...)
\t\t\t\t\t\treturn false
\t\t\t\t\tend,
\t\t\t\t\tShowIn = "SignatureAbilities",
\t\t\t\t\tSortKey = 100,
\t\t\t\t\tgroup = "SignatureAbilities",
\t\t\t\t\tid = "GruntyPerk_JAZZ",
\t\t\t\t}}),
"""

BUFF_COMPANION = """UndefineClass('Grunty_AdditionalAP')
DefineClass.Grunty_AdditionalAP = {
	__parents = { "CharacterEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "CharacterEffect",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcStartTurnAP",
			Handler = function (self, target, value)
				if not self:ResolveValue("applied") then
					local ap = target:GetMaxActionPoints()
					return value + DivRound(ap,2)
				end
			end,
		}),
	},
	Conditions = {
		PlaceObj('CheckExpression', {
			Expression = function (self, obj) return g_Combat and IsKindOf(obj, "Unit") end,
		}),
	},
	DisplayName = T(952338905331, --[[ModItemCharacterEffectCompositeDef Grunty_AdditionalAP DisplayName]] "Überraschung"),
	Description = T(890000000001266, --[[ModItemCharacterEffectCompositeDef Grunty_AdditionalAP Description]] "Дает <em><bonus> ОД</em>."),
	OnAdded = function (self, obj)
		if g_Teams[g_CurrentTeam] == obj.team then
			local ap = obj:GetMaxActionPoints()
			obj:GainAP(DivRound(ap,2) )
			self:SetParameter("applied", true)
		end
	end,
	type = "Buff",
	lifetime = "Until End of Turn",
	Icon = "UI/Icons/Perks/GruntyPerk",
	RemoveOnEndCombat = true,
	Shown = true,
}
"""


def has_passive_ca(text: str) -> bool:
    # Find CombatAction with id GruntyPerk_JAZZ
    for m in re.finditer(
        r"PlaceObj\('ModItemCombatAction',\s*\{([\s\S]*?)\bid\s*=\s*\"GruntyPerk_JAZZ\"",
        text,
    ):
        if 'ActionType = "Passive"' in m.group(1):
            return True
    return False


def main() -> None:
    items = ITEMS.read_text(encoding="utf-8")
    if has_passive_ca(items):
        print("Passive CA already present")
    else:
        needle = (
            "\t\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {\n"
            "\t\t\t\t\t'Group', \"Perk-Personal\",\n"
            "\t\t\t\t\t'Id', \"GruntyPerk_JAZZ\","
        )
        if needle not in items:
            raise SystemExit("GruntyPerk_JAZZ CE block not found")
        items = items.replace(needle, PASSIVE_CA + needle, 1)
        print("Inserted Passive CA")

    # Fix AdditionalAP in items: remove OnBeginTurn reaction
    buff_pat = re.compile(
        r"(PlaceObj\('ModItemCharacterEffectCompositeDef', \{\s*"
        r"'Group', \"Perk-NPC\",\s*'Id', \"Grunty_AdditionalAP\",[\s\S]*?"
        r"'unit_reactions', \{)([\s\S]*?)(\n\t\t\t\t\t\},)",
        re.M,
    )

    def fix_buff_items(m: re.Match[str]) -> str:
        body = m.group(2)
        if "OnBeginTurn" not in body and "OnCalcStartTurnAP" in body:
            return m.group(0)
        only = """
						PlaceObj('UnitReaction', {
							Event = "OnCalcStartTurnAP",
							Handler = function (self, target, value)
								if not self:ResolveValue("applied") then
									local ap = target:GetMaxActionPoints()
									return value + DivRound(ap,2)
								end
							end,
							param_bindings = false,
						}),
					"""
        return m.group(1) + only + m.group(3)

    items2, n = buff_pat.subn(fix_buff_items, items, count=1)
    if n:
        items = items2
        print("Rewrote AdditionalAP unit_reactions in items")
    else:
        print("WARN: AdditionalAP block not rewritten")

    ITEMS.write_text(items, encoding="utf-8")
    CE_BUFF.write_text(BUFF_COMPANION, encoding="utf-8", newline="\n")
    print("Wrote companion Grunty_AdditionalAP.lua")

    meta = META.read_text(encoding="utf-8")
    ca_marker = (
        "'Class', \"CombatAction\",\n"
        "\t\t\t'Id', \"GruntyPerk_JAZZ\",\n"
        "\t\t\t'ClassDisplayName', \"Combat Actions\","
    )
    if ca_marker not in meta:
        ce_preset = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "CharacterEffectCompositeDef",
\t\t\t'Id', "GruntyPerk_JAZZ",
\t\t\t'ClassDisplayName', "Character effect",
\t\t}),"""
        ca_preset = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "CombatAction",
\t\t\t'Id', "GruntyPerk_JAZZ",
\t\t\t'ClassDisplayName', "Combat Actions",
\t\t}),
"""
        if ce_preset not in meta:
            raise SystemExit("metadata CE preset GruntyPerk_JAZZ missing")
        meta = meta.replace(ce_preset, ca_preset + ce_preset, 1)
        print("Inserted metadata CombatAction preset")
    else:
        print("metadata CombatAction preset already present")

    m = re.search(r"'version',\s*(\d+)", meta)
    if not m:
        raise SystemExit("version not found")
    ver = int(m.group(1))
    meta = meta[: m.start(1)] + str(ver + 1) + meta[m.end(1) :]
    print(f"version {ver} -> {ver + 1}")

    # Literal backslash-n in file (never a raw LF inside the quoted value).
    bullet = (
        "- UNITS-006: GruntyPerk_JAZZ — restore hotbar Passive CA (perk_grunty_perk); "
        "AdditionalAP no double GainAP; BD 10%×morale [no new game]"
        + "\\"
        + "n"
    )
    meta = re.sub(
        r"('last_changes',\s*\")",
        lambda m: m.group(1) + bullet,
        meta,
        count=1,
    )
    META.write_text(meta, encoding="utf-8")
    print("metadata updated")


if __name__ == "__main__":
    main()
