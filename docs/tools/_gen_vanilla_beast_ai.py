"""Extract vanilla CombatAI functions into Code/System_AI_VanillaBeasts.lua."""
from __future__ import annotations

from pathlib import Path

JA3 = Path(r"F:\SteamLibrary\steamapps\common\Jagged Alliance 3")
SRC = JA3 / "ModTools" / "Src" / "Lua" / "Tactical" / "CombatAI.lua"
OUT = Path(__file__).resolve().parents[2] / "Code" / "System_AI_VanillaBeasts.lua"

RANGES = {
    "AIGetAttackTargetingOptions": (162, 188),
    "AIPlayAttacks": (190, 397),
    "AIExecuteUnitBehavior": (486, 507),
    "AITakeCover": (509, 536),
    "AIFindDestinations": (645, 714),
    "AICreateContext": (718, 847),
    "AIUpdateDestLosCache": (862, 970),
    "AICalcAttacksAndAim": (976, 1007),
    "AIBuildArchetypePaths": (1009, 1133),
    "AIScoreDest": (1135, 1205),
    "AIEnumValidDests": (1208, 1260),
    "AIFindOptimalLocation": (1262, 1377),
    "AIGetWeaponCheckRange": (1379, 1391),
    "AIPrecalcDamageScore": (1418, 1705),
}

RENAMES = [
    ("function AIGetAttackTargetingOptions", "function JazzAI_VanillaGetAttackTargetingOptions"),
    ("function AIPlayAttacks", "function JazzAI_VanillaPlayAttacks"),
    ("function AIExecuteUnitBehavior", "function JazzAI_VanillaExecuteUnitBehavior"),
    ("function AITakeCover", "function JazzAI_VanillaTakeCover"),
    ("function AIFindDestinations", "function JazzAI_VanillaFindDestinations"),
    ("function AICreateContext", "function JazzAI_VanillaCreateContext"),
    ("function AIUpdateDestLosCache", "function JazzAI_VanillaUpdateDestLosCache"),
    ("function AICalcAttacksAndAim", "function JazzAI_VanillaCalcAttacksAndAim"),
    ("function AIBuildArchetypePaths", "function JazzAI_VanillaBuildArchetypePaths"),
    ("function AIScoreDest", "function JazzAI_VanillaScoreDest"),
    ("function AIEnumValidDests", "function JazzAI_VanillaEnumValidDests"),
    ("function AIFindOptimalLocation", "function JazzAI_VanillaFindOptimalLocation"),
    ("function AIGetWeaponCheckRange", "function JazzAI_VanillaGetWeaponCheckRange"),
    ("function AIPrecalcDamageScore", "function JazzAI_VanillaPrecalcDamageScore"),
]

# Longest names first so nested replacements stay unique.
CALLS = [
    ("JazzAI_VanillaGetAttackTargetingOptions", "AIGetAttackTargetingOptions"),
    ("JazzAI_VanillaFindOptimalLocation", "AIFindOptimalLocation"),
    ("JazzAI_VanillaEnumValidDests", "AIEnumValidDests"),
    ("JazzAI_VanillaPrecalcDamageScore", "AIPrecalcDamageScore"),
    ("JazzAI_VanillaBuildArchetypePaths", "AIBuildArchetypePaths"),
    ("JazzAI_VanillaExecuteUnitBehavior", "AIExecuteUnitBehavior"),
    ("JazzAI_VanillaGetWeaponCheckRange", "AIGetWeaponCheckRange"),
    ("JazzAI_VanillaUpdateDestLosCache", "AIUpdateDestLosCache"),
    ("JazzAI_VanillaCalcAttacksAndAim", "AICalcAttacksAndAim"),
    ("JazzAI_VanillaFindDestinations", "AIFindDestinations"),
    ("JazzAI_VanillaPlayAttacks", "AIPlayAttacks"),
    ("JazzAI_VanillaCreateContext", "AICreateContext"),
    ("JazzAI_VanillaTakeCover", "AITakeCover"),
    ("JazzAI_VanillaScoreDest", "AIScoreDest"),
]


def slice_lines(lines: list[str], start: int, end: int) -> str:
    return "".join(lines[start - 1 : end])


def remap_calls(body: str) -> str:
    for new, old in CALLS:
        body = body.replace(f"{old}(", f"{new}(")
        body = body.replace(f"{old} ", f"{new} ")
    return body


HEADER = r'''-- JAZZ-AI beasts: vanilla CombatAI copies.
-- Non-human units (Crocodile / Hyena / Hen) must not run JAZZ Dump, dest caps,
-- cover-disengage, or firearm Ensure. StandardAI:Think still calls these
-- globals; wrappers in CombatAI.lua / AiActions.lua dispatch here.

function JazzAI_UsesJazzCombatAI(unit)
	return IsValid(unit) and unit.species == "Human"
end

function JazzAI_ContextUsesJazzCombatAI(context)
	return JazzAI_UsesJazzCombatAI(context and context.unit)
end

function JazzAI_BeastPickNearestEnemy(unit, enemies)
	local best, best_d
	for _, enemy in ipairs(enemies or empty_table) do
		if IsValidTarget(enemy) and not (IsKindOf(enemy, "Unit") and enemy:IsIncapacitated()) then
			local d = unit:GetDist(enemy)
			local eh = enemy.handle or 0
			if not best or d < best_d or (d == best_d and eh < (best.handle or 0)) then
				best, best_d = enemy, d
			end
		end
	end
	return best
end

function JazzAI_BeastLockNearestEnemy(context)
	if type(context) ~= "table" or not IsValid(context.unit) then
		return false
	end
	local locked = JazzAI_BeastPickNearestEnemy(context.unit, context.enemies)
	context.target_locked = locked or false
	return locked
end

function JazzAI_BeastClosestDestToTarget(dests, target, fallback)
	if not target then
		return fallback
	end
	local tpos = GetPackedPosAndStance(target)
	if not tpos then
		return fallback
	end
	local best, best_d = fallback, fallback and stance_pos_dist(fallback, tpos) or nil
	for _, dest in ipairs(dests or empty_table) do
		if dest then
			local d = stance_pos_dist(dest, tpos)
			if not best_d or d < best_d then
				best, best_d = dest, d
			end
		end
	end
	return best
end

function JazzAI_BeastFindOptimalLocation(context)
	JazzAI_BeastLockNearestEnemy(context)
	local dest = JazzAI_BeastClosestDestToTarget(
		context.all_destinations,
		context.target_locked,
		context.unit_stance_pos
	)
	context.best_dest = dest
	return dest
end

function JazzAI_BeastScoreNearestEnemyDest(context)
	JazzAI_BeastLockNearestEnemy(context)
	local stay = context.unit_stance_pos
	if context.voxel_to_dest and context.unit_world_voxel then
		stay = context.voxel_to_dest[context.unit_world_voxel] or stay
	end
	local dest = JazzAI_BeastClosestDestToTarget(context.destinations, context.target_locked, stay)
	context.ai_destination = dest
	context.best_end_dest = dest
	return dest, 100
end

'''


def main() -> None:
    lines = SRC.read_text(encoding="utf-8").splitlines(keepends=True)
    chunks = [HEADER]
    for name, (start, end) in RANGES.items():
        body = slice_lines(lines, start, end)
        for old, new in RENAMES:
            body = body.replace(old, new, 1)
        body = remap_calls(body)
        # Vanilla CreateContext assumes default_attack exists.
        if name == "AICreateContext":
            body = body.replace(
                "context.default_attack_cost = default_attack:GetAPCost(unit)",
                "context.default_attack_cost = default_attack and default_attack:GetAPCost(unit) or 0",
            )
            body = body.replace(
                "default_attack.id)",
                "default_attack and default_attack.id)",
            )
            body = body.replace(
                "\tunit.ai_context = context\n\treturn context",
                "\tJazzAI_BeastLockNearestEnemy(context)\n\tunit.ai_context = context\n\treturn context",
            )
        if name == "AIPrecalcDamageScore":
            body = body.replace(
                "\tif #targets == 0 then\n\t\treturn\n\tend",
                "\tlocal locked = JazzAI_BeastLockNearestEnemy(context)\n"
                "\tif locked then\n"
                "\t\ttargets = { locked }\n"
                "\t\tpreferred_target = locked\n"
                "\tend\n"
                "\tif #targets == 0 then\n"
                "\t\treturn\n"
                "\tend",
            )
        if name == "AICalcAttacksAndAim":
            body = body.replace(
                "\tlocal \tcost = context.default_attack_cost\n"
                "\tlocal num_attacks = Min(ap / cost, context.max_attacks)",
                "\tlocal cost = context.default_attack_cost\n"
                "\tif not cost or cost <= 0 then\n"
                "\t\treturn 1, {}\n"
                "\tend\n"
                "\tlocal num_attacks = Min(ap / cost, context.max_attacks)",
            )
        chunks.append(body.rstrip() + "\n\n")
    OUT.write_text("".join(chunks), encoding="utf-8", newline="\n")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
