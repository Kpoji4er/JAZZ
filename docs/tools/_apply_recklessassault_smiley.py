# -*- coding: utf-8 -*-
"""UNITS-006 Smiley RecklessAssault List2: 4 attacks, SMG/carbine/AR, CTH bonus, no tiredness."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"

DN = "890000000009935"
DESC = "890000000009936"

ROWS = {
    DN: ("Безрассудный натиск", "Reckless Rush", "jazz:CharacterEffect/RecklessAssault.lua"),
    DESC: (
        "Улучшенный <em>Run and Gun</em>: до <em>4</em> атак с пистолет-пулемётом, карабином или автоматом. <em>+<cth_bonus></em> к точности. Без потери <GameTerm('Energy')>.",
        "Improved <em>Run and Gun</em>: up to <em>4</em> attacks with an SMG, carbine, or assault rifle. <em>+<cth_bonus></em> Accuracy. No <GameTerm('Energy')> loss.",
        "jazz:CharacterEffect/RecklessAssault.lua",
    ),
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
\t\t\t\t\t'Id', "RecklessAssault",
\t\t\t\t\t'object_class', "Perk",
\t\t\t\t\t'Parameters', {{
\t\t\t\t\t\tPlaceObj('PresetParamNumber', {{
\t\t\t\t\t\t\t'Name', "cth_bonus",
\t\t\t\t\t\t\t'Value', 15,
\t\t\t\t\t\t\t'Tag', "<cth_bonus>",
\t\t\t\t\t\t}}),
\t\t\t\t\t}},
\t\t\t\t\t'unit_reactions', {{
\t\t\t\t\t\tPlaceObj('UnitReaction', {{
\t\t\t\t\t\t\tEvent = "OnCalcChanceToHit",
\t\t\t\t\t\t\tHandler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
\t\t\t\t\t\t\t\tif target ~= attacker or not data or not action then
\t\t\t\t\t\t\t\t\treturn
\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\t\tif action.id ~= "RecklessAssault" then
\t\t\t\t\t\t\t\t\treturn
\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\t\tlocal bonus = self:ResolveValue("cth_bonus") or 15
\t\t\t\t\t\t\t\tApplyCthModifier_Add(self, data, bonus)
\t\t\t\t\t\t\tend,
\t\t\t\t\t\t}}),
\t\t\t\t\t}},
\t\t\t\t\t'DisplayName', T({DN}, --[[ModItemCharacterEffectCompositeDef RecklessAssault DisplayName]] "Безрассудный натиск"),
\t\t\t\t\t'Description', T({DESC}, --[[ModItemCharacterEffectCompositeDef RecklessAssault Description]] "Улучшенный <em>Run and Gun</em>: до <em>4</em> атак с пистолет-пулемётом, карабином или автоматом. <em>+<cth_bonus></em> к точности. Без потери <GameTerm('Energy')>."),
\t\t\t\t\t'Icon', "UI/Icons/Perks/RecklessAssault",
\t\t\t\t\t'Tier', "Personal",
\t\t\t\t}}),
"""

# CombatAction override — keep structure close to vanilla, List2 params/weapons.
CA_BLOCK = r"""				PlaceObj('ModItemCombatAction', {
					ActionCamera = true,
					ActionPoints = 5000,
					ActionType = "Ranged Attack",
					AimType = "mobile",
					ConfigurableKeybind = false,
					CostBasedOnWeapon = true,
					DisplayName = T(586171031351, --[[ModItemCombatAction RecklessAssault DisplayName]] "<placeholder>"),
					GetAPCost = function (self, unit, args)
						local add = (unit.stance ~= "Standing") and CombatActions.StanceStanding:GetAPCost(unit, args) or 0
						return self.ActionPoints + add
					end,
					GetActionDamage = function (self, unit, target, args)
						local weapon = self:GetAttackWeapons(unit, args)
						if not weapon then return 0 end
						local damage = unit:GetBaseDamage(weapon)
						local num_shots = self:ResolveValue("mobile_num_shots")
						return damage, damage / num_shots, 0
					end,
					GetActionDescription = function (self, units)
						return GetSignatureActionDescription(self)
					end,
					GetActionDisplayName = function (self, units)
						return GetSignatureActionDisplayName(self)
					end,
					GetActionResults = function (self, unit, args)
						local weapon = self:GetAttackWeapons(unit)
						args.attack_id = "BurstFire"
						args.num_shots = weapon and weapon:GetAutofireShots("BurstFire") or CombatActions.BurstFire:ResolveValue("num_shots")
						args.multishot = true
						return GetMobileShotResults(self, unit, args)
					end,
					GetAttackWeapons = function (self, unit, args)
						return Jazz_RecklessAssaultGetWeapon(unit, args)
					end,
					GetTargets = function (self, units)
						local unit = units[1]
						if unit then
							return table.ifilter(GetEnemies(unit), function(i, enemy)
								return IsValidTarget(enemy)
							end)
						end
						return {}
					end,
					GetUIState = function (self, units, args)
						if not g_Combat then
							return "disabled", AttackDisableReasons.CombatOnly
						end
						local unit = units and units[1]
						if unit and not Jazz_RecklessAssaultGetWeapon(unit, args) then
							return "disabled", AttackDisableReasons.WrongWeapon
						end
						return CombatActionGenericAttackGetUIState(self, units, args)
					end,
					Icon = "UI/Icons/Hud/perk_reckless_assault",
					IdDefault = "RecklessAssaultdefault",
					IsAimableAttack = false,
					KeybindingFromAction = "actionRedirectSignatureAbility",
					MultiSelectBehavior = "first",
					Parameters = {
						PlaceObj('PresetParamNumber', {
							'Name', "mobile_move_ap",
							'Value', 12,
							'Tag', "<mobile_move_ap>",
						}),
						PlaceObj('PresetParamNumber', {
							'Name', "mobile_num_shots",
							'Value', 4,
							'Tag', "<mobile_num_shots>",
						}),
					},
					RequireState = "any",
					Run = function (self, unit, ap, ...)
						unit:SetActionCommand("RecklessAssault", self.id, ap, ...)
					end,
					ShowIn = "SignatureAbilities",
					SortKey = 100,
					UIBegin = function (self, units, args)
						CombatActionAttackStart(self, units, args, "IModeCombatMovingAttack")
					end,
					group = "SignatureAbilities",
					id = "RecklessAssault",
				}),
"""


def ensure_items() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    changed = False
    has_ce = bool(re.search(r"'Id',\s*\"RecklessAssault\"", text))
    if not has_ce:
        needle = (
            "\t\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {\n"
            "\t\t\t\t\t'Group', \"Perk-Personal\",\n"
            "\t\t\t\t\t'Id', \"GloryHog\","
        )
        if needle not in text:
            raise SystemExit("GloryHog CE anchor missing for RecklessAssault insert")
        text = text.replace(needle, CE_BLOCK + needle, 1)
        changed = True
        print("Inserted RecklessAssault CE")
    else:
        print("RecklessAssault CE already in items")

    if not re.search(r"id\s*=\s*\"RecklessAssault\"", text):
        needle = (
            "\t\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {\n"
            "\t\t\t\t\t'Group', \"Perk-Personal\",\n"
            "\t\t\t\t\t'Id', \"RecklessAssault\","
        )
        if needle not in text:
            raise SystemExit("RecklessAssault CE missing for CA insert")
        text = text.replace(needle, CA_BLOCK + needle, 1)
        changed = True
        print("Inserted RecklessAssault CA")
    else:
        # Replace existing CA block
        pat = re.compile(
            r"\t\t\t\tPlaceObj\('ModItemCombatAction', \{\s*"
            r"ActionCamera = true,.*?id = \"RecklessAssault\",\s*\}\),",
            re.S,
        )
        text2, n = pat.subn(CA_BLOCK.rstrip() + "\n", text, count=1)
        if n:
            text = text2
            changed = True
            print("Replaced RecklessAssault CA")
        else:
            print("RecklessAssault CA present (leave)")

    if changed:
        ITEMS.write_text(text, encoding="utf-8")
    print("items.lua OK")


def ensure_metadata() -> None:
    meta = META.read_text(encoding="utf-8")
    code_line = '"CharacterEffect/RecklessAssault.lua",'
    if code_line not in meta:
        anchor = '"CharacterEffect/GloryHog.lua",'
        if anchor not in meta:
            raise SystemExit("GloryHog code entry missing")
        meta = meta.replace(anchor, code_line + "\n\t\t" + anchor, 1)
        print("metadata.code: RecklessAssault.lua")

    for marker, block in [
        (
            "'Id', \"RecklessAssault\",\n\t\t\t'ClassDisplayName', \"Character effect\",",
            """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "CharacterEffectCompositeDef",
\t\t\t'Id', "RecklessAssault",
\t\t\t'ClassDisplayName', "Character effect",
\t\t}),
""",
        ),
        (
            "'Id', \"RecklessAssault\",\n\t\t\t'ClassDisplayName', \"Combat Actions\",",
            """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "CombatAction",
\t\t\t'Id', "RecklessAssault",
\t\t\t'ClassDisplayName', "Combat Actions",
\t\t}),
""",
        ),
    ]:
        if marker not in meta:
            exp = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "CombatAction",
\t\t\t'Id', "Jazz_PierreRecruit",
\t\t\t'ClassDisplayName', "Combat Actions",
\t\t}),
"""
            if exp not in meta:
                raise SystemExit("Jazz_PierreRecruit preset anchor missing")
            meta = meta.replace(exp, block + exp, 1)
            print(f"metadata preset: {marker.splitlines()[0]}")

    m = re.search(r"'version',\s*(\d+)", meta)
    if not m:
        raise SystemExit("version missing")
    ver = int(m.group(1))
    meta = meta[: m.start(1)] + str(ver + 1) + meta[m.end(1) :]
    print(f"version {ver} -> {ver + 1}")

    bullet = (
        "- UNITS-006: Smiley RecklessAssault — 4 attacks SMG/carbine/AR +15 CTH; no Energy/Tiredness [no new game]"
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
    print("OK RecklessAssault List2")


if __name__ == "__main__":
    main()
