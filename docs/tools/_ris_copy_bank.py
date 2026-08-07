"""Canonical importable RU+EN copy bank for R.I.S.

Runtime apply tools consume these values; this module itself never writes files.
The legacy ``_ris_dossier_copy`` module is only a compatibility facade.
"""

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
            "automatic weapon; some also carry smoke grenades or flashbangs. Do not bunch behind one "
            "wall—pin them in the open before a grenade clears their route."
        ),
        "body_ru": (
            "Штурмовики — это бойцы ранних штурмовых отрядов, которых переучили не останавливать атаку "
            "под ответным огнём. Они начинают штурм с нескольких гранат, а затем сближаются с "
            "автоматическим оружием; у некоторых есть дымовые или светошумовые гранаты. Не собирайтесь за "
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
            "Костоправ. Майор выбирает тех, кто не теряется при виде крови, выдаёт им "
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
            "careless move with accurate rifle fire. Do not advance blindly into ground they have chosen; scout "
            "ahead, use smoke, and force them to reveal themselves early."
        ),
        "body_ru": (
            "Засадники — терпеливые стрелки, обученные заранее готовить скрытые позиции на вероятных "
            "путях противника. С подготовленной позиции они ждут открытой цели и отвечают точным "
            "винтовочным огнём на первое неосторожное движение. Не продвигайтесь вслепую по выбранной ими местности: "
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
            "in using them. They set up along roads and in courtyards and spray enough fire to pin anyone "
            "caught away from cover, but remain vulnerable while moving. Do not cross their field of fire in the "
            "open; use smoke, buildings, or a side approach to reach them safely."
        ),
        "body_ru": (
            "Самым крепким новобранцам Легион выдаёт старые пулемёты и наспех учит с ними обращаться. Они "
            "разворачиваются на дорогах и во дворах и прижимают к земле всех, кто не успел укрыться, но "
            "остаются уязвимыми на ходу. Не пересекайте их сектор огня по открытому месту: используйте "
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
            "without wasting ammunition. From prepared positions, they use machine-gun fire to cover "
            "roads, courtyards, and wide approaches. A frontal charge feeds their "
            "advantage; block their view with smoke, force them to move, or attack from a direction their "
            "position cannot cover."
        ),
        "body_ru": (
            "Пулемётчиками становятся надёжные бойцы, которых учат долго вести огонь, не паля впустую. С "
            "подготовленных позиций они перекрывают пулемётным огнём дороги, дворы и широкие "
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
            "and clustered targets, but after a launch they need time before they can fire again. Spread "
            "out and press them immediately after a launch; one unanswered "
            "rocket can turn a defensible position into wreckage."
        ),
        "body_ru": (
            "Ракетчики — новобранцы, которым хватает смелости взвалить установку на плечо и подготовки, "
            "чтобы не накрыть своих. Они стреляют из РПГ или одноразовых установок по машинам, стенам и "
            "плотным группам, но после пуска им нужно время на подготовку следующего выстрела. Рассредоточьтесь и "
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
            "so identify and remove the officer before pressing the fight."
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
        "title_en": "Legion",
        "title_ru": "Легион",
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

# Existing generated localization layout.  The key order above is part of the
# bank contract and produces the same title/body pairs as System_RIS_Content.
DOSSIER_LOC_IDS: dict[str, dict[str, str]] = {
    key: {
        "title_id": str(890000000011013 + index * 2),
        "body_id": str(890000000011014 + index * 2),
    }
    for index, key in enumerate(DOSSIERS)
}

QUEST_DOSSIER_LOC_IDS: dict[str, dict[str, str]] = {
    key: {
        "title_id": str(890000000011089 + index * 2),
        "body_id": str(890000000011090 + index * 2),
    }
    for index, key in enumerate(QUEST_DOSSIERS)
}

# ---------------------------------------------------------------------------
# Existing localized strings: (id_str, en, ru)
# ---------------------------------------------------------------------------

WELCOME_FIXES: list[tuple[str, str, str]] = [
    (
        "890000000006922",
        "R.I.S. field-intelligence channel",
        "Канал полевой разведки R.I.S.",
    ),
    (
        "890000000006923",
        (
            "Commander,\n\nR.I.S. has opened a field-intelligence channel for your team for the duration "
            "of this campaign. We will send an assessment whenever confirmed reports show a change in "
            "Legion weapons or equipment. As evidence accumulates, the field desk will add dossiers and "
            "after-action summaries to its bulletin.\n\n— R.I.S. Field Desk"
        ),
        (
            "Командир,\n\nR.I.S. открыла для вашего отряда канал полевой разведки на время этой кампании. "
            "Когда подтверждённые донесения укажут на перемены в оружии или снаряжении Легиона, мы "
            "направим новую оценку. По мере накопления данных полевой отдел будет дополнять оперативную "
            "сводку досье и итогами боёв.\n\n— Полевой отдел R.I.S."
        ),
    ),
    (
        "890000000006924",
        (
            "Recon Intelligence Services\n\nThis field channel carries confirmed Legion supply "
            "assessments, unit dossiers, and after-action summaries. Reports are revised as evidence "
            "accumulates."
        ),
        (
            "Разведывательно-информационная служба R.I.S.\n\nПо этому полевому каналу поступают "
            "подтверждённые оценки снабжения Легиона, досье бойцов и итоги боёв. Сводки уточняются по "
            "мере накопления данных."
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
        "No supply assessment has reached the field desk yet.",
        "Полевой отдел пока не получал оценок снабжения.",
    ),
    (
        "890000000011005",
        "No Legion fighter type has been confirmed yet. The first contact reports will provide enough "
        "evidence for short profiles.",
        "Пока не подтверждён ни один тип бойцов Легиона. Первые полевые контакты дадут материал для "
        "кратких справок.",
    ),
    (
        "890000000011006",
        "No completed engagement has been recorded yet.",
        "Завершённых боестолкновений пока не зарегистрировано.",
    ),
    (
        "890000000011007",
        "Fighters of this type confirmed killed: <count>/3",
        "Подтверждено погибших бойцов этого типа: <count>/3",
    ),
    (
        "890000000011008",
        "Full assessment after 3 fighters of this type are confirmed killed",
        "Полная оценка — после подтверждения гибели 3 бойцов этого типа",
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

# All 60 existing AAR strings, in their generated localization-id order.
AAR_FIXES: list[tuple[str, str, str]] = [
    # win | low
    (
        "890000000011097",
        "Favorable outcome after a brief engagement",
        "Благоприятный исход после короткого боя",
    ),
    (
        "890000000011098",
        "Brief engagement ended in our favor",
        "Короткий бой завершён в нашу пользу",
    ),
    (
        "890000000011099",
        "Limited resistance overcome",
        "Слабое сопротивление преодолено",
    ),
    # win | mid
    (
        "890000000011100",
        "Favorable outcome after sustained fighting",
        "Благоприятный исход после упорного боя",
    ),
    (
        "890000000011101",
        "Sustained engagement ended in our favor",
        "Затяжной бой завершён в нашу пользу",
    ),
    (
        "890000000011102",
        "Resistance broken after a hard fight",
        "Сопротивление сломлено после тяжёлого боя",
    ),
    # win | high
    (
        "890000000011103",
        "Favorable outcome at heavy cost",
        "Благоприятный исход ценой тяжёлых потерь",
    ),
    (
        "890000000011104",
        "Severe fighting ended in our favor",
        "Тяжёлый бой завершён в нашу пользу",
    ),
    (
        "890000000011105",
        "Victory with heavy losses",
        "Победа при тяжёлых потерях",
    ),
    # loss | low
    (
        "890000000011106",
        "Adverse outcome after brief resistance",
        "Неблагоприятный исход после короткого сопротивления",
    ),
    (
        "890000000011107",
        "Brief engagement ended against us",
        "Короткий бой завершён не в нашу пользу",
    ),
    (
        "890000000011108",
        "Limited losses despite the adverse outcome",
        "Небольшие потери при неблагоприятном исходе",
    ),
    # loss | mid
    (
        "890000000011109",
        "Adverse outcome after sustained fighting",
        "Неблагоприятный исход после упорного боя",
    ),
    (
        "890000000011110",
        "Sustained engagement ended against us",
        "Затяжной бой завершён не в нашу пользу",
    ),
    (
        "890000000011111",
        "Enemy pressure decided the engagement",
        "Давление противника решило исход боя",
    ),
    # loss | high
    (
        "890000000011112",
        "Adverse outcome at heavy cost",
        "Неблагоприятный исход ценой тяжёлых потерь",
    ),
    (
        "890000000011113",
        "Severe fighting ended against us",
        "Тяжёлый бой завершён не в нашу пользу",
    ),
    (
        "890000000011114",
        "Heavy losses, hostile force prevailed",
        "Тяжёлые потери, противник одержал верх",
    ),
    # retreat | low
    (
        "890000000011115",
        "Orderly withdrawal after brief contact",
        "Организованный отход после короткого контакта",
    ),
    (
        "890000000011116",
        "Force withdrew after a brief engagement",
        "После короткого боя отряд отошёл",
    ),
    (
        "890000000011117",
        "Contact broken with limited losses",
        "Контакт прерван с небольшими потерями",
    ),
    # retreat | mid
    (
        "890000000011118",
        "Withdrawal under sustained pressure",
        "Отход под постоянным давлением",
    ),
    (
        "890000000011119",
        "Force disengaged after a hard fight",
        "Отряд вышел из тяжёлого боя",
    ),
    (
        "890000000011120",
        "Withdrawal ordered to preserve the force",
        "Отход предпринят для сохранения отряда",
    ),
    # retreat | high
    (
        "890000000011121",
        "Withdrawal under heavy fire",
        "Отход под плотным огнём",
    ),
    (
        "890000000011122",
        "Costly disengagement completed",
        "Выход из боя обошёлся дорого",
    ),
    (
        "890000000011123",
        "Withdrawal completed after severe fighting",
        "Отход завершён после тяжёлого боя",
    ),
    # Weather observations
    (
        "890000000011124",
        "Final field reports indicate clear weather and good visibility.",
        "По итоговым полевым донесениям, погода была ясной, видимость — хорошей.",
    ),
    (
        "890000000011125",
        "Final field reports indicate rain.",
        "В итоговых полевых донесениях отмечался дождь.",
    ),
    (
        "890000000011126",
        "Visibility was limited by darkness.",
        "Темнота ограничивала видимость.",
    ),
    (
        "890000000011127",
        "Final field reports note fog and reduced visibility.",
        "В итоговых полевых донесениях отмечены туман и ограниченная видимость.",
    ),
    (
        "890000000011128",
        "Final field reports note extreme heat.",
        "В итоговых полевых донесениях отмечена сильная жара.",
    ),
    (
        "890000000011129",
        "Final field reports note a dust storm and reduced visibility.",
        "В итоговых полевых донесениях отмечены пылевая буря и ограниченная видимость.",
    ),
    (
        "890000000011130",
        "Final field reports identify no notable weather condition.",
        "В итоговых полевых донесениях не отмечены заметные погодные условия.",
    ),
    # Intensity assessment
    (
        "890000000011131",
        "The exchange was brief and appears to have drawn little attention outside the area.",
        "Перестрелка была короткой и, судя по всему, почти не привлекла внимания за пределами района.",
    ),
    (
        "890000000011132",
        "Sustained fighting is likely to draw wider attention.",
        "Затяжной бой, вероятно, привлечёт более широкое внимание.",
    ),
    (
        "890000000011133",
        "The scale of the fighting will be difficult for hostile commanders to ignore.",
        "Командованию противника будет трудно оставить без внимания бой такого масштаба.",
    ),
    # Forces and location
    (
        "890000000011134",
        "Across the engagement, field reports placed friendly strength at about <player> and hostile "
        "strength at about <enemy>.",
        "За всё время боя, по полевым данным, своих насчитывалось около <player>, противников — около "
        "<enemy>.",
    ),
    (
        "890000000011135",
        "Engagement location: <sector>.",
        "Место боя: <sector>.",
    ),
    (
        "890000000011136",
        "Engagement location: <sector>. Nearest reported landmark: <poi>.",
        "Место боя: <sector>. Ближайший отмеченный ориентир: <poi>.",
    ),
    # Assignment context
    (
        "890000000011137",
        "The engagement was connected to this assignment: <quest>. One confirmed detail may matter: <note>",
        "Бой был связан со следующим заданием: <quest>. Одна подтверждённая подробность может иметь "
        "значение: <note>",
    ),
    (
        "890000000011138",
        "The engagement was connected to this assignment: <quest>.",
        "Бой был связан со следующим заданием: <quest>.",
    ),
    (
        "890000000011139",
        "Field records connect the engagement to several active assignments: <quests>.",
        "Полевые записи связывают бой с несколькими активными заданиями: <quests>.",
    ),
    (
        "890000000011140",
        "The team also had this assignment: <quest>. No link to the area was confirmed.",
        "У отряда также было задание: <quest>. Его связь с этим районом не подтверждена.",
    ),
    (
        "890000000011141",
        "No active assignment was tied to this area.",
        "С этим районом не было связано ни одного активного задания.",
    ),
    # Outcome reading
    (
        "890000000011142",
        "The engagement ended in your team's favor.",
        "Бой завершился в пользу вашего отряда.",
    ),
    (
        "890000000011143",
        "The engagement ended in the hostile force's favor.",
        "Бой завершился в пользу противника.",
    ),
    (
        "890000000011144",
        "Your team broke contact and withdrew under fire.",
        "Ваш отряд прервал контакт и отошёл под огнём.",
    ),
    (
        "890000000011145",
        "The opening pattern is consistent with an ambush; the first shots shaped the rest of the "
        "engagement.",
        "Начало боя похоже на засаду: первые выстрелы определили дальнейший ход столкновения.",
    ),
    (
        "890000000011146",
        "The engagement was tied to an active assignment; the favorable outcome may support further work.",
        "Бой был связан с активным заданием; благоприятный исход может помочь в дальнейшей работе.",
    ),
    (
        "890000000011147",
        "The engagement was tied to an active assignment. The adverse outcome may complicate further "
        "work.",
        "Бой был связан с активным заданием. Неблагоприятный исход может осложнить дальнейшую работу.",
    ),
    (
        "890000000011148",
        "Your team withdrew from an area tied to an active assignment.",
        "Ваш отряд отошёл из района, связанного с активным заданием.",
    ),
    # Losses and named opponents
    (
        "890000000011149",
        "Friendly losses — killed: <pkia>, wounded: <pwia>. Hostile losses — killed: <ekia>, wounded: "
        "<ewia>.",
        "Наши потери — погибших: <pkia>, раненых: <pwia>. Потери противника — погибших: <ekia>, "
        "раненых: <ewia>.",
    ),
    (
        "890000000011150",
        "Confirmed killed during the engagement: <name>.",
        "В ходе боя подтверждена гибель: <name>.",
    ),
    (
        "890000000011151",
        "Confirmed wounded during the engagement: <name>. Current condition is unknown.",
        "В ходе боя подтверждено ранение: <name>. Текущее состояние неизвестно.",
    ),
    (
        "890000000011152",
        "Confirmed withdrawal from the engagement: <name>. Further contact remains possible.",
        "Подтверждён отход из боя: <name>. Повторный контакт возможен.",
    ),
    (
        "890000000011153",
        "Confirmed still combat-capable when the engagement ended: <name>. The threat remains.",
        "На момент окончания боя подтверждено, что <name> сохраняет боеспособность. Угроза остаётся.",
    ),
    # Closing assessment
    (
        "890000000011154",
        "The limited scale of the engagement is unlikely to alter enemy activity by itself.",
        "Ограниченный масштаб боя сам по себе вряд ли изменит активность противника.",
    ),
    (
        "890000000011155",
        "Reports of sustained fighting are likely to draw closer attention from hostile forces in the area.",
        "Донесения о затяжном бое, вероятно, привлекут пристальное внимание сил противника в этом районе.",
    ),
    (
        "890000000011156",
        "Losses on this scale are likely to draw attention from hostile commanders beyond the immediate area.",
        "Потери такого масштаба, вероятно, привлекут внимание командования противника за пределами этого "
        "района.",
    ),
]

FIELD_MAIL_FIXES: list[tuple[str, str, str]] = [
    (
        "890000000011200",
        "R.I.S. <desk@ris-intel.net>",
        "R.I.S. <desk@ris-intel.net>",
    ),
    (
        "890000000011201",
        "R.I.S. — confirmed fighter type: <unit_title>",
        "R.I.S. — подтверждён тип бойца: <unit_title>",
    ),
    (
        "890000000011202",
        (
            "Confirmed contact: <unit_title>.\n\nThe report is sufficient to distinguish this fighter "
            "type in the field, but not yet to assess its methods with confidence. A fuller assessment "
            "will follow after three fighters of this type have been confirmed killed.\n\n— R.I.S. Field "
            "Desk"
        ),
        (
            "Контакт подтверждён: <unit_title>.\n\nЭтого донесения уже достаточно, чтобы отличать этот тип "
            "бойцов в бою, но пока недостаточно для уверенной оценки его действий. Подробная сводка "
            "будет подготовлена после подтверждения гибели трёх бойцов этого типа.\n\n— Полевой отдел "
            "R.I.S."
        ),
    ),
    (
        "890000000011203",
        "R.I.S. — confirmed death: <name>",
        "R.I.S. — подтверждена гибель: <name>",
    ),
    (
        "890000000011204",
        (
            "Confirmed after the fighting: <name> is dead.\n\nThe local force has lost a proven fighter. "
            "The tactical effect cannot yet be assessed.\n\n— R.I.S. Field Desk"
        ),
        (
            "После боя подтверждена гибель: <name>.\n\nМестные силы потеряли опытного бойца. Тактические "
            "последствия пока оценить невозможно.\n\n— Полевой отдел R.I.S."
        ),
    ),
    (
        "890000000011205",
        "R.I.S. — key figure confirmed dead: <name>",
        "R.I.S. — подтверждена гибель ключевой фигуры: <name>",
    ),
    (
        "890000000011206",
        (
            "Confirmed after the fighting: <name> is dead.\n\nThis may change the local balance of power; "
            "the consequences remain unclear.\n\n— R.I.S. Field Desk"
        ),
        (
            "После боя подтверждена гибель: <name>.\n\nЭто может изменить местный расклад сил; последствия "
            "пока неясны.\n\n— Полевой отдел R.I.S."
        ),
    ),
]

# Kept as the legacy apply surface; field mail and reserved-range strings have
# their own explicit categories so old partial apply tools cannot wire them by
# accident.
STRING_FIXES: list[tuple[str, str, str]] = WELCOME_FIXES + UI_FIXES + AAR_FIXES


# ---------------------------------------------------------------------------
# The Major's Strategy — keyed by stable public Email id.
# Text is identical to docs/design/ris-major-strategy.md.
# ---------------------------------------------------------------------------

MAJOR_STRATEGY: dict[str, dict[str, str]] = {
    "RIS_MajorStrategy_Network": {
        "design_id": "strategy_network",
        "title_id": "890000000011322",
        "body_id": "890000000011323",
        "title_en": "The Major's Strategy: a network of strongpoints",
        "title_ru": "Стратегия Майора: сеть опорных пунктов",
        "body_en": (
            "Recent reports suggest that the Major does not run the Legion as one army. He has divided "
            "the country into districts, each centered on a fort. Patrols leave from it, battered units "
            "return to it, and money and recruits gathered from nearby settlements pass through its "
            "gates.\n\n"
            "Destroying a column is a serious loss, but it does not end the system. As long as its "
            "strongpoint remains active, the Major's men will eventually return to the roads. If you want "
            "an area to stay quiet, watch where the units go home—not only where you meet them.\n\n"
            "— R.I.S. Field Desk"
        ),
        "body_ru": (
            "По последним донесениям, Майор управляет Легионом не как одной армией. Он разделил страну на "
            "округа, и в центре каждого стоит форт. Оттуда выходят патрули, туда возвращаются потрёпанные "
            "отряды, там собирают деньги и новобранцев из окрестных поселений.\n\n"
            "Уничтоженная колонна — серьёзная потеря, но не конец. Пока её опорный пункт действует, люди "
            "Майора со временем вернутся на дороги. Если хотите надолго успокоить район, следите не только "
            "за отрядами, но и за тем, куда они возвращаются.\n\n"
            "— Полевой отдел R.I.S."
        ),
    },
    "RIS_MajorStrategy_Roads": {
        "design_id": "strategy_roads",
        "title_id": "890000000011324",
        "body_id": "890000000011325",
        "title_en": "The Major's Strategy: a new flag does not close the road",
        "title_ru": "Стратегия Майора: смена флага не закрывает дорогу",
        "body_en": (
            "Our observers confirm that Legion patrols continue to use familiar routes even after the "
            "ground has changed hands. They are especially willing to cross stretches where they see no "
            "permanent guard.\n\n"
            "To the Major, a road is still his as long as his men can walk it. Taking an area and keeping "
            "it quiet are different jobs. If a route matters to you, changing the flag over it will not "
            "be enough.\n\n"
            "— R.I.S. Field Desk"
        ),
        "body_ru": (
            "Наши наблюдатели подтверждают: патрули Легиона продолжают пользоваться знакомыми маршрутами, "
            "даже когда территория уже перешла под ваш контроль. Особенно охотно они проходят там, где не "
            "видят постоянной охраны.\n\n"
            "Для Майора дорога остаётся его дорогой, пока по ней можно пройти. Взять район и действительно "
            "успокоить его — разные задачи. Если маршрут для вас важен, одной смены флага недостаточно.\n\n"
            "— Полевой отдел R.I.S."
        ),
    },
    "RIS_MajorStrategy_Villages": {
        "design_id": "strategy_villages",
        "title_id": "890000000011326",
        "body_id": "890000000011327",
        "title_en": "The Major's Strategy: two kinds of tribute",
        "title_ru": "Стратегия Майора: две дани",
        "body_en": (
            "The Legion demands more than money from the villages. Collectors make their rounds for cash, "
            "while recruiters follow other routes in search of new bodies. Both travel with small "
            "escorts: their job is to bring what they gather back to the fort, not to look for a major "
            "fight.\n\n"
            "After each run they return to base, deliver the money or recruits, rest, and leave again. "
            "Intercepting one trip will cost the district money or manpower, but the system will continue "
            "as long as the fort controls the surrounding settlements.\n\n"
            "— R.I.S. Field Desk"
        ),
        "body_ru": (
            "Легион требует от деревень не только деньги. Сборщики объезжают хозяйства и забирают выручку; "
            "по другим маршрутам идут вербовщики, которым нужны новые люди. Обоим обычно хватает небольшого "
            "эскорта: их задача — довезти собранное до форта, а не искать большой бой.\n\n"
            "После рейса они возвращаются на базу, сдают деньги или приводят новобранцев, отдыхают и через "
            "некоторое время выходят снова. Перехваченный рейс лишит округ части дохода или пополнения, но "
            "сама система будет работать, пока форт держит окрестности.\n\n"
            "— Полевой отдел R.I.S."
        ),
    },
    "RIS_MajorStrategy_Recon": {
        "design_id": "strategy_eyes",
        "title_id": "890000000011328",
        "body_id": "890000000011329",
        "title_en": "The Major's Strategy: first, they look",
        "title_ru": "Стратегия Майора: сначала — разведка",
        "body_en": (
            "When a district becomes unsettled, the Major does not always answer with force at once. A "
            "small party leaves the fort first—to check the roads, pick up a trail, and learn where you "
            "have stopped. If it returns empty-handed, the alarm gradually fades. If it sees you, the "
            "local commander receives coordinates instead of rumors.\n\n"
            "The danger is not the size of the scouting party. Its real weapon is the report that tells "
            "the next unit where to go. If the scouts broke contact and headed home, assume the clock has "
            "already started.\n\n"
            "— R.I.S. Field Desk"
        ),
        "body_ru": (
            "Когда в округе становится неспокойно, Майор не всегда сразу отвечает силой. Сначала из форта "
            "выходит небольшая группа: проверить дороги, найти следы и понять, где вы остановились. Если "
            "она возвращается ни с чем, тревога постепенно стихает. Если замечает вас, местный командир "
            "получает уже не слухи, а координаты.\n\n"
            "Такая группа опасна не числом. Её главное оружие — донесение, после которого другие отряды "
            "знают, куда идти. Если разведчики ушли после контакта, считайте, что время уже пошло.\n\n"
            "— Полевой отдел R.I.S."
        ),
    },
    "RIS_MajorStrategy_Response": {
        "design_id": "strategy_answer",
        "title_id": "890000000011330",
        "body_id": "890000000011331",
        "title_en": "The Major's Strategy: the nearest fort answers",
        "title_ru": "Стратегия Майора: ответ ближайшего форта",
        "body_en": (
            "The Major leaves most urgent decisions to his local commanders. A lost position or a "
            "confirmed report prompts the nearest fort to reinforce its approaches and send men toward "
            "the threat.\n\n"
            "This is not an endless reserve or a general offensive. The response is tied to a specific "
            "threat, and its size depends on the men and money available in that district. If a separate "
            "column is already moving your way, assume that someone has told the fort where to look.\n\n"
            "— R.I.S. Field Desk"
        ),
        "body_ru": (
            "Большинство срочных решений Майор оставляет местным командирам. Потерянная позиция или "
            "подтверждённое донесение заставляют ближайший форт укреплять подступы и высылать людей к месту "
            "угрозы.\n\n"
            "Это не бесконечный резерв и не общее наступление. Такой ответ привязан к конкретной угрозе, а "
            "его размах зависит от людей и денег в данном округе. Если отдельная колонна уже движется в "
            "вашу сторону, исходите из того, что кто-то сообщил форту, где вас искать.\n\n"
            "— Полевой отдел R.I.S."
        ),
    },
    "RIS_MajorStrategy_Cargo": {
        "design_id": "strategy_cargo",
        "title_id": "890000000011332",
        "body_id": "890000000011333",
        "title_en": "The Major's Strategy: cargo takes the quiet road",
        "title_ru": "Стратегия Майора: груз выбирает тихую дорогу",
        "body_en": (
            "Combat patrols may cross ground under your control without hesitation. Valuable cargo is "
            "handled more carefully. Convoys carrying money, diamonds, or reinforcements will try to avoid "
            "your positions whenever another route remains open.\n\n"
            "A long detour will not stop them. If every road passes under your guns, however, a new "
            "shipment may not leave at all. A patrol is prepared to risk contact; cargo looks for a route "
            "where contact never happens.\n\n"
            "— R.I.S. Field Desk"
        ),
        "body_ru": (
            "Боевые патрули могут идти прямо через подконтрольную вам территорию. Ценный груз ведут "
            "осторожнее. Конвои с деньгами, алмазами и пополнением стараются обходить ваши позиции, если "
            "остаётся другой путь.\n\n"
            "Даже длинный крюк их не остановит. Но если все дороги проходят под вашими стволами, новый "
            "рейс могут вовсе не выпустить. Патруль готов рисковать встречей; груз ищет маршрут, на котором "
            "встречи не будет.\n\n"
            "— Полевой отдел R.I.S."
        ),
    },
    "RIS_MajorStrategy_Recovery": {
        "design_id": "strategy_wounded",
        "title_id": "890000000011334",
        "body_id": "890000000011335",
        "title_en": "The Major's Strategy: they come back",
        "title_ru": "Стратегия Майора: они возвращаются",
        "body_en": (
            "A depleted Legion unit is not written off after a failed mission. When too many of its men "
            "are wounded or dead, it falls back to the nearest fort, waits for replacements, and only then "
            "returns to the road.\n\n"
            "The quiet after a successful ambush may therefore be temporary. A familiar patrol has not "
            "vanished; it is rebuilding behind the walls. If you want to know whether a district is truly "
            "empty, keep watching the roads that lead back to the fort.\n\n"
            "— R.I.S. Field Desk"
        ),
        "body_ru": (
            "Поредевший отряд Легиона не списывают после неудачного выхода. Если слишком много бойцов "
            "ранено или убито, он отходит к ближайшему форту, остаётся там до пополнения и лишь потом снова "
            "выходит на дорогу.\n\n"
            "Поэтому затишье после удачной засады может оказаться временным. Знакомый патруль не исчез — он "
            "восстанавливает силы за стенами. Если хотите понять, действительно ли округ опустел, "
            "наблюдайте за дорогами, ведущими к форту.\n\n"
            "— Полевой отдел R.I.S."
        ),
    },
    "RIS_MajorStrategy_Retribution": {
        "design_id": "strategy_red",
        "title_id": "890000000011336",
        "body_id": "890000000011337",
        "title_en": "The Major's Strategy: retribution from headquarters",
        "title_ru": "Стратегия Майора: возмездие из штаба",
        "body_en": (
            "The nearest forts handle most threats. When losses and alarm continue to mount, however, the "
            "reports eventually reach the Major himself. A heavy column then leaves his headquarters—not "
            "to scout or guard a road, but to exact retribution.\n\n"
            "Such deployments are rare, which is precisely why they matter. They mean the local forces "
            "were judged insufficient and the Major chose to spend his own reserve. A column this heavy "
            "points beyond the nearest fort—to the Major's own reserve.\n\n"
            "— R.I.S. Field Desk"
        ),
        "body_ru": (
            "С большинством угроз разбираются ближайшие форты. Но когда потери и тревога накапливаются, "
            "донесения доходят до самого Майора. Тогда из его штаба выходит тяжёлая колонна — не для "
            "разведки и не для охраны дороги, а для возмездия.\n\n"
            "Такие выходы редки, и именно поэтому важны. Они означают, что местных сил уже сочли "
            "недостаточными и Майор решил потратить собственный резерв. Такая тяжёлая колонна указывает "
            "не на ближайший форт, а на собственный резерв Майора.\n\n"
            "— Полевой отдел R.I.S."
        ),
    },
    "RIS_MajorStrategy_Awakening": {
        "design_id": "strategy_sleep",
        "title_id": "890000000011338",
        "body_id": "890000000011339",
        "title_en": "The Major's Strategy: not every district wakes at once",
        "title_ru": "Стратегия Майора: не все округа просыпаются сразу",
        "body_en": (
            "The Legion's distant forts do not all move at the same pace. Some survive on what they have "
            "for a long time: they rarely send out new units, conserve their men, and make little response "
            "to trouble. It can look like weakness or indecision, but the cause is usually simpler—the "
            "district has not yet received help from headquarters.\n\n"
            "The first serious delivery changes that. Recruiters and fresh columns appear on the roads, "
            "and the local commander begins to act with greater confidence. If a formerly quiet district "
            "suddenly comes alive, the Major's supply line has probably reached it.\n\n"
            "— R.I.S. Field Desk"
        ),
        "body_ru": (
            "Дальние форты Легиона живут не в одном ритме. Некоторые долго держатся на остатках: редко "
            "выводят новые отряды, берегут людей и почти не отвечают на тревогу. Это легко принять за "
            "слабость или нерешительность, но причина обычно проще — до округа ещё не дошла помощь из "
            "штаба.\n\n"
            "После первой серьёзной поставки всё меняется. На дорогах появляются вербовщики и новые "
            "колонны, а местный командир начинает действовать увереннее. Если прежде тихий район внезапно "
            "пришёл в движение, вероятнее всего, до него наконец дотянулась линия снабжения.\n\n"
            "— Полевой отдел R.I.S."
        ),
    },
}

# Fixed R.I.S. identity/sender strings outside the feature-reserved range.
RIS_FIXED_STRINGS: list[tuple[str, str, str]] = [
    ("890000000006920", "R.I.S.", "R.I.S."),
    (
        "890000000006921",
        "R.I.S. <desk@ris-intel.net>",
        "R.I.S. <desk@ris-intel.net>",
    ),
    (
        "890000000006939",
        "R.I.S. <legion-desk@ris-intel.net>",
        "R.I.S. <legion-desk@ris-intel.net>",
    ),
]

# Additional approved R.I.S. strings in the remainder of the reserved range.
# 890000000011348…11349 remain intentionally unallocated.
RIS_EXTRA_STRINGS: list[tuple[str, str, str]] = [
    (
        "890000000011340",
        "The Major's Strategy",
        "Стратегия Майора",
    ),
    (
        "890000000011341",
        "This account is based on remote reports; field detail remains limited.",
        "Сводка составлена по дистанционным донесениям; полевых подробностей мало.",
    ),
    (
        "890000000011342",
        "Archived engagement",
        "Архивная боевая сводка",
    ),
    (
        "890000000011343",
        (
            "An older engagement in <sector> survives only as a partial record. The available evidence "
            "is not enough to reconstruct the original field account with confidence."
        ),
        (
            "Старая сводка о бое в районе <sector> сохранилась лишь частично. Имеющихся данных "
            "недостаточно, чтобы уверенно восстановить первоначальное полевое донесение."
        ),
    ),
    (
        "890000000011344",
        (
            "The immediate objective was achieved, but confirmed hostiles remained in the area when the "
            "report closed."
        ),
        (
            "Непосредственная задача выполнена, но на момент закрытия сводки в районе оставались "
            "подтверждённые противники."
        ),
    ),
    (
        "890000000011345",
        "Unidentified fighter",
        "Неопознанный боец",
    ),
    (
        "890000000011346",
        "Unidentified opponent",
        "Неопознанный противник",
    ),
    (
        "890000000011347",
        (
            "Archived engagement in <sector>. Record time: <time>. The available evidence is not enough "
            "to reconstruct the original field account with confidence."
        ),
        (
            "Архивная запись боя в секторе <sector>. Время записи: <time>. Доступных сведений "
            "недостаточно, чтобы уверенно восстановить первоначальное полевое донесение."
        ),
    ),
]

ALL_SIMPLE_STRINGS: list[tuple[str, str, str]] = (
    RIS_FIXED_STRINGS + STRING_FIXES + FIELD_MAIL_FIXES + RIS_EXTRA_STRINGS
)


__all__ = [
    "DOSSIERS",
    "DOSSIER_LOC_IDS",
    "QUEST_DOSSIERS",
    "QUEST_DOSSIER_LOC_IDS",
    "WELCOME_FIXES",
    "UI_FIXES",
    "AAR_FIXES",
    "FIELD_MAIL_FIXES",
    "RIS_FIXED_STRINGS",
    "RIS_EXTRA_STRINGS",
    "STRING_FIXES",
    "ALL_SIMPLE_STRINGS",
    "MAJOR_STRATEGY",
]
