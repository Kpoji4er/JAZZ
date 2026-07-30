-- Shell eject: PlayFX("ShellEject", ..., ammo.class) — Target is ammo class, not caliber.
-- Ammo_Shells atlas is 4x4; DynamicPoint1 AmmoType selects the frame (vanilla mapping).
-- JAZZ calibers map to the closest vanilla shell size/frame.

local shell_frame_by_caliber = {
	-- row 1: shotgun
	JAZZ_Caliber_12gauge = point(2, 1), -- Buckshot frame
	JAZZ_Caliber_50BMG = point(1, 1), -- largest available (Breacher-sized)
	-- row 2: intermediate / magnum pistol
	JAZZ_Caliber_556 = point(1, 2),
	JAZZ_Caliber_545 = point(1, 2),
	JAZZ_Caliber_30CAL = point(1, 2),
	JAZZ_Caliber_57 = point(1, 2),
	JAZZ_Caliber_46 = point(1, 2),
	JAZZ_Caliber_44CAL = point(3, 2),
	JAZZ_Caliber_45ACP = point(3, 2),
	JAZZ_Caliber_357 = point(3, 2),
	JAZZ_Caliber_38 = point(3, 2),
	JAZZ_Caliber_50AE = point(3, 2),
	-- row 3: rifle / pistol
	JAZZ_Caliber_762x51 = point(1, 3),
	JAZZ_Caliber_762x39 = point(1, 3),
	JAZZ_Caliber_762x54R = point(1, 3),
	JAZZ_Caliber_3006 = point(1, 3),
	JAZZ_Caliber_792 = point(1, 3),
	JAZZ_Caliber_792x33 = point(1, 3),
	JAZZ_Caliber_75French = point(1, 3),
	JAZZ_Caliber_9x39 = point(1, 3),
	JAZZ_Caliber_9x19 = point(3, 3),
	JAZZ_Caliber_9x18 = point(3, 3),
	JAZZ_Caliber_762x25 = point(3, 3),
}

-- Match variants shift column +1 within the same row (vanilla pattern).
local function shell_frame_for(caliber, ammo_id)
	local frame = shell_frame_by_caliber[caliber]
	if not frame then
		return point(3, 3) -- fallback: 9mm Basic
	end
	if ammo_id:find("Match", 1, true) then
		return point(frame:x() + 1, frame:y())
	end
	return frame
end

-- { ammo_class, caliber }
local ammo_cartridge = {
	{ "JAZZ_AMMO_12gauge_APSlug", "JAZZ_Caliber_12gauge" },
	{ "JAZZ_AMMO_12gauge_Birdshot", "JAZZ_Caliber_12gauge" },
	{ "JAZZ_AMMO_12gauge_Buckshot", "JAZZ_Caliber_12gauge" },
	{ "JAZZ_AMMO_12gauge_Saltshot", "JAZZ_Caliber_12gauge" },
	{ "JAZZ_AMMO_12gauge_Slug", "JAZZ_Caliber_12gauge" },
	{ "JAZZ_AMMO_30_FMJ", "JAZZ_Caliber_30CAL" },
	{ "JAZZ_AMMO_30_P", "JAZZ_Caliber_30CAL" },
	{ "JAZZ_AMMO_30_Tracer", "JAZZ_Caliber_30CAL" },
	{ "JAZZ_AMMO_3006_AP", "JAZZ_Caliber_3006" },
	{ "JAZZ_AMMO_3006_FMJ", "JAZZ_Caliber_3006" },
	{ "JAZZ_AMMO_3006_Match", "JAZZ_Caliber_3006" },
	{ "JAZZ_AMMO_357_FMJ", "JAZZ_Caliber_357" },
	{ "JAZZ_AMMO_357_JHP", "JAZZ_Caliber_357" },
	{ "JAZZ_AMMO_38special_FMJ", "JAZZ_Caliber_38" },
	{ "JAZZ_AMMO_38special_JHP", "JAZZ_Caliber_38" },
	{ "JAZZ_AMMO_44CAL_FMJ", "JAZZ_Caliber_44CAL" },
	{ "JAZZ_AMMO_44CAL_JHP", "JAZZ_Caliber_44CAL" },
	{ "JAZZ_AMMO_44CAL_Match", "JAZZ_Caliber_44CAL" },
	{ "JAZZ_AMMO_45ACP_Crafted", "JAZZ_Caliber_45ACP" },
	{ "JAZZ_AMMO_45ACP_FMJ", "JAZZ_Caliber_45ACP" },
	{ "JAZZ_AMMO_45ACP_JHP", "JAZZ_Caliber_45ACP" },
	{ "JAZZ_AMMO_45ACP_P", "JAZZ_Caliber_45ACP" },
	{ "JAZZ_AMMO_45ACP_Poor", "JAZZ_Caliber_45ACP" },
	{ "JAZZ_AMMO_46_AP", "JAZZ_Caliber_46" },
	{ "JAZZ_AMMO_46_FMJ", "JAZZ_Caliber_46" },
	{ "JAZZ_AMMO_46_JHP", "JAZZ_Caliber_46" },
	{ "JAZZ_AMMO_50AE_FMJ", "JAZZ_Caliber_50AE" },
	{ "JAZZ_AMMO_50AE_JHP", "JAZZ_Caliber_50AE" },
	{ "JAZZ_AMMO_50BMG_API_HEI", "JAZZ_Caliber_50BMG" },
	{ "JAZZ_AMMO_50BMG_APIT", "JAZZ_Caliber_50BMG" },
	{ "JAZZ_AMMO_50BMG_Basic", "JAZZ_Caliber_50BMG" },
	{ "JAZZ_AMMO_545_AP", "JAZZ_Caliber_545" },
	{ "JAZZ_AMMO_545_Army", "JAZZ_Caliber_545" },
	{ "JAZZ_AMMO_545_Crafted", "JAZZ_Caliber_545" },
	{ "JAZZ_AMMO_545_EPR", "JAZZ_Caliber_545" },
	{ "JAZZ_AMMO_545_Poor", "JAZZ_Caliber_545" },
	{ "JAZZ_AMMO_545_Tracer", "JAZZ_Caliber_545" },
	{ "JAZZ_AMMO_556_AP", "JAZZ_Caliber_556" },
	{ "JAZZ_AMMO_556_Army", "JAZZ_Caliber_556" },
	{ "JAZZ_AMMO_556_Crafted", "JAZZ_Caliber_556" },
	{ "JAZZ_AMMO_556_EPR", "JAZZ_Caliber_556" },
	{ "JAZZ_AMMO_556_FMJ", "JAZZ_Caliber_556" },
	{ "JAZZ_AMMO_556_Match", "JAZZ_Caliber_556" },
	{ "JAZZ_AMMO_556_Poor", "JAZZ_Caliber_556" },
	{ "JAZZ_AMMO_556_Tracer", "JAZZ_Caliber_556" },
	{ "JAZZ_AMMO_57_AP", "JAZZ_Caliber_57" },
	{ "JAZZ_AMMO_57_JHP", "JAZZ_Caliber_57" },
	{ "JAZZ_AMMO_57_Subsonic", "JAZZ_Caliber_57" },
	{ "JAZZ_AMMO_75French_AP", "JAZZ_Caliber_75French" },
	{ "JAZZ_AMMO_75French_FMJ", "JAZZ_Caliber_75French" },
	{ "JAZZ_AMMO_762x25_AP", "JAZZ_Caliber_762x25" },
	{ "JAZZ_AMMO_762x25_FMJ", "JAZZ_Caliber_762x25" },
	{ "JAZZ_AMMO_762x25_JHP", "JAZZ_Caliber_762x25" },
	{ "JAZZ_AMMO_762x25_Poor", "JAZZ_Caliber_762x25" },
	{ "JAZZ_AMMO_762x39_APP", "JAZZ_Caliber_762x39" },
	{ "JAZZ_AMMO_762x39_Army", "JAZZ_Caliber_762x39" },
	{ "JAZZ_AMMO_762x39_Crafted", "JAZZ_Caliber_762x39" },
	{ "JAZZ_AMMO_762x39_FMJ", "JAZZ_Caliber_762x39" },
	{ "JAZZ_AMMO_762x39_JHP", "JAZZ_Caliber_762x39" },
	{ "JAZZ_AMMO_762x39_Poor", "JAZZ_Caliber_762x39" },
	{ "JAZZ_AMMO_762x39_Tracer", "JAZZ_Caliber_762x39" },
	{ "JAZZ_AMMO_762x39_US", "JAZZ_Caliber_762x39" },
	{ "JAZZ_AMMO_762x51_AP", "JAZZ_Caliber_762x51" },
	{ "JAZZ_AMMO_762x51_Army", "JAZZ_Caliber_762x51" },
	{ "JAZZ_AMMO_762x51_Crafted", "JAZZ_Caliber_762x51" },
	{ "JAZZ_AMMO_762x51_FMJ", "JAZZ_Caliber_762x51" },
	{ "JAZZ_AMMO_762x51_Match", "JAZZ_Caliber_762x51" },
	{ "JAZZ_AMMO_762x51_Poor", "JAZZ_Caliber_762x51" },
	{ "JAZZ_AMMO_762x51_Tracer", "JAZZ_Caliber_762x51" },
	{ "JAZZ_AMMO_762x54_APIT", "JAZZ_Caliber_762x54R" },
	{ "JAZZ_AMMO_762x54_Crafted", "JAZZ_Caliber_762x54R" },
	{ "JAZZ_AMMO_762x54_FMJ", "JAZZ_Caliber_762x54R" },
	{ "JAZZ_AMMO_762x54_Match", "JAZZ_Caliber_762x54R" },
	{ "JAZZ_AMMO_762x54_Poor", "JAZZ_Caliber_762x54R" },
	{ "JAZZ_AMMO_762x54_Tracer", "JAZZ_Caliber_762x54R" },
	{ "JAZZ_AMMO_792_AP", "JAZZ_Caliber_792" },
	{ "JAZZ_AMMO_792_APIT", "JAZZ_Caliber_792" },
	{ "JAZZ_AMMO_792_FMJ", "JAZZ_Caliber_792" },
	{ "JAZZ_AMMO_792x33_AP", "JAZZ_Caliber_792x33" },
	{ "JAZZ_AMMO_792x33_FMJ", "JAZZ_Caliber_792x33" },
	{ "JAZZ_AMMO_792x33_Tracer", "JAZZ_Caliber_792x33" },
	{ "JAZZ_AMMO_9x18_AP", "JAZZ_Caliber_9x18" },
	{ "JAZZ_AMMO_9x18_APP", "JAZZ_Caliber_9x18" },
	{ "JAZZ_AMMO_9x18_Crafted", "JAZZ_Caliber_9x18" },
	{ "JAZZ_AMMO_9x18_FMJ", "JAZZ_Caliber_9x18" },
	{ "JAZZ_AMMO_9x18_JHP", "JAZZ_Caliber_9x18" },
	{ "JAZZ_AMMO_9x18_Poor", "JAZZ_Caliber_9x18" },
	{ "JAZZ_AMMO_9x19_AP", "JAZZ_Caliber_9x19" },
	{ "JAZZ_AMMO_9x19_APP", "JAZZ_Caliber_9x19" },
	{ "JAZZ_AMMO_9x19_Crafted", "JAZZ_Caliber_9x19" },
	{ "JAZZ_AMMO_9x19_FMJ", "JAZZ_Caliber_9x19" },
	{ "JAZZ_AMMO_9x19_JHP", "JAZZ_Caliber_9x19" },
	{ "JAZZ_AMMO_9x19_JHP_copy", "JAZZ_Caliber_9x19" },
	{ "JAZZ_AMMO_9x19_Match", "JAZZ_Caliber_9x19" },
	{ "JAZZ_AMMO_9x19_Poor", "JAZZ_Caliber_9x19" },
	{ "JAZZ_AMMO_9x39_AP", "JAZZ_Caliber_9x39" },
	{ "JAZZ_AMMO_9x39_Crafted", "JAZZ_Caliber_9x39" },
	{ "JAZZ_AMMO_9x39_JHP", "JAZZ_Caliber_9x39" },
}

for _, row in ipairs(ammo_cartridge) do
	local ammo, caliber = row[1], row[2]
	PlaceObj('ActionFXParticles', {
		Action = "ShellEject",
		DynamicName1 = "AmmoType",
		DynamicPoint1 = shell_frame_for(caliber, ammo),
		FxId = "ammo_shell",
		GameTime = true,
		Moment = "start",
		Particles = "Ammo_Shells",
		Spot = "Barrel",
		Target = ammo,
		group = "Weapons Ammo Shells VFX",
		id = "JazzAmmoShell_" .. ammo,
	})
end
