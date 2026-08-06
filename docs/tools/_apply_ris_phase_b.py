# -*- coding: utf-8 -*-
"""JAZZ-UI-RIS-001 Phase B: loc banks + System_RIS_Content.lua dossiers/AAR templates.

IDs: 890000000010031+ (free). Idempotent CSV append by ID.
Also ensures metadata.code lists RIS/AME mail + Phase B code files.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = 890000000011000
TAG = "JAZZ-UI-RIS-001-B"

LEGION_IDS = [
    "JAZZ_Legion_Recruit",
    "JAZZ_Legion_AssaultT1_Crusher",
    "JAZZ_Legion_AssaultT1_Grenadier",
    "JAZZ_Legion_AssaultT1_Roughneck",
    "JAZZ_Legion_AssaultT2_Pillager",
    "JAZZ_Legion_AssaultT2_Pyro",
    "JAZZ_Legion_AssaultT2_ShockTrooper",
    "JAZZ_Legion_AssaultT3_Punisher",
    "JAZZ_Legion_AssaultT3_SkullCrusher",
    "JAZZ_Legion_AssaultT4_Headsman",
    "JAZZ_Legion_FlankerT1_Warden",
    "JAZZ_Legion_FlankerT2_Scout",
    "JAZZ_Legion_FlankerT2_Skirmisher",
    "JAZZ_Legion_FlankerT3_Pathfinder",
    "JAZZ_Legion_FlankerT3_Recon",
    "JAZZ_Legion_FlankerT4_Ranger",
    "JAZZ_Legion_FrontT1_Bonemaker",
    "JAZZ_Legion_FrontT1_Marauder",
    "JAZZ_Legion_FrontT1_Rifleman",
    "JAZZ_Legion_FrontT2_Ambusher",
    "JAZZ_Legion_FrontT2_Marksman",
    "JAZZ_Legion_FrontT2_Raider",
    "JAZZ_Legion_FrontT3_Sniper",
    "JAZZ_Legion_FrontT3_Veteran",
    "JAZZ_Legion_FrontT4_Mercenary",
    "JAZZ_Legion_FrontT4_MercenarySniper",
    "JAZZ_Legion_GunnerT1_Gunner",
    "JAZZ_Legion_GunnerT2_AssaultGunner",
    "JAZZ_Legion_GunnerT2_GMPG",
    "JAZZ_Legion_GunnerT3_VeteranGunner",
    "JAZZ_Legion_GunnerT4_MercGunner",
    "JAZZ_Legion_HeavyT1_Rocketeer",
    "JAZZ_Legion_HeavyT2_Grenadier",
    "JAZZ_Legion_HeavyT3_Mortarman",
    "JAZZ_Legion_LeaderT1_Sergeant",
    "JAZZ_Legion_LeaderT2_Lieutenant",
    "JAZZ_Legion_LeaderT3_Captain",
    "JAZZ_Legion_LeaderT4_MercenaryCaptain",
]

# Short title EN / RU + body EN / RU covering Major / training / skill / fight / power.
DOSSIER_FLAVOR = {
    "Recruit": (
        "Recruit",
        "Рекрут",
        "The Major sweeps villages for warm bodies: cheap boots, a rifle if lucky, and a week of shouted drill. Recruits freeze under fire and bunch up. Dangerous only in numbers — and as a reminder that the Legion always has more.",
        "Майор выметает деревни за «тёплыми телами»: дешёвые ботинки, винтовка если повезёт, неделя орёного строя. Рекруты цепенеют под огнём и сбиваются в кучу. Опасны только числом — и как напоминание, что у Легиона всегда есть ещё.",
    ),
}

ROLE_FLAVOR = {
    "Assault": (
        "breach and smash",
        "ломают и рвут",
        "close assault, grenades, and panic in doorways",
        "ближний штурм, гранаты и паника в дверных проёмах",
        "high — once they close the gap",
        "высокая — если успеют сократить дистанцию",
    ),
    "Flanker": (
        "move quiet, hit the side",
        "ходят тихо, бьют с фланга",
        "scouting, ambush lanes, and cutting runners",
        "разведка, засады и отрезание бегущих",
        "medium-high when you ignore the edges",
        "средне-высокая, если забыть про края карты",
    ),
    "Front": (
        "hold the line and shoot straight",
        "держат линию и стреляют ровно",
        "aimed fire, overwatch, and patient kills",
        "прицельный огонь, овервотч и терпеливые убийства",
        "steady — they punish mistakes more than heroics",
        "стабильная — наказывают ошибки сильнее героизма",
    ),
    "Gunner": (
        "own a lane with automatic fire",
        "держат сектор автоогнём",
        "suppression belts and denying approaches",
        "подавление и запрет подходов",
        "high in open ground, softer in tight rooms",
        "высокая на открытом, мягче в тесных комнатах",
    ),
    "Heavy": (
        "bring the boom",
        "тащат «бум»",
        "rockets, bombs, and area denial",
        "ракеты, бомбы и запрет площади",
        "spike threat — one shot can rewrite a fight",
        "пиковая угроза — один выстрел может переписать бой",
    ),
    "Leader": (
        "keep the pack pointed",
        "держат стаю в узде",
        "orders, rally, and making rabble fight like a unit",
        "приказы, сбор и превращение сброда в отряд",
        "force multiplier — kill them early if you can",
        "мультипликатор силы — уберите их рано, если можете",
    ),
}

TIER_NOTE = {
    "T1": ("green kit and loud nerves", "сырой кит и громкие нервы"),
    "T2": ("blooded enough to push", "уже с кровью на руках, готовы давить"),
    "T3": ("trained killers, not militia", "тренированные убийцы, не ополчение"),
    "T4": ("paid steel — the Major's favorites", "платная сталь — любимчики Майора"),
}


def _parse_legion(uid: str):
    if uid.endswith("Recruit"):
        return "Recruit", None, "Recruit"
    m = re.match(r"JAZZ_Legion_(Assault|Flanker|Front|Gunner|Heavy|Leader)(T[1-4])_(.+)$", uid)
    if not m:
        return "Front", "T1", uid.split("_")[-1]
    return m.group(1), m.group(2), m.group(3)


def dossier_texts(uid: str):
    role, tier, nick = _parse_legion(uid)
    if role == "Recruit":
        return DOSSIER_FLAVOR["Recruit"]
    train_en, train_ru, fight_en, fight_ru, power_en, power_ru = ROLE_FLAVOR[role]
    t_en, t_ru = TIER_NOTE.get(tier or "T1", TIER_NOTE["T1"])
    title_en = nick.replace("GMPG", "GPMG")
    # humanize CamelCase-ish
    title_en = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", title_en)
    title_ru = title_en  # display name still from UnitData in UI; dossier title is English role nick with RU body
    # Prefer RU titles that match common nick translations where we know them — keep EN nick as title key for both, body bilingual.
    body_en = (
        f"The Major pulls {title_en} types to {train_en}. Drill is short, standards are brutal: {t_en}. "
        f"In a fight they {fight_en}. Power reading: {power_en}."
    )
    body_ru = (
        f"Майор набирает тип «{title_en}», чтобы {train_ru}. Учёба короткая, требования жёсткие: {t_ru}. "
        f"В бою они {fight_ru}. Оценка силы: {power_ru}."
    )
    return title_en, title_en, body_en, body_ru


QUEST = [
    (
        "Pierre",
        "Pierre Laurent",
        "Пьер Лоран",
        "Father's boy turned Legion face on Ernie — pride, uniforms, and a chip on his shoulder. Useful as a weather vane for how hard the Major is leaning on the island.",
        "Сын отца, ставший лицом Легиона на Эрни — гордость, форма и обида. Удобный флюгер: насколько жёстко Майор давит на остров.",
    ),
    (
        "Bastien",
        "Bastien",
        "Бастьен",
        "Local muscle with a merchant's smile. When he talks trade, listen for who really owns the road.",
        "Местная сила с улыбкой торговца. Когда говорит о сделках — слушайте, кому на самом деле принадлежит дорога.",
    ),
    (
        "TheMajor",
        "The Major",
        "Майор",
        "Not a rumor — a commander who builds an army out of fear, payroll, and stolen warehouses. Every supply brief you get is really about him.",
        "Не слух — командир, который собирает армию из страха, жалования и украденных складов. Каждый бриф о снабжении на самом деле о нём.",
    ),
    (
        "Legion",
        "Legion (faction)",
        "Легион (фракция)",
        "A private war machine wearing stolen legitimacy. Expect raids, pressed recruits, and officers who treat villages like inventory.",
        "Частная военная машина в краденой легитимности. Ждите рейдов, насильно набранных рекрутов и офицеров, для которых деревни — инвентарь.",
    ),
]


def alloc():
    state = {"i": BASE}

    def next_id():
        v = state["i"]
        state["i"] += 1
        return v

    return next_id, state


def build_rows_and_lua():
    nid, state = alloc()
    rows = []  # (id, en_source_for_T, ru, en)
    lua_parts = []

    def add(en: str, ru: str):
        i = nid()
        rows.append((str(i), en, ru, en))
        return i

    # --- UI ---
    ui = {
        "site_title": add("Recon Intelligence Services", "Разведывательная служба R.I.S."),
        "tab_bulletin": add("Bulletin", "Сводка"),
        "tab_dossiers": add("Dossiers", "Досье"),
        "tab_reports": add("Battle reports", "Боевые сводки"),
        "empty_bulletin": add(
            "No supply briefs on file yet. Watch your inbox — R.I.S. mails appear here after you receive them.",
            "Оценок снабжения пока нет. Следите за почтой — письма R.I.S. появятся здесь после получения.",
        ),
        "empty_dossiers": add(
            "No dossiers unlocked. Kill three fighters of the same Legion type to open their file.",
            "Досье ещё не открыты. Убейте трёх бойцов одного типа Легиона, чтобы открыть карточку.",
        ),
        "empty_reports": add(
            "No after-action reports yet. Finish a fight — the desk will file a summary here (no mail spam).",
            "Боевых сводок пока нет. Завершите бой — стол положит сюда отчёт (без спама в почту).",
        ),
        "kills_progress": add("Observed kills: <count>/3", "Зафиксировано убийств: <count>/3"),
        "dossier_locked": add("(sealed — need 3 confirmed kills)", "(запечатано — нужно 3 подтверждённых убийства)"),
        "section_quest": add("Persons of interest", "Особые фигуры"),
        "section_legion": add("Legion types", "Типы Легиона"),
        "supply_header": add("Latest supply assessment", "Последняя оценка снабжения"),
        "mail_archive": add("R.I.S. mail archive", "Архив писем R.I.S."),
    }

    # --- Dossiers ---
    dossier_map = []
    for uid in LEGION_IDS:
        title_en, title_ru, body_en, body_ru = dossier_texts(uid)
        tid = add(title_en, title_ru)
        bid = add(body_en, body_ru)
        dossier_map.append((uid, tid, bid))

    quest_map = []
    for qid, ten, tru, ben, bru in QUEST:
        tid = add(ten, tru)
        bid = add(ben, bru)
        quest_map.append((qid, tid, bid))

    # --- AAR banks ---
    headlines = {
        ("win", "low"): [
            ("Quiet clearance", "Тихая зачистка"),
            ("Sector secured without fireworks", "Сектор взят без фейерверка"),
            ("Low noise, clean finish", "Мало шума, чистый финиш"),
        ],
        ("win", "mid"): [
            ("Hard fight, held the ground", "Жёсткий бой — землю удержали"),
            ("They pushed; you pushed back", "Они давили — вы ответили"),
            ("Victory with bruised knuckles", "Победа с разбитыми костяшками"),
        ],
        ("win", "high"): [
            ("Blood bath — and you walked out", "Мясорубка — и вы вышли"),
            ("The Major will hear about this", "Майор об этом услышит"),
            ("Thunder over the sector", "Гром над сектором"),
        ],
        ("loss", "low"): [
            ("Forced back, light losses", "Отошли — потери лёгкие"),
            ("Probe failed", "Прощупывание провалилось"),
            ("Bad ground, worse timing", "Плохой грунт, хуже тайминг"),
        ],
        ("loss", "mid"): [
            ("Beaten off the field", "Сбиты с поля"),
            ("They kept the sector", "Сектор остался у них"),
            ("Retreat under fire", "Отход под огнём"),
        ],
        ("loss", "high"): [
            ("Rout — write it honestly", "Разгром — пишите честно"),
            ("The desk calls it a disaster", "Стол называет это катастрофой"),
            ("Smoke and empty stretchers", "Дым и пустые носилки"),
        ],
        ("retreat", "low"): [
            ("Ordered withdrawal", "Организованный отход"),
            ("You left before it got expensive", "Ушли, пока не стало дорого"),
            ("Discretion over medals", "Осторожность вместо медалей"),
        ],
        ("retreat", "mid"): [
            ("Pulled out under pressure", "Вытянули под давлением"),
            ("Falling back to fight another day", "Отходим, чтобы биться завтра"),
            ("The line wouldn't hold", "Линия не держалась"),
        ],
        ("retreat", "high"): [
            ("Bloody extraction", "Кровавая эвакуация"),
            ("Ran the gauntlet out", "Проскочили коридор наружу"),
            ("Survival first, pride later", "Сначала выжить — гордость потом"),
        ],
    }

    hl_ids = {}
    for key, variants in headlines.items():
        ids = []
        for en, ru in variants:
            ids.append(add(en, ru))
        hl_ids[key] = ids

    weather = {
        "clear": add("Weather: clear skies over the fight.", "Погода: ясное небо над боем."),
        "rain": add("Weather: rain turned powder damp and tempers shorter.", "Погода: дождь отсырел порох и укоротил нервы."),
        "night": add("Weather/time: night fight — muzzle flashes did the talking.", "Погода/время: ночной бой — говорили вспышки дул."),
        "fog": add("Weather: fog cut sightlines; everyone hugged cover.", "Погода: туман резал обзор; все жались к укрытиям."),
        "heat": add("Weather: baking heat — fatigue hit as hard as bullets.", "Погода: пекло — усталость била не хуже пуль."),
        "dust": add("Weather: dust storm grit in every weapon.", "Погода: пылевая буря — песок в каждом стволе."),
        "default": add("Weather: unremarkable — the shooting was the story.", "Погода: обычная — историю сделала стрельба."),
    }

    intensity = {
        "low": add(
            "Intensity: a sharp exchange, then quiet. Heat on the grid barely stirred.",
            "Интенсивность: короткая перестрелка, потом тишина. Жара на сетке почти не шевельнулась.",
        ),
        "mid": add(
            "Intensity: sustained fire and movement. Local Heat climbed enough for the desk to notice.",
            "Интенсивность: плотный огонь и манёвр. Местная Жара выросла так, что стол это заметил.",
        ),
        "high": add(
            "Intensity: a meat grinder. Expect the Major's network to smell the smoke.",
            "Интенсивность: мясорубка. Сеть Майора наверняка учует дым.",
        ),
    }

    forces = add(
        "Forces: roughly <player> friendlies against <enemy> hostiles at contact.",
        "Силы: примерно <player> своих против <enemy> врагов на контакте.",
    )
    sector = {
        "line": add(
            "Theatre: <sector>.",
            "Театр: <sector>.",
        ),
        "poi": add(
            "Theatre: <sector> — local label <poi>.",
            "Театр: <sector> — местная метка <poi>.",
        ),
    }
    quest = {
        "one": add(
            "Operational thread: <quest>. Desk note on this grid: <note>",
            "Операционная нить: <quest>. Заметка стола по этой клетке: <note>",
        ),
        "one_nonote": add(
            "Operational thread: <quest> — badges pin this fight to that job.",
            "Операционная нить: <quest> — бейджи привязывают этот бой к заданию.",
        ),
        "many": add(
            "Operational threads on this sector: <quests>. Treat the shooting as part of those jobs, not random noise.",
            "Операционные нити на секторе: <quests>. Считайте стрельбу частью этих заданий, не случайным шумом.",
        ),
        "active": add(
            "Active desk job (not sector-badged): <quest>.",
            "Активное задание стола (без бейджа на секторе): <quest>.",
        ),
        "none": add(
            "No live quest badge on this grid — logged as a free-fire sector action.",
            "Живого квестового бейджа на клетке нет — записано как свободный секторный бой.",
        ),
    }
    character = {
        "win": add("Character: your side held the field.", "Характер: ваша сторона удержала поле."),
        "loss": add("Character: the enemy kept the sector.", "Характер: сектор остался за врагом."),
        "retreat": add("Character: fighting withdrawal — not a stand.", "Характер: отход с боем — не стояли насмерть."),
        "ambush": add("Character: smelled like an ambush — first shots decided the map.", "Характер: похоже на засаду — первые выстрелы решили карту."),
        "quest_win": add(
            "Character: quest-linked fight — objective pressure held; the sector stayed yours.",
            "Характер: квестовый бой — давление по цели выдержали; сектор ваш.",
        ),
        "quest_loss": add(
            "Character: quest-linked fight — the job on this grid just got harder.",
            "Характер: квестовый бой — задание на этой клетке только усложнилось.",
        ),
        "quest_retreat": add(
            "Character: quest-linked withdrawal — you left the badge sector under protest.",
            "Характер: квестовый отход — ушли с бейдж-сектора не по плану.",
        ),
    }
    losses = add(
        "Losses: friendlies KIA <pkia>, WIA <pwia>; hostiles KIA <ekia>, WIA <ewia>.",
        "Потери: свои убиты <pkia>, ранены <pwia>; враги убиты <ekia>, ранены <ewia>.",
    )
    elite = {
        "killed": add(
            "<name> went down in the fight — one less elite name on the Major's roster.",
            "<name> лёг в этом бою — на одно элитное имя в списке Майора меньше.",
        ),
        "wounded": add(
            "<name> left the field bleeding. If they live, they'll remember your faces.",
            "<name> ушёл с поля истекая кровью. Если выживет — запомнит ваши лица.",
        ),
        "escaped": add(
            "<name> slipped the net. Expect that name again.",
            "<name> выскользнул из сети. Ждите это имя снова.",
        ),
        "threat": add(
            "<name> was still standing when the shooting stopped — unfinished business.",
            "<name> ещё стоял, когда стрельба стихла — незакрытый счёт.",
        ),
    }
    closing = {
        "quiet": add(
            "Closing: the sector goes quiet; Heat footprint looks manageable.",
            "Итог: сектор стихает; след Жары выглядит управляемым.",
        ),
        "noise": add(
            "Closing: the noise will travel — patrols and payoffs usually follow.",
            "Итог: шум разнесётся — обычно следом идут патрули и выплаты.",
        ),
        "disaster": add(
            "Closing: write this one in red. Command will ask hard questions.",
            "Итог: пишите красным. Командование будет спрашивать жёстко.",
        ),
    }

    # Emit Lua content file
    def tref(i, sample):
        esc = sample.replace("\\", "\\\\").replace('"', '\\"')
        return f'T({i}, "{esc}")'

    lines = [
        "-- R.I.S. Phase B content banks (generated by docs/tools/_apply_ris_phase_b.py).",
        "-- Do not hand-edit ID numbers; re-run the script.",
        "",
        "JAZZ_RIS_KILL_THRESHOLD = 3",
        "JAZZ_RIS_BATTLE_CAP = 20",
        "",
        "JAZZ_RIS_UI = {",
    ]
    for k, i in ui.items():
        sample = next(r[1] for r in rows if r[0] == str(i))
        lines.append(f"\t{k} = {tref(i, sample)},")
    lines.append("}")
    lines.append("")
    lines.append("JAZZ_RIS_DOSSIERS = {")
    for uid, tid, bid in dossier_map:
        ts = next(r[1] for r in rows if r[0] == str(tid))
        bs = next(r[1] for r in rows if r[0] == str(bid))
        lines.append(f'\t["{uid}"] = {{ title = {tref(tid, ts)}, body = {tref(bid, bs)} }},')
    lines.append("}")
    lines.append("")
    lines.append("JAZZ_RIS_QUEST_DOSSIERS = {")
    for qid, tid, bid in quest_map:
        ts = next(r[1] for r in rows if r[0] == str(tid))
        bs = next(r[1] for r in rows if r[0] == str(bid))
        lines.append(f'\t["{qid}"] = {{ title = {tref(tid, ts)}, body = {tref(bid, bs)} }},')
    lines.append("}")
    lines.append("")
    lines.append("JAZZ_RIS_AAR = {")
    lines.append("\theadlines = {")
    for (outcome, inten), ids in sorted(hl_ids.items()):
        arr = ", ".join(
            tref(i, next(r[1] for r in rows if r[0] == str(i))) for i in ids
        )
        lines.append(f'\t\t["{outcome}|{inten}"] = {{ {arr} }},')
    lines.append("\t},")
    lines.append("\tweather = {")
    for k, i in weather.items():
        s = next(r[1] for r in rows if r[0] == str(i))
        lines.append(f"\t\t{k} = {tref(i, s)},")
    lines.append("\t},")
    lines.append("\tintensity = {")
    for k, i in intensity.items():
        s = next(r[1] for r in rows if r[0] == str(i))
        lines.append(f"\t\t{k} = {tref(i, s)},")
    lines.append("\t},")
    s = next(r[1] for r in rows if r[0] == str(forces))
    lines.append(f"\tforces = {tref(forces, s)},")
    lines.append("\tsector = {")
    for k, i in sector.items():
        s = next(r[1] for r in rows if r[0] == str(i))
        lines.append(f"\t\t{k} = {tref(i, s)},")
    lines.append("\t},")
    lines.append("\tquest = {")
    for k, i in quest.items():
        s = next(r[1] for r in rows if r[0] == str(i))
        lines.append(f"\t\t{k} = {tref(i, s)},")
    lines.append("\t},")
    lines.append("\tcharacter = {")
    for k, i in character.items():
        s = next(r[1] for r in rows if r[0] == str(i))
        lines.append(f"\t\t{k} = {tref(i, s)},")
    lines.append("\t},")
    s = next(r[1] for r in rows if r[0] == str(losses))
    lines.append(f"\tlosses = {tref(losses, s)},")
    lines.append("\telite = {")
    for k, i in elite.items():
        s = next(r[1] for r in rows if r[0] == str(i))
        lines.append(f"\t\t{k} = {tref(i, s)},")
    lines.append("\t},")
    lines.append("\tclosing = {")
    for k, i in closing.items():
        s = next(r[1] for r in rows if r[0] == str(i))
        lines.append(f"\t\t{k} = {tref(i, s)},")
    lines.append("\t},")
    lines.append("}")
    lines.append("")

    return rows, "\n".join(lines) + "\n", state["i"] - 1


def append_csv(rows):
    for name in ("English.csv", "Russian.csv"):
        path = ROOT / name
        text = path.read_text(encoding="utf-8-sig")
        existing = set()
        for line in text.splitlines():
            if not line.strip() or line.startswith("sep="):
                continue
            try:
                row = next(csv.reader([line]))
            except Exception:
                continue
            if row:
                existing.add(row[0])
        additions = []
        for id_, en_src, ru, en in rows:
            if id_ in existing:
                continue
            # English.csv: id, Russian-col-as-source?, English — match project convention for AME rows
            # Observed: English.csv has id, RU text, EN text
            # Russian.csv: id, EN source?, RU — check AME
            if name == "English.csv":
                additions.append([id_, ru, en, "", TAG])
            else:
                additions.append([id_, en, ru, "", TAG])
        if not additions:
            print(name, "no new rows")
            continue
        buf = text
        if not buf.endswith("\n"):
            buf += "\n"
        for row in additions:
            # IMPORTANT: do not ",".join() the csv line — that splits every character.
            buf += _csv_line(row) + "\n"
        path.write_text(buf, encoding="utf-8-sig")
        print(name, "appended", len(additions))


def _csv_line(row):
    import io

    bio = io.StringIO()
    w = csv.writer(bio, lineterminator="")
    w.writerow(row)
    return bio.getvalue()


CODE_FILES = [
    "Code/System_AME_Mail.lua",
    "Code/System_RIS_Mail.lua",
    "Code/System_RIS_Content.lua",
    "Code/System_RIS_Combat.lua",
    "Code/System_RIS_Browser.lua",
]


def patch_metadata():
    path = ROOT / "metadata.lua"
    text = path.read_text(encoding="utf-8")
    block = "\n".join(f'\t\t"{f}",' for f in CODE_FILES)
    # Prefer replace existing RIS/AME mail cluster after AME_Market
    import re

    pat = re.compile(
        r'("Code/System_AME_Market\.lua",)\n(?:\t\t"Code/System_(?:AME_Mail|RIS_[^"]+)\.lua",\n)*',
        re.M,
    )
    if pat.search(text):
        text = pat.sub(r"\1\n" + block + "\n", text, count=1)
        path.write_text(text, encoding="utf-8")
        print("metadata: replaced RIS/AME mail code cluster")
        return
    needle = '"Code/System_AME_Market.lua",'
    if needle not in text:
        raise SystemExit("metadata: AME_Market anchor missing")
    text = text.replace(needle, needle + "\n" + block, 1)
    path.write_text(text, encoding="utf-8")
    print("metadata: inserted code cluster")


def patch_items_moditem_code():
    path = ROOT / "items.lua"
    text = path.read_text(encoding="utf-8")
    # Insert ModItemCode after LegionTierProgression block
    anchor = """\t\tPlaceObj('ModItemCode', {
\t\t\t'name', "LegionTierProgression",
\t\t\t'CodeFileName', "Code/LegionTierProgression.lua",
\t\t}),"""
    if anchor not in text:
        print("items: LegionTierProgression anchor missing — skip ModItemCode")
        return
    chunk = anchor
    for f in CODE_FILES:
        name = Path(f).stem
        if f"CodeFileName', \"{f}\"" in text or f"CodeFileName', '{f}'" in text:
            continue
        chunk += f"""
\t\tPlaceObj('ModItemCode', {{
\t\t\t'name', "{name}",
\t\t\t'CodeFileName', "{f}",
\t\t}}),"""
        print("items +", f)
    if chunk != anchor:
        text = text.replace(anchor, chunk, 1)
        path.write_text(text, encoding="utf-8")


def write_design_docs():
    dossiers = ["# R.I.S. Legion unit dossiers (canon)", "", "Unlock: ≥3 player-side kills of that `JAZZ_Legion_*` type.", "", "| UnitData id | Notes |", "| --- | --- |"]
    for uid in LEGION_IDS:
        title_en, _, body_en, _ = dossier_texts(uid)
        dossiers.append(f"| `{uid}` | **{title_en}** — {body_en[:100]}… |")
    dossiers.append("")
    dossiers.append("Quest / faction cards: Pierre, Bastien, TheMajor, Legion — unlock via IsMet / affiliation meet.")
    (ROOT / "docs/design/ris-legion-dossiers.md").write_text("\n".join(dossiers) + "\n", encoding="utf-8")

    aar = """# R.I.S. battle-report paragraph templates

Runtime: `Code/System_RIS_Content.lua` + `System_RIS_Combat.lua` (JAZZ-UI-RIS-001 Phase B).

## Slots

| Slot | Bands | Pick |
| --- | --- | --- |
| Headline | win/loss/retreat × low/mid/high × ≥3 variants | deterministic hash |
| **Sector** | display name via `GetSectorName` (+ optional POI/label) | always |
| **Quest** | `GetQuestsAssociatedWithSector` badges; else `GetActiveQuest` | one/many/active/none |
| Weather | clear / rain / night / fog / heat / dust / default | map GameState / weather |
| Intensity | low / mid / high | Heat delta + casualty rate |
| Forces | counts | `<player>` / `<enemy>` |
| Character | win / loss / retreat / ambush (+ quest_* variants) | ConflictEnd + quest link |
| Losses | KIA/WIA both sides | combat snap |
| Elite+named | killed / wounded / escaped / threat | `T{…, name=…}` per elite |
| Closing | quiet / noise / disaster | intensity × outcome |

Loc IDs allocated from `890000000011000` by `_apply_ris_phase_b.py`.
"""
    (ROOT / "docs/design/ris-battle-report-templates.md").write_text(aar, encoding="utf-8")


def main():
    rows, lua, last = build_rows_and_lua()
    out = ROOT / "Code" / "System_RIS_Content.lua"
    out.write_text(lua, encoding="utf-8")
    print("wrote", out, "last id", last, "rows", len(rows))
    append_csv(rows)
    patch_metadata()
    patch_items_moditem_code()
    write_design_docs()
    print("done")


if __name__ == "__main__":
    main()
