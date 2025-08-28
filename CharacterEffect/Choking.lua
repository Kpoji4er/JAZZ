UndefineClass('Choking')
DefineClass.Choking = {
	__parents = { "CharacterEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "CharacterEffect",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function (self, target)
				if target:IsMerc() then
					PlayVoiceResponse(target, "GasAreaSelection")
				else
					PlayVoiceResponse(target, "AIGasAreaSelection")
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnEndTurn",
			Handler = function (self, target)
				if not target:IsDead() then
					EnvEffectToxicGasTick(target, nil, "end turn")
				end
			end,
		}),
	},
	DisplayName = T(720153419307, "Удушье"),
	Description = T(120652127957, "Этот персонаж будет <em>получать <damage> ед. урона</em> в конце своего хода. Также этот персонаж <em>теряет энергию</em>."),
	AddEffectText = T(478064574365, "<em><DisplayName></em> задыхается"),
	OnAdded = function (self, obj)
		self:SetParameter("choking_start_time", GameTime())
		if obj:IsMerc() then
			PlayVoiceResponse(obj, "GasAreaSelection")
		else
			PlayVoiceResponse(obj, "AIGasAreaSelection")
		end
	end,
	type = "Debuff",
	Icon = "UI/Hud/Status effects/choking",
	RemoveOnEndCombat = true,
	RemoveOnSatViewTravel = true,
	RemoveOnCampaignTimeAdvance = true,
	Shown = true,
	HasFloatingText = true,
}

