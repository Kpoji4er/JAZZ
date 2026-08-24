# SUPERSEDED 2026-08-24. Do not run: would re-apply skill_mod on mishap (1–2 tile elite misses).
# Historical: 90/90 at max ≈ 80% of pre-tune scatter accuracy (skill floor 10% on both bands).
from pathlib import Path

path = Path(__file__).resolve().parents[2] / "Code" / "System_OR_Weapons.lua"
text = path.read_text(encoding="utf-8")

start = text.find("--- Deterministic Min/Max deviation bounds (no RNG). band = \"min\" | \"max\".")
end = text.find("function MishapProperties:GetMishapDeviationVector(", start)
if start < 0 or end < 0:
    raise SystemExit(f"anchors not found start={start} end={end}")

new = '''--- Deterministic Min/Max deviation bounds (no RNG). band = "min" | "max".
--- Magnitude: physical half ≈ old full-range scatter; full throw ≈ +25% vs that
--- (≈80% of pre-tune accuracy for blend 90 / skill_mod 10%). Skill floor stays 10%.
function MishapProperties:GetMishapDeviationBounds(unit, target, band)
	local blend = self:GetMishapSkillBlend(unit)
	local dist_eff = self:GetEffectiveMishapDist(unit, target)
	local dist_tiles = DivRound(dist_eff, const.SlabSizeX)
	local skill_mod_x100 = Clamp(100 - blend, 10, 100)

	local full_tiles = Max(DivRound(self:GetMishapFullRange(), const.SlabSizeX), 1)
	local half_tiles = Max(DivRound(full_tiles, 2), 1)
	local scatter_tiles
	if dist_tiles <= half_tiles then
		scatter_tiles = MulDivRound(dist_tiles, full_tiles, half_tiles)
	else
		-- half → full_tiles intensity; full → full_tiles * 125/100
		local over = dist_tiles - half_tiles
		local extra = MulDivRound(full_tiles, 25, 100)
		scatter_tiles = full_tiles + MulDivRound(over, extra, half_tiles)
	end

	local min_range, max_range, dist_mod_x100
	if band == "min" then
		min_range = 1 * const.SlabSizeX
		max_range = (self.MinMishapRange or 2) * const.SlabSizeX
		dist_mod_x100 = Clamp(MulDivRound(scatter_tiles, 100, 10), 40, 200)
	else
		min_range = (self.MinMishapRange or 1) * const.SlabSizeX
		max_range = (self.MaxMishapRange or 4) * const.SlabSizeX
		dist_mod_x100 = Clamp(MulDivRound(scatter_tiles, 100, 8), 100, 400)
	end

	local min_dev = MulDivRound(MulDivRound(min_range, dist_mod_x100, 100), skill_mod_x100, 100)
	local max_dev = MulDivRound(MulDivRound(max_range, dist_mod_x100, 100), skill_mod_x100, 100)
	if max_dev < min_dev then
		max_dev = min_dev
	end

	local cap = self:GetMishapCapTiles() * const.SlabSizeX
	min_dev = Min(min_dev, cap)
	max_dev = Min(max_dev, cap)
	if max_dev < min_dev then
		max_dev = min_dev
	end
	return min_dev, max_dev
end

'''

path.write_text(text[:start] + new + text[end:], encoding="utf-8")
print("patched GetMishapDeviationBounds")
