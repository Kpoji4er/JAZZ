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
    if not (is_ammo or is_ordnance) and not is_bag_item then
        return
    end

    local weapon_class = is_ammo and "Firearm" or "HeavyWeapon"
    -- Highlight portraits
    local left = dlg:ResolveId("idPartyContainer")
    local squad_list = left.idParty and left.idParty.idContainer or empty_table
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
                        button:SetHighlightedStatOrIcon(bShow and "UI/Icons/Rollover/ammo")
                        -- backpack
                        h_members[member] = true
                    end
                end
            end
        end

        -- Highlight weapons
        local all_slots = dlg:GetSlotsArray()
        for slot_wnd in pairs(all_slots) do
            local slot_name = slot_wnd.slot_name
            local target = slot_wnd:GetContext()
            local found = false
            for wnd, witem in pairs(slot_wnd.item_windows or empty_table) do
                if (is_ammo or is_ordnance) and IsKindOf(witem, weapon_class) and ammo.Caliber == witem.Caliber then
                    wnd:OnSetRollover(bShow)
                    HighlihgtRollover(witem:GetUIWidth(), wnd, bShow)
                    found = true
                end
            end
            if not IsKindOf(target, "SquadBag") and slot_wnd and not IsEquipSlot(slot_name) and
                (IsKindOf(target, "Unit") and not target:IsDead()) and (found or not bShow or h_members[target]) then
                local name = slot_wnd.parent.idName
                -- print(slot_wnd.parent.idName)
                if name then
                    name:SetHightlighted(bShow)
                end
            end
        end

        if not bShow then
            button:SetHighlighted(bShow)
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
