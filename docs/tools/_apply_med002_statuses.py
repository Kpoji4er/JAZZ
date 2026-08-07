# MED-002: insert WoundInfected + BloodLoss50..1 CharacterEffects into companions/items/metadata.
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Loc IDs 890000000010300+
WI_DN, WI_DESC, WI_ADD = 890000000010300, 890000000010301, 890000000010302

BLOOD = [
    # id, pct label, ap, dn_id, desc_id, en_name, en_desc, ru_name, ru_desc
    ("BloodLoss50", 50, 1, 890000000010310, 890000000010311,
     "Weakness", "Blood loss: <color EmStyle>−<APLoss> AP</color> at the start of the turn. Below 50% HP. Clears only when HP rises.",
     "Слабость", "Потеря крови: <color EmStyle>−<APLoss> ОД</color> в начале хода. Ниже 50% ОЗ. Снимается только ростом ОЗ."),
    ("BloodLoss40", 40, 2, 890000000010312, 890000000010313,
     "Pallor", "Blood loss: <color EmStyle>−<APLoss> AP</color> at the start of the turn. Below 40% HP. Clears only when HP rises.",
     "Бледность", "Потеря крови: <color EmStyle>−<APLoss> ОД</color> в начале хода. Ниже 40% ОЗ. Снимается только ростом ОЗ."),
    ("BloodLoss30", 30, 3, 890000000010314, 890000000010315,
     "Severe Weakness", "Blood loss: <color EmStyle>−<APLoss> AP</color> at the start of the turn. Below 30% HP. Clears only when HP rises.",
     "Сильная слабость", "Потеря крови: <color EmStyle>−<APLoss> ОД</color> в начале хода. Ниже 30% ОЗ. Снимается только ростом ОЗ."),
    ("BloodLoss20", 20, 4, 890000000010316, 890000000010317,
     "Heavy Blood Loss", "Blood loss: <color EmStyle>−<APLoss> AP</color> at the start of the turn. Below 20% HP. Clears only when HP rises.",
     "Тяжёлая кровопотеря", "Потеря крови: <color EmStyle>−<APLoss> ОД</color> в начале хода. Ниже 20% ОЗ. Снимается только ростом ОЗ."),
    ("BloodLoss10", 10, 5, 890000000010318, 890000000010319,
     "Critical Weakness", "Blood loss: <color EmStyle>−<APLoss> AP</color> at the start of the turn. Below 10% HP. Clears only when HP rises.",
     "Критическая слабость", "Потеря крови: <color EmStyle>−<APLoss> ОД</color> в начале хода. Ниже 10% ОЗ. Снимается только ростом ОЗ."),
    ("BloodLoss5", 5, 6, 890000000010320, 890000000010321,
     "Near Collapse", "Blood loss: <color EmStyle>−<APLoss> AP</color> at the start of the turn. Below 5% HP. Clears only when HP rises.",
     "Почти коллапс", "Потеря крови: <color EmStyle>−<APLoss> ОД</color> в начале хода. Ниже 5% ОЗ. Снимается только ростом ОЗ."),
    ("BloodLoss1", 1, 7, 890000000010322, 890000000010323,
     "Critical Blood Loss", "Critical blood loss: <color EmStyle>−<APLoss> AP</color> at the start of the turn. Below 1% HP — still conscious. Clears only when HP rises.",
     "Критическая кровопотеря", "Критическая кровопотеря: <color EmStyle>−<APLoss> ОД</color> в начале хода. Ниже 1% ОЗ — ещё в сознании. Снимается только ростом ОЗ."),
]


def blood_companion(eid: str, ap: int, dn: int, desc: int, en_name: str, en_desc: str) -> str:
    return f"""UndefineClass('{eid}')
DefineClass.{eid} = {{
\t__parents = {{ "StatusEffect" }},
\t__generated_by_class = "ModItemCharacterEffectCompositeDef",
\tobject_class = "StatusEffect",
\tParameters = {{
\t\tPlaceObj('PresetParamNumber', {{
\t\t\t'Name', "APLoss",
\t\t\t'Value', {ap},
\t\t\t'Tag', "<APLoss>",
\t\t}}),
\t}},
\tunit_reactions = {{
\t\tPlaceObj('UnitReaction', {{
\t\t\tEvent = "OnCalcStartTurnAP",
\t\t\tHandler = function(self, target, value)
\t\t\t\treturn value - self:ResolveValue("APLoss") * const.Scale.AP
\t\t\tend,
\t\t}}),
\t}},
\tDisplayName = T({dn}, "{en_name}"),
\tDescription = T({desc}, "{en_desc}"),
\ttype = "Debuff",
\tIcon = "Mod/e6L4ECj/Icons/StatusEffects/{eid}.png",
\tShown = true,
\tShownSatelliteView = true,
}}
"""


def blood_items(eid: str, ap: int, dn: int, desc: int, en_name: str, en_desc: str) -> str:
    return f"""\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {{
\t\t\t\t'Id', "{eid}",
\t\t\t\t'Parameters', {{
\t\t\t\t\tPlaceObj('PresetParamNumber', {{
\t\t\t\t\t\t'Name', "APLoss",
\t\t\t\t\t\t'Value', {ap},
\t\t\t\t\t\t'Tag', "<APLoss>",
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
\t\t\t\t}},
\t\t\t\t'DisplayName', T({dn}, "{en_name}"),
\t\t\t\t'Description', T({desc}, "{en_desc}"),
\t\t\t\t'type', "Debuff",
\t\t\t\t'Icon', "Mod/e6L4ECj/Icons/StatusEffects/{eid}.png",
\t\t\t\t'Shown', true,
\t\t\t\t'ShownSatelliteView', true,
\t\t\t}}),
"""


WI_COMPANION = f"""UndefineClass('WoundInfected')
DefineClass.WoundInfected = {{
\t__parents = {{ "StatusEffect" }},
\t__generated_by_class = "ModItemCharacterEffectCompositeDef",
\tobject_class = "StatusEffect",
\tDisplayName = T({WI_DN}, "Infected Wound"),
\tDescription = T({WI_DESC}, "Festering wound. Progress checks on the campaign map: failure can be fatal. Heavy trauma that fails to improve may become infected."),
\tAddEffectText = T({WI_ADD}, "<color EmStyle><DisplayName></color>"),
\tOnAdded = function(self, obj)
\t\tlocal init = rawget(_G, "JazzInitWoundInfectedProgressTimer")
\t\tif type(init) == "function" then
\t\t\tinit(self)
\t\tend
\tend,
\ttype = "Debuff",
\tIcon = "Mod/e6L4ECj/Icons/StatusEffects/WoundInfected.png",
\tShown = true,
\tShownSatelliteView = true,
\tHasFloatingText = true,
}}
"""

WI_ITEMS = f"""\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {{
\t\t\t\t'Id', "WoundInfected",
\t\t\t\t'object_class', "StatusEffect",
\t\t\t\t'DisplayName', T({WI_DN}, "Infected Wound"),
\t\t\t\t'Description', T({WI_DESC}, "Festering wound. Progress checks on the campaign map: failure can be fatal. Heavy trauma that fails to improve may become infected."),
\t\t\t\t'AddEffectText', T({WI_ADD}, "<color EmStyle><DisplayName></color>"),
\t\t\t\t'OnAdded', function(self, obj)
\t\t\t\t\tlocal init = rawget(_G, "JazzInitWoundInfectedProgressTimer")
\t\t\t\t\tif type(init) == "function" then
\t\t\t\t\t\tinit(self)
\t\t\t\t\tend
\t\t\t\tend,
\t\t\t\t'type', "Debuff",
\t\t\t\t'Icon', "Mod/e6L4ECj/Icons/StatusEffects/WoundInfected.png",
\t\t\t\t'Shown', true,
\t\t\t\t'ShownSatelliteView', true,
\t\t\t\t'HasFloatingText', true,
\t\t\t}}),
"""


def upsert_csv_row(path: Path, id_: int, en: str, ru: str, note: str) -> None:
    text = path.read_text(encoding="utf-8")
    # English.csv: id,en,en,,note  OR Russian.csv: id,en,ru,,note
    prefix = f"{id_},"
    lines = text.splitlines(keepends=True)
    out = []
    found = False
    new_line = None
    name = path.name
    if name == "English.csv":
        new_line = f"{id_},{en},{en},,{note}\n"
    else:
        new_line = f"{id_},{en},{ru},,{note}\n"
    for line in lines:
        if line.startswith(prefix):
            out.append(new_line)
            found = True
        else:
            out.append(line)
    if not found:
        if out and not out[-1].endswith("\n"):
            out[-1] += "\n"
        out.append(new_line)
    path.write_text("".join(out), encoding="utf-8")


def main() -> None:
    ids: list[str] = ["WoundInfected"] + [b[0] for b in BLOOD]

    # Companions
    (ROOT / "CharacterEffect" / "WoundInfected.lua").write_text(WI_COMPANION, encoding="utf-8")
    print("wrote WoundInfected.lua")
    for eid, _pct, ap, dn, desc, en_n, en_d, _ru_n, _ru_d in BLOOD:
        (ROOT / "CharacterEffect" / f"{eid}.lua").write_text(
            blood_companion(eid, ap, dn, desc, en_n, en_d), encoding="utf-8"
        )
        print("wrote", eid)

    # items.lua insert after Analgesia
    items = ROOT / "items.lua"
    text = items.read_text(encoding="utf-8")
    block = WI_ITEMS + "".join(
        blood_items(eid, ap, dn, desc, en_n, en_d)
        for eid, _pct, ap, dn, desc, en_n, en_d, _ru_n, _ru_d in BLOOD
    )
    if "'Id', \"WoundInfected\"" in text:
        print("items.lua already has WoundInfected — skip insert")
    else:
        marker = "\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {\n\t\t\t\t'Id', \"TraumaArmsLight\","
        if marker not in text:
            raise SystemExit("TraumaArmsLight marker missing")
        text = text.replace(marker, block + marker, 1)
        items.write_text(text, encoding="utf-8")
        print("items.lua: inserted MED-002 effects before TraumaArmsLight")

    # metadata code + resources
    meta = ROOT / "metadata.lua"
    mtext = meta.read_text(encoding="utf-8")
    code_chunk = "".join(f'\t\t"CharacterEffect/{eid}.lua",\n' for eid in ids)
    if "CharacterEffect/WoundInfected.lua" not in mtext:
        m_marker = '\t\t"CharacterEffect/TraumaArmsLight.lua",\n'
        if m_marker not in mtext:
            raise SystemExit("metadata code marker missing")
        mtext = mtext.replace(m_marker, code_chunk + m_marker, 1)
        print("metadata.code: MED-002 companions")
    res_chunk = "".join(
        f"""\t\tPlaceObj('ModResourcePreset', {{
\t\t\t'Class', "CharacterEffectCompositeDef",
\t\t\t'Id', "{eid}",
\t\t\t'ClassDisplayName', "Character effect",
\t\t}}),
"""
        for eid in ids
    )
    if "'Id', \"WoundInfected\"" not in mtext:
        r_marker = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "CharacterEffectCompositeDef",
\t\t\t'Id', "TraumaArmsLight",
\t\t\t'ClassDisplayName', "Character effect",
\t\t}),
"""
        if r_marker not in mtext:
            raise SystemExit("metadata resources marker missing")
        mtext = mtext.replace(r_marker, res_chunk + r_marker, 1)
        print("metadata.resources: MED-002")
    meta.write_text(mtext, encoding="utf-8")

    # Loc
    note = "jazz:MED-002"
    upsert_csv_row(ROOT / "English.csv", WI_DN, "Infected Wound", "Infected Wound", note)
    upsert_csv_row(
        ROOT / "English.csv",
        WI_DESC,
        "Festering wound. Progress checks on the campaign map: failure can be fatal. Heavy trauma that fails to improve may become infected.",
        "",
        note,
    )
    upsert_csv_row(ROOT / "English.csv", WI_ADD, "<color EmStyle><DisplayName></color>", "", note)
    upsert_csv_row(ROOT / "Russian.csv", WI_DN, "Infected Wound", "Инфицированная рана", note)
    upsert_csv_row(
        ROOT / "Russian.csv",
        WI_DESC,
        "Festering wound. Progress checks on the campaign map: failure can be fatal. Heavy trauma that fails to improve may become infected.",
        "Загноившаяся рана. Проверки на глобалке: провал может быть смертелен. Тяжёлая травма, не прошедшая улучшение, может инфицироваться.",
        note,
    )
    upsert_csv_row(ROOT / "Russian.csv", WI_ADD, "<color EmStyle><DisplayName></color>", "<color EmStyle><DisplayName></color>", note)

    for eid, _pct, ap, dn, desc, en_n, en_d, ru_n, ru_d in BLOOD:
        upsert_csv_row(ROOT / "English.csv", dn, en_n, en_n, note)
        upsert_csv_row(ROOT / "English.csv", desc, en_d, en_d, note)
        upsert_csv_row(ROOT / "Russian.csv", dn, en_n, ru_n, note)
        upsert_csv_row(ROOT / "Russian.csv", desc, en_d, ru_d, note)

    # Combat log strings
    for lid, en, ru in (
        (890000000010303, "<merc>'s wound became infected", "<merc>: рана загноилась"),
        (890000000010304, "<merc>'s infection subsided", "<merc>: инфекция отступила"),
        (890000000010305, "<merc> died of infection", "<merc> умер от инфекции"),
    ):
        upsert_csv_row(ROOT / "English.csv", lid, en, en, note)
        upsert_csv_row(ROOT / "Russian.csv", lid, en, ru, note)

    # Update Pain/Analgesia descriptions
    pain_en = "Each stack costs <color EmStyle><APLoss> AP</color> and <color EmStyle><cth_penalty>% chance to hit</color>. Decreases by one stack each turn. Clears when combat ends. Morphine clears Pain and blocks new stacks while Analgesia lasts."
    pain_ru = "Каждый стак: <color EmStyle><APLoss> ОД</color> и <color EmStyle><cth_penalty>% к точности</color>. −1 стак/ход. Снимается в конце боя. Морфий снимает боль и блокирует набор, пока действует обезболивание."
    upsert_csv_row(ROOT / "English.csv", 890000000010008, pain_en, pain_en, note)
    upsert_csv_row(ROOT / "Russian.csv", 890000000010008, pain_en, pain_ru, note)
    an_en = "Clears Pain and suppresses new Pain stacks. Does not stop bleeding or heal injuries."
    an_ru = "Снимает боль и блокирует набор новых стаков. Не останавливает кровь и не лечит травмы."
    upsert_csv_row(ROOT / "English.csv", 890000000010010, an_en, an_en, note)
    upsert_csv_row(ROOT / "Russian.csv", 890000000010010, an_en, an_ru, note)

    print("OK MED-002 CharacterEffects + loc")


if __name__ == "__main__":
    main()
