"""Generate docs/design/ame-roster-60.md — design cards for AME pool (JAZZ-UNITS-005)."""
from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "design" / "ame-roster-60.md"


def pot(wis: int) -> str:
    if wis < 45:
        return "Low"
    if wis < 65:
        return "Medium"
    return "High"


def stats_line(d: dict[str, int]) -> str:
    order = [
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
    ]
    return " · ".join(f"{k} {d[k]}" for k in order)


# id, name, nick|None, nat, cat, role, lvl, salary, traits, bio_ru, inv, stats
# StartingLevel always 1. Traits = Specialization only (no Bronze/Silver tree perks).
ROSTER: list[dict] = []

SPECIALIZATION_TRAITS = frozenset(
    {
        "AutoWeapons",
        "CQCTraining",
        "HeavyWeaponsTraining",
        "NightOps",
        "Teacher",
        "Throwing",
    }
)


def stable_roll(name: str, mod: int = 5) -> int:
    return sum(ord(c) for c in name) % mod


def ensure_bandage(inv: str, count: int = 1) -> str:
    if "Bandage" in inv:
        return inv
    return f"{inv} · Bandage×{count}"


def add(**kw):
    kw.setdefault("female", False)
    kw["lvl"] = 1
    traits = kw.get("traits") or []
    kw["traits"] = [t for t in traits if t in SPECIALIZATION_TRAITS]
    ROSTER.append(kw)


def _roster_slot(m: dict) -> int:
    try:
        return ROSTER.index(m) + 1
    except ValueError:
        return 1


# Vanilla ships 6 IMP UnitData (3♂+3♀). Only 2 VoiceResponse banks exist
# (IMP_male_01 / IMP_female_01); 02/03 UnitData also point at those banks.
IMP_MALE_POOL = ("IMP_male_01", "IMP_male_02", "IMP_male_03")
IMP_FEMALE_POOL = ("IMP_female_01", "IMP_female_02", "IMP_female_03")


def resolve_imp_voice(unit_id: str) -> str:
    """Map IMP UnitData id → existing VoiceResponse preset id."""
    if unit_id.startswith("IMP_female"):
        return "IMP_female_01"
    if unit_id.startswith("IMP_male"):
        return "IMP_male_01"
    return unit_id


def voice_for(m: dict) -> str:
    """Jazz remesh banks + all 6 IMP UnitData ids (resolve to working VR).

    ~3/4 of roster uses IMP pool (cycling male_01..03 / female_01..03);
    remaining keep Jazz remesh for local flavour.
    """
    slot = _roster_slot(m)
    if m.get("female"):
        if slot % 4 == 0:
            return "Jazz_AME_Female"
        return resolve_imp_voice(IMP_FEMALE_POOL[(slot - 1) % 3])
    if slot % 4 == 0:
        if m["cat"] in ("Hardened", "Specialists"):
            return "Jazz_AME_Male_Hard"
        return "Jazz_AME_Male_Low"
    return resolve_imp_voice(IMP_MALE_POOL[(slot - 1) % 3])


def voice_pool_label(m: dict) -> str:
    """Design-roster label: which of the 6 IMP UnitData (or Jazz bank) was picked."""
    slot = _roster_slot(m)
    if m.get("female"):
        if slot % 4 == 0:
            return "Jazz_AME_Female"
        return IMP_FEMALE_POOL[(slot - 1) % 3]
    if slot % 4 == 0:
        if m["cat"] in ("Hardened", "Specialists"):
            return "Jazz_AME_Male_Hard"
        return "Jazz_AME_Male_Low"
    return IMP_MALE_POOL[(slot - 1) % 3]


def voice_fallback(m: dict) -> str:
    """Pain/AiDeath only (Banter.lua) — never Ice/Fox (vanilla merc identity).

    IMP assignees fall back to the shared hireable bank (male_01 / female_01).
    Jazz remesh banks point at the enemy UnitData/VR they remeshed from.
    Calm slots (Selection/Move) stay silent when omitted on remesh banks.
    """
    voice = voice_for(m)
    if voice in ("IMP_male_01", "IMP_female_01"):
        return voice
    if m.get("female"):
        return "AnneLeMitrailleur"
    if m["cat"] in ("Hardened", "Specialists"):
        return "ArmySoldier"
    return "LegionRaider"


def appearance_for(m: dict, slot: int | None = None) -> str:
    """Cloned AME AppearancePreset id (JAZZ_AME_NN). Donor lives in ame-appearance-map.json."""
    if slot is None:
        try:
            slot = ROSTER.index(m) + 1
        except ValueError:
            slot = 1
    return f"JAZZ_AME_{slot:02d}"


def appearance_donor_for(m: dict, slot: int | None = None) -> str:
    """Vanilla donor id from ame-appearance-map.json (after _gen_ame_appearances.py)."""
    if slot is None:
        try:
            slot = ROSTER.index(m) + 1
        except ValueError:
            slot = 1
    map_path = Path(__file__).resolve().parents[2] / "docs" / "design" / "ame-appearance-map.json"
    if map_path.is_file():
        import json

        rows = json.loads(map_path.read_text(encoding="utf-8"))
        for row in rows:
            if int(row.get("slot", -1)) == slot:
                return str(row.get("donor", "?"))
    return "?"


# Legacy role→donor heuristic kept only as documentation of old shared pool.
def appearance_donor_heuristic(m: dict) -> str:
    """Donor AppearancePreset id to clone → AME blue (do not edit source)."""
    name = m["name"]
    role = m.get("role", "")
    cat = m.get("cat", "")
    bg = m.get("bg", "")
    if m.get("female"):
        if role in ("Instructor", "Medic", "Mechanic") or "Captain" in name or "Dr." in name:
            return "GrandChien_CommanderFemale"
        return "RebelFemaleSniper"
    if role == "Machinegunner":
        return ("Legion_Heavy", "Heavy_Rebels", "Legion_Heavy02")[stable_roll(name, 3)]
    if role == "Grenadier" or role == "Sapper":
        return ("Legion_Demolishion", "Demolitions_Rebels", "Militia_Demolition")[stable_roll(name, 3)]
    if role == "Sniper":
        return ("Marksman_Rebels", "Legion_Marksman", "Marksman_Rebels_02")[stable_roll(name, 3)]
    if role == "Medic":
        return ("Soldier_Rebels_02", "Militia_Marksman", "Legion_Soldier03")[stable_roll(name, 3)]
    if role == "Instructor":
        return ("Commander_Rebels", "Legion_Soldier06", "Legion_Soldier")[stable_roll(name, 3)]
    if role == "Mechanic":
        return ("Militia_Stormer", "Legion_Soldier04", "Soldier_Rebels_03")[stable_roll(name, 3)]
    if role == "Autorifleman":
        return ("Legion_Stormer", "Soldier_Rebels", "Legionraider")[stable_roll(name, 3)]
    if cat == "Irregulars":
        if bg in ("militia", "recruit", "police"):
            return ("Militia_Stormer", "Militia_Recon", "Militia_Marksman", "Militia_Heavy")[stable_roll(name, 4)]
        return ("Soldier_Rebels_04", "Recon_Rebels", "Marksman_Rebels_03", "LegionGoon")[stable_roll(name, 4)]
    if cat == "Hardened":
        return ("Legionraider", "Legion_Soldier", "Soldier_Rebels", "Legion_Stormer02")[stable_roll(name, 4)]
    return ("Legion_Soldier02", "Soldier_Rebels_02", "Militia_Stormer", "Legion_Recon")[stable_roll(name, 4)]


FEMALE_NAMES = {
    "Aisha Hassan",
    "Wanjiku Mwangi",
    "Awa Sow",
    "Amina Yusuf",
    "Dr. Fatoumata Sy",
    "Grace Wanjiru",
    "Captain Amara Koné",
    "Sgt. Nadia Okonkwo",
    "Lindiwe Mokoena",
    "Marie-Claire Mbala",
}

# ---------- Irregulars ×20 ----------
# Kit ≤1-2. Stats: Agi/Dex ≈60, Marks median ≈45 (novice −15). Will low. HP/Str wide.
IRR = [
    ("Kwame Mensah", None, "Ghana", "militia",
     "Кваме Менса вырос в Аккре и годы ходил в дружинном патруле, пока кому-то не надоело платить. Он крепкий, спокойный и внимательный — слушает больше, чем говорит, — а стрелять его учили урывками, между сменами. Теперь ищет нормальную работу: не очередной пост у склада, а дело, за которое не стыдно взять деньги.",
     "Knife"),
    ("Jean-Baptiste Okoro", None, "GrandChien", "hunter",
     "Жан-Батист Окоро — охотник из Гранд-Шьен. Когда зверь ушёл дальше, чем позволяла лицензия, он остался с опустевшей сумкой и привычкой считать каждый выстрел. Крадётся тихо, смотрит зорко, а про шумные автоматы говорит с недоверием. Хочет снова есть регулярно — без вопросов, откуда добыча.",
     "DoubleBarrelShotgun · 12g×6 · Knife"),
    ("Ibrahim Touré", None, "Mali", "police",
     "Ибрахим Туре служил постовым в Мали: разнимал драки, выписывал протоколы и умел успокоить толпу голосом, а не дубинкой. Когда участок сократили, он ушёл с привычкой перевязывать чужие ссадины и со служебным револьвером на память. Стреляет посредственно и сам это знает — зато не паникует, когда вокруг кричат.",
     "SWModel10 · .38×12 · Knife"),
    ("Sani Abubakar", None, "Nigeria", "recruit",
     "Сани Абубакар — новобранец без полка. Руки сильные: таскал мешки, ломал двери, помогал на стройке казармы. Нервы тоньше тела — от чужого крика сжимается раньше, чем успевает подумать. Честно говорит, что учиться придётся на ходу, и всё равно просится в дело.",
     "Knife"),
    ("Pierre Ndongo", None, "Congo", "militia",
     "Пьер Ндонго молчал на блокпостах Конго так долго, что коллеги перестали ждать от него шуток. Голова варит быстрее рук: запоминает лица, маршруты, кто кому должен. Оружие сдал при увольнении, карманы пусты, взгляд цепкий. Лучше слушает, чем стреляет — пока.",
     "— (empty hands)"),
    ("Moussa Diop", None, "Senegal", "hunter",
     "Мусса Диоп из Сенегала ходил следами лучше, чем по асфальту. Дед оставил ему старый винчестер — и Мусса бережёт его так, будто это последний родственник. Не любит шумные компании, патроны считает заранее. Говорит, что лес его ещё не отпустил — просто теперь добыча иногда ходит на двух ногах.",
     "Winchester1894 · .44×14 · Knife"),
    ("Abel Getachew", None, "Ethiopia", "recruit",
     "Абель Гетачью сбежал с учений в Эфиопии раньше, чем успел привыкнуть к строевой. Учится быстро: один раз покажи — и уже повторяет, пусть и криво. Попадает редко — руки ещё не поймали ритм. Упрямство у него сильнее опыта: хочет доказать, что из него выйдет солдат, а не вечный дезертир.",
     "— (empty hands)"),
    ("Thabo Molefe", None, "SouthAfrica", "militia",
     "Табо Молефе патрулировал фермы в Южной Африке: пугал воров, таскал мешки и спал в сарае. Корпус крепкий, шаг тяжёлый; дальше простого ружья ему ничего не выдавали — «хватит и так». У ворот стоит спокойно и от первого хлопка не бежит.",
     "DoubleBarrelShotgun · 12g×8 · Knife"),
    ("Daniel Kiprop", None, "Kenya", "hunter",
     "Даниэль Кипроп — егерь из Кении: глаза замечают движение раньше звука. Тело худое, выносливость охотничья, а не казарменная. О хорошей винтовке мечтал — дали то, что было. Ему важнее увидеть первым, чем носить красивую форму.",
     "DoubleBarrelShotgun · 12g×6 · Knife"),
    ("Emmanuel Kabongo", None, "GrandChien", "rebel",
     "Эммануэль Кабонго водил связных по тропам Гранд-Шьен и знал, где не стоит шуметь после заката. Люди его слушают чуть-чуть — не как офицера, а как того, кто уже проводил таких же потерянных. Стрелять почти не умеет, зато тропы помнит лучше карт.",
     "— (empty hands)"),
    ("Aisha Hassan", None, "Kenya", "recruit",
     "Аиша Хассан грузила ящики в кенийском порту, пока не поняла: спина ещё терпит, а нервы — уже нет. Хрупкая и вспыльчивая: любой резкий звук заставляет вздрагивать. Хочет уехать от порта подальше — даже если первая работа окажется самой грязной.",
     "Knife"),
    ("Amadou Keita", None, "Mali", "militia",
     "Амаду Кейта — деревенский дружинник из Мали. Сильный, привыкший работать руками, боится взрывчатки до дрожи: однажды видел, как мина разорвала телегу, и с тех пор обходит подозрительную землю по широкой дуге. Простую работу без «сюрпризов» делает лучше многих храбрецов.",
     "Machete"),
    ("Chidi Okonkwo", None, "Nigeria", "police",
     "Чиди Оконкво провалил медкомиссию армии Нигерии — сердце «не то», бумаги «не те». Зато пальцы ловкие: вскрывал ящики улик, чинил замки, однажды утащил из архива старый служебный револьвер. Чуть понимает в механизмах, больше — в том, как не попасться.",
     "Colt38Special · .38×12 · Knife"),
    ("Lucien Mbarga", None, "GrandChien", "hunter",
     "Люсьен Мбарга браконьерствовал в Гранд-Шьен, пока рейнджеры не отняли ружьё и не пообещали тюрьму при следующей встрече. Осталась привычка ходить тихо. Не герой и не кается вслух — просто ищет оплату там, где никто не спрашивает про лицензии.",
     "Knife"),
    ("Kofi Asante", None, "Ghana", "recruit",
     "Кофи Асанте сторожил школу в Гане и читал всё, что забывали на партах. Соображает отлично — схватывает быстрее многих «настоящих» бойцов, — но руками почти не владеет. Спокойно учится на чужих ошибках, лишь бы платили и давали шанс.",
     "— (empty hands)"),
    ("João Domingos", None, "Angola", "militia",
     "Жуан Домингос из Анголы один раз видел мины — и этого хватило, чтобы навсегда обходить рыхлую землю стороной. Медленный, упрямый и честно боится взрывов. Врать про храбрость не станет — и за это его иногда ценят больше, чем за смелость.",
     "Knife"),
    ("Wanjiku Mwangi", None, "Kenya", "hunter",
     "Ванджику Мванги помогала егерю в Кении: чистила следы, носила воду, дежурила на опушке. Зоркая и лёгкая на ногу, без громких обещаний. Привыкла, что работа грязная, а деньги маленькие — и всё равно делает её тихо и до конца.",
     "DoubleBarrelShotgun · 12g×4 · Knife"),
    ("Serge Kouassi", None, "GrandChien", "recruit",
     "Серж Куасси — сын механика из Гранд-Шьен, и отцу за него стыдно: отвёртку Серж не берёт. Голова светлая, рук нет — зато вопросы задаёт правильные. Хочет доказать, что ум тоже бывает оружием, даже если карманы пока пусты.",
     "— (empty hands)"),
    ("Bongani Dlamini", None, "SouthAfrica", "militia",
     "Бонгани Дламини работал на шахтёрской дружине в Южной Африке: таскал мешки, не бегал кроссы и спал кусками между сменами. Тяжёлый, молчаливый, привыкший к пыли. У двери стоит так, что объяснять дважды не приходится.",
     "ColtM1917 · .45×12 · Knife"),
    ("Idrissa Bah", None, "Senegal", "police",
     "Идрисса Бах регулировал движение в Сенегале лучше, чем стрелял: жестами командовал так, что даже пьяные водители иногда слушались. Не герой перестрелок — зато умеет остановить хаос на секунду дольше, чем другие.",
     "SWModel10 · .38×6 · Knife"),
]

# A/D ≈60, Marks median ≈45 (−15 vs prior); Will low; Wis high (рост); HP/Str wide.
# Weak shooters (empty hands / «не умеет») → Marks ≈30; hunters keep mid band.
IRR_STATS = [
    # H A D S Wis Will Lead Marks Mech Exp Med
    (86, 60, 60, 64, 70, 28, 5, 45, 0, 0, 5),
    (84, 62, 60, 56, 66, 26, 0, 45, 0, 0, 0),
    (88, 58, 58, 62, 72, 32, 10, 43, 0, 0, 10),
    (92, 56, 54, 78, 58, 22, 0, 43, 0, 0, 0),  # strongman — A/D lower, Str peak
    (85, 60, 60, 54, 76, 30, 8, 30, 0, 0, 5),  # Pierre — empty hands, listens > shoots
    (80, 68, 64, 52, 68, 28, 0, 49, 0, 0, 0),  # unique Agi≤70
    (87, 58, 56, 48, 78, 34, 5, 30, 0, 0, 8),  # Abel — empty hands, hits rarely
    (90, 60, 58, 70, 56, 26, 12, 45, 0, 0, 0),
    (76, 64, 62, 46, 72, 24, 0, 47, 0, 0, 0),  # frail HP
    (86, 60, 60, 60, 64, 30, 8, 32, 0, 0, 5),  # Emmanuel — empty hands, barely shoots
    (78, 58, 56, 42, 74, 20, 0, 30, 0, 0, 0),  # Aisha — recruit, frail
    (88, 60, 58, 68, 54, 28, 5, 45, 0, 0, 0),
    (84, 60, 66, 50, 66, 26, 0, 45, 12, 0, 5),
    (82, 64, 60, 56, 62, 27, 0, 45, 0, 0, 0),
    (83, 58, 54, 46, 80, 33, 5, 30, 0, 0, 10),  # Kofi — empty hands, no hands skill
    (87, 56, 54, 66, 54, 22, 0, 33, 0, 0, 0),  # João — militia, scared not sharp
    (82, 66, 64, 52, 70, 26, 0, 47, 0, 0, 0),
    (86, 60, 58, 58, 72, 29, 5, 30, 0, 0, 0),  # Serge — empty hands, mechanic's son
    (94, 54, 52, 80, 50, 30, 10, 43, 0, 0, 0),  # peak HP/Str
    (85, 60, 60, 54, 64, 28, 8, 45, 0, 0, 8),
]


for i, ((name, nick, nat, bg, bio, inv), st) in enumerate(zip(IRR, IRR_STATS)):
    keys = ["Health", "Agility", "Dexterity", "Strength", "Wisdom", "Will", "Leadership", "Marksmanship", "Mechanical", "Explosives", "Medical"]
    add(
        name=name,
        nick=nick,
        nat=nat,
        cat="Irregulars",
        role="Rifle",
        spec="AllRounder",
        lvl=1,
        salary=80 + (i % 8) * 8,
        traits=[],
        bio=bio,
        inv=inv,
        stats=dict(zip(keys, st)),
        bg=bg,
        female=name in FEMALE_NAMES,
    )

# ---------- Fighters ×18 ----------
# Kit ≤1-3. Stats: Agi/Dex ≈65, Marks median ≈55 (−10). Will low. Perk tax Auto/HW.
FIGHTERS = [
    ("Omar Diallo", None, "Senegal", "Rifle", "Marksmen", [], 220,
     "Winchester1894 · .44×40 · Knife",
     "Омар Диалло дезертировал из сенегальской части, когда понял, что легион зовёт громче командования. Отказался — и ушёл с привычкой целиться один раз, но точно. Не орёт, не хвастается: делает работу и считает патроны."),
    ("Bastien Lafontaine", None, "GrandChien", "Autorifleman", "Autoriflemen", ["AutoWeapons"], 240,
     "STG44 · 7.92Kurz×60 · Knife",
     "Бастьен Лафонтен служил милицейским автоматчиком в Гранд-Шьен и до сих пор пахнет машинным маслом и дешёвым табаком. Очереди для него важнее красоты ствола: улица становится тесной — и он уже на линии. Платят лучше участка — и этого ему достаточно."),
    ("Chukwuemeka Obi", "Emeka", "Nigeria", "Machinegunner", "HeavyWeapons", ["HeavyWeaponsTraining", "AutoWeapons"], 260,
     "MAC2429 · 7.5French×60 · Knife",
     "Чуквуэмека Оби сидел на пулемётной точке нигерийского блокпоста, пока блокпост не стёрли с карты. Крепкий, тяжёлый, бьёт по земле увереннее, чем по мишеням — и сам над этим иногда шутит. Закрыть сектор огнём для него привычнее, чем выигрывать конкурс стрелков."),
    ("Michel Kabeya", None, "Congo", "Grenadier", "ExplosiveExpert", ["Throwing"], 250,
     "Colt1911 · .45×24 · FragGrenade×2 · Knife",
     "Мишель Кабейа из Конго всегда любил банки больше стволов. Настоящая работа для него начинается, когда свистит чека. Шумный в баре и тихий перед броском — и не притворяется героем."),
    ("Juma Otieno", None, "Kenya", "Rifle", "Marksmen", [], 200,
     "Winchester1894 · .44×28 · Knife",
     "Джума Отиено служил на кенийской границе: лёгкий на ногу, привыкший к пыли и долгим сменам. Дальнюю винтовку ему не доверили — приказали не геройствовать. Не обижается: главное — увидеть первым. Скорость ног для него важнее красивой стойки."),
    ("Andile Nkosi", None, "SouthAfrica", "Autorifleman", "Autoriflemen", ["AutoWeapons"], 230,
     "STG44 · 7.92Kurz×60 · Knife",
     "Андиле Нкоси охранял конвои в Южной Африке и научился стрелять очередями так, чтобы охраняемый груз не превращался в решето раньше времени. Спокоен, немногословен и не любит, когда новички трогают его оружие «просто посмотреть»."),
    ("Sekou Camara", None, "Mali", "Rifle", "AllRounder", [], 190,
     "M3GreaseGun · .45×60 · Knife",
     "Секу Камара патрулировал пустыню в Мали и не считал короткий ствол унижением. Подвижный, с нервами крепче, чем у многих «настоящих» стрелков, умеет смещаться и не торчать на открытом месте. Доходит туда, куда тяжёлые ребята только собираются."),
    ("Pascal Ngoma", None, "GrandChien", "Machinegunner", "HeavyWeapons", ["HeavyWeaponsTraining"], 270,
     "BAR · .30-06×60 · Knife",
     "Паскаль Нгома держал огневую точку в Гранд-Шьен с характером человека, который не любит бегать. Тяжёлый, упрямый: закрывает сектор и ждёт, пока сектор перестанет шевелиться. Под огнём не дёргается первым — и этим уже выигрывает время для остальных."),
    ("Kwesi Boateng", None, "Ghana", "Grenadier", "ExplosiveExpert", ["Throwing", "HeavyWeaponsTraining"], 255,
     "PPS43 · 7.62x25×70 · FragGrenade×2 · Knife",
     "Квеси Боатенг из Ганы любит короткую работу и тяжёлую ладонь на банке. Взрывчатки у него немного, зато бросок уверенный — как у человека, который тренировался на пустых бутылках за складом. Улыбается редко и работает быстро: пришёл, бросил, ушёл, пока эхо ещё гуляет."),
    ("Tesfaye Alemu", None, "Ethiopia", "Rifle", "Marksmen", [], 210,
     "M1897 · 12g×20 · Knife",
     "Тесфайе Алем — горный стрелок из Эфиопии. Целится аккуратно, дышит ровно и не делает вид, что ему «просто забыли» выдать лучшее оружие. Хороший глаз, скромные ожидания, готов учиться на том, что дадут."),
    ("Rafael dos Santos", None, "Angola", "Autorifleman", "Autoriflemen", ["AutoWeapons"], 235,
     "STG44 · 7.92Kurz×60 · Knife",
     "Рафаэль дос Сантос из Анголы учится медленнее иных, зато не ломается от первой тяжёлой недели. Очереди для него — ремесло, выученное кровью и пылью. Не обещает чудес. Обещает явиться трезвым и не бросить позицию без приказа."),
    ("Awa Sow", None, "Senegal", "Rifle", "AllRounder", [], 180,
     "PPSH · 7.62x25×70 · Knife",
     "Ава Соу из Сенегала попала в тесные коридоры не по любви, а по расписанию смен. Юркая и нервная, без армейской школы длинных очередей — зато живее многих «правильных» автоматчиков. Держится особняком и ненавидит, когда мужчины объясняют ей, как «правильно» стрелять."),
    ("Claude Mvemba", None, "GrandChien", "Rifle", "Marksmen", [], 200,
     "Auto5 · 12g×20 · Knife",
     "Клод Мвемба охранял плантации в Гранд-Шьен — привык к дроби, не к оптике. Говорит мало, курит много, считает, что хороший выстрел тот, после которого никто не спорит. Работает ближе, чем любят дальние стрелки, и дальше, чем удобно трусам."),
    ("Emeka Nwosu", None, "Nigeria", "Machinegunner", "HeavyWeapons", ["HeavyWeaponsTraining", "AutoWeapons"], 280,
     "MAC2429 · 7.5French×60 · Knife",
     "Эмека Нвосу — силач с нигерийским характером: здоровье и упрямство у него заметнее меткости, и он не стесняется этого. Про него шутят, что его проще нанять, чем сдвинуть. Он не возражает — лишь бы платили вовремя."),
    ("Samuel Cheruiyot", None, "Kenya", "Rifle", "Marksmen", [], 215,
     "Winchester1894 · .44×28 · Knife",
     "Сэмюэл Черуйот охотился в Кении раньше, чем научился читать уставы. Охотничья винтовка ему роднее любой казённой; с длинным болтом не заигрывает и без зависти. Быстрый, зоркий, с привычкой целиться перед выстрелом. Любит воздух чаще, чем порох казармы."),
    ("Mamadou Traoré", None, "Mali", "Autorifleman", "Autoriflemen", ["AutoWeapons"], 225,
     "STG44 · 7.92Kurz×60 · Knife · Wirecutter",
     "Мамаду Траоре из Мали чинит стволы соседей чаще, чем хвастается своими. Отвёртка часто чужая, зато руки помнят, куда крутить. После боя ещё и собирает то, что осталось стрелять."),
    ("Felix Tshisekedi", None, "Congo", "Rifle", "AllRounder", [], 195,
     "Auto5 · 12g×16 · Knife · Bandage×2",
     "Феликс Чисекеди — человек конголезского блокпоста: перевяжет рану, закроет сектор, не будет спрашивать, почему смена опять без воды. Не гений ни в чём — зато не провал ни в чём. Командиры любят таких именно за отсутствие сюрпризов."),
    ("Noah van Wyk", None, "SouthAfrica", "Rifle", "Marksmen", [], 205,
     "Winchester1894 · .44×28 · Knife",
     "Ноа ван Вик — фермерский стрелок из Южной Африки с голосом, к которому прислушиваются даже те, кто старше. Люди его слушают не из страха — из привычки, что он говорит по делу. Меньше позы, больше работы."),
]

# A/D ≈65, Marks median ≈55 (−10); Will low; HP/Str wide. Perk tax on Auto/HW.
FIGHTER_STATS = [
    # H A D S Wis Will Lead Marks Mech Exp Med
    (78, 66, 66, 60, 58, 30, 8, 56, 0, 5, 8),  # Omar TakeAim
    (76, 64, 64, 58, 52, 28, 5, 54, 0, 0, 5),  # Bastien Auto
    (88, 58, 56, 78, 46, 32, 0, 48, 0, 0, 0),  # Chukwu HW+Auto — HP/Str high, Marks tax
    (80, 66, 66, 62, 54, 26, 5, 56, 0, 12, 5),  # Michel Throwing
    (72, 70, 68, 50, 60, 30, 8, 60, 0, 0, 8),  # Juma no perk — top Fight
    (78, 64, 64, 60, 50, 28, 8, 54, 0, 0, 5),  # Andile Auto
    (74, 70, 66, 52, 56, 35, 10, 56, 0, 0, 5),  # Sekou — high Agi, no MinFreeMove
    (86, 56, 58, 74, 46, 30, 5, 50, 0, 5, 0),  # Pascal HW — tanky
    (78, 62, 64, 66, 50, 24, 0, 50, 5, 12, 0),  # Kwesi Throw+HW
    (70, 68, 66, 48, 62, 28, 5, 58, 0, 0, 5),  # Tesfaye TakeAim — frail HP
    (80, 64, 64, 62, 48, 30, 5, 54, 0, 0, 5),  # Rafael Auto
    (72, 68, 68, 50, 54, 22, 0, 58, 0, 0, 5),  # Awa no perk
    (78, 66, 66, 58, 56, 28, 10, 56, 0, 0, 8),  # Claude
    (90, 56, 54, 80, 44, 34, 5, 48, 0, 0, 0),  # Emeka HW+Auto — peak HP/Str
    (76, 68, 66, 54, 58, 26, 8, 58, 0, 0, 5),  # Samuel TakeAim
    (78, 64, 62, 58, 52, 28, 5, 54, 15, 0, 5),  # Mamadou Auto; tiny Mech
    (80, 66, 64, 56, 56, 30, 8, 56, 0, 0, 12),  # Felix
    (82, 64, 64, 64, 54, 32, 50, 56, 0, 0, 5),  # Noah Lead≈50
]


for (name, nick, nat, role, spec, traits, salary, inv, bio), st in zip(FIGHTERS, FIGHTER_STATS):
    keys = ["Health", "Agility", "Dexterity", "Strength", "Wisdom", "Will", "Leadership", "Marksmanship", "Mechanical", "Explosives", "Medical"]
    # ~40% Fighters carry a bandage (design-fixed; not runtime invent-roll).
    if "Bandage" in inv or stable_roll(name) < 2:
        inv = ensure_bandage(inv, 1)
    add(
        name=name,
        nick=nick,
        nat=nat,
        cat="Fighters",
        role=role,
        spec=spec,
        lvl=1,
        salary=salary,
        traits=traits,
        bio=bio,
        inv=inv,
        stats=dict(zip(keys, st)),
        bg="ex-army" if "Autorifle" in role or role == "Machinegunner" else "militia",
        female=name in FEMALE_NAMES,
    )

# ---------- Hardened ×10 (nicks on ~3) ----------
# Kit ≤2-1. Type56 = AR ceiling, Hardened-only. A/D ≈70, Marks median ≈60 (−10). HP/Str wide.
HARD = [
    ("Joseph Mukendi", "Hyena", "GrandChien", "Autorifleman", "Autoriflemen", ["AutoWeapons", "CQCTraining"], 480,
     "Thompson · .45×60 · Knife · FragGrenade×1",
     "Жозефа Мукенди в Гранд-Шьен зовут «Гиена»: годами делал засады так, что жертвы узнавали кличку раньше лица. В тесноте бьёт грязно и быстро — красивой стрельбы меньше, зато чаще остаётся живым. Нервы держат. Знает себе цену и не любит, когда её занижают."),
    ("Abraham Tekle", None, "Ethiopia", "Rifle", "Marksmen", [], 420,
     "Mini14 · 5.56×40 · Knife",
     "Абрахам Текле — горный ветеран из Эфиопии. Дышит ровно, ждёт, бьёт; уставы помнит хуже, чем привычку к прицелу. Корпус крепче, чем кажется по лицу. Уже видел поражение — и не сломался."),
    ("Sipho Khumalo", "Anvil", "SouthAfrica", "Machinegunner", "HeavyWeapons", ["HeavyWeaponsTraining", "AutoWeapons"], 520,
     "BAR · .30-06×80 · Knife",
     "Сифо Кхумало, «Наковальня», тащит тяжесть так, будто мир обязан подождать. Тяжёлый ствол и очереди делают своё дело — и меткость от этого страдает, он знает. Не спорит: его работа — давить сектор, а не выигрывать тир."),
    ("Boubacar Kane", None, "Senegal", "Rifle", "AllRounder", [], 400,
     "STG44 · 7.92Kurz×40 · Knife",
     "Бубакар Кане — офицер запаса из Сенегала со спокойным прицелом. С людьми получается чуть лучше, чем у многих ветеранов: объяснит задачу так, что даже усталые кивают. Не орёт. Не геройствует. За сутки на старшего позицию обычно оставляет целой."),
    ("Didier Mbemba", "Smoke", "Congo", "Grenadier", "ExplosiveExpert", ["Throwing", "HeavyWeaponsTraining"], 500,
     "Ithaca · 12g×16 · FragGrenade×2 · Knife",
     "Дидье Мбемба, «Дым», из Конго приходит с банками и уходит в дыму, который сам же и ставит. Не спринтер — зато сектор задымления знает наизусть. Когда тишина уже не вариант, он как раз на месте."),
    ("Amina Yusuf", None, "Nigeria", "Autorifleman", "Autoriflemen", ["AutoWeapons"], 450,
     "Type56 · 7.62×90 · Knife · Bandage×2",
     "Амина Юсуф бережёт хороший автомат и бинты в кармане — ветераны дольше живут, когда не стесняются собственной крови. Очереди короткие, взгляд холодный. Про неё говорят мало и уважительно — так безопаснее."),
    ("Léopold Sassou", None, "GrandChien", "Rifle", "Marksmen", [], 430,
     "STG44 · 7.92Kurz×40 · Knife · Wirecutter",
     "Леопольд Сассу — сержант Гранд-Шьен с тяжёлым корпусом, ровным прицелом и чуточкой механики, достаточной, чтобы ствол соседа не клинил в самый плохой момент. Не улыбается для камеры. Улыбается, когда магазин встаёт с первого раза."),
    ("Kofi Mensah", None, "Ghana", "Machinegunner", "HeavyWeapons", ["HeavyWeaponsTraining"], 490,
     "MAC2429 · 7.5French×80 · Knife",
     "Кофи Менса из Ганы — силач: здоровье и мощь замечают раньше, чем меткость. Не догоняет — занимает место и делает его непригодным для врага. Там, где нужна тяжесть, а не грация, он уместен."),
    ("Hassan Ibrahim", "Scorpion", "Mali", "Grenadier", "ExplosiveExpert", ["Throwing"], 510,
     "HiPower · 9mm×30 · FragGrenade×2 · Molotov×1 · Knife",
     "Хассана Ибрахима в Мали зовут «Скорпион»: быстрее многих ветеранов, с ухмылкой человека, который любит, когда взрыв случается вовремя. Бросок уверенный, характер ядовитый. Кличка известнее имени — и он над этим не работает."),
    ("Patrick Omondi", None, "Kenya", "Rifle", "Marksmen", ["NightOps"], 440,
     "Mini14 · 5.56×40 · Knife",
     "Патрик Омонди — ночной стрелок из Кении со спокойным голосом, к которому прислушиваются даже уставшие. Лучше видит в темноте и лучше ждёт. После заката говорит шёпотом так, что всё равно слушаются."),
]

# A/D ≈70, Marks median ≈60 (−10); Will mid; HP/Str wide. Perk tax HW+Auto / dual.
HARD_STATS = [
    # H A D S Wis Will Lead Marks Mech Exp Med
    (84, 70, 68, 72, 44, 55, 12, 54, 0, 10, 8),  # Joseph Auto+CQC — Marks tax
    (80, 70, 70, 70, 50, 52, 10, 60, 5, 8, 5),  # Abraham TakeAim+Steady
    (94, 62, 60, 90, 36, 58, 8, 50, 0, 8, 5),  # Sipho HW+Auto — peak HP/Str, Marks tax
    (82, 70, 70, 68, 48, 52, 18, 60, 0, 12, 8),  # Boubacar TakeAim
    (78, 68, 70, 70, 44, 48, 5, 58, 5, 14, 5),  # Didier Throw+HW
    (80, 70, 68, 64, 52, 54, 16, 58, 0, 8, 12),  # Amina Auto
    (88, 68, 66, 76, 40, 56, 14, 60, 28, 10, 8),  # Léopold TakeAim + Mech — tanky
    (92, 60, 58, 92, 34, 60, 5, 56, 0, 8, 5),  # Kofi HW — peak Str, Agi lower
    (80, 70, 70, 66, 46, 50, 8, 60, 5, 14, 5),  # Hassan Throwing
    (82, 70, 70, 64, 48, 52, 48, 60, 0, 10, 8),  # Patrick TakeAim+NightOps — Lead≈50
]


for (name, nick, nat, role, spec, traits, salary, inv, bio), st in zip(HARD, HARD_STATS):
    keys = ["Health", "Agility", "Dexterity", "Strength", "Wisdom", "Will", "Leadership", "Marksmanship", "Mechanical", "Explosives", "Medical"]
    inv = ensure_bandage(inv, 1)  # Hardened always pack a bandage
    add(
        name=name,
        nick=nick,
        nat=nat,
        cat="Hardened",
        role=role,
        spec=spec,
        lvl=1,
        salary=salary,
        traits=traits,
        bio=bio,
        inv=inv,
        stats=dict(zip(keys, st)),
        bg="ex-army",
        female=name in FEMALE_NAMES,
    )

# ---------- Specialists ×12 ----------
# Snipers: SKS/Gewehr. +Mechanic×2. Cap ≤ 2-1 but no Type56 (Hardened-only ceiling).
SPEC = [
    ("Dr. Fatoumata Sy", None, "Senegal", "Medic", "Doctor", [], 950,
     "HiPower · 9mm×24 · Medkit · Bandage×6 · Morphine×2 · Knife",
     "Доктор Фатумата Си — полевой хирург из Сенегала. Руки лечат, не стреляют; пистолет носит скорее для страха и редкой необходимости. В лазарете говорит тихо, режет уверенно и ненавидит, когда «герои» приходят без бинтов. Считает, что живые бойцы дороже мёртвых легенд."),
    ("Grace Wanjiru", None, "Kenya", "Medic", "Doctor", [], 880,
     "Knife · Medkit · Bandage×8 · Stim×2",
     "Грейс Ванджиру — лазаретная медсестра из Кении. Ствола нет и не будет: её сила — набор, бинты и умение не паниковать, когда крови слишком много. Тихая и незаменимая в тылу; экономить на таких обычно заканчивается плохо."),
    ("Dr. Emile Kabongo", None, "GrandChien", "Medic", "Doctor", [], 1000,
     "HiPower · 9mm×24 · Medkit · Bandage×6 · Knife",
     "Доктор Эмиль Кабонго — травматолог из Гранд-Шьен. Учит младших перевязывать так, чтобы раненый дожил до настоящей помощи. Голос спокойный, руки точные. Выглядит старше своих лет — так бывает с теми, кто слишком часто видел, чем кончается «ещё одна небольшая царапина»."),
    ("Captain Amara Koné", None, "Mali", "Instructor", "Leader", ["Teacher"], 1200,
     "STG44 · 7.92Kurz×30 · Knife · Bandage×2",
     "Капитан Амара Коне — инструктор из Мали с учительским характером. Учит жёстко, без театра: оставляет объяснения, которые потом спасают жизни. Считает, что один хороший учитель дешевле десяти свежих могил."),
    ("Sgt. Nadia Okonkwo", None, "Nigeria", "Instructor", "Leader", ["Teacher"], 1150,
     "STG44 · 7.92Kurz×40 · Knife · Bandage×2",
     "Сержант Надия Оконкво из Нигерии учит прицелу так, будто это одна профессия со стрельбой: научить попадать важнее, чем самой красиво попасть на глазах у начальства. В бой идёт редко, говорит часто — и обычно по делу. Её слушают даже те, кто не любит женщин с голосом громче их собственного."),
    ("Maj. Théodore Ngalula", None, "GrandChien", "Instructor", "Leader", ["Teacher"], 1300,
     "STG44 · 7.92Kurz×30 · Knife · Bandage×3",
     "Майор Теодор Нгалула помнит, как строить людей так, чтобы они не разваливались в первую же неделю. Мудрость и отвёртка у него рядом с привычкой объяснять до тех пор, пока не поймут. В Гранд-Шьен его ещё помнят по званию — и по тому, что скидок на работу он не любит."),
    ("Issa Camara", None, "Senegal", "Sniper", "Marksmen", [], 780,
     "Gewehr98 · 7.62×20 · Knife",
     "Исса Камара стреляет редко и метко. Тело хрупкое: один выстрел, не спринт. Ровное дыхание и терпение — его религия; беготня — чужая. Штурмовиком себя не считает и другим не врёт."),
    ("Lindiwe Mokoena", None, "SouthAfrica", "Sniper", "Marksmen", ["NightOps"], 820,
     "SKS · 7.62×30 · Knife",
     "Линдиве Мокоена работает ночью. Хрупкая, зоркая; темнота для неё союзник, а не чужой кошмар. Не обещает чудес и не набивает цену громкими словами. Любит, когда дело заканчивается одним тихим щелчком."),
    ("Bakary Diarra", None, "Mali", "Sapper", "ExplosiveExpert", ["Throwing"], 720,
     "Knife · ShapedCharge×2 · TNT×1 · PipeBomb×2 · Detonator · Wirecutter",
     "Бакари Диарра из Мали однажды пропил пистолет на детонаторы — и не жалеет. Взрывчатку знает лучше стрельбы, и сам об этом не стесняется. Его боятся ровно настолько, насколько уважают."),
    ("Marie-Claire Mbala", None, "Congo", "Sapper", "ExplosiveExpert", ["Throwing"], 760,
     "Makarov · 9x18×16 · ShapedCharge×2 · Knife · Wirecutter",
     "Мари-Клер Мбала ставит мины в Конго без лишней поэзии. Взрывчатка для неё важнее патронов, и она это повторяет всем новичкам. Бросок уверенный, характер сухой — сначала любопытство, потом осторожность."),
    ("Ousmane Fall", None, "Senegal", "Mechanic", "AllRounder", [], 680,
     "Wirecutter · Crowbar · Knife",
     "Усман Фалл из Сенегала чинит стволы лучше, чем держит их в бою. Желания геройствовать нет. В бой его не зовут, если есть хоть кто-то другой; после боя зовут первыми. Без него отряд разваливается быстрее, чем без лишнего героя."),
    ("Jean-Pierre Kalala", None, "GrandChien", "Mechanic", "AllRounder", [], 720,
     "Wirecutter · Lockpick · Knife · Bandage×1",
     "Жан-Пьер Калала — бывший гаражный мастер из Гранд-Шьен. Замок вскроет, очередь — вряд ли. Инструменты ему роднее любого автомата. Хорошие механики не любят рекламу — его обычно находят по рекомендации."),
]

# Soft peaks: Medical/Lead/Mech ≤70; Explosives <70; Marks ≤70 (Sniper). Instructors = Lead peak + Marks dump.
SPEC_STATS = [
    (70, 52, 54, 40, 72, 28, 30, 24, 8, 5, 70),  # Fatoumata Medic — Medical ceiling 70
    (68, 54, 56, 38, 70, 26, 28, 22, 5, 0, 66),  # Grace
    (74, 50, 52, 44, 74, 30, 38, 26, 12, 5, 68),  # Emile
    (68, 48, 50, 52, 85, 32, 68, 35, 50, 28, 35),  # Amara Instructor — Lead ceiling 70
    (66, 50, 52, 50, 82, 28, 65, 38, 42, 22, 30),  # Nadia
    (72, 46, 48, 58, 88, 34, 70, 32, 55, 30, 40),  # Théodore — Lead peak 70
    (54, 62, 58, 48, 58, 28, 8, 68, 20, 5, 5),  # Issa Sniper ≤70 Marks
    (52, 66, 60, 46, 55, 30, 12, 70, 15, 0, 8),  # Lindiwe Sniper =70
    (70, 48, 52, 55, 60, 26, 8, 24, 50, 68, 8),  # Bakary Sapper — Exp <70
    (72, 50, 54, 54, 62, 28, 6, 26, 52, 66, 10),  # Marie-Claire — Exp <70
    (76, 48, 52, 58, 62, 26, 0, 22, 70, 5, 5),  # Ousmane Mechanic — Mech ceiling 70
    (78, 50, 50, 60, 58, 28, 5, 24, 68, 0, 8),  # Jean-Pierre
]

for (name, nick, nat, role, spec, traits, salary, inv, bio), st in zip(SPEC, SPEC_STATS):
    keys = ["Health", "Agility", "Dexterity", "Strength", "Wisdom", "Will", "Leadership", "Marksmanship", "Mechanical", "Explosives", "Medical"]
    add(
        name=name,
        nick=nick,
        nat=nat,
        cat="Specialists",
        role=role,
        spec=spec,
        lvl=1,
        salary=salary,
        traits=traits,
        bio=bio,
        inv=inv,
        stats=dict(zip(keys, st)),
        bg="ex-army" if role in ("Instructor", "Sniper") else "specialist",
        female=name in FEMALE_NAMES,
    )

assert len(ROSTER) == 60, len(ROSTER)


def render() -> str:
    lines: list[str] = []
    lines.append("# AME Roster — 60 карточек (design)")
    lines.append("")
    lines.append("Источник контракта: [`JAZZ-UNITS-005`](../specs/active/JAZZ-UNITS-005.md), companion [`ame-mercenary-exchange.md`](ame-mercenary-exchange.md).")
    lines.append("")
    lines.append("Это **design-roster** для реализации: фиксированные имя/статы/био/один инвентарь. Runtime-ротация меняет только Available/`NotListed`/terminal — не перегенерирует карточку после hire.")
    lines.append("")
    lines.append("## Сводка пула")
    lines.append("")
    lines.append("| Категория (вкладка) | Кол-во | Примечание |")
    lines.append("| --- | ---: | --- |")
    lines.append("| Irregulars | 20 | A/D ≈60; Marks median ≈45 (weak ≈30); HP/Str wide; high Wisdom |")
    lines.append("| Fighters | 18 | A/D/Marks ≈65; kit ≤1-3; ≥30% autorifle/MG/GL с Hardened |")
    lines.append("| Hardened | 10 | A/D/Marks ≈70; Will mid; kit ≤2-1 |")
    lines.append("| Specialists | 12 | Medic×3, Instructor×3, Sniper×2, Sapper×2, Mechanic×2 |")
    lines.append("")
    lines.append("- Инвентарь: **1 фиксированный вариант** на слот (без `Randomization`).")
    lines.append("- **Appearance:** на слот свой клон `JAZZ_AME_NN` (donor Rebels/Legion/Militia; Hardened/Spec — ещё GrandChien). Красное → синее; кожа с пресета. Карта: [`ame-appearance-map.json`](ame-appearance-map.json).")
    lines.append("- **Кит:** Irr ≤ **1-2**; Fight ≤ **1-3**; Hard/Spec ≤ **2-1**. **`Type56` — потолок AR, только Hardened.** `SKS`/bolt — только Sniper.")
    lines.append("- **ПП:** винтаж T1 — `Thompson` / `M3GreaseGun` / `PPS43` / `PPSH` / `MP40` / `MAT49` / `Sterling`. **`UZI` и прочий T2 ПП в стартовых китах нет.**")
    lines.append("- **Бинты:** Fighters ~40%; Hardened всегда. **Sapper:** часть с `PipeBomb`.")
    lines.append("- Voice pool: Jazz remesh (~1/4) + all 6 IMP UnitData `IMP_male_01..03` / `IMP_female_01..03` (~3/4; VR resolves to `IMP_male_01` / `IMP_female_01`).")
    lines.append("- **Bio:** полная игровая проза карточки найма (RU); без мета-цифр статов/тиров.")
    lines.append("- Nick: в основном Hardened. Grand Chien: заметная доля.")
    lines.append("")

    by_cat: dict[str, list[tuple[int, dict]]] = {}
    for i, m in enumerate(ROSTER, 1):
        by_cat.setdefault(m["cat"], []).append((i, m))

    for cat in ("Irregulars", "Fighters", "Hardened", "Specialists"):
        lines.append(f"## {cat}")
        lines.append("")
        for i, m in by_cat[cat]:
            nick = f' «{m["nick"]}»' if m["nick"] else ""
            lines.append(f"### `JAZZ_AME_{i:02d}` — {m['name']}{nick}")
            lines.append("")
            lines.append(f"- **Nationality:** `{m['nat']}`")
            lines.append(f"- **Category / CombatRole:** {m['cat']} / {m['role']}")
            lines.append(f"- **Specialization:** `{m['spec']}`")
            lines.append(f"- **Level / Salary:** {m['lvl']} / ${m['salary']}")
            lines.append(f"- **Potential (Wisdom):** {pot(m['stats']['Wisdom'])}")
            traits = ", ".join(f"`{t}`" for t in m["traits"]) if m["traits"] else "—"
            lines.append(f"- **Traits (common):** {traits}")
            lines.append(f"- **Voice:** `{voice_pool_label(m)}` → VR `{voice_for(m)}`")
            app = appearance_for(m, i)
            donor = appearance_donor_for(m, i)
            sex = "female" if m.get("female") else "male"
            lines.append(f"- **Appearance:** `{app}` ← donor `{donor}` ({sex}; blue recolor, source не править)")
            lines.append(f"- **Inventory (fixed):** {m['inv']}")
            lines.append("")
            lines.append("| Stat | |")
            lines.append("| --- | ---: |")
            for k, v in m["stats"].items():
                lines.append(f"| {k} | {v} |")
            lines.append("")
            lines.append(f"**Биография:** {m['bio']}")
            lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    text = render()
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT} chars={len(text)} mercs={len(ROSTER)}")


if __name__ == "__main__":
    main()
