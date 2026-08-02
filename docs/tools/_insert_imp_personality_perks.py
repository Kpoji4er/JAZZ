# -*- coding: utf-8 -*-
"""Insert Jazz_Perk_Mimicry/Veteran/Sniper into Personality folder of items.lua."""
from pathlib import Path

path = Path(r"C:/Users/SsAnd/AppData/Roaming/Jagged Alliance 3/Mods/jazz/items.lua")
text = path.read_text(encoding="utf-8")

if "'Id', \"Jazz_Perk_Mimicry\"" in text:
    print("already present")
    raise SystemExit(0)

marker = """\t\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {
\t\t\t\t\t'Group', \"Perk-Personality\",
\t\t\t\t\t'Id', \"Scoundrel\",
\t\t\t\t\t'SortKey', 10,
\t\t\t\t\t'object_class', \"Perk\",
\t\t\t\t\t'DisplayName', T(687227379969, --[[ModItemCharacterEffectCompositeDef Scoundrel DisplayName]] \"Scoundrel\"),
\t\t\t\t\t'Description', T(252249063178, --[[ModItemCharacterEffectCompositeDef Scoundrel Description]] \"First <em>weapon swap</em> for the turn is <em>free</em>.\\n\\nAdditional <em>conversation options</em>.\"),
\t\t\t\t\t'Icon', \"UI/Icons/Perks/Scoundrel\",
\t\t\t\t\t'Tier', \"Personality\",
\t\t\t\t}),
"""

# tolerate weird whitespace before Loner
import re

pat = re.compile(
    r"(PlaceObj\('ModItemCharacterEffectCompositeDef',\s*\{\s*"
    r"'Group',\s*\"Perk-Personality\",\s*"
    r"'Id',\s*\"Scoundrel\",.*?"
    r"'Tier',\s*\"Personality\",\s*"
    r"\}\),\s*)"
    r"\t*PlaceObj\('ModItemCharacterEffectCompositeDef',\s*\{\s*"
    r"'Group',\s*\"Quirk\",\s*"
    r"'Id',\s*\"Loner\",",
    re.S,
)

m = pat.search(text)
if not m:
    print("FAIL: Scoundrel→Loner anchor not found")
    raise SystemExit(1)

insert = m.group(1) + """\t\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {
\t\t\t\t\t'Group', \"Perk-Personality\",
\t\t\t\t\t'Id', \"Jazz_Perk_Mimicry\",
\t\t\t\t\t'SortKey', 20,
\t\t\t\t\t'object_class', \"Perk\",
\t\t\t\t\t'DisplayName', T(890000000001931, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Mimicry DisplayName]] \"Мимикрия\"),
\t\t\t\t\t'Description', T(890000000001932, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Mimicry Description]] \"Проходит проверки на разговорные перки <em>Переговорщик</em>, <em>Тёртый калач</em> и <em>Псих</em> без их боевых и экономических эффектов.\"),
\t\t\t\t\t'Icon', \"UI/Icons/Perks/Bond\",
\t\t\t\t\t'Tier', \"Personality\",
\t\t\t\t}),
\t\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {
\t\t\t\t\t'Group', \"Perk-Personality\",
\t\t\t\t\t'Id', \"Jazz_Perk_Veteran\",
\t\t\t\t\t'SortKey', 21,
\t\t\t\t\t'object_class', \"Perk\",
\t\t\t\t\t'DisplayName', T(890000000001933, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Veteran DisplayName]] \"Ветеран\"),
\t\t\t\t\t'Description', T(890000000001934, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Veteran Description]] \"Бонус <em>+10</em> ко всем проверкам навыков и характеристик (диалоги, исследование, skill checks).\"),
\t\t\t\t\t'Icon', \"UI/Icons/Perks/Teacher\",
\t\t\t\t\t'Tier', \"Personality\",
\t\t\t\t}),
\t\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {
\t\t\t\t\t'Group', \"Perk-Personality\",
\t\t\t\t\t'Id', \"Jazz_Perk_Sniper\",
\t\t\t\t\t'SortKey', 22,
\t\t\t\t\t'object_class', \"Perk\",
\t\t\t\t\t'unit_reactions', {
\t\t\t\t\t\tPlaceObj('UnitReaction', {
\t\t\t\t\t\t\tEvent = \"OnCalcMaxAimActions\",
\t\t\t\t\t\t\tHandler = function(self, value, attacker, target, action, weapon)
\t\t\t\t\t\t\t\treturn value + 1
\t\t\t\t\t\t\tend,
\t\t\t\t\t\t}),
\t\t\t\t\t},
\t\t\t\t\t'DisplayName', T(890000000001935, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Sniper DisplayName]] \"Снайпер\"),
\t\t\t\t\t'Description', T(890000000001936, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Sniper Description]] \"Максимальный уровень прицеливания <em>+1</em> при стрельбе из любого оружия.\"),
\t\t\t\t\t'Icon', \"UI/Icons/Perks/Deadeye\",
\t\t\t\t\t'Tier', \"Personality\",
\t\t\t\t}),
\t\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {
\t\t\t\t\t'Group', \"Quirk\",
\t\t\t\t\t'Id', \"Loner\","""

new_text = text[: m.start()] + insert + text[m.end() :]
path.write_text(new_text, encoding="utf-8")
print("inserted OK, new size", len(new_text))
for i in ("Jazz_Perk_Mimicry", "Jazz_Perk_Veteran", "Jazz_Perk_Sniper"):
    print(i, "'Id', \"%s\"" % i in new_text)
