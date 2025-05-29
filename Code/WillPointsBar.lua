DefineClass.WillPointBar = {
	__parents = {"XFrame", "XContextControl"},
	properties = {
		{ category = "Progress", id = "MaxValueProperty", name = "Max Value Property", editor = "text", default = "MaxWillPoints", },
		{ category = "Progress", id = "Progress", name = "Progress values", editor = "number_list", default = {}, item_default = 0, invalidate = "measure" },
		{ category = "Progress", id = "MaxProgress", name = "Max progress", editor = "number", default = 100, invalidate = true, },
		{ category = "Progress", id = "MinProgressSize", name = "Size at progress 0", editor = "number", default = 0 },
		{ category = "Progress", id = "DisplayTempWp", name = "Display Temporary WillPoints", editor = "bool", default = false },
		{ category = "Progress", id = "FitSegments", name = "Fit Segments", help = "Fit segments in the max width", editor = "bool", default = false },
		
		{ category = "Icons", id = "ShowIcons", name = "Show Prediction Icons", editor = "bool", default = false, },

		{ category = "Icons", id = "PotentialDeathIcon", name = "Potential Death Icon", editor = "ui_image", default = "UI/Hud/death_blow", },
		{ category = "Icons", id = "CoverIcon", name = "Cover Icon", editor = "ui_image", default = "UI/Hud/cover", },
		{ category = "Icons", id = "CoverExposeIcon", name = "Cover Icon", editor = "ui_image", default = "UI/Hud/enemy_broken_cover", },
		{ category = "Icons", id = "ObstructedIcon", name = "Obstructured Icon", editor = "ui_image", default = "UI/Hud/obstructedHit", },
	},
	FrameBox = box(2, 0, 2, 0),
	ProgressFrameBox = box(2, 0, 2, 0),
	BindTo = {
		"WillPoints",
	},
	SecondaryBarsAlignment = {
		"right",
		"relative",
		"relative"
	},
	
	SqueezeY = false,
	prop_metas = false,
	MaxWidth = 100,

	barBox = false,
	bgBox = false,
	tempWpBgBox = false,
	primaryBarBox = false,
	primaryBarClipBox = false,
	tempWpBarBox = false,
	tempWpBarClipBox = false,
	
	otherBarBoxes = false,
	maxWpChangedBox = false,
	maxWpChangedBoxBg = false,
	maxWpChangedBgColor = false,
	
	predictionIconSrc = false,

	LayoutMethod = "Box",
	WpColor = false,
	TempWpColor = false,
	PotentialDamageColor = false,
	ConditionalDamageColor = false,
	
	secondary_bar_modifiers = false,
	idText = false,
	max_width_textless = false,
	max_height_textless = false,
	
	-- Wp loss anim
	Wp_loss_amount = false,
	Wp_loss_rect = false,
	Wp_loss_interp = false,
	Wp_loss_healing = false,
}

---
--- Sets the maximum width of the WillPoint bar.
---
--- @param val number The maximum width to set.
---
function WillPointBar:SetMaxWidth(val)
	self.max_width_textless = val
	XWindow.SetMaxWidth(self, self.idText and 9999 or val)
end

---
--- Sets the maximum height of the WillPoint bar.
---
--- @param val number The maximum height to set.
---
function WillPointBar:SetMaxHeight(val)
	self.max_height_textless = val
	XWindow.SetMaxHeight(self, self.idText and 9999 or val)
end

---
--- Sets the color preset for the WillPoint bar.
---
--- @param presetName string The name of the color preset to use. Can be "enemy", "disabled", "desaturated", or the default "".
---
function WillPointBar:SetColorPreset(presetName)
	if presetName == "enemy" then
		self.WpColor = RGB(156, 8, 218)
		self.TempWpColor = RGB(156, 8, 218)
		self.PotentialDamageColor = RGB(218, 156, 8)
		self.ConditionalDamageColor = RGB(255, 211, 106)
	elseif presetName == "disabled" then
		self.WpColor = GameColors.D
		self.TempWpColor = GameColors.PlayerLighter
		self.PotentialDamageColor = RGB(152, 249, 255)
		self.ConditionalDamageColor = RGB(255, 211, 106)
	elseif presetName == "desaturated" then
		self.WpColor = GameColors.K--GetColorWithAlpha(, 120)
		self.TempWpColor = GetColorWithAlpha(GameColors.K, 200)
		self.PotentialDamageColor = RGB(152, 249, 255)
		self.ConditionalDamageColor = RGB(255, 211, 106)
	else
		self.WpColor = RGB(156, 8, 218)
		self.TempWpColor = RGB(156, 8, 218)
		self.PotentialDamageColor = RGB(152, 249, 255)
		self.ConditionalDamageColor = RGB(255, 211, 106)
	end
	
	local shouldHaveText = presetName == "enemy" and not CthVisible()
	local hasText = self.idText
	if shouldHaveText and not hasText then
		local text = XTemplateSpawn("XText", self) 
		text:SetId("idText")
		text:SetTranslate(true)
		text:SetTextStyle("BadgeName")
		text:SetClip(false)
		text:SetUseClipBox(false)
		text:SetDrawOnTop(true)
		text:SetTextVAlign("center")
		text:SetHandleMouse(false)
		text:SetWordWrap(false)
		text:SetPadding(box(2, -3, 2, -3))
		text:SetText(self.context:HasMember("GetWillPointAsText") and self.context:GetWillPointAsText() or "")
		if self.window_state == "open" then text:Open() end
		
		self:SetMaxWidth(self.max_width_textless)
		self:SetMaxHeight(self.max_height_textless)
		self:SetHAlign("stretch")
	elseif not shouldHaveText and hasText then
		self.idText:Close()
		self.idText = false
		
		self:SetMaxWidth(self.max_width_textless)
		self:SetMaxHeight(self.max_height_textless)
		self:SetHAlign("left")
	end
end

---
--- Initializes the WillPointBar object.
--- Sets the color preset to "default" and initializes the `predictionIconSrc` table.
---
function WillPointBar:Init()
	self.predictionIconSrc = {}
	self:SetColorPreset("default")
end

---
--- Callback function that is called when the `BindTo` property of the `WillPointBar` object is set.
--- Ensures that the `Progress` property is a table of the same size as the `BindTo` property.
---
--- @param prop_id string The ID of the property that was set.
--- @param old_value any The previous value of the property.
---
function WillPointBar:OnXTemplateSetProperty(prop_id, old_value)
	if prop_id ~= "BindTo" then return end
	-- make sure the Progress property is a table of the same size
	local progress = self.Progress
	local progress_count = #progress
	local bind_count = #self.BindTo
	if bind_count ~= progress_count then
		local progress_meta = self:GetPropertyMetadata("Progress")
		--remove not needed Progress values
		for i = progress_count, bind_count + 1, -1 do
			progress[i] = nil
		end
		--add missing Progress values
		for i = progress_count + 1, bind_count do
			progress[i] = progress_meta.item_default or 0
		end
		self.Progress = progress
	end
end

---
--- Returns the maximum progress value from the `Progress` table.
---
--- @return number The maximum progress value, clamped between 0 and `MaxProgress`.
---
function WillPointBar:GetCurrentProgress()
	local current = 0
	for _, value in ipairs(self.Progress) do
		current = Max(current, value)
	end
	return Clamp(current, 0, self.MaxProgress)
end

---
--- Adjusts the size of the WillPointBar based on the current progress.
---
--- @param max_width number The maximum width of the WillPointBar.
--- @param max_height number The maximum height of the WillPointBar.
--- @return number, number The adjusted width and height of the WillPointBar.
---
function WillPointBar:MeasureSizeAdjust(max_width, max_height)
	local progress = self:GetCurrentProgress()
	local min = ScaleXY(self.scale, self.MinProgressSize)
	if progress == 0 then return max_width, max_height end
	max_width = min + (max_width - min) * progress / self.MaxProgress
	return max_width, max_height
end

---
--- Sets the bounding box of the WillPointBar and updates the bar visualization.
---
--- @param x number The x-coordinate of the bounding box.
--- @param y number The y-coordinate of the bounding box.
--- @param width number The width of the bounding box.
--- @param height number The height of the bounding box.
--- @param move_children boolean If true, the children of the WillPointBar will also be moved.
---
function WillPointBar:SetBox(x, y, width, height, move_children)
	XFrame.SetBox(self, x, y, width, height, move_children)
	self:UpdateBars()
end

local baseWpSegment = 15
local margins = 1
local distanceBetweenSegments = 1

---
--- Updates the visual representation of the WillPoint bar based on the current progress.
---
--- This function is responsible for setting the size and position of the various elements that make up the WillPoint bar,
--- such as the primary WillPoint bar, temporary WillPoint bar, and any additional secondary bars. It also handles clipping
--- the bars to the current WillPoint values and updating the background box.
---
--- @param self WillPointBar The WillPointBar instance.
---
function WillPointBar:UpdateBars()
	if not IsKindOfClasses(self.context, "CombatObject", "UnitData") then return end
	
	if self.idText then
		self.idText:SetText(self.context:HasMember("GetWillPointAsText") and self.context:GetWillPointAsText() or "")
	end
	
	local b = self.box
	local minx = b:minx()
	local miny = b:miny()
	local width = b:sizex()
	local height = b:sizey()
	if width == 0 then return end -- Wait for layout
	self.barBox = b
	
	-- Margins
	minx = minx + margins
	width = width - margins * 2
	height = height - margins * 2
	miny = miny + margins
	
	local frameBoxX = 0--(--self.ProgressFrameBox:minx() / 2) + 2
	local frameBoxWidth = 0--(self.ProgressFrameBox:maxx() / 2) + 2
	local horizontalFrameBoxSize = frameBoxX + frameBoxWidth
	
	local unitCurrentWp = self.context.WillPoints
	local unitMaxWp
	if self.context:HasMember("GetModifiedMaxWillPoints") then
		local _, positive_modifier_max = self.context:GetModifiedMaxWillPoints()
		unitMaxWp = positive_modifier_max
	else
		unitMaxWp = self.context.MaxWillPoints
	end
	
	-- if unit has wounds
	local unitCurrentMaxWp = self.context.MaxWillPoints
	if unitCurrentMaxWp > unitMaxWp then 
		unitMaxWp = unitCurrentMaxWp
	end
	
	-- The segments are (baseWpSegment) large
	local primarySegments = Max((unitMaxWp - 1), 1) / baseWpSegment + 1
	
	-- TempWp Segment count
	local unitTempWp =  0
	local unitCombinedMaxWp = unitMaxWp
	local tempWpSegments = 0
	if unitTempWp and unitTempWp > 0 then
		tempWpSegments = Max((unitTempWp - 1), 1) / baseWpSegment + 1
		unitCombinedMaxWp = self.FitSegments and unitMaxWp + unitTempWp or unitMaxWp
	end
	
	self:SetMaxProgress(unitCombinedMaxWp)

	-- all segments
	local segments = self.FitSegments and primarySegments + tempWpSegments or primarySegments
	local segmentSpacing = segments > 1 and segments * distanceBetweenSegments or 0
	local extraWpAmount = unitCombinedMaxWp - baseWpSegment * segments
	if extraWpAmount > 0 then segmentSpacing = segmentSpacing + distanceBetweenSegments end
	local effectiveSize = width - segmentSpacing
	
	-- segmentSizeMod changes when you want to fit all the segments in the width
	local segmentSizeMod
	if self.FitSegments then
		if unitCurrentWp + unitTempWp >= unitMaxWp then
			segmentSizeMod = unitCurrentWp + unitTempWp
		else
			segmentSizeMod = unitMaxWp
		end
	else
		segmentSizeMod = unitCombinedMaxWp
	end	
	
	local segmentPixelSize = Max(DivCeil(effectiveSize * baseWpSegment, segmentSizeMod), 1)
	
	-- The primary bar extends from the left in segments.
	local push = 0
	self.primaryBarBox = {}
	for i = 1, primarySegments do
		self.primaryBarBox[i] = sizebox(minx + push, miny, segmentPixelSize, height)
		push = push + segmentPixelSize + distanceBetweenSegments
	end
	
	-- Clip segments to current Wp
	local primary = self.Progress[1]
	local primaryBarWidth = primary > 0 and MulDivRound(width, primary, segmentSizeMod) or 0
	self.primaryBarClipBox = sizebox(minx, miny, primaryBarWidth, height)
	
	local border = self.BorderWidth
	self.bgBox = sizebox(minx - border, miny - border, width + border * 2, height + border * 2)
	
	-- TempWp segments go here
	self.tempWpBarBox = {}
	self.tempWpBarClipBox = false
	self.tempWpBgBox = false
	local tempBarWidth = 0
	if unitTempWp and unitTempWp > 0 then
		-- tempWp segments are a bit bigger
		local tempWpSegmentXpos = minx + primaryBarWidth
		local tempWpSegmentYpos = self.FitSegments and miny or (miny - 1)
		local tempWpSegmentHeight = self.FitSegments and height or (height + 2)
		
		push = distanceBetweenSegments
		
		for i = 1, tempWpSegments do
			self.tempWpBarBox[i] = sizebox(tempWpSegmentXpos + push, tempWpSegmentYpos, segmentPixelSize, tempWpSegmentHeight)
			push = push + segmentPixelSize + distanceBetweenSegments
		end
		
		-- clip temp Wp
		tempBarWidth = MulDivRound(width, unitTempWp, segmentSizeMod) or 0
		
		if self.FitSegments and tempWpSegmentXpos + tempBarWidth > minx + width then
			tempBarWidth = minx + width - tempWpSegmentXpos
		end
		
		self.tempWpBarClipBox = sizebox(tempWpSegmentXpos, tempWpSegmentYpos, tempBarWidth, tempWpSegmentHeight)
		self.tempWpBgBox = sizebox(tempWpSegmentXpos, tempWpSegmentYpos, tempBarWidth, tempWpSegmentHeight)
	end
	
	-- If the unit's current max Wp is less than the initial, display another bar on the right side.
	-- The bar background is equal to the initial maximum.
	local currentMax = self.context.MaxWillPoints
	if unitMaxWp == currentMax then
		self.maxWpChangedBox = false
	else
		local lostMaxWp = unitMaxWp - currentMax
		local barSize = MulDivRound(width, lostMaxWp, segmentSizeMod)
		barSize = Min(barSize, width) -- Dont overflow
		local fullRightSide = minx + width - barSize
		
		if self.FitSegments then
			barSize = barSize + margins
		end
		
		local _, padding = ScaleXY(self.scale, 0, 2)
		self.maxWpChangedBox = sizebox(fullRightSide, miny + padding, barSize, height - padding * 2)
		
		if self.FitSegments then
			self.maxWpChangedBoxBg = sizebox(fullRightSide, miny + padding / 2, barSize, height)
			self.bgBox = box(self.bgBox:minx(), self.bgBox:miny(), self.bgBox:maxx() - barSize, self.bgBox:maxy())
		else
			self.maxWpChangedBoxBg = false
		end
	end
	
	-- Wp loss
	if self.Wp_loss_amount then
		local isHealing = self.Wp_loss_healing
		if isHealing then
			local gainInWidth = self.Wp_loss_amount < 0 and MulDivRound(width, -self.Wp_loss_amount, segmentSizeMod) or self.Wp_loss_amount
			self.Wp_loss_rect = sizebox(self.primaryBarClipBox:maxx() - gainInWidth, self.bgBox:miny(), gainInWidth, self.bgBox:sizey())
		else
			local lossInWidth = self.Wp_loss_amount > 0 and MulDivRound(width, self.Wp_loss_amount, segmentSizeMod) or self.Wp_loss_amount
			self.Wp_loss_rect = sizebox(self.primaryBarClipBox:maxx(), self.bgBox:miny(), lossInWidth, self.bgBox:sizey())
		end
	end
	
	-- Other bars anchored right on the primary (and tempWp if any), minus missing.
	local rightSide = minx + primaryBarWidth
	if unitTempWp and unitTempWp > 0 then rightSide = rightSide + tempBarWidth end
	
	if not self.otherBarBoxes then self.otherBarBoxes = {} end
	for i=2, #self.Progress do
		local value = self.Progress[i]
		local alignment = self.SecondaryBarsAlignment[i - 1]
		if alignment == "relative" and not self.otherBarBoxes[i - 1] then alignment = "right" end
		local barWidth = 0
		local barHeight = height
		if value > 0 then
			if self.BindTo[i] == "PotentialSecondaryConditional" then
				local modifiedHeight = MulDivRound(barHeight, 600, 1000)
				miny = miny + (barHeight - modifiedHeight) / 2
				barHeight = modifiedHeight
			end
		
			barWidth = MulDivRound(width, value, unitCombinedMaxWp)
			barWidth = Max(barWidth, horizontalFrameBoxSize) -- We want to show at least one pixel.
			if alignment == "right" then
				barWidth = Min(barWidth, primaryBarWidth)
				self.otherBarBoxes[i] = sizebox(rightSide - barWidth, miny, barWidth, barHeight)
			elseif alignment == "relative" then
				local start = self.otherBarBoxes[i - 1]:minx()
				local endR = self.otherBarBoxes[i - 1]:sizex()
				barWidth = Min(endR + barWidth, primaryBarWidth - endR)
				self.otherBarBoxes[i] = sizebox(start - barWidth, miny, barWidth + frameBoxWidth, barHeight)
			end
		else
			self.otherBarBoxes[i] = false
		end
	end
end

---
--- Updates the progress value for a specific index in the `WillPointBar` object.
---
--- @param context table The context object associated with the `WillPointBar` object.
--- @param idx integer The index of the progress value to update.
--- @param value number The new progress value.
---
function WillPointBar:OnPropUpdate(context, idx, value)
	assert(type(value) == "number")
	if type(value) == "number" then
		local progress = self.Progress
		progress[idx] = value
		self:InvalidateMeasure()
	end
end

---
--- Sets the property IDs that the `WillPointBar` object is bound to.
---
--- @param prop_ids table An array of property IDs that the `WillPointBar` object is bound to.
---
function WillPointBar:SetBindTo(prop_ids)
	self.prop_metas = self.prop_metas or {}
	self.BindTo = prop_ids
	for i, prop_id in ipairs(prop_ids) do
		local prop_meta
		ForEachObjInContext(self.context, function(obj, self, prop_id)
			prop_meta = prop_meta or IsKindOf(obj, "PropertyObject") and obj:GetPropertyMetadata(prop_id)
		end, self, prop_id)
		self.prop_metas[i] = prop_meta
	end
end

---
--- Updates the `WillPointBar` object's context and progress values.
---
--- This function is called when the `WillPointBar` object's context is updated. It retrieves the
--- values for the properties the `WillPointBar` object is bound to, and updates the progress
--- values accordingly. It then calls the `UpdateBars()` function to update the visual
--- representation of the WillPoint bar.
---
--- @param context table The updated context object associated with the `WillPointBar` object.
---
function WillPointBar:OnContextUpdate(context)
	XContextControl.OnContextUpdate(self, context)

	local prop_ids = self.BindTo
	local values = {}
	for i, prop_id in ipairs(prop_ids) do
		if context then
			local value = ResolveValue(context, prop_id) or 0
			values[i] = value
			if value ~= rawget(self.Progress, i) then
				self:OnPropUpdate(context, i, value)
			end
		end
	end

	--print("WillBar context:", self.context and self.context.session_id, self.Progress[1])
	self:UpdateBars()
end

local function lSecondaryBarAnimation(self, mod)
	local setting_name = "ConditionalDamage"
	local fade_in, fade_out

	fade_in = {
		id = "conditional_damage_in",
		type = const.intAlpha,
		startValue = 0,
		endValue = 255,
		duration = const.Healthbar[setting_name .. "FadeInTime"],
		flags = const.intfRealTime,
		on_complete = function()
			Sleep(const.Healthbar[setting_name .. "TimeOn"])
			self.secondary_bar_modifiers = lSecondaryBarAnimation(self, fade_out)
		end
	}

	fade_out = {
		id = "conditional_damage_out",
		type = const.intAlpha,
		startValue = 255,
		endValue = 0,
		duration = const.Healthbar[setting_name .. "FadeOutTime"],
		flags = const.intfRealTime,
		on_complete = function()
			Sleep(const.Healthbar[setting_name .. "TimeOff"])
			self.secondary_bar_modifiers = lSecondaryBarAnimation(self, fade_in)
		end
	}

	local int = mod or fade_out
	int.modifier_type = const.modInterpolation
	local time = GetPreciseTicks()
	int.start = time
	if int.autoremove or int.on_complete then
		assert(not IsFlagSet(int.flags or 0, const.intfGameTime))
		local time_to_end = int.start + int.duration - time
		CreateRealTimeThread(function(self, int, time_to_end)
			Sleep(time_to_end)
			if self.window_state == "destroying" then return end
			int.on_complete(self, int)
		end, self, int, time_to_end)
	end
	self:Invalidate()
	
	return int
end

---
--- Draws the background of the WillPoint bar.
--- This function is currently empty and does not perform any drawing.
---
function WillPointBar:DrawBackground(clip_box)
	return
end

local UIL = UIL
local irOutside = const.irOutside
---
--- Draws the content of the WillPoint bar, including the background, Wp bar, and prediction icons.
---
--- @param clip_box table The clipping box to use for drawing.
---
function WillPointBar:DrawContent(clip_box)
	if not self.barBox then return end
	
	if self.UseClipBox and self.box:Intersect2D(clip_box) == 0 then return end
 	
	if self.UseClipBox then
		UIL.PushClipRect(self.box)
	end
	
	local desaturation = UIL.GetDesaturation()
	UIL.SetDesaturation(self.Desaturation)
	
	if self.idText then 
		-- draw Wp to text with prediction icons
		self:DrawBGBox()
		XWindow.DrawChildren(self, clip_box)
		self:DrawPredictionIcons()
	else
		-- draw Wp bar with prediction icons
		if self:DrawBGBox() then
			-- TempWp border background
			if self.DisplayTempWp and self.tempWpBgBox then
				UIL.DrawSolidRect(self.tempWpBgBox, self:CalcBackground())
			end
		end
		self:DrawWpBar(clip_box)
		
		-- Draw Wp loss animation (used for DamageNotification)
		if self.Wp_loss_rect then
			local isHealing = self.Wp_loss_healing
		
			local prev_top_mod
			if self.Wp_loss_interp then
				if self.Wp_loss_interp.applied_box ~= self.Wp_loss_rect then
					local rectOffset = isHealing and self.Wp_loss_rect:max() or self.Wp_loss_rect:min()
				
					local ogRect = self.Wp_loss_interp.originalRect
					local tarRect = self.Wp_loss_interp.targetRect
					self.Wp_loss_interp.originalRect = Offset(ogRect, rectOffset - ogRect:min())
					self.Wp_loss_interp.targetRect = Offset(tarRect, rectOffset - tarRect:min())
					self.Wp_loss_interp.applied_box = self.Wp_loss_rect
				end
			
				prev_top_mod = UIL.ModifiersGetTop()
				UIL.PushModifier(self.Wp_loss_interp)
			end

			UIL.PushClipRect(self.Wp_loss_rect)
			UIL.DrawSolidRect(self.box, isHealing and RGB(78, 164, 200) or GameColors.M)
			for i, s in ipairs(self.primaryBarBox) do
				UIL.DrawSolidRect(s, isHealing and GameColors.C or GameColors.C)
			end
			UIL.PopClipRect(self.Wp_loss_rect)
			
			if prev_top_mod then UIL.ModifiersSetTop(prev_top_mod) end
		end
	end
	
	UIL.SetDesaturation(desaturation)
	
	if self.UseClipBox then
		UIL.PopClipRect()
	end
end

--override func  and call XWindow.DrawChildren before DrawPredictionIcons so that they are drawn on top of text
---
--- Draws the children of the WillPointBar UI element.
---
--- This function is called to render the child elements of the WillPointBar, such as prediction icons or other overlays.
---
--- @function WillPointBar:DrawChildren
--- @return nil
function WillPointBar:DrawChildren()
end

---
--- Draws the background box for the WillPointBar UI element.
---
--- This function is responsible for rendering the background box of the WillPointBar, including the border and background color.
---
--- @function WillPointBar:DrawBGBox
--- @return boolean Whether the background box was successfully drawn
function WillPointBar:DrawBGBox()
	local border = self.BorderWidth
	local borderColor = self:CalcBorderColor()
	local background = self:CalcBackground()
	if border ~= 0 and background ~= 0 then
		if background == borderColor then
			UIL.DrawSolidRect(self.bgBox, background)
		else
			UIL.DrawBorderRect(self.bgBox, border, border, borderColor, background)
		end
		return true
	end
end

---
--- Draws the Wp bar and related elements for the WillPointBar UI element.
---
--- This function is responsible for rendering the Wp bar, including the primary bar, temporary Wp bar, and any additional bars (e.g. for damage prediction). It also handles clipping and animation effects.
---
--- @function WillPointBar:DrawWpBar
--- @param clip_box table The clipping box to use for drawing the Wp bar
--- @return nil
function WillPointBar:DrawWpBar(clip_box)
	local border = self.BorderWidth
	local background = self:CalcBackground()
	local primary = self.Progress[1]
	
	-- Bar Background
--[[	local scaleX, scaleY = ScaleXY(self.scale, self.ImageScale:xy())
		UIL.DrawFrame(self.Image, self.barBox, self.Rows, self.Columns, self:GetRow(), self:GetColumn(),
			self.FrameBox, not self.TileFrame, self.TransparentCenter, scaleX, scaleY, self.FlipX, self.FlipY)
			
		if not primary then 
			UIL.SetDesaturation(desaturation)
			return
		end
		]]
		
	-- Wp bar segments
	if self.primaryBarClipBox then UIL.PushClipRect(self.primaryBarClipBox) end
	if self.primaryBarBox then
		for i, s in ipairs(self.primaryBarBox) do
			UIL.DrawSolidRect(s, self.WpColor)
		end
	end
	if self.primaryBarClipBox then UIL.PopClipRect() end
	
	-- Missing max Wp
	if self.maxWpChangedBox then
		if border ~= 0 and background ~= 0 and self.maxWpChangedBoxBg then
			UIL.DrawSolidRect(self.maxWpChangedBoxBg, self.maxWpChangedBgColor or background)
			UIL.DrawBorderRect(self.maxWpChangedBox, border + 3, border + 3, self:CalcBorderColor(), background)
		end
		UIL.PushClipRect(self.maxWpChangedBox)
		for i, s in ipairs(self.primaryBarBox) do
			UIL.DrawSolidRect(s, RGB(91, 91, 91))
		end
		UIL.PopClipRect()
	end
	
	-- TempWp
	if self.DisplayTempWp then
		if self.tempWpBarClipBox then UIL.PushClipRect(self.tempWpBarClipBox) end
		if self.tempWpBarBox then
			for i, s in ipairs(self.tempWpBarBox) do
				UIL.DrawSolidRect(s, self.TempWpColor)
			end
		end
		if self.tempWpBarClipBox then UIL.PopClipRect() end
	end
	
	-- Other bars (used for damage prediction currently)
--	if self.otherBarBoxes then
--		for i = 2, #self.Progress do
--			if self.otherBarBoxes[i] then
--				if not self.secondary_bar_modifiers then
--					self.secondary_bar_modifiers = lSecondaryBarAnimation(self)
--				end
--				local prev_top_mod = UIL.ModifiersGetTop()
--				UIL.PushModifier(self.secondary_bar_modifiers)
--				
--				local color = i == 2 and self.PotentialDamageColor or self.ConditionalDamageColor
--				UIL.DrawSolidRect(self.otherBarBoxes[i], color)
--		
--				if prev_top_mod then
--					UIL.ModifiersSetTop(prev_top_mod)
--				end
--			end
--		end
--	end

	XWindow.DrawChildren(self, clip_box)
	self:DrawPredictionIcons()
end

---
--- Draws the prediction icons for the WillPoint bar.
--- This function is responsible for rendering the small and large potential damage icons on the WillPoint bar.
--- It checks if the icons are available and ready to be drawn, and then positions them appropriately on the WillPoint bar.
---
--- @param self WillPointBar The WillPoint bar object.
---
function WillPointBar:DrawPredictionIcons()
	-- Additional prediction icons
	local predictionIconSmall = rawget(self.context, "SmallPotentialDamageIcon")
	if predictionIconSmall == "InRange" then predictionIconSmall = false end
	local predictionIconLarge = rawget(self.context, "LargePotentialDamageIcon")
	if (predictionIconSmall or predictionIconLarge) and self.ShowIcons then
		local iconImageSmall = predictionIconSmall and self:GetProperty(predictionIconSmall) or predictionIconSmall
		local iconImageLarge = predictionIconLarge and self:GetProperty(predictionIconLarge) or predictionIconLarge

		local function lDrawIcon(iconImage, smallIcon)
			if UIL.IsImageReady(iconImage) then
				-- Get image size if we don't have it
				local src = self.predictionIconSrc[iconImage]
				if not src then
					local w, h = UIL.MeasureImage(iconImage)
					src = sizebox(0, 0, w, h)
					self.predictionIconSrc[iconImage] = src
				end
				local width, height = ScaleXY(self.scale, src:sizexyz())
				local b = self.barBox
				local xPos = (b:minx() + b:sizex() / 2) - width / 2
				-- Small icons are positioned after the back, large icons are in the middle of the bar.
				if smallIcon then
					xPos = b:maxx()
				end
				local iconDst = sizebox(xPos, (b:miny() + b:sizey() / 2) - height / 2, width, height)
				UIL.DrawFrame(iconImage, iconDst, 1, 1, 1, 1, empty_box, true, false, self.scale:x(), self.scale:y())
			else
				UIL.RequestImage(iconImage)
			end
		end
		if iconImageSmall then lDrawIcon(iconImageSmall, true) end
		if iconImageLarge then lDrawIcon(iconImageLarge) end
	end
end

-- Wp loss animation

---
--- Prepares the animation for Wp loss on the WillPoint bar.
---
--- This function is responsible for setting up the necessary state for animating the Wp loss on the WillPoint bar. It updates the `Wp_loss_amount` variable with the provided amount, and resets the `Wp_loss_rect` and `Wp_loss_interp` variables. It also sets a flag `Wp_loss_healing` to indicate whether the Wp loss is actually a healing amount.
---
--- @param self WillPointBar The WillPoint bar object.
--- @param amount number The amount of Wp loss to animate.
--- @return number The total Wp loss amount.
---
function WillPointBar:PrepareAnimateWpLoss(amount)
	self.Wp_loss_amount = (self.Wp_loss_amount or 0) + amount
	self:DeleteThread("animateWpLoss")
	self.Wp_loss_rect = false
	self.Wp_loss_interp = false
	self.Wp_loss_healing = self.Wp_loss_amount < 0
	return self.Wp_loss_amount
end

---
--- Animates the Wp loss on the WillPoint bar.
---
--- This function is responsible for setting up the necessary state for animating the Wp loss on the WillPoint bar. It creates an interpolation object to animate the Wp loss rect, and starts a thread to reset the Wp loss state after the animation is complete.
---
--- @param self WillPointBar The WillPoint bar object.
--- @param time number The duration of the Wp loss animation in milliseconds.
---
function WillPointBar:AnimateWpLoss(time)
	self:DeleteThread("animateWpLoss")
	self.Wp_loss_interp = {
		interpolate_clip = const.interpolateClipOnly,
		id = "Wp_loss_interp",
		type = const.intRect,
		modifier_type = const.modInterpolation,
		start = GetPreciseTicks(),
		duration = time,
		targetRect = box(0, 0, 0, 1000),
		originalRect = box(0, 0, 1000, 1000),
		flags = band(const.intfInverse, const.intfRealTime)
	}
	
	self:CreateThread("animateWpLoss", function()
		Sleep(time)
		self.Wp_loss_rect = false
		self.Wp_loss_amount = false
		self.Wp_loss_interp = false
	end)
	
	self:Invalidate()
end


function DamageNotificationPopup:AnimateDamageTaken(dmg)
	local isHealing = dmg < 0
	
	local hudMerc = self.idHudMerc
	local container = hudMerc.idContent
	local bottomPart = hudMerc.idBottomPart
	bottomPart:SetBackground(isHealing and RGB(41, 61, 79) or GameColors.N)
	hudMerc.idName:SetTextStyle("PDAMercNameCard_Blue")

	local background = self.idHudMerc.idBackground
	background:SetBackground(isHealing and RGB(41, 61, 79) or GameColors.M)
	background:SetBackgroundRectGlowColor(isHealing and RGB(41, 61, 79) or GameColors.M)

	local hpBar = self.idHudMerc.idBar
    --local wpBar = self.idHudMerc.idWillBar
	local damageText = self.idHudMerc.idDamageText
	damageText:SetTextStyle(isHealing and "PDAMercNameCard_DamageHealed" or "PDAMercNameCard_DamageTaken")
	
	local portrait = hudMerc.idPortrait
	portrait:SetDesaturation(isHealing and 0 or 255)
	portrait:SetTransparency(isHealing and 80 or 125)
	portrait:SetUIEffectModifierId(isHealing and "UIFX_Portrait_Heal" or "UIFX_Portrait_Damage")
	
	dmg = dmg or 0
	damageText:SetVisible(self.visible)
	
	self:DeleteThread("animation")
	self:CreateThread("animation", function()
		hpBar:OnContextUpdate(hpBar.context)
		local amount = hpBar:PrepareAnimateHPLoss(dmg)
		damageText:SetText(T{711949015241, "<numberWithSign(amount)>", amount = -amount})
		
		hpBar:UpdateBars()
        --wpBar:UpdateBars()
		RunWhenXWindowIsReady(hpBar, function()
			damageText:SetBox(
				hpBar.hp_loss_rect:minx() - damageText.measure_width / 2 + hpBar.hp_loss_rect:sizex() / 2,
				hpBar.hp_loss_rect:miny() - damageText.measure_height,
				damageText.measure_width,
				damageText.measure_height
			)
		end)
		
		self.visible = true
		damageText:SetVisible(self.visible)
		
		Sleep(1200)
		hpBar:AnimateHPLoss(500)
        --wpBar:AnimateHPLoss(500)
		
		Sleep(500)
		self:delete()
	end)
end


function OnMsg.CombatEnd()

	local units = g_Units
	units = table.ifilter(units, function(k, v)
		return v.HireStatus ~= "Dead"
	end)
	
	

	for _, unit in ipairs(g_Units) do
		unit.WillPoints = unit.MaxWillPoints
		local player_team = unit.player_team and unit.team

		if not IsMerc(unit) and (#GetAllAlliedUnits(unit) <= CurrentModOptions.ShowLastEnemy) then
			unit:RevealTo(player_team)
			unit.innerInfoRevealed = true
		end

	end

end

function OnMsg.TurnEnd()

	local units = g_Units
	units = table.ifilter(units, function(k, v)
		return v.HireStatus ~= "Dead"
	end)
	
	

	for _, unit in ipairs(g_Units) do
		local player_team = unit.player_team and unit.team

		if not isMerc(unit) and (#GetAllAlliedUnits(unit) <= CurrentModOptions.ShowLastEnemy) then
			unit:RevealTo(player_team)
			unit.innerInfoRevealed = true
		end

	end

end

--function OnMsg.CombatStart()
--
--	local units = g_Units
--	units = table.ifilter(units, function(k, v)
--		return v.HireStatus ~= "Dead"
--	end)
--
--	for _, unit in ipairs(units) do
--		unit.WillPoints = unit.MaxWillPoints
--	end
--end
