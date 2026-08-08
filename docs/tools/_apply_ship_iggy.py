#!/usr/bin/env python3
"""Ship Jazz_Iggy under JAZZ-UNITS-002. Idempotent. Run from anywhere."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
UNITS = JAZZ.parent / "jazz-units"
SNIP = Path(__file__).resolve().parent / "_grom_snippets"

ID = {
    "perk_name": 890000000004825,
    "perk_desc": 890000000004826,
    "Name": 890000000004827,
    "Nick": 890000000004828,
    "AllCapsNick": 890000000004829,
    "Bio": 890000000004830,
    "Title": 890000000004831,
    "Email": 890000000004832,
    "snype": 890000000004833,
    "Refusal": 890000000004834,
    "Mitigation": 890000000004835,
    "ExtraParting": 890000000004836,
    "Offline": 890000000004837,
    "Greeting": 890000000004838,
    "Restart": 890000000004839,
    "Idle": 890000000004840,
    "Parting": 890000000004841,
    "RehireIntro": 890000000004842,
    "RehireOutro": 890000000004843,
    "VR_Selection": 890000000004844,
    "VR_Aim1": 890000000004845,
    "VR_Aim2": 890000000004846,
    "VR_Kill": 890000000004847,
    "VR_Death": 890000000004848,
    "VR_Downed": 890000000004849,
    "VR_Combat": 890000000004850,
    "VR_LevelUp": 890000000004851,
    "VR_Ammo": 890000000004852,
    "VR_Idle": 890000000004853,
    "VR_Mock": 890000000004854,
    "VR_Praise": 890000000004855,
}

LOC_ROWS = [
    (ID["perk_name"], "Совесть дезертира", "Deserter's Conscience", "Jazz_Perk_Iggy"),
    (ID["perk_desc"], "Эта именная способность пока не действует.", "This personal ability does nothing yet.", "Jazz_Perk_Iggy"),
    (ID["Name"], "Игмус «Игги» Палков", 'Igmus "Iggy" Palkov', "Jazz_Iggy"),
    (ID["Nick"], "Игги", "Iggy", "Jazz_Iggy"),
    (ID["AllCapsNick"], "ИГГИ", "IGGY", "Jazz_Iggy"),
    (
        ID["Bio"],
        "Русский наёмник, которого королева Дейдранна наняла в армию под командованием Майка ($2000/день). После убийства Майка и осознания режима Дейдранны дезертировал с совестью; позже сидит в баре и нанимается за $1950/день. Гордость и мораль сильные; мечтает о «Великой России». Эксперт тяжёлого оружия. Дружит с Иваном; Конрад его ценит; ненавидит Фиделя.",
        "A Russian merc hired into Queen Deidranna's army under Mike ($2000/day). After Mike was killed he deserted with a guilty conscience; later hireable for $1950/day. Strong pride and morality; dreams of a \"Greater Russia.\" Heavy Weapons Expert. Likes Ivan; liked by Conrad; dislikes Fidel.",
        "Jazz_Iggy",
    ),
    (ID["Title"], "Тяжеловес из Сан-Моны", "The San Mona Heavy", "Jazz_Iggy"),
    (ID["Email"], "Iggy@palkov.ru", "Iggy@palkov.ru", "Jazz_Iggy"),
    (ID["snype"], "iggy", "iggy", "Jazz_Iggy"),
    (ID["Refusal"], "Пока Фидель у вас — нет. С ним я не служу.", "Not while Fidel's on the team. I don't serve with him.", "Jazz_Iggy"),
    (ID["Mitigation"], "Иван уже здесь? Тогда своих не бросаю.", "Ivan already here? Then I don't abandon my own.", "Jazz_Iggy"),
    (ID["ExtraParting"], "Возьмите Ивана, если найдёте — свой человек.", "Hire Ivan if you find him — one of ours.", "Jazz_Iggy"),
    (ID["Offline"], "Палков. Позже — сейчас не у бара.", "Palkov. Later — not at the bar right now.", "Jazz_Iggy"),
    (ID["Greeting"], "Игги. Служил у Дейдранны — больше нет. Тысяча девятьсот пятьдесят в день, и я ваш.", "Iggy. Worked for Deidranna — not anymore. Nineteen-fifty a day, and I'm yours.", "Jazz_Iggy"),
    (ID["Restart"], "Связь пропала. Говорите.", "Line dropped. Speak.", "Jazz_Iggy"),
    (ID["Idle"], "Почему люди не могут быть как я? А?", "Why can't more people be like me? Hm?", "Jazz_Iggy"),
    (ID["Parting"], "Тяжёлое оружие со мной. Идём.", "Heavy weapons with me. Let's move.", "Jazz_Iggy"),
    (ID["RehireIntro"], "Контракт кончается. Продлеваем — те же тысяча девятьсот пятьдесят?", "Contract ending. Extend — same nineteen-fifty?", "Jazz_Iggy"),
    (ID["RehireOutro"], "Остаюсь. Совесть уже чище, чем при королеве.", "Staying. Conscience cleaner than under the Queen.", "Jazz_Iggy"),
    (ID["VR_Selection"], "Игги на месте.", "Iggy here.", "Jazz_Iggy"),
    (ID["VR_Aim1"], "Огонь!", "Fire!", "Jazz_Iggy"),
    (ID["VR_Aim2"], "Тяжёлое готово.", "Heavy's ready.", "Jazz_Iggy"),
    (ID["VR_Kill"], "Этот я выиграл!", "I win this one!", "Jazz_Iggy"),
    (ID["VR_Death"], "Верните пепел Матушке России…", "Return my ashes to Mother Russia…!", "Jazz_Iggy"),
    (ID["VR_Downed"], "Ранило… ещё держусь.", "Hit… still holding.", "Jazz_Iggy"),
    (ID["VR_Combat"], "Предатели в секторе!", "Traitors in the area!", "Jazz_Iggy"),
    (ID["VR_LevelUp"], "Опыт растёт.", "Experience grows.", "Jazz_Iggy"),
    (ID["VR_Ammo"], "Боекомплект на исходе!", "Ammo running low!", "Jazz_Iggy"),
    (ID["VR_Idle"], "Внутри я тёплый и пушистый.", "Inside I am warm and fuzzy.", "Jazz_Iggy"),
    (ID["VR_Mock"], "Хорошо, что Фиделя тут нет.", "Good thing Fidel's not here.", "Jazz_Iggy"),
    (ID["VR_Praise"], "Со своими — проще.", "Easier with our own.", "Jazz_Iggy"),
]


def csv_escape(s: str) -> str:
    if any(c in s for c in ',"\n'):
        return '"' + s.replace('"', '""') + '"'
    return s


def ensure_loc() -> None:
    for fname in ("English.csv", "Russian.csv"):
        path = JAZZ / fname
        text = path.read_text(encoding="utf-8")
        missing = [row for row in LOC_ROWS if str(row[0]) not in text]
        if not missing:
            print("loc ok:", fname)
            continue
        lines = []
        for lid, ru, en, ctx in missing:
            if fname == "English.csv":
                lines.append(f"{lid},{csv_escape(ru)},{csv_escape(en)},,{ctx}")
            else:
                lines.append(f"{lid},{csv_escape(ru)},{csv_escape(ru)},,{ctx}")
        if not text.endswith("\n"):
            text += "\n"
        path.write_text(text + "\n".join(lines) + "\n", encoding="utf-8")
        print("loc append", len(lines), "->", fname)


def bump_metadata(path: Path, bullet: str) -> None:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"'version',\s*(\d+)", text)
    if not m:
        raise SystemExit(f"no version in {path}")
    ver = int(m.group(1)) + 1
    text = text[: m.start(1)] + str(ver) + text[m.end(1) :]
    # append last_changes with \\n only
    m2 = re.search(r"'last_changes',\s*\"", text)
    if not m2:
        raise SystemExit(f"no last_changes in {path}")
    insert_at = m2.end()
    text = text[:insert_at] + f"- {bullet}\\n" + text[insert_at:]
    path.write_text(text, encoding="utf-8")
    print(f"metadata {path.parent.name}: version={ver}, last_changes prepended")


def write_perk() -> None:
    dest = JAZZ / "CharacterEffect" / "Jazz_Perk_Iggy.lua"
    icon_src = JAZZ / "Perks" / "Personal" / "Grom.png"
    icon_dst = JAZZ / "Perks" / "Personal" / "Iggy.png"
    if not icon_dst.exists() and icon_src.exists():
        shutil.copy2(icon_src, icon_dst)
        print("perk icon placeholder: Grom.png -> Iggy.png")
    dest.write_text(
        "UndefineClass('Jazz_Perk_Iggy')\n"
        "DefineClass.Jazz_Perk_Iggy = {\n"
        '\t__parents = { "Perk" },\n'
        '\t__generated_by_class = "ModItemCharacterEffectCompositeDef",\n\n\n'
        '\tobject_class = "Perk",\n'
        "\tunit_reactions = {},\n"
        f'\tDisplayName = T({ID["perk_name"]}, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Iggy DisplayName]] "Совесть дезертира"),\n'
        f'\tDescription = T({ID["perk_desc"]}, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Iggy Description]] "Эта именная способность пока не действует."),\n'
        '\tIcon = "Mod/e6L4ECj/Perks/Personal/Iggy.png",\n'
        '\tTier = "Personal",\n'
        "}\n",
        encoding="utf-8",
    )
    print("wrote", dest)

    items = JAZZ / "items.lua"
    t = items.read_text(encoding="utf-8")
    if "Jazz_Perk_Iggy" in t:
        print("jazz items perk already present")
    else:
        needle = "\t\t\tPlaceObj('ModItemFolder', {\n\t\t\t\t'name', \"Rothman\",\n"
        insert = (
            "\t\t\tPlaceObj('ModItemFolder', {\n"
            "\t\t\t\t'name', \"Iggy\",\n"
            "\t\t\t}, {\n"
            "\t\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {\n"
            "\t\t\t\t\t'Group', \"Perk-Personal\",\n"
            "\t\t\t\t\t'Id', \"Jazz_Perk_Iggy\",\n"
            "\t\t\t\t\t'object_class', \"Perk\",\n"
            "\t\t\t\t\t'unit_reactions', {},\n"
            f"\t\t\t\t\t'DisplayName', T({ID['perk_name']}, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Iggy DisplayName]] \"Совесть дезертира\"),\n"
            f"\t\t\t\t\t'Description', T({ID['perk_desc']}, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Iggy Description]] \"Эта именная способность пока не действует.\"),\n"
            "\t\t\t\t\t'Icon', \"Mod/e6L4ECj/Perks/Personal/Iggy.png\",\n"
            "\t\t\t\t\t'Tier', \"Personal\",\n"
            "\t\t\t\t}),\n"
            "\t\t\t\t}),\n"
        )
        if needle not in t:
            raise SystemExit("Rothman perk folder anchor missing")
        items.write_text(t.replace(needle, insert + needle, 1), encoding="utf-8")
        print("inserted perk ModItem")

    meta = JAZZ / "metadata.lua"
    mt = meta.read_text(encoding="utf-8")
    if "CharacterEffect/Jazz_Perk_Iggy.lua" not in mt:
        mt = mt.replace(
            '"CharacterEffect/Jazz_Perk_Grom.lua",',
            '"CharacterEffect/Jazz_Perk_Grom.lua",\n\t\t"CharacterEffect/Jazz_Perk_Iggy.lua",',
            1,
        )
        meta.write_text(mt, encoding="utf-8")
        print("jazz metadata.code + perk")


def write_unitdata_companion() -> None:
    # reuse content from earlier design — write by reading template from Grom companion and not
    # Keep as dedicated file written below via shared UNITDATA_LUA
    dest = UNITS / "UnitData" / "Jazz_Iggy.lua"
    dest.write_text(UNITDATA_LUA, encoding="utf-8")
    print("wrote", dest)


UNITDATA_LUA = None  # filled after ID dict


def _build_unitdata() -> str:
    return f'''UndefineClass('Jazz_Iggy')
DefineClass.Jazz_Iggy = {{
	__parents = {{ "UnitData" }},
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Affiliation = "AIM",
	Health = 88,
	Agility = 81,
	Dexterity = 79,
	Strength = 85,
	Wisdom = 71,
	Will = 72,
	Leadership = 15,
	Marksmanship = 87,
	Mechanical = 42,
	Explosives = 21,
	Medical = 33,
	Portrait = "Mod/Dv3mFVN/MercPortraits/Iggy.png",
	BigPortrait = "Mod/Dv3mFVN/MercPortraits/Iggy_Big.png",
	IsMercenary = true,
	Name = T({ID["Name"]}, --[[ModItemUnitDataCompositeDef Jazz_Iggy Name]] "Игмус «Игги» Палков"),
	Nick = T({ID["Nick"]}, --[[ModItemUnitDataCompositeDef Jazz_Iggy Nick]] "Игги"),
	AllCapsNick = T({ID["AllCapsNick"]}, --[[ModItemUnitDataCompositeDef Jazz_Iggy AllCapsNick]] "ИГГИ"),
	Bio = T({ID["Bio"]}, --[[ModItemUnitDataCompositeDef Jazz_Iggy Bio]] "Русский наёмник, которого королева Дейдранна наняла в армию под командованием Майка ($2000/день). После убийства Майка и осознания режима Дейдранны дезертировал с совестью; позже сидит в баре и нанимается за $1950/день. Гордость и мораль сильные; мечтает о «Великой России». Эксперт тяжёлого оружия. Дружит с Иваном; Конрад его ценит; ненавидит Фиделя."),
	Nationality = "Russia",
	Title = T({ID["Title"]}, --[[ModItemUnitDataCompositeDef Jazz_Iggy Title]] "Тяжеловес из Сан-Моны"),
	Email = T({ID["Email"]}, --[[ModItemUnitDataCompositeDef Jazz_Iggy Email]] "Iggy@palkov.ru"),
	snype_nick = T({ID["snype"]}, --[[ModItemUnitDataCompositeDef Jazz_Iggy snype_nick]] "iggy"),
	Refusals = {{
		PlaceObj('MercChatRefusal', {{
			'Lines', {{
				PlaceObj('ChatMessage', {{
					'Text', T({ID["Refusal"]}, --[[ModItemUnitDataCompositeDef Jazz_Iggy Text MercChatRefusal Lines ChatMessage voice:Jazz_Iggy]] "Пока Фидель у вас — нет. С ним я не служу."),
				}}),
			}},
			'Conditions', {{
				PlaceObj('UnitHireStatus', {{
					Status = "Hired",
					TargetUnit = "Fidel",
				}}),
			}},
			'chanceToRoll', 100,
		}}),
	}},
	Haggles = {{}},
	HaggleRehire = {{}},
	Mitigations = {{
		PlaceObj('MercChatMitigation', {{
			'Lines', {{
				PlaceObj('ChatMessage', {{
					'Text', T({ID["Mitigation"]}, --[[ModItemUnitDataCompositeDef Jazz_Iggy Text MercChatMitigation Lines ChatMessage voice:Jazz_Iggy]] "Иван уже здесь? Тогда своих не бросаю."),
				}}),
			}},
			'Conditions', {{
				PlaceObj('CheckExpression', {{
					Expression = function (self, obj)
						return table.count(gv_UnitData, function(k, ud)
							return IsKindOf(ud, "UnitData") and ud.HireStatus == "Hired" and k == "Ivan"
						end) >= 1
					end,
				}}),
			}},
			'chanceToRoll', 100,
		}}),
	}},
	ExtraPartingWords = {{
		PlaceObj('MercChatBranch', {{
			'Lines', {{
				PlaceObj('ChatMessage', {{
					'Text', T({ID["ExtraParting"]}, --[[ModItemUnitDataCompositeDef Jazz_Iggy Text MercChatBranch Lines ChatMessage voice:Jazz_Iggy]] "Возьмите Ивана, если найдёте — свой человек."),
				}}),
			}},
			'Conditions', {{
				PlaceObj('CheckExpression', {{
					Expression = function (self, obj)
						return table.count(gv_UnitData, function(k, ud)
							return IsKindOf(ud, "UnitData") and ud.HireStatus == "Hired" and k == "Ivan"
						end) < 1
					end,
				}}),
			}},
		}}),
	}},
	Offline = {{
		PlaceObj('ChatMessage', {{
			'Text', T({ID["Offline"]}, --[[ModItemUnitDataCompositeDef Jazz_Iggy Text Offline ChatMessage voice:Jazz_Iggy]] "Палков. Позже — сейчас не у бара."),
		}}),
	}},
	GreetingAndOffer = {{
		PlaceObj('ChatMessage', {{
			'Text', T({ID["Greeting"]}, --[[ModItemUnitDataCompositeDef Jazz_Iggy Text GreetingAndOffer ChatMessage voice:Jazz_Iggy]] "Игги. Служил у Дейдранны — больше нет. Тысяча девятьсот пятьдесят в день, и я ваш."),
		}}),
	}},
	ConversationRestart = {{
		PlaceObj('ChatMessage', {{
			'Text', T({ID["Restart"]}, --[[ModItemUnitDataCompositeDef Jazz_Iggy Text ConversationRestart ChatMessage voice:Jazz_Iggy]] "Связь пропала. Говорите."),
		}}),
	}},
	IdleLine = {{
		PlaceObj('ChatMessage', {{
			'Text', T({ID["Idle"]}, --[[ModItemUnitDataCompositeDef Jazz_Iggy Text IdleLine ChatMessage voice:Jazz_Iggy]] "Почему люди не могут быть как я? А?"),
		}}),
	}},
	PartingWords = {{
		PlaceObj('ChatMessage', {{
			'Text', T({ID["Parting"]}, --[[ModItemUnitDataCompositeDef Jazz_Iggy Text PartingWords ChatMessage voice:Jazz_Iggy]] "Тяжёлое оружие со мной. Идём."),
		}}),
	}},
	RehireIntro = {{
		PlaceObj('ChatMessage', {{
			'Text', T({ID["RehireIntro"]}, --[[ModItemUnitDataCompositeDef Jazz_Iggy Text RehireIntro ChatMessage voice:Jazz_Iggy]] "Контракт кончается. Продлеваем — те же тысяча девятьсот пятьдесят?"),
		}}),
	}},
	RehireOutro = {{
		PlaceObj('ChatMessage', {{
			'Text', T({ID["RehireOutro"]}, --[[ModItemUnitDataCompositeDef Jazz_Iggy Text RehireOutro ChatMessage voice:Jazz_Iggy]] "Остаюсь. Совесть уже чище, чем при королеве."),
		}}),
	}},
	MedicalDeposit = "small",
	StartingSalary = 1950,
	SalaryIncrease = 200,
	SalaryLv1 = 1950,
	SalaryMaxLv = 4500,
	StartingLevel = 5,
	CustomEquipGear = function (self, items)
		self:TryEquip(items, "Handheld A", "Firearm")
		self:TryEquip(items, "Handheld B", "Firearm")
	end,
	MaxHitPoints = 88,
	Likes = {{
		"Ivan",
	}},
	Dislikes = {{
		"Fidel",
	}},
	StartingPerks = {{
		"Jazz_Perk_Iggy",
		"HeavyWeaponsTraining",
		"Throwing",
		"Hardened",
	}},
	AppearancesList = {{
		PlaceObj('AppearanceWeight', {{
			'Preset', "Iggy",
		}}),
	}},
	Equipment = {{
		"Loot_JAZZ_Iggy",
	}},
	Tier = "Veteran",
	Specialization = "HeavyWeapons",
	pollyvoice = "Matthew",
	gender = "Male",
	VoiceResponseId = "Jazz_Iggy",
	FallbackMissingVR = "Ice",
	DaysUntilOnline = 0,
}}
'''


def moditem_unitdata_block() -> str:
    """ModItemUnitDataCompositeDef mirroring companion (editor format with quoted keys)."""
    return f"""\t\t\tPlaceObj('ModItemFolder', {{
\t\t\t\t'name', "Jazz_Iggy",
\t\t\t}}, {{
\t\t\t\tPlaceObj('ModItemUnitDataCompositeDef', {{
\t\t\t\t\t'Group', "MercenariesOld",
\t\t\t\t\t'Id', "Jazz_Iggy",
\t\t\t\t\t'object_class', "UnitData",
\t\t\t\t'Affiliation', "AIM",
\t\t\t\t'Health', 88,
\t\t\t\t'Agility', 81,
\t\t\t\t'Dexterity', 79,
\t\t\t\t'Strength', 85,
\t\t\t\t'Wisdom', 71,
\t\t\t\t'Will', 72,
\t\t\t\t'Leadership', 15,
\t\t\t\t'Marksmanship', 87,
\t\t\t\t'Mechanical', 42,
\t\t\t\t'Explosives', 21,
\t\t\t\t'Medical', 33,
\t\t\t\t'Portrait', "Mod/Dv3mFVN/MercPortraits/Iggy.png",
\t\t\t\t'BigPortrait', "Mod/Dv3mFVN/MercPortraits/Iggy_Big.png",
\t\t\t\t'IsMercenary', true,
\t\t\t\t'Name', T({ID["Name"]}, "Игмус «Игги» Палков"),
\t\t\t\t'Nick', T({ID["Nick"]}, "Игги"),
\t\t\t\t'AllCapsNick', T({ID["AllCapsNick"]}, "ИГГИ"),
\t\t\t\t'Bio', T({ID["Bio"]}, "Русский наёмник, которого королева Дейдранна наняла в армию под командованием Майка ($2000/день). После убийства Майка и осознания режима Дейдранны дезертировал с совестью; позже сидит в баре и нанимается за $1950/день. Гордость и мораль сильные; мечтает о «Великой России». Эксперт тяжёлого оружия. Дружит с Иваном; Конрад его ценит; ненавидит Фиделя."),
\t\t\t\t'Nationality', "Russia",
\t\t\t\t'Title', T({ID["Title"]}, "Тяжеловес из Сан-Моны"),
\t\t\t\t'Email', T({ID["Email"]}, "Iggy@palkov.ru"),
\t\t\t\t'snype_nick', T({ID["snype"]}, "iggy"),
\t\t\t\t'Refusals', {{
\t\t\t\t\tPlaceObj('MercChatRefusal', {{
\t\t\t\t\t\t'Lines', {{ PlaceObj('ChatMessage', {{ 'Text', T({ID["Refusal"]}, --[[voice:Jazz_Iggy]] "Пока Фидель у вас — нет. С ним я не служу.") }}) }},
\t\t\t\t\t\t'Conditions', {{ PlaceObj('UnitHireStatus', {{ Status = "Hired", TargetUnit = "Fidel" }}) }},
\t\t\t\t\t\t'chanceToRoll', 100,
\t\t\t\t\t}}),
\t\t\t\t}},
\t\t\t\t'Mitigations', {{
\t\t\t\t\tPlaceObj('MercChatMitigation', {{
\t\t\t\t\t\t'Lines', {{ PlaceObj('ChatMessage', {{ 'Text', T({ID["Mitigation"]}, --[[voice:Jazz_Iggy]] "Иван уже здесь? Тогда своих не бросаю.") }}) }},
\t\t\t\t\t\t'Conditions', {{
\t\t\t\t\t\t\tPlaceObj('CheckExpression', {{
\t\t\t\t\t\t\t\tExpression = function (self, obj)
\t\t\t\t\t\t\t\t\treturn table.count(gv_UnitData, function(k, ud)
\t\t\t\t\t\t\t\t\t\treturn IsKindOf(ud, "UnitData") and ud.HireStatus == "Hired" and k == "Ivan"
\t\t\t\t\t\t\t\t\tend) >= 1
\t\t\t\t\t\t\t\tend,
\t\t\t\t\t\t\t}}),
\t\t\t\t\t\t}},
\t\t\t\t\t\t'chanceToRoll', 100,
\t\t\t\t\t}}),
\t\t\t\t}},
\t\t\t\t'ExtraPartingWords', {{
\t\t\t\t\tPlaceObj('MercChatBranch', {{
\t\t\t\t\t\t'Lines', {{ PlaceObj('ChatMessage', {{ 'Text', T({ID["ExtraParting"]}, --[[voice:Jazz_Iggy]] "Возьмите Ивана, если найдёте — свой человек.") }}) }},
\t\t\t\t\t\t'Conditions', {{
\t\t\t\t\t\t\tPlaceObj('CheckExpression', {{
\t\t\t\t\t\t\t\tExpression = function (self, obj)
\t\t\t\t\t\t\t\t\treturn table.count(gv_UnitData, function(k, ud)
\t\t\t\t\t\t\t\t\t\treturn IsKindOf(ud, "UnitData") and ud.HireStatus == "Hired" and k == "Ivan"
\t\t\t\t\t\t\t\t\tend) < 1
\t\t\t\t\t\t\t\tend,
\t\t\t\t\t\t\t}}),
\t\t\t\t\t\t}},
\t\t\t\t\t}}),
\t\t\t\t}},
\t\t\t\t'Offline', {{ PlaceObj('ChatMessage', {{ 'Text', T({ID["Offline"]}, --[[voice:Jazz_Iggy]] "Палков. Позже — сейчас не у бара.") }}) }},
\t\t\t\t'GreetingAndOffer', {{ PlaceObj('ChatMessage', {{ 'Text', T({ID["Greeting"]}, --[[voice:Jazz_Iggy]] "Игги. Служил у Дейдранны — больше нет. Тысяча девятьсот пятьдесят в день, и я ваш.") }}) }},
\t\t\t\t'ConversationRestart', {{ PlaceObj('ChatMessage', {{ 'Text', T({ID["Restart"]}, --[[voice:Jazz_Iggy]] "Связь пропала. Говорите.") }}) }},
\t\t\t\t'IdleLine', {{ PlaceObj('ChatMessage', {{ 'Text', T({ID["Idle"]}, --[[voice:Jazz_Iggy]] "Почему люди не могут быть как я? А?") }}) }},
\t\t\t\t'PartingWords', {{ PlaceObj('ChatMessage', {{ 'Text', T({ID["Parting"]}, --[[voice:Jazz_Iggy]] "Тяжёлое оружие со мной. Идём.") }}) }},
\t\t\t\t'RehireIntro', {{ PlaceObj('ChatMessage', {{ 'Text', T({ID["RehireIntro"]}, --[[voice:Jazz_Iggy]] "Контракт кончается. Продлеваем — те же тысяча девятьсот пятьдесят?") }}) }},
\t\t\t\t'RehireOutro', {{ PlaceObj('ChatMessage', {{ 'Text', T({ID["RehireOutro"]}, --[[voice:Jazz_Iggy]] "Остаюсь. Совесть уже чище, чем при королеве.") }}) }},
\t\t\t\t'MedicalDeposit', "small",
\t\t\t\t'StartingSalary', 1950,
\t\t\t\t'SalaryIncrease', 200,
\t\t\t\t'SalaryLv1', 1950,
\t\t\t\t'SalaryMaxLv', 4500,
\t\t\t\t'StartingLevel', 5,
\t\t\t\t'CustomEquipGear', function (self, items)
\t\t\t\tself:TryEquip(items, "Handheld A", "Firearm")
\t\t\t\tself:TryEquip(items, "Handheld B", "Firearm")
\t\t\t\tend,
\t\t\t\t'MaxHitPoints', 88,
\t\t\t\t'Likes', {{ "Ivan" }},
\t\t\t\t'Dislikes', {{ "Fidel" }},
\t\t\t\t'StartingPerks', {{
\t\t\t\t"Jazz_Perk_Iggy",
\t\t\t\t"HeavyWeaponsTraining",
\t\t\t\t"Throwing",
\t\t\t\t"Hardened",
\t\t\t\t}},
\t\t\t\t'AppearancesList', {{ PlaceObj('AppearanceWeight', {{ 'Preset', "Iggy" }}) }},
\t\t\t\t'Equipment', {{ "Loot_JAZZ_Iggy" }},
\t\t\t\t'Tier', "Veteran",
\t\t\t\t'Specialization', "HeavyWeapons",
\t\t\t\t'pollyvoice', "Matthew",
\t\t\t\t'gender', "Male",
\t\t\t\t'VoiceResponseId', "Jazz_Iggy",
\t\t\t\t'FallbackMissingVR', "Ice",
\t\t\t\t'DaysUntilOnline', 0,
\t\t\t\t}}),
\t\t\t\tPlaceObj('ModItemVoiceResponse', {{
\t\t\t\t\tSelection = TConcat({{ T({ID["VR_Selection"]}, --[[voice:Jazz_Iggy]] "Игги на месте.") }}),
\t\t\t\t\tAimAttack = TConcat({{
\t\t\t\t\t\tT({ID["VR_Aim1"]}, --[[voice:Jazz_Iggy]] "Огонь!"),
\t\t\t\t\t\tT({ID["VR_Aim2"]}, --[[voice:Jazz_Iggy]] "Тяжёлое готово."),
\t\t\t\t\t}}),
\t\t\t\t\tOpponentKilled = TConcat({{ T({ID["VR_Kill"]}, --[[voice:Jazz_Iggy]] "Этот я выиграл!") }}),
\t\t\t\t\tDeathGeneral = TConcat({{ T({ID["VR_Death"]}, --[[voice:Jazz_Iggy]] "Верните пепел Матушке России…") }}),
\t\t\t\t\tDowned = TConcat({{ T({ID["VR_Downed"]}, --[[voice:Jazz_Iggy]] "Ранило… ещё держусь.") }}),
\t\t\t\t\tCombatStartDetected = TConcat({{ T({ID["VR_Combat"]}, --[[voice:Jazz_Iggy]] "Предатели в секторе!") }}),
\t\t\t\t\tLevelUp = TConcat({{ T({ID["VR_LevelUp"]}, --[[voice:Jazz_Iggy]] "Опыт растёт.") }}),
\t\t\t\t\tAmmoLow = TConcat({{ T({ID["VR_Ammo"]}, --[[voice:Jazz_Iggy]] "Боекомплект на исходе!") }}),
\t\t\t\t\tIdle = TConcat({{ T({ID["VR_Idle"]}, --[[voice:Jazz_Iggy]] "Внутри я тёплый и пушистый.") }}),
\t\t\t\t\tMockDislike1 = TConcat({{ T({ID["VR_Mock"]}, --[[voice:Jazz_Iggy]] "Хорошо, что Фиделя тут нет.") }}),
\t\t\t\t\tPraisesBuddy1 = TConcat({{ T({ID["VR_Praise"]}, --[[voice:Jazz_Iggy]] "Со своими — проще.") }}),
\t\t\t\t\tgroup = "MercenariesOld",
\t\t\t\t\tid = "Jazz_Iggy",
\t\t\t\t}}),
\t\t\t\t}}),
"""


def insert_units_items() -> None:
    items = UNITS / "items.lua"
    t = items.read_text(encoding="utf-8")
    if "'Id', \"Jazz_Iggy\"" in t:
        print("units items already has Jazz_Iggy")
        return

    # 1) Loot aggregator after Loot_JAZZ_Grom
    agg = (SNIP / "Loot_JAZZ_Grom.lua.txt").read_text(encoding="utf-8").strip()
    iggy_agg = agg.replace("Loot_JAZZ_Grom", "Loot_JAZZ_Iggy").replace("JAZZ_Grom", "JAZZ_Iggy")
    if agg not in t:
        raise SystemExit("Loot_JAZZ_Grom aggregator snippet not found in items")
    t = t.replace(agg, agg + "\n\t\t\t\t" + iggy_agg, 1)

    # 2) Tier defs after JAZZ_Grom20
    g20 = (SNIP / "JAZZ_Grom20.lua.txt").read_text(encoding="utf-8").strip()
    tiers = []
    for tid in ("JAZZ_Grom50", "JAZZ_Grom35", "JAZZ_Grom25", "JAZZ_Grom20"):
        block = (SNIP / f"{tid}.lua.txt").read_text(encoding="utf-8").strip()
        tiers.append(block.replace("Grom", "Iggy"))
    iggy_tiers = "\n\t\t\t\t".join(tiers)
    if g20 not in t:
        raise SystemExit("JAZZ_Grom20 snippet not found")
    t = t.replace(g20, g20 + "\n\t\t\t\t" + iggy_tiers, 1)

    # 3) UnitData folder after Jazz_Grom folder
    folder_anchor = "PlaceObj('ModItemFolder', {\n\t\t\t\t'name', \"Jazz_Grom\","
    idx = t.find(folder_anchor)
    if idx < 0:
        raise SystemExit("Jazz_Grom folder missing")
    rest = t[idx + 10 :]
    nxt = rest.find("\n\t\t\tPlaceObj('ModItemFolder', {")
    insert_at = idx + 10 + nxt
    t = t[:insert_at] + "\n" + moditem_unitdata_block() + t[insert_at:]

    # 4) Appearance after Grom appearance
    app = (SNIP / "Appearance_Grom.lua.txt").read_text(encoding="utf-8").rstrip() + "\n"
    iggy_app = app.replace('id = "Grom"', 'id = "Iggy"', 1)
    if app not in t:
        raise SystemExit("Appearance Grom block missing")
    t = t.replace(app, app + iggy_app, 1)

    items.write_text(t, encoding="utf-8")
    print("units items.lua: loot + UnitData folder + Appearance inserted")


def update_units_metadata() -> None:
    meta = UNITS / "metadata.lua"
    mt = meta.read_text(encoding="utf-8")
    if "UnitData/Jazz_Iggy.lua" not in mt:
        mt = mt.replace(
            '"UnitData/Jazz_Grom.lua",',
            '"UnitData/Jazz_Grom.lua",\n\t\t"UnitData/Jazz_Iggy.lua",',
            1,
        )
        # if Grom not adjacent, insert after Biggens
        if "UnitData/Jazz_Iggy.lua" not in mt:
            mt = mt.replace(
                '"UnitData/Jazz_Biggens.lua",',
                '"UnitData/Jazz_Biggens.lua",\n\t\t"UnitData/Jazz_Iggy.lua",',
                1,
            )
    # affected_resources after Biggens loot block
    marker = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "LootDef",
\t\t\t'Id', "Loot_JAZZ_Biggens",
\t\t\t'ClassDisplayName', "Loot definition",
\t\t}),"""
    res = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "UnitDataCompositeDef",
\t\t\t'Id', "Jazz_Iggy",
\t\t\t'ClassDisplayName', "Unit",
\t\t}),
\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "VoiceResponse",
\t\t\t'Id', "Jazz_Iggy",
\t\t\t'ClassDisplayName', "Unit voice responses",
\t\t}),
\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "AppearancePreset",
\t\t\t'Id', "Iggy",
\t\t\t'ClassDisplayName', "Unit appearance",
\t\t}),
\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "LootDef",
\t\t\t'Id', "Loot_JAZZ_Iggy",
\t\t\t'ClassDisplayName', "Loot definition",
\t\t}),"""
    if "'Id', \"Jazz_Iggy\"" not in mt and marker in mt:
        mt = mt.replace(marker, marker + "\n" + res, 1)
    meta.write_text(mt, encoding="utf-8")
    print("units metadata updated")


def wire_carlos_dislike() -> None:
    path = UNITS / "UnitData" / "Jazz_Carlos.lua"
    t = path.read_text(encoding="utf-8")
    if "Jazz_Iggy" in t:
        print("Carlos already wires Iggy")
        return
    if "Dislikes = {" in t:
        t = t.replace("Dislikes = {", 'Dislikes = {\n\t\t"Jazz_Iggy",', 1)
    else:
        # insert before StartingPerks
        t = t.replace(
            "StartingPerks = {",
            'Dislikes = {\n\t\t"Jazz_Iggy",\n\t},\n\tStartingPerks = {',
            1,
        )
    path.write_text(t, encoding="utf-8")
    # mirror in items.lua if present
    items = UNITS / "items.lua"
    it = items.read_text(encoding="utf-8")
    # only touch Jazz_Carlos ModItem Dislikes if empty / missing Jazz_Iggy nearby
    print("Carlos companion Dislikes += Jazz_Iggy (items.lua may need editor sync)")


def main() -> None:
    global UNITDATA_LUA
    UNITDATA_LUA = _build_unitdata()
    assert (UNITS / "MercPortraits" / "Iggy.png").exists()
    assert SNIP.joinpath("Loot_JAZZ_Grom.lua.txt").exists()
    assert SNIP.joinpath("Appearance_Grom.lua.txt").exists()

    ensure_loc()
    write_perk()
    write_unitdata_companion()
    insert_units_items()
    update_units_metadata()
    wire_carlos_dislike()
    bump_metadata(JAZZ / "metadata.lua", "UNITS-002: ship Jazz_Iggy (perk stub, AIM hire, portraits) [new game recommended]")
    bump_metadata(UNITS / "metadata.lua", "UNITS-002: ship Jazz_Iggy UnitData/loot/appearance/VR [new game recommended]")
    print("DONE")


if __name__ == "__main__":
    main()
