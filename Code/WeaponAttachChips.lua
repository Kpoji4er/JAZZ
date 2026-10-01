-- JAZZ-UI-001: overlay chips disabled; weapon artwork now shows components.
-- Prefer WeaponComponent.ChipIcon (miniature); else convention Chips/<id>.png; else slot fallback.
-- Legacy lookup helpers and resources remain available; Apply only clears overlays.

JazzAttachChips_Max = 4
JazzAttachChips_Size = 24
JazzAttachChips_PerCol = 3
JazzAttachChips_Margin = box(-4, 0, 0, 0)

local SlotIconFamily = {
	Scope = "slot_scope",
	Sightsr = "slot_sights",
	Sight = "slot_sights",
	Muzzle = "slot_muzzle",
	Barrel = "slot_barrel",
	Magazine = "slot_magazine",
	Stock = "slot_stock",
	Under = "slot_under",
	Side = "slot_side",
	Side1 = "slot_side",
	Side2 = "slot_side",
	Side3 = "slot_side",
	Bipod = "slot_bipod",
	Handgrip = "slot_handgrip",
	Handguard = "slot_handguard",
	Mount = "slot_mount",
	Mount1 = "slot_mount",
	Mount2 = "slot_mount",
	Mountside = "slot_mount",
	Mountfront = "slot_mount",
	General = "slot_general",
}

-- Display order (top → bottom). Side/Under early so lasers/lights aren't clipped by Max.
local SlotDisplayPriority = {
	Scope = 10,
	Sightsr = 20,
	Sight = 20,
	Side = 30,
	Side1 = 31,
	Side2 = 32,
	Side3 = 33,
	Under = 40,
	Muzzle = 50,
	Barrel = 60,
	Magazine = 70,
	Stock = 80,
	Handgrip = 90,
	Handguard = 100,
	Bipod = 110,
	General = 120,
}

function JazzAttachChips_SlotIcon(slotType)
	local family = SlotIconFamily[slotType or ""] or "slot_general"
	return string.format("Mod/e6L4ECj/Icons/Upgrades/%s.png", family)
end

function JazzAttachChips_ChipPath(componentId)
	if not componentId or componentId == "" then
		return false
	end
	return string.format("Mod/e6L4ECj/Icons/Upgrades/Chips/%s.png", componentId)
end

local function ComponentPreset(id)
	if not id or id == "" then
		return false
	end
	if WeaponComponents and WeaponComponents[id] then
		return WeaponComponents[id]
	end
	if g_Classes and g_Classes[id] then
		return g_Classes[id]
	end
	return false
end

local function ResolveChipImage(preset, componentId, slotType)
	-- 1) Explicit ChipIcon on preset (wired in items.lua).
	if preset then
		local chip = preset.ChipIcon
		if chip and chip ~= "" and chip ~= 0 then
			return chip
		end
	end
	-- 2) Convention path — always prefer over cabinet Icon when ChipIcon unset.
	--    XImage resolves Mod/... even when io.exists cannot see the virtual path.
	--    Never use WeaponComponent.Icon as chip (Optics/PSO.png etc. look photographic at 20px).
	if componentId and componentId ~= "" then
		return JazzAttachChips_ChipPath(componentId)
	end
	-- 3) Slot family glyph.
	return JazzAttachChips_SlotIcon(slotType)
end

local function ComponentSlotsOf(weapon)
	local slots = weapon and weapon.ComponentSlots
	if (not slots or #slots == 0) and g_Classes and weapon and weapon.class and g_Classes[weapon.class] then
		slots = g_Classes[weapon.class].ComponentSlots
	end
	return slots
end

function JazzAttachChips_IsFirearm(item)
	return item and IsKindOf(item, "FirearmBase")
end

function JazzAttachChips_IsSkippedSlot(slotType)
	slotType = slotType or ""
	-- Mount rails/adapters are not shown as inventory chips (owner: mounts not needed).
	if slotType == "Mount" or slotType == "Mount1" or slotType == "Mount2"
		or slotType == "Mountside" or slotType == "Mountfront" then
		return true
	end
	return false
end

local function HasModificationEffects(preset)
	local effects = preset and preset.ModificationEffects
	return effects and #effects > 0
end

-- Match CountWeaponUpgrades intent: removable default accessories (e.g. MP5A4 Side=Flashlight)
-- still count as upgrades when they have ModificationEffects / CanBeEmpty.
function JazzAttachChips_ShouldShow(slot, componentId)
	if not componentId or componentId == "" then
		return false
	end
	local def = slot.DefaultComponent or ""
	if componentId ~= def then
		return true
	end
	if slot.CanBeEmpty then
		local preset = ComponentPreset(componentId)
		if HasModificationEffects(preset) then
			return true
		end
	end
	return false
end

function JazzAttachChips_List(weapon)
	local chips = {}
	if not JazzAttachChips_IsFirearm(weapon) then
		return chips
	end
	local slots = ComponentSlotsOf(weapon)
	if not slots or #slots == 0 then
		return chips
	end
	local components = weapon.components or empty_table
	local pending = {}
	for _, slot in ipairs(slots) do
		local slotType = slot.SlotType or slot.Slot or ""
		if not JazzAttachChips_IsSkippedSlot(slotType) then
			local cur = components[slotType] or ""
			if JazzAttachChips_ShouldShow(slot, cur) then
				local preset = ComponentPreset(cur)
				pending[#pending + 1] = {
					id = cur,
					slot = slotType,
					icon = ResolveChipImage(preset, cur, slotType),
					name = preset and preset.DisplayName,
					prio = SlotDisplayPriority[slotType] or 200,
				}
			end
		end
	end
	table.sort(pending, function(a, b)
		if a.prio ~= b.prio then
			return a.prio < b.prio
		end
		return (a.slot or "") < (b.slot or "")
	end)
	local max = JazzAttachChips_Max or 4
	for i = 1, Min(#pending, max) do
		chips[i] = pending[i]
	end
	return chips
end

local function FindModBadge(img)
	if not img then
		return false
	end
	return rawget(img, "idItemModImg")
		or rawget(img, "idModIcon")
		or (img.ResolveId and (img:ResolveId("idItemModImg") or img:ResolveId("idModIcon")))
end

local function ClearChipRow(row)
	if not row then
		return
	end
	if row.DeleteChildren then
		row:DeleteChildren()
		return
	end
	if row.Clear then
		row:Clear()
		return
	end
	for i = #(row or empty_table), 1, -1 do
		local child = row[i]
		if child and child.Close then
			child:Close()
		elseif IsValid and IsValid(child) and DoneObject then
			DoneObject(child)
		end
	end
end

-- Keep the entry point used by HUD/inventory refreshes. Clear legacy overlays
-- after a reload without recreating them or touching native weapon layers.
function JazzAttachChips_Apply(hostImg, item)
	if not hostImg then
		return false
	end
	local row = rawget(hostImg, "idJazzAttachChips")
		or (hostImg.ResolveId and hostImg:ResolveId("idJazzAttachChips"))
	if row then
		ClearChipRow(row)
		row:SetFoldWhenHidden(true)
		row:SetVisible(false)
	end
	local badge = FindModBadge(hostImg)
	if badge then
		badge:SetVisible(not JazzAttachChips_IsFirearm(item))
	end
	return false
end
