# -*- coding: utf-8 -*-
"""Restore Scope HawksEye JAZZ override (UNITS-006 + Bayun cookies 96h×7).

Does not bump metadata Revision / last_changes (commit-time).
"""
from __future__ import annotations

import csv
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"
RU = ROOT / "Russian.csv"
EN = ROOT / "English.csv"

DESC_ID = "890000000009870"
NAME_ID = "890000000009869"
DESC_RU = (
    "Со снайперской винтовкой: Overwatch за <overwatchCostOverwrite> ОД (остальные ОД остаются). "
    "Pin Down / Focus Fire — мин. <pindownCostOverwrite> ОД. Снайперские выстрелы дают ×2 подавления. "
    "Каждые <hoursToProduce> ч — <amountToProduce>× Печенье. При найме тоже печёт печенье (перезарядка сигнатур)."
)
DESC_EN = (
    "With a sniper rifle: Overwatch costs <overwatchCostOverwrite> AP (remaining AP kept). "
    "Pin Down / Focus Fire min <pindownCostOverwrite> AP. Sniper shots deal ×2 suppression. "
    "Every <hoursToProduce> h — <amountToProduce>× biscuits. Also bakes biscuits on hire (recharge signatures)."
)
NAME_RU = "Ястребиный глаз"
NAME_EN = "Eagle Eye"

LOC = {
    NAME_ID: (NAME_RU, NAME_EN, "jazz:CharacterEffect/HawksEye.lua"),
    DESC_ID: (DESC_RU, DESC_EN, "jazz:CharacterEffect/HawksEye.lua"),
}

OW_BRANCH = """\t\t\t\t\t\t-- Scope HawksEye: sniper Overwatch costs 1 AP (keep remaining AP).
\t\t\t\t\t\tif HasPerk(unit, "HawksEye") and IsKindOf(weapon, "SniperRifle") then
\t\t\t\t\t\t\tlocal ap = (CharacterEffectDefs.HawksEye and CharacterEffectDefs.HawksEye:ResolveValue("overwatchCostOverwrite") or 1) * const.Scale.AP
\t\t\t\t\t\t\treturn ap, ap
\t\t\t\t\t\tend
"""

HAWKSEYE_ITEM = f"""\t\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {{
\t\t\t\t\t'Group', "Perk-Personal",
\t\t\t\t\t'Id', "HawksEye",
\t\t\t\t\t'object_class', "Perk",
\t\t\t\t\t'Parameters', {{
\t\t\t\t\t\tPlaceObj('PresetParamNumber', {{
\t\t\t\t\t\t\t'Name', "pindownCostOverwrite",
\t\t\t\t\t\t\t'Value', 1,
\t\t\t\t\t\t\t'Tag', "<pindownCostOverwrite>",
\t\t\t\t\t\t}}),
\t\t\t\t\t\tPlaceObj('PresetParamNumber', {{
\t\t\t\t\t\t\t'Name', "overwatchCostOverwrite",
\t\t\t\t\t\t\t'Value', 1,
\t\t\t\t\t\t\t'Tag', "<overwatchCostOverwrite>",
\t\t\t\t\t\t}}),
\t\t\t\t\t\tPlaceObj('PresetParamNumber', {{
\t\t\t\t\t\t\t'Name', "hoursToProduce",
\t\t\t\t\t\t\t'Value', 96,
\t\t\t\t\t\t\t'Tag', "<hoursToProduce>",
\t\t\t\t\t\t}}),
\t\t\t\t\t\tPlaceObj('PresetParamNumber', {{
\t\t\t\t\t\t\t'Name', "amountToProduce",
\t\t\t\t\t\t\t'Value', 7,
\t\t\t\t\t\t\t'Tag', "<amountToProduce>",
\t\t\t\t\t\t}}),
\t\t\t\t\t\tPlaceObj('PresetParamNumber', {{
\t\t\t\t\t\t\t'Name', "nextProductionTime",
\t\t\t\t\t\t\t'Tag', "<nextProductionTime>",
\t\t\t\t\t\t}}),
\t\t\t\t\t}},
\t\t\t\t\t'Comment', "Scope: sniper OW 1 AP keep leftover; PinDown min 1; sniper suppress ×2; biscuits 96h×7 + hire",
\t\t\t\t\t'unit_reactions', {{
\t\t\t\t\t\tPlaceObj('UnitReaction', {{
\t\t\t\t\t\t\tEvent = "OnMercHired",
\t\t\t\t\t\t\tHandler = function (self, target, price, days, alreadyHired)
\t\t\t\t\t\t\t\tif days > 0 then
\t\t\t\t\t\t\t\t\tlocal canPlaceError = CanPlaceItemInInventory("Cookie", days, target)
\t\t\t\t\t\t\t\t\tif canPlaceError then
\t\t\t\t\t\t\t\t\t\tCombatLog("important", T(667077082306, "Scope has baked some biscuits. Unfortunately the inventory is full. "))
\t\t\t\t\t\t\t\t\t\treturn
\t\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\t\t\tCombatLog("important", T(754424382903, "Scope has baked some biscuits"))
\t\t\t\t\t\t\t\t\tPlaceItemInInventory("Cookie", days, target)
\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\tend,
\t\t\t\t\t\t}}),
\t\t\t\t\t\tPlaceObj('UnitReaction', {{
\t\t\t\t\t\t\tEvent = "OnNewHour",
\t\t\t\t\t\t\tHandler = function (self, target)
\t\t\t\t\t\t\t\tif target.HireStatus ~= "Hired" then return end

\t\t\t\t\t\t\t\tlocal next_production = self:ResolveValue("nextProductionTime")
\t\t\t\t\t\t\t\tif not next_production or next_production == 0 then
\t\t\t\t\t\t\t\t\tself:SetParameter("nextProductionTime", Game.CampaignTime + self:ResolveValue("hoursToProduce") * const.Scale.h)
\t\t\t\t\t\t\t\t\treturn
\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\t\tlocal squad = target.Squad and gv_Squads[target.Squad]
\t\t\t\t\t\t\t\tif Game.CampaignTime < next_production or (squad and squad.water_travel) then return end

\t\t\t\t\t\t\t\tlocal amountToProduce = self:ResolveValue("amountToProduce")
\t\t\t\t\t\t\t\tlocal cookie = g_Classes["Cookie"]
\t\t\t\t\t\t\t\tlocal item_name = cookie and (amountToProduce > 1 and cookie.DisplayNamePlural or cookie.DisplayName) or Untranslated("Cookie")
\t\t\t\t\t\t\t\tself:SetParameter("nextProductionTime", Game.CampaignTime + self:ResolveValue("hoursToProduce") * const.Scale.h)

\t\t\t\t\t\t\t\tlocal slots = {{ "Handheld A", "Handheld B", "Inventory" }}
\t\t\t\t\t\t\t\tlocal canPlaceError, amountLeft
\t\t\t\t\t\t\t\tlocal amountToPlace = amountToProduce
\t\t\t\t\t\t\t\tfor _, slot in ipairs(slots) do
\t\t\t\t\t\t\t\t\tcanPlaceError, amountLeft = CanPlaceItemInInventory("Cookie", amountToPlace, target, slot)
\t\t\t\t\t\t\t\t\tif not canPlaceError then
\t\t\t\t\t\t\t\t\t\tPlaceItemInInventory("Cookie", amountToPlace, target, nil, nil, slot)
\t\t\t\t\t\t\t\t\t\tif not amountLeft then
\t\t\t\t\t\t\t\t\t\t\tbreak
\t\t\t\t\t\t\t\t\t\telse
\t\t\t\t\t\t\t\t\t\t\tamountToPlace = amountLeft
\t\t\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\t\tend

\t\t\t\t\t\t\t\tlocal text = T{{318623454402, "<merc> produced <amount> <item_name>.", merc = target.Nick, amount = amountToProduce, item_name = item_name}}
\t\t\t\t\t\t\t\tif canPlaceError or (amountLeft and amountLeft > 0) then
\t\t\t\t\t\t\t\t\tamountToPlace = amountToPlace or amountToProduce
\t\t\t\t\t\t\t\t\tif squad and squad.CurrentSector then
\t\t\t\t\t\t\t\t\t\tPlaceItemInInventory("Cookie", amountToPlace, squad.CurrentSector)
\t\t\t\t\t\t\t\t\t\ttext = text .. T(447763084369, " Some were placed in the sector stash.")
\t\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\t\t\tCombatLog("important", text)
\t\t\t\t\t\t\t\telse
\t\t\t\t\t\t\t\t\tCombatLog("important", text)
\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\tend,
\t\t\t\t\t\t}}),
\t\t\t\t\t}},
\t\t\t\t\t'DisplayName', T({NAME_ID}, --[[ModItemCharacterEffectCompositeDef HawksEye DisplayName]] "{NAME_RU}"),
\t\t\t\t\t'Description', T({DESC_ID}, --[[ModItemCharacterEffectCompositeDef HawksEye Description]] "{DESC_RU}"),
\t\t\t\t\t'OnAdded', function (self, obj)
\t\t\t\t\t\tself:SetParameter("nextProductionTime", Game.CampaignTime + self:ResolveValue("hoursToProduce") * const.Scale.h)
\t\t\t\t\t\tend,
\t\t\t\t\t'Icon', "UI/Icons/Perks/HawksEye",
\t\t\t\t\t'Tier', "Personal",
\t\t\t\t}}),
"""

PRESET = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "CharacterEffectCompositeDef",
\t\t\t'Id', "HawksEye",
\t\t\t'ClassDisplayName', "Character effect",
\t\t}),
"""


def upsert_csv(path: Path, lang: str) -> None:
    raw = path.read_text(encoding="utf-8-sig")
    newline = "\r\n" if "\r\n" in raw else "\n"
    lines = raw.splitlines()
    by_id = {}
    for lid, (ru, en, ctx) in LOC.items():
        translation = ru if lang == "ru" else en
        fields = [lid, ru, translation, "", ctx]
        buf = io.StringIO()
        writer = csv.writer(buf, lineterminator="", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(fields)
        by_id[lid] = buf.getvalue()
    out = []
    seen = set()
    for line in lines:
        rid = line.split(",", 1)[0] if line else ""
        if rid in by_id:
            out.append(by_id[rid])
            seen.add(rid)
        else:
            out.append(line)
    for lid, row in by_id.items():
        if lid not in seen:
            out.append(row)
            print(f"{path.name} inserted {lid}")
        else:
            print(f"{path.name} updated {lid}")
    text = newline.join(out)
    if not text.endswith(newline):
        text += newline
    path.write_text(text, encoding="utf-8-sig")


def patch_items() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    ow_return = "\t\t\t\t\t\treturn Max(unit:GetUIActionPoints(), atk_cost), atk_cost\n"
    if "Scope HawksEye: sniper Overwatch costs 1 AP" in text:
        print("items.lua: Overwatch HawksEye branch already present")
    elif ow_return in text:
        text = text.replace(ow_return, OW_BRANCH + ow_return, 1)
        print("items.lua: inserted Overwatch HawksEye 1 AP branch")
    else:
        raise SystemExit("items.lua: Overwatch GetAPCost return not found")

    if "'Id', \"HawksEye\"" in text and "hoursToProduce" in text[text.find("'Id', \"HawksEye\"") : text.find("'Id', \"HawksEye\"") + 2500]:
        print("items.lua: HawksEye ModItem already present")
    elif "'Id', \"HawksEye\"" in text:
        raise SystemExit("items.lua: HawksEye ModItem exists without hoursToProduce — remove/replace first")
    else:
        needle = (
            "\t\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {\n"
            "\t\t\t\t\t'Group', \"Perk-Personal\",\n"
            "\t\t\t\t\t'Id', \"Nazdarovya\","
        )
        if needle not in text:
            raise SystemExit("items.lua: Nazdarovya ModItem anchor missing")
        text = text.replace(needle, HAWKSEYE_ITEM + needle, 1)
        print("items.lua: inserted HawksEye ModItem before Nazdarovya")

    ITEMS.write_text(text, encoding="utf-8")


def patch_metadata() -> None:
    text = META.read_text(encoding="utf-8")
    code = '\t\t"CharacterEffect/HawksEye.lua",\n'
    if '"CharacterEffect/HawksEye.lua"' in text:
        print("metadata.lua: HawksEye.lua already in code")
    else:
        anchor = '\t\t"CharacterEffect/DesignerExplosives.lua",\n'
        if anchor not in text:
            raise SystemExit("metadata.lua: DesignerExplosives.lua missing from code")
        text = text.replace(anchor, code + anchor, 1)
        print("metadata.lua: inserted CharacterEffect/HawksEye.lua")

    if "'Id', \"HawksEye\"" in text:
        print("metadata.lua: HawksEye preset already present")
    else:
        needle = (
            "\t\tPlaceObj('ModResourcePreset', {\n"
            "\t\t\t'Class', \"CharacterEffectCompositeDef\",\n"
            "\t\t\t'Id', \"GrizzlyPerk\",\n"
            "\t\t\t'ClassDisplayName', \"Character effect\",\n"
            "\t\t}),\n"
        )
        if needle not in text:
            raise SystemExit("metadata.lua: GrizzlyPerk CE preset anchor missing")
        text = text.replace(needle, needle + PRESET, 1)
        print("metadata.lua: inserted HawksEye ModResourcePreset")

    META.write_text(text, encoding="utf-8")


def main() -> None:
    patch_items()
    patch_metadata()
    upsert_csv(RU, "ru")
    upsert_csv(EN, "en")
    print("HawksEye restore apply done")


if __name__ == "__main__":
    main()
