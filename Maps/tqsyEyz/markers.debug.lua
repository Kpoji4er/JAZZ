{
	{
		Groups = false,
		LootTableIds = {
			"RimvilleGlobeLoot",
		},
		handle = 282337280,
		items = {
			{
				editor_view_abridged = "if RimvilleGlobe_Opened",
				filter_type = "quest",
				reference_id = "FleatownGeneral",
				type = "QuestIsVariableBool",
				var = set( "RimvilleGlobe_Opened" ),
			},
		},
		map = "I-9 - Rimville",
		name = 'InventoryItemSpawn#280 "SECRET STASH"',
		path = "InventoryItemSpawn ",
		type = "InventoryItemSpawn",
	},
	{
		Groups = false,
		LootTableIds = {
			"LargeContainer_Exceptional",
		},
		handle = 512483328,
		map = "I-9 - Rimville",
		name = 'InventoryItemSpawn#328 "Locker"',
		path = "InventoryItemSpawn ",
		type = "InventoryItemSpawn",
	},
	{
		ApproachedBanters = {
			"RimvilleApproach_Thugs_BeforeSm_Intruders",
		},
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"RimvilleGuardsAll",
			"InsideGuardsAll",
			"ThugActor_2",
		},
		handle = 1001673415,
		items = {
			{
				editor_view_abridged = "if not SupportLuigi and not SupportNoOne",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set({
	SupportLuigi = false,
	SupportNoOne = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#415 (RimvilleGuardsAll, InsideGuardsAll, ThugActor_2)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		ApproachedBanters = {
			"RimvilleApproach_Blaubert_Any_Luigi",
			"RimvilleApproach_Blaubert_BeforeSm_Invited",
			"RimvilleApproach_Blaubert_BeforeSm_Intruders",
		},
		Groups = {
			"SmileyBoss",
		},
		handle = 1086731602,
		items = {
			{
				editor_view_abridged = "if not BossDead",
				filter_type = "quest",
				reference_id = "Smiley",
				type = "QuestIsVariableBool",
				var = set({
	BossDead = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#602 (SmileyBoss)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		ApproachedBanters = {
			"RimvilleApproach_Thugs_BeforeSm_Intruders",
		},
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"RimvilleGuardsAll",
			"InsideGuardsAll",
			"ThugActor_1",
		},
		handle = 1107653081,
		items = {
			{
				editor_view_abridged = "if not SupportLuigi and not SupportNoOne",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set({
	SupportLuigi = false,
	SupportNoOne = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#081 (RimvilleGuardsAll, InsideGuardsAll, ThugActor_1)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		BanterTriggerEffects = {
			PlaceObj('BanterHasPlayed', {
				Banters = {
					"RimvilleGlobeLock_quarrel",
				},
				WaitOver = true,
			}),
		},
		Groups = {
			"GlobeLogic",
		},
		handle = 1112158006,
		items = {
			{
				editor_view_abridged = "if not BossInvited",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set({
	BossInvited = false,
}),
			},
			{
				editor_view_abridged = "If any of banter(s) played: RimvilleGlobeLock_quarrel",
				filter_type = "banter",
				reference_id = "RimvilleGlobeLock_quarrel",
				type = "BanterHasPlayed",
			},
		},
		map = "I-9 - Rimville",
		name = "Position#006 (GlobeLogic)",
		path = "Position ",
		type = "Position",
	},
	{
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"LuigiAndJailbirds",
			"Jailbird",
		},
		handle = 1158868609,
		items = {
			{
				editor_view_abridged = "if LuigiSaved and not SupportBlaubert and not SupportNoOne",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set({
	LuigiSaved = true,
	SupportBlaubert = false,
	SupportNoOne = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#609 (LuigiAndJailbirds, Jailbird)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		BanterTriggerEffects = {
			PlaceObj('PlayBanterEffect', {
				Banters = {
					"12Chairs_InteractNecklaceFound",
				},
			}),
			PlaceObj('PlayBanterEffect', {
				Banters = {
					"12Chairs_InteractQuestGiven",
				},
				banterSequentialWaitFor = "BanterStart",
			}),
			PlaceObj('PlayBanterEffect', {
				Banters = {
					"12Chairs_InteractQuestNotGiven",
				},
				banterSequentialWaitFor = "BanterLineStart",
				searchInMap = true,
				searchInMarker = false,
			}),
		},
		Groups = {
			"12Chairs_ChairMarker",
		},
		handle = 1162093880,
		items = {
			{
				editor_view_abridged = "NearChair = true",
				filter_type = "quest",
				reference_id = "TheTwelveChairs",
				type = "QuestSetVariableBool",
				var = "NearChair",
			},
			{
				editor_view_abridged = "NearChair = false",
				filter_type = "quest",
				reference_id = "TheTwelveChairs",
				type = "QuestSetVariableBool",
				var = "NearChair",
			},
			{
				editor_view_abridged = "if not ChairPicked and not Completed and not FoundNecklace",
				filter_type = "quest",
				reference_id = "TheTwelveChairs",
				type = "QuestIsVariableBool",
				var = {
					ChairPicked = false,
					Completed = false,
					FoundNecklace = false,
				},
			},
			{
				editor_view_abridged = "if NumberChairsFound(TheTwelveChairs) >= TargetChairs(TheTwelveChairs) ",
				filter_type = "quest",
				reference_id = "TheTwelveChairs",
				type = "QuestIsVariableNum",
				var = "NumberChairsFound",
				var2 = "TargetChairs",
			},
			{
				editor_view_abridged = "ChairPicked = true",
				filter_type = "quest",
				reference_id = "TheTwelveChairs",
				type = "QuestSetVariableBool",
				var = "ChairPicked",
			},
			{
				editor_view_abridged = "if Given",
				filter_type = "quest",
				reference_id = "TheTwelveChairs",
				type = "QuestIsVariableBool",
				var = set( "Given" ),
			},
			{
				editor_view_abridged = "Quest TheTwelveChairs:NumberChairsFound =  100% from (NumberChairsFound + 1)",
				filter_type = "quest",
				reference_id = "TheTwelveChairs",
				type = "QuestSetVariableNum",
				var = "NumberChairsFound",
			},
			{
				editor_view_abridged = "Play banter(s): 12Chairs_InteractNecklaceFound",
				filter_type = "banter",
				reference_id = "12Chairs_InteractNecklaceFound",
				type = "PlayBanterEffect",
			},
			{
				editor_view_abridged = "Play banter(s): 12Chairs_InteractQuestGiven",
				filter_type = "banter",
				reference_id = "12Chairs_InteractQuestGiven",
				type = "PlayBanterEffect",
			},
			{
				editor_view_abridged = "Play banter(s): 12Chairs_InteractQuestNotGiven",
				filter_type = "banter",
				reference_id = "12Chairs_InteractQuestNotGiven",
				type = "PlayBanterEffect",
			},
		},
		map = "I-9 - Rimville",
		name = 'CustomInteractable#880 "Examine" (12Chairs_ChairMarker)',
		path = "CustomInteractable ",
		type = "CustomInteractable",
	},
	{
		ApproachedBanters = {
			"RimvilleApproach_Thugs_BeforeSm_Intruders",
		},
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"RimvilleGuardsAll",
			"InsideGuardsAll",
		},
		handle = 1190068466,
		items = {
			{
				editor_view_abridged = "if not SupportLuigi and not SupportNoOne",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set({
	SupportLuigi = false,
	SupportNoOne = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#466 (RimvilleGuardsAll, InsideGuardsAll)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		ApproachedBanters = {
			"RimvilleApproach_Thugs_BeforeSm_Intruders",
		},
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"RimvilleGuardsAll",
			"InsideGuardsAll",
		},
		handle = 1200812113,
		items = {
			{
				editor_view_abridged = "if not SupportLuigi and not SupportNoOne",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set({
	SupportLuigi = false,
	SupportNoOne = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#113 (RimvilleGuardsAll, InsideGuardsAll)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"LuigiAndJailbirds",
			"Jailbird",
		},
		handle = 1222468002,
		items = {
			{
				editor_view_abridged = "if LuigiSaved and not SupportBlaubert and not SupportNoOne",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set({
	LuigiSaved = true,
	SupportBlaubert = false,
	SupportNoOne = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#002 (LuigiAndJailbirds, Jailbird)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"RimvilleGuardsAll",
			"FrontGuardD",
		},
		handle = 1228362868,
		items = {
			{
				editor_view_abridged = "if not SupportLuigi and not SupportNoOne",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set({
	SupportLuigi = false,
	SupportNoOne = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#868 (RimvilleGuardsAll, FrontGuardD)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		BanterTriggerEffects = {
			PlaceObj('PlayBanterEffect', {
				Banters = {
					"RimvilleGlobeLock_success",
				},
				banterSequentialWaitFor = "BanterLineStart",
				searchInMap = true,
				searchInMarker = false,
			}),
			PlaceObj('PlayBanterEffect', {
				Banters = {
					"RimvilleGlobeLock_failure",
				},
				banterSequentialWaitFor = "BanterStart",
				searchInMap = true,
				searchInMarker = false,
			}),
		},
		Groups = {
			"GlobeStash",
		},
		handle = 1237444012,
		items = {
			{
				editor_view_abridged = "if RimvilleGlobe_Given",
				filter_type = "quest",
				reference_id = "FleatownGeneral",
				type = "QuestIsVariableBool",
				var = set( "RimvilleGlobe_Given" ),
			},
			{
				editor_view_abridged = "RimvilleGlobe_Opened = true",
				filter_type = "quest",
				reference_id = "FleatownGeneral",
				type = "QuestSetVariableBool",
				var = "RimvilleGlobe_Opened",
			},
			{
				editor_view_abridged = "Play banter(s): RimvilleGlobeLock_success",
				filter_type = "banter",
				reference_id = "RimvilleGlobeLock_success",
				type = "PlayBanterEffect",
			},
			{
				editor_view_abridged = "Play banter(s): RimvilleGlobeLock_failure",
				filter_type = "banter",
				reference_id = "RimvilleGlobeLock_failure",
				type = "PlayBanterEffect",
			},
		},
		map = "I-9 - Rimville",
		name = 'CustomInteractable#012 "Examine" (GlobeStash)',
		path = "CustomInteractable ",
		type = "CustomInteractable",
	},
	{
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"LuigiAndJailbirds",
			"Jailbird",
		},
		handle = 1245685096,
		items = {
			{
				editor_view_abridged = "if LuigiSaved and not SupportBlaubert and not SupportNoOne",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set({
	LuigiSaved = true,
	SupportBlaubert = false,
	SupportNoOne = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#096 (LuigiAndJailbirds, Jailbird)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		BanterTriggerEffects = {
			PlaceObj('PlayBanterEffect', {
				Banters = {
					"RimvilleThugMale_01",
					"RimvilleThugMale_04",
					"RimvilleThugMale_15",
				},
				searchInMap = true,
				searchInMarker = false,
			}),
		},
		Groups = false,
		handle = 1260945171,
		items = {
			{
				editor_view_abridged = "Play banter(s): RimvilleThugMale_01, RimvilleThugMale_04, RimvilleThugMale_15",
				filter_type = "banter",
				reference_id = "RimvilleThugMale_01",
				type = "PlayBanterEffect",
			},
			{
				editor_view_abridged = "Play banter(s): RimvilleThugMale_01, RimvilleThugMale_04, RimvilleThugMale_15",
				filter_type = "banter",
				reference_id = "RimvilleThugMale_04",
				type = "PlayBanterEffect",
			},
			{
				editor_view_abridged = "Play banter(s): RimvilleThugMale_01, RimvilleThugMale_04, RimvilleThugMale_15",
				filter_type = "banter",
				reference_id = "RimvilleThugMale_15",
				type = "PlayBanterEffect",
			},
		},
		map = "I-9 - Rimville",
		name = "Position#171 DoorTrigger",
		path = "Position DoorTrigger",
		type = "Position",
	},
	{
		ApproachedBanters = {
			"RimvilleApproach_Thugs_BeforeSm_Intruders",
		},
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"RimvilleGuardsAll",
			"InsideGuardsAll",
		},
		handle = 1353828358,
		items = {
			{
				editor_view_abridged = "if not SupportLuigi and not SupportNoOne",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set({
	SupportLuigi = false,
	SupportNoOne = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#358 (RimvilleGuardsAll, InsideGuardsAll)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"RimvilleGuardsAll",
			"FrontGuardC",
		},
		handle = 1384222764,
		items = {
			{
				editor_view_abridged = "if not SupportLuigi and not SupportNoOne",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set({
	SupportLuigi = false,
	SupportNoOne = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#764 (RimvilleGuardsAll, FrontGuardC)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		ApproachedBanters = {
			"RimvilleApproach_Mollie_AfterSm_SmileyDead",
			"RimvilleApproach_Mollie_AfterSm_SmileyLeft",
			"RimvilleApproach_Mollie_BeforeSm_BossDead",
		},
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"SmileyBoss",
		},
		handle = 1408494420,
		items = {
			{
				editor_view_abridged = "if not MollieDead and not Mollie_return",
				filter_type = "quest",
				reference_id = "Smiley",
				type = "QuestIsVariableBool",
				var = set({
	MollieDead = false,
	Mollie_return = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#420 (SmileyBoss)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"LuigiAndJailbirds",
		},
		handle = 1411440944,
		items = {
			{
				editor_view_abridged = "if LuigiSaved and not SupportBlaubert and not SupportNoOne",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set({
	LuigiSaved = true,
	SupportBlaubert = false,
	SupportNoOne = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#944 (LuigiAndJailbirds)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		ApproachedBanters = {
			"RimvilleApproach_Thugs_BeforeSm_Intruders",
		},
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"RimvilleGuardsAll",
			"InsideGuardsAll",
		},
		handle = 1435988902,
		items = {
			{
				editor_view_abridged = "if not SupportLuigi and not SupportNoOne",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set({
	SupportLuigi = false,
	SupportNoOne = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#902 (RimvilleGuardsAll, InsideGuardsAll)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		ApproachedBanters = {
			"RimvilleApproach_Thugs_BeforeSm_Intruders",
		},
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"RimvilleGuardsAll",
			"InsideGuardsAll",
		},
		handle = 1454322112,
		items = {
			{
				editor_view_abridged = "if not SupportLuigi and not SupportNoOne",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set({
	SupportLuigi = false,
	SupportNoOne = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#112 (RimvilleGuardsAll, InsideGuardsAll)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		Groups = {
			"SmileyBoss",
		},
		handle = 1457491451,
		items = {
			{
				editor_view_abridged = "if LaBouePartDone and not MollieDead and not Mollie_return",
				filter_type = "quest",
				reference_id = "Smiley",
				type = "QuestIsVariableBool",
				var = {
					LaBouePartDone = true,
					MollieDead = false,
					Mollie_return = false,
				},
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#451 (SmileyBoss)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"RimvilleGuardsAll",
			"FrontGuardA",
		},
		handle = 1545305678,
		items = {
			{
				editor_view_abridged = "if not SupportLuigi and not SupportNoOne",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set({
	SupportLuigi = false,
	SupportNoOne = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#678 (RimvilleGuardsAll, FrontGuardA)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"LuigiAndJailbirds",
			"Jailbird",
		},
		handle = 1572657777,
		items = {
			{
				editor_view_abridged = "if LuigiSaved and not SupportBlaubert and not SupportNoOne",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set({
	LuigiSaved = true,
	SupportBlaubert = false,
	SupportNoOne = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#777 (LuigiAndJailbirds, Jailbird)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"RimvilleGuardsAll",
			"FrontGuardB",
		},
		handle = 1620248061,
		items = {
			{
				editor_view_abridged = "if not SupportLuigi and not SupportNoOne",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set({
	SupportLuigi = false,
	SupportNoOne = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#061 (RimvilleGuardsAll, FrontGuardB)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		ApproachedBanters = {
			"RimvilleApproach_Thugs_BeforeSm_Intruders",
		},
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"RimvilleGuardsAll",
			"InsideGuardsAll",
		},
		handle = 1647633857,
		items = {
			{
				editor_view_abridged = "if not SupportLuigi and not SupportNoOne",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set({
	SupportLuigi = false,
	SupportNoOne = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#857 (RimvilleGuardsAll, InsideGuardsAll)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		ApproachedBanters = {
			"RimvilleApproach_Thugs_BeforeSm_Intruders",
		},
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"RimvilleGuardsAll",
			"InsideGuardsAll",
		},
		handle = 1712255307,
		items = {
			{
				editor_view_abridged = "if not SupportLuigi and not SupportNoOne",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set({
	SupportLuigi = false,
	SupportNoOne = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#307 (RimvilleGuardsAll, InsideGuardsAll)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"RimvilleGuardsAll",
			"FrontGuardD",
		},
		handle = 1722199123,
		items = {
			{
				editor_view_abridged = "if not SupportLuigi and not SupportNoOne",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set({
	SupportLuigi = false,
	SupportNoOne = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#123 (RimvilleGuardsAll, FrontGuardD)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		ApproachedBanters = {
			"LuigiBoss_01_approach",
			"LuigiBoss_02_approach",
		},
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"LuigiAndJailbirds",
		},
		handle = 1759269675,
		items = {
			{
				editor_view_abridged = "if LuigiSaved",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set( "LuigiSaved" ),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#675 (LuigiAndJailbirds)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"LuigiAndJailbirds",
			"Jailbird",
		},
		handle = 1787385139,
		items = {
			{
				editor_view_abridged = "if LuigiSaved and not SupportBlaubert and not SupportNoOne",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set({
	LuigiSaved = true,
	SupportBlaubert = false,
	SupportNoOne = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#139 (LuigiAndJailbirds, Jailbird)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		ApproachedBanters = {
			"RimvilleApproach_Thugs_BeforeSm_Intruders",
		},
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"RimvilleGuardsAll",
			"InsideGuardsAll",
		},
		handle = 1791817653,
		items = {
			{
				editor_view_abridged = "if not SupportLuigi and not SupportNoOne",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set({
	SupportLuigi = false,
	SupportNoOne = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#653 (RimvilleGuardsAll, InsideGuardsAll)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"LuigiAndJailbirds",
			"Jailbird",
		},
		handle = 1814020843,
		items = {
			{
				editor_view_abridged = "if LuigiSaved and not SupportBlaubert and not SupportNoOne",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set({
	LuigiSaved = true,
	SupportBlaubert = false,
	SupportNoOne = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#843 (LuigiAndJailbirds, Jailbird)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		BanterGroups = {
			"Banters_Civilians",
			"Banters_Local_Fleatown",
		},
		Groups = {
			"RimvilleGuardsAll",
			"FrontGuardD",
		},
		handle = 1857219886,
		items = {
			{
				editor_view_abridged = "if not SupportLuigi and not SupportNoOne",
				filter_type = "quest",
				reference_id = "Luigi",
				type = "QuestIsVariableBool",
				var = set({
	SupportLuigi = false,
	SupportNoOne = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "UnitMarker#886 (RimvilleGuardsAll, FrontGuardD)",
		path = "UnitMarker ",
		type = "UnitMarker",
	},
	{
		Groups = {
			"GuardsHostile",
		},
		handle = 1868447335,
		items = {
			{
				editor_view_abridged = "if not Completed",
				filter_type = "quest",
				reference_id = "RimvilleGuardsLogic",
				type = "QuestIsVariableBool",
				var = set({
	Completed = false,
}),
			},
		},
		map = "I-9 - Rimville",
		name = "Logic#335 (GuardsHostile)",
		path = "Logic ",
		type = "Logic",
	},
}