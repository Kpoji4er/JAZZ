#!/usr/bin/env python3
"""Generate AME UnitData companions, loot, loc, portraits (JAZZ-UNITS-005).

Loads ROSTER from docs/tools/_gen_ame_roster_60.py via importlib.
Idempotent: replaces JAZZ-UNITS-005-AME-BEGIN/END marked blocks.
"""
from __future__ import annotations

import importlib.util
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JAZZ = ROOT
JAZZ_UNITS = ROOT.parent / "jazz-units"
ROSTER_SCRIPT = Path(__file__).resolve().parent / "_gen_ame_roster_60.py"

# Russian Name/Nick forms for hire UI (REQ-029).
_names_spec = importlib.util.spec_from_file_location(
    "ame_names_ru", Path(__file__).resolve().parent / "_ame_names_ru.py"
)
_names_mod = importlib.util.module_from_spec(_names_spec)
assert _names_spec and _names_spec.loader
_names_spec.loader.exec_module(_names_mod)
AME_NAME_RU = _names_mod.AME_NAME_RU
AME_NICK_RU = _names_mod.AME_NICK_RU

SECTION = "JAZZ-UNITS-005-AME"
ITEMS_BEGIN = f"-- {SECTION}-BEGIN"
ITEMS_END = f"-- {SECTION}-END"
META_CODE_BEGIN = f"-- {SECTION}-CODE-BEGIN"
META_CODE_END = f"-- {SECTION}-CODE-END"
META_RES_BEGIN = f"-- {SECTION}-RES-BEGIN"
META_RES_END = f"-- {SECTION}-RES-END"
JAZZ_CODE_BEGIN = f"-- {SECTION}-JAZZ-CODE-BEGIN"
JAZZ_CODE_END = f"-- {SECTION}-JAZZ-CODE-END"
LOC_BEGIN = f"# {SECTION}-LOC-BEGIN"
LOC_END = f"# {SECTION}-LOC-END"

MERC_LOC_BASE = 890000000005100
MERC_LOC_STRIDE = 10
NAT_LOC_BASE = 890000000005021

STAT_ORDER = (
    "Health",
    "Agility",
    "Dexterity",
    "Strength",
    "Wisdom",
    "Will",
    "Leadership",
    "Marksmanship",
    "Mechanical",
    "Explosives",
    "Medical",
)

AMMO_MAP: dict[str, str] = {
    ".44": "JAZZ_AMMO_44CAL_FMJ",
    ".38": "JAZZ_AMMO_38special_FMJ",
    ".45": "JAZZ_AMMO_45ACP_FMJ",
    "9mm": "JAZZ_AMMO_9x19_FMJ",
    "9x18": "JAZZ_AMMO_9x18_FMJ",
    "12g": "JAZZ_AMMO_12gauge_Buckshot",
    "7.92Kurz": "JAZZ_AMMO_792x33_FMJ",
    "7.5French": "JAZZ_AMMO_75French_FMJ",
    ".30-06": "JAZZ_AMMO_30_FMJ",
    "5.56": "JAZZ_AMMO_556_FMJ",
    "7.62x25": "JAZZ_AMMO_762x25_FMJ",
    "7.62Tok": "JAZZ_AMMO_762x25_FMJ",
}

CONSUMABLE_MAP: dict[str, str] = {
    "Bandage": "JAZZ_Bandage",
    "Morphine": "JAZZ_Morphine",
    "Stim": "CombatStim",
    # Design aliases → real InventoryItem ids (vanilla has no Toolkit / HE_Charge).
    "Toolkit": "Wirecutter",
    "HE_Charge": "ShapedCharge",
}

NON_FIREARM_ITEMS = frozenset(
    {
        "Bandage",
        "FragGrenade",
        "Morphine",
        "Stim",
        "HE_Charge",
        "ShapedCharge",
        "TNT",
        "PipeBomb",
        "Detonator",
        "Toolkit",
        "Wirecutter",
        "Crowbar",
        "Lockpick",
        "Medkit",
        "Molotov",
    }
)

# (id, ru, en, flag icon path relative to jazz mod root via Mod/<jazz-id>/)
JAZZ_MOD_ID = "e6L4ECj"
NATIONALITIES: list[tuple[str, str, str, str]] = [
    ("Nigeria", "Нигерия", "Nigeria", f"Mod/{JAZZ_MOD_ID}/Icons/Flags/f_nigeria.png"),
    ("Kenya", "Кения", "Kenya", f"Mod/{JAZZ_MOD_ID}/Icons/Flags/f_kenya.png"),
    ("Angola", "Ангола", "Angola", f"Mod/{JAZZ_MOD_ID}/Icons/Flags/f_angola.png"),
    ("Mali", "Мали", "Mali", f"Mod/{JAZZ_MOD_ID}/Icons/Flags/f_mali.png"),
    ("Congo", "Конго", "Congo", f"Mod/{JAZZ_MOD_ID}/Icons/Flags/f_congo.png"),
    ("Ghana", "Гана", "Ghana", f"Mod/{JAZZ_MOD_ID}/Icons/Flags/f_ghana.png"),
    ("Senegal", "Сенегал", "Senegal", f"Mod/{JAZZ_MOD_ID}/Icons/Flags/f_senegal.png"),
    ("Ethiopia", "Эфиопия", "Ethiopia", f"Mod/{JAZZ_MOD_ID}/Icons/Flags/f_ethiopia.png"),
]

UI_STRINGS: list[tuple[int, str, str, str]] = [
    (890000000005000, "Африканская биржа наёмников", "A.M.E. Exchange", "AME_UI"),
    (890000000005001, "Новобранцы", "Irregulars", "AME_Filter"),
    (890000000005002, "Irregulars", "Irregulars", "AME_Filter"),
    (890000000005003, "Бойцы", "Fighters", "AME_Filter"),
    (890000000005004, "Fighters", "Fighters", "AME_Filter"),
    (890000000005005, "Закалённые", "Hardened", "AME_Filter"),
    (890000000005006, "Hardened", "Hardened", "AME_Filter"),
    (890000000005007, "Специалисты", "Specialists", "AME_Filter"),
    (890000000005008, "Specialists", "Specialists", "AME_Filter"),
    (890000000005009, "Все", "All", "AME_Filter"),
    (890000000005010, "All", "All", "AME_Filter"),
    (890000000005011, "Моя команда [<AMEPlayerMercCount()>]", "My Team [<AMEPlayerMercCount()>]", "AME_Filter"),
    (890000000005012, "My%20Team", "My%20Team", "AME_Filter"),
    (890000000005013, "http://www.ame-exchange.net/", "http://www.ame-exchange.net/", "AME_Browser"),
    (890000000005014, "http://www.ame-exchange.net/Roster/", "http://www.ame-exchange.net/Roster/", "AME_Browser"),
    (890000000005015, "Низкий", "Low", "AME_Potential"),
    (890000000005016, "Средний", "Medium", "AME_Potential"),
    (890000000005017, "Высокий", "High", "AME_Potential"),
    (890000000005018, "Категория:", "Category:", "AME_UI"),
    (890000000005019, "Потенциал:", "Potential:", "AME_UI"),
    (890000000005020, "Африканская биржа наёмников", "African Mercenary Exchange", "AME_UI"),
    (
        890000000005049,
        "<style AimCopyrightTextC><copyright></style> A.M.E. 2001",
        "<style AimCopyrightTextC><copyright></style> A.M.E. 2001",
        "AME_Browser_copyright",
    ),
    (890000000006890, "Об A.M.E.", "About A.M.E.", "AME_Browser_about_title"),
    (
        890000000006891,
        "Африканская биржа наёмников сводит нанимателей с местными бойцами до того, как известность сделает их дорогими. Мы проверяем имена, доступность и условия; выбирать всё равно вам. Хороший контракт может дать человеку будущее. Плохой обычно освобождает место в списке.",
        "The African Mercenary Exchange connects employers with local fighters before reputation makes them expensive. We verify names, availability, and terms; judgment remains yours. A good contract can make a career. A bad one usually makes a vacancy.",
        "AME_Browser_about_body",
    ),
    (890000000006892, "Условия A.M.E.", "A.M.E. terms", "AME_Browser_terms_title"),
    (
        890000000006893,
        "A.M.E. подтверждает личность и доступность, но не храбрость, здравый смысл или удачу. Оплата, лечение, перевозка и похороны остаются делом нанимателя и бойца. С погибших биржа комиссию не берёт.",
        "A.M.E. confirms identity and availability, not courage, judgment, or luck. Pay, medical care, transport, and burial arrangements are settled between employer and contractor. The board takes no commission from the dead.",
        "AME_Browser_terms_body",
    ),
    (890000000006990, "Ушёл в Легион", "Joined the Legion", "AME_Terminal"),
    (
        890000000006991,
        "<style PDAMercPrice_Dead>Погиб в бою</style>",
        "<style PDAMercPrice_Dead>Killed in action</style>",
        "AME_Terminal",
    ),
    (
        890000000006992,
        "Подписал контракт с другим нанимателем",
        "Signed with another employer",
        "AME_Terminal",
    ),
]


def load_roster_module():
    spec = importlib.util.spec_from_file_location("gen_ame_roster_60", ROSTER_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load roster module: {ROSTER_SCRIPT}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    roster = mod.ROSTER
    if len(roster) != 60:
        raise RuntimeError(f"ROSTER must have 60 entries, got {len(roster)}")
    return mod


def lua_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def t_expr(tid: int, text: str, comment: str = "") -> str:
    suffix = f" --[[{comment}]]" if comment else ""
    return f'T({tid}, "{lua_escape(text)}"){suffix}'


def merc_loc_ids(slot: int) -> dict[str, int]:
    base = MERC_LOC_BASE + (slot - 1) * MERC_LOC_STRIDE
    return {
        "name": base + 0,
        "nick": base + 1,
        "allcaps": base + 2,
        "bio": base + 3,
        "offline": base + 4,
        "greeting": base + 5,
        "parting": base + 6,
    }


def slot_id(slot: int) -> str:
    return f"JAZZ_AME_{slot:02d}"


_TITLE_PREFIXES = (
    "Dr.",
    "Doctor",
    "Captain",
    "Capt.",
    "Sgt.",
    "Sergeant",
)


def display_nick(m: dict) -> str:
    """Hire UI uses Nick (list/chat/URL). Keep it short; Name stays full formal.

    Hire portrait tiles clip around ~9 glyphs — hyphenated given names
    (Jean-Baptiste) use the first segment; oversize tokens are truncated.
    """
    explicit = m.get("nick")
    if explicit:
        return explicit
    name = (m.get("name") or "").strip()
    return _short_given_from_full(name)


def _short_given_from_full(name: str) -> str:
    """Strip titles, take given name, hyphen→first segment, max 9 glyphs."""
    name = (name or "").strip()
    changed = True
    while changed and name:
        changed = False
        for title in _TITLE_PREFIXES:
            if name.lower().startswith(title.lower()):
                name = name[len(title) :].lstrip(" .")
                changed = True
                break
    # RU titles in name_ru forms.
    for title in ("Доктор", "Капитан", "Сержант", "Майор"):
        if name.startswith(title):
            name = name[len(title) :].lstrip(" .")
    parts = [p for p in name.replace(",", " ").split() if p]
    if not parts:
        return name or "Merc"
    given = parts[0]
    if "-" in given:
        given = given.split("-", 1)[0].strip() or given
    if len(given) > 9:
        given = given[:9]
    return given


def allcaps_nick(m: dict) -> str:
    return display_nick(m).upper()


def full_name_en(m: dict) -> str:
    name = m.get("name") or ""
    nick = m.get("nick")
    if not nick:
        return name
    parts = name.split()
    if len(parts) < 2:
        return f'{name} "{nick}"'
    return f'{parts[0]} "{nick}" {" ".join(parts[1:])}'


def name_ru(m: dict) -> str:
    en = m.get("name") or ""
    name = AME_NAME_RU.get(en)
    if not name:
        raise SystemExit(f"missing AME_NAME_RU for {en!r}")
    nick = m.get("nick")
    if not nick:
        return name
    nick_ru = AME_NICK_RU.get(nick, nick)
    parts = name.split()
    if len(parts) < 2:
        return f'{name} "{nick_ru}"'
    return f'{parts[0]} "{nick_ru}" {" ".join(parts[1:])}'


def display_nick_ru(m: dict) -> str:
    explicit = m.get("nick")
    if explicit:
        return AME_NICK_RU.get(explicit, explicit)
    return _short_given_from_full(name_ru(m))


def allcaps_nick_ru(m: dict) -> str:
    return display_nick_ru(m).upper()


def nat_display_en(nat: str) -> str:
    for nat_id, _ru, en, _icon in NATIONALITIES:
        if nat_id == nat:
            return en
    if nat == "GrandChien":
        return "Grand Chien"
    if nat == "SouthAfrica":
        return "South Africa"
    return nat


def resolve_ammo(caliber: str, last_weapon: str | None) -> str:
    if caliber == "7.62":
        if last_weapon == "Gewehr98":
            return "JAZZ_AMMO_792_FMJ"
        if last_weapon in ("SKS", "Type56"):
            return "JAZZ_AMMO_762x39_FMJ"
        return "JAZZ_AMMO_762x39_FMJ"
    item = AMMO_MAP.get(caliber)
    if not item:
        raise ValueError(f"unknown ammo caliber {caliber!r} (weapon={last_weapon!r})")
    return item


def is_ammo_token(name: str) -> bool:
    if name in AMMO_MAP:
        return True
    if name == "7.62":
        return True
    return name.startswith(".") or name.endswith("mm") or name.endswith("g") or "Kurz" in name or "French" in name


def parse_inv(inv: str) -> list[tuple[str, int]]:
    """Return [(item_id, stack_count), ...]."""
    out: list[tuple[str, int]] = []
    last_weapon: str | None = None
    for raw in inv.split("·"):
        tok = raw.strip()
        if not tok or tok.startswith("—") or tok == "(empty hands)":
            continue
        if "×" in tok:
            name, count_s = tok.rsplit("×", 1)
            name = name.strip()
            count = int(count_s.strip())
            if is_ammo_token(name):
                out.append((resolve_ammo(name, last_weapon), count))
            else:
                item_id = CONSUMABLE_MAP.get(name, name)
                out.append((item_id, count))
            continue
        item_id = CONSUMABLE_MAP.get(tok, tok)
        out.append((item_id, 1))
        if tok not in NON_FIREARM_ITEMS and tok not in CONSUMABLE_MAP:
            last_weapon = tok
    return out


def loot_entry_rows(items: list[tuple[str, int]]) -> list[str]:
    rows: list[str] = []
    for item_id, count in items:
        if count <= 1:
            rows.append(f"\t\tPlaceObj('LootEntryInventoryItem', {{ item = \"{item_id}\" }}),")
        else:
            rows.append(
                f"\t\tPlaceObj('LootEntryInventoryItem', {{ item = \"{item_id}\", "
                f"stack_min = {count}, stack_max = {count} }}),"
            )
    return rows


def perks_lua(traits: list[str]) -> str:
    if not traits:
        return "\tStartingPerks = {},"
    lines = ["\tStartingPerks = {"]
    for t in traits:
        lines.append(f'\t"{t}",')
    lines.append("\t},")
    return "\n".join(lines)


def chat_copy(cat: str) -> dict[str, tuple[str, str]]:
    copy = {
        "Irregulars": {
            "offline": ("You're through. I'm listening.", "Вы дозвонились. Слушаю."),
            "greeting": ("I'm looking for work. What do you have?", "Ищу работу. Что предлагаете?"),
            "parting": ("All right. Speak soon.", "Хорошо. До связи."),
        },
        "Fighters": {
            "offline": ("On the line.", "На связи."),
            "greeting": ("I'm listening. Tell me about the job.", "Слушаю. Расскажите о работе."),
            "parting": ("Understood. I'll be here.", "Понял. Я буду на связи."),
        },
        "Hardened": {
            "offline": ("I'm here. Talk.", "Я на линии. Говорите."),
            "greeting": ("If there's work, I'm listening.", "Если есть работа — слушаю."),
            "parting": ("Send the terms.", "Присылайте условия."),
        },
        "Specialists": {
            "offline": ("I'm available. We can discuss a contract.", "На связи. Можем обсудить контракт."),
            "greeting": ("Go ahead. Tell me what the job needs.", "Слушаю. Что требуется для этой работы?"),
            "parting": ("Understood. I will wait for your terms.", "Понятно. Буду ждать ваших условий."),
        },
    }
    return copy[cat]


def render_companion(slot: int, m: dict, mod) -> str:
    uid = slot_id(slot)
    loc = merc_loc_ids(slot)
    voice = mod.voice_for(m)
    fallback = mod.voice_fallback(m) if hasattr(mod, "voice_fallback") else voice
    appearance = mod.appearance_for(m, slot)
    gender = "Female" if m.get("female") else "Male"
    nick = display_nick(m)
    caps = allcaps_nick(m)
    chat = chat_copy(m["cat"])
    stats = m["stats"]
    portrait = f"Mod/Dv3mFVN/MercPortraits/{uid}.png"
    big = f"Mod/Dv3mFVN/MercPortraits/{uid}_Big.png"

    stat_lines = [f"\t{k} = {stats[k]}," for k in STAT_ORDER]
    lines = [
        f"UndefineClass('{uid}')",
        f"DefineClass.{uid} = {{",
        '\t__parents = { "UnitData" },',
        '\t__generated_by_class = "ModItemUnitDataCompositeDef",',
        "",
        '\tobject_class = "UnitData",',
        '\tAffiliation = "AME",',
        *stat_lines,
        f'\tPortrait = "{portrait}",',
        f'\tBigPortrait = "{big}",',
        "\tIsMercenary = true,",
        f"\tName = {t_expr(loc['name'], full_name_en(m), f'ModItemUnitDataCompositeDef {uid} Name')},",
        f"\tNick = {t_expr(loc['nick'], nick, f'ModItemUnitDataCompositeDef {uid} Nick')},",
        f"\tAllCapsNick = {t_expr(loc['allcaps'], caps, f'ModItemUnitDataCompositeDef {uid} AllCapsNick')},",
        f"\tBio = {t_expr(loc['bio'], m['bio_en'], f'ModItemUnitDataCompositeDef {uid} Bio')},",
        f'\tNationality = "{m["nat"]}",',
        f"\tHireStatus = \"NotMet\",",
        f'\tAMECategory = "{m["cat"]}",',
        f'\tAMERole = "{m["role"]}",',
        f"\tOffline = {{ PlaceObj('ChatMessage', {{ 'Text', {t_expr(loc['offline'], chat['offline'][0])} }}) }},",
        f"\tGreetingAndOffer = {{ PlaceObj('ChatMessage', {{ 'Text', {t_expr(loc['greeting'], chat['greeting'][0])} }}) }},",
        f"\tPartingWords = {{ PlaceObj('ChatMessage', {{ 'Text', {t_expr(loc['parting'], chat['parting'][0])} }}) }},",
        '\tMedicalDeposit = "none",',
        f"\tStartingSalary = {m['salary']},",
        f"\tStartingLevel = {m['lvl']},",
        perks_lua(m.get("traits") or []),
        f'\tSpecialization = "{m["spec"]}",',
        f"\tMaxHitPoints = {stats['Health']},",
        f"\tAppearancesList = {{ PlaceObj('AppearanceWeight', {{ 'Preset', \"{appearance}\" }}) }},",
        f'\tEquipment = {{ "Loot_{uid}" }},',
        f'\tgender = "{gender}",',
        f'\tVoiceResponseId = "{voice}",',
        f'\tFallbackMissingVR = "{fallback}",',
        "\tDaysUntilOnline = 0,",
        "}",
        "",
    ]
    return "\n".join(lines)


def render_items_block(roster: list[dict], mod) -> str:
    loot_blocks: list[str] = []
    unit_folders: list[str] = []

    for i, m in enumerate(roster, 1):
        uid = slot_id(i)
        loot_id = f"Loot_{uid}"
        inv_items = parse_inv(m["inv"])
        loot_entries = "\n".join(loot_entry_rows(inv_items))
        loot_blocks.append(
            "\t\tPlaceObj('ModItemLootDef', {\n"
            f'\t\t\tComment = "AME merc {i:02d}",\n'
            '\t\t\tgroup = "Mercs",\n'
            f'\t\t\tid = "{loot_id}",\n'
            '\t\t\tloot = "all",\n'
            f"{loot_entries}\n"
            "\t\t}),"
        )

        loc = merc_loc_ids(i)
        voice = mod.voice_for(m)
        fallback = mod.voice_fallback(m) if hasattr(mod, "voice_fallback") else voice
        appearance = mod.appearance_for(m, i)
        gender = "Female" if m.get("female") else "Male"
        nick = display_nick(m)
        caps = allcaps_nick(m)
        stats = m["stats"]
        portrait = f"Mod/Dv3mFVN/MercPortraits/{uid}.png"
        big = f"Mod/Dv3mFVN/MercPortraits/{uid}_Big.png"
        chat = chat_copy(m["cat"])

        perk_lines = ""
        if m.get("traits"):
            perk_lines = "\n".join(f"\t\t\t\t'{p}'," for p in m["traits"])

        unit_folders.append(
            f"\t\tPlaceObj('ModItemFolder', {{\n"
            f"\t\t\t'name', \"{uid}\",\n"
            f"\t\t}}, {{\n"
            f"\t\t\tPlaceObj('ModItemUnitDataCompositeDef', {{\n"
            f"\t\t\t\t'Group', \"MercenariesNew\",\n"
            f"\t\t\t\t'Id', \"{uid}\",\n"
            f"\t\t\t\t'comment', \"AME slot {i:02d}\",\n"
            f"\t\t\t\t'object_class', \"UnitData\",\n"
            f"\t\t\t\t'Affiliation', \"AME\",\n"
            + "".join(f"\t\t\t\t'{k}', {stats[k]},\n" for k in STAT_ORDER)
            + f"\t\t\t\t'Portrait', \"{portrait}\",\n"
            f"\t\t\t\t'BigPortrait', \"{big}\",\n"
            f"\t\t\t\t'IsMercenary', true,\n"
            f"\t\t\t\t'Name', {t_expr(loc['name'], full_name_en(m), f'ModItemUnitDataCompositeDef {uid} Name')},\n"
            f"\t\t\t\t'Nick', {t_expr(loc['nick'], nick, f'ModItemUnitDataCompositeDef {uid} Nick')},\n"
            f"\t\t\t\t'AllCapsNick', {t_expr(loc['allcaps'], caps, f'ModItemUnitDataCompositeDef {uid} AllCapsNick')},\n"
            f"\t\t\t\t'Bio', {t_expr(loc['bio'], m['bio_en'], f'ModItemUnitDataCompositeDef {uid} Bio')},\n"
            f"\t\t\t\t'Nationality', \"{m['nat']}\",\n"
            f"\t\t\t\t'HireStatus', \"NotMet\",\n"
            f"\t\t\t\t'AMECategory', \"{m['cat']}\",\n"
            f"\t\t\t\t'AMERole', \"{m['role']}\",\n"
            f"\t\t\t\t'Offline', {{ PlaceObj('ChatMessage', {{ 'Text', {t_expr(loc['offline'], chat['offline'][0])} }}) }},\n"
            f"\t\t\t\t'GreetingAndOffer', {{ PlaceObj('ChatMessage', {{ 'Text', {t_expr(loc['greeting'], chat['greeting'][0])} }}) }},\n"
            f"\t\t\t\t'PartingWords', {{ PlaceObj('ChatMessage', {{ 'Text', {t_expr(loc['parting'], chat['parting'][0])} }}) }},\n"
            f"\t\t\t\t'MedicalDeposit', \"none\",\n"
            f"\t\t\t\t'StartingSalary', {m['salary']},\n"
            f"\t\t\t\t'StartingLevel', {m['lvl']},\n"
            + (f"\t\t\t\t'StartingPerks', {{\n{perk_lines}\n\t\t\t\t}},\n" if perk_lines else "")
            + f"\t\t\t\t'Specialization', \"{m['spec']}\",\n"
            f"\t\t\t\t'MaxHitPoints', {stats['Health']},\n"
            f"\t\t\t\t'AppearancesList', {{\n"
            f"\t\t\t\t\tPlaceObj('AppearanceWeight', {{\n"
            f"\t\t\t\t\t\t'Preset', \"{appearance}\",\n"
            f"\t\t\t\t\t}}),\n"
            f"\t\t\t\t}},\n"
            f"\t\t\t\t'Equipment', {{ \"{loot_id}\" }},\n"
            f"\t\t\t\t'gender', \"{gender}\",\n"
            f"\t\t\t\t'VoiceResponseId', \"{voice}\",\n"
            f"\t\t\t\t'FallbackMissingVR', \"{fallback}\",\n"
            f"\t\t\t\t'DaysUntilOnline', 0,\n"
            f"\t\t\t}}),\n"
            f"\t\t}}),"
        )

    body = (
        f"{ITEMS_BEGIN}\n"
        "\tPlaceObj('ModItemFolder', {\n"
        '\t\t\'name\', "JAZZ AME Mercs",\n'
        '\t\t\'comment\', "JAZZ-UNITS-005 generated pool",\n'
        "\t}, {\n"
        + "\n".join(loot_blocks)
        + "\n"
        + "\n".join(unit_folders)
        + "\n\t}),\n"
        f"{ITEMS_END}"
    )
    return body


def replace_marked_block(text: str, begin: str, end: str, new_block: str) -> str:
    pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end), re.S)
    if pattern.search(text):
        return pattern.sub(new_block, text, count=1)
    return text


def patch_items_lua(text: str, block: str) -> str:
    text = replace_marked_block(text, ITEMS_BEGIN, ITEMS_END, block)
    if ITEMS_BEGIN in text:
        # Drop accidental lone-comma lines left by older generator inserts.
        text = re.sub(r"\n,\n(?=" + re.escape(ITEMS_BEGIN) + r")", "\n", text)
        return text
    if not text.rstrip().endswith("}"):
        raise RuntimeError("items.lua does not end with '}'")
    # Previous root entry already ends with `}),` — do not emit a lone `,` line.
    insert = "\n" + block + "\n"
    idx = text.rstrip().rfind("}")
    return text[:idx] + insert + text[idx:]


def patch_units_metadata_code(text: str, roster: list[dict]) -> str:
    lines = [f'\t\t"UnitData/{slot_id(i)}.lua",' for i in range(1, len(roster) + 1)]
    block = (
        f"\n\t\t{META_CODE_BEGIN}\n"
        + "\n".join(lines)
        + f"\n\t\t{META_CODE_END}\n"
    )
    text = replace_marked_block(text, META_CODE_BEGIN, META_CODE_END, block.strip("\n"))
    if META_CODE_BEGIN in text:
        return text
    anchor = '\t\t"UnitData/JAZZ_Merc_Spouke.lua",'
    if anchor not in text:
        raise RuntimeError("metadata code anchor JAZZ_Merc_Spouke.lua not found")
    return text.replace(anchor, anchor + block, 1)


def patch_units_metadata_resources(text: str, roster: list[dict]) -> str:
    presets: list[str] = []
    for i in range(1, len(roster) + 1):
        uid = slot_id(i)
        loot_id = f"Loot_{uid}"
        presets.append(
            "\t\tPlaceObj('ModResourcePreset', {\n"
            '\t\t\t\'Class\', "UnitDataCompositeDef",\n'
            f"\t\t\t'Id', \"{uid}\",\n"
            '\t\t\t\'ClassDisplayName\', "Unit",\n'
            "\t\t}),"
        )
        presets.append(
            "\t\tPlaceObj('ModResourcePreset', {\n"
            '\t\t\t\'Class\', "LootDef",\n'
            f"\t\t\t'Id', \"{loot_id}\",\n"
            '\t\t\t\'ClassDisplayName\', "Loot definition",\n'
            "\t\t}),"
        )
    block = f"\n\t\t{META_RES_BEGIN}\n" + "\n".join(presets) + f"\n\t\t{META_RES_END}"
    text = replace_marked_block(text, META_RES_BEGIN, META_RES_END, block.strip("\n"))
    if META_RES_BEGIN in text:
        return text
    anchor = "'Id', \"JAZZ_Merc_Spouke\","
    idx = text.find(anchor)
    if idx == -1:
        raise RuntimeError("metadata resource anchor JAZZ_Merc_Spouke not found")
    end = text.find("}),", idx)
    if end == -1:
        raise RuntimeError("metadata resource anchor close not found")
    end += 3
    return text[:end] + block + text[end:]


def bump_version(text: str) -> tuple[str, int, int]:
    m = re.search(r"'version', (\d+),", text)
    if not m:
        raise RuntimeError("metadata version not found")
    old = int(m.group(1))
    new = old + 1
    text = text.replace(f"'version', {old},", f"'version', {new},", 1)
    return text, old, new


def append_last_changes(text: str, bullet: str) -> str:
    """Append a bullet to metadata last_changes using Lua \\n escapes (never raw LF)."""
    if bullet.strip("- ") in text:
        return text
    m = re.search(r"'last_changes',\s*\"", text)
    if not m:
        m = re.search(r"'last_changes',\s*'", text)
        if not m:
            raise RuntimeError("last_changes not found")
        inner_start = m.end()
    else:
        inner_start = m.end()
    # File must contain backslash + n, not a real newline (breaks ModDef parse).
    ins = f"- {bullet}\\n"
    return text[:inner_start] + ins + text[inner_start:]


# Generators must not touch last_changes; append only on explicit commit (see
# .cursor/rules/jazz-metadata-last-changes.mdc). Kept for rare manual --commit use.


def patch_jazz_metadata_code(text: str) -> str:
    path_entry = '"Code/System_AME_Nationalities.lua",'
    block = f"\n\t\t{JAZZ_CODE_BEGIN}\n\t\t{path_entry}\n\t\t{JAZZ_CODE_END}\n"
    text = replace_marked_block(text, JAZZ_CODE_BEGIN, JAZZ_CODE_END, block.strip("\n"))
    if JAZZ_CODE_BEGIN in text:
        return text
    if path_entry in text:
        return text
    anchor = '"Code/System_AME_Browser_Template.lua",'
    if anchor not in text:
        raise RuntimeError("jazz metadata AME anchor not found")
    return text.replace(anchor, anchor + block, 1)


def render_nationalities_lua() -> str:
    rows: list[str] = []
    for i, (nat_id, ru, en, icon) in enumerate(NATIONALITIES):
        tid = NAT_LOC_BASE + i
        rows.append(
            "PlaceObj('MercNationalities', {\n"
            f"\tDisplayName = {t_expr(tid, en, f'MercNationalities {nat_id} DisplayName')},\n"
            f'\tIcon = "{icon}",\n'
            f'\tid = "{nat_id}",\n'
            "})"
        )
    return (
        "-- AME nationality presets (JAZZ-UNITS-005).\n"
        + "\n\n".join(rows)
        + "\n"
    )


def collect_loc_rows(roster: list[dict]) -> list[tuple[int, str, str, str]]:
    rows: list[tuple[int, str, str, str]] = []
    rows.extend(UI_STRINGS)
    for j, (nat_id, ru, en, _icon) in enumerate(NATIONALITIES):
        rows.append((NAT_LOC_BASE + j, ru, en, f"AME_Nationality_{nat_id}"))
    for slot, m in enumerate(roster, 1):
        loc = merc_loc_ids(slot)
        uid = slot_id(slot)
        nick = display_nick(m)
        caps = allcaps_nick(m)
        chat = chat_copy(m["cat"])
        rows.extend(
            [
                (loc["name"], name_ru(m), full_name_en(m), uid),
                (loc["nick"], display_nick_ru(m), nick, uid),
                (loc["allcaps"], allcaps_nick_ru(m), caps, uid),
                (loc["bio"], m["bio"], m["bio_en"], uid),
                (loc["offline"], chat["offline"][1], chat["offline"][0], uid),
                (loc["greeting"], chat["greeting"][1], chat["greeting"][0], uid),
                (loc["parting"], chat["parting"][1], chat["parting"][0], uid),
            ]
        )
    return rows


def patch_loc_csv(path: Path, rows: list[tuple[int, str, str, str]]) -> int:
    if not path.exists():
        raise RuntimeError(f"missing loc file: {path}")
    from _apply_ris_editorial import LocEntry, parse_csv_document, upsert_runtime_csv

    entries = {
        str(tid): LocEntry(
            source_en=en,
            russian=ru,
            english=en,
            context=ctx,
            category="ame",
            locations="",
        )
        for tid, ru, en, ctx in rows
    }
    language = "russian" if path.name.lower().startswith("russian") else "english"
    document = parse_csv_document(path, path.read_bytes())
    updated = upsert_runtime_csv(
        document,
        entries,
        language=language,
        label=path.name,
    )
    path.write_bytes(updated.render())
    return len(rows)


def copy_portraits(roster: list[dict]) -> tuple[int, int]:
    src_dir = JAZZ_UNITS / "MercPortraits"
    donors = ("Bull", "Blade", "Carlos", "Gamos")
    donor = next((d for d in donors if (src_dir / f"{d}.png").exists()), None)
    if not donor:
        print("WARNING: no placeholder portrait donor found", file=sys.stderr)
        return 0, len(roster)
    src = src_dir / f"{donor}.png"
    src_big = src_dir / f"{donor}_Big.png"
    copied = 0
    skipped = 0
    for i in range(1, len(roster) + 1):
        uid = slot_id(i)
        dst = src_dir / f"{uid}.png"
        dst_big = src_dir / f"{uid}_Big.png"
        if not dst.exists():
            shutil.copy2(src, dst)
            copied += 1
        if src_big.exists():
            if not dst_big.exists():
                shutil.copy2(src_big, dst_big)
                copied += 1
        elif not dst_big.exists():
            skipped += 1
    return copied, skipped


def write_companions(roster: list[dict], mod) -> int:
    out_dir = JAZZ_UNITS / "UnitData"
    out_dir.mkdir(parents=True, exist_ok=True)
    for i, m in enumerate(roster, 1):
        path = out_dir / f"{slot_id(i)}.lua"
        path.write_text(render_companion(i, m, mod), encoding="utf-8")
    return len(roster)


def main() -> int:
    mod = load_roster_module()
    roster = mod.ROSTER

    companions = write_companions(roster, mod)
    items_block = render_items_block(roster, mod)
    items_path = JAZZ_UNITS / "items.lua"
    items_text = items_path.read_text(encoding="utf-8")
    items_path.write_text(patch_items_lua(items_text, items_block), encoding="utf-8")

    units_meta_path = JAZZ_UNITS / "metadata.lua"
    units_meta = units_meta_path.read_text(encoding="utf-8")
    units_had_ame = META_CODE_BEGIN in units_meta
    units_meta = patch_units_metadata_code(units_meta, roster)
    units_meta = patch_units_metadata_resources(units_meta, roster)
    if units_had_ame:
        m = re.search(r"'version', (\d+),", units_meta)
        old_ver = new_ver = int(m.group(1)) if m else -1
    else:
        units_meta, old_ver, new_ver = bump_version(units_meta)
        # Do not append last_changes here — only on explicit commit.
    units_meta_path.write_text(units_meta, encoding="utf-8")

    nat_path = JAZZ / "Code" / "System_AME_Nationalities.lua"
    nat_path.write_text(render_nationalities_lua(), encoding="utf-8")
    jazz_meta_path = JAZZ / "metadata.lua"
    jazz_meta = jazz_meta_path.read_text(encoding="utf-8")
    jazz_had_ame = JAZZ_CODE_BEGIN in jazz_meta or "System_AME_Nationalities.lua" in jazz_meta
    jazz_meta = patch_jazz_metadata_code(jazz_meta)
    if jazz_had_ame:
        m = re.search(r"'version', (\d+),", jazz_meta)
        jazz_old = jazz_new = int(m.group(1)) if m else -1
    else:
        jazz_meta, jazz_old, jazz_new = bump_version(jazz_meta)
        # Do not append last_changes here — only on explicit commit.
    jazz_meta_path.write_text(jazz_meta, encoding="utf-8")

    loc_rows = collect_loc_rows(roster)
    ru_count = patch_loc_csv(JAZZ / "Russian.csv", loc_rows)
    en_count = patch_loc_csv(JAZZ / "English.csv", loc_rows)

    portraits_copied, portrait_warn = copy_portraits(roster)

    loot_count = len(roster)
    fixed_loc = len(UI_STRINGS) + len(NATIONALITIES)
    merc_loc = len(roster) * 7

    print("JAZZ-UNITS-005 AME generator summary")
    print(f"  roster mercs:     {len(roster)}")
    print(f"  companions:       {companions}")
    print(f"  loot defs:        {loot_count}")
    print(f"  items block:      {items_path}")
    print(f"  jazz-units meta:  version {old_ver} -> {new_ver}")
    print(f"  jazz meta:        version {jazz_old} -> {jazz_new}")
    print(f"  nationalities:    {nat_path}")
    print(f"  loc rows (RU):    {ru_count}")
    print(f"  loc rows (EN):    {en_count}")
    print(f"    fixed UI/nat:   {fixed_loc}")
    print(f"    merc/chat ids:  {merc_loc}")
    print(f"  portraits copied: {portraits_copied} (warnings/skips: {portrait_warn})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
