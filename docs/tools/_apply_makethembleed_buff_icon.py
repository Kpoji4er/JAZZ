# -*- coding: utf-8 -*-
"""UNITS-006 Flay: status buff icon showing count of visible bleeding enemies.

- New CE Jazz_MakeThemBleedBuff (max_stacks 5, Shown, bloodthirst icon)
- Sync stacks from GetVisibleEnemies with any Bleeding* effect
- MakeThemBleed damage uses shared count helper; sync on BeginTurn + CombatActionEnd
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"
CE_PERK = ROOT / "CharacterEffect" / "MakeThemBleed.lua"
CE_BUFF = ROOT / "CharacterEffect" / "Jazz_MakeThemBleedBuff.lua"
NAMED = ROOT / "Code" / "System_NamedPerks.lua"
EN = ROOT / "English.csv"
RU = ROOT / "Russian.csv"
ICON_SRC = ROOT / "Icons" / "StatusEffects" / "references" / "bloodthirst.png"
ICON_DST = ROOT / "Icons" / "StatusEffects" / "Jazz_MakeThemBleedBuff.png"

DN_ID = "890000000009863"
DESC_ID = "890000000009864"

DN_RU = "Кровавый след"
DN_EN = "Blood Trail"
DESC_RU = (
    "Видимые враги с кровотечением: <em><stacks></em> "
    "(+10% урона за каждого, макс. +50%)."
)
DESC_EN = (
    "Visible bleeding enemies: <em><stacks></em> "
    "(+10% damage each, cap +50%)."
)

BUFF_CE = f'''UndefineClass('Jazz_MakeThemBleedBuff')
DefineClass.Jazz_MakeThemBleedBuff = {{
	__parents = {{ "CharacterEffect" }},
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "CharacterEffect",
	DisplayName = T({DN_ID}, --[[ModItemCharacterEffectCompositeDef Jazz_MakeThemBleedBuff DisplayName]] "{DN_RU}"),
	Description = T({DESC_ID}, --[[ModItemCharacterEffectCompositeDef Jazz_MakeThemBleedBuff Description]] "{DESC_RU}"),
	type = "Buff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/Jazz_MakeThemBleedBuff.png",
	max_stacks = 5,
	RemoveOnEndCombat = true,
	Shown = true,
}}
'''

PERK_CE = '''UndefineClass('MakeThemBleed')
DefineClass.MakeThemBleed = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function (self, target)
				if type(Jazz_MakeThemBleedSyncBuff) == "function" then
					Jazz_MakeThemBleedSyncBuff(target)
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcDamageAndEffects",
			Handler = function (self, owner, attacker, target, action, weapon, attack_args, hit, data)
				if owner ~= attacker or not data then
					return
				end
				local n = 0
				if type(Jazz_MakeThemBleedCountVisible) == "function" then
					n = Jazz_MakeThemBleedCountVisible(attacker) or 0
				end
				local bonus = Min(50, n * 10)
				if bonus > 0 then
					data.damage_percent = (data.damage_percent or 100) + bonus
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnUnitAttack",
			Handler = function (self, target, attacker, action, attack_target, results, attack_args)
				-- Refresh after Flay's attack (bleed may have been applied).
				if target == attacker and type(Jazz_MakeThemBleedSyncBuff) == "function" then
					Jazz_MakeThemBleedSyncBuff(attacker)
				end
			end,
		}),
	},
	DisplayName = T(890000000009861, --[[ModItemCharacterEffectCompositeDef MakeThemBleed DisplayName]] "Пусть кровоточат"),
	Description = T(890000000009862, --[[ModItemCharacterEffectCompositeDef MakeThemBleed Description]] "Удары в пах и по животным вызывают кровотечение. +10% урона за каждого врага с кровотечением в зоне видимости (макс. +50%)."),
	Icon = "UI/Icons/Perks/MakeThemBleed",
	Tier = "Personal",
}
'''

HELPERS = r'''
--- Flay MakeThemBleed: count distinct visible enemies with any bleeding tier.
function Jazz_MakeThemBleedCountVisible(unit)
	if not unit or not unit.GetVisibleEnemies then
		return 0
	end
	local n = 0
	for _, u in ipairs(unit:GetVisibleEnemies() or empty_table) do
		if IsValid(u) and not (u.IsDead and u:IsDead()) then
			if u:HasStatusEffect("Bleeding")
				or u:HasStatusEffect("BleedingMedium")
				or u:HasStatusEffect("BleedingHeavy")
			then
				n = n + 1
			end
		end
	end
	return n
end

--- HUD stacks = min(5, visible bleeders); remove buff when 0.
function Jazz_MakeThemBleedSyncBuff(unit)
	if not unit or not HasPerk(unit, "MakeThemBleed") then
		return false
	end
	if not g_Combat then
		if unit.HasStatusEffect and unit:HasStatusEffect("Jazz_MakeThemBleedBuff") then
			unit:RemoveStatusEffect("Jazz_MakeThemBleedBuff", "all")
		end
		return false
	end
	local n = Min(5, Jazz_MakeThemBleedCountVisible(unit) or 0)
	if unit.HasStatusEffect and unit:HasStatusEffect("Jazz_MakeThemBleedBuff") then
		unit:RemoveStatusEffect("Jazz_MakeThemBleedBuff", "all")
	end
	if n <= 0 then
		return false
	end
	unit:AddStatusEffect("Jazz_MakeThemBleedBuff", n)
	return true
end

function Jazz_MakeThemBleedSyncAll()
	local units = g_Units or empty_table
	for _, u in pairs(units) do
		if IsValid(u) and HasPerk(u, "MakeThemBleed") then
			Jazz_MakeThemBleedSyncBuff(u)
		end
	end
end
'''

ITEMS_BUFF = f"""\t\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {{
\t\t\t\t\t'Group', "System",
\t\t\t\t\t'Id', "Jazz_MakeThemBleedBuff",
\t\t\t\t\t'object_class', "CharacterEffect",
\t\t\t\t\t'DisplayName', T({DN_ID}, --[[ModItemCharacterEffectCompositeDef Jazz_MakeThemBleedBuff DisplayName]] "{DN_RU}"),
\t\t\t\t\t'Description', T({DESC_ID}, --[[ModItemCharacterEffectCompositeDef Jazz_MakeThemBleedBuff Description]] "{DESC_RU}"),
\t\t\t\t\t'type', "Buff",
\t\t\t\t\t'Icon', "Mod/e6L4ECj/Icons/StatusEffects/Jazz_MakeThemBleedBuff.png",
\t\t\t\t\t'max_stacks', 5,
\t\t\t\t\t'RemoveOnEndCombat', true,
\t\t\t\t\t'Shown', true,
\t\t\t\t}}),
"""

ITEMS_PERK = f"""\t\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {{
\t\t\t\t\t'Group', "Perk-Personal",
\t\t\t\t\t'Id', "MakeThemBleed",
\t\t\t\t\t'object_class', "Perk",
\t\t\t\t\t'unit_reactions', {{
\t\t\t\t\t\tPlaceObj('UnitReaction', {{
\t\t\t\t\t\t\tEvent = "OnBeginTurn",
\t\t\t\t\t\t\tHandler = function (self, target)
\t\t\t\t\t\t\t\tif type(Jazz_MakeThemBleedSyncBuff) == "function" then
\t\t\t\t\t\t\t\t\tJazz_MakeThemBleedSyncBuff(target)
\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\tend,
\t\t\t\t\t\t}}),
\t\t\t\t\t\tPlaceObj('UnitReaction', {{
\t\t\t\t\t\t\tEvent = "OnCalcDamageAndEffects",
\t\t\t\t\t\t\tHandler = function (self, owner, attacker, target, action, weapon, attack_args, hit, data)
\t\t\t\t\t\t\t\tif owner ~= attacker or not data then
\t\t\t\t\t\t\t\t\treturn
\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\t\tlocal n = 0
\t\t\t\t\t\t\t\tif type(Jazz_MakeThemBleedCountVisible) == "function" then
\t\t\t\t\t\t\t\t\tn = Jazz_MakeThemBleedCountVisible(attacker) or 0
\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\t\tlocal bonus = Min(50, n * 10)
\t\t\t\t\t\t\t\tif bonus > 0 then
\t\t\t\t\t\t\t\t\tdata.damage_percent = (data.damage_percent or 100) + bonus
\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\tend,
\t\t\t\t\t\t}}),
\t\t\t\t\t\tPlaceObj('UnitReaction', {{
\t\t\t\t\t\t\tEvent = "OnUnitAttack",
\t\t\t\t\t\t\tHandler = function (self, target, attacker, action, attack_target, results, attack_args)
\t\t\t\t\t\t\t\tif target == attacker and type(Jazz_MakeThemBleedSyncBuff) == "function" then
\t\t\t\t\t\t\t\t\tJazz_MakeThemBleedSyncBuff(attacker)
\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\tend,
\t\t\t\t\t\t}}),
\t\t\t\t\t}},
\t\t\t\t\t'DisplayName', T(890000000009861, --[[ModItemCharacterEffectCompositeDef MakeThemBleed DisplayName]] "Пусть кровоточат"),
\t\t\t\t\t'Description', T(890000000009862, --[[ModItemCharacterEffectCompositeDef MakeThemBleed Description]] "Удары в пах и по животным вызывают кровотечение. +10% урона за каждого врага с кровотечением в зоне видимости (макс. +50%)."),
\t\t\t\t\t'Icon', "UI/Icons/Perks/MakeThemBleed",
\t\t\t\t\t'Tier', "Personal",
\t\t\t\t}}),
"""


def upsert_csv(path: Path, tid: str, ru: str, en: str, source: str) -> None:
    text = path.read_text(encoding="utf-8")

    def esc(s: str) -> str:
        if any(c in s for c in ',"\n'):
            return '"' + s.replace('"', '""') + '"'
        return s

    row = f"{tid},{esc(ru)},{esc(en)},,{source}"
    pat = re.compile(rf"(?m)^{re.escape(tid)},.*$")
    if pat.search(text):
        text = pat.sub(row, text, count=1)
    else:
        if not text.endswith("\n"):
            text += "\n"
        text += row + "\n"
    path.write_text(text, encoding="utf-8")


def main() -> None:
    if ICON_SRC.exists() and not ICON_DST.exists():
        shutil.copy2(ICON_SRC, ICON_DST)
        print("Copied status icon")
    elif ICON_DST.exists():
        print("Status icon already present")
    else:
        print("WARN: no bloodthirst reference; Icon path still wired")

    CE_BUFF.write_text(BUFF_CE, encoding="utf-8", newline="\n")
    CE_PERK.write_text(PERK_CE, encoding="utf-8", newline="\n")
    print("Wrote CE companions")

    items = ITEMS.read_text(encoding="utf-8")
    perk_pat = re.compile(
        r"PlaceObj\('ModItemCharacterEffectCompositeDef', \{\s*"
        r"'Group', \"Perk-Personal\",\s*'Id', \"MakeThemBleed\",[\s\S]*?"
        r"'Tier', \"Personal\",\s*\}\),",
        re.M,
    )
    items2, n = perk_pat.subn(ITEMS_PERK.rstrip() + "\n", items, count=1)
    if not n:
        raise SystemExit("MakeThemBleed ModItem not found")
    items = items2
    print("Replaced MakeThemBleed ModItem")

    if "'Id', \"Jazz_MakeThemBleedBuff\"" not in items:
        # insert buff ModItem right after MakeThemBleed CE
        needle = ITEMS_PERK.rstrip() + "\n"
        # after replace, find the closing of MakeThemBleed and insert after
        m = re.search(
            r"('Id', \"MakeThemBleed\",[\s\S]*?'Tier', \"Personal\",\s*\}\),)",
            items,
        )
        if not m:
            raise SystemExit("cannot find MakeThemBleed for buff insert")
        items = items[: m.end()] + "\n" + ITEMS_BUFF + items[m.end() :]
        print("Inserted Jazz_MakeThemBleedBuff ModItem")
    else:
        print("Buff ModItem already present")

    ITEMS.write_text(items, encoding="utf-8")

    named = NAMED.read_text(encoding="utf-8")
    if "function Jazz_MakeThemBleedCountVisible" not in named:
        anchor = "-- Soft lock EV −25% med consume"
        if anchor not in named:
            raise SystemExit("NamedPerks anchor missing")
        named = named.replace(anchor, HELPERS.strip() + "\n\n" + anchor, 1)
        print("Inserted MakeThemBleed helpers")
    else:
        print("Helpers already present")

    # Sync all Flays on combat/turn start (visibility + bleed changes between turns).
    if "Jazz_MakeThemBleedSyncAll()" not in named:
        named = named.replace(
            "function Jazz_NamedPerks006OnCombatStart()\n"
            "\tlNamedPerks006OnCombatStart_Signatures()\n"
            "\tlNamedPerks006OnCombatStart_Economy()\n"
            "\tlNamedPerks006OnCombatStart_Satellite()\n"
            "\tlNamedPerks006OnCombatStart_SectionD()\n"
            "end",
            "function Jazz_NamedPerks006OnCombatStart()\n"
            "\tlNamedPerks006OnCombatStart_Signatures()\n"
            "\tlNamedPerks006OnCombatStart_Economy()\n"
            "\tlNamedPerks006OnCombatStart_Satellite()\n"
            "\tlNamedPerks006OnCombatStart_SectionD()\n"
            "\tif type(Jazz_MakeThemBleedSyncAll) == \"function\" then\n"
            "\t\tJazz_MakeThemBleedSyncAll()\n"
            "\tend\n"
            "end",
            1,
        )
        named = named.replace(
            "function Jazz_NamedPerks006OnTurnStart()\n"
            "\tlNamedPerks006OnTurnStart_Signatures()\n"
            "\tlNamedPerks006OnTurnStart_Economy()\n"
            "\tlNamedPerks006OnTurnStart_Satellite()\n"
            "end",
            "function Jazz_NamedPerks006OnTurnStart()\n"
            "\tlNamedPerks006OnTurnStart_Signatures()\n"
            "\tlNamedPerks006OnTurnStart_Economy()\n"
            "\tlNamedPerks006OnTurnStart_Satellite()\n"
            "\tif type(Jazz_MakeThemBleedSyncAll) == \"function\" then\n"
            "\t\tJazz_MakeThemBleedSyncAll()\n"
            "\tend\n"
            "end",
            1,
        )
        print("Wired combat/turn sync")
    NAMED.write_text(named, encoding="utf-8", newline="\n")

    # metadata: code path + preset
    meta = META.read_text(encoding="utf-8")
    if '"CharacterEffect/Jazz_MakeThemBleedBuff.lua"' not in meta:
        meta = meta.replace(
            '"CharacterEffect/MakeThemBleed.lua",',
            '"CharacterEffect/MakeThemBleed.lua",\n\t\t"CharacterEffect/Jazz_MakeThemBleedBuff.lua",',
            1,
        )
        print("metadata.code path added")

    if "'Id', \"Jazz_MakeThemBleedBuff\"" not in meta:
        presets = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "CharacterEffectCompositeDef",
\t\t\t'Id', "Jazz_MakeThemBleedBuff",
\t\t\t'ClassDisplayName', "Character effect",
\t\t}),
"""
        needle = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "CharacterEffectCompositeDef",
\t\t\t'Id', "GruntyPerk",
\t\t\t'ClassDisplayName', "Character effect",
\t\t}),"""
        if needle not in meta:
            raise SystemExit("GruntyPerk preset needle missing for buff preset")
        meta = meta.replace(needle, presets + needle, 1)
        print("metadata preset added")

    m = re.search(r"'version',\s*(\d+)", meta)
    ver = int(m.group(1))
    meta = meta[: m.start(1)] + str(ver + 1) + meta[m.end(1) :]
    bullet = (
        "- UNITS-006: Flay MakeThemBleed — HUD buff stacks = visible bleeding enemies "
        "(cap 5) [no new game]"
        + "\\"
        + "n"
    )
    if "MakeThemBleed — HUD" not in meta.split("'last_changes'")[1][:500]:
        meta = re.sub(r"('last_changes',\s*\")", lambda mm: mm.group(1) + bullet, meta, count=1)
    META.write_text(meta, encoding="utf-8")
    print(f"version {ver} -> {ver + 1}")

    upsert_csv(EN, DN_ID, DN_RU, DN_EN, "jazz:CharacterEffect/Jazz_MakeThemBleedBuff.lua")
    upsert_csv(RU, DN_ID, DN_RU, DN_EN, "jazz:CharacterEffect/Jazz_MakeThemBleedBuff.lua")
    upsert_csv(EN, DESC_ID, DESC_RU, DESC_EN, "jazz:CharacterEffect/Jazz_MakeThemBleedBuff.lua")
    upsert_csv(RU, DESC_ID, DESC_RU, DESC_EN, "jazz:CharacterEffect/Jazz_MakeThemBleedBuff.lua")
    print("Loc updated")


if __name__ == "__main__":
    main()
