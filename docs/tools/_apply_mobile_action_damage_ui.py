# -*- coding: utf-8 -*-
"""Patch mobile CombatAction GetActionDamage (and RunAndGun GetActionResults) in jazz/items.lua.

Vanilla formula `return base, base/volleys` makes CombatActionRollover show `volleys × (base/volleys)`
(e.g. 3×7). Replace with Jazz_GetMobileActionDamage (total bullets × per-bullet).
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"

RNG_DAMAGE = """\
					GetActionDamage = function (self, unit, target, args)
						return Jazz_GetMobileActionDamage(self, unit, args)
					end,"""

RNG_DAMAGE_OLD = """\
					GetActionDamage = function (self, unit, target, args)
						local weapon = self:GetAttackWeapons(unit, args)
						if not weapon then return 0 end
						local damage = unit:GetBaseDamage(weapon)
						local num_shots = self:ResolveValue("mobile_num_shots")
						return damage, damage / num_shots, 0
					end,"""

STORM_DAMAGE_OLD = """\
					GetActionDamage = function (self, unit, target, args)
						local weapon = self:GetAttackWeapons(unit, args)
						if not weapon then return 0 end
						local damage = unit:GetBaseDamage(weapon)
						local num_shots = self:ResolveValue("mobile_num_shots") * weapon:GetAutofireShots("JAZZ_SmgStorm")
						return damage, damage / num_shots, 0
					end,"""

# Two storm-like actions: SMGStorm uses JAZZ_SmgStorm; ManeuverAR runtime uses JAZZ_LargeAutoFire
SMGSTORM_DAMAGE = """\
					GetActionDamage = function (self, unit, target, args)
						return Jazz_GetMobileActionDamage(self, unit, args, "JAZZ_SmgStorm")
					end,"""

MANEUVER_DAMAGE = """\
					GetActionDamage = function (self, unit, target, args)
						return Jazz_GetMobileActionDamage(self, unit, args, "JAZZ_LargeAutoFire")
					end,"""

RNG_RESULTS_OLD = """\
					GetActionResults = function (self, unit, args)
						local weapon = self:GetAttackWeapons(unit)
						args.attack_id =  weapon:CanBurstfire() and "BurstFire" or "SingleShot"
						args.num_shots = weapon and weapon:GetAutofireShots(args.attack_id) 
						and weapon:CanBurstfire() or 1
						args.multishot = true
						return GetMobileShotResults(self, unit, args)
					end,"""

RNG_RESULTS_NEW = """\
					GetActionResults = function (self, unit, args)
						local weapon = self:GetAttackWeapons(unit)
						local can_burst = weapon and weapon:CanBurstfire()
						args.attack_id = can_burst and "BurstFire" or "SingleShot"
						args.num_shots = can_burst and (weapon:GetAutofireShots(args.attack_id) or 1) or 1
						args.multishot = true
						return GetMobileShotResults(self, unit, args)
					end,"""

MOBILESHOT_DAMAGE_OLD = """\
					GetActionDamage = function (self, unit, target, args)
						local rangedAttack = unit:GetDefaultAttackAction("ranged") 
						local weapon1, weapon2 = self:GetAttackWeapons(unit, args)
						if weapon1 and weapon2 then args.attack_id = "AttackDual" end
						
						return rangedAttack:GetActionDamage(unit, target, args)
					end,"""

MOBILESHOT_DAMAGE_NEW = """\
					GetActionDamage = function (self, unit, target, args)
						return Jazz_GetMobileActionDamage(self, unit, args, "SingleShot")
					end,"""


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    n = 0

    c_rng = text.count(RNG_DAMAGE_OLD)
    if c_rng != 2:
        raise SystemExit(f"RunAndGun/Carbine damage pattern count={c_rng} expected 2")
    text = text.replace(RNG_DAMAGE_OLD, RNG_DAMAGE)
    n += 2

    c_storm = text.count(STORM_DAMAGE_OLD)
    if c_storm != 2:
        raise SystemExit(f"Storm damage pattern count={c_storm} expected 2")
    text = text.replace(STORM_DAMAGE_OLD, SMGSTORM_DAMAGE, 1)
    text = text.replace(STORM_DAMAGE_OLD, MANEUVER_DAMAGE, 1)
    n += 2

    if RNG_RESULTS_OLD not in text:
        raise SystemExit("RunAndGun GetActionResults pattern not found")
    text = text.replace(RNG_RESULTS_OLD, RNG_RESULTS_NEW, 1)
    n += 1

    # Pistol MobileShot only (first occurrence of this GetActionDamage shape after MobileShot DisplayName)
    pistol_marker = 'ModItemCombatAction MobileShot DisplayName'
    idx = text.find(pistol_marker)
    if idx < 0:
        raise SystemExit("MobileShot marker missing")
    end = idx + 3000
    window = text[idx:end]
    if MOBILESHOT_DAMAGE_OLD not in window:
        raise SystemExit("MobileShot GetActionDamage not found near marker")
    window2 = window.replace(MOBILESHOT_DAMAGE_OLD, MOBILESHOT_DAMAGE_NEW, 1)
    text = text[:idx] + window2 + text[end:]
    n += 1

    ITEMS.write_text(text, encoding="utf-8", newline="\n")
    print(f"OK patched {n} mobile damage/results sites in items.lua")


if __name__ == "__main__":
    main()
