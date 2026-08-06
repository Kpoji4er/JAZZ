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
        "title_ru": "Новобранец",
        "body_en": (
            "Legion recruiters sweep up villagers and send them out after only a few days of drill. They "
            "rush forward with whatever weapon they are handed, but lack the training and staying power "
            "of regular troops. Keep them at range and break up the group before they crowd a doorway or "
            "surround a lone merc."
        ),
        "body_ru": (
            "Вербовщики Легиона собирают людей по деревням и отправляют в бой после нескольких дней "
            "муштры. Они бросаются вперёд с тем оружием, которое им выдали, но заметно уступают кадровым "
            "бойцам в подготовке и стойкости. Держите дистанцию и разбейте их группу, прежде чем они "
            "забьют дверной проём или окружат отставшего наёмника."
        ),
    },
    # --- Assault T1 ---
    "JAZZ_Legion_AssaultT1_Crusher": {
        "title_en": "Crusher",
        "title_ru": "Громила",
        "body_en": (
            "The Legion picks its strongest bruisers for Crusher duty and teaches them one job: close the "
            "distance. A shotgun, solid armor, and sheer toughness make them dangerous inside rooms and "
            "narrow alleys. Do not meet them in a doorway; open the range and concentrate fire before the "
            "shotgun takes over."
        ),
        "body_ru": (
            "Громилами в Легионе становятся самые крепкие бойцы; их учат одному — любой ценой сократить "
            "дистанцию. Дробовик, добротная броня и недюжинная выносливость делают их особенно опасными в "
            "комнатах и узких переулках. Не встречайте Громилу в дверях — отходите на простор и "
            "сосредоточьте огонь, пока он не подошёл вплотную."
        ),
    },
    "JAZZ_Legion_AssaultT1_Grenadier": {
        "title_en": "Grenadier",
        "title_ru": "Гренадёр",
        "body_en": (
            "New Grenadiers receive a short course in assault explosives before the Legion sends them "
            "forward. They carry several grenades beside a pistol or submachine gun, and some add a "
            "bottle of burning fuel. Spread out, keep an escape route from cover, and shoot them before "
            "they settle behind a corner."
        ),
        "body_ru": (
            "Новых Гренадёров наскоро учат обращению со взрывчаткой, после чего Легион сразу бросает их в "
            "штурм. Кроме пистолета или пистолета-пулемёта, у них есть несколько гранат, а иногда и "
            "бутылка с зажигательной смесью. Не стойте кучно, оставьте себе выход из укрытия и снимайте "
            "Гренадёра до того, как он устроится за углом."
        ),
    },
    "JAZZ_Legion_AssaultT1_Roughneck": {
        "title_en": "Roughneck",
        "title_ru": "Головорез",
        "body_en": (
            "Roughnecks receive little formal training; the Legion expects speed and aggression to make "
            "up the difference. They fire pistols or automatic weapons on the move and often carry a "
            "knife for the last few steps. Make them cross open ground under overlapping fire, and do not "
            "let them turn a cramped room into a brawl."
        ),
        "body_ru": (
            "Головорезов почти не учат: Легион рассчитывает, что нехватку подготовки заменят скорость и "
            "напор. Они стреляют из пистолетов или автоматического оружия на ходу, а для последних шагов "
            "нередко берут нож. Заставьте их пересекать открытое место под перекрёстным огнём и не "
            "позволяйте превратить тесную комнату в драку."
        ),
    },
    # --- Assault T2 ---
    "JAZZ_Legion_AssaultT2_Pillager": {
        "title_en": "Pillager",
        "title_ru": "Грабитель",
        "body_en": (
            "The Legion forms Pillager teams from raiders who survived their first street fights and "
            "learned to keep moving. Light armor keeps them quick as they press close with an automatic "
            "weapon and, more often than not, a knife. Hold a long line of fire and do not chase them "
            "around a blind corner."
        ),
        "body_ru": (
            "Грабителями становятся налётчики, которые пережили первые уличные бои и научились не "
            "останавливаться под огнём. Лёгкая броня не мешает им быстро сближаться с автоматическим "
            "оружием и, чаще всего, ножом. Не подпускайте их, держите подходы под огнём и не гонитесь за "
            "ними за непросматриваемый угол."
        ),
    },
    "JAZZ_Legion_AssaultT2_Pyro": {
        "title_en": "Pyro",
        "title_ru": "Пироман",
        "body_en": (
            "Pyros are assault troops singled out for incendiary work rather than careful demolition. "
            "They wear heavy armor, carry several firebombs, and follow the flames with a submachine gun "
            "or short rifle. Spread out, stay clear of dead-end cover, and bring them down before they "
            "get within throwing distance."
        ),
        "body_ru": (
            "Пироманов отбирают из штурмовых отрядов и отдельно учат обращению с зажигательными смесями. "
            "Они носят тяжёлую броню, берут несколько бутылок с огнём и идут следом с "
            "пистолетом-пулемётом или короткой винтовкой. Не стойте кучно, избегайте тупиковых укрытий и "
            "снимайте их до броска."
        ),
    },
    "JAZZ_Legion_AssaultT2_ShockTrooper": {
        "title_en": "Shock Trooper",
        "title_ru": "Штурмовик",
        "body_en": (
            "Shock Troopers are survivors of the early assault ranks, retrained to keep an attack moving "
            "through resistance. They open the assault with several grenades, then close in with an "
            "automatic weapon; some also carry smoke or concussion charges. Do not bunch behind one "
            "wall—pin them in the open before a grenade clears their route."
        ),
        "body_ru": (
            "Штурмовики — это бойцы ранних штурмовых отрядов, которых переучили не останавливать атаку "
            "под ответным огнём. Они начинают штурм с нескольких гранат, а затем сближаются с "
            "автоматическим оружием; у некоторых есть дымовые или оглушающие заряды. Не собирайтесь за "
            "одной стеной — прижмите их на открытом месте до первого броска."
        ),
    },
    # --- Assault T3 ---
    "JAZZ_Legion_AssaultT3_Punisher": {
        "title_en": "Punisher",
        "title_ru": "Каратель",
        "body_en": (
            "Punishers are drawn from assault veterans and trained to keep an attack moving after the "
            "first breach. Heavy armor, automatic rifles, and a full load of grenades let them press "
            "forward even when the defense holds. Engage from more than one angle, keep a second position "
            "ready, and finish one before switching targets."
        ),
        "body_ru": (
            "Карателей набирают из опытных штурмовиков и учат не сбавлять темп после первого пролома. "
            "Тяжёлая броня, автоматические винтовки и большой запас гранат позволяют им идти вперёд, даже "
            "когда оборона держится. Бейте с разных сторон, заранее готовьте запасную позицию и добивайте "
            "одного, прежде чем переносить огонь."
        ),
    },
    "JAZZ_Legion_AssaultT3_SkullCrusher": {
        "title_en": "Skull Crusher",
        "title_ru": "Череполом",
        "body_en": (
            "Skull Crushers are veteran brawlers trained to force a close fight through smoke and "
            "confusion. Heavy armor carries them into shotgun or submachine-gun range, where most of them "
            "also have a machete and some bring smoke or firebombs. Keep a clear way out of tight "
            "interiors and wear them down before they can rush."
        ),
        "body_ru": (
            "Череполомов набирают из опытных драчунов и учат навязывать ближний бой в дыму и неразберихе. "
            "Тяжёлая броня помогает им дойти до дистанции дробовика или пистолета-пулемёта; почти каждый "
            "берёт мачете, а некоторые — дым или зажигательную смесь. Оставляйте себе выход из тесных "
            "помещений и изматывайте их до рывка."
        ),
    },
    # --- Assault T4 ---
    "JAZZ_Legion_AssaultT4_Headsman": {
        "title_en": "Headsman",
        "title_ru": "Палач",
        "body_en": (
            "Only the Legion's best assault veterans are promoted to Headsman duty and equipped as elite "
            "professionals. Heavy armor, upgraded automatic weapons, and plenty of grenades let them "
            "cross ground quickly and keep attacking at close range. Make them the first target, cover "
            "more than one approach, and never leave a lone merc on their flank."
        ),
        "body_ru": (
            "Палачами становятся лучшие ветераны штурмовых отрядов; их снаряжают как настоящих "
            "профессионалов. Тяжёлая броня, улучшенное автоматическое оружие и большой запас гранат "
            "позволяют им быстро сближаться и не прерывать атаку. Бейте Палача первым, держите под "
            "контролем несколько подходов и не оставляйте одиночного наёмника у него на фланге."
        ),
    },
    # --- Flanker T1 ---
    "JAZZ_Legion_FlankerT1_Warden": {
        "title_en": "Warden",
        "title_ru": "Дозорный",
        "body_en": (
            "Wardens are ordinary riflemen given basic scouting instruction and posted away from the main "
            "line. Their light gear helps them reach a side position, where they hold cover and punish "
            "movement with steady rifle fire. Check both flanks before advancing, and use smoke or a "
            "second angle to dislodge them."
        ),
        "body_ru": (
            "Дозорные — обычные стрелки, которым дали основы разведки и ставят в стороне от основной "
            "линии. Лёгкое снаряжение помогает им занять боковую позицию, после чего они держатся за "
            "укрытие и ловят движущиеся цели винтовочным огнём. Перед наступлением проверяйте оба фланга. "
            "Подходите под прикрытием дыма или заходите с другой стороны."
        ),
    },
    # --- Flanker T2 ---
    "JAZZ_Legion_FlankerT2_Scout": {
        "title_en": "Scout",
        "title_ru": "Скаут",
        "body_en": (
            "Scouts are survivors of Warden patrols who have learned to move quietly and choose their "
            "approach. They slip around the line with automatic weapons, and may use a knife or smoke "
            "once they reach the rear. Keep the flanks paired, watch covered routes, and do not chase a "
            "Scout into ground you have not cleared."
        ),
        "body_ru": (
            "Скауты — это выжившие Дозорные, которые научились двигаться тихо и выбирать путь для захода. "
            "Они обходят линию с автоматическим оружием, а в тылу могут пустить в ход нож или дым. "
            "Прикрывайте фланги парами, следите за скрытыми подходами и не гонитесь за Скаутом туда, где "
            "ещё не провели разведку."
        ),
    },
    "JAZZ_Legion_FlankerT2_Skirmisher": {
        "title_en": "Skirmisher",
        "title_ru": "Застрельщик",
        "body_en": (
            "Skirmishers are picked for marksmanship and trained to fight away from the main line. They "
            "carry light armor and battle rifles, shifting between flanking positions to fire on exposed "
            "targets. Do not follow them across open ground; move under cover or smoke and pin their "
            "position before advancing."
        ),
        "body_ru": (
            "В Застрельщики отбирают метких бойцов и учат их работать в стороне от главной линии. Они "
            "носят лёгкую броню и переходят между боковыми позициями с боевыми винтовками, выискивая "
            "открытые цели. Не преследуйте их по открытому месту — двигайтесь под прикрытием или дымовой "
            "завесой и сначала прижмите их огнём."
        ),
    },
    # --- Flanker T3 ---
    "JAZZ_Legion_FlankerT3_Pathfinder": {
        "title_en": "Pathfinder",
        "title_ru": "Следопыт",
        "body_en": (
            "Pathfinders are seasoned scouts trained to choose a concealed firing lane and hold it. Their "
            "light gear lets them reach a flank with a carbine or submachine gun, and many also carry "
            "smoke or a knife. Sweep nearby cover before moving the main group, then block their escape "
            "instead of trading shots from one position."
        ),
        "body_ru": (
            "Следопыты — опытные разведчики, которых учат выбирать скрытую линию огня и удерживать её. "
            "Лёгкое снаряжение помогает им выйти во фланг с карабином или пистолетом-пулемётом; многие "
            "также берут дым или нож. Перед движением основной группы проверьте ближайшие укрытия, а "
            "обнаружив Следопыта, перекройте ему отход."
        ),
    },
    "JAZZ_Legion_FlankerT3_Recon": {
        "title_en": "Recon",
        "title_ru": "Разведчик",
        "body_en": (
            "Recon troops are veteran scouts trained for quiet approaches and night fighting. They use "
            "light gear and compact automatic weapons to close from an unseen angle, sometimes covering "
            "the move with smoke. Keep overlapping fields of fire, illuminate dark approaches, and finish "
            "them as soon as they reveal themselves."
        ),
        "body_ru": (
            "Разведчики — опытные бойцы, которых учат скрытно подходить к цели и действовать ночью. "
            "Лёгкое снаряжение и компактное автоматическое оружие позволяют им сближаться с неожиданной "
            "стороны, иногда под прикрытием дыма. Прикрывайте друг друга перекрёстным огнём, освещайте "
            "тёмные подходы и добивайте Разведчика, как только он себя выдаст."
        ),
    },
    # --- Flanker T4 ---
    "JAZZ_Legion_FlankerT4_Ranger": {
        "title_en": "Ranger",
        "title_ru": "Рейнджер",
        "body_en": (
            "Rangers are elite scouts selected from the Legion's best flankers and given its finest field "
            "training. They move quickly and quietly with upgraded carbines or submachine guns, striking "
            "from the side before slipping away. Treat a Ranger as a priority target, overlap your fields "
            "of fire, and never leave one merc isolated."
        ),
        "body_ru": (
            "Рейнджеров отбирают из лучших фланкеров Легиона и готовят как элитных полевых разведчиков. "
            "Они быстро и тихо двигаются с улучшенными карабинами или пистолетами-пулемётами, бьют сбоку "
            "и снова уходят из-под огня. Считайте Рейнджера приоритетной целью, прикрывайте друг друга "
            "перекрёстным огнём и не оставляйте наёмника в одиночку."
        ),
    },
    # --- Front T1 ---
    "JAZZ_Legion_FrontT1_Bonemaker": {
        "title_en": "Bonemaker",
        "title_ru": "Костоправ",
        "body_en": (
            "A recruit who breaks from the line to reach a wounded Legionnaire is probably a Bonemaker. "
            "The Major chooses people who stay calm around blood, gives them a compact firearm, and "
            "hurries them through battlefield medicine. They break off to stop bleeding or treat other "
            "wounds. Remove the medic before pressing forward, or fighters you have already hurt will "
            "stay in the battle far longer than expected."
        ),
        "body_ru": (
            "Если рекрут покидает строй, чтобы помочь раненому легионеру, перед вами, скорее всего, "
            "Костоправ. Майор выбирает для этой роли тех, кто не теряется при виде крови, выдаёт им "
            "компактное огнестрельное оружие и наскоро обучает полевой медицине. Они выходят из боя, "
            "чтобы остановить кровотечение или обработать другие раны. Уберите медика до начала штурма, "
            "иначе уже задетые бойцы останутся в строю гораздо дольше, чем вы рассчитывали."
        ),
    },
    "JAZZ_Legion_FrontT1_Marauder": {
        "title_en": "Marauder",
        "title_ru": "Мародёр",
        "body_en": (
            "Looters and local toughs fill the Marauder ranks. They start with pistols and submachine "
            "guns; assault rifles appear once better supplies reach the Legion. They plug gaps in the "
            "line and rake exposed ground with fire, but pressure can pin them down before they "
            "accomplish much. Their short-range weapons punish careless movement, so return fire quickly, "
            "keep your distance, and force them to keep their heads down."
        ),
        "body_ru": (
            "Мародёров набирают из грабителей и местных громил. Сначала им выдают пистолеты и "
            "пистолеты-пулемёты; штурмовые винтовки появляются, когда снабжение Легиона налаживается. Они "
            "закрывают бреши в передовой и держат открытые участки под огнём, но плотный ответ быстро "
            "прижимает их к земле. Их оружие опаснее всего вблизи, поэтому отвечайте сразу, держите "
            "дистанцию и не давайте им поднять голову."
        ),
    },
    "JAZZ_Legion_FrontT1_Rifleman": {
        "title_en": "Rifleman",
        "title_ru": "Стрелок",
        "body_en": (
            "Most Riflemen are conscripts with a few marksmanship lessons, posted to guard roads, "
            "doorways, and village approaches. From cover, they use their rifles to watch the ground "
            "ahead and wait for a clear shot. A patient Rifleman can punish careless movement, so block "
            "his view with smoke or approach from a direction his firing position does not cover."
        ),
        "body_ru": (
            "Большинство Стрелков — призывники с несколькими уроками меткой стрельбы за плечами; их "
            "ставят охранять дороги, двери и подступы к деревням. Из укрытия они следят за подступами и "
            "ждут удобного выстрела. Терпеливый Стрелок накажет за неосторожное движение, поэтому "
            "закройте ему обзор дымом или подойдите со стороны, которую не перекрывает его позиция."
        ),
    },
    # --- Front T2 ---
    "JAZZ_Legion_FrontT2_Ambusher": {
        "title_en": "Ambusher",
        "title_ru": "Засадник",
        "body_en": (
            "Ambushers are patient shooters taught to prepare concealed firing positions along likely "
            "approaches. From a prepared position, they wait for an exposed target and punish the first "
            "careless move with accurate rifle fire. Do not walk into ground they have chosen; scout "
            "ahead, use smoke, and force them to reveal themselves early."
        ),
        "body_ru": (
            "Засадники — терпеливые стрелки, обученные заранее готовить скрытые позиции на вероятных "
            "путях противника. С подготовленной позиции они ждут открытой цели и отвечают точным "
            "винтовочным огнём на первое неосторожное движение. Не входите вслепую туда, что выбрали они: "
            "разведайте подход, поставьте дым и вынудите Засадников раскрыться раньше срока."
        ),
    },
    "JAZZ_Legion_FrontT2_Marksman": {
        "title_en": "Marksman",
        "title_ru": "Охотник",
        "body_en": (
            "The best shots in regular squads are given accurate rifles and taught to wait for a clean "
            "shot. They work behind the front, hold useful ground, and let the enemy come to them rather "
            "than rushing forward. Their accuracy makes repeated peeking dangerous, so change firing "
            "points often and deny them a clear view with smoke."
        ),
        "body_ru": (
            "Лучшим стрелкам обычных отделений выдают точные винтовки и приучают ждать удобного выстрела. "
            "Они держатся позади передовой, занимают выгодные позиции и позволяют противнику самому выйти "
            "под выстрел. Их меткость превращает повторный выход из укрытия в смертельную ошибку, поэтому "
            "чаще меняйте огневые точки и закрывайте обзор дымом."
        ),
    },
    "JAZZ_Legion_FrontT2_Raider": {
        "title_en": "Raider",
        "title_ru": "Налётчик",
        "body_en": (
            "Raiders are adaptable front-line fighters drilled with automatic weapons; every one also "
            "receives hand grenades. They move with the line, use rapid fire to cover short advances, and "
            "throw grenades when defenders settle behind cover. Rapid fire and grenades make them "
            "dangerous at close and middle range, so spread out, deny them an easy approach, and press "
            "them before they can choose where to throw."
        ),
        "body_ru": (
            "Налётчики — подвижные бойцы передовой, обученные обращаться с автоматическим оружием; "
            "каждому также выдают ручные гранаты. Они движутся вместе с передовой, прикрывают короткие "
            "рывки быстрым огнём и бросают гранаты, когда защитники прочно засели в укрытии. Быстрый "
            "огонь и гранаты делают их опасными на ближней и средней дистанции, поэтому рассредоточьтесь, "
            "перекройте подход и надавите до первого броска."
        ),
    },
    # --- Front T3 ---
    "JAZZ_Legion_FrontT3_Sniper": {
        "title_en": "Sniper",
        "title_ru": "Снайпер",
        "body_en": (
            "Only the Legion's finest riflemen receive sniper training: patience, target selection, and "
            "careful use of scoped rifles. They watch open approaches from distance and begin an "
            "engagement by pinning one exposed target under accurate fire. Crossing open ground gives "
            "them an easy shot, so screen movement with smoke and hunt the Sniper before beginning a "
            "direct assault."
        ),
        "body_ru": (
            "Снайперскую подготовку получают только лучшие стрелки Легиона: их учат терпеливо выбирать "
            "цель и правильно обращаться с винтовками с оптикой. Они наблюдают за открытыми подступами "
            "издалека и начинают бой, прижимая точным огнём одну неосторожно открывшуюся цель. На "
            "открытом месте вы сами подставляетесь под удобный выстрел, поэтому прикрывайте движение "
            "дымом и найдите Снайпера до начала прямого штурма."
        ),
    },
    "JAZZ_Legion_FrontT3_Veteran": {
        "title_en": "Veteran",
        "title_ru": "Ветеран",
        "body_en": (
            "Veterans have survived several campaigns and stayed steady under fire. They advance "
            "stubbornly with automatic fire and grenades; a few also bring a launcher, and all keep "
            "fighting through punishment that would stop less experienced troops. Their durability and "
            "explosives punish a packed formation, so spread out, deny them a clean approach, and "
            "concentrate fire before closing in."
        ),
        "body_ru": (
            "Ветераны пережили несколько кампаний и не растерялись под огнём. Они упрямо наступают с "
            "автоматическим оружием и гранатами; некоторые также несут гранатомёт, и все выдерживают "
            "давление, которое остановило бы менее опытных бойцов. Их стойкость и взрывчатка опасны для "
            "плотного строя, поэтому рассредоточьтесь, не давайте им удобно сблизиться и сосредоточьте "
            "огонь до решающего рывка."
        ),
    },
    # --- Front T4 ---
    "JAZZ_Legion_FrontT4_Mercenary": {
        "title_en": "Mercenary",
        "title_ru": "Наёмник",
        "body_en": (
            "The Legion hires experienced Mercenaries to hold important positions and sends them out with "
            "good weapons. They move with the front and combine accurate rifle fire with grenades; a few "
            "also carry a launcher, and all keep fighting under pressure. They are dangerous at several "
            "ranges, so avoid a fair exchange: split their attention, deny clear shots, and overwhelm one "
            "position at a time."
        ),
        "body_ru": (
            "На важные позиции Легион нанимает опытных Наёмников и выдаёт им неизменно хорошее оружие. "
            "Они движутся вместе с передовой и сочетают точный винтовочный огонь с гранатами; некоторые "
            "также несут гранатомёт, и все продолжают эффективно сражаться под давлением. Они опасны на "
            "разных дистанциях, поэтому не давайте им честного боя: рассеивайте внимание, закрывайте "
            "обзор и подавляйте по одной позиции."
        ),
    },
    "JAZZ_Legion_FrontT4_MercenarySniper": {
        "title_en": "Mercenary Sniper",
        "title_ru": "Наёмник-снайпер",
        "body_en": (
            "Mercenary Snipers are proven specialists hired for operations where accurate long-range fire "
            "can decide the opening exchange. They begin by pinning an exposed target and use powerful "
            "scoped rifles to control open approaches from a distance. Once one is reported, do not "
            "expose yourself twice from the same place. Cover movement with smoke and pressure the "
            "shooter before committing the squad."
        ),
        "body_ru": (
            "Наёмники-снайперы — готовые специалисты, которых нанимают для операций, где точный дальний "
            "огонь может решить исход первой перестрелки. Они начинают бой, прижимая открывшуюся цель, и "
            "держат открытые подступы под огнём мощных винтовок с оптикой. Заметив такого стрелка, не "
            "показывайтесь дважды в одном месте, прикройте движение дымом и надавите на него до общего "
            "наступления."
        ),
    },
    # --- Gunner T1 ---
    "JAZZ_Legion_GunnerT1_Gunner": {
        "title_en": "Gunner",
        "title_ru": "Пуляло",
        "body_en": (
            "The Legion hands its strongest new recruits old machine guns and gives them a hurried lesson "
            "in using them. They set up across roads and courtyards and spray enough fire to pin anyone "
            "caught away from cover, but remain vulnerable while moving. Do not cross their sights in the "
            "open; use smoke, buildings, or a side approach to reach them safely."
        ),
        "body_ru": (
            "Самым крепким новобранцам Легион выдаёт старые пулемёты и наспех учит с ними обращаться. Они "
            "разворачиваются у дорог и дворов и прижимают к земле всех, кто не успел укрыться, но "
            "остаются уязвимыми на ходу. Не входите в их сектор огня через открытое место: используйте "
            "дым, здания или обходной путь."
        ),
    },
    # --- Gunner T2 ---
    "JAZZ_Legion_GunnerT2_AssaultGunner": {
        "title_en": "Assault Gunner",
        "title_ru": "Коммандо",
        "body_en": (
            "Surviving Gunners are promoted to Assault Gunner duty and taught to carry their light "
            "machine guns forward instead of guarding one position. They close the distance, set up near "
            "the fight, and pin defenders from positions that ordinary gunners would consider too "
            "exposed. Most also bring a machete for the last few steps and a firebomb to flush cover. "
            "If they reach useful firing ground the attack becomes hard to stop, so break their "
            "approach with explosives or catch them while they are moving."
        ),
        "body_ru": (
            "Выживших пулемётчиков переводят в Коммандо и учат продвигать лёгкий пулемёт вперёд вместо "
            "охраны одной позиции. Они сближаются, разворачивают оружие рядом с местом боя и прижимают "
            "защитников с позиций, которые обычный пулемётчик счёл бы слишком открытыми. Обычно у них "
            "есть мачете для последних шагов и зажигательная смесь, чтобы выкурить укрытие. Если они "
            "доберутся до удобного места, атаку будет трудно остановить, поэтому сорвите подход взрывом "
            "или ударьте, пока пулемёт ещё несут."
        ),
    },
    "JAZZ_Legion_GunnerT2_GMPG": {
        "title_en": "GPMG",
        "title_ru": "Пулемётчик",
        "body_en": (
            "Reliable machine gunners are assigned to GPMG duty and taught to keep their fire steady "
            "without wasting ammunition. They settle into prepared positions and use a general-purpose "
            "machine gun to cover roads, courtyards, and wide approaches. A frontal charge feeds their "
            "advantage; block their view with smoke, force them to move, or attack from a direction their "
            "position cannot cover."
        ),
        "body_ru": (
            "На роль Пулемётчика ставят надёжных бойцов и учат их долго вести огонь, не паля впустую. Они "
            "занимают подготовленные позиции и перекрывают единым пулемётом дороги, дворы и широкие "
            "подступы. Лобовой бросок играет им на руку; закройте обзор дымом, вынудите пулемётчика "
            "сняться с места или атакуйте с неприкрытой стороны."
        ),
    },
    # --- Gunner T3 ---
    "JAZZ_Legion_GunnerT3_VeteranGunner": {
        "title_en": "Veteran Gunner",
        "title_ru": "Подавитель",
        "body_en": (
            "Veteran Gunners have survived repeated engagements and are trusted with stronger machine "
            "guns. They use disciplined bursts and expert prepared fire to lock down movement, while "
            "tougher defenses let them stay effective under pressure. Their fire can stall an attack, so "
            "keep them occupied from one direction and strike quickly from another, or destroy the "
            "position with explosives."
        ),
        "body_ru": (
            "Подавители — опытные пулемётчики, пережившие не один бой; им доверяют более мощное оружие. С "
            "подготовленных позиций они перекрывают движение точными очередями, а тяжёлая броня помогает "
            "дольше выдерживать ответный огонь. Подавитель способен остановить наступление, поэтому "
            "отвлеките его с одной стороны и быстро ударьте с другой либо накройте позицию взрывчаткой."
        ),
    },
    # --- Gunner T4 ---
    "JAZZ_Legion_GunnerT4_MercGunner": {
        "title_en": "Merc Gunner",
        "title_ru": "Наёмник-пулемётчик",
        "body_en": (
            "Merc Gunners are experienced heavy-weapon specialists hired to use the strongest machine "
            "guns available to the Legion. They combine disciplined bursts, prepared fire, and enough "
            "resilience to keep a broad approach dangerous under sustained pressure. Leaving them alone "
            "can halt an advance, so deny them a clear field of fire and destroy the gunner before "
            "committing anyone across open ground."
        ),
        "body_ru": (
            "Наёмники-пулемётчики — опытные специалисты по тяжёлому оружию, которым выдают лучшие "
            "пулемёты Легиона. С подготовленной позиции они держат под огнём широкий участок и продолжают "
            "стрелять даже под плотным ответным огнём. Если оставить их в покое, они остановят любое "
            "продвижение, поэтому закройте им обзор и уничтожьте пулемётчика до выхода отряда на открытое "
            "место."
        ),
    },
    # --- Heavy T1 ---
    "JAZZ_Legion_HeavyT1_Rocketeer": {
        "title_en": "Rocketeer",
        "title_ru": "Ракетчик",
        "body_en": (
            "Rocketeers are recruits with enough nerve to shoulder a launcher and just enough instruction "
            "to avoid hitting their own squad. They fire RPGs or disposable rockets at vehicles, walls, "
            "and clustered targets, but the launcher usually leaves them with only one attack before they "
            "must recover or reload. Spread out and press them immediately after a launch; one unanswered "
            "rocket can turn a defensible position into wreckage."
        ),
        "body_ru": (
            "Ракетчики — новобранцы, которым хватает смелости взвалить установку на плечо и подготовки, "
            "чтобы не накрыть своих. Они стреляют из РПГ или одноразовых установок по машинам, стенам и "
            "плотным группам, но после пуска обычно не могут сразу атаковать снова. Рассредоточьтесь и "
            "надавите сразу после выстрела: одна оставленная без ответа ракета превратит надёжную позицию "
            "в груду обломков."
        ),
    },
    # --- Heavy T2 ---
    "JAZZ_Legion_HeavyT2_Grenadier": {
        "title_en": "Heavy Grenadier",
        "title_ru": "Гранатомётчик",
        "body_en": (
            "Heavy Grenadiers already understand explosives before they are trained on RPGs and grenade "
            "launchers. They send explosive rounds into rooms, courtyards, and covered approaches, "
            "forcing anyone who survives the blast to abandon a comfortable position. Remaining in one "
            "place invites another round, so move after each shot and pressure the Heavy Grenadier before "
            "the launcher is ready again."
        ),
        "body_ru": (
            "Гранатомётчики уже знакомы со взрывчаткой, прежде чем их начинают учить стрельбе из РПГ и "
            "гранатомётов. Они посылают взрывные выстрелы в помещения, дворы и прикрытые подступы, "
            "вынуждая переживших разрыв покинуть удобную позицию. Тот, кто останется на месте, дождётся "
            "следующего выстрела, поэтому двигайтесь после каждого разрыва и надавите на Гранатомётчика "
            "до перезарядки."
        ),
    },
    # --- Heavy T3 ---
    "JAZZ_Legion_HeavyT3_Mortarman": {
        "title_en": "Mortarman",
        "title_ru": "Миномётчик",
        "body_en": (
            "Mortarmen are proven heavy-weapon crews trained to lob shells over walls and other "
            "obstacles. They use a portable mortar to strike positions that direct fire cannot easily "
            "reach, forcing anyone who remains still to abandon cover. Once the bombardment begins, move "
            "immediately and pressure the crew before it fires again. A wall between you and the crew "
            "will not keep you safe."
        ),
        "body_ru": (
            "Миномётчики — проверенные бойцы тяжёлого оружия, обученные забрасывать мины за стены и "
            "другие препятствия. Они используют переносной миномёт против позиций, до которых трудно "
            "добраться прямым огнём, вынуждая засевших бойцов покинуть укрытие. Как только начался "
            "обстрел, немедленно двигайтесь и надавите на расчёт до следующего выстрела. Стена между вами "
            "и расчётом от мины не спасёт."
        ),
    },
    # --- Leader T1 ---
    "JAZZ_Legion_LeaderT1_Sergeant": {
        "title_en": "Sergeant",
        "title_ru": "Бригадир",
        "body_en": (
            "When frightened recruits suddenly start moving as one, look for the loudest man among them. "
            "The Major turns dependable Legionnaires like that into Sergeants, able to push nearby troops "
            "forward, hold them in place, or focus their fire. Remove the leader early and the rest "
            "become much easier to disrupt."
        ),
        "body_ru": (
            "Если испуганные рекруты вдруг начинают действовать как один, ищите самого громкого среди "
            "них. Из таких надёжных легионеров Майор делает Бригадиров: они гонят ближайших бойцов "
            "вперёд, удерживают их на месте или сосредоточивают огонь. Уберите лидера в начале боя, и "
            "остальных станет гораздо легче рассеять."
        ),
    },
    # --- Leader T2 ---
    "JAZZ_Legion_LeaderT2_Lieutenant": {
        "title_en": "Lieutenant",
        "title_ru": "Командир",
        "body_en": (
            "Successful Sergeants become Lieutenants and trade shouting at one group for directing "
            "several squads. Their orders reach a wider area, sending troops forward, holding them in "
            "place, moving them into cover, or focusing their fire as the situation changes. Their "
            "presence keeps a local attack coherent, so remove the officer before the Legion can regroup "
            "and turn a confused exchange into an organized assault."
        ),
        "body_ru": (
            "Успешные Бригадиры становятся Командирами и вместо одной группы руководят несколькими "
            "отделениями. Их приказы слышны на большей территории: наступать, удерживать позиции, искать "
            "укрытие или сосредоточивать огонь. Пока Командир жив, местная атака сохраняет общий замысел, "
            "поэтому устраните офицера до перегруппировки Легиона."
        ),
    },
    # --- Leader T3 ---
    "JAZZ_Legion_LeaderT3_Captain": {
        "title_en": "Captain",
        "title_ru": "Советник",
        "body_en": (
            "Captains are officers trusted to control several units at once. They issue orders across the "
            "entire Legion force, redirect the attack as conditions change, and support those commands "
            "with accurate rifle fire. Every minute a Captain remains active keeps the enemy coordinated, "
            "so identify the officer quickly and bring him down before pressing the fight."
        ),
        "body_ru": (
            "Советники — офицеры, которым доверяют сразу несколько подразделений. Они отдают приказы "
            "всему отряду Легиона, меняют направление атаки по обстановке и поддерживают свои команды "
            "точным винтовочным огнём. Пока Советник жив, противник действует слаженно, поэтому быстро "
            "найдите офицера и устраните его до решающего натиска."
        ),
    },
    # --- Leader T4 ---
    "JAZZ_Legion_LeaderT4_MercenaryCaptain": {
        "title_en": "Mercenary Captain",
        "title_ru": "Мастер",
        "body_en": (
            "Mercenary Captains are experienced officers hired to command mixed troops; they need little "
            "more than local intelligence. They issue orders across the entire force, preserve discipline "
            "through casualties, and quickly change plans when the first one fails. Assume nearby units "
            "are acting with a common purpose while one survives; bring the Captain down before attacking "
            "the rest."
        ),
        "body_ru": (
            "Мастера — опытные наёмные офицеры, умеющие командовать смешанными силами; им нужны лишь "
            "свежие сведения о местной обстановке. Они отдают приказы всему отряду, сохраняют дисциплину "
            "после потерь и быстро меняют план, если первый не сработал. Пока Мастер жив, считайте, что "
            "окружающие бойцы действуют сообща; устраните его до атаки на остальных."
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
            "Luc Laurent's son serves as the Legion's face on Ernie, always in a pressed uniform and with "
            "something to prove. He likes being seen as much as being obeyed, which makes him easier to "
            "read than most Legion officers. Don't mistake charm for mercy."
        ),
        "body_ru": (
            "Сын Люка Лорана представляет Легион на Эрни — всегда в выглаженной форме и с желанием что-то "
            "доказать. Ему важно не только подчинение, но и внимание, поэтому его легче читать, чем "
            "других офицеров Легиона. Только не принимайте обаяние за доброту."
        ),
    },
    "Bastien": {
        "title_en": "Bastien",
        "title_ru": "Бастьен",
        "body_en": (
            "A local fixer with a trader's smile. He knows who controls each road, what passage costs, "
            "and whom to pay. A useful contact, but never mistake business for friendship."
        ),
        "body_ru": (
            "Местный делец с улыбкой торговца. Он знает, кто держит каждую дорогу, сколько стоит проезд и "
            "кому платить. Полезный контакт, но не путайте дела с дружбой."
        ),
    },
    "TheMajor": {
        "title_en": "The Major",
        "title_ru": "Майор",
        "body_en": (
            "The man behind the Legion built his army with fear, money, and stolen supplies, then spread "
            "it across Grand Chien. Every Legion supply report ultimately leads back to him. He is "
            "patient, ruthless, and remembers every loss."
        ),
        "body_ru": (
            "За Легионом стоит Майор. Он собрал армию страхом, деньгами и крадеными припасами, а затем "
            "раскинул её по всему Гранд-Шьену. Любая сводка о снабжении Легиона в итоге ведёт к нему. Он "
            "терпелив, безжалостен и помнит каждую потерю."
        ),
    },
    "Legion": {
        "title_en": "Legion (faction)",
        "title_ru": "Легион (фракция)",
        "body_en": (
            "The Major's army survives on stolen supplies, forced recruitment, and officers who treat "
            "villages as property. Its troops range from frightened locals to trained specialists. "
            "Wherever the Legion appears, the Major's reach is close behind."
        ),
        "body_ru": (
            "Армия Майора живёт за счёт краденых припасов, насильственного набора и офицеров, которые "
            "считают деревни своей собственностью. В её рядах есть и запуганные местные, и обученные "
            "специалисты. Где появляется Легион, там недалеко и власть Майора."
        ),
    },
}

# ---------------------------------------------------------------------------
# Loc string fixes: (id_str, en, ru)
# ---------------------------------------------------------------------------

WELCOME_FIXES: list[tuple[str, str, str]] = [
    (
        "890000000006922",
        "R.I.S. — free field intelligence for your team",
        "R.I.S. — бесплатная полевая разведка для вашего отряда",
    ),
    (
        "890000000006923",
        (
            "Commander,\n\nR.I.S. has opened a free field-intelligence channel for your team for the "
            "duration of this campaign. When Legion weapons or equipment change, we will send an "
            "assessment to your inbox. As we confirm more information, dossiers and after-action reports "
            "will appear on the R.I.S. site in your PDA.\n\nRead this message to open the R.I.S. tab.\n\n— "
            "Recon Intelligence Services"
        ),
        (
            "Командир,\n\nR.I.S. открыла для вашего отряда бесплатный канал полевой разведки на время этой "
            "кампании. Если Легион сменит оружие или снаряжение, оценка придёт вам на почту. По мере "
            "подтверждения данных на сайте R.I.S. в КПК будут появляться досье и сводки после "
            "боёв.\n\nПрочитайте это письмо, чтобы открыть вкладку R.I.S.\n\n— Разведывательно-информационная "
            "служба R.I.S."
        ),
    ),
    (
        "890000000006924",
        (
            "Recon Intelligence Services\n\nYour free campaign subscription is active. Confirmed dossiers "
            "and after-action reports will appear here.\n\nLegion supply assessments are delivered to your "
            "inbox."
        ),
        (
            "Разведывательно-информационная служба R.I.S.\n\nБесплатная подписка на время кампании активна. "
            "Здесь будут появляться подтверждённые досье и сводки после боёв.\n\nОценки снабжения Легиона "
            "приходят на почту."
        ),
    ),
]

UI_FIXES: list[tuple[str, str, str]] = [
    (
        "890000000011000",
        "Recon Intelligence Services",
        "Разведывательно-информационная служба R.I.S.",
    ),
    (
        "890000000011001",
        "Field bulletin",
        "Оперативная сводка",
    ),
    (
        "890000000011002",
        "Dossiers",
        "Досье",
    ),
    (
        "890000000011003",
        "After-action reports",
        "Сводки после боёв",
    ),
    (
        "890000000011004",
        "No supply assessment yet. Once R.I.S. sends one, it will appear here.",
        "Оценок снабжения пока нет. Когда R.I.S. пришлёт новую, она появится здесь.",
    ),
    (
        "890000000011005",
        "No Legion units identified yet. We will add them as contact reports come in.",
        "Мы пока не опознали ни одного бойца Легиона. Данные появятся после первых контактов.",
    ),
    (
        "890000000011006",
        "No after-action reports yet. Finish a battle and R.I.S. will add a summary here.",
        "Сводок после боёв пока нет. Завершите бой, и R.I.S. добавит сюда итог.",
    ),
    (
        "890000000011007",
        "Confirmed kills: <count>/3",
        "Подтверждённые потери противника: <count>/3",
    ),
    (
        "890000000011008",
        "(classified — requires 3 confirmed kills)",
        "(засекречено — нужно подтвердить 3 устранения)",
    ),
    (
        "890000000011009",
        "Key figures",
        "Ключевые фигуры",
    ),
    (
        "890000000011010",
        "Legion units",
        "Бойцы Легиона",
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
        "Место хуже некуда, момент — ещё хуже",
    ),
    (
        "890000000011118",
        "Forced to pull back",
        "Пришлось отступить",
    ),
    (
        "890000000011122",
        "Broke through the gauntlet",
        "Вырвались из-под огня",
    ),
    # Weather / intensity labels that sound like spreadsheet headers
    (
        "890000000011124",
        "The fighting unfolded under clear skies.",
        "Бой прошёл под ясным небом.",
    ),
    (
        "890000000011125",
        "Rain soaked the ground and frayed everyone's nerves.",
        "Дождь размыл землю и вымотал всем нервы.",
    ),
    (
        "890000000011126",
        "At night, muzzle flashes gave away every shot.",
        "Ночью каждый выстрел выдавали вспышки.",
    ),
    (
        "890000000011127",
        "Fog cut visibility and kept everyone close to cover.",
        "Из-за тумана видимость упала, и все держались ближе к укрытиям.",
    ),
    (
        "890000000011128",
        "In the heat, exhaustion hit almost as hard as the bullets.",
        "Жара выматывала почти не меньше пуль.",
    ),
    (
        "890000000011129",
        "The dust storm worked grit into every weapon.",
        "Пылевая буря забила песком всё оружие.",
    ),
    (
        "890000000011130",
        "The weather stayed out of it; the shooting did not.",
        "Погода не вмешивалась — хватило стрельбы.",
    ),
    (
        "890000000011131",
        "The exchange was brief. It drew little attention beyond the sector.",
        "Перестрелка быстро закончилась и почти не привлекла внимания.",
    ),
    (
        "890000000011132",
        "The firefight dragged on as both sides moved under fire. Word of it will spread.",
        "Бой затянулся: обе стороны маневрировали под огнём. Слухи о нём разойдутся.",
    ),
    (
        "890000000011133",
        "The fight became a slaughter. The Major's people will hear about it.",
        "Бой превратился в бойню. Люди Майора об этом услышат.",
    ),
    (
        "890000000011134",
        "At first contact, we counted about <player> friendlies and <enemy> hostiles.",
        "На момент первого контакта мы насчитали около <player> своих и <enemy> противников.",
    ),
    (
        "890000000011135",
        "The fighting took place in <sector>.",
        "Бой произошёл в секторе <sector>.",
    ),
    (
        "890000000011136",
        "The fighting took place in <sector>, near <poi>.",
        "Бой произошёл в секторе <sector>, в районе <poi>.",
    ),
    # Quest / character lines (calques)
    (
        "890000000011137",
        "This fight was tied to <quest>. One detail may matter: <note>",
        "Бой был связан с заданием <quest>. Важная подробность: <note>",
    ),
    (
        "890000000011138",
        "The evidence ties this fight to <quest>.",
        "Судя по данным, этот бой связан с заданием <quest>.",
    ),
    (
        "890000000011139",
        "Several active jobs led your team here: <quests>. This was no random skirmish.",
        "Сразу несколько текущих заданий привели ваш отряд сюда: <quests>. Случайной эту стычку не "
        "назовёшь.",
    ),
    (
        "890000000011140",
        "The team was also working on <quest>, though that job was not tied to this sector.",
        "Отряд также выполнял задание <quest>, хотя оно не было связано с этим сектором.",
    ),
    (
        "890000000011141",
        "No active assignment led to this area. This was a fight for the sector itself.",
        "Ни одно активное задание не вело в этот район. Это был бой за сам сектор.",
    ),
    (
        "890000000011142",
        "Your team held the field.",
        "Поле боя осталось за вашим отрядом.",
    ),
    (
        "890000000011143",
        "The enemy kept control of the sector.",
        "Противник сохранил контроль над сектором.",
    ),
    (
        "890000000011144",
        "Your team withdrew under fire instead of making a last stand.",
        "Ваш отряд отошёл под огнём, не ввязываясь в бой до последнего.",
    ),
    (
        "890000000011145",
        "It looked like an ambush; the opening shots decided the fight.",
        "Похоже, это была засада: первые выстрелы решили исход боя.",
    ),
    (
        "890000000011146",
        "The fight was tied to an active job. The objective held, and the sector remained yours.",
        "Бой был связан с активным заданием. Цель удалось удержать, и сектор остался за вами.",
    ),
    (
        "890000000011147",
        "The fight was tied to an active job, and losing the sector will make that job harder.",
        "Бой был связан с активным заданием, и потеря сектора теперь усложнит это задание.",
    ),
    (
        "890000000011148",
        "Your team withdrew from a sector tied to an active job.",
        "Ваш отряд отступил из сектора, связанного с активным заданием.",
    ),
    (
        "890000000011149",
        "Our side suffered <pkia> killed and <pwia> wounded; enemy losses were <ekia> killed and "
        "<ewia> wounded.",
        "У нас <pkia> погибших и <pwia> раненых; у противника — <ekia> убитых и <ewia> раненых.",
    ),
    (
        "890000000011154",
        "The sector is quiet again, and the fight should draw little attention.",
        "Сектор снова затих, и этот бой вряд ли привлечёт много внимания.",
    ),
    (
        "890000000011155",
        "Word of this fight will spread. Expect more patrols and more money changing hands.",
        "Слухи об этом бое разойдутся. Ждите новых патрулей и новых сделок.",
    ),
    (
        "890000000011156",
        "Mark this one in red. The Major's command will want answers.",
        "Эту сводку отметьте красным. Командование Майора потребует объяснений.",
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
