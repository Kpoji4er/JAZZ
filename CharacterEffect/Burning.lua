UndefineClass('Burning')
DefineClass.Burning = {
	__parents = { "CharacterEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "CharacterEffect",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function (self, target)
				local chance = 50 - Max(0, target.Health - 50) / 2 - MulDivRound(target:GetLevel(), 25, 10)
				--if target:Random(100) < chance then
				--	target:AddStatusEffect("Panicked")
				--end
				
				local willPointsDamage = 20
				
				target.WillPoints = target.WillPoints - willPointsDamage
				target:ApplySuppressionStatus()
				PlayVoiceResponse(target, "Pain")
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnEndTurn",
			Handler = function (self, target)
				if not target:IsDead() then
					EnvEffectBurningTick(target, nil, "end turn")
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnUnitBandaged",
			Handler = function (self, target, healer, patient, hp_restored)
				if target == patient then
					local voxels = target:GetVisualVoxels()
					local fire, dist = AreVoxelsInFireRange(voxels)
					if not fire or dist >= const.SlabSizeX then
						target:RemoveStatusEffect(self.class)
					end
				end
			end,
		}),
	},
	Modifiers = {
		PlaceObj('UnitModifier', {
			mod_add = -15,
			target_prop = "Wisdom",
		}),
	},
	DisplayName = T(178364189448, "Горение"),
	Description = T(661121942943, "Этот персонаж может <em>запаниковать</em> и будет <em>получать <damage> ед. урона</em> в конце каждого хода, пока не выйдет из области горения. <em>Перевязка</em> мгновенно снимает этот эффект."),
	AddEffectText = T(251545639918, "<em><DisplayName></em> горит"),
	OnAdded = function (self, obj)
		PlayFX("UnitBurning", "start", obj)
		self:SetParameter("burning_start_time", GameTime())
		obj:AddStain("Burning", GetRandomStainSpot())
	end,
	OnRemoved = function (self, obj)
		if IsKindOf(obj, "Unit") then
			PlayFX("UnitBurning", "end", obj)
			obj:ClearStains("Burning")
		end
	end,
	type = "Debuff",
	Icon = "UI/Hud/Status effects/burning",
	RemoveOnSatViewTravel = true,
	RemoveOnCampaignTimeAdvance = true,
	Shown = true,
	HasFloatingText = true,
}

