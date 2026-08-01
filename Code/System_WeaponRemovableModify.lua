-- JAZZ-WEAPONS-002: removable attachments via ModifyWeaponDlg + inventory DnD.
-- Removable slots consume/return JAZZ_RemovableAttachment InventoryItems (no Parts craft).

if FirstLoad then
	JazzIsRemovableInstallTarget = false
	JazzIsRemovableRemoveTarget = false
	JazzMoveItem_BeforeRemovable = false
	JazzCanDropAt_Vanilla = false
	JazzEquipIsDropTarget_Vanilla = false
	JAZZ_IsHiddenModifyWeaponCraftOption = false
	JAZZ_FilterModifyWeaponCraftOptions = false
end

function JazzIsRemovableInstallTarget(attachment, weapon)
	if not IsKindOf(attachment, "JAZZ_RemovableAttachment") or not IsKindOf(weapon, "FirearmBase") then
		return false
	end
	local component_id = attachment.RemovableComponentId
	if type(component_id) ~= "string" or component_id == "" then
		return false
	end
	return not not (weapon.JAZZ_FindSlotForRemovableComponent and weapon:JAZZ_FindSlotForRemovableComponent(component_id))
end

local function JazzRemovableComponentIdsMatch(a, b)
	if not a or not b then
		return false
	end
	if a == b then
		return true
	end
	return a == "JAZZ_" .. b or b == "JAZZ_" .. a
end

function JazzIsRemovableRemoveTarget(weapon, attachment)
	if not IsKindOf(weapon, "FirearmBase") or not IsKindOf(attachment, "JAZZ_RemovableAttachment") then
		return false
	end
	local want = attachment.RemovableComponentId
	if type(want) ~= "string" or want == "" then
		return false
	end
	for s, cid in sorted_pairs(weapon.components or empty_table) do
		if JazzRemovableComponentIdsMatch(cid, want) and JAZZ_IsRemovableWeaponComponent(cid, s) then
			return true
		end
	end
	return false
end

local function JazzResolveMoveItemAtDest(args)
	if type(args) ~= "table" or not args.dest_container or type(args.dest_container) ~= "table" then
		return
	end
	local dest = args.dest_container
	local dest_slot = args.dest_container_slot_name or args.dest_slot
	local dx, dy = args.dest_x or args.x, args.dest_y or args.y
	if not dest_slot or not dx or not dest.GetItemInSlot then
		return
	end
	local item = dest:GetItemInSlot(dest_slot, nil, dx, dy)
	-- Large firearms: cursor on the second tile still resolves the weapon.
	if not item and dy then
		item = dest:GetItemInSlot(dest_slot, nil, dx - 1, dy)
	end
	return item
end

local function JazzTryDnDInstallRemovable(args)
	local attachment = args.item
	if not IsKindOf(attachment, "JAZZ_RemovableAttachment") then
		return
	end
	local weapon = JazzResolveMoveItemAtDest(args)
	if not JazzIsRemovableInstallTarget(attachment, weapon) then
		return
	end
	local component_id = attachment.RemovableComponentId
	local slot = weapon:JAZZ_FindSlotForRemovableComponent(component_id)
	if not slot then
		return "incompatible"
	end
	if args.check_only then
		return true
	end
	local unit = IsKindOfClasses(args.dest_container, "Unit", "UnitData") and args.dest_container
		or IsKindOfClasses(args.src_container, "Unit", "UnitData") and args.src_container
	local src = args.src_container
	local ok, result = weapon:JAZZ_InstallRemovableAttachment(unit, slot, attachment, src)
	if not ok then
		return result or "failed"
	end
	ObjModified(weapon)
	ObjModified(unit)
	ObjModified("inventory tabs")
	return true
end

-- DnD remove: drop firearm onto a JAZZ_RemovableAttachment whose RemovableComponentId
-- matches an installed removable → uninstall that slot into the squad bag.
local function JazzTryDnDRemoveRemovable(args)
	local weapon = args.item
	local dest_item = JazzResolveMoveItemAtDest(args)
	if not JazzIsRemovableRemoveTarget(weapon, dest_item) then
		return
	end
	local want = dest_item.RemovableComponentId
	local slot
	for s, cid in sorted_pairs(weapon.components or empty_table) do
		if JazzRemovableComponentIdsMatch(cid, want) and JAZZ_IsRemovableWeaponComponent(cid, s) then
			slot = s
			break
		end
	end
	if not slot then
		return "not-installed"
	end
	if args.check_only then
		return true
	end
	local unit = IsKindOfClasses(args.src_container, "Unit", "UnitData") and args.src_container
		or IsKindOfClasses(args.dest_container, "Unit", "UnitData") and args.dest_container
	local bag = (unit and unit.Squad and GetSquadBagInventory(unit.Squad)) or args.dest_container
	local ok, result = weapon:JAZZ_RemoveRemovableAttachment(unit, slot, bag)
	if not ok then
		return result or "failed"
	end
	ObjModified(weapon)
	ObjModified(unit)
	ObjModified("inventory tabs")
	-- Keep dest marker item (it identified which module to strip); uninstall already spawned a copy.
	return true
end

-- Keep originals across Lua reload (local capture would wrap our own wrappers).
if not JazzMoveItem_BeforeRemovable then
	rawset(_G, "JazzMoveItem_BeforeRemovable", MoveItem)
end
function MoveItem(args)
	if type(args) == "table" and args.item then
		local install = JazzTryDnDInstallRemovable(args)
		if install == true then
			return false
		elseif install then
			return install
		end
		local remove = JazzTryDnDRemoveRemovable(args)
		if remove == true then
			return false
		elseif remove then
			return remove
		end
	end
	return JazzMoveItem_BeforeRemovable(args)
end

-- Resolve firearm under cursor: item window first, then tile (incl. 2nd cell of large guns).
local function JazzResolveItemUnderPt(slot_ctrl, pt)
	if not slot_ctrl or not pt then
		return
	end
	local _, item = slot_ctrl:FindItemWnd(pt)
	if item then
		return item
	end
	local unit = slot_ctrl:GetContext()
	local _, dx, dy = slot_ctrl:FindTile(pt)
	if not unit or not dx then
		return
	end
	item = unit:GetItemInSlot(slot_ctrl.slot_name, nil, dx, dy)
	if not item and dy then
		item = unit:GetItemInSlot(slot_ctrl.slot_name, nil, dx - 1, dy)
	end
	return item
end

-- Vanilla CanDropAt rejects small MiscItem on large Firearm ("cannot swap") and Removable
-- on Handheld equip slots ("different class"). Mirror ammo reload exception.
if not JazzCanDropAt_Vanilla then
	rawset(_G, "JazzCanDropAt_Vanilla", XInventorySlot.CanDropAt)
end
function XInventorySlot:CanDropAt(pt)
	if pt and InventoryDragItem then
		local item_at_dest = JazzResolveItemUnderPt(self, pt)
		if JazzIsRemovableInstallTarget(InventoryDragItem, item_at_dest)
			or JazzIsRemovableRemoveTarget(InventoryDragItem, item_at_dest) then
			return true
		end
	end
	return JazzCanDropAt_Vanilla(self, pt)
end

if not JazzEquipIsDropTarget_Vanilla then
	rawset(_G, "JazzEquipIsDropTarget_Vanilla", EquipInventorySlot._IsDropTarget)
end
function EquipInventorySlot:_IsDropTarget(drag_win, pt, drag_source_win)
	if InventoryDragItem and pt then
		local item_at_dest = JazzResolveItemUnderPt(self, pt)
		if JazzIsRemovableInstallTarget(InventoryDragItem, item_at_dest) then
			HighlightDropSlot(self, true, pt, drag_win)
			return true
		end
	end
	return JazzEquipIsDropTarget_Vanilla(self, drag_win, pt, drag_source_win)
end


local function JazzFindRemovableAttachmentItem(unit, component_id)
	if not unit or not component_id then
		return
	end
	local found
	unit:ForEachItem("JAZZ_RemovableAttachment", function(item, slot)
		if item.RemovableComponentId == component_id then
			found = item
			return "break"
		end
	end)
	if found then
		return found, unit
	end
	local squad = unit.Squad and gv_Squads[unit.Squad]
	local bag = squad and GetSquadBagInventory(squad.UniqueId or squad.squad_id or unit.Squad)
	if bag then
		bag:ForEachItem("JAZZ_RemovableAttachment", function(item, slot)
			if item.RemovableComponentId == component_id then
				found = item
				return "break"
			end
		end)
		if found then
			return found, bag
		end
	end
end

local function JazzGetOwnerUnit(owner_id)
	return g_Units[owner_id] or gv_UnitData[owner_id]
end

-- Folded half of a fold/unfold pair is combat-toggle only — hide from craft popup.
function JAZZ_IsHiddenModifyWeaponCraftOption(component_id)
	if type(component_id) ~= "string" or component_id == "" then
		return false
	end
	-- "Folded" but not "UnFolded" (covers StockLightFolded / StockFolded).
	if component_id:find("Folded", 1, true) and not component_id:find("UnFolded", 1, true) then
		return true
	end
	return false
end

function JAZZ_FilterModifyWeaponCraftOptions(components)
	local out = {}
	for _, id in ipairs(components or empty_table) do
		if not JAZZ_IsHiddenModifyWeaponCraftOption(id) then
			out[#out + 1] = id
		end
	end
	return out
end

local function JazzFoldingPairIdsMatch(a, b)
	if not a or not b or a == "" or b == "" then
		return false
	end
	if a == b then
		return true
	end
	local function listed(comp, other)
		local pair = comp and comp.zzFoldingPair
		if not pair then
			return false
		end
		if table.find(pair, other) then
			return true
		end
		if other:starts_with("JAZZ_") and table.find(pair, string.sub(other, 6)) then
			return true
		end
		if not other:starts_with("JAZZ_") and table.find(pair, "JAZZ_" .. other) then
			return true
		end
		return false
	end
	local ca, cb = WeaponComponents[a], WeaponComponents[b]
	return listed(ca, b) or listed(cb, a)
end

-- Full replace of GetChangesCost: nil-safe SectorOperationResouces lookup (JAZZ_BarrelParts race)
-- plus removable-attachment install costing InventoryItem instead of Parts.
function ModifyWeaponDlg:GetChangesCost(slotFilter, placedComponentOverride)
	if JazzEnsureBarrelPartsResource then
		JazzEnsureBarrelPartsResource()
	end
	if not self.context or not self.context.weapon then
		return {}, false, true, {}
	end

	local actualWeapon = self.context.weapon
	local weapon = self.weaponClone
	local owner = JazzGetOwnerUnit(self.context.owner)
	local components = weapon.components
	local costs = {}
	local anyChanged = false
	-- Never put non-SectorOperationResouces keys into `costs` — WeaponModChoicePopup
	-- indexes SectorOperationResouces[costName] for special-cost icons.
	local missing_removable = false

	for slot, itemId in pairs(actualWeapon.components) do
		local placedComponent = placedComponentOverride or components[slot] or ""
		if placedComponent ~= itemId and (not slotFilter or slot == slotFilter) then
			-- Fold↔Unfold of the same pair is a toggle, not a paid craft.
			if JazzFoldingPairIdsMatch(itemId, placedComponent) then
				anyChanged = true
				goto continue_slot
			end
			local item
			if slot == "Color" then
				item = Presets.WeaponColor.Default[placedComponent]
			else
				item = WeaponComponents[placedComponent]
			end

			local removable = placedComponent ~= "" and JAZZ_IsRemovableWeaponComponent(placedComponent, slot)
			if removable then
				if not CheatEnabled("FreeParts") and not JazzFindRemovableAttachmentItem(owner, placedComponent) then
					missing_removable = true
				end
			else
				local partCost = item and item.Cost or 0
				if partCost ~= 0 then
					costs.Parts = (costs.Parts or 0) + partCost
				end
				for _, cost in ipairs(item and item.AdditionalCosts or empty_table) do
					local typ = cost.Type
					if typ and typ ~= "" and SectorOperationResouces and SectorOperationResouces[typ] then
						costs[typ] = (costs[typ] or 0) + (cost.Amount or 0)
					elseif typ and typ ~= "" then
						-- Unknown resource: keep unaffordable without crashing the popup icon path.
						missing_removable = true
					end
				end
			end
			anyChanged = true
			::continue_slot::
		end
	end

	if CheatEnabled("FreeParts") then
		return costs, anyChanged, true, {}
	end

	local canAfford = not missing_removable
	local canAffordPerCost = {}
	if missing_removable then
		canAffordPerCost.JAZZ_RemovableAttachment = false
	end
	for typ, cost in pairs(costs) do
		local costPreset = SectorOperationResouces and SectorOperationResouces[typ]
		if not costPreset or not costPreset.current then
			canAfford = false
			canAffordPerCost[typ] = false
		else
			local has = costPreset.current(self.sector)
			if (has or 0) < cost then
				canAfford = false
				canAffordPerCost[typ] = false
			else
				canAffordPerCost[typ] = true
			end
		end
	end

	return costs, anyChanged, canAfford, canAffordPerCost
end

local VanillaPayCosts = ModifyWeaponDlg.PayCosts
function ModifyWeaponDlg:PayCosts(costs)
	if JazzEnsureBarrelPartsResource then
		JazzEnsureBarrelPartsResource()
	end
	local filtered = {}
	for typ, cost in pairs(costs or empty_table) do
		if SectorOperationResouces and SectorOperationResouces[typ] then
			filtered[typ] = cost
		end
	end
	return VanillaPayCosts(self, filtered)
end

-- Hide folded craft options in the modify popup (fold/unfold stays a combat toggle).
function WeaponComponentWindowClass:ToggleOptions()
	local modifyWeaponDlg = self:ResolveId("node")
	modifyWeaponDlg:CloseContextMenu()

	local parentList = self.parent
	local myIdx = parentList and table.find(parentList, self)
	if myIdx and GetUIStyleGamepad() then
		parentList:SetSelection(myIdx)
	else
		parentList:SetSelection(false)
	end

	local slotType = self.context.slot.SlotType
	local slot = self.context.slot
	local popup_ctx = self.context
	if slot and slot.AvailableComponents then
		local filtered = JAZZ_FilterModifyWeaponCraftOptions(slot.AvailableComponents)
		local slot_view = setmetatable({ AvailableComponents = filtered }, { __index = slot })
		popup_ctx = SubContext(self.context, { slot = slot_view })
	end
	local ctxMenu = XTemplateSpawn("WeaponModChoicePopup", modifyWeaponDlg, popup_ctx)
	ctxMenu:SetZOrder(999)
	ctxMenu:SetAnchor(self.box)
	ctxMenu:Open()
	ctxMenu.OnDelete = function()
		if not modifyWeaponDlg.context then
			return
		end
		modifyWeaponDlg:SetActiveSpot(false, "selected")
		RestoreCloneWeaponComponents(modifyWeaponDlg.weaponClone, modifyWeaponDlg.context.weapon)
		modifyWeaponDlg.idTextAboveButtons:SetVisible(true)
	end
	modifyWeaponDlg:SetActiveSpot(slotType, "selected")
	ctxMenu:SetFocus()
	modifyWeaponDlg.idTextAboveButtons:SetVisible(false)
	modifyWeaponDlg.idChoicePopup = ctxMenu
	XDestroyRolloverWindow()
end

local VanillaCanModifySlot = ModifyWeaponDlg.CanModifySlot
function ModifyWeaponDlg:CanModifySlot(slot, partId)
	if partId and JAZZ_IsHiddenModifyWeaponCraftOption(partId) then
		return false, "blocked", partId
	end
	if not slot then
		return VanillaCanModifySlot(self, slot, partId)
	end
	local filtered = JAZZ_FilterModifyWeaponCraftOptions(slot.AvailableComponents)
	local slot_view = setmetatable({ AvailableComponents = filtered }, { __index = slot })
	return VanillaCanModifySlot(self, slot_view, partId)
end

-- CloseRange* is shared by Barrel/Scope/Side — never show slot prefix "Ствол"/"Barrel".
local function JazzSanitizeCloseRangeEffectText(effectName, text)
	if type(text) ~= "string" or text == "" then
		return text
	end
	if effectName ~= "CloseRangeIncrease" and effectName ~= "CloseRangeDecrease"
		and effectName ~= "CloseRangeFactorIncrease" and effectName ~= "CloseRangeFactorDecrease" then
		return text
	end
	text = text:gsub("^Ствол:%s*", "Ближняя зона: ")
	text = text:gsub("^Barrel:%s*", "Close range: ")
	return text
end

-- Harden description data: never Untranslated() a pure lookup-tag string.
function GetWeaponComponentDescriptionData(componentPreset)
	local data = {}
	for _, effectName in ipairs(componentPreset.ModificationEffects or empty_table) do
		local effect = WeaponComponentEffects[effectName]
		if effect and effect.Description then
			local text = _InternalTranslate(effect.Description, componentPreset)
			if type(text) == "string" and text ~= "" and not IsLookupTag(text) then
				text = _InternalTranslate(Untranslated(text), effect)
			end
			text = JazzSanitizeCloseRangeEffectText(effectName, text)
			-- Use %S (any non-space): Lua %w is ASCII-only and drops pure-Cyrillic
			-- descriptions (IncreaseReloadAP / ReduceReliability) that have no digits.
			if type(text) == "string" and text:find("%S") and not IsLookupTag(text) then
				data[effectName] = { display = Untranslated(text) }
			elseif type(text) == "string" and text:find("%S") then
				data[effectName] = { display = TLookupTag(text) }
			end
		end
	end
	return data
end

-- Avoid Untranslated("<bullet_point> ") assert when effect description resolves empty
-- (IsLookupTag treats "<bullet_point> " as a pure lookup-tag string).
local JazzExtraStatExceptions = { "Damage", "WeaponRange", "AimAccuracy", "CritChance", "BaseAP", "ShootAP" }

function ModifyWeaponDlg:GetWeaponComponentsCombinedEffects(components)
	local collectedData = {}
	components = components or (self.weaponClone and self.weaponClone.components)
	for slot, comp in pairs(components or empty_table) do
		if #(comp or "") == 0 or not WeaponComponents[comp] then
			goto continue
		end
		local data = GetWeaponComponentDescriptionData(WeaponComponents[comp])
		for key, mod in pairs(data) do
			if not table.find(JazzExtraStatExceptions, key) then
				local value = mod.value
				if collectedData[key] and value then
					collectedData[key].value = collectedData[key].value + value
				else
					collectedData[key] = mod
				end
			end
		end
		::continue::
	end

	local lines = {}
	for _, mod in sorted_pairs(collectedData) do
		local body = _InternalTranslate(mod.display, mod)
		if type(body) == "string" and body:find("%S") then
			lines[#lines + 1] = T{990002014, "<bullet_point> <text>", text = Untranslated(body)}
		end
	end
	return table.concat(lines, "\n"), collectedData
end

local VanillaGetWeaponComponentDescription = GetWeaponComponentDescription
function GetWeaponComponentDescription(componentPreset)
	local data = GetWeaponComponentDescriptionData(componentPreset)
	local lead = {}
	local effect_lines = {}
	local indices = {}
	-- Always lead with the component name — empty-effect baselines otherwise collapse
	-- to vanilla "Без изменений" with no hint what the option is (P210 factory barrel).
	if componentPreset and componentPreset.DisplayName then
		lead[#lead + 1] = T{987654321, "<style WeaponModHeader><display_name></style>", componentPreset}
	end
	if componentPreset and componentPreset.Description then
		lead[#lead + 1] = T{componentPreset.Description, componentPreset}
	end
	for modName, mod in sorted_pairs(data) do
		local body = _InternalTranslate(mod.display, mod)
		if type(body) == "string" and body:find("%S") then
			local text = T{990002014, "<bullet_point> <text>", text = Untranslated(body)}
			effect_lines[#effect_lines + 1] = text
			local effect = WeaponComponentEffects[modName]
			if effect then
				indices[text] = effect.SortKey
			end
		end
	end
	table.sort(effect_lines, function(a, b)
		return (indices[a] or 0) < (indices[b] or 0)
	end)
	-- Baseline / visual-only options: name + short note instead of opaque "No changes".
	if #effect_lines == 0 and not (componentPreset and componentPreset.Description) then
		lead[#lead + 1] = T(990002451, --[[GetWeaponComponentDescription baseline]] "Базовый вариант. Не меняет характеристики оружия.")
	end
	local lines = lead
	for _, line in ipairs(effect_lines) do
		lines[#lines + 1] = line
	end
	if #lines == 0 then
		return VanillaGetWeaponComponentDescription(componentPreset)
	end
	return table.concat(lines, "\n"), data
end

local VanillaApplyChangesSlot = ModifyWeaponDlg.ApplyChangesSlot
function ModifyWeaponDlg:ApplyChangesSlot(modSlot, skipChance)
	assert(modSlot)
	if not modSlot or not self.canEdit then
		return
	end
	local actualWeapon = self.context.weapon
	local owner_id = self.context.owner
	local owner = JazzGetOwnerUnit(owner_id)
	local newId = self.weaponClone.components[modSlot] or ""
	local oldId = actualWeapon.components[modSlot] or ""
	if newId == oldId then
		return VanillaApplyChangesSlot(self, modSlot, skipChance)
	end

	local bag = owner and owner.Squad and GetSquadBagInventory(owner.Squad)

	-- Removing a removable module → return InventoryItem (Mech check inside API).
	if (newId == "" or newId == false) and JAZZ_IsRemovableWeaponComponent(oldId, modSlot) then
		CreateMapRealTimeThread(function()
			local ok, result = actualWeapon:JAZZ_RemoveRemovableAttachment(owner, modSlot, bag)
			if not ok then
				PlayFX("WeaponModificationFail", "start")
				if result == "broken" then
					CombatLog("important", T(990002503, "Removal failed. Attachment broken."))
					self.weaponClone:SetWeaponComponent(modSlot, false)
					ObjModified(actualWeapon)
					ObjModified(self)
				elseif result == "failed" then
					CombatLog("important", T(990002010, "Removal failed. Weapon resource max reduced."))
				else
					CombatLog("important", T(238606985729, "Modification failed."))
				end
				return
			end
			PlayFX("WeaponModificationSuccess", "start")
			CombatLog("important", T{753849538837, "Modification of <weapon> successful", weapon = actualWeapon.DisplayName})
			self.weaponClone:SetWeaponComponent(modSlot, false)
			ObjModified(actualWeapon)
			ObjModified(self)
		end)
		return
	end

	-- Installing a removable module → consume matching InventoryItem
	-- (FreeParts cheat: spawn a temp item so cabinet install works without inventory stock).
	if newId ~= "" and JAZZ_IsRemovableWeaponComponent(newId, modSlot) then
		CreateMapRealTimeThread(function()
			local item, inv = JazzFindRemovableAttachmentItem(owner, newId)
			if not item and CheatEnabled("FreeParts") then
				item = JAZZ_CreateRemovableAttachment(newId)
				inv = nil
			end
			if not item then
				PlayFX("WeaponModificationFail", "start")
				CombatLog("important", T(990002011, "No removable attachment item in inventory."))
				return
			end
			-- Swap installs eject the previous module inside Install (no second Mech roll).
			local ok, result = actualWeapon:JAZZ_InstallRemovableAttachment(owner, modSlot, item, inv)
			if not ok then
				PlayFX("WeaponModificationFail", "start")
				if result == "failed" then
					CombatLog("important", T(990002012, "Install failed. Weapon resource max reduced."))
				else
					CombatLog("important", T(238606985729, "Modification failed."))
				end
				-- FreeParts temp item was never in inventory — don't leak it on fail.
				if not inv and IsValid(item) then
					DoneObject(item)
				end
				return
			end
			PlayFX("WeaponModificationSuccess", "start")
			CombatLog("important", T{753849538837, "Modification of <weapon> successful", weapon = actualWeapon.DisplayName})
			self.weaponClone:SetWeaponComponent(modSlot, newId)
			ObjModified(actualWeapon)
			ObjModified(self)
		end)
		return
	end

	return VanillaApplyChangesSlot(self, modSlot, skipChance)
end
