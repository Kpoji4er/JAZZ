-- JAZZ-UI-001 path B: attachment chips on firearm tiles; template Icon stays vanilla.
-- WeaponIconBake.lua is dormant (not in metadata.code). Do not read JazzWeaponIcon_BakeEnabled.

function JazzWeaponIcon_BindItemImage(img, item)
	if not img or not item then
		return false
	end
	local icon = (item.GetItemUIIcon and item:GetItemUIIcon()) or item.Icon
	if icon then
		img:SetImage(icon)
	end
	return false
end

function JazzWeaponIcon_RefreshWeaponDisplays()
	local function visit(win)
		if not win then
			return
		end
		local item = win.GetContext and win:GetContext() or rawget(win, "context")
		if item and JazzAttachChips_IsFirearm and JazzAttachChips_IsFirearm(item) then
			local icon = rawget(win, "idIcon") or (win.ResolveId and win:ResolveId("idIcon"))
			if icon then
				JazzWeaponIcon_BindItemImage(icon, item)
				if JazzAttachChips_Apply then
					JazzAttachChips_Apply(icon, item)
				end
			end
		end
		if win.ForEachChild then
			win:ForEachChild(visit)
		else
			for _, child in ipairs(win) do
				visit(child)
			end
		end
	end
	local roots = {}
	local igi = GetInGameInterface and GetInGameInterface()
	if igi then
		roots[#roots + 1] = igi
	end
	local mode = GetInGameInterfaceModeDlg and GetInGameInterfaceModeDlg()
	if mode and mode ~= igi then
		roots[#roots + 1] = mode
	end
	local inv = GetMercInventoryDlg and GetMercInventoryDlg()
	if inv then
		roots[#roots + 1] = inv
	end
	for _, root in ipairs(roots) do
		visit(root)
	end
end

function JazzWeaponIcon_ScheduleWeaponDisplayRefresh()
	if DelayedCall then
		DelayedCall(0, JazzWeaponIcon_RefreshWeaponDisplays)
		DelayedCall(120, JazzWeaponIcon_RefreshWeaponDisplays)
	else
		JazzWeaponIcon_RefreshWeaponDisplays()
	end
end

function OnMsg.SelectionChange()
	JazzWeaponIcon_ScheduleWeaponDisplayRefresh()
end

function OnMsg.SelectedObjChange()
	JazzWeaponIcon_ScheduleWeaponDisplayRefresh()
end

function OnMsg.CombatActionEnd()
	JazzWeaponIcon_ScheduleWeaponDisplayRefresh()
end

function OnMsg.WeaponModifiedSuccessSync()
	JazzWeaponIcon_ScheduleWeaponDisplayRefresh()
end

local JazzWeaponIcon_OldOnContextUpdate = XInventoryItem.OnContextUpdate
function XInventoryItem:OnContextUpdate(item, ...)
	JazzWeaponIcon_OldOnContextUpdate(self, item, ...)
	if not item then
		return
	end
	JazzWeaponIcon_BindItemImage(self.idItemImg, item)
	if JazzAttachChips_Apply then
		JazzAttachChips_Apply(self.idItemImg, item)
	end
end

-- Remountable hover: highlight compatible firearms (same visual as ammo drag).
-- Skip while a drag is active — HighlightWeaponsForAmmo(InventoryDragItem) owns that pass.
local JazzInventoryItem_OnSetRollover = XInventoryItem.OnSetRollover
function XInventoryItem:OnSetRollover(rollover)
	if JazzInventoryItem_OnSetRollover then
		JazzInventoryItem_OnSetRollover(self, rollover)
	elseif XContextControl and XContextControl.OnSetRollover then
		XContextControl.OnSetRollover(self, rollover)
	end
	if InventoryDragItem then
		return
	end
	local item = self.context or (self.GetContext and self:GetContext())
	if IsKindOf(item, "JAZZ_RemovableAttachment") then
		HighlightWeaponsForAmmo(item, not not rollover)
	end
end

-- Compat for UIWeaponDisplay run_after that still calls SuppressModBadge.
function JazzWeaponIcon_SuppressModBadge(img, item, _baked)
	if JazzAttachChips_Apply then
		JazzAttachChips_Apply(img, item)
	end
end

-- Vanilla XInventorySlot:InternalDragStop only calls OnDragDrop (→ ClearDragState) when
-- OnDrop returns falsy. Truthy results keep click-to-drop alive:
--   "not valid target" — intentional (retry / switch merc while holding item)
--   true — target claims the drop was handled (use-item on big portrait)
-- Big-portrait OnDrop returns true on give-distance / can-use failure WITHOUT ClearDragState,
-- so the floating icon stays until capture is lost. Vanilla OnCaptureLost then StopDrag()s
-- (strips mouse follow) but never deletes the window → orphan icon stuck on XDesktop.
function XInventorySlot:InternalDragStop(pt)
	local drag_win = self.drag_win
	if not drag_win then
		return
	end
	self:UpdateDrag(drag_win, pt)

	local result = "not valid target"
	local target = self:GetDragTarget(pt)
	if target then
		result = target:OnDrop(drag_win, pt, self)
	else
		PlayFX("DropItemFail", "start")
	end
	if not result then
		self:OnDragDrop(target, drag_win, result, pt)
	elseif result == true and self.drag_win then
		-- Handled drop that forgot to clear (failed use / too far on big portrait).
		self:CancelDragging()
	end
end

function XInventorySlot:OnCaptureLost()
	if self.drag_win then
		self:CancelDragging()
		return
	end
	XDragAndDropControl.OnCaptureLost(self)
end

local InventoryUIRespawn_shield
function InventoryUIRespawn()
    if InventoryUIRespawn_shield then
        return
    end
    DelayedCall(0, _InventoryUIRespawn)
    -- print("InventoryUIRespawn")
end

function _InventoryUIRespawn()
    if IsValidThread(g_squad_bag_sort_thread) then
        Sleep(1)
        InventoryUIRespawn() -- run after squad bag sort if concurent
		InventoryUIResetSquadBag()
        return
    end
    InventoryUIRespawn_shield = true
    local dlg = GetMercInventoryDlg()
    if dlg then
        local drag_item = InventoryDragItem
        if drag_item then
            CancelDrag(dlg)
        end

        local saveScroll = dlg.idScrollbar.Scroll
        local saveScrollCenter = dlg.idScrollbarCenter.Scroll
        local context = dlg:GetContext()
        if dlg and context then
            if dlg.idUnitInfo then
                dlg.idUnitInfo:RespawnContent()
                dlg.idUnitInfo:OnContextUpdate(context)
            end
            if dlg.idPartyContainer then
                dlg.idPartyContainer.idParty:RespawnContent()
                dlg.idPartyContainer.idParty:OnContextUpdate(context)
            end

            if dlg.idRight then
                dlg.idRight:RespawnContent()
                dlg.idRight:OnContextUpdate(context)
            end
            if dlg.idCenter then
                dlg.idCenter:RespawnContent()
                dlg.idCenter:OnContextUpdate(context)
            end
            dlg:OnContextUpdate(context)
            dlg.idScrollbar:ScrollTo(saveScroll)
            dlg.idScrollbarCenter:ScrollTo(saveScrollCenter)
            Msg("RespawnedInventory")
        end
        -- print("RespawnedInventory")

        if drag_item then
            Sleep(0) -- rebuild ui
            RestartDrag(dlg, drag_item)
        end
    end
    InventoryUIRespawn_shield = nil
	if JazzWeaponIcon_RefreshWeaponDisplays then
		JazzWeaponIcon_RefreshWeaponDisplays()
	end
end

function InventoryEquipAPText(bShow, text)
    local dlg = GetMercInventoryDlg()
    local ctrl = dlg.idRight.idEquipHint
    ctrl:SetVisible(bShow)
    ctrl:SetText(bShow and text or "")
end

local equip_slot_images = {
    ["ArmorPlate"] = "Mod/e6L4ECj/ArmorTypes/ArmorPlate.png",
    ["HeadGear"] = "Mod/e6L4ECj/ArmorTypes/night_vision.png",
    ["Head"] = "UI/Icons/Items/background_helmet",
    ["Legs"] = "UI/Icons/Items/background_pants",
    ["Torso"] = "UI/Icons/Items/background_vest",
    ["Handheld A"] = "UI/Icons/Items/background_weapon",
    ["Handheld B"] = "UI/Icons/Items/background_weapon",
    ["Handheld A Big"] = "UI/Icons/Items/background_weapon_big",
    ["Handheld B Big"] = "UI/Icons/Items/background_weapon_big",
    --	["Vest"]  = "Mod/e6L4ECj/ArmorTypes/vest.png",	
    --	["Belt1"]  = "Mod/e6L4ECj/ArmorTypes/belt.png",	
    --	["Belt2"]  = "Mod/e6L4ECj/ArmorTypes/holster.png",	
    --	["Backpack"]  = "Mod/e6L4ECj/ArmorTypes/backpack.png",	
    ["PocketInventory"] = "Mod/e6L4ECj/ArmorTypes/pocket.png",
    ["AmmoInventory"] = "Mod/e6L4ECj/ArmorTypes/ammo.png",
    ["GrenadesInventory"] = "Mod/e6L4ECj/ArmorTypes/granate.png",
    ["OrdnanceInventory"] = "Mod/e6L4ECj/ArmorTypes/C4.png",
    ["MedicalInventory"] = "Mod/e6L4ECj/ArmorTypes/med.png",
    ["KnifeInventory"] = "Mod/e6L4ECj/ArmorTypes/knife.png"
}

local tile_size = 90
local tile_size_rollover = 110
local function GetTileImage(ctrl, tile)
    local enabled = ctrl:GetEnabled()
    local slot = ctrl.parent:GetInventorySlotCtrl()
    return enabled and
               (tile and "UI/Inventory/T_Backpack_Slot_Small_Empty.tga" or "UI/Inventory/T_Backpack_Slot_Small.tga") or
               "UI/Inventory/T_Backpack_Slot_Small_Empty.tga"
end

function XInventorySlot:SpawnRolloverUI(width, height, left, top)
    local image = self.tiles[left][top]
    if not image then
        return
    end
    image:SetVisible(false)
    if width == 2 then
        self.tiles[left + 1][top]:SetVisible(false)
    end
    local pos = point_pack(left, top, width)
    if not self.rollover_windows[pos] then
        local item_wnd = XTemplateSpawn("XContextWindow", self)
        item_wnd:SetHandleMouse(true)
        item_wnd:SetMinWidth(tile_size_rollover * width)
        item_wnd:SetMaxWidth(tile_size_rollover * width)
        item_wnd:SetMinHeight(tile_size_rollover * height)
        item_wnd:SetMaxHeight(tile_size_rollover * height)
        item_wnd:SetGridX(left)
        item_wnd:SetGridY(top)
        item_wnd:SetGridWidth(width)
        item_wnd:SetGridHeight(height)
        item_wnd:SetUseClipBox(false)

        item_wnd:SetIdNode(true)

        local item_pad = XTemplateSpawn("XImage", item_wnd)
        item_pad:SetMinWidth(tile_size * width)
        item_pad:SetMaxWidth(tile_size * width)
        item_pad:SetMinHeight(tile_size * height)
        item_pad:SetMaxHeight(tile_size * height)
        -- item_pad:SetImageFit("width")
        item_pad:SetId("idItemPad")
        item_pad:SetUseClipBox(false)
        item_pad:SetHandleMouse(false)
        item_pad:SetImage(width == 1 and "UI/Inventory/T_Backpack_Slot_Small_Hover.tga" or
                              "UI/Inventory/T_Backpack_Slot_Large_Hover.tga")
        item_pad:SetImageColor(0xFFc3bdac)

        item_pad:SetTransparency(self.image_transparency)
        item_pad.OnSetRollover = function(this, rollover)
            XImage.OnSetRollover(this, rollover)
            if self.rollover_image_transparency then
                this:SetTransparency(rollover and self.rollover_image_transparency or self.image_transparency)
            end
        end
        local slot_img = equip_slot_images[self.slot_name]
        if equip_slot_images[self.slot_name] then
            local image = XImage:new({
                MinWidth = tile_size,
                MaxWidth = tile_size,
                MinHeight = tile_size,
                MaxHeight = tile_size,
                Id = "idBackImage",
                Image = "UI/Inventory/T_Backpack_Slot_Small.tga"
            }, item_wnd)
            image:SetImage(width > 1 and "UI/Inventory/T_Backpack_Slot_Large.tga" or
                               "UI/Inventory/T_Backpack_Slot_Small.tga")
            local imgslot = XImage:new({
                MinWidth = tile_size,
                MaxWidth = tile_size,
                MinHeight = tile_size,
                MaxHeight = tile_size,

                Dock = "box",
                Id = "idEqSlotImage"
            }, image)
            imgslot:SetImageFit(width > 1 and "none" or "width")
            imgslot:SetImage(width > 1 and equip_slot_images[self.slot_name .. " Big"] or slot_img)
        end
        local rollover_image = XImage:new({
            MinWidth = tile_size_rollover,
            MaxWidth = tile_size_rollover,
            MinHeight = tile_size_rollover,
            MaxHeight = tile_size_rollover,

            Id = "idRollover",
            Image = width == 1 and "UI/Inventory/T_Backpack_Slot_Small_Hover.tga" or
                "UI/Inventory/T_Backpack_Slot_Large_Hover.tga",
            ImageColor = 0xFFc3bdac
        }, item_wnd)
        local center_text = XTemplateSpawn("AutoFitText", item_wnd)
        center_text:SetTranslate(true)
        center_text:SetTextStyle("DescriptionTextAPRed")
        center_text:SetId("idCenterText")
        center_text:SetText("")
        center_text:SetUseClipBox(false)
        center_text:SetTextHAlign("center")
        center_text:SetTextVAlign("center")
        center_text:SetHandleMouse(false)

        item_wnd.IsDropTarget = function(this, drag_win, pt, source)
            return self:_IsDropTarget(drag_win, pt, source)
        end

        item_wnd.OnDropEnter = function(this, drag_win, pt, drag_source_win)
            InventoryOnDragEnterStash()
            local mouse_text = InventoryGetMoveIsInvalidReason(self.context, InventoryStartDragContext)

            -- this only happens when over empty slots
            local drag_item = InventoryDragItem
            HighlightDropSlot(this, true, pt, drag_win)

            -- pick + equip
            local slot = self
            local unit_ap, ap_cost, action_name
            local dest_container = slot:GetContext()
            if dest_container:CheckClass(drag_item, slot.slot_name) then
                local wnd, l, t = slot:FindTile(pt)
                if l and t then
                    ap_cost, unit_ap, action_name = InventoryItemsAPCost(dest_container, slot.slot_name)
                end
            end
            local is_combat = InventoryIsCombatMode()
            if not is_combat then
                drag_win:OnContextUpdate(drag_win:GetContext())
            end

            if not mouse_text then
                mouse_text = action_name or T(155594239482, "Move item")
                if is_combat and ap_cost and ap_cost > 0 then
                    mouse_text = InventoryFormatAPMouseText(unit_ap, ap_cost, mouse_text)
                end
            end
            InventoryShowMouseText(true, mouse_text)
            HighlightAPCost(InventoryDragItem, true, this)
        end

        item_wnd.OnDropLeave = function(this, drag_win, pt, source)
            if drag_win and drag_win.window_state ~= "destroying" then
                HighlightDropSlot(this, false, pt, drag_win)
                InventoryShowMouseText(false)
                HighlightAPCost(InventoryDragItem, false, this)
            end
        end

        item_wnd.GetInventorySlotCtrl = function(this)
            return this.parent or self
        end

        self.rollover_windows[pos] = item_wnd
    end
end

function EquipInventorySlot:SpawnTile(slot_name)
    return XInventoryTile:new({
        slot_image = equip_slot_images[slot_name]
    }, self)
end

function HighlightWeaponsForAmmo(ammo, bShow)
    local dlg = GetMercInventoryDlg()
    if not dlg or not ammo then
        return
    end
    if dlg.compare_mode then
        bShow = false
    end
    -- squad bag	
    local h_members = {}
    local is_bag_item = ammo:IsKindOf("SquadBagItem")
    if is_bag_item then
        local bag = gv_SquadBag
        h_members[bag] = true
    end
    local is_ammo = IsKindOf(ammo, "Ammo")
    local is_ordnance = IsKindOf(ammo, "Ordnance")
    local is_removable = IsKindOf(ammo, "JAZZ_RemovableAttachment")
    if not (is_ammo or is_ordnance or is_removable) and not is_bag_item then
        return
    end

    local weapon_class = is_ammo and "Firearm" or "HeavyWeapon"
    local highlight_icon = "UI/Icons/Rollover/ammo"
    -- Highlight portraits
    local left = dlg:ResolveId("idPartyContainer")
    local squad_list = left and left.idParty and left.idParty.idContainer or empty_table
    for _, button in ipairs(squad_list) do
        local member = button:GetContext()
        if (is_ammo or is_ordnance) and member then
            for _, slot_data in ipairs(member.inventory_slots) do
                local slot_name = slot_data.slot_name
                if IsEquipSlot(slot_name) then
                    local result = member:ForEachItemInSlot(slot_name, weapon_class,
                        function(witem, slot, left, top, caliber)
                            if witem.Caliber == caliber then
                                return "break"
                            end
                        end, ammo.Caliber)
                    if result == "break" then
                        -- head
                        button:SetHighlightedStatOrIcon(bShow and highlight_icon)
                        -- backpack
                        h_members[member] = true
                    end
                end
            end
        elseif is_removable and member and JazzIsRemovableInstallTarget then
            for _, slot_data in ipairs(member.inventory_slots) do
                local slot_name = slot_data.slot_name
                if IsEquipSlot(slot_name) then
                    local result = member:ForEachItemInSlot(slot_name, "FirearmBase", function(witem)
                        if JazzIsRemovableInstallTarget(ammo, witem) then
                            return "break"
                        end
                    end)
                    if result == "break" then
                        button:SetHighlightedStatOrIcon(bShow and highlight_icon)
                        h_members[member] = true
                    end
                end
            end
        end

        if not bShow then
            button:SetHighlighted(bShow)
        end
    end

    -- Highlight weapons (once — independent of party portrait count)
    local all_slots = dlg:GetSlotsArray()
    for slot_wnd in pairs(all_slots or empty_table) do
        local slot_name = slot_wnd.slot_name
        local target = slot_wnd:GetContext()
        local found = false
        for wnd, witem in pairs(slot_wnd.item_windows or empty_table) do
            local match = false
            if (is_ammo or is_ordnance) and IsKindOf(witem, weapon_class) and ammo.Caliber == witem.Caliber then
                match = true
            elseif is_removable and IsKindOf(witem, "FirearmBase")
                and JazzIsRemovableInstallTarget and JazzIsRemovableInstallTarget(ammo, witem) then
                match = true
            end
            if match then
                wnd:OnSetRollover(bShow)
                HighlihgtRollover(witem:GetUIWidth(), wnd, bShow)
                found = true
            end
        end
        if not IsKindOf(target, "SquadBag") and slot_wnd and not IsEquipSlot(slot_name) and
            (IsKindOf(target, "Unit") and not target:IsDead()) and (found or not bShow or h_members[target]) then
            local name = slot_wnd.parent and slot_wnd.parent.idName
            if name then
                name:SetHightlighted(bShow)
            end
        end
    end
end

function InventoryIsValidTargetForUnit(ctrl_context)
    local unit = GetInventoryUnit()
    if gv_SatelliteView and IsKindOf(ctrl_context, "SectorStash") then
        if not InventoryIsValidTargetForUnitInTransit(ctrl_context) then
            return false, T(257112039195, "<style InventoryHintTextRed>In transit")
        end
        if unit and unit.Squad and gv_Squads[unit.Squad] and ctrl_context.sector_id ~=
            gv_Squads[unit.Squad].CurrentSector then
            return false, T(212348537316, "<style InventoryHintTextRed>Not on sector")
        end
    end

    if InventoryIsCombatMode() and (IsKindOf(ctrl_context, "SquadBag") or IsKindOf(ctrl_context, "SectorStash")) then
        return false, T(25711203919511, "<style InventoryHintTextRed>В бою")
    end

    if IsKindOfClasses(ctrl_context, "Unit", "UnitData") and not ctrl_context:IsDead() then
        local ctrl_context_unit = ctrl_context.session_id and g_Units[ctrl_context.session_id]
        if ctrl_context:HasStatusEffect("BandageInCombat") then
            return false, T(107419565286, "Character is busy bandaging")
--        elseif ctrl_context:IsDowned() then
--            return false, T(360582491602, "Character is Downed")
--        elseif ctrl_context:HasStatusEffect("Unconscious") then
--            return false, T(894812059755, "Character is Unconscious")
        elseif g_Overwatch[ctrl_context] or g_Pindown[ctrl_context] then
            return false, T(462153644901, "Character is busy")
        elseif ctrl_context_unit and g_Overwatch[ctrl_context_unit] or g_Pindown[ctrl_context_unit] then
            return false, T(462153644901, "Character is busy")
        elseif ctrl_context.retreat_to_sector then
            return false, T(462153644901, "Character is busy")
        end
    end

    return true
end

function InventoryGetTargetsForGiveAction(context)
    if not InventoryIsContainerOnSameSector(context) then
        return {}
    end
    local targets = table.copy(GetValidMercsToTakeItem(context))
    if IsKindOf(context.item, "SquadBagItem") -- and not IsKindOf(context.context,"SquadBag") 
    and InventoryIsValidTargetForUnitInTransit(context.context) then
        targets[#targets + 1] = context.unit.Squad
    end
    return targets
end

function InventoryGetTargetsForGiveToSquadAction(context)
    local ctx = context.context
    local sector_id
    if IsKindOf(ctx, "SectorStash") then
        sector_id = ctx.sector_id
    else
        local unit_squad = context.unit and context.unit.Squad
        sector_id = gv_Squads[unit_squad].CurrentSector
    end

    local unit = context.context
    local unit_squad = unit.Squad or unit.squad_id -- the second part is a squad bag
    local squads = GetCurrentSectorPlayerSquads(sector_id)

    local unit = context.unit
    table.remove_entry(squads, "UniqueId", unit.Squad or "")
    return squads
end

function HighlightEquipSlots(item, bShow)
	local dlg = GetMercInventoryDlg()
	if not dlg then return end

	local compare_mode_on = item:IsWeapon() and InventoryIsCompareMode(dlg)
	local compare_mode_slot = compare_mode_on and (dlg.compare_mode_weaponslot == 1 and "Handheld A" or "Handheld B") or false

	local context = GetInventoryUnit()
	local width = item:GetUIWidth()
	local height = 1
	local p1 = point_pack(point(1, 1))
	local p2 = point_pack(point(2, 1))

	for _, slot_data in ipairs(context.inventory_slots) do
		local slot_name = slot_data.slot_name
		if IsEquipSlot(slot_name) and context:CheckClass(item, slot_name) and (not compare_mode_slot or compare_mode_slot == slot_name) then
			local target = dlg:GetSlotByName(slot_name)
			if not (target and target.CanEquip and target.tiles) then goto continue end

			local valid_idx = { target:CanEquip(item, p1) or false, target:CanEquip(item, p2) or false }
			local count = context:CountItemsInSlot(slot_name)

			if width == 1 or count <= 1 then
				if count == 0 then
					if width == 1 then
						if bShow then
							for i = 1, 10 do
								if target.tiles[i] then
									target:SpawnRolloverUI(width, height, i, 1)
								end
							end
							for pos, wnd in pairs(target.rollover_windows or empty_table) do
								wnd:OnSetRollover(bShow)
								HighlihgtRollover(width, wnd, bShow)
							end
						else
							for pos, wnd in pairs(target.rollover_windows or empty_table) do
								local l, t, w = point_unpack(pos)
								if target.tiles[l] and target.tiles[l][t] then
									target.tiles[l][t]:SetVisible(true)
								end
								if w > 1 and target.tiles[l + 1] and target.tiles[l + 1][t] then
									target.tiles[l + 1][t]:SetVisible(true)
								end
								wnd:delete()
							end
							target.rollover_windows = {}
						end
					elseif width > 1 then
						if bShow then
							target:SpawnRolloverUI(width, height, 1, 1)
							for pos, wnd in pairs(target.rollover_windows or empty_table) do
								wnd:OnSetRollover(bShow)
								HighlihgtRollover(width, wnd, bShow)
							end
						else
							for pos, wnd in pairs(target.rollover_windows or empty_table) do
								local l, t, w = point_unpack(pos)
								if target.tiles[l] and target.tiles[l][t] then
									target.tiles[l][t]:SetVisible(true)
								end
								if w > 1 and target.tiles[l + 1] and target.tiles[l + 1][t] then
									target.tiles[l + 1][t]:SetVisible(true)
								end
								wnd:delete()
							end
							target.rollover_windows = {}
						end
					end
				elseif count == 1 and width == 1 then
					for wnd, witem in pairs(target.item_windows or empty_table) do
						if witem ~= item then
							wnd:OnSetRollover(bShow)
							HighlihgtRollover(width, wnd, bShow)
						end
					end
					if bShow then
						for i = 1, context:GetMaxTilesInSlot(slot_name) do
							local tile = target.tiles[i] and target.tiles[i][1]
							if tile and tile:GetVisible() then
								if valid_idx[i] then
									target:SpawnRolloverUI(width, height, i, 1)
								else
									if tile.idEqSlotImage then
										tile.idEqSlotImage:SetImage("UI/Inventory/cross")
										tile.idEqSlotImage:SetImageFit("none")
									end
								end
							end
						end
						for pos, wnd in pairs(target.rollover_windows or empty_table) do
							wnd:OnSetRollover(bShow)
							HighlihgtRollover(width, wnd, bShow)
						end
					else
						for pos, wnd in pairs(target.rollover_windows or empty_table) do
							local l, t = point_unpack(pos)
							if target.tiles[l] and target.tiles[l][t] then
								target.tiles[l][t]:SetVisible(true)
							end
							wnd:delete()
						end
						target.rollover_windows = {}
						for i = 1, context:GetMaxTilesInSlot(slot_name) do
							if not valid_idx[i] then
								local tile = target.tiles[i] and target.tiles[i][1]
								if tile and tile.idEqSlotImage then
									tile.idEqSlotImage:SetImage(equip_slot_images[slot_name])
									tile.idEqSlotImage:SetImageFit("width")
								end
							end
						end
					end
				else
					for wnd, witem in pairs(target.item_windows or empty_table) do
						if valid_idx[wnd.GridX] and witem ~= item then
							wnd:OnSetRollover(bShow)
							HighlihgtRollover(width, wnd, bShow)
						end
					end
				end
			end
			::continue::
		end
	end
end

-- Combat HUD: allow ammo-type change when magazine is full (vanilla blocks FullClipHaveOther).
function GetQuickReloadWeaponAndAmmo(parent, weapon)
	local wep = weapon
	if not wep and parent then
		local node = parent.ResolveId and parent:ResolveId("node")
		node = node and node.ResolveId and node:ResolveId("node")
		wep = node and node.context
	end
	if not wep then
		return false
	end
	local unit = SelectedObj
	if not unit then
		return false
	end

	local _, __, wl = unit:GetActiveWeapons()
	local idx = table.find(wl, wep)

	local ammos = unit:GetAvailableAmmos(wep, nil, "unique")
	local can, err = IsWeaponAvailableForReload(wep, ammos)
	if not can then
		return false, err
	end

	local currentClass = wep.ammo and wep.ammo.class
	if err == AttackDisableReasons.FullClipHaveOther then
		for _, ammo in ipairs(ammos) do
			if ammo.class ~= currentClass then
				return idx, ammo
			end
		end
		return false, AttackDisableReasons.FullClip
	end

	local currentAmmo
	if currentClass then
		local haveMoreFromCurrent = table.find(ammos, "class", currentClass)
		currentAmmo = haveMoreFromCurrent and ammos[haveMoreFromCurrent] or ammos[1]
	else
		currentAmmo = ammos[1]
	end

	return idx, currentAmmo
end

-- Small lift above the reload control (px). Keep tiny: full weapon-strip anchor overshoots.
local JazzAmmoMenuGap = 24

local function JazzResolveAmmoChoiceAnchor(mode_dlg, anchor_btn)
	if IsKindOf(anchor_btn, "XWindow") and anchor_btn.window_state ~= "destroying" then
		local b = anchor_btn.box
		if b and b:sizex() > 0 and b:sizey() > 0 then
			return anchor_btn
		end
	end
	local weaponUI = mode_dlg and mode_dlg:ResolveId("idWeaponUI")
	if weaponUI then
		local reload = weaponUI:ResolveId("idReloadButton") or weaponUI:ResolveId("idSubReloadButton")
		if reload then
			local b = reload.box
			if b and b:sizex() > 0 and b:sizey() > 0 then
				return reload
			end
		end
		local b = weaponUI.box
		if b and b:sizex() > 0 and b:sizey() > 0 then
			return weaponUI
		end
	end
	return false
end

local function JazzAmmoMenuAnchorBox(anchor, gap)
	local ab = anchor.box
	if not ab or ab:sizex() <= 0 then
		return ab
	end
	-- Move the anchor rect up so center-top leaves a gap above the button/icon.
	gap = gap or 0
	return box(ab:minx(), ab:miny() - gap, ab:maxx(), ab:maxy() - gap)
end

-- Same text labels as inventory reload submenu: "<ammo_type>(<count>)".
local function JazzShowCombatAmmoTypeChoice(unit, weapon, wepIdx, delayed_fx, anchor_btn)
	local mode_dlg = GetInGameInterfaceModeDlg()
	if not mode_dlg then
		return false
	end
	local options = GetReloadOptionsForWeapon(weapon, unit, "skipSubWeapon")
	if not options or #options == 0 then
		return false
	end

	local anchor = JazzResolveAmmoChoiceAnchor(mode_dlg, anchor_btn)
	if not anchor then
		return false
	end

	-- Toggle closed if already open.
	local existing = rawget(mode_dlg, "jazzAmmoContextPopup")
	if existing and existing.window_state ~= "destroying" then
		existing:Close()
		mode_dlg.jazzAmmoContextPopup = false
		return true
	end
	if mode_dlg.ClosePopup then
		mode_dlg:ClosePopup(CombatActions.Reload)
	end

	local popup
	local slot_wnd = {
		slot_name = unit.current_weapon or "Handheld A",
		ClosePopup = function()
			if popup and popup.window_state ~= "destroying" then
				popup:Close()
			end
			if mode_dlg then
				mode_dlg.jazzAmmoContextPopup = false
			end
		end,
	}
	local context = {
		action = "reload",
		item = weapon,
		context = unit,
		unit = unit,
		slot_wnd = slot_wnd,
	}
	popup = XTemplateSpawn("InventoryContextSubMenu", terminal.desktop, context)
	popup:SetMargins(box(0, 0, 0, JazzAmmoMenuGap))
	popup:SetAnchorType("center-top")
	popup:SetAnchor(JazzAmmoMenuAnchorBox(anchor, JazzAmmoMenuGap))
	mode_dlg.jazzAmmoContextPopup = popup
	popup:Open()
	if popup.idTitle then
		popup.idTitle:SetText(T(231508638088, "Ammo"))
	end
	return true
end

function QuickReloadButton(parent, weapon, delayed_fx)
	local unit = SelectedObj
	local wepIdx, ammo = GetQuickReloadWeaponAndAmmo(parent, weapon)
	if not wepIdx then
		return
	end
	local wep = weapon
	if not wep and parent then
		local node = parent.ResolveId and parent:ResolveId("node")
		wep = node and node.context
	end
	if wep then
		local ammos = unit:GetAvailableAmmos(wep, nil, "unique")
		local can, err = IsWeaponAvailableForReload(wep, ammos)
		if can and err == AttackDisableReasons.FullClipHaveOther then
			if JazzShowCombatAmmoTypeChoice(unit, wep, wepIdx, delayed_fx, parent) then
				return true
			end
		end
	end
	CombatActions.Reload:Execute({ unit }, {
		weapon = wepIdx,
		target = ammo.class,
		delayed_fx = delayed_fx,
		item_id = weapon and weapon.id,
	})
	return true
end
