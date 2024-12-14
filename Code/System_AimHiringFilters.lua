if FirstLoad then
	AIMScreenFilters = false
	ChangeSpecialization()
end

function GetAIMScreenFilters()
	ChangeAIMPremiumState("active", 0)
	if AIMScreenFilters then
		return AIMScreenFilters
	end
	
	ChangeSpecialization()
	AIMScreenFilters = {}




	local Speclist = {};

	for i, Specialization in ipairs(Presets.MercSpecializations.Default) do
		if Specialization.id ~= "None" then
			table.insert(Speclist,Specialization)
		end
	end

--	print("testtesttest")
--	print(Speclist)

	for i, Specialization in ipairs(Speclist) do

		AIMScreenFilters[#AIMScreenFilters + 1] = {
			name = Specialization.name,
			nameString = string.lower(Specialization.id),
			func = function(item)
				return IsMetAIMMerc(item) and item.Specialization == Specialization.id
			end,
			id = i,
			premium = false,
			Specialization = i
		}

	end
	
	table.insert(AIMScreenFilters, {
		name = T(470357587467, "All"),
		nameString = "all",
		func = function(item) return IsMetAIMMerc(item) end,
		id = #AIMScreenFilters + 1
	})
	table.insert(AIMScreenFilters, {
		name = T(521536943297, "My Team [<PlayerMercCount()>]"),
		urlName = T(975990402542, "My%20Team"),
		nameString = "hired",
		func = function(item) return item.HireStatus == "Hired" end,
		id = #AIMScreenFilters + 1,
		hire = true,
	})


--	print(AIMScreenFilters[8])	
--	local noneId = table.find(AIMScreenFilters,nameString,"none")
--	print("noneId "..noneId)
--	table.remove(AIMScreenFilters,8)
--	print(AIMScreenFilters)

	return AIMScreenFilters
end



-- At the start of the game a fraction of the mercs are randomly set to offline.
function RandomizeOfflineMercs()
	local viableMercs = {}
	ForEachMerc(function(mId)
		local ud = gv_UnitData[mId]
		if ud.Affiliation == "AIM" and ud.DaysUntilOnline > 0 then
			table.insert(viableMercs, mId)
		end
	end)
	assert(#viableMercs > 0)
	
	-- Settings
	local offlineMercCount = #viableMercs / 4
	local chanceToGoOffline = 15
	local chanceIncreasePerLevel = 0
	
	local loop = 0
	local offlineSet = 0
	while offlineSet < offlineMercCount do
		for i, mId in ipairs(viableMercs) do
			local unitDataInstance = gv_UnitData[mId]
			local level = unitDataInstance:GetLevel()
			local chance = chanceToGoOffline + chanceIncreasePerLevel * (level - 1)
			local roll = BraidRandom(xxhash(Game.id, mId, loop), 0, 100)
			if roll <= chance then
				unitDataInstance:SetMessengerOnline(false)
				offlineSet = offlineSet + 1
			end
			if offlineSet == offlineMercCount then break end
		end
		loop = loop + 1
	end
	
	-- Unmark online mercs as automatically set online
	for i, mId in ipairs(viableMercs) do
		local ud = gv_UnitData[mId]
		if ud.MessengerOnline then
			ud.DaysUntilOnline = false
		end
	end
end