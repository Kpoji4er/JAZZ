# R.I.S. dossier / UI / AAR copy bank (RU+EN).
# Import: from _ris_dossier_copy import DOSSIERS, QUEST_DOSSIERS, STRING_FIXES
# Also: WELCOME_FIXES, UI_FIXES, AAR_FIXES

from __future__ import annotations

# ---------------------------------------------------------------------------
# Legion unit dossiers — keyed by UnitData id (JAZZ_RIS_DOSSIERS)
# ---------------------------------------------------------------------------

DOSSIERS: dict[str, dict[str, str]] = {
    "JAZZ_Legion_Recruit": {
        "title_en": "Recruit",
        "title_ru": "Рекрут",
        "body_en": (
            "The Major still sweeps villages for warm bodies: cheap boots, a rifle if lucky, "
            "and a week of shouted drill. Recruits freeze when the first magazine empties and "
            "bunch up like sheep in a doorway. Dangerous only in numbers — and as proof the "
            "Legion never runs out of names. Kill three and the desk will keep the file open."
        ),
        "body_ru": (
            "Майор по-прежнему выметает деревни за «тёплыми телами»: дешёвые ботинки, винтовка "
            "если повезёт, неделя орёного строя. Рекруты цепенеют, едва опустеет первый магазин, "
            "и сбиваются в дверных проёмах. Опасны только числом — и как напоминание, что у "
            "Легиона всегда есть ещё имена. Три трупа — и стол держит досье открытым."
        ),
    },
    # --- Assault T1 ---
    "JAZZ_Legion_AssaultT1_Crusher": {
        "title_en": "Crusher",
        "title_ru": "Громила",
        "body_en": (
            "Crusher is the Major's blunt instrument for rooms and alleys: shotgun breath, "
            "shoulder through the jamb, no patience for standoffs. Kit is scrap-yard early — "
            "loud nerves, thin discipline. In CQB they dump the tube and keep walking; leave "
            "them an open door and they own the next five metres. Danger spikes once the gap closes."
        ),
        "body_ru": (
            "Громила — тупой инструмент Майора для комнат и переулков: дыхание дробовика, плечо "
            "в косяк, никаких дуэлей на дистанции. Киты ещё со склада — громкие нервы, тонкая "
            "дисциплина. В ближнем бою опустошают ствол и идут дальше; оставьте открытую дверь — "
            "и следующие пять метров уже их. Опасность высокая, если сократят дистанцию."
        ),
    },
    "JAZZ_Legion_AssaultT1_Grenadier": {
        "title_en": "Grenadier",
        "title_ru": "Гренадёр",
        "body_en": (
            "Assault Grenadiers learn one trick early: toss steel before they see the whites of "
            "your eyes. Drill is short; they still fumble pins under fire, but a green throw into "
            "a hallway rewrites the breach. Watch corners and stairwells — they breach with bangs, "
            "not bravado. Soft kit, hard habit of lobbing first."
        ),
        "body_ru": (
            "Штурмовые гренадёры рано учат один приём: кинуть железо, пока ещё не видно глаз. "
            "Учёба короткая — под огнём чеку ещё роняют, но зелёный бросок в коридор уже ломает "
            "штурм. Смотрите углы и лестницы: они входят со взрывами, не с бравадой. Сырой кит, "
            "но привычка бросать первой уже есть."
        ),
    },
    "JAZZ_Legion_AssaultT1_Roughneck": {
        "title_en": "Roughneck",
        "title_ru": "Головорез",
        "body_en": (
            "Roughnecks are the Major's street dogs — SMG spray, boot in the door, no map beyond "
            "the next room. Green as wet paint: they bunch, shout, and dump magazines into furniture. "
            "Still lethal in a choke point if you give them the first step. Treat them as CQB noise "
            "with teeth, not soldiers."
        ),
        "body_ru": (
            "Головорезы — дворовые псы Майора: очередь из пистолета-пулемёта, ботинок в дверь, "
            "карты дальше следующей комнаты нет. Зелёные как сырая краска — жмутся, орёт, "
            "опорожняют магазины в мебель. В узком месте всё равно смертельны, если отдать им "
            "первый шаг. Это шум ближнего боя с зубами, не солдаты."
        ),
    },
    # --- Assault T2 ---
    "JAZZ_Legion_AssaultT2_Pillager": {
        "title_en": "Pillager",
        "title_ru": "Грабитель",
        "body_en": (
            "Pillagers have already looted a few towns — they breach for loot and leave scorched "
            "rooms behind. Blooded enough to push through smoke instead of freezing in it. Expect "
            "aggressive CQB: flash in, take the corner, strip the dead. They still panic in stacked "
            "doorways, but they panic forward."
        ),
        "body_ru": (
            "Грабители уже обчистили пару посёлков — ломают двери ради добычи и оставляют "
            "выжженные комнаты. Обстреляны достаточно, чтобы идти сквозь дым, а не стынуть в нём. "
            "Ждите агрессивный ближний бой: вспышка, угол, обшарить мёртвых. В набитых проёмах "
            "всё ещё паникуют — но паникуют вперёд."
        ),
    },
    "JAZZ_Legion_AssaultT2_Pyro": {
        "title_en": "Pyro",
        "title_ru": "Пироман",
        "body_en": (
            "Pyros bring fire into the breach — bottles, charges, anything that turns a room into "
            "a kiln. Already blooded; they enjoy the smell more than the Major admits. Deny them "
            "fuel lanes and tight interiors or your cover becomes a trap. CQB with a matchbook "
            "mentality: if they can't take the room, they burn it."
        ),
        "body_ru": (
            "Пироманы несут огонь в пролом — бутылки, заряды, всё, что превращает комнату в печь. "
            "Уже с кровью на руках; запах им нравится больше, чем признаёт Майор. Перекройте "
            "коридоры с горючим и тесные интерьеры — иначе укрытие станет западнёй. Ближний бой "
            "с мышлением спичечного коробка: комнату не взяли — сожгли."
        ),
    },
    "JAZZ_Legion_AssaultT2_ShockTrooper": {
        "title_en": "Shock Trooper",
        "title_ru": "Штурмовик",
        "body_en": (
            "Shock Troopers are the Legion's practiced breach team: stack, bang, clear. Not "
            "militia anymore — they know how to hold a door while the next man enters. Expect "
            "coordinated CQB and fewer wasted magazines. If they seize the first room, the rest "
            "of the building follows like a falling row of tiles."
        ),
        "body_ru": (
            "Штурмовики — отработанная группа пролома Легиона: стэк, хлопок, зачистка. Уже не "
            "ополчение — умеют держать дверь, пока входит следующий. Ждите согласованный ближний "
            "бой и меньше пустых очередей. Взяли первую комнату — остальное здание сыплется, "
            "как ряд плиток."
        ),
    },
    # --- Assault T3 ---
    "JAZZ_Legion_AssaultT3_Punisher": {
        "title_en": "Punisher",
        "title_ru": "Каратель",
        "body_en": (
            "Punishers are trained killers on a short leash — breach specialists who finish rooms "
            "the Major wants quiet. Drill shows: controlled entries, grenades on timers, no "
            "souvenir hunting mid-fight. They turn CQB into a conveyor. High threat once inside; "
            "do not gift them the stairwell."
        ),
        "body_ru": (
            "Каратели — вышколенные убийцы на коротком поводке: специалисты пролома, которые "
            "дочищают комнаты, которые Майор хочет тихими. Видна учёба: контролируемый вход, "
            "гранаты по таймеру, без охоты за сувенирами среди боя. Ближний бой у них — конвейер. "
            "Внутри — высокая угроза; лестницу им не дарите."
        ),
    },
    "JAZZ_Legion_AssaultT3_SkullCrusher": {
        "title_en": "Skull Crusher",
        "title_ru": "Череполом",
        "body_en": (
            "Skull Crushers pair heavy close-in iron with demolition habits — doors, walls, "
            "whatever blocks the rush. Trained, not rabble: they time the boom and walk through "
            "the dust. In assault lanes they erase cover you thought was permanent. Stop them "
            "before the charge, or rewrite your map after it."
        ),
        "body_ru": (
            "Череполомы совмещают тяжёлое ближнее железо с привычкой к подрыву — двери, стены, "
            "всё, что мешает рывку. Вышколены, не сброд: считают взрыв и идут сквозь пыль. "
            "На штурмовых осях стирают укрытия, которые казались вечными. Остановите до рывка — "
            "или переписывайте карту после."
        ),
    },
    # --- Assault T4 ---
    "JAZZ_Legion_AssaultT4_Headsman": {
        "title_en": "Headsman",
        "title_ru": "Палач",
        "body_en": (
            "Headsmen are paid steel — the Major's favourite breach artists. Top kit, cold "
            "timing, no wasted steps into a room. They clear buildings the way butchers clear "
            "hooks: methodical, loud only when it helps. Priority targets in any CQB; if one "
            "stacks on your door, the dossier already assumes you lose the room."
        ),
        "body_ru": (
            "Палачи — наёмная сталь, любимчики Майора на проломе. Лучший кит, холодный тайминг, "
            "ни шага зря в комнату. Чистят здания, как мясники — крючья: методично, громко "
            "только когда это помогает. Приоритет в любом ближнем бою; если такой встал на "
            "вашу дверь, досье уже предполагает, что комнату вы отдадите."
        ),
    },
    # --- Flanker T1 ---
    "JAZZ_Legion_FlankerT1_Warden": {
        "title_en": "Warden",
        "title_ru": "Дозорный",
        "body_en": (
            "Wardens haunt the edges — green scouts with itchy triggers and thin boots. They "
            "ambush runners more than they win gunfights. Ignore the map rim and they cut your "
            "retreat; watch them and they still waste a magazine into brush. Medium threat until "
            "you forget the flanks exist."
        ),
        "body_ru": (
            "Дозорные живут на краях карты — зелёные разведчики с зудящим спуском и тонкими "
            "ботинками. Чаще режут бегущих, чем выигрывают перестрелки. Забудете обочину — "
            "отрежут отход; будете смотреть — всё равно опустошат магазин в кусты. Угроза "
            "средняя, пока вы помните, что фланги существуют."
        ),
    },
    # --- Flanker T2 ---
    "JAZZ_Legion_FlankerT2_Scout": {
        "title_en": "Scout",
        "title_ru": "Скаут",
        "body_en": (
            "Scouts have blood on the boots already — they probe, mark, and call the ambush "
            "before you see the lane. Quieter than Wardens, meaner when you cross their trail. "
            "Expect side shots into overwatch and knives for stragglers. Lose sight of the edges "
            "and the fight arrives from the wrong compass."
        ),
        "body_ru": (
            "У скаутов уже кровь на ботинках — щупают, метят и зовут засаду раньше, чем вы "
            "увидите просеку. Тише дозорных, злее, если пересечёте их след. Ждите боковые "
            "выстрелы в овервотч и нож для отставших. Потеряете края карты — бой придёт с "
            "неверной стороны компаса."
        ),
    },
    "JAZZ_Legion_FlankerT2_Skirmisher": {
        "title_en": "Skirmisher",
        "title_ru": "Застрельщик",
        "body_en": (
            "Skirmishers fight the soft fight on the wing: hit, fade, hit again. Blooded enough "
            "to bait a chase into a second team. They do not hold ground — they punish anyone "
            "who leaves the centre column. Treat every empty alley as occupied until proven "
            "otherwise."
        ),
        "body_ru": (
            "Застрельщики ведут мягкий бой на крыле: удар, исчез, снова удар. Обстреляны "
            "достаточно, чтобы заманить погоню во вторую группу. Землю не держат — наказывают "
            "тех, кто вылез из центральной колонны. Считайте пустой переулок занятым, пока "
            "не доказано обратное."
        ),
    },
    # --- Flanker T3 ---
    "JAZZ_Legion_FlankerT3_Pathfinder": {
        "title_en": "Pathfinder",
        "title_ru": "Следопыт",
        "body_en": (
            "Pathfinders are trained trail killers — they own goat paths, ditch lines, and the "
            "blind spot behind your advance. Not militia: they set lanes and wait. Ambush "
            "quality jumps; runners die before they reach the road. Clear the edges before you "
            "celebrate the centre."
        ),
        "body_ru": (
            "Следопыты — вышколенные убийцы троп: им принадлежат козьи тропки, канавы и "
            "слепая зона за вашим наступлением. Не ополчение — ставят просеки и ждут. Качество "
            "засад растёт; бегущие гибнут, не дойдя до дороги. Зачистите края, прежде чем "
            "праздновать центр."
        ),
    },
    "JAZZ_Legion_FlankerT3_Recon": {
        "title_en": "Recon",
        "title_ru": "Разведчик",
        "body_en": (
            "Recon teams feed the Major eyes — trained to count, shadow, and only shoot when "
            "the ambush is already closed. They vanish after contact and return with friends. "
            "If you feel watched on the approach, you probably are. Kill them early or fight "
            "their report later."
        ),
        "body_ru": (
            "Разведчики кормят Майора глазами — умеют считать, вести хвост и стрелять только "
            "когда кольцо уже сомкнуто. После контакта исчезают и возвращаются с друзьями. "
            "Если на подходе кажется, что за вами смотрят — скорее всего, так и есть. Уберите "
            "их рано или потом бейтесь с их докладом."
        ),
    },
    # --- Flanker T4 ---
    "JAZZ_Legion_FlankerT4_Ranger": {
        "title_en": "Ranger",
        "title_ru": "Рейнджер",
        "body_en": (
            "Rangers are paid ghosts on the Major's favourite payroll — elite flank work with "
            "top glass and no wasted noise. They cut logistics, silence sentries, and collapse "
            "retreats. If one is on the board, assume every tree line is hostile. Priority "
            "kill: force multipliers who never stand in the middle."
        ),
        "body_ru": (
            "Рейнджеры — платные призраки в любимом списке Майора: элитный фланг, лучшая "
            "оптика, без лишнего шума. Режут снабжение, глушат часовых, схлопывают отходы. "
            "Если такой на доске — считайте каждую лесополосу враждебной. Приоритет: "
            "мультипликаторы силы, которые никогда не стоят в середине."
        ),
    },
    # --- Front T1 ---
    "JAZZ_Legion_FrontT1_Bonemaker": {
        "title_en": "Bonemaker",
        "title_ru": "Костоправ",
        "body_en": (
            "Bonemakers are the Legion's field medics with rifles — they hold the line while "
            "dragging their own back up. Green kit, shaky aim, but every one you leave alive "
            "puts another Legionnaire on his feet. Overwatch around their stretchers; they "
            "punish heroic rushes more than they win duels."
        ),
        "body_ru": (
            "Костоправы — полевые медики Легиона с винтовками: держат линию и одновременно "
            "поднимают своих. Сырой кит, дрожащий прицел, но каждый живой снова ставит "
            "легионера на ноги. Держите овервотч вокруг их носилок — они сильнее наказывают "
            "героические рывки, чем выигрывают дуэли."
        ),
    },
    "JAZZ_Legion_FrontT1_Marauder": {
        "title_en": "Marauder",
        "title_ru": "Мародёр",
        "body_en": (
            "Marauders fill the firing line with scavenged rifles and bad attitudes. Green, "
            "loud, and fond of spraying the lane they think is yours. They hold ground by "
            "volume more than craft. Steady threat if you stand in the open; softer if you "
            "force them to move."
        ),
        "body_ru": (
            "Мародёры заполняют линию огня трофейными винтовками и скверным нравом. Зелёные, "
            "шумные, любят поливать просеку, которую считают вашей. Держат землю объёмом "
            "огня, не мастерством. Угроза ровная, если стоите на открытом; мягче, если "
            "заставите их двигаться."
        ),
    },
    "JAZZ_Legion_FrontT1_Rifleman": {
        "title_en": "Rifleman",
        "title_ru": "Стрелок",
        "body_en": (
            "Riflemen are the textbook green line — aimed shots when they remember to breathe, "
            "panic magazines when they don't. They overwatch doorways with more hope than "
            "skill. Still: a patient bullet from cover kills heroes. Punish mistakes harder "
            "than they punish courage."
        ),
        "body_ru": (
            "Стрелки — учебниковая зелёная линия: прицельный выстрел, если вспомнят дышать, "
            "панический магазин — если нет. Держат овервотч на дверях скорее надеждой, чем "
            "умением. И всё же терпеливая пуля из укрытия убивает героев. Ошибки наказывают "
            "жёстче, чем храбрость."
        ),
    },
    # --- Front T2 ---
    "JAZZ_Legion_FrontT2_Ambusher": {
        "title_en": "Ambusher",
        "title_ru": "Засадник",
        "body_en": (
            "Ambushers own prepared lanes on the front — blooded shooters who wait for the "
            "first man to cross a chalk line. Not runners; hunters with a static kill zone. "
            "Expect overwatch that actually bites. Probe with smoke or angles before you "
            "commit the column."
        ),
        "body_ru": (
            "Засадники владеют подготовленными просеками на фронте — обстрелянные стрелки, "
            "ждущие, пока первый пересечёт меловую черту. Не бегуны; охотники со статичной "
            "зоной поражения. Овервотч у них уже кусается. Щупайте дымом или углами, прежде "
            "чем гнать колонну."
        ),
    },
    "JAZZ_Legion_FrontT2_Marksman": {
        "title_en": "Marksman",
        "title_ru": "Охотник",
        "body_en": (
            "Marksmen pick officers and MG nests from the second rank — blooded enough to "
            "hold fire until the shot matters. They punish silhouettes on ridges and anyone "
            "who peeks the same window twice. Steady threat: they do not need to rush you."
        ),
        "body_ru": (
            "Охотники снимают офицеров и пулемётные точки со второго ряда — обстреляны "
            "достаточно, чтобы ждать выстрела, который важен. Наказывают силуэты на гребнях "
            "и тех, кто выглядывает в одно окно дважды. Угроза ровная: им не нужно к вам "
            "бежать."
        ),
    },
    "JAZZ_Legion_FrontT2_Raider": {
        "title_en": "Raider",
        "title_ru": "Налётчик",
        "body_en": (
            "Raiders are line troops with a habit of sudden advances — blooded soldiers who "
            "push after a volley instead of hugging dirt forever. They hold, then take the "
            "next wall. Overwatch plus short assaults: treat them as a moving front, not a "
            "static fence."
        ),
        "body_ru": (
            "Налётчики — линейные с привычкой к внезапному рывку: обстрелянные солдаты, "
            "которые после залпа идут вперёд, а не вечно жмутся к земле. Держат — и берут "
            "следующую стену. Овервотч плюс короткие штурмы: это движущийся фронт, не "
            "статичный забор."
        ),
    },
    # --- Front T3 ---
    "JAZZ_Legion_FrontT3_Sniper": {
        "title_en": "Sniper",
        "title_ru": "Снайпер",
        "body_en": (
            "Legion snipers are trained glass — one shot, one changed plan. They pick lanes "
            "and wait; heroics across open ground are gifts. Not militia with scopes: they "
            "know when to relocate after the first kill. Clear overwatch before you stack "
            "for assault."
        ),
        "body_ru": (
            "Снайперы Легиона — вышколенная оптика: один выстрел, один сломанный план. "
            "Выбирают просеку и ждут; героизм через открытое — подарок. Не ополчение с "
            "прицелом: умеют сменить позицию после первого трупа. Снимите овервотч, прежде "
            "чем собирать стэк на штурм."
        ),
    },
    "JAZZ_Legion_FrontT3_Veteran": {
        "title_en": "Veteran",
        "title_ru": "Ветеран",
        "body_en": (
            "Veterans are the backbone of a trained Legion line — patient fire, smart "
            "overwatch, few wasted magazines. They punish mistakes and survive the ones you "
            "thought would break them. Expect grenade tricks and disciplined mutual support. "
            "Steady, ugly threat."
        ),
        "body_ru": (
            "Ветераны — хребет вышколенной линии Легиона: терпеливый огонь, умный овервотч, "
            "мало пустых магазинов. Наказывают ошибки и переживают те, что должны были их "
            "сломить. Ждите гранатные фокусы и взаимную поддержку. Угроза ровная и неприятная."
        ),
    },
    # --- Front T4 ---
    "JAZZ_Legion_FrontT4_Mercenary": {
        "title_en": "Mercenary",
        "title_ru": "Наёмник",
        "body_en": (
            "Mercenaries on the Major's payroll fight like professionals who bill by the "
            "hour — paid steel on the line. Top kit, calm overwatch, no panic dumps. They "
            "hold sectors the way contractors hold contracts. Kill them or pay later in "
            "reinforcements."
        ),
        "body_ru": (
            "Наёмники на жалованье Майора бьются как профи с почасовой оплатой — платная "
            "сталь на линии. Лучший кит, спокойный овервотч, без панических очередей. "
            "Держат сектора, как подрядчики держат контракты. Уберите их — или потом "
            "платите подкреплениями."
        ),
    },
    "JAZZ_Legion_FrontT4_MercenarySniper": {
        "title_en": "Mercenary Sniper",
        "title_ru": "Наёмник-снайпер",
        "body_en": (
            "Mercenary Snipers are the Major's favourite long knives — paid glass that "
            "erases leadership and MG before the assault starts. Relocate after every "
            "shot; expect no second chance in the same window. Priority over almost "
            "everything else on the front."
        ),
        "body_ru": (
            "Наёмные снайперы — любимые длинные ножи Майора: платная оптика, которая "
            "снимает командиров и пулемёты до начала штурма. Меняют позицию после каждого "
            "выстрела; второго шанса в том же окне не ждите. Приоритет почти над всем "
            "остальным на фронте."
        ),
    },
    # --- Gunner T1 ---
    "JAZZ_Legion_GunnerT1_Gunner": {
        "title_en": "Gunner",
        "title_ru": "Пуляло",
        "body_en": (
            "Green gunners own a lane with belts they barely know how to feed. Loud, "
            "inaccurate, still enough to pin anyone who stands tall in the open. Soft in "
            "tight rooms; brutal across courtyards. Flank them or eat suppression."
        ),
        "body_ru": (
            "Зелёные пулемётчики держат просеку лентами, которые едва умеют подавать. "
            "Громко, криво — но достаточно, чтобы прижать тех, кто выпрямился на открытом. "
            "В тесных комнатах мягче; через дворы — жестоко. Зайдите с фланга или ешьте "
            "подавление."
        ),
    },
    # --- Gunner T2 ---
    "JAZZ_Legion_GunnerT2_AssaultGunner": {
        "title_en": "Assault Gunner",
        "title_ru": "Коммандо",
        "body_en": (
            "Assault Gunners walk the belt forward — blooded crews who displace with the "
            "push instead of camping one sandbag forever. Suppression that moves with the "
            "breach. Open ground still favours them; rooms punish slow mounts. Deny the "
            "approach or pay in inches."
        ),
        "body_ru": (
            "Штурмовые пулемётчики несут ленту вперёд — обстрелянные расчёты, которые "
            "смещаются с натиском, а не вечно сидят за одним мешком. Подавление, идущее "
            "вместе с проломом. Открытое всё ещё их; комнаты наказывают медленную установку. "
            "Перекройте подход — или платите метрами."
        ),
    },
    "JAZZ_Legion_GunnerT2_GMPG": {
        "title_en": "GPMG",
        "title_ru": "Пулемётчик",
        "body_en": (
            "GPMG teams are the classic blooded nest — sustained belts, interlocking "
            "lanes, patience. They deny approaches until something bigger breaks the "
            "gun. High threat across plazas; softer if you force a move under fire. "
            "Smoke and angles beat heroism."
        ),
        "body_ru": (
            "Расчёты GPMG — классическое обстрелянное гнездо: длинные ленты, пересекающиеся "
            "просеки, терпение. Закрывают подходы, пока что-то крупнее не сломает ствол. "
            "Угроза высокая через площади; мягче, если заставить смещаться под огнём. "
            "Дым и углы бьют героизм."
        ),
    },
    # --- Gunner T3 ---
    "JAZZ_Legion_GunnerT3_VeteranGunner": {
        "title_en": "Veteran Gunner",
        "title_ru": "Подавитель",
        "body_en": (
            "Veteran Gunners are trained belt artists — they walk fire, save bursts, and "
            "kill the first man who thinks the lane is clear. Not militia with a bipod. "
            "Expect disciplined suppression that shapes the whole fight. Flank hard or "
            "bring boom."
        ),
        "body_ru": (
            "Ветераны-пулемётчики — вышколенные мастера ленты: водят огонь, экономят "
            "очереди и убивают первого, кто решил, что просека чиста. Не ополчение с "
            "сошками. Ждите дисциплинированное подавление, которое лепит весь бой. Жёсткий "
            "фланг или тяжёлое железо."
        ),
    },
    # --- Gunner T4 ---
    "JAZZ_Legion_GunnerT4_MercGunner": {
        "title_en": "Merc Gunner",
        "title_ru": "Наёмник-пулемётчик",
        "body_en": (
            "Merc Gunners are paid steel behind the best belts the Major can buy. They "
            "own open ground like contractors own a clause. Relocate under smoke, reappear "
            "on a worse angle. Priority target: one nest can freeze a whole push."
        ),
        "body_ru": (
            "Наёмные пулемётчики — платная сталь за лучшими лентами, какие Майор может "
            "купить. Владеют открытым, как подрядчики — пунктом договора. Уходят под дымом "
            "и встают под худшим углом. Приоритет: одно гнездо может заморозить весь натиск."
        ),
    },
    # --- Heavy T1 ---
    "JAZZ_Legion_HeavyT1_Rocketeer": {
        "title_en": "Rocketeer",
        "title_ru": "Ракетчик",
        "body_en": (
            "Green rocketeers still flinch at their own backblast — and still erase a "
            "wall if the tube leaves the shoulder. Spike threat: one shot rewrites cover "
            "and morale. Soft if you catch them mid-reload; catastrophic if you stack in "
            "their sight picture. Area denial by accident and intent."
        ),
        "body_ru": (
            "Зелёные ракетчики ещё вздрагивают от собственного подрыва сзади — и всё равно "
            "сносят стену, если труба ушла с плеча. Угроза-всплеск: один выстрел переписывает "
            "укрытия и мораль. Мягкие, если поймать на перезарядке; катастрофа, если "
            "встать им в прицел. Зона поражения — и по привычке, и по заданию."
        ),
    },
    # --- Heavy T2 ---
    "JAZZ_Legion_HeavyT2_Grenadier": {
        "title_en": "Grenadier",
        "title_ru": "Гранатомётчик",
        "body_en": (
            "Heavy Grenadiers are blooded boom specialists — tubes and launchers that "
            "carve rooms and courtyards. They shape approaches with timed blasts, not "
            "hope. Expect area denial that forces you into their gunners' lanes. Kill "
            "or displace before the second round lands."
        ),
        "body_ru": (
            "Тяжёлые гранатомётчики — обстрелянные специалисты грома: трубы и пусковые, "
            "которые режут комнаты и дворы. Формируют подходы взрывами по таймеру, не "
            "надеждой. Ждите зону поражения, которая гонит вас под чужие пулемёты. "
            "Уберите или сместите до второго выстрела."
        ),
    },
    # --- Heavy T3 ---
    "JAZZ_Legion_HeavyT3_Mortarman": {
        "title_en": "Mortarman",
        "title_ru": "Миномётчик",
        "body_en": (
            "Mortarmen are trained to drop steel where you thought the sky was empty. "
            "Indirect fire turns cover into a suggestion. Not militia with a tube: they "
            "walk rounds onto a grid. Break the team or abandon the square — standing "
            "still under trained mortar is a choice, not a plan."
        ),
        "body_ru": (
            "Миномётчики вышколены ронять железо туда, где небо казалось пустым. Навесной "
            "огонь превращает укрытие в рекомендацию. Не ополчение с трубой — ведут "
            "разрывы по сетке. Сломайте расчёт или бросьте квадрат: стоять под вышколенным "
            "миномётом — выбор, не план."
        ),
    },
    # --- Leader T1 ---
    "JAZZ_Legion_LeaderT1_Sergeant": {
        "title_en": "Sergeant",
        "title_ru": "Бригадир",
        "body_en": (
            "Sergeants keep green packs pointed the same way — shouted orders, slapstick "
            "rally, enough presence to stop a rout. Soft individually; dangerous as a "
            "force multiplier. Kill the voice early and the rabble forgets why it came."
        ),
        "body_ru": (
            "Бригадиры держат зелёную стаю в одном направлении — резкие окрики, грубый "
            "сбор, достаточно присутствия, чтобы остановить бегство. Поодиночке мягки; "
            "опасны как усилитель отряда. Уберите голос рано — сброд забудет, зачем "
            "пришёл."
        ),
    },
    # --- Leader T2 ---
    "JAZZ_Legion_LeaderT2_Lieutenant": {
        "title_en": "Lieutenant",
        "title_ru": "Командир",
        "body_en": (
            "Lieutenants are blooded mid-tier glue — they rally after the first casualties "
            "and push the pack instead of letting it melt. Expect timed advances and "
            "fewer freezes under fire. Force multiplier: remove them and the local plan "
            "collapses into noise."
        ),
        "body_ru": (
            "Лейтенанты — обстрелянный клей среднего звена: собирают после первых потерь "
            "и толкают стаю, а не дают ей растаять. Ждите выверенные рывки и меньше "
            "оцепенения под огнём. Мультипликатор силы: уберите их — местный план "
            "схлопнется в шум."
        ),
    },
    # --- Leader T3 ---
    "JAZZ_Legion_LeaderT3_Captain": {
        "title_en": "Captain",
        "title_ru": "Советник",
        "body_en": (
            "Captains are trained commanders who make rabble fight like a unit — fire "
            "control, mutual support, ugly competence. The Major trusts them with "
            "sectors that matter. Priority kill: every minute they live, the Legion "
            "around them gets smarter."
        ),
        "body_ru": (
            "Капитаны — вышколенные командиры, из сброда делают подразделение: контроль "
            "огня, взаимная поддержка, неприятная грамотность. Майор доверяет им сектора, "
            "которые важны. Приоритет: каждую минуту их жизни Легион вокруг умнеет."
        ),
    },
    # --- Leader T4 ---
    "JAZZ_Legion_LeaderT4_MercenaryCaptain": {
        "title_en": "Mercenary Captain",
        "title_ru": "Мастер",
        "body_en": (
            "Mercenary Captains are paid steel with a radio — elite force multipliers on "
            "the Major's short list. They hold cohesion under disasters that would scatter "
            "militia. If one is present, assume the fight has a brain. Kill first; argue "
            "about medals later."
        ),
        "body_ru": (
            "Наёмные капитаны — платная сталь с рацией: элитные мультипликаторы в коротком "
            "списке Майора. Держат связность под катастрофами, которые развеяли бы ополчение. "
            "Если такой на поле — у боя есть мозг. Уберите первым; о медалях поспорите "
            "потом."
        ),
    },
}

# ---------------------------------------------------------------------------
# Quest / faction dossiers
# ---------------------------------------------------------------------------

QUEST_DOSSIERS: dict[str, dict[str, str]] = {
    "Pierre": {
        "title_en": "Pierre Laurent",
        "title_ru": "Пьер Лоран",
        "body_en": (
            "Father's boy turned Legion face on Ernie — pride, pressed uniforms, and a chip "
            "on the shoulder big enough to hide a rifle behind. Useful as a weather vane for "
            "how hard the Major is leaning on the island. Treat charm as cover fire."
        ),
        "body_ru": (
            "Папенькин сынок, ставший лицом Легиона на Эрни — гордость, выглаженная форма и "
            "обида размером с винтовку за спиной. Удобен как флюгер: по нему видно, как сильно "
            "Майор давит на остров. Обаяние считайте прикрывающим огнём."
        ),
    },
    "Bastien": {
        "title_en": "Bastien",
        "title_ru": "Бастьен",
        "body_en": (
            "Local muscle with a merchant's smile. When he talks trade, listen for who really "
            "owns the road — tolls, tips, and quiet threats travel the same dirt. Desk note: "
            "useful contact, never a friend."
        ),
        "body_ru": (
            "Местная сила с улыбкой торговца. Когда говорит о торговле, слушайте, кто на "
            "самом деле держит дорогу — пошлины, наводки и тихие угрозы ходят по одной пыли. "
            "Заметка стола: полезный контакт, никогда не друг."
        ),
    },
    "TheMajor": {
        "title_en": "The Major",
        "title_ru": "Майор",
        "body_en": (
            "Not a rumor — a commander who builds an army from fear, payroll, and stolen "
            "warehouses. Every supply brief on this desk is really about him. Expect "
            "patience, cruelty, and a long memory for whoever spoils his inventory."
        ),
        "body_ru": (
            "Не слух — командир, который собирает армию из страха, жалованья и краденых "
            "складов. Каждая сводка снабжения на этом столе на самом деле о нём. Ждите "
            "терпения, жестокости и длинной памяти к тем, кто портит его учёт."
        ),
    },
    "Legion": {
        "title_en": "Legion (faction)",
        "title_ru": "Легион (фракция)",
        "body_en": (
            "A private war machine wearing stolen legitimacy. Expect raids, pressed "
            "recruits, and officers who treat villages like inventory ledgers. The "
            "faction is the Major's shadow cast across every sector you will fight."
        ),
        "body_ru": (
            "Частная военная машина в краденой легитимности. Ждите налётов, рекрутов "
            "под конвоем и офицеров, для которых деревня — строка в инвентаре. Фракция — "
            "тень Майора на каждом секторе, где вам предстоит биться."
        ),
    },
}

# ---------------------------------------------------------------------------
# Loc string fixes: (id_str, en, ru)
# ---------------------------------------------------------------------------

WELCOME_FIXES: list[tuple[str, str, str]] = [
    (
        "890000000006922",
        "R.I.S. — complimentary intelligence subscription",
        "R.I.S. — бесплатная подписка разведки",
    ),
    (
        "890000000006923",
        (
            "Commander,\n\n"
            "Recon Intelligence Services has activated your complimentary field subscription "
            "for this campaign. We will send assessments when Legion supply quality shifts, "
            "and host dossiers and battle reports on our PDA site as the desk expands.\n\n"
            "Read this message to unlock the R.I.S. browser tab.\n\n"
            "— Recon Intelligence Services"
        ),
        (
            "Командир,\n\n"
            "Разведывательная служба R.I.S. открыла вам бесплатную полевую подписку на эту "
            "кампанию. Мы будем присылать оценки, когда изменится качество снабжения Легиона, "
            "а на сайте в КПК — вести досье и боевые сводки по мере расширения стола.\n\n"
            "Прочитайте это письмо, чтобы открыть вкладку R.I.S.\n\n"
            "— Разведывательная служба R.I.S."
        ),
    ),
    (
        "890000000006924",
        (
            "Recon Intelligence Services\n\n"
            "Complimentary field subscription active. Dossiers and battle reports will appear "
            "here as the desk expands.\n\n"
            "Watch your inbox for Legion supply assessments."
        ),
        (
            "Разведывательная служба R.I.S.\n\n"
            "Бесплатная полевая подписка активна. Досье и боевые сводки появятся здесь по мере "
            "расширения стола.\n\n"
            "Следите за почтой — там оценки снабжения Легиона."
        ),
    ),
]

UI_FIXES: list[tuple[str, str, str]] = [
    (
        "890000000011000",
        "Recon Intelligence Services",
        "Разведывательная служба R.I.S.",
    ),
    (
        "890000000011001",
        "Bulletin",
        "Сводка",
    ),
    (
        "890000000011002",
        "Dossiers",
        "Досье",
    ),
    (
        "890000000011003",
        "Battle reports",
        "Боевые сводки",
    ),
    (
        "890000000011004",
        "No supply briefs on file yet. Watch your inbox — R.I.S. mails appear here after you receive them.",
        "Оценок снабжения пока нет. Следите за почтой — письма R.I.S. появятся здесь после получения.",
    ),
    (
        "890000000011005",
        "No dossiers unlocked yet. New Legion types appear here when their R.I.S. contact note arrives.",
        "Досье ещё не открыты. Новые типы Легиона появляются здесь, когда приходит заметка R.I.S. о контакте.",
    ),
    (
        "890000000011006",
        "No battle reports yet. Finish a fight — the desk will file a summary here (no mail spam).",
        "Боевых сводок пока нет. Завершите бой — стол положит сюда отчёт (без спама в почту).",
    ),
    (
        "890000000011007",
        "Observed kills: <count>/3",
        "Зафиксировано убийств: <count>/3",
    ),
    (
        "890000000011008",
        "(sealed — need 3 confirmed kills)",
        "(запечатано — нужно 3 подтверждённых убийства)",
    ),
    (
        "890000000011009",
        "Persons of interest",
        "Особые фигуры",
    ),
    (
        "890000000011010",
        "Legion types",
        "Типы Легиона",
    ),
    (
        "890000000011011",
        "Latest supply assessment",
        "Последняя оценка снабжения",
    ),
    (
        "890000000011012",
        "R.I.S. mail archive",
        "Архив писем R.I.S.",
    ),
]

# AAR samples that read as calques / machine RU — polish RU, keep EN desk-voice.
AAR_FIXES: list[tuple[str, str, str]] = [
    # Headlines with rough RU
    (
        "890000000011108",
        "Bad ground, worse timing",
        "Плохая позиция, ещё хуже момент",
    ),
    (
        "890000000011118",
        "Pulled out under pressure",
        "Отошли под давлением",
    ),
    (
        "890000000011122",
        "Ran the gauntlet out",
        "Пробились наружу сквозь огонь",
    ),
    # Weather / intensity labels that sound like spreadsheet headers
    (
        "890000000011124",
        "Weather: clear skies over the fight.",
        "Над боем — ясное небо.",
    ),
    (
        "890000000011125",
        "Weather: rain turned powder damp and tempers shorter.",
        "Дождь отсырил порох и укоротил нервы.",
    ),
    (
        "890000000011126",
        "Weather/time: night fight — muzzle flashes did the talking.",
        "Ночной бой — говорили вспышки дул.",
    ),
    (
        "890000000011127",
        "Weather: fog cut sightlines; everyone hugged cover.",
        "Туман резал обзор; все жались к укрытиям.",
    ),
    (
        "890000000011128",
        "Weather: baking heat — fatigue hit as hard as bullets.",
        "Пекло — усталость била не хуже пуль.",
    ),
    (
        "890000000011129",
        "Weather: dust storm grit in every weapon.",
        "Пылевая буря — песок в каждом стволе.",
    ),
    (
        "890000000011130",
        "Weather: unremarkable — the shooting was the story.",
        "Погода обычная — историю сделала стрельба.",
    ),
    (
        "890000000011131",
        "Intensity: a sharp exchange, then quiet. Heat on the grid barely stirred.",
        "Короткая перестрелка — и тишина. Жара на клетке почти не шевельнулась.",
    ),
    (
        "890000000011132",
        "Intensity: sustained fire and movement. Local Heat climbed enough for the desk to notice.",
        "Плотный огонь и манёвр. Местная Жара выросла так, что стол это заметил.",
    ),
    (
        "890000000011133",
        "Intensity: a meat grinder. Expect the Major's network to smell the smoke.",
        "Мясорубка. Сеть Майора наверняка учует дым.",
    ),
    (
        "890000000011134",
        "Forces: roughly <player> friendlies against <enemy> hostiles at contact.",
        "Силы на контакте: примерно <player> своих против <enemy> противника.",
    ),
    (
        "890000000011135",
        "Theatre: <sector>.",
        "Район: <sector>.",
    ),
    (
        "890000000011136",
        "Theatre: <sector> — local label <poi>.",
        "Район: <sector> — местное название <poi>.",
    ),
    # Quest / character lines (calques)
    (
        "890000000011137",
        "Operational thread: <quest>. Desk note on this grid: <note>",
        "Оперативная линия: <quest>. Заметка стола по клетке: <note>",
    ),
    (
        "890000000011138",
        "Operational thread: <quest> — badges pin this fight to that job.",
        "Оперативная линия: <quest> — метки привязывают этот бой к заданию.",
    ),
    (
        "890000000011139",
        "Operational threads on this sector: <quests>. Treat the shooting as part of those jobs, not random noise.",
        "На секторе сходятся задания: <quests>. Стрельбу считайте частью этих дел, а не случайным шумом.",
    ),
    (
        "890000000011140",
        "Active desk job (not sector-badged): <quest>.",
        "Активное задание стола (без метки на секторе): <quest>.",
    ),
    (
        "890000000011141",
        "No live quest badge on this grid — logged as a free-fire sector action.",
        "Живой метки задания на клетке нет — записано как свободный бой за сектор.",
    ),
    (
        "890000000011142",
        "Character: your side held the field.",
        "Характер боя: поле осталось за вами.",
    ),
    (
        "890000000011143",
        "Character: the enemy kept the sector.",
        "Характер боя: сектор остался у противника.",
    ),
    (
        "890000000011144",
        "Character: fighting withdrawal — not a stand.",
        "Характер боя: отход с боем — не стояли насмерть.",
    ),
    (
        "890000000011145",
        "Character: smelled like an ambush — first shots decided the map.",
        "Характер боя: похоже на засаду — первые выстрелы решили карту.",
    ),
    (
        "890000000011146",
        "Character: quest-linked fight — objective pressure held; the sector stayed yours.",
        "Характер боя: бой по заданию — давление по цели выдержали; сектор ваш.",
    ),
    (
        "890000000011147",
        "Character: quest-linked fight — the job on this grid just got harder.",
        "Характер боя: бой по заданию — дело на этой клетке только усложнилось.",
    ),
    (
        "890000000011148",
        "Character: quest-linked withdrawal — you left the badge sector under protest.",
        "Характер боя: отход по заданию — ушли с отмеченного сектора не по плану.",
    ),
    (
        "890000000011149",
        "Losses: friendlies KIA <pkia>, WIA <pwia>; hostiles KIA <ekia>, WIA <ewia>.",
        "Потери: свои убиты <pkia>, ранены <pwia>; противник убит <ekia>, ранен <ewia>.",
    ),
    (
        "890000000011154",
        "Closing: the sector goes quiet; Heat footprint looks manageable.",
        "Итог: сектор стихает; след Жары выглядит управляемым.",
    ),
    (
        "890000000011155",
        "Closing: the noise will travel — patrols and payoffs usually follow.",
        "Итог: шум разнесётся — обычно следом идут патрули и выплаты.",
    ),
    (
        "890000000011156",
        "Closing: write this one in red. Command will ask hard questions.",
        "Итог: пишите красным. Командование будет спрашивать жёстко.",
    ),
]

STRING_FIXES: list[tuple[str, str, str]] = WELCOME_FIXES + UI_FIXES + AAR_FIXES

__all__ = [
    "DOSSIERS",
    "QUEST_DOSSIERS",
    "WELCOME_FIXES",
    "UI_FIXES",
    "AAR_FIXES",
    "STRING_FIXES",
]
