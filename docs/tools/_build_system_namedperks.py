# -*- coding: utf-8 -*-
"""Build one Code/System_NamedPerks.lua from restored hub+section sources (no BatchN files)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CODE = ROOT / "Code"
OUT = CODE / "System_NamedPerks.lua"
OLD = CODE / "System_NamedPerks_006.lua"
META = ROOT / "metadata.lua"
ITEMS = ROOT / "items.lua"

SECTIONS = [
    ("_np_hub.lua", None),
    ("_np_b3.lua", "signatures"),
    ("_np_b4.lua", "economy"),
    ("_np_b5.lua", "satellite"),
    ("_np_b6.lua", "section_d"),
]

HELPER = '''
--- Read a Named Perk Parameter from unit effect or CharacterEffectDefs (ModItem-tunable).
function Jazz_NamedPerkParam(unit, perk_id, key, default)
\tlocal effect
\tif unit and unit.GetStatusEffect then
\t\teffect = unit:GetStatusEffect(perk_id)
\tend
\tif (not effect or not effect.ResolveValue) and CharacterEffectDefs then
\t\teffect = CharacterEffectDefs[perk_id]
\tend
\tif effect and effect.ResolveValue then
\t\tlocal v = effect:ResolveValue(key)
\t\tif v ~= nil then
\t\t\treturn v
\t\tend
\tend
\treturn default
end

'''

# String renames applied to whole assembled text (BatchN -> semantic).
RENAMES = [
    ("g_JAZZ_NamedPerks006Batch2Wrapped", "g_JAZZ_NamedPerks006OpsWrapped"),
    ("g_JAZZ_NamedPerks006Batch3Wrapped", "g_JAZZ_NamedPerks006SignaturesWrapped"),
    ("g_JAZZ_NamedPerks006Batch4Wrapped", "g_JAZZ_NamedPerks006EconomyWrapped"),
    ("g_JAZZ_NamedPerks006Batch5Wrapped", "g_JAZZ_NamedPerks006SatelliteWrapped"),
    ("g_JAZZ_NamedPerks006Batch6Wrapped", "g_JAZZ_NamedPerks006SectionDWrapped"),
    ("function Jazz_InstallNamedPerks006Batch3", "local function lInstallNamedPerks006Signatures"),
    ("function Jazz_InstallNamedPerks006Batch4", "local function lInstallNamedPerks006Economy"),
    ("function Jazz_InstallNamedPerks006Batch5", "local function lInstallNamedPerks006Satellite"),
    ("function Jazz_InstallNamedPerks006Batch6", "local function lInstallNamedPerks006SectionD"),
    ("local function lInstallNamedPerks006Batch2", "local function lInstallNamedPerks006Ops"),
    ("Jazz_InstallNamedPerks006Batch3()", "lInstallNamedPerks006Signatures()"),
    ("Jazz_InstallNamedPerks006Batch4()", "lInstallNamedPerks006Economy()"),
    ("Jazz_InstallNamedPerks006Batch5()", "lInstallNamedPerks006Satellite()"),
    ("Jazz_InstallNamedPerks006Batch6()", "lInstallNamedPerks006SectionD()"),
    ("lInstallNamedPerks006Batch2()", "lInstallNamedPerks006Ops()"),
    ("function Jazz_NamedPerks006Batch3OnCombatStart", "local function lNamedPerks006OnCombatStart_Signatures"),
    ("function Jazz_NamedPerks006Batch4OnCombatStart", "local function lNamedPerks006OnCombatStart_Economy"),
    ("function Jazz_NamedPerks006Batch5OnCombatStart", "local function lNamedPerks006OnCombatStart_Satellite"),
    ("function Jazz_NamedPerks006Batch6OnCombatStart", "local function lNamedPerks006OnCombatStart_SectionD"),
    ("function Jazz_NamedPerks006Batch3OnTurnStart", "local function lNamedPerks006OnTurnStart_Signatures"),
    ("function Jazz_NamedPerks006Batch4OnTurnStart", "local function lNamedPerks006OnTurnStart_Economy"),
    ("function Jazz_NamedPerks006Batch5OnTurnStart", "local function lNamedPerks006OnTurnStart_Satellite"),
]


PARAM_WIRES = [
    (
        'return InteractionRand(100, "Jazz_Perk_Vince") < 25',
        'return InteractionRand(100, "Jazz_Perk_Vince") < Jazz_NamedPerkParam(healer, "Jazz_Perk_Vince", "med_skip_chance", 25)',
    ),
    (
        "return Max(1, MulDivRound(amount, 75, 100))",
        'return Max(1, MulDivRound(amount, Jazz_NamedPerkParam(healer, "Jazz_Perk_Vince", "med_amount_mul", 75), 100))',
    ),
    (
        'return Clamp(tonumber(unit:GetEffectValue("Jazz_NervousBonusShots")) or 0, 0, 10)',
        'return Clamp(tonumber(unit:GetEffectValue("Jazz_NervousBonusShots")) or 0, 0, Jazz_NamedPerkParam(unit, "Jazz_Perk_Nervous", "stack_cap", 10))',
    ),
    (
        'unit:SetEffectValue("Jazz_NervousBonusShots", Clamp(cur + hits, 0, 10))',
        'unit:SetEffectValue("Jazz_NervousBonusShots", Clamp(cur + hits, 0, Jazz_NamedPerkParam(unit, "Jazz_Perk_Nervous", "stack_cap", 10)))',
    ),
    (
        "u.WillPoints = Max(0, wp - 10)",
        'u.WillPoints = Max(0, wp - Jazz_NamedPerkParam(center_unit, "Jazz_Perk_Madman", "will_drain", 10))',
    ),
    (
        "if DivRound(center_unit:GetDist(u), slab) <= 5 then",
        'if DivRound(center_unit:GetDist(u), slab) <= Jazz_NamedPerkParam(center_unit, "Jazz_Perk_Madman", "radius", 5) then',
    ),
    (
        "return Clamp((tonumber(lvl) or 1) * 5, 0, 25)",
        'return Clamp((tonumber(lvl) or 1) * Jazz_NamedPerkParam(unit, "Jazz_Perk_Static", "parts_per_level", 5), 0, Jazz_NamedPerkParam(unit, "Jazz_Perk_Static", "parts_cap", 25))',
    ),
    (
        "cost = MulDivRound(cost, 88, 100)",
        'local disc = Jazz_NamedPerkParam(nil, "Jazz_Perk_Flo", "buy_discount", 12)\n\t\t\t\tcost = MulDivRound(cost, 100 - disc, 100)',
    ),
    (
        "item.Cost = MulDivRound(old, 112, 100)",
        'local bonus = Jazz_NamedPerkParam(nil, "Jazz_Perk_Flo", "sell_bonus", 12)\n\t\t\t\titem.Cost = MulDivRound(old, 100 + bonus, 100)',
    ),
    (
        "radius = MulDivRound(radius, 67, 100)",
        'radius = MulDivRound(radius, Jazz_NamedPerkParam(attacker, "Jazz_Perk_Cougar", "noise_mul", 67), 100)',
    ),
    (
        "return 10 + MulDivRound(Max(0, 100 - loyalty), 30, 100)",
        'local base = Jazz_NamedPerkParam(nil, "Jazz_Perk_Rothman", "mine_bonus_base", 10)\n\tlocal span = Jazz_NamedPerkParam(nil, "Jazz_Perk_Rothman", "mine_bonus_loyalty_span", 30)\n\treturn base + MulDivRound(Max(0, 100 - loyalty), span, 100)',
    ),
    (
        "if DivRound(miguel:GetDist(u), slab) <= 30 then",
        'if DivRound(miguel:GetDist(u), slab) <= Jazz_NamedPerkParam(miguel, "Jazz_Perk_Miguel", "aura_radius", 30) then',
    ),
    (
        "return Max(ldr, 90)",
        'return Max(ldr, Jazz_NamedPerkParam(merc, "Jazz_Perk_Conrad", "leadership_floor", 90))',
    ),
    (
        "parts = Max(0, MulDivRound(parts, 90, 100))",
        'local disc = Jazz_NamedPerkParam(merc, "Jazz_Perk_Cord", "repair_parts_discount", 10)\n\t\t\t\t\t\tparts = Max(0, MulDivRound(parts, 100 - disc, 100))',
    ),
    (
        "t = MulDivRound(t, 85, 100)",
        'local td = Jazz_NamedPerkParam(merc, "Jazz_Perk_Cord", "repair_time_discount", 15)\n\t\t\t\tt = MulDivRound(t, 100 - td, 100)',
    ),
    (
        "if ldr < 90 and ldr > 0 then",
        'local floor = Jazz_NamedPerkParam(merc, "Jazz_Perk_Conrad", "leadership_floor", 90)\n\t\t\t\tif ldr < floor and ldr > 0 then',
    ),
    (
        "t = MulDivRound(t, ldr, 90)",
        "t = MulDivRound(t, ldr, floor)",
    ),
    (
        'if InteractionRand(100, "Jazz_Perk_Carlos") < 50 then',
        'if InteractionRand(100, "Jazz_Perk_Carlos") < Jazz_NamedPerkParam(self, "Jazz_Perk_Carlos", "keep_hidden_chance", 50) then',
    ),
    (
        "if DivRound(unit:GetDist(enemy), slab) <= 8 then",
        'if DivRound(unit:GetDist(enemy), slab) <= Jazz_NamedPerkParam(unit, "Jazz_Perk_Benny", "lure_range", 8) then',
    ),
    (
        "unit[stat] = Clamp(cur + 20, 0, 100)",
        'unit[stat] = Clamp(cur + Jazz_NamedPerkParam(nil, "Jazz_Perk_Ira", "primary_bonus", 20), 0, 100)',
    ),
    (
        "profile.effective_recoil = (profile.effective_recoil or 0) * 0.5",
        'local mul = Jazz_NamedPerkParam(attacker, "Jazz_Perk_Kulba", "recoil_mul", 50)\n\t\t\t\tprofile.effective_recoil = (profile.effective_recoil or 0) * mul / 100',
    ),
    (
        "profile.perk_factor = (profile.perk_factor or 1) * 0.5",
        "profile.perk_factor = (profile.perk_factor or 1) * mul / 100",
    ),
]


IRA_HOOK = r'''
function Jazz_SectorHasIraTrainer(sector)
	local sector_id = type(sector) == "table" and (sector.Id or sector.id) or sector
	if not sector_id then
		return false
	end
	local mercs = GetOperationProfessionals and GetOperationProfessionals(sector_id, "MilitiaTraining") or empty_table
	if not next(mercs) then
		mercs = GetOperationProfessionals and GetOperationProfessionals(sector_id, "TrainMilitia") or empty_table
	end
	for _, merc in ipairs(mercs) do
		if merc and HasPerk(merc, "Jazz_Perk_Ira") and not (merc.IsDead and merc:IsDead()) then
			return true
		end
	end
	for _, squad in pairs(gv_Squads or empty_table) do
		if squad and (squad.Side == "player1" or squad.Side == "player2") and squad.CurrentSector == sector_id then
			for _, uid in ipairs(squad.units or empty_table) do
				local u = gv_UnitData and gv_UnitData[uid]
				if u and HasPerk(u, "Jazz_Perk_Ira") and not (u.IsDead and u:IsDead()) then
					return true
				end
			end
		end
	end
	return false
end

function Jazz_IraBoostMilitiaInSector(sector)
	if not Jazz_SectorHasIraTrainer(sector) then
		return
	end
	local sector_id = type(sector) == "table" and (sector.Id or sector.id) or sector
	local sector_obj = (type(sector) == "table" and sector) or (gv_Sectors and gv_Sectors[sector_id])
	local squad_id = sector_obj and sector_obj.militia_squad_id
	local squad = squad_id and gv_Squads and gv_Squads[squad_id]
	if not squad then
		return
	end
	for _, uid in ipairs(squad.units or empty_table) do
		local u = gv_UnitData and gv_UnitData[uid]
		if u and not u.Jazz_IraTrainedBonus then
			local ok = Jazz_IraApplyMilitiaTrainBonus(u)
			if ok then
				u.Jazz_IraTrainedBonus = true
			end
		end
	end
end

function Jazz_InstallIraMilitiaTrainHook()
	if rawget(_G, "g_JAZZ_IraMilitiaHook") or not SectorOperations then
		return
	end
	local op = SectorOperations.MilitiaTraining or SectorOperations.TrainMilitia
	if not op then
		return
	end
	rawset(_G, "g_JAZZ_IraMilitiaHook", true)
	local base_complete = op.Complete or op.OnComplete
	if type(base_complete) ~= "function" then
		return
	end
	local key = op.Complete and "Complete" or "OnComplete"
	local prev = op[key]
	op[key] = function(self, sector, ...)
		local ret = prev(self, sector, ...)
		if type(Jazz_IraBoostMilitiaInSector) == "function" then
			Jazz_IraBoostMilitiaInSector(sector)
		end
		return ret
	end
end
'''


def strip_section_header(text: str) -> str:
    lines = text.splitlines(True)
    while lines and lines[0].startswith("--"):
        lines.pop(0)
    while lines and lines[0].strip() == "":
        lines.pop(0)
    # drop "Install from System_NamedPerks..." lines
    out = []
    for line in lines:
        if "Install from System_NamedPerks" in line or "do not overwrite OnMsg" in line:
            continue
        out.append(line)
    return "".join(out)


def main() -> None:
    hub = (CODE / "_np_hub.lua").read_text(encoding="utf-8")
    # Drop hub's old install-all / OnMsg tail
    marker = "local function lInstallAllNamedPerks006()"
    idx = hub.find(marker)
    if idx < 0:
        raise SystemExit("hub install-all missing")
    hub_head = hub[:idx].rstrip() + "\n\n"
    # drop old header
    hub_head = re.sub(r"^--.*\n(--.*\n)*\n*", "", hub_head, count=1)

    parts = [HELPER, hub_head]
    for fname, _kind in SECTIONS[1:]:
        parts.append("\n" + strip_section_header((CODE / fname).read_text(encoding="utf-8")).rstrip() + "\n")

    body = "".join(parts)
    for a, b in RENAMES:
        if a not in body:
            print("warn missing rename", a)
        body = body.replace(a, b)

    for old, new in PARAM_WIRES:
        if old in body:
            body = body.replace(old, new, 1)
            print("wired", old[:40])
        else:
            print("warn wire miss", old[:40])

    # Barry
    body = re.sub(
        r"function Jazz_BarryCraftDiscountPercent\(unit\)\n"
        r"\tif unit and HasPerk\(unit, \"DesignerExplosives\"\) then\n"
        r"\t\treturn 30\n"
        r"\tend\n"
        r"\treturn 0\n"
        r"end",
        "function Jazz_BarryCraftDiscountPercent(unit)\n"
        "\tif unit and HasPerk(unit, \"DesignerExplosives\") then\n"
        "\t\treturn Jazz_NamedPerkParam(unit, \"DesignerExplosives\", \"craft_discount\", 30)\n"
        "\tend\n"
        "\treturn 0\n"
        "end",
        body,
        count=1,
    )

    # DangerClose bleed/minRange soft
    body = body.replace(
        """\tif CharacterEffectDefs and CharacterEffectDefs.Bleeding and target.AddStatusEffect then
\t\ttarget:AddStatusEffect("Bleeding")
\t\ttarget:AddStatusEffect("Bleeding")
\tend""",
        """\tlocal stacks = Jazz_NamedPerkParam(attacker, "DangerClose", "bleed_stacks", 2)
\tif CharacterEffectDefs and CharacterEffectDefs.Bleeding and target.AddStatusEffect then
\t\tfor _ = 1, stacks do
\t\t\ttarget:AddStatusEffect("Bleeding")
\t\tend
\tend""",
    )
    body = body.replace(
        "if dist < 8 then",
        'if dist < Jazz_NamedPerkParam(attacker, "DangerClose", "minRange", 8) then',
    )

    # Ira hook: inject before satellite install end if missing
    if "Jazz_InstallIraMilitiaTrainHook" not in body:
        # append helpers before SectionD wrap flag area — insert after Jazz_IraApplyMilitiaTrainBonus function
        needle = "function Jazz_IraApplyMilitiaTrainBonus(unit)"
        pos = body.find(needle)
        if pos < 0:
            raise SystemExit("Ira helper missing")
        # find end of that function
        m = re.search(
            r"function Jazz_IraApplyMilitiaTrainBonus\(unit\).*?\nend\n",
            body,
            re.S,
        )
        if not m:
            raise SystemExit("Ira helper end missing")
        body = body[: m.end()] + "\n" + IRA_HOOK + body[m.end() :]
        # call from satellite install
        body = body.replace(
            'rawset(_G, "g_JAZZ_NamedPerks006SatelliteWrapped", true)\nend',
            'Jazz_InstallIraMilitiaTrainHook()\n\trawset(_G, "g_JAZZ_NamedPerks006SatelliteWrapped", true)\nend',
            1,
        )
        # also retry hook when already wrapped
        body = body.replace(
            "local function lInstallNamedPerks006Satellite()\n\tif rawget(_G, \"g_JAZZ_NamedPerks006SatelliteWrapped\") then\n\t\treturn\n\tend",
            "local function lInstallNamedPerks006Satellite()\n\tif rawget(_G, \"g_JAZZ_NamedPerks006SatelliteWrapped\") then\n\t\tJazz_InstallIraMilitiaTrainHook()\n\t\treturn\n\tend",
            1,
        )
        print("ira hook added")

    tail = """
local function lInstallAllNamedPerks006()
\tlInstallNamedPerks006()
\tlInstallNamedPerks006Ops()
\tlInstallNamedPerks006Signatures()
\tlInstallNamedPerks006Economy()
\tlInstallNamedPerks006Satellite()
\tlInstallNamedPerks006SectionD()
end

function Jazz_NamedPerks006OnCombatStart()
\tlNamedPerks006OnCombatStart_Signatures()
\tlNamedPerks006OnCombatStart_Economy()
\tlNamedPerks006OnCombatStart_Satellite()
\tlNamedPerks006OnCombatStart_SectionD()
end

function Jazz_NamedPerks006OnTurnStart()
\tlNamedPerks006OnTurnStart_Signatures()
\tlNamedPerks006OnTurnStart_Economy()
\tlNamedPerks006OnTurnStart_Satellite()
end

OnMsg.ModsReloaded = function()
\tlInstallAllNamedPerks006()
end
OnMsg.DataLoaded = function()
\tlInstallAllNamedPerks006()
end
OnMsg.NewGame = function()
\tlInstallAllNamedPerks006()
end
OnMsg.LoadGame = function()
\tlInstallAllNamedPerks006()
end

OnMsg.CombatStart = function()
\tJazz_NamedPerks006OnCombatStart()
end
OnMsg.TurnStart = function()
\tJazz_NamedPerks006OnTurnStart()
end
"""

    header = (
        "-- JAZZ named personal perks runtime (spec UNITS-006).\n"
        "-- Single Code module + ModItem CharacterEffect Parameters/reactions.\n"
        "-- Loc note: VR 6300-6499 reserved; perk text often 6500+ / 9885+.\n\n"
    )
    text = header + body.rstrip() + "\n" + tail
    # scrub leftover Batch banners
    text = re.sub(r"(?m)^-- .*Batch[0-9].*\n", "", text)
    text = re.sub(r"(?m)^-- JAZZ-UNITS-006 §.*\n", "", text)

    OUT.write_text(text, encoding="utf-8", newline="\n")
    print("wrote", OUT, "bytes", OUT.stat().st_size)
    if "Batch3" in text or "Batch4" in text or "_Batch" in text:
        print("WARN still contains Batch index tokens")

    # Retire old path
    if OLD.exists():
        OLD.unlink()
        print("deleted", OLD.name)

    # metadata.code
    meta = META.read_text(encoding="utf-8")
    meta = meta.replace('"Code/System_NamedPerks_006.lua"', '"Code/System_NamedPerks.lua"')
    for b in ("Batch3", "Batch4", "Batch5", "Batch6"):
        meta = meta.replace(f'\t\t"Code/System_NamedPerks_006_{b}.lua",\n', "")
    META.write_text(meta, encoding="utf-8", newline="\n")
    print("metadata updated")

    # ModItemCode name/path
    items = ITEMS.read_text(encoding="utf-8")
    items2 = items.replace(
        "'name', \"System_NamedPerks_006\"",
        "'name', \"System_NamedPerks\"",
    ).replace(
        "'CodeFileName', \"Code/System_NamedPerks_006.lua\"",
        "'CodeFileName', \"Code/System_NamedPerks.lua\"",
    )
    if items2 != items:
        tmp = ITEMS.with_suffix(".lua.tmp_np")
        tmp.write_text(items2, encoding="utf-8", newline="\n")
        tmp.replace(ITEMS)
        print("items ModItemCode updated")

    # cleanup temp sources
    for fname, _ in SECTIONS:
        p = CODE / fname
        if p.exists():
            p.unlink()
    print("cleaned _np_* temps")


if __name__ == "__main__":
    main()
