UndefineClass('UnitPropertiesStats')
DefineClass.UnitPropertiesStats = {
	__parents = { "PropertyObject", "Modifiable", },
	__generated_by_class = "ClassDef",

	properties = {
		{ category = "Stats", id = "Health", name = T(561192724204, --[[ClassDef Zulu UnitPropertiesStats name]] "Health"), help = T(755618869033, --[[ClassDef Zulu UnitPropertiesStats help]] "Represents both the physical well-being of a merc and the amount of damage they can take before becoming downed."), 
			editor = "number", default = 60, template = true, slider = true, min = 0, max = 100, modifiable = true, },
		{ category = "Stats", id = "Agility", name = T(427915460935, --[[ClassDef Zulu UnitPropertiesStats name]] "Agility"), help = T(313570226997, --[[ClassDef Zulu UnitPropertiesStats help]] "Measures how well a merc reacts physically to a new situation. Affects the total amount of AP, free movement at start of turn, and how stealthy the merc is."), 
			editor = "number", default = 60, template = true, slider = true, min = 0, max = 100, modifiable = true, },
		{ category = "Stats", id = "Dexterity", name = T(460461870476, --[[ClassDef Zulu UnitPropertiesStats name]] "Dexterity"), help = T(485643076124, --[[ClassDef Zulu UnitPropertiesStats help]] "Measures a merc's ability to perform delicate or precise movements correctly. Affects bonus from aiming and Stealth Kill chance."), 
			editor = "number", default = 60, template = true, slider = true, min = 0, max = 100, modifiable = true, },
		{ category = "Stats", id = "Strength", name = T(736846833602, --[[ClassDef Zulu UnitPropertiesStats name]] "Strength"), help = T(790754099931, --[[ClassDef Zulu UnitPropertiesStats help]] "Represents muscle and brawn. It's particularly important in Melee combat, affects throwing range and the size of the personal inventory of the character."), 
			editor = "number", default = 60, template = true, slider = true, min = 0, max = 100, modifiable = true, },
		{ category = "Stats", id = "Wisdom", name = T(140562214443, --[[ClassDef Zulu UnitPropertiesStats name]] "Wisdom"), help = T(731447408225, --[[ClassDef Zulu UnitPropertiesStats help]] "Affects a merc's ability to learn from experience and training. Affects wilderness survival and the chance to notice hidden items and enemies."), 
			editor = "number", default = 60, template = true, slider = true, min = 0, max = 100, modifiable = true, },
        { category = "Stats", id = "Will", name = T(14056221444311, --[[ClassDef Zulu UnitPropertiesStats name]] "Сила Воли"), help = T(73144740822511, --[[ClassDef Zulu UnitPropertiesStats help]] "Влияет на сопротивление подавлению."), 
			editor = "number", default = 50, template = true, slider = true, min = 0, max = 100, modifiable = true, },
        { category = "Stats", id = "Leadership", name = T(693671613488, --[[ClassDef Zulu UnitPropertiesStats name]] "Leadership"), help = T(396825125419, --[[ClassDef Zulu UnitPropertiesStats help]] "Measures charm, respect and presence. Affects the rate for training militia and other mercs. Affects the chance for getting positive and negative Morale events."), 
			editor = "number", default = 60, template = true, slider = true, min = 0, max = 100, modifiable = true, },
		{ category = "Stats", id = "Marksmanship", name = T(616386794188, --[[ClassDef Zulu UnitPropertiesStats name]] "Marksmanship"), help = T(403638137917, --[[ClassDef Zulu UnitPropertiesStats help]] "Reflects a merc's ability to shoot accurately at any given target with a firearm."), 
			editor = "number", default = 60, template = true, slider = true, min = 0, max = 100, modifiable = true, },
		{ category = "Stats", id = "Mechanical", name = T(302186486914, --[[ClassDef Zulu UnitPropertiesStats name]] "Mechanical"), help = T(338853681186, --[[ClassDef Zulu UnitPropertiesStats help]] "Rates a merc's ability to repair damaged, worn-out or broken items and equipment. Important for lockpicking, machine handling and hacking electronic devices. Used for detecting and disarming non-explosive traps."), 
			editor = "number", default = 60, template = true, slider = true, min = 0, max = 100, modifiable = true, },
		{ category = "Stats", id = "Explosives", name = T(205333258567, --[[ClassDef Zulu UnitPropertiesStats name]] "Explosives"), help = T(767865457232, --[[ClassDef Zulu UnitPropertiesStats help]] "Determines a merc's ability to use grenades and other explosives and affects damage and mishap chance when using thrown items. Used for detecting and disarming explosive traps."), 
			editor = "number", default = 60, template = true, slider = true, min = 0, max = 100, modifiable = true, },
		{ category = "Stats", id = "Medical", name = T(295773259174, --[[ClassDef Zulu UnitPropertiesStats name]] "Medical"), help = T(249121777425, --[[ClassDef Zulu UnitPropertiesStats help]] "Represents a merc's medical knowledge and ability to heal the wounded."), 
			editor = "number", default = 60, template = true, slider = true, min = 0, max = 100, modifiable = true, },
        },
}

--- Returns a table of the unit's attribute properties.
---
--- The returned table contains the following properties:
--- - Health: Represents the unit's overall health and vitality.
--- - Agility: Measures a unit's ability to perform quick and nimble movements.
--- - Dexterity: Measures a unit's ability to perform delicate or precise movements correctly.
--- - Strength: Represents the unit's muscle and brawn.
--- - Wisdom: Affects the unit's ability to learn from experience and training.
---
--- @return table The unit's attribute properties.
function UnitPropertiesStats:GetAttributes()
	local result = self:GetProperties()
	result = table.ifilter(result, function(k, v)
		return v.id == "Health" or
					v.id == "Agility" or
					v.id == "Dexterity" or
					v.id == "Strength" or
					v.id == "Wisdom" or
					v.id == "Will"
	end)
	return result
end

--- Returns a table of the unit's skill properties.
---
--- The returned table contains the following properties:
--- - Marksmanship: Reflects a merc's ability to shoot accurately at any given target with a firearm.
--- - Mechanical: Rates a merc's ability to repair damaged, worn-out or broken items and equipment. Important for lockpicking, machine handling and hacking electronic devices. Used for detecting and disarming non-explosive traps.
--- - Explosives: Determines a merc's ability to use grenades and other explosives and affects damage and mishap chance when using thrown items. Used for detecting and disarming explosive traps.
--- - Medical: Represents a merc's medical knowledge and ability to heal the wounded.
--- - Leadership: Measures charm, respect and presence. Affects the rate for training militia and other mercs. Affects the chance for getting positive and negative Morale events.
---
--- @return table The unit's skill properties.
function UnitPropertiesStats:GetSkills()
	local result = self:GetProperties()
	result = table.ifilter(result, function(k, v)
		return v.id == "Marksmanship" or
					v.id == "Mechanical" or
					v.id == "Explosives" or
					v.id == "Medical"  or
					v.id == "Leadership"
	end)
	return result
end

function UnitProperties:GetInitialMaxWillPoints()
--    local mod = self:GetProperty("villain") and const.Combat.LieutenantHpMod or 100
    local mod = 100
	local maxhp = MulDivRound(self:GetProperty("Will"), mod, 100)
--	if HasPerk(self, "BeefedUp") then
--		maxhp = MulDivRound(maxhp, 100 + CharacterEffectDefs.BeefedUp:ResolveValue("bonus_health"), 100)
--	end
	return maxhp
end

UnitProperties.properties[#UnitProperties.properties+1] =
    { category = "Derived Stats", 
        id = "WillPoints",
        name = "Will Points", 
    	editor = "number", 
        default = -1, 
	    no_edit = true, 
        min = -1,
        max = 100, }

UnitProperties.properties[#UnitProperties.properties+1] = 
    { category = "Derived Stats", id = "MaxWillPoints", name = "Max Will Points", 
    editor = "number", default = 0, read_only = true, no_edit = true, template = true, }             


    function UnitProperties:GetModifiedMaxWillPoints()

        local buff = 5 * self:GetPersonalMorale()
        local maxwp = self:GetInitialMaxWillPoints() + buff
        local positive_mods_only = maxwp

       
        
  --      local idx = self:HasStatusEffect("Wounded")
   --     local effect = idx and self.StatusEffects[idx]
   --     if effect then
    --        local value = effect:ResolveValue("MaxWpReductionPerStack") or 0
     --       local maxreduce = effect:ResolveValue("MinMaxWp") or 0
    --        local min = MulDivRound(maxhp, maxreduce, 100)
    --        maxhp = Max(min, maxhp - effect.stacks * value)
    --    end
        return maxwp, positive_mods_only
    end    

function RecalcMaxWillPoints(unit) -- unit can be Unit or UnitData
--	local count = AdjustWoundsToHP(unit)
--	if count and count>0 then
--		local effect = unit:GetStatusEffect("Wounded")
--		local to_remove = effect.stacks - count
--		if to_remove>0 then
--			unit:RemoveStatusEffect("Wounded", to_remove)
--		end
--	end
	local maxwp = unit:GetModifiedMaxWillPoints()
	local prev_maxwp = unit.MaxWillPoints
	unit.MaxWillPoints = maxwp
	if maxwp > prev_maxwp then
		unit.WillPoints = unit.WillPoints + maxwp - prev_maxwp
	end
	unit.WillPoints = Min(unit.WillPoints, unit.MaxWillPoints)
	ObjModified(unit)
    return maxwp
end

function UnitData:InitDerivedProperties()
	self.MaxHitPoints = self:GetInitialMaxHitPoints()
    self.MaxWillPoints = self:GetInitialMaxWillPoints()
	self.HitPoints = self.MaxHitPoints
    self.WillPoints = self.MaxWillPoints
	self.GetMaxActionPoints = UnitProperties.GetMaxActionPoints
	self.ActionPoints = self:GetMaxActionPoints()
	
	self.Likes = table.copy(self.Likes)
	self.Dislikes = table.copy(self.Dislikes)
	
	if not self.Experience then
		local minXP = GetXPTable(self.StartingLevel)
		self.Experience = minXP
	end
end




function UnitMarker:SpawnObjects()
	if not self.UnitDataSpawnDefs or #self.UnitDataSpawnDefs < 1 then 
		return
	end
	
	-- Empty table is not allowed intentionally to prevent respawning on
	-- deleted unit object as some markers are not setup as "once".
	if self.objects and not self.AlwaysSpawn then return end
	if self.Trigger == "once" and self.last_spawned_objects then return end
	
	local pts =  GetReachablePositionsFromPos(self:GetPos(), 1)
	
	-- prepare template & session ids
	local session_id, template_idx = self:GenerateUnitIds()
	
	if pts and #pts > 0 then
		local idx = template_idx
		local spawnEntry = self.UnitDataSpawnDefs[idx]
		local unit_template_id = spawnEntry.UnitDataDefId
		local name = spawnEntry.Name
		local pos = pts[1]
		
		-- check for existing UnitData for this session_id, if the unit has died skip the spawn
		local unit_data = gv_UnitData and gv_UnitData[session_id]
		
		if unit_data and unit_data.HealPersistentOnSpawn and not unit_data:IsDead() then
			unit_data:RemoveAllStatusEffects()
			--Wounded and unconscious are not removed by Remove all status effect as they are character effects
			if unit_data.StatusEffects["Wounded"] then
				unit_data:RemoveStatusEffect("Wounded", "all")
			end
			if unit_data.StatusEffects["Unconscious"] then
				unit_data:RemoveStatusEffect("Unconscious", "all")
			end
			unit_data.HitPoints = unit_data.MaxHitPoints
            unit_data.WillPoints = unit_data.MaxWillPoints
		end
	
		if not (unit_data and unit_data:IsDead()) then
			-- If changing the template id of a unit we need to recreate the unit data.
			if unit_data and unit_data.class ~= unit_template_id then
				unit_data:delete()
				gv_UnitData[session_id] = false
			end
		
			pos:SetInvalidZ()
			local unit = SpawnUnit(unit_template_id,
				session_id,
				pos,
				self:GetAngle(),
				self.Groups,
				self)
				
			unit.sequential_banter = self.BantersSequential
			
			local approach_banters = {}
			table.iappend(approach_banters, self.ApproachedBanters)
			table.iappend(approach_banters, table.keys2(Presets.BanterDef[self.ApproachBanterGroup] or {}, "sorted"))
			unit.approach_banters = approach_banters
			unit.approach_banters_distance = self.ApproachRadius
			
			if name and name~="" then
				unit.Name = name
			end
			self.objects = { unit }
			ShowHideCollectionMarker.SpawnObjects(self)
			unit:SetSide(self.Side)
			unit.routine = self.Routine
			unit.routine_area = self.RoutineArea
			unit.routine_spawner = self
			unit.conflict_ignore = self.ConflictIgnore
			if self.Side == "neutral" and GameState.Conflict and unit:CanCower() then
				unit:TeleportToCower()
			end
			if self.kill_on_spawn then
				unit:SetCommand("Die")
			end
		end
	end
	
	if self.Persistent then
		self.unit_template_idx = template_idx
	end
	
	self.last_spawned_objects = true
	return self.objects
end


