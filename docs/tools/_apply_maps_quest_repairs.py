#!/usr/bin/env python3
"""Apply the generated-data part of JAZZ-QUESTS-001.

Map object exports are intentionally excluded: they must be saved by JA3 Map
Editor. This script updates the source-aware ModItem graph and the three
generated companions owned by the affected presets.
"""

from __future__ import annotations

import argparse
import csv
import io
import re
from pathlib import Path


CORE_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MAPS_ROOT = CORE_ROOT.parent / "jazz-maps"


def replace_exact(
    text: str,
    old: str,
    new: str,
    label: str,
    *,
    expected: int = 1,
) -> str:
    count = text.count(old)
    if count == expected:
        return text.replace(old, new)
    if old != new and text.count(new) == expected:
        print(f"skip (already applied): {label}")
        return text
    raise RuntimeError(f"{label}: expected {expected} source match(es), found {count}")


def replace_regex(
    text: str,
    pattern: str,
    replacement: str,
    label: str,
    *,
    expected: int = 1,
    already_pattern: str | None = None,
) -> str:
    patched, count = re.subn(pattern, replacement, text, flags=re.MULTILINE)
    if count == expected:
        return patched
    if already_pattern and len(re.findall(already_pattern, text, flags=re.MULTILINE)) == expected:
        print(f"skip (already applied): {label}")
        return text
    raise RuntimeError(f"{label}: expected {expected} source match(es), found {count}")


def patch_items(text: str) -> str:
    applied_markers = (
        'AssignToGroup = "BarrySeal_Recruit"',
        'ParamId = "TCE_HostageDead"',
        'Prop = "SuppliesDelivered"',
        'Name = "AdvancePaid"',
        'Text = T(890000000013004, --[[ModItemQuestsDef RescueHerMan Text]]',
        'DisplayName = T(890000000013000, --[[ModItemQuestsDef Jazz_Alkatraz DisplayName]]',
        '\'Icon\', "Mod/FhNNYd/Images/Inventory_Images/AmmoCrate.png",\n'
        '\t\t\'SubIcon\', "Mod/FhNNYd/Images/Inventory_Images/AmmoCrate.png",\n'
        '\t\t\'DisplayName\', T(732750682366',
    )
    if all(marker in text for marker in applied_markers):
        print("skip (already applied): jazz-maps/items.lua quest repairs")
        return text

    # J7's two generated sector representations both lost the vanilla
    # EncounterHerman on-enter event when I3 was remapped to J7.
    event = """\
\t\t\t\t\t'Events', {
\t\t\t\t\t\tPlaceObj('SE_OnEnterMapVisual', {
\t\t\t\t\t\t\t'Conditions', {
\t\t\t\t\t\t\t\tPlaceObj('QuestIsVariableBool', {
\t\t\t\t\t\t\t\t\tQuestId = "RescueHerMan",
\t\t\t\t\t\t\t\t\tVars = set({
\tFailed = false,
\tHermanRescued = false,
}),
\t\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\t},
\t\t\t\t\t\t\t'SequentialEffects', true,
\t\t\t\t\t\t\t'Effects', {
\t\t\t\t\t\t\t\tPlaceObj('NeutralNPCDontMove', {
\t\t\t\t\t\t\t\t\tTargetUnit = "Herman",
\t\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\t\tPlaceObj('PlaySetpiece', {
\t\t\t\t\t\t\t\t\tsetpiece = "EncounterHerman",
\t\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\t},
\t\t\t\t\t\t}),
\t\t\t\t\t},
"""
    for loc_line in (
        '\t\t\t\t\t\'display_name\', T(468789385226, "Emerald Coast"),\n',
        '\t\t\t\t\t\'display_name\', T(890000000001523, --[[ModItemCampaignPreset HotDiamonds display_name Sector name for J7]] "Emerald Coast"),\n',
    ):
        old = (
            loc_line
            + '\t\t\t\t\t\'TerrainType\', "Jungle",\n'
            + '\t\t\t\t\t\'WeatherZone\', "Erny",\n'
            + "\t\t\t\t\t'MaxFlareCarriers', 5,\n"
        )
        new = old + event
        text = replace_exact(text, old, new, "restore J7 EncounterHerman event")

    text = replace_exact(
        text,
        '\t\t\t\t\t\trequiredSectors = {\n\t\t\t\t\t\t\t"I3",\n\t\t\t\t\t\t},\n',
        '\t\t\t\t\t\trequiredSectors = {\n\t\t\t\t\t\t\t"J7",\n\t\t\t\t\t\t},\n',
        "align RescueHerMan required sector",
    )
    text = replace_exact(
        text,
        'custom_code = "if gv_Sectors.H14.conflict then gv_Sectors.H14.conflict.locked = false end"',
        'custom_code = "if gv_Sectors.P17.conflict then gv_Sectors.P17.conflict.locked = false end"',
        "unlock the P17 reinforcement conflict",
    )
    text = replace_exact(
        text,
        'Text = T(706580608154, --[[ModItemQuestsDef RescueHerMan Text]] "<em>Martha</em> is looking for her husband who was kidnapped by the <em>Legion</em> and was last seen on the <em><SectorName(\'M7\')></em>"),',
        'Text = T(890000000013004, --[[ModItemQuestsDef RescueHerMan Text]] "<em>Martha</em> is looking for her husband who was kidnapped by the <em>Legion</em> and was last seen on the <em><SectorName(\'J7\')></em>"),',
        "correct RescueHerMan journal sector",
    )

    # Kiki is required for SaveMyFamily completion.
    text = replace_exact(
        text,
        "\t\t\t\t\t'Name', T(356243372579, --[[ModItemUnitDataCompositeDef JAZZ_Ernie_Locals_M2_SaveMyFamily_Woman Name]] \"Кики\"),\n"
        '\t\t\t\t\t\'Affiliation\', "Civilian",\n',
        "\t\t\t\t\t'Name', T(356243372579, --[[ModItemUnitDataCompositeDef JAZZ_Ernie_Locals_M2_SaveMyFamily_Woman Name]] \"Кики\"),\n"
        "\t\t\t\t\t'immortal', true,\n"
        "\t\t\t\t\t'ImportantNPC', true,\n"
        '\t\t\t\t\t\'Affiliation\', "Civilian",\n',
        "protect Kiki quest NPC",
    )
    text = replace_exact(
        text,
        """\
\t\t\t\t\t\t\t\t\tEffects = {
\t\t\t\t\t\t\t\t\t\tPlaceObj('CityGrantLoyalty', {
\t\t\t\t\t\t\t\t\t\t\tAmount = -20,
""",
        """\
\t\t\t\t\t\t\t\t\tAutoRemove = true,
\t\t\t\t\t\t\t\t\tEffects = {
\t\t\t\t\t\t\t\t\t\tPlaceObj('UnitGrantItem', {
\t\t\t\t\t\t\t\t\t\t\tItemId = "BigDiamond",
\t\t\t\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\t\t\t\tPlaceObj('CityGrantLoyalty', {
\t\t\t\t\t\t\t\t\t\t\tAmount = -20,
""",
        "grant the Psycho-path diamond once",
    )
    text = replace_exact(
        text,
        """\
\t\t\t\t\t\tLines = {
\t\t\t\t\t\t\tPlaceObj('ConversationLine', {
\t\t\t\t\t\t\t\tCharacter = "JAZZ_Ernie_Locals_M2_SaveMyFamily_Woman",
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\tid = "Goodbye2",
""",
        """\
\t\t\t\t\t\tid = "Goodbye2",
""",
        "remove Kiki's empty goodbye line",
    )

    # Dead Pigs: a single advance and a single accepted reward path.
    text = replace_exact(
        text,
        """\
\t\t\t\t\t\tConditions = {
\t\t\t\t\t\t\tPlaceObj('QuestIsVariableBool', {
\t\t\t\t\t\t\t\tQuestId = "Jazz_DeadPigs",
\t\t\t\t\t\t\t\tVars = set( "NotStarted" ),
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\tEffects = {
\t\t\t\t\t\t\tPlaceObj('UnitGrantItem', {
\t\t\t\t\t\t\t\tItemId = "DiamondBriefcase",
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
""",
        """\
\t\t\t\t\t\tConditions = {
\t\t\t\t\t\t\tPlaceObj('QuestIsVariableBool', {
\t\t\t\t\t\t\t\tQuestId = "Jazz_DeadPigs",
\t\t\t\t\t\t\t\tVars = set( "NotStarted" ),
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\tPlaceObj('QuestIsVariableBool', {
\t\t\t\t\t\t\t\tQuestId = "Jazz_DeadPigs",
\t\t\t\t\t\t\t\tVars = set({
\tAdvancePaid = false,
}),
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\tEffects = {
\t\t\t\t\t\t\tPlaceObj('UnitGrantItem', {
\t\t\t\t\t\t\t\tItemId = "DiamondBriefcase",
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\tPlaceObj('QuestSetVariableBool', {
\t\t\t\t\t\t\t\tProp = "AdvancePaid",
\t\t\t\t\t\t\t\tQuestId = "Jazz_DeadPigs",
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
""",
        "guard the Dead Pigs advance",
    )
    text = replace_exact(
        text,
        """\
\t\t\t\t\t\t\t\t\tPlaceObj('ConversationPhrase', {
\t\t\t\t\t\t\t\t\t\tEffects = {
\t\t\t\t\t\t\t\t\t\t\tPlaceObj('UnitGrantItem', {
""",
        """\
\t\t\t\t\t\t\t\t\tPlaceObj('ConversationPhrase', {
\t\t\t\t\t\t\t\t\t\tAutoRemove = true,
\t\t\t\t\t\t\t\t\t\tConditions = {
\t\t\t\t\t\t\t\t\t\t\tPlaceObj('QuestIsVariableBool', {
\t\t\t\t\t\t\t\t\t\t\t\tQuestId = "Jazz_DeadPigs",
\t\t\t\t\t\t\t\t\t\t\t\tVars = set({
\tAccepted = false,
\tGiven = false,
}),
\t\t\t\t\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\t\t\t\t},
\t\t\t\t\t\t\t\t\t\tEffects = {
\t\t\t\t\t\t\t\t\t\t\tPlaceObj('QuestSetVariableBool', {
\t\t\t\t\t\t\t\t\t\t\t\tProp = "Accepted",
\t\t\t\t\t\t\t\t\t\t\t\tQuestId = "Jazz_DeadPigs",
\t\t\t\t\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\t\t\t\t\tPlaceObj('QuestSetVariableBool', {
\t\t\t\t\t\t\t\t\t\t\t\tProp = "NotStarted",
\t\t\t\t\t\t\t\t\t\t\t\tQuestId = "Jazz_DeadPigs",
\t\t\t\t\t\t\t\t\t\t\t\tSet = false,
\t\t\t\t\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\t\t\t\t\tPlaceObj('UnitGrantItem', {
""",
        "make Dead Pigs acceptance one-shot",
    )
    text = replace_exact(
        text,
        """\
\t\t\t\t\tPlaceObj('QuestVarBool', {
\t\t\t\t\t\tName = "PigsDead",
\t\t\t\t\t}),
""",
        """\
\t\t\t\t\tPlaceObj('QuestVarBool', {
\t\t\t\t\t\tName = "PigsDead",
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('QuestVarBool', {
\t\t\t\t\t\tName = "AdvancePaid",
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('QuestVarBool', {
\t\t\t\t\t\tName = "Accepted",
\t\t\t\t\t}),
""",
        "add Dead Pigs one-shot variables",
    )
    text = replace_exact(
        text,
        'Text = T(492169252126, --[[ModItemQuestsDef Jazz_DeadPigs Text]] "Uno, Dos, Tres\\nЯ достану свинорез\\nТы откуда вылез, хлопчик\\nТы зачем сюда полез?\\nQuatro, Cinquo, Senco, Ses\\nЯ протру мой свинорез\\nЛучше б ты бежал на запад\\nИ глотал х*и в ЕС"),',
        'Text = T(492169252126, --[[ModItemQuestsDef Jazz_DeadPigs Text]] "Зачистить лагерь перебежчиков в <em>секторе K6</em> и вернуться к Балумбе.\\n\\nUno, Dos, Tres\\nЯ достану свинорез\\nТы откуда вылез, хлопчик\\nТы зачем сюда полез?\\nQuatro, Cinquo, Senco, Ses\\nЯ протру мой свинорез\\nЛучше б ты бежал на запад\\nИ глотал х*и в ЕС"),',
        "clarify the Dead Pigs journal objective",
    )

    # Meet the Rebels and Clear the Way reward paths.
    text = replace_exact(
        text,
        """\
\t\t\t\t\tPlaceObj('ConversationPhrase', {
\t\t\t\t\t\tAutoRemove = true,
\t\t\t\t\t\tCompleteQuests = {
\t\t\t\t\t\t\t"JAZZ_REBELS_0_MeetTheRebels",
\t\t\t\t\t\t},
\t\t\t\t\t\tEffects = {
""",
        """\
\t\t\t\t\tPlaceObj('ConversationPhrase', {
\t\t\t\t\t\tAutoRemove = true,
\t\t\t\t\t\tCompleteQuests = {
\t\t\t\t\t\t\t"JAZZ_REBELS_0_MeetTheRebels",
\t\t\t\t\t\t},
\t\t\t\t\t\tConditions = {
\t\t\t\t\t\t\tPlaceObj('QuestIsVariableBool', {
\t\t\t\t\t\t\t\tQuestId = "JAZZ_REBELS_0_MeetTheRebels",
\t\t\t\t\t\t\t\tVars = set({
\tCompleted = false,
\tGiven = true,
}),
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\tEffects = {
""",
        "gate Meet the Rebels completion",
    )
    text = replace_exact(
        text,
        """\
\t\t\t\t\t\t\tPlaceObj('ConversationPhrase', {
\t\t\t\t\t\t\t\tEffects = {
\t\t\t\t\t\t\t\t\tPlaceObj('SectorGrantIntel', {
""",
        """\
\t\t\t\t\t\t\tPlaceObj('ConversationPhrase', {
\t\t\t\t\t\t\t\tAutoRemove = true,
\t\t\t\t\t\t\t\tConditions = {
\t\t\t\t\t\t\t\t\tPlaceObj('QuestIsVariableBool', {
\t\t\t\t\t\t\t\t\t\tQuestId = "Jazz_ClearTheWay",
\t\t\t\t\t\t\t\t\t\tVars = set({
\tGiven = false,
}),
\t\t\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\t\t},
\t\t\t\t\t\t\t\tEffects = {
\t\t\t\t\t\t\t\t\tPlaceObj('SectorGrantIntel', {
""",
        "guard Clear the Way quest grant",
    )
    text = replace_exact(
        text,
        'Text = T(890000000000795, --[[ModItemConversation Ernie_M1_Rebel_Briefing Text voice:RebelSergeant_Immortal_M1 section:Ernie_M1_Rebel_Briefing keyword:Значит, если мы их предварительно зачистим, пробиться к Эмме будет проще?]] "Мы тут накидали примерный план лагеря в <L3>, готовили штурм, вот смотри, тут секретка, тут охранение, тут проход есть, можно ночью пройти и шомполами в ухо всех перещелкать.\\nа с другими стоянками Легов извини, с собой не взял. Тут самому придется <em>разведать</em>. Походи по окрестностям, пару человек на задание можно выделить, кто сметливый и в засаду не попадет."),',
        'Text = T(890000000000795, --[[ModItemConversation Ernie_M1_Rebel_Briefing Text voice:RebelSergeant_Immortal_M1 section:Ernie_M1_Rebel_Briefing keyword:Значит, если мы их предварительно зачистим, пробиться к Эмме будет проще?]] "Мы набросали примерный план лагеря в <em>секторе L3</em>. Там есть скрытая позиция, охранение и проход, которым можно воспользоваться ночью.\\nПо остальным стоянкам Легиона данных нет — придётся провести разведку самостоятельно."),',
        "repair the Clear the Way sector markup",
    )
    for tce_id in (
        "Jazz_ClearTheWay",
        "Jazz_ClearTheWay_K3",
        "Jazz_ClearTheWay_L3",
        "Jazz_ClearTheWay_K5",
        "Jazz_ClearTheWay_L4",
        "Jazz_ClearTheWay_L5",
    ):
        old = f'\t\t\t\t\t\tParamId = "{tce_id}",\n\t\t\t\t\t\tQuestId = "Jazz_ClearTheWay",\n'
        new = f'\t\t\t\t\t\tOnce = true,\n{old}'
        text = replace_exact(text, old, new, f"make {tce_id} one-shot")
    for tce_id in (
        "Jazz_ClearTheWay_K3",
        "Jazz_ClearTheWay_K5",
        "Jazz_ClearTheWay_L3",
        "Jazz_ClearTheWay_L4",
        "Jazz_ClearTheWay_L5",
    ):
        text = replace_exact(
            text,
            f'\t\t\t\t\t\t\t\tProp = "{tce_id}",\n'
            '\t\t\t\t\t\t\t\tQuestId = "Jazz_ClearTheWay",\n'
            "\t\t\t\t\t\t\t\tValue = true,\n",
            f'\t\t\t\t\t\t\t\tProp = "{tce_id}",\n'
            '\t\t\t\t\t\t\t\tQuestId = "Jazz_ClearTheWay",\n'
            '\t\t\t\t\t\t\t\tValue = "done",\n',
            f"use done state for {tce_id}",
        )

    # The Outlook state and final report refer to M4 consistently.
    text = replace_exact(
        text,
        "M3_UnderControl",
        "M4_UnderControl",
        "rename The Outlook capture state",
        expected=5,
    )
    text = replace_exact(
        text,
        """\
\t\t\t\t\t\tConditions = {
\t\t\t\t\t\t\tPlaceObj('PlayerIsInSectors', {
\t\t\t\t\t\t\t\tSectors = {
\t\t\t\t\t\t\t\t\t"M4",
\t\t\t\t\t\t\t\t},
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
""",
        """\
\t\t\t\t\t\tConditions = {
\t\t\t\t\t\t\tPlaceObj('PlayerIsInSectors', {
\t\t\t\t\t\t\t\tSectors = {
\t\t\t\t\t\t\t\t\t"M4",
\t\t\t\t\t\t\t\t},
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\tPlaceObj('QuestIsVariableBool', {
\t\t\t\t\t\t\t\tQuestId = "JAZZ_REBELS_1_SeizeTheOutlook",
\t\t\t\t\t\t\t\tVars = set({
\tCompleted = false,
\tM4_UnderControl = true,
}),
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
""",
        "gate The Outlook report on captured M4",
    )

    # RescueTeam must distinguish a living hostage from a failed rescue.
    text = replace_exact(
        text,
        'DisplayName = T(805716788538, --[[ModItemQuestsDef RescueTeam DisplayName]] "Мы в спасатели нанимались"),',
        'DisplayName = T(805716788538, --[[ModItemQuestsDef RescueTeam DisplayName]] "Мы в спасатели не нанимались"),',
        "correct RescueTeam title",
    )
    text = replace_exact(
        text,
        'Text = T(191474319874, --[[ModItemQuestsDef RescueTeam Text]] "Приговоренный <em>Партизан</em> находится где-то на <em>пирсе</em>"),',
        'Text = T(191474319874, --[[ModItemQuestsDef RescueTeam Text]] "Приговорённый повстанец находится на <em>пирсе</em>."),',
        "correct RescueTeam pier objective",
    )
    text = replace_exact(
        text,
        'Text = T(724348814002, --[[ModItemQuestsDef RescueTeam Text]] "<em>Спасенный</em> должен вернуться в лагерь, надо бы вернуться туда тоже."),',
        'Text = T(724348814002, --[[ModItemQuestsDef RescueTeam Text]] "Спасённый повстанец возвращается в лагерь. Нужно доложить сержанту."),',
        "correct RescueTeam return objective",
    )
    text = replace_exact(
        text,
        """\
\t\t\t\t\t\tConditions = {
\t\t\t\t\t\t\tPlaceObj('GroupIsDead', {
\t\t\t\t\t\t\t\tGroup = "Legion_Hostage_Killer",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
""",
        """\
\t\t\t\t\t\tConditions = {
\t\t\t\t\t\t\tPlaceObj('GroupIsDead', {
\t\t\t\t\t\t\t\tGroup = "Legion_Hostage_Killer",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\tPlaceObj('UnitIsOnMap', {
\t\t\t\t\t\t\t\tTargetUnit = "Rebel_Hostage",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\tPlaceObj('QuestIsVariableBool', {
\t\t\t\t\t\t\t\tQuestId = "RescueTeam",
\t\t\t\t\t\t\t\tVars = set({
\tFailed = false,
}),
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
""",
        "require a living hostage for rescue",
    )
    text = replace_exact(
        text,
        """\
\t\t\t\t\t\tParamId = "TCE_Rescued",
\t\t\t\t\t\tQuestId = "RescueTeam",
\t\t\t\t\t}),
""",
        """\
\t\t\t\t\t\tOnce = true,
\t\t\t\t\t\tParamId = "TCE_Rescued",
\t\t\t\t\t\tQuestId = "RescueTeam",
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('TriggeredConditionalEvent', {
\t\t\t\t\t\tConditions = {
\t\t\t\t\t\t\tPlaceObj('GroupIsDead', {
\t\t\t\t\t\t\t\tGroup = "Rebel_Hostage",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\tPlaceObj('QuestIsVariableBool', {
\t\t\t\t\t\t\t\tQuestId = "RescueTeam",
\t\t\t\t\t\t\t\tVars = set({
\tCompleted = false,
\tGiven = true,
\tRescued = false,
}),
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\tEffects = {
\t\t\t\t\t\t\tPlaceObj('QuestSetVariableBool', {
\t\t\t\t\t\t\t\tProp = "Failed",
\t\t\t\t\t\t\t\tQuestId = "RescueTeam",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\tOnce = true,
\t\t\t\t\t\tParamId = "TCE_HostageDead",
\t\t\t\t\t\tQuestId = "RescueTeam",
\t\t\t\t\t}),
""",
        "add RescueTeam failure transition",
    )
    text = replace_exact(
        text,
        """\
\t\t\t\t\tPlaceObj('QuestVarTCEState', {
\t\t\t\t\t\tName = "TCE_Rescued",
\t\t\t\t\t}),
""",
        """\
\t\t\t\t\tPlaceObj('QuestVarTCEState', {
\t\t\t\t\t\tName = "TCE_Rescued",
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('QuestVarTCEState', {
\t\t\t\t\t\tName = "TCE_HostageDead",
\t\t\t\t\t}),
""",
        "register RescueTeam failure TCE state",
    )

    # RebelsSavior hand-in and Barry recruitment.
    text = replace_exact(
        text,
        'DisplayName = T(995472785344, --[[ModItemQuestsDef RebelsSavior DisplayName]] "Маленькая спасательная операция"),',
        'DisplayName = T(995472785344, --[[ModItemQuestsDef RebelsSavior DisplayName]] "Снабжение для повстанцев"),',
        "correct RebelsSavior title",
    )
    text = replace_exact(
        text,
        'Text = T(484530953168, --[[ModItemQuestsDef RebelsSavior Text]] "Необходимо забрать из старого лагеря <em>4 Винтовки Zastava M76 и 4 Комплекта оказания мед помощи</em>."),',
        'Text = T(484530953168, --[[ModItemQuestsDef RebelsSavior Text]] "Забрать из старого лагеря <em>4 винтовки Zastava M76</em> и <em>4 комплекта Medkit</em>."),',
        "clarify RebelsSavior supplies",
    )
    text = replace_exact(
        text,
        """\
\t\t\t\t\t\t\t\tPlaceObj('ConversationPhrase', {
\t\t\t\t\t\t\t\t\tCompleteQuests = {
\t\t\t\t\t\t\t\t\t\t"RebelsSavior",
\t\t\t\t\t\t\t\t\t},
\t\t\t\t\t\t\t\t\tGoTo = "<end conversation>",
""",
        """\
\t\t\t\t\t\t\t\tPlaceObj('ConversationPhrase', {
\t\t\t\t\t\t\t\t\tGoTo = "<end conversation>",
""",
        "do not complete RebelsSavior on acceptance",
    )
    text = replace_regex(
        text,
        r"""(?P<med>^(?P<i>[ \t]*)PlaceObj\('UnitSquadHasItem', \{
(?P=i)\tAmount = 4,
(?P=i)\tItemId = "Medkit",
(?P=i)\tparam_bindings = false,
(?P=i)\}\),)
^(?P<o>[ \t]*)\},""",
        r"""\g<med>
\g<i>PlaceObj('QuestIsVariableBool', {
\g<i>	QuestId = "RebelsSavior",
\g<i>	Vars = set({
	Completed = false,
	SuppliesDelivered = false,
}),
\g<i>	param_bindings = false,
\g<i>}),
\g<o>},""",
        "gate RebelsSavior delivery",
        already_pattern=r"""QuestId = "RebelsSavior",
[ \t]*Vars = set\(\{
	Completed = false,
	SuppliesDelivered = false,
\}\),""",
    )
    text = replace_regex(
        text,
        r"""^(?P<i>[ \t]*)PlaceObj\('QuestSetVariableBool', \{
(?P=i)\tProp = "Completed",
(?P=i)\tQuestId = "RebelsSavior",
(?P=i)\tparam_bindings = false,
(?P=i)\}\),
(?P=i)PlaceObj\('UnitTakeItem', \{
(?P=i)\tAmount = 4,
(?P=i)\tItemId = "ZastavaM76",
(?P=i)\tparam_bindings = false,
(?P=i)\}\),
(?P=i)PlaceObj\('UnitTakeItem', \{
(?P=i)\tAmount = 4,
(?P=i)\tItemId = "Medkit",
(?P=i)\tparam_bindings = false,
(?P=i)\}\),""",
        r"""\g<i>PlaceObj('QuestSetVariableBool', {
\g<i>	Prop = "SuppliesDelivered",
\g<i>	QuestId = "RebelsSavior",
\g<i>	param_bindings = false,
\g<i>}),
\g<i>PlaceObj('UnitTakeItem', {
\g<i>	Amount = 4,
\g<i>	AnySquad = true,
\g<i>	ItemId = "ZastavaM76",
\g<i>	param_bindings = false,
\g<i>}),
\g<i>PlaceObj('UnitTakeItem', {
\g<i>	Amount = 4,
\g<i>	AnySquad = true,
\g<i>	ItemId = "Medkit",
\g<i>	param_bindings = false,
\g<i>}),""",
        "record and consume RebelsSavior delivery",
        already_pattern=r"""Prop = "SuppliesDelivered",
[ \t]*QuestId = "RebelsSavior",""",
    )
    text = replace_exact(
        text,
        'Text = T(480799336285, --[[ModItemConversation Ernie_LegionCamp5_Rebels Text voice:RebelSergant_Immortal section:Ernie_LegionCamp5_Rebels keyword:Да мы счастливы]] "Вы очень сильно помогли нам, спасибо наемники, у нас тут затесался ваш колега по опасному бизнессу, такой же солдат удачи, думаю он с радостью пойдёт с вами, по началу бредил про какую-то несуществующую страну, под названием Арулько, но вроде отпустило. Он вроде как потерял память, но боевые навыки точно не растерял. Вон он стоит у палаток."),',
        'Text = T(480799336285, --[[ModItemConversation Ernie_LegionCamp5_Rebels Text voice:RebelSergant_Immortal section:Ernie_LegionCamp5_Rebels keyword:Да мы счастливы]] "Вы нас здорово выручили. У палаток ждёт один американец — Берриман Сил, пилот и контрабандист. Его последний рейс закончился здесь не по плану. Он ищет новую команду; думаю, вы найдёте общий язык."),',
        "introduce Barry Seal naturally",
    )
    text = replace_exact(
        text,
        """\
\t\t\t\t\tPlaceObj('QuestVarTCEState', {
\t\t\t\t\t\tName = "TCE_All_Found",
\t\t\t\t\t}),
""",
        """\
\t\t\t\t\tPlaceObj('QuestVarTCEState', {
\t\t\t\t\t\tName = "TCE_All_Found",
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('QuestVarBool', {
\t\t\t\t\t\tName = "SuppliesDelivered",
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('QuestVarBool', {
\t\t\t\t\t\tName = "BarryJoined",
\t\t\t\t\t}),
""",
        "add RebelsSavior delivery and Barry variables",
    )
    barry_conversation = """\
\t\t\t\tPlaceObj('ModItemConversation', {
\t\t\t\t\tAssignToGroup = "BarrySeal_Recruit",
\t\t\t\t\tConditions = {
\t\t\t\t\t\tPlaceObj('QuestIsVariableBool', {
\t\t\t\t\t\t\tQuestId = "RebelsSavior",
\t\t\t\t\t\t\tVars = set({
\tBarryJoined = false,
\tSuppliesDelivered = true,
}),
\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t}),
\t\t\t\t\t},
\t\t\t\t\tDefaultActor = "Merc_BarrySeal",
\t\t\t\t\tgroup = "Ernie",
\t\t\t\t\tid = "BarrySeal_Recruit",
\t\t\t\t\tPlaceObj('ConversationPhrase', {
\t\t\t\t\t\tKeyword = "Greeting",
\t\t\t\t\t\tKeywordT = T(890000000001581, --[[ModItemConversation BarrySeal_Recruit KeywordT]] "Greeting"),
\t\t\t\t\t\tLines = {
\t\t\t\t\t\t\tPlaceObj('ConversationLine', {
\t\t\t\t\t\t\t\tCharacter = "Merc_BarrySeal",
\t\t\t\t\t\t\t\tText = T(890000000013005, --[[ModItemConversation BarrySeal_Recruit Text voice:Merc_BarrySeal section:BarrySeal_Recruit keyword:Greeting]] "Сержант сказал, это вы доставили винтовки. Хороший знак. В моём деле люди чаще теряют груз, деньги или голову — иногда всё сразу."),
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\tid = "Greeting",
\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\tPlaceObj('ConversationPhrase', {
\t\t\t\t\t\t\tAlign = "right",
\t\t\t\t\t\t\tEffects = {
\t\t\t\t\t\t\t\tPlaceObj('UnitJoinAsMerc', {
\t\t\t\t\t\t\t\t\tMerc = "Merc_BarrySeal",
\t\t\t\t\t\t\t\t\tTargetUnit = "BarrySeal_Recruit",
\t\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\t\tPlaceObj('QuestSetVariableBool', {
\t\t\t\t\t\t\t\t\tProp = "BarryJoined",
\t\t\t\t\t\t\t\t\tQuestId = "RebelsSavior",
\t\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\t},
\t\t\t\t\t\t\tGoTo = "<end conversation>",
\t\t\t\t\t\t\tKeyword = "Пойдёшь с нами?",
\t\t\t\t\t\t\tKeywordT = T(890000000013006, --[[ModItemConversation BarrySeal_Recruit KeywordT]] "Пойдёшь с нами?"),
\t\t\t\t\t\t\tLines = {
\t\t\t\t\t\t\t\tPlaceObj('ConversationLine', {
\t\t\t\t\t\t\t\t\tCharacter = "Merc_BarrySeal",
\t\t\t\t\t\t\t\t\tText = T(890000000013007, --[[ModItemConversation BarrySeal_Recruit Text voice:Merc_BarrySeal section:BarrySeal_Recruit keyword:Пойдёшь с нами?]] "Почему бы и нет? Самолёта у меня больше нет, груз сгорел, а сидеть без дела я не умею. Оставьте место в отряде — маршрут обсудим по дороге."),
\t\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\t},
\t\t\t\t\t\t\tid = "Join",
\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t}),
\t\t\t\t\t\tPlaceObj('ConversationPhrase', {
\t\t\t\t\t\t\tAlign = "right",
\t\t\t\t\t\t\tGoTo = "<end conversation>",
\t\t\t\t\t\t\tKeyword = "Не сейчас",
\t\t\t\t\t\t\tKeywordT = T(890000000013008, --[[ModItemConversation BarrySeal_Recruit KeywordT]] "Не сейчас"),
\t\t\t\t\t\t\tLines = {
\t\t\t\t\t\t\t\tPlaceObj('ConversationLine', {
\t\t\t\t\t\t\t\t\tCharacter = "Merc_BarrySeal",
\t\t\t\t\t\t\t\t\tText = T(890000000013009, --[[ModItemConversation BarrySeal_Recruit Text voice:Merc_BarrySeal section:BarrySeal_Recruit keyword:Не сейчас]] "Как скажете. Я пока здесь."),
\t\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\t},
\t\t\t\t\t\t\tid = "NotNow",
\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t}),
\t\t\t\t\t}),
\t\t\t\t}),
"""
    text = replace_exact(
        text,
        """\
\t\t\t\t}),
\t\t\t\tPlaceObj('ModItemConversation', {
\t\t\t\t\tAssignToGroup = "RebelSergeant_Immortal_M1",
""",
        "\t\t\t\t}),\n" + barry_conversation + """\
\t\t\t\tPlaceObj('ModItemConversation', {
\t\t\t\t\tAssignToGroup = "RebelSergeant_Immortal_M1",
""",
        "add Barry Seal recruitment conversation",
    )

    # Doctor hand-in checks live inventory and keeps all three wounded explicit.
    text = replace_exact(
        text,
        'Vars = set( "AmmoTaken", "InjuredRebels_Healed", "MedsTaken", "MinesTaken" ),',
        'Vars = set( "AmmoTaken", "InjuredRebels_Healed", "MedsTaken", "MinesTaken" ),',
        "doctor legacy aggregate remains explicit",
    )
    text = replace_exact(
        text,
        """\
\t\t\t\t\t\t\tPlaceObj('QuestIsVariableBool', {
\t\t\t\t\t\t\t\tQuestId = "Jazz_Doctor_need_Help",
\t\t\t\t\t\t\t\tVars = set( "AmmoTaken", "InjuredRebels_Healed", "MedsTaken", "MinesTaken" ),
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
""",
        """\
\t\t\t\t\t\t\tPlaceObj('QuestIsVariableBool', {
\t\t\t\t\t\t\t\tQuestId = "Jazz_Doctor_need_Help",
\t\t\t\t\t\t\t\tVars = set( "AmmoTaken", "InjuredRebels_Healed", "MedsTaken", "MinesTaken" ),
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\tPlaceObj('UnitSquadHasItem', {
\t\t\t\t\t\t\t\tAmount = 50,
\t\t\t\t\t\t\t\tItemId = "Meds",
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\tPlaceObj('UnitSquadHasItem', {
\t\t\t\t\t\t\t\tItemId = "JazzQuestItem_AmmoBox",
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\tPlaceObj('UnitSquadHasItem', {
\t\t\t\t\t\t\t\tItemId = "JazzQuestItem_MinesBox",
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
""",
        "recheck doctor hand-in inventory",
    )
    text = replace_exact(
        text,
        """\
\t\t\t\t\t\t\tPlaceObj('NpcUnitTakeItem', {
\t\t\t\t\t\t\t\tItemId = "JazzQuestItem_MinesBox",
\t\t\t\t\t\t\t\tTargetUnit = "Jazz_Doctor_Leevsy",
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\tPlaceObj('NpcUnitTakeItem', {
\t\t\t\t\t\t\t\tItemId = "JazzQuestItem_AmmoBox",
\t\t\t\t\t\t\t\tTargetUnit = "Jazz_Doctor_Leevsy",
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}),
""",
        """\
\t\t\t\t\t\t\tPlaceObj('UnitTakeItem', {
\t\t\t\t\t\t\t\tAnySquad = true,
\t\t\t\t\t\t\t\tItemId = "JazzQuestItem_MinesBox",
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\tPlaceObj('UnitTakeItem', {
\t\t\t\t\t\t\t\tAnySquad = true,
\t\t\t\t\t\t\t\tItemId = "JazzQuestItem_AmmoBox",
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}),
""",
        "take doctor quest boxes from player squads",
    )
    text = replace_exact(
        text,
        """\
\t\t\t\t\t\t\tPlaceObj('UnitTakeItem', {
\t\t\t\t\t\t\t\tAmount = 50,
\t\t\t\t\t\t\t\tAnySquad = true,
\t\t\t\t\t\t\t\tItemId = "Meds",
""",
        """\
\t\t\t\t\t\t\tPlaceObj('UnitTakeItem', {
\t\t\t\t\t\t\t\tAmount = 50,
\t\t\t\t\t\t\t\tAnySquad = true,
\t\t\t\t\t\t\t\tItemId = "Meds",
""",
        "keep doctor Meds removal cross-squad",
    )
    text = replace_exact(
        text,
        'Vars = set( "AmmoTaken", "MedsTaken", "MinesTaken" ),',
        'Vars = set( "AmmoTaken", "InjuredRebels_Healed", "MedsTaken", "MinesTaken" ),',
        "keep doctor objective visible through all healing",
    )
    text = replace_exact(
        text,
        'Text = T(555833394027, --[[ModItemQuestsDef Jazz_Doctor_need_Help Text]] "Нашему айболиту нужна помощь, придется заморочиться и поискать <em>медикаменты</em> ажно <em>50</em> штук, мины и боеприпасы должны быть в секторе <em>I3</em> на <em>Блок посту возле моста и в тайнике в вентилиционной шахте</em>, Также нужно поднять <em>выживших повстанцев</em>, сто процентов мы не заметили их при подъёме, коммуняки умеют в маскировку."),',
        'Text = T(555833394027, --[[ModItemQuestsDef Jazz_Doctor_need_Help Text]] "Собрать <em>50 Meds</em>, забрать в <em>секторе I3</em> ящик с боеприпасами у моста и ящик с минами в тайнике у разрушенного ангара, затем стабилизировать <em>трёх раненых повстанцев</em>."),',
        "clarify doctor quest requirements",
    )
    text = replace_exact(
        text,
        """\
\t\t\t\t\tPlaceObj('TriggeredConditionalEvent', {
\t\t\t\t\t\tConditions = {
\t\t\t\t\t\t\tPlaceObj('UnitSquadHasItem', {
\t\t\t\t\t\t\t\tItemId = "JazzQuestItem_MinesBox",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\tEffects = {
\t\t\t\t\t\t\tPlaceObj('QuestSetVariableBool', {
\t\t\t\t\t\t\t\tProp = "MinesTaken",
\t\t\t\t\t\t\t\tQuestId = "Jazz_Doctor_need_Help",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\tParamId = "TCE_MinesTaken",
\t\t\t\t\t\tQuestId = "Jazz_Doctor_need_Help",
\t\t\t\t\t}),
""",
        """\
\t\t\t\t\tPlaceObj('TriggeredConditionalEvent', {
\t\t\t\t\t\tConditions = {
\t\t\t\t\t\t\tPlaceObj('UnitSquadHasItem', {
\t\t\t\t\t\t\t\tItemId = "JazzQuestItem_MinesBox",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\tEffects = {
\t\t\t\t\t\t\tPlaceObj('QuestSetVariableBool', {
\t\t\t\t\t\t\t\tProp = "MinesTaken",
\t\t\t\t\t\t\t\tQuestId = "Jazz_Doctor_need_Help",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\tParamId = "TCE_MinesTaken",
\t\t\t\t\t\tQuestId = "Jazz_Doctor_need_Help",
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('TriggeredConditionalEvent', {
\t\t\t\t\t\tConditions = {
\t\t\t\t\t\t\tPlaceObj('QuestIsVariableBool', {
\t\t\t\t\t\t\t\tQuestId = "Jazz_Doctor_need_Help",
\t\t\t\t\t\t\t\tVars = set( "InjuredRebel1_Healed", "InjuredRebel2_Healed", "InjuredRebel3_Healed" ),
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\tEffects = {
\t\t\t\t\t\t\tPlaceObj('QuestSetVariableBool', {
\t\t\t\t\t\t\t\tProp = "InjuredRebels_Healed",
\t\t\t\t\t\t\t\tQuestId = "Jazz_Doctor_need_Help",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\tOnce = true,
\t\t\t\t\t\tParamId = "TCE_InjuredRebels_Healed",
\t\t\t\t\t\tQuestId = "Jazz_Doctor_need_Help",
\t\t\t\t\t}),
""",
        "aggregate the three wounded states",
    )
    text = replace_exact(
        text,
        """\
\t\t\t\t\tPlaceObj('QuestVarBool', {
\t\t\t\t\t\tName = "InjuredRebels_Healed",
\t\t\t\t\t}),
""",
        """\
\t\t\t\t\tPlaceObj('QuestVarBool', {
\t\t\t\t\t\tName = "InjuredRebels_Healed",
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('QuestVarBool', {
\t\t\t\t\t\tName = "InjuredRebel1_Healed",
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('QuestVarBool', {
\t\t\t\t\t\tName = "InjuredRebel2_Healed",
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('QuestVarBool', {
\t\t\t\t\t\tName = "InjuredRebel3_Healed",
\t\t\t\t\t}),
""",
        "add individual wounded variables",
    )
    text = replace_exact(
        text,
        """\
\t\t\t\t\tPlaceObj('QuestVarTCEState', {
\t\t\t\t\t\tName = "TCE_MinesTaken",
\t\t\t\t\t}),
""",
        """\
\t\t\t\t\tPlaceObj('QuestVarTCEState', {
\t\t\t\t\t\tName = "TCE_MinesTaken",
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('QuestVarTCEState', {
\t\t\t\t\t\tName = "TCE_InjuredRebels_Healed",
\t\t\t\t\t}),
""",
        "register doctor healing TCE state",
    )

    # Alkatraz gets a complete journal and only progresses after it was given.
    text = replace_exact(
        text,
        """\
\t\t\tPlaceObj('ModItemQuestsDef', {
\t\t\t\tKillTCEsConditions = {
\t\t\t\t\tPlaceObj('QuestKillTCEsOnCompleted', {}),
\t\t\t\t},
\t\t\t\tTCEs = {
\t\t\t\t\tPlaceObj('TriggeredConditionalEvent', {
\t\t\t\t\t\tConditions = {
\t\t\t\t\t\t\tPlaceObj('SectorCheckOwner', {
\t\t\t\t\t\t\t\tsector_id = "L6_Underground",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
""",
        """\
\t\t\tPlaceObj('ModItemQuestsDef', {
\t\t\t\tDisplayName = T(890000000013000, --[[ModItemQuestsDef Jazz_Alkatraz DisplayName]] "Зачистить бункер"),
\t\t\t\tKillTCEsConditions = {
\t\t\t\t\tPlaceObj('QuestKillTCEsOnCompleted', {}),
\t\t\t\t},
\t\t\t\tNoteDefs = {
\t\t\t\t\tLastNoteIdx = 3,
\t\t\t\t\tPlaceObj('QuestNote', {
\t\t\t\t\t\tCompletionConditions = {
\t\t\t\t\t\t\tPlaceObj('QuestIsVariableBool', {
\t\t\t\t\t\t\t\tQuestId = "Jazz_Alkatraz",
\t\t\t\t\t\t\t\tVars = set( "All__Dead" ),
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\tShowConditions = {
\t\t\t\t\t\t\tPlaceObj('QuestIsVariableBool', {
\t\t\t\t\t\t\t\tQuestId = "Jazz_Alkatraz",
\t\t\t\t\t\t\t\tVars = set( "Given" ),
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\tText = T(890000000013001, --[[ModItemQuestsDef Jazz_Alkatraz Text]] "Зачистить бункер в <em>подземном секторе L6</em>."),
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('QuestNote', {
\t\t\t\t\t\tCompletionConditions = {
\t\t\t\t\t\t\tPlaceObj('QuestIsVariableBool', {
\t\t\t\t\t\t\t\tQuestId = "Jazz_Alkatraz",
\t\t\t\t\t\t\t\tVars = set( "Completed" ),
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\tIdx = 2,
\t\t\t\t\t\tShowConditions = {
\t\t\t\t\t\t\tPlaceObj('QuestIsVariableBool', {
\t\t\t\t\t\t\t\tQuestId = "Jazz_Alkatraz",
\t\t\t\t\t\t\t\tVars = set({
\tAll__Dead = true,
\tCompleted = false,
}),
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\tText = T(890000000013002, --[[ModItemQuestsDef Jazz_Alkatraz Text]] "Вернуться к сержанту в <em>сектор L1</em> и доложить о зачистке."),
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('QuestNote', {
\t\t\t\t\t\tIdx = 3,
\t\t\t\t\t\tShowConditions = {
\t\t\t\t\t\t\tPlaceObj('QuestIsVariableBool', {
\t\t\t\t\t\t\t\tQuestId = "Jazz_Alkatraz",
\t\t\t\t\t\t\t\tVars = set( "Completed" ),
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\tShowWhenCompleted = true,
\t\t\t\t\t\tText = T(890000000013003, --[[ModItemQuestsDef Jazz_Alkatraz Text]] "Бункер снова под контролем повстанцев."),
\t\t\t\t\t}),
\t\t\t\t},
\t\t\t\tTCEs = {
\t\t\t\t\tPlaceObj('TriggeredConditionalEvent', {
\t\t\t\t\t\tConditions = {
\t\t\t\t\t\t\tPlaceObj('QuestIsVariableBool', {
\t\t\t\t\t\t\t\tQuestId = "Jazz_Alkatraz",
\t\t\t\t\t\t\t\tVars = set( "Given" ),
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\tPlaceObj('SectorCheckOwner', {
\t\t\t\t\t\t\t\tsector_id = "L6_Underground",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
""",
        "add Alkatraz journal and given gate",
    )
    text = replace_exact(
        text,
        """\
\t\t\t\t\t\tParamId = "All_Dead",
\t\t\t\t\t\tQuestId = "Jazz_Alkatraz",
""",
        """\
\t\t\t\t\t\tOnce = true,
\t\t\t\t\t\tParamId = "All_Dead",
\t\t\t\t\t\tQuestId = "Jazz_Alkatraz",
""",
        "make Alkatraz clear transition one-shot",
    )

    # Item art is assigned to the matching quest item.
    text = replace_exact(
        text,
        '\t\t\'Icon\', "Mod/FhNNYd/Images/Inventory_Images/MinesBox.png",\n'
        '\t\t\'SubIcon\', "Mod/FhNNYd/Images/Inventory_Images/MinesBox.png",\n',
        '\t\t\'Icon\', "Mod/FhNNYd/Images/Inventory_Images/AmmoCrate.png",\n'
        '\t\t\'SubIcon\', "Mod/FhNNYd/Images/Inventory_Images/AmmoCrate.png",\n',
        "assign AmmoBox art",
    )
    text = replace_exact(
        text,
        '\t\t\'Icon\', "Mod/FhNNYd/Images/Inventory_Images/AmmoCrate.png",\n'
        '\t\t\'SubIcon\', "Mod/FhNNYd/Images/Inventory_Images/AmmoCrate.png",\n'
        '\t\t\'DisplayName\', T(872338951889',
        '\t\t\'Icon\', "Mod/FhNNYd/Images/Inventory_Images/MinesBox.png",\n'
        '\t\t\'SubIcon\', "Mod/FhNNYd/Images/Inventory_Images/MinesBox.png",\n'
        '\t\t\'DisplayName\', T(872338951889',
        "assign MinesBox art",
    )

    return text


def patch_modtexts(text: str) -> str:
    if not text.startswith("sep=,\n"):
        raise RuntimeError("ModTextsMaps.csv must start with 'sep=,'")
    reader = csv.DictReader(io.StringIO(text[len("sep=,\n") :]))
    expected_fields = ["ID", "Text", "Translation", "VoiceActor", "Context"]
    if reader.fieldnames != expected_fields:
        raise RuntimeError(f"unexpected ModTextsMaps.csv header: {reader.fieldnames}")

    rows = list(reader)
    updates = {
        "191474319874": ("Приговорённый повстанец находится на <em>пирсе</em>.", "", "ModItemQuestsDef RescueTeam Text"),
        "480799336285": (
            "Вы нас здорово выручили. У палаток ждёт один американец — Берриман Сил, пилот и контрабандист. "
            "Его последний рейс закончился здесь не по плану. Он ищет новую команду; думаю, вы найдёте общий язык.",
            "RebelSergant_Immortal",
            "ModItemConversation Ernie_LegionCamp5_Rebels Text  section:Ernie_LegionCamp5_Rebels keyword:Да мы счастливы",
        ),
        "484530953168": (
            "Забрать из старого лагеря <em>4 винтовки Zastava M76</em> и <em>4 комплекта Medkit</em>.",
            "",
            "ModItemQuestsDef RebelsSavior Text",
        ),
        "492169252126": (
            "Зачистить лагерь перебежчиков в <em>секторе K6</em> и вернуться к Балумбе.\n\n"
            "Uno, Dos, Tres\nЯ достану свинорез\nТы откуда вылез, хлопчик\nТы зачем сюда полез?\n"
            "Quatro, Cinquo, Senco, Ses\nЯ протру мой свинорез\nЛучше б ты бежал на запад\nИ глотал х*и в ЕС",
            "",
            "ModItemQuestsDef Jazz_DeadPigs Text",
        ),
        "555833394027": (
            "Собрать <em>50 Meds</em>, забрать в <em>секторе I3</em> ящик с боеприпасами у моста и ящик "
            "с минами в тайнике у разрушенного ангара, затем стабилизировать <em>трёх раненых повстанцев</em>.",
            "",
            "ModItemQuestsDef Jazz_Doctor_need_Help Text",
        ),
        "724348814002": (
            "Спасённый повстанец возвращается в лагерь. Нужно доложить сержанту.",
            "",
            "ModItemQuestsDef RescueTeam Text",
        ),
        "805716788538": ("Мы в спасатели не нанимались", "", "ModItemQuestsDef RescueTeam DisplayName"),
        "995472785344": ("Снабжение для повстанцев", "", "ModItemQuestsDef RebelsSavior DisplayName"),
        "890000000000795": (
            "Мы набросали примерный план лагеря в <em>секторе L3</em>. Там есть скрытая позиция, охранение "
            "и проход, которым можно воспользоваться ночью.\nПо остальным стоянкам Легиона данных нет — "
            "придётся провести разведку самостоятельно.",
            "RebelSergeant_Immortal_M1",
            "ModItemConversation Ernie_M1_Rebel_Briefing Text  section:Ernie_M1_Rebel_Briefing",
        ),
        "890000000013000": ("Зачистить бункер", "", "ModItemQuestsDef Jazz_Alkatraz DisplayName"),
        "890000000013001": (
            "Зачистить бункер в <em>подземном секторе L6</em>.",
            "",
            "ModItemQuestsDef Jazz_Alkatraz Text",
        ),
        "890000000013002": (
            "Вернуться к сержанту в <em>сектор L1</em> и доложить о зачистке.",
            "",
            "ModItemQuestsDef Jazz_Alkatraz Text",
        ),
        "890000000013003": (
            "Бункер снова под контролем повстанцев.",
            "",
            "ModItemQuestsDef Jazz_Alkatraz Text",
        ),
        "890000000013004": (
            "<em>Martha</em> is looking for her husband who was kidnapped by the <em>Legion</em> and was "
            "last seen on the <em><SectorName('J7')></em>",
            "",
            "ModItemQuestsDef RescueHerMan Text",
        ),
        "890000000013005": (
            "Сержант сказал, это вы доставили винтовки. Хороший знак. В моём деле люди чаще теряют груз, "
            "деньги или голову — иногда всё сразу.",
            "Merc_BarrySeal",
            "ModItemConversation BarrySeal_Recruit Text  section:BarrySeal_Recruit keyword:Greeting",
        ),
        "890000000013006": ("Пойдёшь с нами?", "", "ModItemConversation BarrySeal_Recruit KeywordT"),
        "890000000013007": (
            "Почему бы и нет? Самолёта у меня больше нет, груз сгорел, а сидеть без дела я не умею. "
            "Оставьте место в отряде — маршрут обсудим по дороге.",
            "Merc_BarrySeal",
            "ModItemConversation BarrySeal_Recruit Text  section:BarrySeal_Recruit keyword:Пойдёшь с нами?",
        ),
        "890000000013008": ("Не сейчас", "", "ModItemConversation BarrySeal_Recruit KeywordT"),
        "890000000013009": (
            "Как скажете. Я пока здесь.",
            "Merc_BarrySeal",
            "ModItemConversation BarrySeal_Recruit Text  section:BarrySeal_Recruit keyword:Не сейчас",
        ),
    }
    remove_ids = {"706580608154"}
    seen = {loc_id: 0 for loc_id in updates}
    output_rows = []
    for row in rows:
        loc_id = row["ID"]
        if loc_id in remove_ids:
            continue
        if loc_id in updates:
            seen[loc_id] += 1
            source, voice, context = updates[loc_id]
            row["Text"] = source
            row["Translation"] = ""
            row["VoiceActor"] = voice
            row["Context"] = context
        output_rows.append(row)
    duplicates = {loc_id: count for loc_id, count in seen.items() if count > 1}
    if duplicates:
        raise RuntimeError(f"duplicate quest localization rows in ModTextsMaps.csv: {duplicates}")
    for loc_id, count in seen.items():
        if count == 0:
            source, voice, context = updates[loc_id]
            output_rows.append(
                {
                    "ID": loc_id,
                    "Text": source,
                    "Translation": "",
                    "VoiceActor": voice,
                    "Context": context,
                }
            )

    rendered = io.StringIO(newline="")
    writer = csv.DictWriter(rendered, fieldnames=expected_fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(output_rows)
    return "sep=,\n" + rendered.getvalue()


def patch_simple_companions(maps_root: Path) -> dict[Path, str]:
    patched_files: dict[Path, str] = {}
    edits = {
        maps_root / "InventoryItem" / "JazzQuestItem_AmmoBox.lua": (
            "Mod/FhNNYd/Images/Inventory_Images/MinesBox.png",
            "Mod/FhNNYd/Images/Inventory_Images/AmmoCrate.png",
            2,
        ),
        maps_root / "InventoryItem" / "JazzQuestItem_MinesBox.lua": (
            "Mod/FhNNYd/Images/Inventory_Images/AmmoCrate.png",
            "Mod/FhNNYd/Images/Inventory_Images/MinesBox.png",
            2,
        ),
    }
    for path, (old, new, expected) in edits.items():
        text = path.read_text(encoding="utf-8")
        text = replace_exact(text, old, new, path.name, expected=expected)
        patched_files[path] = text

    kiki = maps_root / "UnitData" / "JAZZ_Ernie_Locals_M2_SaveMyFamily_Woman.lua"
    text = kiki.read_text(encoding="utf-8")
    text = replace_exact(
        text,
        '\tName = T(356243372579, --[[ModItemUnitDataCompositeDef JAZZ_Ernie_Locals_M2_SaveMyFamily_Woman Name]] "Кики"),\n'
        '\tAffiliation = "Civilian",\n',
        '\tName = T(356243372579, --[[ModItemUnitDataCompositeDef JAZZ_Ernie_Locals_M2_SaveMyFamily_Woman Name]] "Кики"),\n'
        "\timmortal = true,\n"
        "\tImportantNPC = true,\n"
        '\tAffiliation = "Civilian",\n',
        "Kiki companion",
    )
    patched_files[kiki] = text
    return patched_files


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--maps-root", type=Path, default=DEFAULT_MAPS_ROOT)
    parser.add_argument("--check", action="store_true", help="verify applicability without writing")
    args = parser.parse_args()
    maps_root = args.maps_root.resolve()
    items = maps_root / "items.lua"
    modtexts = maps_root / "ModTextsMaps.csv"
    original = items.read_text(encoding="utf-8")
    patched = patch_items(original)
    patched_modtexts = patch_modtexts(modtexts.read_text(encoding="utf-8-sig"))
    companions = patch_simple_companions(maps_root)
    if args.check:
        print("JAZZ-QUESTS-001 generated-data apply plan is valid")
        return 0
    items.write_text(patched, encoding="utf-8", newline="")
    modtexts.write_text(patched_modtexts, encoding="utf-8", newline="")
    for path, contents in companions.items():
        path.write_text(contents, encoding="utf-8", newline="")
    print("Applied JAZZ-QUESTS-001 generated-data repairs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
