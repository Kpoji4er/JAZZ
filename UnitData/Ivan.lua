UndefineClass('Ivan_1')
DefineClass.Ivan= {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 94,
	Agility = 91,
	Dexterity = 95,
	Strength = 87,
	Wisdom = 82,
	Leadership = 35,
	Marksmanship = 92,
	Mechanical = 14,
	Explosives = 55,
	Medical = 15,
	Portrait = "Mod/FhNNYd/UI/MercsPortraits/Ivan",
	BigPortrait = "Mod/FhNNYd/UI/Mercs/Ivan",
	IsMercenary = true,
	Name = T(902287094053, --[[ModItemUnitDataCompositeDef Ivan_1 Name]] "Иван Долвич"),
	Nick = T(176944876895, --[[ModItemUnitDataCompositeDef Ivan_1 Nick]] "Иван"),
	AllCapsNick = T(138924706795, --[[ModItemUnitDataCompositeDef Ivan_1 AllCapsNick]] "ИВАН"),
	Bio = T(785289074791, --[[ModItemUnitDataCompositeDef Ivan_1 Bio]] "После развала Советского Союза Иван, в прошлом майор Советской Армии, решил попытать удачи на рынке капиталистических стран. Хотя разговорный английский по-прежнему дается ему с трудом, время, проведенное в A.I.M., лишь отточило его и без того выдающиеся навыки бойца. Иван настолько прославился своими подвигами, что в Голливуде даже решили снять о нем фильм. Однако проект пришлось отменить, поскольку Иван настаивал, что главную роль будет играть он сам, а все перестрелки в фильме должны вестись с применением боевого оружия."),
	Nationality = "Russia",
	Title = T(916297781192, --[[ModItemUnitDataCompositeDef Ivan_1 Title]] "Русский медведь"),
	Email = T(924462703234, --[[ModItemUnitDataCompositeDef Ivan_1 Email]] "иван@aim.com"),
	snype_nick = T(992505855899, --[[ModItemUnitDataCompositeDef Ivan_1 snype_nick]] "иван"),
	Refusals = {
		PlaceObj('MercChatRefusal', {
			'Lines', {
				PlaceObj('ChatMessage', {
					'Text', T(682680719409, --[[ModItemUnitDataCompositeDef Ivan_1 Text MercChatRefusal Lines ChatMessage voice:Ivan_1]] "Игорь погиб, потому что связался с kretinami вроде тебя. Я не пойду. Ты плохой komandir, из-за тебя Игорь погиб."),
				}),
			},
			'Conditions', {
				PlaceObj('UnitHireStatus', {
					Status = "Dead",
					TargetUnit = "Igor",
				}),
			},
		}),
		PlaceObj('MercChatRefusal', {
			'Lines', {
				PlaceObj('ChatMessage', {
					'Text', T(494640056540, --[[ModItemUnitDataCompositeDef Ivan_1 Text MercChatRefusal Lines ChatMessage voice:Ivan_1]] "Nyet! От тебя одни problems, а денег нет. Я устал от durakov без денег, за которыми мне потом подтирать."),
				}),
			},
			'Conditions', {
				PlaceObj('MercChatConditionMoney', {}),
			},
		}),
	},
	Mitigations = {
		PlaceObj('MercChatMitigation', {
			'Lines', {
				PlaceObj('ChatMessage', {
					'Text', T(401589484447, --[[ModItemUnitDataCompositeDef Ivan_1 Text MercChatMitigation Lines ChatMessage voice:Ivan_1]] "Дурацкая затея, но я согласен. Все-таки Игорь - rodnya, буду за ним приглядывать. Сколько раз мне из-за Игоря ещё придётся с такими idiotami работать..."),
				}),
			},
			'Conditions', {
				PlaceObj('UnitHireStatus', {
					Status = "Hired",
					TargetUnit = "Igor",
				}),
			},
			'chanceToRoll', 100,
		}),
	},
	ExtraPartingWords = {
		PlaceObj('MercChatBranch', {
			'Lines', {
				PlaceObj('ChatMessage', {
					'Text', T(222326137047, --[[ModItemUnitDataCompositeDef Ivan_1 Text MercChatBranch Lines ChatMessage voice:Ivan_1]] "Plemyannika моего найми. Он, конечно, govna бесполезного кусок, но так он хоть какое-то время пить не будет."),
				}),
			},
			'Conditions', {
				PlaceObj('UnitHireStatus', {
					Negate = true,
					Status = "Hired",
					TargetUnit = "Igor",
				}),
			},
		}),
		PlaceObj('MercChatBranch', {
			'Lines', {
				PlaceObj('ChatMessage', {
					'Text', T(717952932530, --[[ModItemUnitDataCompositeDef Ivan_1 Text MercChatBranch Lines ChatMessage voice:Ivan_1]] "Я слышал, Грунти ищет работу. Грунти - хороший soldat. Найми его."),
				}),
			},
			'Conditions', {
				PlaceObj('UnitHireStatus', {
					TargetUnit = "Grunty",
				}),
			},
		}),
	},
	Offline = {
		PlaceObj('ChatMessage', {
			'Text', T(120535048983, --[[ModItemUnitDataCompositeDef Ivan_1 Text Offline ChatMessage voice:Ivan_1]] "Это Иван Долвич. Я на задании. Перезвоню позже. Если ты durak, больше не звони."),
		}),
	},
	GreetingAndOffer = {
		PlaceObj('ChatMessage', {
			'Text', T(651799087543, --[[ModItemUnitDataCompositeDef Ivan_1 Text GreetingAndOffer ChatMessage voice:Ivan_1]] "Это Иван Долвич. У тебя есть zadaniye? Очередной дебил хочет меня нанять. Надеюсь, хотя бы у этого деньги будут."),
		}),
	},
	ConversationRestart = {
		PlaceObj('ChatMessage', {
			'Text', T(987546327838, --[[ModItemUnitDataCompositeDef Ivan_1 Text ConversationRestart ChatMessage voice:Ivan_1]] "Ты куда пропал? Idioty, тратят моё время..."),
		}),
	},
	IdleLine = {
		PlaceObj('ChatMessage', {
			'Text', T(348037122891, --[[ModItemUnitDataCompositeDef Ivan_1 Text IdleLine ChatMessage voice:Ivan_1]] "Ты здесь, idiotina? Я занят. Не будем тратить время."),
		}),
	},
	PartingWords = {
		PlaceObj('ChatMessage', {
			'Text', T(101253399279, --[[ModItemUnitDataCompositeDef Ivan_1 Text PartingWords ChatMessage voice:Ivan_1]] "Хорошо. Договорились. Я поеду в этот ваш Гран-Шьен."),
		}),
	},
	RehireIntro = {
		PlaceObj('ChatMessage', {
			'Text', T(155211445129, --[[ModItemUnitDataCompositeDef Ivan_1 Text RehireIntro ChatMessage voice:Ivan_1]] "Мой kontrakt скоро закончится. Как насчёт обновить его? Ты что, совсем durak - остаться без Ивана?"),
		}),
	},
	RehireOutro = {
		PlaceObj('ChatMessage', {
			'Text', T(850713834082, --[[ModItemUnitDataCompositeDef Ivan_1 Text RehireOutro ChatMessage voice:Ivan_1]] "Хорошо. Этот, похоже, не настолько durak, как все остальные, раз хочет со мной работать."),
		}),
	},
	StartingSalary = 2650,
	SalaryIncrease = 200,
	SalaryLv1 = 1400,
	SalaryMaxLv = 6200,
	LegacyNotes = 'JA1\n\n"A new member and a onetime decorated Major in the Red Army, Ivan Dolvich has, like his country, switched from killing for Lenin to dying for Lincolns. However, unlike his homeland, Ivan actually appears to be good at it." \n\nJA2\n\n"Ivan, a former highly decorated Red Army Major, joined the organization over three years ago on a freelance assignment. Despite serious difficulties communicating in English, he took the mercenary world by storm, breaking all kill-rate records and tallying up the kind of stats that perhaps only he himself is capable of breaking. Ivan himself says it best, \'gun, all gun, like finger on hand.\' In order to improve his relationship with commanders, Ivan has enrolled in an "English as a second language" course."\n\nSkills - Auto Weapons; Heavy Weapons',
	StartingLevel = 4,
	CustomEquipGear = function (self, items)  end,
	MaxHitPoints = 94,
	Likes = {
		"Igor",
		"Grunty",
	},
	StartingPerks = {
		"YouSeeIgor",
		"AutoWeapons",
		"Flanker",
		"BeefedUp",
		"TakeAim",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "Ivan",
		}),
	},
	Equipment = {
		"Ivan",
	},
	Tier = "Elite",
	Specialization = "Marksmen",
	pollyvoice = "Russell",
	gender = "Male",
	VoiceResponseId = "Ivan",
}

