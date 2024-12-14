local InventoryUIRespawn_shield
function InventoryUIRespawn()
	if InventoryUIRespawn_shield then return end
	DelayedCall(0, _InventoryUIRespawn)
	--print("InventoryUIRespawn")
end


function _InventoryUIRespawn()
	if IsValidThread(g_squad_bag_sort_thread) then
		Sleep(1)
		InventoryUIRespawn() --run after squad bag sort if concurent
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
		dlg.idUnitInfo:RespawnContent()
		dlg.idPartyContainer.idParty:RespawnContent()
		dlg.idRight:RespawnContent()
		--dlg.idRight:RespawnContent()
		dlg.idCenter:RespawnContent()
		dlg.idUnitInfo:OnContextUpdate(context)			
		dlg.idRight:OnContextUpdate(context)	
		dlg.idCenter:OnContextUpdate(context)
		
		dlg.idCenter:RespawnContent()
		dlg:OnContextUpdate(context)
		dlg.idScrollbar:ScrollTo(saveScroll)
		dlg.idScrollbarCenter:ScrollTo(saveScrollCenter)
		Msg("RespawnedInventory")
		--print("RespawnedInventory")
		
		if drag_item then
			Sleep(0) --rebuild ui
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
	["ArmorPlate"]  = "Mod/e6L4ECj/ArmorTypes/ArmorPlates.png",	
    ["HeadGear"]  = "Mod/e6L4ECj/ArmorTypes/night_vision.png",	
	["Head"]  = "UI/Icons/Items/background_helmet",	
	["Legs"]  = "UI/Icons/Items/background_pants", 
	["Torso"]  = "UI/Icons/Items/background_vest", 
	["Handheld A"]  = "UI/Icons/Items/background_weapon",
	["Handheld B"]  = "UI/Icons/Items/background_weapon",
	["Handheld A Big"]  = "UI/Icons/Items/background_weapon_big",
	["Handheld B Big"]  = "UI/Icons/Items/background_weapon_big", 
	["Vest"]  = "Mod/e6L4ECj/ArmorTypes/vest.png",	
	["Belt1"]  = "Mod/e6L4ECj/ArmorTypes/belt.png",	
	["Belt2"]  = "Mod/e6L4ECj/ArmorTypes/holster.png",	
	["Backpack"]  = "Mod/e6L4ECj/ArmorTypes/backpack.png",	
}

local tile_size = 90
local tile_size_rollover = 110
local function GetTileImage(ctrl, tile)
	local enabled = ctrl:GetEnabled()
	local slot = ctrl.parent:GetInventorySlotCtrl()
	return enabled and (tile and "UI/Inventory/T_Backpack_Slot_Small_Empty.tga" or  "UI/Inventory/T_Backpack_Slot_Small.tga" )or  "UI/Inventory/T_Backpack_Slot_Small_Empty.tga" 
end


function XInventorySlot:SpawnRolloverUI(width, height, left, top)
	local image = self.tiles[left][top]
	image:SetVisible(false)
	if width==2 then
		self.tiles[left+1][top]:SetVisible(false)
	end
	local pos = point_pack(left, top, width)
	if not self.rollover_windows[pos] then
		local item_wnd = XTemplateSpawn("XContextWindow", self)
		item_wnd:SetHandleMouse(true)
		item_wnd:SetMinWidth(tile_size_rollover*width)
		item_wnd:SetMaxWidth(tile_size_rollover*width)
		item_wnd:SetMinHeight(tile_size_rollover*height)
		item_wnd:SetMaxHeight(tile_size_rollover*height)
		item_wnd:SetGridX(left)
		item_wnd:SetGridY(top)
		item_wnd:SetGridWidth(width)
		item_wnd:SetGridHeight(height)
		item_wnd:SetUseClipBox(false)

		item_wnd:SetIdNode(true)

	
		local item_pad = XTemplateSpawn("XImage", item_wnd)
		item_pad:SetMinWidth(tile_size*width)
		item_pad:SetMaxWidth(tile_size*width)
		item_pad:SetMinHeight(tile_size*height)
		item_pad:SetMaxHeight(tile_size*height)
		--item_pad:SetImageFit("width")
		item_pad:SetId("idItemPad")
		item_pad:SetUseClipBox(false)
		item_pad:SetHandleMouse(false)
		item_pad:SetImage(width==1 and "UI/Inventory/T_Backpack_Slot_Small_Hover.tga" or "UI/Inventory/T_Backpack_Slot_Large_Hover.tga")
		item_pad:SetImageColor(0xFFc3bdac)
		
		item_pad:SetTransparency(self.image_transparency)
		item_pad.OnSetRollover = function(this,rollover)	
			XImage.OnSetRollover(this,rollover)			
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
				Image = "UI/Inventory/T_Backpack_Slot_Small.tga",				
			},
			item_wnd)
			image:SetImage(width>1 and "UI/Inventory/T_Backpack_Slot_Large.tga" or "UI/Inventory/T_Backpack_Slot_Small.tga")
			local imgslot = XImage:new({
				MinWidth = tile_size,
				MaxWidth = tile_size,
				MinHeight = tile_size,
				MaxHeight = tile_size,

				Dock = "box",
				Id = "idEqSlotImage",
			},
			image)	
			imgslot:SetImageFit(width>1 and "none" or "width")
			imgslot:SetImage(width>1 and equip_slot_images[self.slot_name.." Big"] or slot_img)			
		end
		local rollover_image = XImage:new({
			MinWidth = tile_size_rollover,
			MaxWidth = tile_size_rollover,
			MinHeight = tile_size_rollover,
			MaxHeight = tile_size_rollover,

			Id = "idRollover",
			Image = width==1 and "UI/Inventory/T_Backpack_Slot_Small_Hover.tga" or "UI/Inventory/T_Backpack_Slot_Large_Hover.tga",
			ImageColor = 0xFFc3bdac,
			},
		item_wnd)
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

			--this only happens when over empty slots
			local drag_item = InventoryDragItem	
			HighlightDropSlot(this, true, pt, drag_win)

			-- pick + equip
			local slot = self
			local unit_ap, ap_cost, action_name
			local dest_container = slot:GetContext()
			if dest_container:CheckClass(drag_item, slot.slot_name) then
				local wnd, l, t =  slot:FindTile(pt)
				if l and t then
					ap_cost, unit_ap, action_name = InventoryItemsAPCost( dest_container, slot.slot_name)
				end
			end
			local is_combat = InventoryIsCombatMode()
			if not is_combat then 
				drag_win:OnContextUpdate(drag_win:GetContext())
			end

			if not mouse_text then
				mouse_text = action_name or T(155594239482, "Move item")			
				if is_combat and ap_cost and ap_cost>0 then
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
	return XInventoryTile:new({slot_image = equip_slot_images[slot_name]}, self)
end

