# -*- coding: utf-8 -*-
"""UNITS-006 Pierre GloryHog: CE override + Jazz_PierreRecruit signature CA + loc."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"

DN_GH = "890000000009927"
DESC_GH = "890000000009928"
DN_REC = "890000000009929"
DESC_REC = "890000000009933"
USED_ID = "890000000009934"
BOSS_ID = "890000000009932"

ROWS = {
    DN_GH: ("Жажда славы", "Glory Hog", "jazz:CharacterEffect/GloryHog.lua"),
    DESC_GH: (
        "Спецатака мачете <em>Charge</em> без прямой линии пути и даёт <em><temp_hp></em> <GameTerm('Grit')>. "
        "Активка: один раз за бой перевербовать видимого врага в союзника под ИИ (не боссы).",
        "Machete <em>Charge</em> without a straight-line path; grants <em><temp_hp></em> <GameTerm('Grit')>. "
        "Active: once per combat, recruit a visible enemy as an AI-controlled ally (not bosses).",
        "jazz:CharacterEffect/GloryHog.lua",
    ),
    DN_REC: ("Вербовка", "Recruit", "jazz:items.lua:Jazz_PierreRecruit"),
    DESC_REC: (
        "Перевербовать видимого врага в союзника под управлением ИИ. Один раз за бой. Не действует на боссов.",
        "Recruit a visible enemy as an AI-controlled ally. Once per combat. Does not affect bosses.",
        "jazz:items.lua:Jazz_PierreRecruit",
    ),
    USED_ID: ("Уже использовано в этом бою", "Already used this combat", "jazz:items.lua:Jazz_PierreRecruit"),
    BOSS_ID: ("Нельзя вербовать боссов", "Cannot recruit bosses", "jazz:items.lua:Jazz_PierreRecruit"),
}


def csv_escape(s: str) -> str:
    if any(c in s for c in ',"\n\r'):
        return '"' + s.replace('"', '""') + '"'
    return s


def patch_csv(path: Path) -> None:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines(keepends=True)
    found: set[str] = set()
    out: list[str] = []
    for line in lines:
        rid = line.split(",", 1)[0] if line else ""
        if rid in ROWS:
            ru, en, src = ROWS[rid]
            nl = "\r\n" if line.endswith("\r\n") else ("\n" if line.endswith("\n") else "\n")
            out.append(f"{rid},{csv_escape(ru)},{csv_escape(en)},,{src}{nl}")
            found.add(rid)
        else:
            out.append(line)
    missing = [rid for rid in ROWS if rid not in found]
    if missing:
        if out and not out[-1].endswith("\n"):
            out[-1] += "\n"
        for rid in missing:
            ru, en, src = ROWS[rid]
            out.append(f"{rid},{csv_escape(ru)},{csv_escape(en)},,{src}\n")
    path.write_text("".join(out), encoding="utf-8-sig")
    print(f"{path.name}: upsert {sorted(ROWS)}; appended={missing}")


CE_BLOCK = f"""\t\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {{
\t\t\t\t\t'Group', "Perk-Personal",
\t\t\t\t\t'Id', "GloryHog",
\t\t\t\t\t'object_class', "Perk",
\t\t\t\t\t'Parameters', {{
\t\t\t\t\t\tPlaceObj('PresetParamNumber', {{
\t\t\t\t\t\t\t'Name', "temp_hp",
\t\t\t\t\t\t\t'Value', 15,
\t\t\t\t\t\t\t'Tag', "<temp_hp>",
\t\t\t\t\t\t}}),
\t\t\t\t\t}},
\t\t\t\t\t'DisplayName', T({DN_GH}, --[[ModItemCharacterEffectCompositeDef GloryHog DisplayName]] "Жажда славы"),
\t\t\t\t\t'Description', T({DESC_GH}, --[[ModItemCharacterEffectCompositeDef GloryHog Description]] "Спецатака мачете <em>Charge</em> без прямой линии пути и даёт <em><temp_hp></em> <GameTerm('Grit')>. Активка: один раз за бой перевербовать видимого врага в союзника под ИИ (не боссы)."),
\t\t\t\t\t'Icon', "UI/Icons/Perks/GloryHog",
\t\t\t\t\t'Tier', "Personal",
\t\t\t\t}}),
"""

CA_BLOCK = """\t\t\t\tPlaceObj('ModItemCombatAction', {
\t\t\t\t\tActionPoints = 4000,
\t\t\t\t\tActionType = "Other",
\t\t\t\t\tActivePauseBehavior = "instant",
\t\t\t\t\tComment = "Pierre GloryHog List2 recruit (hotbar via GloryHog perk)",
\t\t\t\t\tConfigurableKeybind = false,
\t\t\t\t\tDescription = T(__DESC_REC__, --[[ModItemCombatAction Jazz_PierreRecruit Description]] "Перевербовать видимого врага в союзника под управлением ИИ. Один раз за бой. Не действует на боссов."),
\t\t\t\t\tDisplayName = T(__DN_REC__, --[[ModItemCombatAction Jazz_PierreRecruit DisplayName]] "Вербовка"),
\t\t\t\t\tGetAPCost = function (self, unit, args)
\t\t\t\t\t\treturn self.ActionPoints or 0
\t\t\t\t\tend,
\t\t\t\t\tGetActionDescription = function (self, units)
\t\t\t\t\t\treturn self.Description
\t\t\t\t\tend,
\t\t\t\t\tGetActionDisplayName = function (self, units)
\t\t\t\t\t\treturn self.DisplayName
\t\t\t\t\tend,
\t\t\t\t\tGetAnyTarget = function (self, units)
\t\t\t\t\t\tlocal t = Jazz_PierreRecruitGetTargets and Jazz_PierreRecruitGetTargets(units and units[1])
\t\t\t\t\t\treturn t and t[1]
\t\t\t\t\tend,
\t\t\t\t\tGetTargets = function (self, units)
\t\t\t\t\t\treturn Jazz_PierreRecruitGetTargets and Jazz_PierreRecruitGetTargets(units and units[1]) or empty_table
\t\t\t\t\tend,
\t\t\t\t\tGetUIState = function (self, units, args)
\t\t\t\t\t\tlocal unit = units and units[1]
\t\t\t\t\t\tif not unit or not HasPerk(unit, "GloryHog") then
\t\t\t\t\t\t\treturn "hidden"
\t\t\t\t\t\tend
\t\t\t\t\t\tlocal cost = self:GetAPCost(unit, args)
\t\t\t\t\t\tif cost < 0 then
\t\t\t\t\t\t\treturn "hidden"
\t\t\t\t\t\tend
\t\t\t\t\t\tif not g_Combat then
\t\t\t\t\t\t\treturn "disabled", AttackDisableReasons.CombatOnly
\t\t\t\t\t\tend
\t\t\t\t\t\tif unit.GetEffectValue and unit:GetEffectValue("Jazz_PierreRecruitUsed") then
\t\t\t\t\t\t\treturn "disabled", T(__USED_ID__, "Уже использовано в этом бою")
\t\t\t\t\t\tend
\t\t\t\t\t\tif not unit:UIHasAP(cost) then
\t\t\t\t\t\t\treturn "disabled"
\t\t\t\t\t\tend
\t\t\t\t\t\tlocal targets = self:GetTargets(units)
\t\t\t\t\t\tif not targets or not targets[1] then
\t\t\t\t\t\t\treturn "disabled", AttackDisableReasons.NoTarget
\t\t\t\t\t\tend
\t\t\t\t\t\treturn "enabled"
\t\t\t\t\tend,
\t\t\t\t\tIcon = "UI/Icons/Hud/perk_glory_hog",
\t\t\t\t\tIdDefault = "Jazz_PierreRecruitdefault",
\t\t\t\t\tIsAimableAttack = false,
\t\t\t\t\tKeybindingFromAction = "actionRedirectSignatureAbility",
\t\t\t\t\tMultiSelectBehavior = "first",
\t\t\t\t\tRequireState = "any",
\t\t\t\t\tRequireTargets = true,
\t\t\t\t\tExecute = function (self, units, args)
\t\t\t\t\t\tlocal unit = units[1]
\t\t\t\t\t\tif CombatActionIsBusy(self, unit) then return end
\t\t\t\t\t\tlocal ap = self:GetAPCost(unit, args)
\t\t\t\t\t\tNetStartCombatAction(self.id, unit, ap, args)
\t\t\t\t\tend,
\t\t\t\t\tRun = function (self, unit, ap, ...)
\t\t\t\t\t\tunit:SetActionCommand("Jazz_PierreRecruit", self.id, ap, ...)
\t\t\t\t\tend,
\t\t\t\t\tShowIn = "SignatureAbilities",
\t\t\t\t\tSortKey = 110,
\t\t\t\t\tUIBegin = function (self, units, args)
\t\t\t\t\t\tlocal mode_dlg = GetInGameInterfaceModeDlg()
\t\t\t\t\t\tlocal targets = self:GetTargets(units)
\t\t\t\t\t\tif IsKindOf(mode_dlg, "IModeCommonUnitControl") and targets and targets[1] then
\t\t\t\t\t\t\tlocal list = {}
\t\t\t\t\t\t\tfor _, t in ipairs(targets) do
\t\t\t\t\t\t\t\tlist[#list + 1] = {
\t\t\t\t\t\t\t\t\tDisplayName = t.GetLogName and t:GetLogName() or (t.Name or Untranslated("?")),
\t\t\t\t\t\t\t\t\ttarget = t,
\t\t\t\t\t\t\t\t\tuiCtx = t,
\t\t\t\t\t\t\t\t}
\t\t\t\t\t\t\tend
\t\t\t\t\t\t\tmode_dlg:ShowCombatActionTargetChoice(self, units, list, function(u, entry)
\t\t\t\t\t\t\t\tself:Execute({ u }, { target = entry.target })
\t\t\t\t\t\t\tend)
\t\t\t\t\t\t\treturn
\t\t\t\t\t\tend
\t\t\t\t\t\tCombatActionAttackStart(self, units, args, "IModeCombatAttack")
\t\t\t\t\tend,
\t\t\t\t\tgroup = "SignatureAbilities",
\t\t\t\t\tid = "Jazz_PierreRecruit",
\t\t\t\t}),
""".replace("__DESC_REC__", DESC_REC).replace("__DN_REC__", DN_REC).replace("__USED_ID__", USED_ID)


def ensure_items() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    changed = False
    has_gh = bool(re.search(r"'Id',\s*\"GloryHog\"", text))
    if not has_gh:
        needle = (
            "\t\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {\n"
            "\t\t\t\t\t'Group', \"Perk-Personal\",\n"
            "\t\t\t\t\t'Id', \"DangerClose\","
        )
        if needle not in text:
            raise SystemExit("DangerClose CE anchor not found for GloryHog insert")
        text = text.replace(needle, CE_BLOCK + needle, 1)
        changed = True
        print("Inserted GloryHog CE ModItem")
    else:
        pat = re.compile(
            r"\t\t\t\tPlaceObj\('ModItemCharacterEffectCompositeDef', \{\s*"
            r"'Group', \"Perk-Personal\",\s*'Id', \"GloryHog\",.*?"
            r"'Tier', \"Personal\",\s*\}\),",
            re.S,
        )
        text2, n = pat.subn(CE_BLOCK.rstrip() + "\n", text, count=1)
        if n:
            text = text2
            changed = True
            print("Replaced GloryHog CE ModItem")
        else:
            print("GloryHog CE present (leave as-is)")

    if 'id = "Jazz_PierreRecruit"' not in text:
        needle = (
            "\t\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {\n"
            "\t\t\t\t\t'Group', \"Perk-Personal\",\n"
            "\t\t\t\t\t'Id', \"GloryHog\","
        )
        if needle not in text:
            raise SystemExit("GloryHog CE not found for CA insert")
        text = text.replace(needle, CA_BLOCK + needle, 1)
        changed = True
        print("Inserted Jazz_PierreRecruit CA")
    else:
        print("Jazz_PierreRecruit CA already present")

    if changed:
        ITEMS.write_text(text, encoding="utf-8")
    print("items.lua OK")


def ensure_metadata() -> None:
    meta = META.read_text(encoding="utf-8")
    changed = False
    code_line = '"CharacterEffect/GloryHog.lua",'
    if code_line not in meta:
        anchor = '"CharacterEffect/DangerClose.lua",'
        if anchor not in meta:
            raise SystemExit("DangerClose code entry missing")
        meta = meta.replace(anchor, code_line + "\n\t\t" + anchor, 1)
        changed = True
        print("metadata.code: GloryHog.lua")

    presets = [
        (
            "'Id', \"GloryHog\",\n\t\t\t'ClassDisplayName', \"Character effect\",",
            """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "CharacterEffectCompositeDef",
\t\t\t'Id', "GloryHog",
\t\t\t'ClassDisplayName', "Character effect",
\t\t}),
""",
        ),
        (
            "'Id', \"Jazz_PierreRecruit\",\n\t\t\t'ClassDisplayName', \"Combat Actions\",",
            """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "CombatAction",
\t\t\t'Id', "Jazz_PierreRecruit",
\t\t\t'ClassDisplayName', "Combat Actions",
\t\t}),
""",
        ),
    ]
    for marker, block in presets:
        if marker not in meta:
            # insert before ExplodingPalm CombatAction preset
            exp = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "CombatAction",
\t\t\t'Id', "ExplodingPalm",
\t\t\t'ClassDisplayName', "Combat Actions",
\t\t}),
"""
            if exp not in meta:
                raise SystemExit("ExplodingPalm CombatAction preset anchor missing")
            meta = meta.replace(exp, block + exp, 1)
            changed = True
            print(f"metadata preset: {marker.split(chr(10))[0]}")

    m = re.search(r"'version',\s*(\d+)", meta)
    if not m:
        raise SystemExit("version missing")
    ver = int(m.group(1))
    meta = meta[: m.start(1)] + str(ver + 1) + meta[m.end(1) :]
    print(f"version {ver} -> {ver + 1}")

    bullet = (
        "- UNITS-006: Pierre GloryHog — recruit 1 enemy/combat (AI ally, not bosses); keep Charge+15 grit [no new game]"
        + "\\"
        + "n"
    )
    meta = re.sub(
        r"('last_changes',\s*\")",
        lambda mm: mm.group(1) + bullet,
        meta,
        count=1,
    )
    META.write_text(meta, encoding="utf-8")
    print("metadata updated")


def main() -> None:
    ensure_items()
    ensure_metadata()
    patch_csv(ROOT / "English.csv")
    patch_csv(ROOT / "Russian.csv")
    print("OK Pierre GloryHog / Jazz_PierreRecruit")


if __name__ == "__main__":
    main()
