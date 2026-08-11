# -*- coding: utf-8 -*-
"""Insert Fidel DoubleTossAG–DG (GrenadesInventory) + metadata presets."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"

SLOTS = [
    ("DoubleTossAG", 1),
    ("DoubleTossBG", 2),
    ("DoubleTossCG", 3),
    ("DoubleTossDG", 4),
]


def ca_block(cid: str, x: int) -> str:
    return f"""\t\t\t\tPlaceObj('ModItemCombatAction', {{
\t\t\t\t\tActionPoints = 6000,
\t\t\t\t\tActionType = "Ranged Attack",
\t\t\t\t\tAimType = "parabola aoe",
\t\t\t\t\tAlwaysHits = true,
\t\t\t\t\tConfigurableKeybind = false,
\t\t\t\t\tDisplayName = T(355737085755, --[[ModItemCombatAction {cid} DisplayName]] "<placeholder>"),
\t\t\t\t\tGetAPCost = function (self, unit, args)
\t\t\t\t\t\tif self.CostBasedOnWeapon then
\t\t\t\t\t\t\tlocal weapon = self:GetAttackWeapons(unit)
\t\t\t\t\t\t\treturn weapon and unit:GetAttackAPCost(self, weapon, nil, args and args.aim or 0, self.ActionPointDelta) or -1
\t\t\t\t\t\tend
\t\t\t\t\t\treturn self.ActionPoints
\t\t\t\t\tend,
\t\t\t\t\tGetActionDamage = function (self, unit, target, args)
\t\t\t\t\t\tlocal weapon = self:GetAttackWeapons(unit)
\t\t\t\t\t\tlocal base = unit:GetBaseDamage(weapon)
\t\t\t\t\t\tlocal bonus = GetGrenadeDamageBonus(unit)
\t\t\t\t\t\treturn MulDivRound(base, Max(0, 100 + bonus), 100)
\t\t\t\t\tend,
\t\t\t\t\tGetActionDescription = function (self, units)
\t\t\t\t\t\tlocal action = {{id = "DoubleToss", Description = self.Description}}
\t\t\t\t\t\tlocal description = GetSignatureActionDescription(action)
\t\t\t\t\t\tlocal grenadeDescription = CombatActionGrenadeDescription(self, units)
\t\t\t\t\t\tdescription = description .. T(866574791377, "<newline><newline>") .. grenadeDescription
\t\t\t\t\t\treturn description
\t\t\t\t\tend,
\t\t\t\t\tGetActionDisplayName = function (self, units)
\t\t\t\t\t\tlocal action = {{id = "DoubleToss", DisplayName = self.DisplayName}}
\t\t\t\t\t\tlocal name = GetSignatureActionDisplayName(action)
\t\t\t\t\t\tlocal unit = units[1]
\t\t\t\t\t\tif unit then
\t\t\t\t\t\t\tlocal weapon = self:GetAttackWeapons(unit)
\t\t\t\t\t\t\tif weapon then
\t\t\t\t\t\t\t\tname = name .. T{{279081600107, " <name>", name = weapon.DisplayName}}
\t\t\t\t\t\t\tend
\t\t\t\t\t\tend
\t\t\t\t\t\treturn name
\t\t\t\t\tend,
\t\t\t\t\tGetActionIcon = function (self, units)
\t\t\t\t\t\treturn GetThrowItemIcon(self, units and units[1])
\t\t\t\t\tend,
\t\t\t\t\tGetActionResults = function (self, unit, args)
\t\t\t\t\t\treturn CombatActions.DoubleTossA.GetActionResults(self, unit, args)
\t\t\t\t\tend,
\t\t\t\t\tGetAttackWeapons = function (self, unit, args)
\t\t\t\t\t\treturn unit:GetItemInSlot("GrenadesInventory", "Grenade", {x}, 1)
\t\t\t\t\tend,
\t\t\t\t\tGetMaxAimRange = function (self, unit, weapon)
\t\t\t\t\t\treturn weapon:GetMaxAimRange(unit)
\t\t\t\t\tend,
\t\t\t\t\tGetUIState = function (self, units, args)
\t\t\t\t\t\treturn CombatActions.DoubleTossA.GetUIState(self, units, args)
\t\t\t\t\tend,
\t\t\t\t\tIcon = "UI/Icons/Hud/perk_double_toss",
\t\t\t\t\tIdDefault = "{cid}default",
\t\t\t\t\tIsAimableAttack = false,
\t\t\t\t\tKeybindingFromAction = "actionRedirectSignatureAbility",
\t\t\t\t\tMultiSelectBehavior = "first",
\t\t\t\t\tParameters = {{
\t\t\t\t\t\tPlaceObj('PresetParamPercent', {{
\t\t\t\t\t\t\t'Name', "target_offset",
\t\t\t\t\t\t\t'Value', 75,
\t\t\t\t\t\t\t'Tag', "<target_offset>%",
\t\t\t\t\t\t}}),
\t\t\t\t\t\tPlaceObj('PresetParamNumber', {{
\t\t\t\t\t\t\t'Name', "recharge_on_kill",
\t\t\t\t\t\t\t'Value', 1,
\t\t\t\t\t\t\t'Tag', "<recharge_on_kill>",
\t\t\t\t\t\t}}),
\t\t\t\t\t}},
\t\t\t\t\tRequireState = "any",
\t\t\t\t\tRun = function (self, unit, ap, ...)
\t\t\t\t\t\tunit:SetActionCommand("DoubleToss", self.id, ap, ...)
\t\t\t\t\tend,
\t\t\t\t\tShowIn = "SignatureAbilities",
\t\t\t\t\tSortKey = 100,
\t\t\t\t\tUIBegin = function (self, units, args)
\t\t\t\t\t\tCombatActionAttackStart(self, units, args, "IModeCombatAreaAim")
\t\t\t\t\tend,
\t\t\t\t\tgroup = "SignatureAbilities",
\t\t\t\t\tid = "{cid}",
\t\t\t\t}}),
"""


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    if 'id = "DoubleTossAG"' in text:
        print("items: DoubleTossAG already present")
    else:
        marker = '\t\t\t\t\tid = "ThrowGrenadeDG",\n\t\t\t\t}),\n'
        idx = text.find(marker)
        if idx < 0:
            raise SystemExit("ThrowGrenadeDG marker not found")
        insert_at = idx + len(marker)
        block = "".join(ca_block(cid, x) for cid, x in SLOTS)
        text = text[:insert_at] + block + text[insert_at:]
        ITEMS.write_text(text, encoding="utf-8", newline="\n")
        print("items: inserted DoubleTossAG–DG")

    meta = META.read_text(encoding="utf-8")
    if "'Id', \"DoubleTossAG\"" in meta:
        print("metadata: DoubleTossAG already present")
    else:
        needle = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', \"CombatAction\",
\t\t\t'Id', \"ThrowGrenadeDG\",
\t\t\t'ClassDisplayName', \"Combat Actions\",
\t\t}),"""
        insert = needle + "\n" + "\n".join(
            f"""\t\tPlaceObj('ModResourcePreset', {{
\t\t\t'Class', \"CombatAction\",
\t\t\t'Id', \"{cid}\",
\t\t\t'ClassDisplayName', \"Combat Actions\",
\t\t}}),"""
            for cid, _ in SLOTS
        )
        if needle not in meta:
            raise SystemExit("metadata ThrowGrenadeDG not found")
        meta = meta.replace(needle, insert, 1)
        print("metadata: presets added")

    m = re.search(r"'version',\s*(\d+)", meta)
    ver = int(m.group(1))
    if ver < 6132:
        meta = meta[: m.start(1)] + "6132" + meta[m.end(1) :]
        print(f"version {ver} -> 6132")

    marker = "'last_changes', \""
    idx = meta.find(marker)
    start = idx + len(marker)
    i = start
    while i < len(meta):
        if meta[i] == "\\" and i + 1 < len(meta):
            i += 2
            continue
        if meta[i] == '"':
            end = i
            break
        i += 1
    value = meta[start:end]
    bullet = "- UNITS-006: Fidel DoubleToss from GrenadesInventory pockets (DoubleTossAG–DG) [no new game]"
    if "DoubleToss from GrenadesInventory" not in value:
        value = bullet + "\\n" + value
        meta = meta[:start] + value + meta[end:]
        print("last_changes prepended")

    META.write_text(meta, encoding="utf-8", newline="\n")
    print("done")


if __name__ == "__main__":
    main()
