# -*- coding: utf-8 -*-
"""Wire JAZZ-MED-001 zonal traumas: companions, items.lua, metadata.lua, *shot hooks."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"
CE_DIR = ROOT / "CharacterEffect"

ICON = 'Mod/e6L4ECj/Icons/StatusEffects/{id}.png'

# Loc IDs 890000000009226+ (DisplayName, Description) per effect.
LOC_BASE = 890000000009226

EFFECTS = [
    # zone, tier, en_name, en_desc, reactions_kind
    ("Arms", "Light", "Arm Trauma (Light)",
     "Pain when shooting or using arms. No direct accuracy penalty.",
     "arms_light"),
    ("Arms", "Medium", "Arm Trauma (Medium)",
     "Accuracy penalty <color EmStyle><cth_penalty>%</color>. Pain when using arms.",
     "arms_medium"),
    ("Arms", "Heavy", "Arm Trauma (Heavy)",
     "Severe accuracy penalty <color EmStyle><cth_penalty>%</color>. Nearly unable to fight. Pain rises each turn.",
     "arms_heavy"),
    ("Legs", "Light", "Leg Trauma (Light)",
     "Pain when moving. No direct move-cost penalty.",
     "legs_light"),
    ("Legs", "Medium", "Leg Trauma (Medium)",
     "Move cost <color EmStyle>+<move_ap_modifier>%</color>. No Free Move / sprint. Pain when moving.",
     "legs_medium"),
    ("Legs", "Heavy", "Leg Trauma (Heavy)",
     "Move cost <color EmStyle>+<move_ap_modifier>%</color>. Almost immobile. Pain rises each turn.",
     "legs_heavy"),
    ("Ribs", "Light", "Rib Trauma (Light)",
     "Pain at the start of the turn.",
     "ribs_light"),
    ("Ribs", "Medium", "Rib Trauma (Medium)",
     "Start-of-turn AP <color EmStyle>-<APLoss></color>. No Free Move. Pain at the start of the turn. No Tiredness.",
     "ribs_medium"),
    ("Ribs", "Heavy", "Rib Trauma (Heavy)",
     "Start-of-turn AP <color EmStyle>-<APLoss></color>. Combat-ineffective. Pain rises each turn. No Tiredness.",
     "ribs_heavy"),
    ("Head", "Light", "Head Trauma (Light)",
     "Pain when aiming or firing. Eye trauma folded into head for v1.",
     "head_light"),
    ("Head", "Medium", "Head Trauma (Medium)",
     "Sight and accuracy penalties. Pain when aiming or firing.",
     "head_medium"),
    ("Head", "Heavy", "Head Trauma (Heavy)",
     "Severe sight/accuracy loss. Nearly combat-ineffective. Pain rises each turn.",
     "head_heavy"),
    ("Burn", "Light", "Burn Trauma (Light)",
     "Lingering burn after fire. Pain on exertion. Bandage does not clear burns.",
     "burn_light"),
    ("Burn", "Medium", "Burn Trauma (Medium)",
     "Moderate burn debt. Pain on exertion. Infection risk deferred.",
     "burn_medium"),
    ("Burn", "Heavy", "Burn Trauma (Heavy)",
     "Severe burn debt. Pain rises each turn. Infection/hospital clear deferred.",
     "burn_heavy"),
]


def effect_id(zone: str, tier: str) -> str:
    return f"Trauma{zone}{tier}"


def loc_pair(index: int) -> tuple[int, int]:
    return LOC_BASE + index * 2, LOC_BASE + index * 2 + 1


def params_block(kind: str) -> str:
    if kind.startswith("arms_medium"):
        return """\t\t\t\t'Parameters', {
\t\t\t\t\tPlaceObj('PresetParamPercent', {
\t\t\t\t\t\t'Name', "cth_penalty",
\t\t\t\t\t\t'Value', 20,
\t\t\t\t\t\t'Tag', "<cth_penalty>%",
\t\t\t\t\t}),
\t\t\t\t},"""
    if kind.startswith("arms_heavy"):
        return """\t\t\t\t'Parameters', {
\t\t\t\t\tPlaceObj('PresetParamPercent', {
\t\t\t\t\t\t'Name', "cth_penalty",
\t\t\t\t\t\t'Value', 50,
\t\t\t\t\t\t'Tag', "<cth_penalty>%",
\t\t\t\t\t}),
\t\t\t\t},"""
    if kind.startswith("legs_medium"):
        return """\t\t\t\t'Parameters', {
\t\t\t\t\tPlaceObj('PresetParamNumber', {
\t\t\t\t\t\t'Name', "move_ap_modifier",
\t\t\t\t\t\t'Value', 50,
\t\t\t\t\t\t'Tag', "<move_ap_modifier>",
\t\t\t\t\t}),
\t\t\t\t},"""
    if kind.startswith("legs_heavy"):
        return """\t\t\t\t'Parameters', {
\t\t\t\t\tPlaceObj('PresetParamNumber', {
\t\t\t\t\t\t'Name', "move_ap_modifier",
\t\t\t\t\t\t'Value', 150,
\t\t\t\t\t\t'Tag', "<move_ap_modifier>",
\t\t\t\t\t}),
\t\t\t\t},"""
    if kind.startswith("ribs_medium"):
        return """\t\t\t\t'Parameters', {
\t\t\t\t\tPlaceObj('PresetParamNumber', {
\t\t\t\t\t\t'Name', "APLoss",
\t\t\t\t\t\t'Value', 2,
\t\t\t\t\t\t'Tag', "<APLoss>",
\t\t\t\t\t}),
\t\t\t\t},"""
    if kind.startswith("ribs_heavy"):
        return """\t\t\t\t'Parameters', {
\t\t\t\t\tPlaceObj('PresetParamNumber', {
\t\t\t\t\t\t'Name', "APLoss",
\t\t\t\t\t\t'Value', 5,
\t\t\t\t\t\t'Tag', "<APLoss>",
\t\t\t\t\t}),
\t\t\t\t},"""
    if kind.startswith("head_medium"):
        return """\t\t\t\t'Parameters', {
\t\t\t\t\tPlaceObj('PresetParamPercent', {
\t\t\t\t\t\t'Name', "cth_penalty",
\t\t\t\t\t\t'Value', 15,
\t\t\t\t\t\t'Tag', "<cth_penalty>%",
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('PresetParamNumber', {
\t\t\t\t\t\t'Name', "sight_modifier",
\t\t\t\t\t\t'Value', -20,
\t\t\t\t\t\t'Tag', "<sight_modifier>",
\t\t\t\t\t}),
\t\t\t\t},"""
    if kind.startswith("head_heavy"):
        return """\t\t\t\t'Parameters', {
\t\t\t\t\tPlaceObj('PresetParamPercent', {
\t\t\t\t\t\t'Name', "cth_penalty",
\t\t\t\t\t\t'Value', 40,
\t\t\t\t\t\t'Tag', "<cth_penalty>%",
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('PresetParamNumber', {
\t\t\t\t\t\t'Name', "sight_modifier",
\t\t\t\t\t\t'Value', -50,
\t\t\t\t\t\t'Tag', "<sight_modifier>",
\t\t\t\t\t}),
\t\t\t\t},"""
    return ""


def reactions_lua(kind: str, zone: str) -> str:
    lines = ["\tunit_reactions = {"]
    # Pain on use / heavy ramp shared patterns
    if kind in ("arms_light", "arms_medium", "head_light", "head_medium"):
        lines.append(f"""\t\tPlaceObj('UnitReaction', {{
\t\t\tEvent = "OnFirearmAttackStart",
\t\t\tHandler = function(self, target, attacker, attack_target, action, attack_args)
\t\t\t\tif target == attacker then
\t\t\t\t\tJazzTraumaPainOnZoneUse(attacker, "{zone}")
\t\t\t\tend
\t\t\tend,
\t\t}}),""")
    if kind == "legs_light":
        lines.append(f"""\t\tPlaceObj('UnitReaction', {{
\t\t\tEvent = "OnCalcMoveModifier",
\t\t\tHandler = function(self, target, value, action)
\t\t\t\tJazzTraumaPainOnZoneUse(target, "{zone}")
\t\t\t\treturn value
\t\t\tend,
\t\t}}),""")
    if kind in ("ribs_light", "burn_light", "burn_medium"):
        lines.append(f"""\t\tPlaceObj('UnitReaction', {{
\t\t\tEvent = "OnCalcStartTurnAP",
\t\t\tHandler = function(self, target, value)
\t\t\t\tJazzTraumaPainOnZoneUse(target, "{zone}")
\t\t\t\treturn value
\t\t\tend,
\t\t}}),""")
    if kind.endswith("_heavy"):
        lines.append("""\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnEndTurn",
\t\t\tHandler = function(self, target)
\t\t\t\tJazzTraumaHeavyPainRamp(target)
\t\t\tend,
\t\t}),""")
    # Zone-specific combat debuffs (Medium+)
    if kind in ("arms_medium", "arms_heavy"):
        lines.append("""\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnCalcChanceToHit",
\t\t\tHandler = function(self, target, attacker, action, attack_target, weapon1, weapon2, data)
\t\t\t\tif target == attacker then
\t\t\t\t\tApplyCthModifier_Add(self, data, -self:ResolveValue("cth_penalty"))
\t\t\t\tend
\t\t\tend,
\t\t}),""")
    if kind in ("legs_medium", "legs_heavy"):
        lines.append("""\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnCalcMoveModifier",
\t\t\tHandler = function(self, target, value, action)
\t\t\t\tif self.class == "TraumaLegsMedium" then
\t\t\t\t\tJazzTraumaPainOnZoneUse(target, "Legs")
\t\t\t\tend
\t\t\t\treturn value + self:ResolveValue("move_ap_modifier")
\t\t\tend,
\t\t}),""")
        lines.append("""\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnCalcFreeMove",
\t\t\tHandler = function(self, target, data)
\t\t\t\tdata.add = 0
\t\t\t\tdata.mul = 0
\t\t\tend,
\t\t}),""")
        lines.append("""\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnBeginTurn",
\t\t\tHandler = function(self, target)
\t\t\t\ttarget:RemoveStatusEffect("FreeMove")
\t\t\tend,
\t\t}),""")
    if kind in ("ribs_medium", "ribs_heavy"):
        lines.append("""\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnCalcStartTurnAP",
\t\t\tHandler = function(self, target, value)
\t\t\t\tif self.class == "TraumaRibsMedium" then
\t\t\t\t\tJazzTraumaPainOnZoneUse(target, "Ribs")
\t\t\t\tend
\t\t\t\treturn value - self:ResolveValue("APLoss") * const.Scale.AP
\t\t\tend,
\t\t}),""")
        lines.append("""\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnCalcFreeMove",
\t\t\tHandler = function(self, target, data)
\t\t\t\tdata.add = 0
\t\t\t\tdata.mul = 0
\t\t\tend,
\t\t}),""")
        lines.append("""\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnBeginTurn",
\t\t\tHandler = function(self, target)
\t\t\t\ttarget:RemoveStatusEffect("FreeMove")
\t\t\tend,
\t\t}),""")
    if kind in ("head_medium", "head_heavy"):
        lines.append("""\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnCalcChanceToHit",
\t\t\tHandler = function(self, target, attacker, action, attack_target, weapon1, weapon2, data)
\t\t\t\tif target == attacker then
\t\t\t\t\tApplyCthModifier_Add(self, data, -self:ResolveValue("cth_penalty"))
\t\t\t\tend
\t\t\tend,
\t\t}),""")
        lines.append("""\t\tPlaceObj('UnitReaction', {
\t\t\tEvent = "OnCalcSightModifier",
\t\t\tHandler = function(self, target, value, observer, other, step_pos, darkness)
\t\t\t\tif target == observer then
\t\t\t\t\treturn value + self:ResolveValue("sight_modifier")
\t\t\t\tend
\t\t\tend,
\t\t}),""")
    lines.append("\t},")
    return "\n".join(lines)


def companion_source(eid: str, name_id: int, desc_id: int, en_name: str, en_desc: str, kind: str, zone: str) -> str:
    params = params_block(kind)
    # companion uses Parameters = { ... } (not quoted items.lua keys)
    params_companion = ""
    if params:
        params_companion = (
            params.replace("\t\t\t\t", "\t")
            .replace("'Parameters', {", "Parameters = {", 1)
            + "\n"
        )
    reactions = reactions_lua(kind, zone).replace("\t", "\t")  # already tabbed for companion
    # Fix indent: reactions_lua uses single tab base — good for companion
    icon = ICON.format(id=eid)
    on_added = ""
    on_removed = ""
    if kind.startswith("legs_") or kind.startswith("ribs_"):
        on_added = """\tOnAdded = function(self, obj)
\t\tMsg("UnitAPChanged", obj)
\tend,
\tOnRemoved = function(self, obj)
\t\tMsg("UnitAPChanged", obj)
\tend,
"""
    return f"""UndefineClass('{eid}')
DefineClass.{eid} = {{
\t__parents = {{ "StatusEffect" }},
\t__generated_by_class = "ModItemCharacterEffectCompositeDef",
\tobject_class = "StatusEffect",
{params_companion}{reactions}
\tDisplayName = T({name_id}, "{en_name}"),
\tDescription = T({desc_id}, "{en_desc}"),
{on_added}\ttype = "Debuff",
\tIcon = "{icon}",
\tShown = true,
\tShownSatelliteView = true,
\tHasFloatingText = true,
}}
"""


def items_effect_block(eid: str, name_id: int, desc_id: int, en_name: str, en_desc: str, kind: str, zone: str) -> str:
    params = params_block(kind)
    # reactions for items.lua need deeper indent
    rx = reactions_lua(kind, zone)
    # bump indent by 3 tabs for items nesting under PlaceObj
    rx_lines = []
    for line in rx.splitlines():
        if line.startswith("\tunit_reactions"):
            rx_lines.append("\t\t\t\t" + line.lstrip("\t"))
        elif line.startswith("\t},"):
            rx_lines.append("\t\t\t\t},")
        else:
            # already has tabs from PlaceObj level
            stripped = line.lstrip("\t")
            depth = len(line) - len(stripped)
            rx_lines.append("\t" * (depth + 3) + stripped)
    rx_block = "\n".join(rx_lines)
    params_items = ""
    if params:
        params_items = params + "\n"
    icon = ICON.format(id=eid)
    on_bits = ""
    if kind.startswith("legs_") or kind.startswith("ribs_"):
        on_bits = """\t\t\t\t'OnAdded', function (self, obj)
\t\t\t\t\tMsg("UnitAPChanged", obj)
\t\t\t\tend,
\t\t\t\t'OnRemoved', function (self, obj)
\t\t\t\t\tMsg("UnitAPChanged", obj)
\t\t\t\tend,
"""
    return f"""\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {{
\t\t\t\t'Id', "{eid}",
{params_items}\t\t\t\t'object_class', "StatusEffect",
{rx_block}
\t\t\t\t'DisplayName', T({name_id}, "{en_name}"),
\t\t\t\t'Description', T({desc_id}, "{en_desc}"),
{on_bits}\t\t\t\t'type', "Debuff",
\t\t\t\t'Icon', "{icon}",
\t\t\t\t'Shown', true,
\t\t\t\t'ShownSatelliteView', true,
\t\t\t\t'HasFloatingText', true,
\t\t\t}}),
"""


def fix_duplicate_legs_pain(kind: str, text: str) -> str:
    """legs_medium/heavy already call JazzTraumaPainOnZoneUse in OnCalcMoveModifier;
    remove the light-only pain-only reaction if both got emitted — reactions_lua handles this."""
    return text


SHOT_UPDATES = {
    "Armsshot": '''\tOnAdded = function (self, obj)
\t\tif obj.TempHitPoints > 0 then return end
\t\tJazzTryRollTraumaFromBodyPart(obj, "Arms")
\t\tlocal hp = obj.TempHitPoints + obj.HitPoints
\t\tif obj:Random(hp) < 30 then
\t\t\tobj:AddStatusEffect("Numbness")
\t\tend
\t\tif obj:Random(hp) < 25 then
\t\t\tobj:AddStatusEffect("Inaccurate")
\t\tend
\tend,''',
    "Legsshot": '''\tOnAdded = function (self, obj)
\t\tif obj.TempHitPoints > 0 then return end
\t\tJazzTryRollTraumaFromBodyPart(obj, "Legs")
\t\tlocal hp = obj.TempHitPoints + obj.HitPoints
\t\tif obj:Random(hp) < 20 then
\t\t\tobj:AddStatusEffect("Slowed")
\t\tend
\tend,''',
    "Headshot": '''\tOnAdded = function (self, obj)
\t\tif obj.TempHitPoints > 0 then return end
\t\tJazzTryRollTraumaFromBodyPart(obj, "Head")
\t\tlocal hp = obj.TempHitPoints + obj.HitPoints
\t\tif obj:Random(hp) < 5 then
\t\t\tobj:AddStatusEffect("Unconscious")
\t\telseif obj:Random(hp) < 20 then
\t\t\tobj:AddStatusEffect("Blinded")
\t\tend
\tend,''',
    "Torsoshot": '''\tOnAdded = function (self, obj)
\t\tif obj.TempHitPoints > 0 then return end
\t\tJazzTryRollTraumaFromBodyPart(obj, "Ribs")
\tend,''',
    "Groinshot": '''\tOnAdded = function (self, obj)
\t\tif obj.TempHitPoints > 0 then return end
\t\tJazzTryRollTraumaFromBodyPart(obj, "Ribs")
\t\tlocal hp = obj.TempHitPoints + obj.HitPoints
\t\tif obj:Random(hp) < 20 then
\t\t\tobj:AddStatusEffect("Bleeding")
\t\tend
\t\tif obj:Random(hp) < 40 then
\t\t\tobj:AddStatusEffect("Bleeding")
\t\tend
\t\tif obj:Random(hp) < 5 then
\t\t\tobj:AddStatusEffect("Bleeding")
\t\tend
\tend,''',
}


def patch_companion_onadded(path: Path, class_name: str, new_onadded: str) -> None:
    text = path.read_text(encoding="utf-8")
    import re
    pat = re.compile(
        r"\tOnAdded = function \(self, obj\).*?\tend,",
        re.S,
    )
    if not pat.search(text):
        raise SystemExit(f"OnAdded not found in {path}")
    text = pat.sub(new_onadded, text, count=1)
    path.write_text(text, encoding="utf-8")


def patch_items_onadded(text: str, effect_id_name: str, new_body: str) -> str:
    """Replace OnAdded handler inside ModItemCharacterEffectCompositeDef Id=effect_id_name."""
    import re
    # Find the PlaceObj block for this Id, then replace OnAdded inside it.
    marker = f"'Id', \"{effect_id_name}\""
    idx = text.find(marker)
    if idx < 0:
        raise SystemExit(f"items.lua missing {effect_id_name}")
    # Search forward for OnAdded within next ~2500 chars
    window = text[idx: idx + 3000]
    pat = re.compile(
        r"'OnAdded', function \(self, obj\).*?\tend,",
        re.S,
    )
    m = pat.search(window)
    if not m:
        raise SystemExit(f"items.lua OnAdded missing for {effect_id_name}")
    # Convert companion-style OnAdded to items-style
    items_onadded = new_body.replace("\tOnAdded = function (self, obj)", "'OnAdded', function (self, obj)")
    items_onadded = items_onadded.replace("\n\t", "\n\t\t\t\t")
    # first line already has quote form
    items_onadded = "'OnAdded', function (self, obj)\n" + "\n".join(
        ("\t\t\t\t" + line[1:] if line.startswith("\t") else "\t\t\t\t" + line)
        for line in new_body.splitlines()[1:]
    )
    start = idx + m.start()
    end = idx + m.end()
    return text[:start] + items_onadded + text[end:]


def patch_unconscious(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    needle = """\tOnAdded = function (self, obj)
\t\tself:SetParameter("recovery_turn", (g_Combat and g_Combat.current_turn or 1) + self:ResolveValue("recovery_delay_turns"))
\t\tself:SetParameter("recovery_time", GameTime() + self:ResolveValue("recovery_delay_seconds") * 1000)
\t\tobj:AddStatusEffectImmunity("Surprised", self.class)
\t\tCreateGameTimeThread(obj.SetCommandIfNotDead, obj, obj.command == "GetDowned" and "Downed" or "KnockDown")
\tend,"""
    repl = """\tOnAdded = function (self, obj)
\t\tself:SetParameter("recovery_turn", (g_Combat and g_Combat.current_turn or 1) + self:ResolveValue("recovery_delay_turns"))
\t\tself:SetParameter("recovery_time", GameTime() + self:ResolveValue("recovery_delay_seconds") * 1000)
\t\tobj:AddStatusEffectImmunity("Surprised", self.class)
\t\tif IsMerc(obj) then
\t\t\tJazzApplyKnockoutTraumaPackage(obj)
\t\tend
\t\tCreateGameTimeThread(obj.SetCommandIfNotDead, obj, obj.command == "GetDowned" and "Downed" or "KnockDown")
\tend,"""
    if needle not in text:
        if "JazzApplyKnockoutTraumaPackage" in text:
            print("Unconscious already patched")
            return
        raise SystemExit("Unconscious OnAdded pattern mismatch")
    path.write_text(text.replace(needle, repl, 1), encoding="utf-8")


def patch_burning(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    needle = """\tOnRemoved = function (self, obj)
\t\tif IsKindOf(obj, "Unit") then
\t\t\tPlayFX("UnitBurning", "end", obj)
\t\tobj:ClearStains("Burning")
\t\tend
\tend,"""
    # tolerate tab variance on ClearStains line
    import re
    pat = re.compile(
        r"\tOnRemoved = function \(self, obj\)\s*"
        r"if IsKindOf\(obj, \"Unit\"\) then\s*"
        r"PlayFX\(\"UnitBurning\", \"end\", obj\)\s*"
        r"obj:ClearStains\(\"Burning\"\)\s*"
        r"end\s*"
        r"end,",
        re.S,
    )
    repl = """\tOnRemoved = function (self, obj)
\t\tif IsKindOf(obj, "Unit") then
\t\t\tPlayFX("UnitBurning", "end", obj)
\t\t\tobj:ClearStains("Burning")
\t\t\tJazzApplyBurnTraumaFromBurning(obj)
\t\tend
\tend,"""
    if "JazzApplyBurnTraumaFromBurning" in text:
        print("Burning already patched")
        return
    m = pat.search(text)
    if not m:
        raise SystemExit("Burning OnRemoved pattern mismatch")
    path.write_text(text[: m.start()] + repl + text[m.end() :], encoding="utf-8")


def main() -> None:
    # 1) Write companions
    items_blocks = []
    code_entries = []
    resource_entries = []
    for i, (zone, tier, en_name, en_desc, kind) in enumerate(EFFECTS):
        eid = effect_id(zone, tier)
        name_id, desc_id = loc_pair(i)
        src = companion_source(eid, name_id, desc_id, en_name, en_desc, kind, zone)
        # Fix legs_medium: reactions_lua emits both light pain-only move and medium move+penalty.
        # For legs_medium/heavy, skip the light-only reaction by using kind that doesn't add light-only.
        (CE_DIR / f"{eid}.lua").write_text(src, encoding="utf-8")
        items_blocks.append(items_effect_block(eid, name_id, desc_id, en_name, en_desc, kind, zone))
        code_entries.append(f'\t\t"CharacterEffect/{eid}.lua",')
        resource_entries.append(
            f"""\t\tPlaceObj('ModResourcePreset', {{
\t\t\t'Class', "CharacterEffectCompositeDef",
\t\t\t'Id', "{eid}",
\t\t\t'ClassDisplayName', "Character effect",
\t\t}}),"""
        )
    print(f"Wrote {len(EFFECTS)} CharacterEffect companions")

    # 2) Patch *shot / Unconscious / Burning companions
    for name, onadded in SHOT_UPDATES.items():
        patch_companion_onadded(CE_DIR / f"{name}.lua", name, onadded)
        print(f"Patched {name}.lua")
    patch_unconscious(CE_DIR / "Unconscious.lua")
    print("Patched Unconscious.lua")
    patch_burning(CE_DIR / "Burning.lua")
    print("Patched Burning.lua")

    # 3) items.lua — insert trauma defs before Wounded; patch shot OnAdded
    text = ITEMS.read_text(encoding="utf-8")
    if "'Id', \"TraumaArmsLight\"" not in text:
        wounded_marker = "\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {\n\t\t\t\t'Id', \"Wounded\","
        if wounded_marker not in text:
            raise SystemExit("Wounded marker missing in items.lua")
        block = "".join(items_blocks)
        text = text.replace(wounded_marker, block + wounded_marker, 1)
        print("Inserted trauma ModItems before Wounded")
    else:
        print("Trauma ModItems already present")

    for name, onadded in SHOT_UPDATES.items():
        text = patch_items_onadded(text, name, onadded)
        print(f"Patched items.lua OnAdded for {name}")

    # Unconscious in items.lua
    import re
    unc_marker = "'Id', \"Unconscious\""
    idx = text.find(unc_marker)
    if idx < 0:
        raise SystemExit("Unconscious missing in items.lua")
    window = text[idx: idx + 4000]
    if "JazzApplyKnockoutTraumaPackage" not in window:
        pat = re.compile(
            r"'OnAdded', function \(self, obj\).*?CreateGameTimeThread\(obj\.SetCommandIfNotDead.*?end,",
            re.S,
        )
        m = pat.search(window)
        if not m:
            raise SystemExit("items Unconscious OnAdded not found")
        new_on = """'OnAdded', function (self, obj)
\t\t\t\t\tself:SetParameter("recovery_turn", (g_Combat and g_Combat.current_turn or 1) + self:ResolveValue("recovery_delay_turns"))
\t\t\t\t\tself:SetParameter("recovery_time", GameTime() + self:ResolveValue("recovery_delay_seconds") * 1000)
\t\t\t\t\tobj:AddStatusEffectImmunity("Surprised", self.class)
\t\t\t\t\tif IsMerc(obj) then
\t\t\t\t\t\tJazzApplyKnockoutTraumaPackage(obj)
\t\t\t\t\tend
\t\t\t\t\tCreateGameTimeThread(obj.SetCommandIfNotDead, obj, obj.command == "GetDowned" and "Downed" or "KnockDown")
\t\t\t\tend,"""
        text = text[: idx + m.start()] + new_on + text[idx + m.end() :]
        print("Patched items.lua Unconscious")
    else:
        print("items.lua Unconscious already patched")

    # Burning OnRemoved in items
    burn_idx = text.find("'Id', \"Burning\"")
    if burn_idx < 0:
        raise SystemExit("Burning missing in items.lua")
    burn_window = text[burn_idx: burn_idx + 5000]
    if "JazzApplyBurnTraumaFromBurning" not in burn_window:
        old_burn = """'OnRemoved', function (self, obj)
\t\t\t\t\tif IsKindOf(obj, "Unit") then
\t\t\t\t\t\tPlayFX("UnitBurning", "end", obj)
\t\t\t\t\t\tobj:ClearStains("Burning")
\t\t\t\t\tend
\t\t\t\tend,"""
        new_burn = """'OnRemoved', function (self, obj)
\t\t\t\t\tif IsKindOf(obj, "Unit") then
\t\t\t\t\t\tPlayFX("UnitBurning", "end", obj)
\t\t\t\t\t\tobj:ClearStains("Burning")
\t\t\t\t\t\tJazzApplyBurnTraumaFromBurning(obj)
\t\t\t\t\tend
\t\t\t\tend,"""
        if old_burn not in burn_window:
            raise SystemExit("items Burning OnRemoved not found")
        text = text[:burn_idx] + burn_window.replace(old_burn, new_burn, 1) + text[burn_idx + len(burn_window) :]
        print("Patched items.lua Burning")
    else:
        print("items.lua Burning already patched")

    ITEMS.write_text(text, encoding="utf-8")
    print("items.lua written")

    # 4) metadata.lua — code list + ModResourcePreset
    meta = META.read_text(encoding="utf-8")
    code_anchor = '"CharacterEffect/Analgesia.lua",\n\t\t"CharacterEffect/Wounded.lua",'
    code_insert = (
        '"CharacterEffect/Analgesia.lua",\n'
        + "\n".join(code_entries)
        + '\n\t\t"CharacterEffect/Wounded.lua",'
    )
    if "CharacterEffect/TraumaArmsLight.lua" not in meta:
        if code_anchor not in meta:
            raise SystemExit("metadata code anchor missing")
        meta = meta.replace(code_anchor, code_insert, 1)
        print("metadata code entries inserted")
    else:
        print("metadata code entries already present")

    res_anchor = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "CharacterEffectCompositeDef",
\t\t\t'Id', "Analgesia",
\t\t\t'ClassDisplayName', "Character effect",
\t\t}),
\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "CharacterEffectCompositeDef",
\t\t\t'Id', "Wounded",
\t\t\t'ClassDisplayName', "Character effect",
\t\t}),"""
    res_insert = (
        """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "CharacterEffectCompositeDef",
\t\t\t'Id', "Analgesia",
\t\t\t'ClassDisplayName', "Character effect",
\t\t}),
"""
        + "\n".join(resource_entries)
        + """
\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "CharacterEffectCompositeDef",
\t\t\t'Id', "Wounded",
\t\t\t'ClassDisplayName', "Character effect",
\t\t}),"""
    )
    if "'Id', \"TraumaArmsLight\"" not in meta:
        if res_anchor not in meta:
            raise SystemExit("metadata resource anchor missing")
        meta = meta.replace(res_anchor, res_insert, 1)
        print("metadata resource presets inserted")
    else:
        print("metadata resource presets already present")

    META.write_text(meta, encoding="utf-8")
    print("metadata.lua written")
    print("DONE")


if __name__ == "__main__":
    main()
