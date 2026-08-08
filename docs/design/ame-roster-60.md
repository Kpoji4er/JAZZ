# AME Roster — 60 карточек (design)

Источник контракта: [`JAZZ-UNITS-005`](../specs/active/JAZZ-UNITS-005.md), companion [`ame-mercenary-exchange.md`](ame-mercenary-exchange.md).

Это **design-roster** для реализации: фиксированные имя/статы/био/один инвентарь. Runtime-ротация меняет только Available/`NotListed`/terminal — не перегенерирует карточку после hire.

## Сводка пула

| Категория (вкладка) | Кол-во | Примечание |
| --- | ---: | --- |
| Irregulars | 20 | A/D ≈60; Marks median ≈45 (weak ≈30); HP/Str wide; high Wisdom |
| Fighters | 18 | A/D/Marks ≈65; kit ≤1-3; ≥30% autorifle/MG/GL с Hardened |
| Hardened | 10 | A/D/Marks ≈70; Will mid; kit ≤2-1 |
| Specialists | 12 | Medic×3, Instructor×3, Sniper×2, Sapper×2, Mechanic×2 |

- Инвентарь: **1 фиксированный вариант** на слот (без `Randomization`).
- **Appearance:** на слот свой клон `JAZZ_AME_NN` (donor jazz-units `Legion*` / Rebels / GrandChien / keep; Irregulars lean jazz Legion*; blue recolor; каски снимаются). Карта: [`ame-appearance-map.json`](ame-appearance-map.json).
- **Кит:** Irr ≤ **1-2**; Fight ≤ **1-3**; Hard/Spec ≤ **2-1**. **`Type56` — потолок AR, только Hardened.** `SKS`/bolt — только Sniper.
- **ПП:** винтаж T1 — `Thompson` / `M3GreaseGun` / `PPS43` / `PPSH` / `MP40` / `MAT49` / `Sterling`. **`UZI` и прочий T2 ПП в стартовых китах нет.**
- **Бинты:** Fighters ~40%; Hardened всегда. **Sapper:** часть с `PipeBomb`.
- Voice pool: Jazz remesh majority (`Jazz_AME_Male_Low` / `Male_Hard` / `Female`) + `PierreMerc` variety (~1/8 males on bucket) + small IMP minority (~1/8; VR → `IMP_male_01` / `IMP_female_01`).
- **Bio canon:** самостоятельные RU+EN биографии и двуязычные profile blurbs; без мета-цифр статов/тиров.
- Nick: в основном Hardened. Grand Chien: заметная доля.
- **Personality:** sparse — **12/60** slots get one Personality-tier perk (`Negotiator`/`Scoundrel`/`Psycho`/`Stealthy`/`Optimist`/`Pessimist`/`Loner`); no Mimicry/Veteran. AME hire Loadout still hides Traits strip.

## Irregulars

### `JAZZ_AME_01` — Kwame Mensah

- **Nationality:** `Ghana`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $7
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Personality:** `Negotiator`
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_01` ← donor `LegionGoon` (male; blue recolor, source не править)
- **Inventory (fixed):** Knife

| Stat | |
| --- | ---: |
| Health | 86 |
| Agility | 60 |
| Dexterity | 60 |
| Strength | 64 |
| Wisdom | 70 |
| Will | 28 |
| Leadership | 5 |
| Marksmanship | 45 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 5 |

**Биография (RU):** По ночам в Аккре Кваме Менса обходил кварталы с добровольным патрулём, пока общая касса не опустела. Он говорит негромко, сперва выслушивает обе стороны и лишь потом решает, стоит ли вмешиваться. Оружию его учили урывками между сменами, поэтому ясную задачу Кваме любит больше поспешной пальбы. На ремне он до сих пор носит начищенный латунный свисток, хотя пользуется им только в крайнем случае.

**Biography (EN):** A polished brass whistle still hangs from Kwame Mensah's belt, rarely blown but always ready. It outlasted years of walking an Accra neighbourhood after dark and settling doorstep quarrels after the watch fund ran dry. Kwame would rather hear the whole story than win an argument. Formal weapons practice came to him in scraps, so he is happiest when someone makes the purpose plain.

**Профиль (RU):** Тихий патрульный с латунным свистком и внимательным взглядом

**Profile (EN):** A quiet watchman with a brass whistle and attentive eyes

### `JAZZ_AME_02` — Jean-Baptiste Okoro

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $14
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_02` ← donor `LegionGoon_alt` (male; blue recolor, source не править)
- **Inventory (fixed):** DoubleBarrelShotgun · 12g×6 · Knife

| Stat | |
| --- | ---: |
| Health | 84 |
| Agility | 62 |
| Dexterity | 60 |
| Strength | 56 |
| Wisdom | 66 |
| Will | 26 |
| Leadership | 0 |
| Marksmanship | 45 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 0 |

**Биография (RU):** Охота в Гранд-Шьен кормила Жан-Батиста Окоро, пока зверь не ушёл за границу его лицензии, а вместе с ним и заработок. Он не любит суеты и заранее выбирает место, где не придётся делать второй выстрел. В потрёпанном кожаном подсумке Окоро хранит горсть старых гильз, напоминающих об особенно долгих зимах. Шумное оружие заставляет его насторожиться; ждать же Окоро умеет так долго, что окружающие начинают говорить шёпотом.

**Biography (EN):** The forests of Grand Chien once paid Jean-Baptiste Okoro's way, until a licensing dispute left his traps empty and his name unwelcome. He moves with a hunter's economy and dislikes anything that scatters birds before the work begins. Weathered shell cases ride in a leather pouch, keepsakes from lean seasons he survived without complaint. Crowded streets make him wary, but stillness brings out the best in him.

**Профиль (RU):** Охотник, который бережёт тишину и горсть старых гильз

**Profile (EN):** A patient hunter carrying a handful of winter memories

### `JAZZ_AME_03` — Ibrahim Touré

- **Nationality:** `Mali`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $21
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Personality:** `Negotiator`
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_03` ← donor `LegionGoon_alt_2` (male; blue recolor, source не править)
- **Inventory (fixed):** SWModel10 · .38×12 · Knife

| Stat | |
| --- | ---: |
| Health | 88 |
| Agility | 58 |
| Dexterity | 58 |
| Strength | 62 |
| Wisdom | 72 |
| Will | 32 |
| Leadership | 10 |
| Marksmanship | 43 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 10 |

**Биография (RU):** На малийском посту Ибрахиму Туре чаще приходилось разнимать уличные ссоры, чем доставать револьвер. Он умеет понизить голос именно тогда, когда все вокруг начинают кричать, и обычно этим выигрывает нужную минуту. После закрытия участка Ибрахим оставил себе потёртый жетон и привычку складывать чистый платок в аккуратный квадрат для чужих ссадин. Блеска в его стрельбе нет, а в толчее он не забывает, кто нуждается в помощи первым.

**Biography (EN):** A worn police badge shares Ibrahim Touré's pocket with a spotless handkerchief folded for the next split lip. Both survived a Malian street post where tempers caused more trouble than weapons. Ibrahim can turn a shouting match down by speaking softly, though a distant target gives him fewer clues than an angry face. When panic spreads through a crowd, he looks for the person everyone else has overlooked.

**Профиль (RU):** Бывший постовой, умеющий вернуть голос шумной улице

**Profile (EN):** The former constable who lowers the temperature of a street

### `JAZZ_AME_04` — Sani Abubakar

- **Nationality:** `Nigeria`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $27
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Personality:** —
- **Voice:** `PierreMerc` → VR `PierreMerc`
- **Appearance:** `JAZZ_AME_04` ← donor `LegionGoon_alt_3` (male; blue recolor, source не править)
- **Inventory (fixed):** Knife

| Stat | |
| --- | ---: |
| Health | 92 |
| Agility | 56 |
| Dexterity | 54 |
| Strength | 78 |
| Wisdom | 58 |
| Will | 22 |
| Leadership | 0 |
| Marksmanship | 43 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 0 |

**Биография (RU):** Сани Абубакар таскал цемент на стройке нигерийской казармы и так и не дождался части, которая назвала бы его своим. Он охотно берётся за тяжёлую работу, но от внезапного окрика сперва вздрагивает и лишь затем собирается. За ухом Сани держит красный плотницкий карандаш и машинально отмечает на дверях, что уже укреплено. Опыта у него мало, однако после испуга он всегда возвращается закончить начатое.

**Biography (EN):** Before anyone issued him a uniform, Sani Abubakar was hauling cement and forcing warped doors into place at a Nigerian barracks. Loud voices unsettle him more than he admits, yet his broad hands seldom abandon a task halfway through. A red carpenter's pencil lives behind his ear, and he marks every repaired hinge with a tiny cross. He has much to learn about danger, but none about carrying another person's share.

**Профиль (RU):** Сильные руки, красный карандаш и честно признанный страх

**Profile (EN):** Strong hands, a red pencil, and fear honestly faced

### `JAZZ_AME_05` — Pierre Ndongo

- **Nationality:** `Congo`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $34
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_05` ← donor `LegionButcher` (male; blue recolor, source не править)
- **Inventory (fixed):** — (empty hands)

| Stat | |
| --- | ---: |
| Health | 85 |
| Agility | 60 |
| Dexterity | 60 |
| Strength | 54 |
| Wisdom | 76 |
| Will | 30 |
| Leadership | 8 |
| Marksmanship | 30 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 5 |

**Биография (RU):** Долгие годы на конголезских блокпостах научили Пьера Ндонго узнавать постоянных путников по походке. Он быстрее запоминает лицо и маршрут, чем осваивает новое движение с оружием. В кармане Пьер хранит автобусные билеты, раскладывая их по дорогам и датам, словно маленький личный атлас. Сейчас его руки пусты, но рядом с ним редко теряется человек или нужный поворот.

**Biography (EN):** Old bus tickets fill Pierre Ndongo's breast pocket, sorted by route in neat paper bundles. They accumulated while he watched the same Congolese road until faces, debts, and detours arranged themselves into a private map. Pierre is slow to volunteer an opinion and quick to notice when a familiar traveller changes shoes. A weapon never felt as natural as remembering where people came from, so he listens before placing himself in danger.

**Профиль (RU):** Молчаливый хранитель дорог, лиц и старых автобусных билетов

**Profile (EN):** A quiet keeper of roads, faces, and old bus tickets

### `JAZZ_AME_06` — Moussa Diop

- **Nationality:** `Senegal`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $39
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Personality:** `Loner`
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_06` ← donor `LegionButcher_alt` (male; blue recolor, source не править)
- **Inventory (fixed):** Winchester1894 · .44×14 · Knife

| Stat | |
| --- | ---: |
| Health | 80 |
| Agility | 68 |
| Dexterity | 64 |
| Strength | 52 |
| Wisdom | 68 |
| Will | 28 |
| Leadership | 0 |
| Marksmanship | 49 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 0 |

**Биография (RU):** Сенегальские тропы долго кормили Муссу Диопа за умение заметить след раньше других. Старый винчестер достался ему от деда, и после каждого выхода Мусса протирает приклад кусочком льняной ткани. Компания делает его угрюмым; в одиночестве шаг Муссы становится лёгким и почти бесшумным. Патроны считает заранее, потому что терпеть не может исправлять спешку вторым выстрелом.

**Biography (EN):** The Winchester inherited from his grandfather is Moussa Diop's sole indulgence, polished nightly with linen worn almost transparent. Before paved roads drew younger hunters away, Senegalese game trails provided his living. Strangers find Moussa distant, but the bush brings a loose, unhurried grace to his step. He counts cartridges before leaving camp and regards a wasted shot as a failure of patience, not equipment.

**Профиль (RU):** Охотник, дедовский винчестер и почти бесшумный шаг

**Profile (EN):** A solitary tracker devoted to his grandfather's Winchester

### `JAZZ_AME_07` — Abel Getachew

- **Nationality:** `Ethiopia`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $43
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_07` ← donor `LegionButcher_alt_2` (male; blue recolor, source не править)
- **Inventory (fixed):** — (empty hands)

| Stat | |
| --- | ---: |
| Health | 87 |
| Agility | 58 |
| Dexterity | 56 |
| Strength | 48 |
| Wisdom | 78 |
| Will | 34 |
| Leadership | 5 |
| Marksmanship | 30 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 8 |

**Биография (RU):** С эфиопских учений Абель Гетачью ушёл прежде, чем строевая успела стать привычкой. Достаточно показать ему приём один раз, и к вечеру он уже повторяет его, пусть пока слишком напряжённо. Каждое утро Абель заново шнурует ботинки по уставной схеме, будто этим можно наверстать пропущенную службу. В момент выстрела он торопится, но замечание запоминает надолго и упрямо пробует снова.

**Biography (EN):** Every dawn Abel Getachew relaces his boots exactly as a sergeant once taught him, preserving a small ritual of unfinished service. He left an Ethiopian training ground before the drills could sand down his doubts. A demonstration stays with Abel after a single viewing, then eagerness spoils the result. His hands have not found a calm rhythm under pressure, but embarrassment only sends him back to practise.

**Профиль (RU):** Недоученный солдат, который каждое утро начинает заново

**Profile (EN):** An unfinished soldier who starts over every morning

### `JAZZ_AME_08` — Thabo Molefe

- **Nationality:** `SouthAfrica`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $48
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Personality:** —
- **Voice:** `IMP_male_02` → VR `IMP_male_01`
- **Appearance:** `JAZZ_AME_08` ← donor `LegionButcher_alt_3` (male; blue recolor, source не править)
- **Inventory (fixed):** DoubleBarrelShotgun · 12g×8 · Knife

| Stat | |
| --- | ---: |
| Health | 90 |
| Agility | 60 |
| Dexterity | 58 |
| Strength | 70 |
| Wisdom | 56 |
| Will | 26 |
| Leadership | 12 |
| Marksmanship | 45 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 0 |

**Биография (RU):** Табо Молефе сторожил южноафриканские фермы, спал в сараях и отгонял воров старым двуствольным ружьём. Его неспешное движение у ворот сменяется таким спокойствием, что хозяева забывали проверять замок. Единственная прихоть Табо — зелёная эмалированная кружка, из которой он пьёт даже холодную воду. Сложные приёмы даются ему не сразу, но первый хлопок никогда не срывает его с места.

**Biography (EN):** Thabo Molefe guarded South African farmyards, sleeping among feed sacks with a double-barrelled gun within reach. He is deliberate rather than quick, a broad presence that makes a gate feel narrower. A chipped green enamel mug travels everywhere with him, because tea tastes wrong from tin. Nobody trusted Thabo with elaborate instructions, yet sudden noise never sends him running and a long night seldom draws a complaint.

**Профиль (RU):** Неспешный сторож с зелёной кружкой и надёжной стойкой

**Profile (EN):** A steadfast farm guard with a chipped green mug

### `JAZZ_AME_09` — Daniel Kiprop

- **Nationality:** `Kenya`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $9
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_09` ← donor `LegionRaider` (male; blue recolor, source не править)
- **Inventory (fixed):** DoubleBarrelShotgun · 12g×6 · Knife

| Stat | |
| --- | ---: |
| Health | 76 |
| Agility | 64 |
| Dexterity | 62 |
| Strength | 46 |
| Wisdom | 72 |
| Will | 24 |
| Leadership | 0 |
| Marksmanship | 47 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 0 |

**Биография (RU):** Движение в траве Даниэль Кипроп замечал раньше хруста ветки ещё в годы работы с кенийским егерем. Он худощав, не любит долгой возни с тяжестью и всегда ищет путь, где можно пройти легче. Перед рассветом Даниэль касается земли двумя пальцами, проверяя ночные следы, даже на городской улице. Хорошей винтовки у него никогда не было, поэтому он научился ценить удачно выбранное место больше дорогой вещи.

**Biography (EN):** At first light Daniel Kiprop still presses two fingers to the ground, even when the only tracks belong to bicycles. A Kenyan ranger taught him to read the flicker of grass before other men heard a branch move. Bulky burdens tire Daniel, so he chooses cleaner routes through rough country. Fine rifles passed him by, but an early glimpse and a well-chosen position have often served him better.

**Профиль (RU):** Зоркий егерь, читающий следы даже на городской пыли

**Profile (EN):** A lean scout who reads tracks even in city dust

### `JAZZ_AME_10` — Emmanuel Kabongo

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $16
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_10` ← donor `LegionRaider_alt` (male; blue recolor, source не править)
- **Inventory (fixed):** — (empty hands)

| Stat | |
| --- | ---: |
| Health | 86 |
| Agility | 60 |
| Dexterity | 60 |
| Strength | 60 |
| Wisdom | 64 |
| Will | 30 |
| Leadership | 8 |
| Marksmanship | 32 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 5 |

**Биография (RU):** Когда прямые дороги Гранд-Шьен стали слишком заметны, Эммануэль Кабонго повёл связных по тропам. Он не командует голосом, но растерянные люди почему-то держатся ближе к его плечу. В рубашке Эммануэль носит сложенный лист, где углём отмечены ручьи, колючие заросли и места для короткого сна. Оружие лежит в его руках неловко — к неправильной развилке он при этом не вывел ни одного спутника.

**Biography (EN):** When the main roads of Grand Chien became unsafe, Emmanuel Kabongo led couriers along creek beds and forgotten footpaths. He has no taste for speeches, though frightened companions naturally match his pace. A charcoal map, softened by sweat and repeated folding, stays tucked inside his shirt. Emmanuel handles a gun like a borrowed tool, but darkness has never made him forget which fork leads home.

**Профиль (RU):** Проводник с угольной картой и памятью на развилки

**Profile (EN):** A pathfinder carrying a charcoal map close to his heart

### `JAZZ_AME_11` — Aisha Hassan

- **Nationality:** `Kenya`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $23
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Personality:** `Psycho`
- **Voice:** `Jazz_AME_Female` → VR `Jazz_AME_Female`
- **Appearance:** `JAZZ_AME_11` ← donor `GrandChien_CommanderFemale` (female; blue recolor, source не править)
- **Inventory (fixed):** Knife

| Stat | |
| --- | ---: |
| Health | 78 |
| Agility | 58 |
| Dexterity | 56 |
| Strength | 42 |
| Wisdom | 74 |
| Will | 20 |
| Leadership | 0 |
| Marksmanship | 30 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 0 |

**Биография (RU):** Грохот металла до сих пор преследует Аишу Хассан после лет, проведённых за разгрузкой кенийского порта. Она вспыхивает быстро, а после резкого звука ненавидит себя за заметную дрожь в пальцах. На шее Аиша носит старый жетон от шкафчика, единственную вещь, которую забрала с последней смены. Ей не хватает спокойствия и опыта, но тесные проходы и тяжёлый день уже не кажутся поводом отступить.

**Biography (EN):** The brass token from Aisha Hassan's old dock locker hangs on a cord, its stamped edge polished by sleepless fingers. Years of crates slamming down beside her boots ended when she finally left the Kenyan port. Sharp sounds still catch Aisha's breath, and embarrassment can turn fright into a cutting reply. She is slight and unseasoned, but knows how to keep moving through cramped spaces when everyone is tired.

**Профиль (RU):** Портовый жетон, быстрый нрав и упрямое движение вперёд

**Profile (EN):** A dock token, a quick temper, and stubborn forward motion

### `JAZZ_AME_12` — Amadou Keita

- **Nationality:** `Mali`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $30
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Personality:** —
- **Voice:** `PierreMerc` → VR `PierreMerc`
- **Appearance:** `JAZZ_AME_12` ← donor `LegionRaider_alt_2` (male; blue recolor, source не править)
- **Inventory (fixed):** Machete

| Stat | |
| --- | ---: |
| Health | 88 |
| Agility | 60 |
| Dexterity | 58 |
| Strength | 68 |
| Wisdom | 54 |
| Will | 28 |
| Leadership | 5 |
| Marksmanship | 45 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 0 |

**Биография (RU):** Амаду Кейта защищал родную деревню в Мали и привык чинить руками то, что другим казалось слишком тяжёлым. Однажды мина разнесла телегу рядом с ним, и с тех пор рыхлая земля заставляет его менять дорогу. Амаду носит длинную ореховую палку и проверяет ею каждый подозрительный край тропы, не скрывая причины. Сюрпризов он не любит; простую опасную работу выполняет без хвастовства и всегда доводит до конца.

**Biography (EN):** Amadou Keita joined a village watch in Mali, where broken shutters and overturned carts usually mattered more than drills. A mine took a wagon apart in front of him, leaving a fear of disturbed soil that no teasing has cured. He tests each doubtful verge with a long walnut stick and explains exactly why. Amadou may choose the widest path around hidden danger, but once a threat is visible he meets it with plain, dependable effort.

**Профиль (RU):** Честный дружинник, проверяющий землю ореховой палкой

**Profile (EN):** An honest watchman who tests the earth before stepping

### `JAZZ_AME_13` — Chidi Okonkwo

- **Nationality:** `Nigeria`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $36
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_13` ← donor `Artillery_Rebels` (male; blue recolor, source не править)
- **Inventory (fixed):** Colt38Special · .38×12 · Knife

| Stat | |
| --- | ---: |
| Health | 84 |
| Agility | 60 |
| Dexterity | 66 |
| Strength | 50 |
| Wisdom | 66 |
| Will | 26 |
| Leadership | 0 |
| Marksmanship | 45 |
| Mechanical | 12 |
| Explosives | 0 |
| Medical | 5 |

**Биография (RU):** Армейская комиссия в Нигерии отвергла Чиди Оконкво, и он устроился разбирать ящики с уликами при полицейском складе. Замки и защёлки поддавались ему легче, чем строевая, а старый револьвер однажды поддался особенно удачно. В спичечном коробке Чиди хранит крошечные пружины, сортируя их по упругости на слух. Он быстро понимает устройство простых вещей, хотя собственное сердце порой напоминает, почему форма ему так и не досталась.

**Biography (EN):** Tiny springs rattle in Chidi Okonkwo's matchbox, each sorted by feel and sound. The Nigerian army rejected him, so stubborn evidence crates behind a police station became his daily work. Latches made sense in a way marching never did, and a forgotten revolver eventually followed Chidi out. His fingers solve small mechanisms quickly, though a hard rush can leave him waiting for his pulse to settle.

**Профиль (RU):** Ловкие пальцы, коробок пружин и чужой револьвер

**Profile (EN):** Quick fingers, a matchbox of springs, and a borrowed revolver

### `JAZZ_AME_14` — Lucien Mbarga

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $41
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Personality:** `Scoundrel`
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_14` ← donor `LegionScout` (male; blue recolor, source не править)
- **Inventory (fixed):** Knife

| Stat | |
| --- | ---: |
| Health | 82 |
| Agility | 64 |
| Dexterity | 60 |
| Strength | 56 |
| Wisdom | 62 |
| Will | 27 |
| Leadership | 0 |
| Marksmanship | 45 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 0 |

**Биография (RU):** Последнее предупреждение рейнджеров лишило Люсьена Мбаргу ружья после силков в заповедных местах Гранд-Шьен. Он не оправдывается и не ищет сочувствия, предпочитая исчезнуть из разговора раньше неудобного вопроса. Просроченную лицензию Люсьен всё же хранит, аккуратно сложив её в рукояти ножен. Без ружья он осторожнее прежнего, но привычка ступать бесшумно осталась при нём.

**Biography (EN):** An expired licence lies absurdly neat inside Lucien Mbarga's knife sheath after many wet seasons. It survived the day Grand Chien rangers confiscated his poaching gun and promised a cell next time. Lucien performs no regret for company, preferring to leave before questions grow specific. Empty-handed at distance, he falls back on the craft nobody managed to seize: moving without announcing himself.

**Профиль (RU):** Браконьер без ружья, сохранивший бесшумную походку

**Profile (EN):** A disarmed poacher whose quiet tread remains untouched

### `JAZZ_AME_15` — Kofi Asante

- **Nationality:** `Ghana`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $45
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_15` ← donor `LegionScout_alt` (male; blue recolor, source не править)
- **Inventory (fixed):** — (empty hands)

| Stat | |
| --- | ---: |
| Health | 83 |
| Agility | 58 |
| Dexterity | 54 |
| Strength | 46 |
| Wisdom | 80 |
| Will | 33 |
| Leadership | 5 |
| Marksmanship | 30 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 10 |

**Биография (RU):** Забытые под партами книги стали ночной школой Кофи Асанте, когда он сторожил здание в Гане. Новую мысль он схватывает быстро, но простая работа руками часто превращается у него в долгий спор с самим собой. В кармане Кофи лежит обломок синего мела, которым он записывает вопросы на любой свободной стене. Ему неловко быть самым неопытным в комнате, хотя чужую ошибку он обычно понимает раньше её владельца.

**Biography (EN):** A blue nub of classroom chalk follows Kofi Asante wherever a blank board might accept a question. He educated himself from books abandoned beneath desks while guarding a Ghanaian school at night. Ideas come readily, while knots, catches, and unfamiliar tools can make Kofi's hands look borrowed. Being treated as useless stings him, but he learns from a mistake before repeating it himself.

**Профиль (RU):** Ночной читатель с синим мелом и неудобными вопросами

**Profile (EN):** A night reader armed with blue chalk and awkward questions

### `JAZZ_AME_16` — João Domingos

- **Nationality:** `Angola`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $50
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Personality:** —
- **Voice:** `IMP_male_01` → VR `IMP_male_01`
- **Appearance:** `JAZZ_AME_16` ← donor `Commander_Rebels` (male; blue recolor, source не править)
- **Inventory (fixed):** Knife

| Stat | |
| --- | ---: |
| Health | 87 |
| Agility | 56 |
| Dexterity | 54 |
| Strength | 66 |
| Wisdom | 54 |
| Will | 22 |
| Leadership | 0 |
| Marksmanship | 33 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 0 |

**Биография (RU):** Жуан Домингос состоял в ангольской дружине, где одна встреча с минами заменила ему все последующие уроки храбрости. Он идёт медленно, внимательно смотрит под ноги и никогда не смеётся над чужой осторожностью. В ладони Жуан часто перекатывает гладкий болт от той самой разбитой телеги, напоминая себе не спешить. Скрытая угроза сковывает его, тогда как перед видимой он остаётся упрямым и прямым.

**Biography (EN):** One mine-struck cart was enough to shape João Domingos's years in an Angolan local watch. Loose earth slows him at once, and he refuses to disguise caution as some grand tactical instinct. A smooth iron bolt recovered from the wreck rolls between his fingers whenever a road feels wrong. Hidden danger can hold João back, but a threat he can see receives the full weight of a stubborn, unsentimental man.

**Профиль (RU):** Осторожный дружинник с болтом от разбитой телеги

**Profile (EN):** A wary guardsman carrying a bolt from a shattered cart

### `JAZZ_AME_17` — Wanjiku Mwangi

- **Nationality:** `Kenya`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $12
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Personality:** —
- **Voice:** `Jazz_AME_Female` → VR `Jazz_AME_Female`
- **Appearance:** `JAZZ_AME_17` ← donor `MilitiaRookie_Female_01` (female; blue recolor, source не править)
- **Inventory (fixed):** DoubleBarrelShotgun · 12g×4 · Knife

| Stat | |
| --- | ---: |
| Health | 82 |
| Agility | 66 |
| Dexterity | 64 |
| Strength | 52 |
| Wisdom | 70 |
| Will | 26 |
| Leadership | 0 |
| Marksmanship | 47 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 0 |

**Биография (RU):** Там, где кенийский лес подходил к полям, Ванджику Мванги носила воду егерю и часами дежурила на опушке. Она не тратит слов на обещания и легко проходит по тропе, которая у других отнимает дыхание. К веткам Ванджику привязывает короткие синие нитки, чтобы на обратном пути проверить, что изменил ветер. Тяжёлая работа быстро выдаёт её тонкие плечи, но наблюдение она редко бросает раньше срока.

**Biography (EN):** Blue threads tied to low branches tell Wanjiku Mwangi what the wind changed while she was away. A Kenyan ranger taught her fieldcraft through water runs, tracks, and long hours at the silent edge of a clearing. She is light on rough ground and sparing with conversation around boastful strangers. Heavy burdens expose her slight frame, yet Wanjiku holds a watch long after louder people grow restless.

**Профиль (RU):** Тихая егерь, оставляющая ветру синие нитки

**Profile (EN):** A quiet scout who leaves blue threads for the wind

### `JAZZ_AME_18` — Serge Kouassi

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $18
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_18` ← donor `Demolitions_Rebels` (male; blue recolor, source не править)
- **Inventory (fixed):** — (empty hands)

| Stat | |
| --- | ---: |
| Health | 86 |
| Agility | 60 |
| Dexterity | 58 |
| Strength | 58 |
| Wisdom | 72 |
| Will | 29 |
| Leadership | 5 |
| Marksmanship | 30 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 0 |

**Биография (RU):** Над гаражом отца в Гранд-Шьен Серж Куасси с детства раздражал его отказом брать отвёртку правильно. С железом Серж спорит до сих пор, а несходящееся чужое объяснение замечает почти сразу. Он носит промасленный блокнот из мастерской и записывает туда не детали, а вопросы. Пустые руки его смущают меньше, чем пустая голова, хотя на деле одной догадки часто недостаточно.

**Biography (EN):** Questions rather than repair figures fill the grease-stained shop notebook in Serge Kouassi's pocket. He grew up above his father's Grand Chien garage, surrounded by tools he never learned to love. Practical work makes Serge's hands fumble, while contradictions in a story catch him immediately. He believes thought can open doors that muscle cannot and sometimes forgets that a good idea still needs someone to turn the handle.

**Профиль (RU):** Сын механика, записывающий вопросы вместо схем

**Profile (EN):** A mechanic's son who records questions instead of diagrams

### `JAZZ_AME_19` — Bongani Dlamini

- **Nationality:** `SouthAfrica`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $25
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_19` ← donor `LegionMedic` (male; blue recolor, source не править)
- **Inventory (fixed):** ColtM1917 · .45×12 · Knife

| Stat | |
| --- | ---: |
| Health | 94 |
| Agility | 54 |
| Dexterity | 52 |
| Strength | 80 |
| Wisdom | 50 |
| Will | 30 |
| Leadership | 10 |
| Marksmanship | 43 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 0 |

**Биография (RU):** Между сменами в южноафриканском шахтёрском посёлке Бонгани Дламини сторожил ворота, переносил мешки и спал короткими кусками. Он тяжёл на подъём, молчалив и совершенно не заинтересован в том, чтобы выглядеть проворнее. Обед Бонгани носит в вмятой жестяной коробке, которая пережила больше падений, чем её хозяин готов обсудить. Когда нужно долго держать дверь или не уступать тесный проход, его медлительность внезапно перестаёт быть недостатком.

**Biography (EN):** A dented tin lunch box has survived every fall Bongani Dlamini declines to discuss. It accompanied years of guarding a South African mining compound, carrying sacks by day and stealing sleep between alarms. Bongani rises slowly, speaks rarely, and sees no virtue in hurrying merely to impress someone. He will never be first around a corner, but once his bulk settles into a doorway, moving him becomes everybody else's problem.

**Профиль (RU):** Шахтёрский сторож с вмятой коробкой и тяжёлым шагом

**Profile (EN):** A mining guard with a dented lunch tin and heavy tread

### `JAZZ_AME_20` — Idrissa Bah

- **Nationality:** `Senegal`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $32
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Personality:** —
- **Voice:** `PierreMerc` → VR `PierreMerc`
- **Appearance:** `JAZZ_AME_20` ← donor `LegionSharpShooter_alt` (male; blue recolor, source не править)
- **Inventory (fixed):** SWModel10 · .38×6 · Knife

| Stat | |
| --- | ---: |
| Health | 85 |
| Agility | 60 |
| Dexterity | 60 |
| Strength | 54 |
| Wisdom | 64 |
| Will | 28 |
| Leadership | 8 |
| Marksmanship | 45 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 8 |

**Биография (RU):** На сенегальском перекрёстке Идрисса Бах мог одним жестом распутать движение, которое уже считало себя безнадёжным. Перестрелка лишает его уюта; видимый порядок возвращает самообладание. Идрисса сам стирает белые перчатки по воскресеньям и сушит их на спинке единственного стула. Люди не всегда слышат его с первого раза, но руки у него говорят достаточно ясно, чтобы хаос сделал короткую паузу.

**Biography (EN):** White gloves dry over the back of Idrissa Bah's only chair every Sunday. They once conducted Senegalese traffic with more success than he ever found on a firing line. Confusion unsettles Idrissa until he can give it lanes, turns, and a place to stop. He is no hero of sudden violence, but a crowd often borrows its first calm moment from his precise gestures.

**Профиль (RU):** Белые перчатки и жест, на миг останавливающий хаос

**Profile (EN):** White gloves and a gesture that briefly stills chaos

## Fighters

### `JAZZ_AME_21` — Omar Diallo

- **Nationality:** `Senegal`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $81
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Personality:** `Pessimist`
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_21` ← donor `LegionGunner` (male; blue recolor, source не править)
- **Inventory (fixed):** Winchester1894 · .44×40 · Knife

| Stat | |
| --- | ---: |
| Health | 78 |
| Agility | 66 |
| Dexterity | 66 |
| Strength | 60 |
| Wisdom | 58 |
| Will | 30 |
| Leadership | 8 |
| Marksmanship | 56 |
| Mechanical | 0 |
| Explosives | 5 |
| Medical | 8 |

**Биография (RU):** Из сенегальской части Омар Диалло ушёл, когда понял, что очередной приказ заведёт его людей туда, откуда их не собираются возвращать. Теперь он говорит мало и долго выбирает момент, прежде чем приложить к плечу старый винчестер. После каждого выхода Омар ставит карандашную черту на внутренней стороне патронной коробки, считая не победы, а потраченные выстрелы. Решительность приходит к нему не сразу; принятое решение Омар уже не украшает словами.

**Biography (EN):** Pencil marks cover the inside of Omar Diallo's cartridge box, accounting for rounds that did not return. He deserted a Senegalese unit after an order treated lives as replaceable supplies. Omar keeps his distance from uniforms now and speaks only after watching a room settle. The path forward can make him hesitate, but once the rifle reaches his shoulder he wastes neither motion nor breath.

**Профиль (RU):** Дезертир, считающий каждый выстрел карандашной чертой

**Profile (EN):** A deserter who accounts for every shot in pencil

### `JAZZ_AME_22` — Bastien Lafontaine

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Fighters / Autorifleman
- **Specialization:** `Autoriflemen`
- **Level / Salary:** 1 / $92
- **Potential (Wisdom):** Medium
- **Traits (common):** `AutoWeapons`
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_22` ← donor `Heavy_Rebels_02` (male; blue recolor, source не править)
- **Inventory (fixed):** STG44 · 7.92Kurz×60 · Knife

| Stat | |
| --- | ---: |
| Health | 76 |
| Agility | 64 |
| Dexterity | 64 |
| Strength | 58 |
| Wisdom | 52 |
| Will | 28 |
| Leadership | 5 |
| Marksmanship | 54 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 5 |

**Биография (RU):** Машинное масло и дешёвый табак выдают Бастьена Лафонтена раньше, чем он успевает заговорить. В местной милиции Гранд-Шьен ему чаще встречались тесные улицы, чем открытое поле. Самокрутку Бастьен заворачивает в промасленную тряпицу, курит только после работы и сердится, если кто-то без спроса трогает его оружие. Красивого ракурса он не ищет — минуту, когда узкий проход нужно наполнить шумом, чувствует и без красоты.

**Biography (EN):** Bastien Lafontaine learned his trade with a Grand Chien militia, covering alleys where walls seemed to close in during trouble. Cheap tobacco stains his fingers, but he saves the cigarette until everything has gone quiet. A rolling paper stays folded inside the oil rag he uses on his rifle, a private promise of rest. Bastien is not imaginative under changing orders, yet in a confined street his steady bursts arrive exactly where companions expect them.

**Профиль (RU):** Масло, дешёвый табак и спокойствие тесных улиц

**Profile (EN):** Gun oil, cheap tobacco, and composure in narrow streets

### `JAZZ_AME_23` — Chukwuemeka "Emeka" Obi

- **Nationality:** `Nigeria`
- **Category / CombatRole:** Fighters / Machinegunner
- **Specialization:** `HeavyWeapons`
- **Level / Salary:** 1 / $101
- **Potential (Wisdom):** Medium
- **Traits (common):** `HeavyWeaponsTraining`, `AutoWeapons`
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_23` ← donor `LegionGunner_alt` (male; blue recolor, source не править)
- **Inventory (fixed):** MAC2429 · 7.5French×60 · Knife · Bandage×1

| Stat | |
| --- | ---: |
| Health | 88 |
| Agility | 58 |
| Dexterity | 56 |
| Strength | 78 |
| Wisdom | 46 |
| Will | 32 |
| Leadership | 0 |
| Marksmanship | 48 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 0 |

**Биография (RU):** Однажды утром от нигерийского блокпоста Чуквуэмеки «Эмеки» Оби не осталось ничего, кроме мешков и пыли. До этого он месяцами держал там пулемётную точку, а теперь шутит, что земля — единственная мишень, которая не уклоняется. Чай Эмека пьёт из банки с вмятиной от осколка и не разрешает её выпрямлять. Отдельную цель он ведёт неровно; под долгим грохотом Эмеки целый участок земли быстро пустеет.

**Biography (EN):** Tea comes from Chukwuemeka “Emeka” Obi's shrapnel-dented tin cup, which nobody is allowed to repair. The dent outlived a Nigerian checkpoint erased after months behind its machine gun. Built for weight rather than delicacy, Emeka laughs first when a careful shot goes astray. He may not pick one point from the landscape elegantly, but knows how to make an entire stretch of ground feel unwelcoming.

**Профиль (RU):** Тяжёлый ствол и осколочная вмятина на кружке

**Profile (EN):** A checkpoint survivor with a shrapnel dent in his cup

### `JAZZ_AME_24` — Michel Kabeya

- **Nationality:** `Congo`
- **Category / CombatRole:** Fighters / Grenadier
- **Specialization:** `HeavyWeapons`
- **Level / Salary:** 1 / $95
- **Potential (Wisdom):** Medium
- **Traits (common):** `Throwing`
- **Personality:** —
- **Voice:** `IMP_male_03` → VR `IMP_male_01`
- **Appearance:** `JAZZ_AME_24` ← donor `Marksman_Rebels` (male; blue recolor, source не править)
- **Inventory (fixed):** Colt1911 · .45×24 · FragGrenade×2 · Knife · Bandage×1

| Stat | |
| --- | ---: |
| Health | 80 |
| Agility | 66 |
| Dexterity | 66 |
| Strength | 62 |
| Wisdom | 54 |
| Will | 26 |
| Leadership | 5 |
| Marksmanship | 56 |
| Mechanical | 0 |
| Explosives | 12 |
| Medical | 5 |

**Биография (RU):** Пустые банки Мишель Кабейа забрасывал в щели между ящиками, развлекая смену на речной пристани в Конго. Позже оказалось, что тот же глазомер полезен для предметов, которые лучше не возвращать обратно. В баре Мишель шумен, но перед броском всегда замолкает и касается большим пальцем медного кольца на чеке. Он двигается охотно, хотя близость собственного взрыва уважает сильнее, чем показывает друзьям.

**Biography (EN):** Michel Kabeya once unloaded riverboats in Congo, betting his lunch on whether a dented can would land inside a distant crate. The game eventually became a practical occupation involving objects no one wanted thrown back. He is loud over drinks and utterly silent before a toss, rubbing a copper pull ring threaded onto his belt. Michel trusts his arm, but never lingers to admire the place where its delivery comes down.

**Профиль (RU):** Речной грузчик, превративший бросок жестянки в ремесло

**Profile (EN):** A river hand who made an art of thrown tin

### `JAZZ_AME_25` — Juma Otieno

- **Nationality:** `Kenya`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $66
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_25` ← donor `LegionSniper` (male; blue recolor, source не править)
- **Inventory (fixed):** Winchester1894 · .44×28 · Knife · Bandage×1

| Stat | |
| --- | ---: |
| Health | 72 |
| Agility | 70 |
| Dexterity | 68 |
| Strength | 50 |
| Wisdom | 60 |
| Will | 30 |
| Leadership | 8 |
| Marksmanship | 60 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 8 |

**Биография (RU):** На кенийской границе Джума Отиено научился читать пыль, которая появлялась раньше машин и часто была единственным предупреждением. Он привык быстро менять место и не обижается на приказ не изображать героя. Перед выходом Джума завязывает на лице выцветший клетчатый платок, сохранивший запах дорожного мыла. Тяжёлая ноша утомляет его быстрее долгого пути, а первым увидеть движение на горизонте для Джумы почти личная обязанность.

**Biography (EN):** A faded checked scarf covers Juma Otieno's mouth on the road, still faintly scented with his sister's soap. It crossed a Kenyan border where dust announced company before an engine arrived. Juma learned to relocate before a position became a trap and has little patience for theatrical last stands. Weight tires him quickly, but open ground sharpens his attention and seems to quicken every choice.

**Профиль (RU):** Пограничник в выцветшем платке, читающий дорожную пыль

**Profile (EN):** A border runner who reads the dust through a faded scarf

### `JAZZ_AME_26` — Andile Nkosi

- **Nationality:** `SouthAfrica`
- **Category / CombatRole:** Fighters / Autorifleman
- **Specialization:** `Autoriflemen`
- **Level / Salary:** 1 / $87
- **Potential (Wisdom):** Medium
- **Traits (common):** `AutoWeapons`
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_26` ← donor `Marksman_Rebels_03` (male; blue recolor, source не править)
- **Inventory (fixed):** STG44 · 7.92Kurz×60 · Knife

| Stat | |
| --- | ---: |
| Health | 78 |
| Agility | 64 |
| Dexterity | 64 |
| Strength | 60 |
| Wisdom | 50 |
| Will | 28 |
| Leadership | 8 |
| Marksmanship | 54 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 5 |

**Биография (RU):** Конвои Южной Африки научили Андиле Нкоси отвечать на засаду, не превращая груз за спиной в решето. Он спокоен, немногословен и раздражается, когда новички берут его оружие просто из любопытства. На ремне Андиле закреплена полоска синей изоленты с номером первой машины, которую он довёл целой. Неожиданные перемены сбивают его ритм; знакомая последовательность возвращает короткую и бережную пальбу.

**Biography (EN):** Blue electrical tape around Andile Nkosi's sling bears the plate number of the first truck he brought through untouched. South African convoy work taught him that careless fire could ruin cargo before an attacker reached it. Andile prefers routine, short instructions, and people who keep their hands to themselves. Sudden improvisation can leave him behind, but a revealed pattern brings disciplined restraint back to his weapon.

**Профиль (RU):** Конвойный стрелок с синей лентой первой спасённой машины

**Profile (EN):** A convoy guard marked by one safely delivered truck

### `JAZZ_AME_27` — Sekou Camara

- **Nationality:** `Mali`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $60
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_27` ← donor `Medic_Rebels` (male; blue recolor, source не править)
- **Inventory (fixed):** M3GreaseGun · .45×60 · Knife

| Stat | |
| --- | ---: |
| Health | 74 |
| Agility | 70 |
| Dexterity | 66 |
| Strength | 52 |
| Wisdom | 56 |
| Will | 35 |
| Leadership | 10 |
| Marksmanship | 56 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 5 |

**Биография (RU):** В малийской пустыне Секу Камара рано понял, что неподвижная фигура на светлом фоне долго не живёт. Он постоянно смещается, выбирает низины и терпеть не может ждать на месте только ради чужой важности. Компас Секу треснул много лет назад, но стрелка всё ещё находит север, если постучать по стеклу ногтем. Короткое оружие не прощает дальних амбиций, и Секу отвечает на это ногами, уносящими его вперёд тяжёлых товарищей.

**Biography (EN):** A cracked compass needs one sharp tap from Sekou Camara before its needle remembers north. He carried it while patrolling the Malian desert, where an upright man against a pale horizon becomes everyone's landmark. Restlessness serves Sekou in open country and irritates patient companions. He lacks reach for distant contests, but crosses exposed ground fast enough to give slower people room to breathe.

**Профиль (RU):** Пустынный патрульный с треснувшим, но верным компасом

**Profile (EN):** A desert patrolman guided by a cracked but faithful compass

### `JAZZ_AME_28` — Pascal Ngoma

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Fighters / Machinegunner
- **Specialization:** `HeavyWeapons`
- **Level / Salary:** 1 / $104
- **Potential (Wisdom):** Medium
- **Traits (common):** `HeavyWeaponsTraining`
- **Personality:** —
- **Voice:** `PierreMerc` → VR `PierreMerc`
- **Appearance:** `JAZZ_AME_28` ← donor `LegionMedic_alt` (male; blue recolor, source не править)
- **Inventory (fixed):** BAR · .30-06×60 · Knife · Bandage×1

| Stat | |
| --- | ---: |
| Health | 86 |
| Agility | 56 |
| Dexterity | 58 |
| Strength | 74 |
| Wisdom | 46 |
| Will | 30 |
| Leadership | 5 |
| Marksmanship | 50 |
| Mechanical | 0 |
| Explosives | 5 |
| Medical | 0 |

**Биография (RU):** Месяцы на огневой точке в Гранд-Шьен приучили Паскаля Нгому любить места, откуда не нужно никуда бежать. Он упрям, тяжёл и воспринимает движение скорее как уступку обстоятельствам. Под вещами Паскаля всегда привязан крошечный складной табурет, вызывающий смех ровно до первой долгой ночи. Плана он быстро не меняет, и вокруг выбранной позиции постепенно становится тихо.

**Biography (EN):** A ridiculous folding stool appears beneath Pascal Ngoma whenever waiting stretches past an hour. Grand Chien gun posts taught him to regard running as evidence of poor planning. Pascal is stubborn, durable, and happiest when a patch of ground becomes clearly his responsibility. New directions reach him slowly, but incoming noise rarely persuades him to leave the old one.

**Профиль (RU):** Упрямый хозяин позиции с крошечным складным табуретом

**Profile (EN):** A stubborn position keeper with a tiny folding stool

### `JAZZ_AME_29` — Kwesi Boateng

- **Nationality:** `Ghana`
- **Category / CombatRole:** Fighters / Grenadier
- **Specialization:** `HeavyWeapons`
- **Level / Salary:** 1 / $98
- **Potential (Wisdom):** Medium
- **Traits (common):** `Throwing`, `HeavyWeaponsTraining`
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_29` ← donor `Medic_Rebels_03` (male; blue recolor, source не править)
- **Inventory (fixed):** PPS43 · 7.62x25×70 · FragGrenade×2 · Knife · Bandage×1

| Stat | |
| --- | ---: |
| Health | 78 |
| Agility | 62 |
| Dexterity | 64 |
| Strength | 66 |
| Wisdom | 50 |
| Will | 24 |
| Leadership | 0 |
| Marksmanship | 50 |
| Mechanical | 5 |
| Explosives | 12 |
| Medical | 0 |

**Биография (RU):** За ганским складом Квеси Боатенг после смены часами бросал пустые бутылки в меловой круг на стене. Эта забава сделала его уверенным с предметами, которые звенят куда опаснее стекла. Квеси собирает крышки в табачную коробку и встряхивает её перед выходом, проверяя спокойствие руки. Он действует быстро и улыбается редко, а после громкого результата предпочитает уже быть в другом месте.

**Biography (EN):** Bottle caps fill Kwesi Boateng's old tobacco tin, shaken before work to hear whether his hand is steady. The habit began behind a Ghanaian warehouse, where he aimed empty bottles at a chalk circle after every shift. Heavier objects with shorter fuses eventually replaced the glass. Kwesi commits quickly but dislikes the seconds after impact, when the echo seems to search for whoever caused it.

**Профиль (RU):** Бросок в меловой круг и крышки в табачной коробке

**Profile (EN):** A chalk target and bottle caps rattling in a tobacco tin

### `JAZZ_AME_30` — Tesfaye Alemu

- **Nationality:** `Ethiopia`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $75
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_30` ← donor `Recon_Rebels` (male; blue recolor, source не править)
- **Inventory (fixed):** M1897 · 12g×20 · Knife

| Stat | |
| --- | ---: |
| Health | 70 |
| Agility | 68 |
| Dexterity | 66 |
| Strength | 48 |
| Wisdom | 62 |
| Will | 28 |
| Leadership | 5 |
| Marksmanship | 58 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 5 |

**Биография (RU):** В эфиопских горах Тесфайе Алему научился успокаивать дыхание раньше, чем получил оружие, достойное этого умения. Он худощав, терпелив и без зависти принимает то, что оказалось под рукой. Перед выстрелом Тесфайе сжимает гладкий серый камень, когда-то поднятый у дома, а затем убирает его в карман. Долгая драка быстро его истощает; первый спокойный миг почти никогда не пропадает зря.

**Biography (EN):** A smooth grey stone from his Ethiopian home valley rests in Tesfaye Alemu's palm, then disappears before the shot. There he learned that a hurried breath could carry farther than a footstep. Better rifles always belonged to somebody else, a fact Tesfaye accepts without bitterness. He is not made for prolonged punishment, but patience often lets him finish before endurance becomes the question.

**Профиль (RU):** Горный стрелок, успокаивающий дыхание серым камнем

**Profile (EN):** A highland shooter who steadies himself with a grey stone

### `JAZZ_AME_31` — Rafael dos Santos

- **Nationality:** `Angola`
- **Category / CombatRole:** Fighters / Autorifleman
- **Specialization:** `Autoriflemen`
- **Level / Salary:** 1 / $89
- **Potential (Wisdom):** Medium
- **Traits (common):** `AutoWeapons`
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_31` ← donor `LegionScout_alt_2` (male; blue recolor, source не править)
- **Inventory (fixed):** STG44 · 7.92Kurz×60 · Knife

| Stat | |
| --- | ---: |
| Health | 80 |
| Agility | 64 |
| Dexterity | 64 |
| Strength | 62 |
| Wisdom | 48 |
| Will | 30 |
| Leadership | 5 |
| Marksmanship | 54 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 5 |

**Биография (RU):** На ангольских дорогах Рафаэль дос Сантос сопровождал рабочие бригады и осваивал каждое новое дело медленнее тех, кто любил давать советы. Он не спорил, а повторял движение до тех пор, пока оно не становилось привычкой. Вокруг запястья Рафаэля намотан запасной шнурок, потому что однажды порванный ботинок задержал всю колонну. Внезапная выдумка ему чужда; трезвость, порядок и обещание остаться после тяжёлого дня — нет.

**Biography (EN):** A spare bootlace circles Rafael dos Santos's wrist, recalling the day a broken boot delayed an entire column. Angolan road crews rarely saw him understand a new drill before anyone else. Rather than pretend, Rafael repeated the motion until it belonged to him. Sudden changes make him rigid, but fatigue and dust do little to loosen a promise he has already made.

**Профиль (RU):** Упрямый ученик со шнурком на запястье

**Profile (EN):** A persistent learner with a spare bootlace around his wrist

### `JAZZ_AME_32` — Awa Sow

- **Nationality:** `Senegal`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $57
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Personality:** `Stealthy`
- **Voice:** `IMP_female_02` → VR `IMP_female_01`
- **Appearance:** `JAZZ_AME_32` ← donor `MilitiaRookie_Female_02` (female; blue recolor, source не править)
- **Inventory (fixed):** PPSH · 7.62x25×70 · Knife · Bandage×1

| Stat | |
| --- | ---: |
| Health | 72 |
| Agility | 68 |
| Dexterity | 68 |
| Strength | 50 |
| Wisdom | 54 |
| Will | 22 |
| Leadership | 0 |
| Marksmanship | 58 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 5 |

**Биография (RU):** Ночные смены на сенегальской пристани научили Аву Соу встречать неприятности в узких коридорах почти вплотную. Она быстра, колка и слишком хорошо слышит каждый неожиданный скрип за дверью. От старого склада у Авы остался погнутый ключ, которым она постукивает по бедру, когда кто-то начинает поучать её снисходительным тоном. Долгая пальба расшатывает ей нервы; теснота позволяет исчезнуть с чужой линии прежде, чем там станет опасно.

**Biography (EN):** The bent key to Awa Sow's vanished dockside job taps against her thigh whenever someone explains her own work to her. Its Senegalese storehouse had passages too narrow for grand gestures. Awa learned to slip around trouble quickly without enjoying the sound of its arrival. Sustained noise wears at her composure, but close walls give that speed somewhere useful to go.

**Профиль (RU):** Быстрый шаг, погнутый ключ и нетерпение к поучениям

**Profile (EN):** Quick feet, a bent key, and no patience for lectures

### `JAZZ_AME_33` — Claude Mvemba

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $69
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_33` ← donor `Recon_Rebels_03` (male; blue recolor, source не править)
- **Inventory (fixed):** Auto5 · 12g×20 · Knife

| Stat | |
| --- | ---: |
| Health | 78 |
| Agility | 66 |
| Dexterity | 66 |
| Strength | 58 |
| Wisdom | 56 |
| Will | 28 |
| Leadership | 10 |
| Marksmanship | 56 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 8 |

**Биография (RU):** Среди плантаций Гранд-Шьен Клод Мвемба привык решать споры на расстоянии, удобном для дробовика. Он говорит мало, курит много и считает лишний шаг навстречу таким же расточительством, как лишнее слово. Серебристый портсигар Клода давно смят каблуком, но закрывается с приятным щелчком. Открытый простор лишает его уверенности; изгороди и сараи возвращают безошибочное чувство дистанции.

**Biography (EN):** A crushed silver-coloured cigarette case still shuts for Claude Mvemba with a satisfying click, though opening it needs a thumbnail. Grand Chien plantation work taught him to let most trouble come closer to the shotgun. Conversation bores Claude; cigarettes do not. Distant contests hold little appeal, but among sheds, fences, and cane he judges space with the ease of long habit.

**Профиль (RU):** Молчаливый сторож со смятым портсигаром и дробовиком

**Profile (EN):** A taciturn guard with a crushed cigarette case

### `JAZZ_AME_34` — Emeka Nwosu

- **Nationality:** `Nigeria`
- **Category / CombatRole:** Fighters / Machinegunner
- **Specialization:** `HeavyWeapons`
- **Level / Salary:** 1 / $107
- **Potential (Wisdom):** Low
- **Traits (common):** `HeavyWeaponsTraining`, `AutoWeapons`
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_34` ← donor `LegionManiac` (male; blue recolor, source не править)
- **Inventory (fixed):** MAC2429 · 7.5French×60 · Knife · Bandage×1

| Stat | |
| --- | ---: |
| Health | 90 |
| Agility | 56 |
| Dexterity | 54 |
| Strength | 80 |
| Wisdom | 44 |
| Will | 34 |
| Leadership | 5 |
| Marksmanship | 48 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 0 |

**Биография (RU):** Груз в нигерийском порту привёл Эмеку Нвосу к пулемёту: никто другой не хотел носить его достаточно долго. Он силён, упрям и не обижается на шутку, если успел рассказать её первым. Пустую патронную коробку Эмека использует как стул и подписал снизу: «не сдвигать вместе с хозяином». Тонкая работа ему чужда, тогда как тяжесть и долгий шум кажутся естественным продолжением самого Эмеки.

**Biography (EN):** An empty ammunition box serves as Emeka Nwosu's chair and carries the label, “Do not relocate with owner.” Nigerian quay work first revealed that he could carry a machine gun farther than anyone else. Finesse never followed, but good humour did whenever the joke concerns his immovable size. Emeka struggles with delicate choices at distance, yet weight, recoil, and stubborn ground suit him perfectly.

**Профиль (RU):** Портовый силач на собственной патронной коробке

**Profile (EN):** A dockside strongman seated on his own ammunition box

### `JAZZ_AME_35` — Samuel Cheruiyot

- **Nationality:** `Kenya`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $78
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_35` ← donor `Soldier_Rebels_02` (male; blue recolor, source не править)
- **Inventory (fixed):** Winchester1894 · .44×28 · Knife

| Stat | |
| --- | ---: |
| Health | 76 |
| Agility | 68 |
| Dexterity | 66 |
| Strength | 54 |
| Wisdom | 58 |
| Will | 26 |
| Leadership | 8 |
| Marksmanship | 58 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 5 |

**Биография (RU):** Задолго до строевых слов Сэмюэл Черуйот выучил охотничьи тропы Кении. В лесу он лёгок, внимателен и предпочитает сделать паузу, а не исправлять поспешность новым выстрелом. На ремне его винчестера пришита пуговица из полированного рога, оставшаяся от первой куртки. Казарменная теснота делает Сэмюэла раздражительным; открытый воздух словно заранее подсказывает ему, откуда появится движение.

**Biography (EN):** A polished horn button from Samuel Cheruiyot's first hunting coat is sewn into his rifle sling. Kenyan trails taught him long before regulations or military vocabulary arrived. Outdoors Samuel is quick and watchful, taking the extra breath that impatient shooters resent. Barracks make him restless and sharp-tongued, but a horizon seems to reveal movement before everyone else has decided where to look.

**Профиль (RU):** Охотник, пришивший к ремню память о первой куртке

**Profile (EN):** A hunter carrying his first coat's button on the sling

### `JAZZ_AME_36` — Mamadou Traoré

- **Nationality:** `Mali`
- **Category / CombatRole:** Fighters / Autorifleman
- **Specialization:** `Autoriflemen`
- **Level / Salary:** 1 / $84
- **Potential (Wisdom):** Medium
- **Traits (common):** `AutoWeapons`
- **Personality:** —
- **Voice:** `PierreMerc` → VR `PierreMerc`
- **Appearance:** `JAZZ_AME_36` ← donor `Soldier_Rebels_03` (male; blue recolor, source не править)
- **Inventory (fixed):** STG44 · 7.92Kurz×60 · Knife · Wirecutter

| Stat | |
| --- | ---: |
| Health | 78 |
| Agility | 64 |
| Dexterity | 62 |
| Strength | 58 |
| Wisdom | 52 |
| Will | 28 |
| Leadership | 5 |
| Marksmanship | 54 |
| Mechanical | 15 |
| Explosives | 0 |
| Medical | 5 |

**Биография (RU):** После смен в малийском дорожном патруле Мамаду Траоре разбирал соседские стволы, пока остальные спорили о вчерашней стрельбе. Он не мастер, но терпеливо запоминает, какая пружина куда возвращается, и редко выдаёт догадку за знание. Чужая отвёртка, обмотанная красной тканью, всегда лежит у него рядом с кусачками. Ремонт Мамаду схватывает не мгновенно, но простая неисправность после него обычно перестаёт повторяться.

**Biography (EN):** A mismatched screwdriver wrapped in red cloth shares Mamadou Traoré's pocket with a wire cutter. He began tending other men's weapons during quiet hours on a Malian road patrol. No gifted engineer, Mamadou simply remembers which small part caused trouble last time. Machinery yields to repetition rather than insight for him, but uncomplicated faults tend to stay fixed once his careful hands have visited.

**Профиль (RU):** Патрульный с чужой отвёрткой в красной ткани

**Profile (EN):** A patrolman with a borrowed screwdriver wrapped in red cloth

### `JAZZ_AME_37` — Felix Tshisekedi

- **Nationality:** `Congo`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $63
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_37` ← donor `LegionManiac_alt` (male; blue recolor, source не править)
- **Inventory (fixed):** Auto5 · 12g×16 · Knife · Bandage×2

| Stat | |
| --- | ---: |
| Health | 80 |
| Agility | 66 |
| Dexterity | 64 |
| Strength | 56 |
| Wisdom | 56 |
| Will | 30 |
| Leadership | 8 |
| Marksmanship | 56 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 12 |

**Биография (RU):** На конголезском блокпосту Феликс Чисекеди привык, что одна смена редко оставляет другой воду, бинты или внятные объяснения. Он закрывает чужие мелкие промахи без жалоб и не считает это подвигом. В кармане Феликс носит обмылок в жестяной крышке, чтобы после перевязки руки не пахли железом. Ничем Феликс не блистает, и всё же в плохой день о нём не приходится тревожиться отдельно.

**Biography (EN):** A sliver of soap rides in Felix Tshisekedi's tin lid to scrub the iron smell from his hands. Congolese checkpoint shifts taught him to inherit empty canteens and unfinished chores without complaint. Felix tied the bandage, watched the road, and requested explanations later. He offers no remarkable flourish, but difficult days improve simply because he does not become another problem to solve.

**Профиль (RU):** Надёжный человек блокпоста с обмылком в жестяной крышке

**Profile (EN):** A dependable checkpoint hand carrying soap in a tin lid

### `JAZZ_AME_38` — Noah van Wyk

- **Nationality:** `SouthAfrica`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $72
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Personality:** `Optimist`
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_38` ← donor `Stormer_Rebels` (male; blue recolor, source не править)
- **Inventory (fixed):** Winchester1894 · .44×28 · Knife

| Stat | |
| --- | ---: |
| Health | 82 |
| Agility | 64 |
| Dexterity | 64 |
| Strength | 64 |
| Wisdom | 54 |
| Will | 32 |
| Leadership | 50 |
| Marksmanship | 56 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 5 |

**Биография (RU):** Соседи по южноафриканской ферме приносили Ноа ван Вику споры о воде и заблудившемся скоте. Он не повышает голос и не торопит ответ, поэтому даже старшие часто замолкают, когда Ноа начинает говорить. В карманном журнале рядом с датами посева он записывает обещания, данные людям. Стреляет он без показного блеска, но рядом с его спокойным порядком усталые товарищи реже делают глупости.

**Biography (EN):** A pocket ledger mixes Noah van Wyk's planting dates with promises made to people, every fulfilled one neatly crossed through. South African neighbours once brought him quarrels about water, fences, and wandering cattle. Noah speaks without hurry, leaving silence to push where louder men would shout. He is capable rather than dazzling with a rifle, but tired companions often recover their sense when his plain voice gives the next step.

**Профиль (RU):** Фермерский голос, которому доверяют воду, скот и обещания

**Profile (EN):** A farmer's voice trusted with water, cattle, and promises

## Hardened

### `JAZZ_AME_39` — Joseph "Hyena" Mukendi

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Hardened / Autorifleman
- **Specialization:** `Autoriflemen`
- **Level / Salary:** 1 / $127
- **Potential (Wisdom):** Low
- **Traits (common):** `AutoWeapons`, `CQCTraining`
- **Personality:** `Psycho`
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_39` ← donor `GrandChien_Artillery` (male; blue recolor, source не править)
- **Inventory (fixed):** Thompson · .45×60 · Knife · FragGrenade×1 · Bandage×1

| Stat | |
| --- | ---: |
| Health | 84 |
| Agility | 70 |
| Dexterity | 68 |
| Strength | 72 |
| Wisdom | 44 |
| Will | 55 |
| Leadership | 12 |
| Marksmanship | 54 |
| Mechanical | 0 |
| Explosives | 10 |
| Medical | 8 |

**Биография (RU):** В Гранд-Шьен противники Жозефа Мукенди сперва слышали смешок и лишь потом видели лицо, так за ним закрепилась кличка «Гиена». В тесном месте он действует быстро, грязно и без интереса к красивым правилам. Жозеф носит помятое карманное зеркальце и проверяет им дверные углы, прежде чем сунуться вперёд. Его решительность спасает чаще, чем осторожность, но иногда эти два слова он явно путает.

**Biography (EN):** A dented pocket mirror lets Joseph “Hyena” Mukendi inspect a doorway without offering it his head. Grand Chien survivors remembered his ambush laugh before they remembered the face. Joseph fights with quick, practical cruelty and considers elegance a luxury for safer rooms. Nerve carries him through ugly moments, though his appetite for nearness can place him where a wiser man would never go.

**Профиль (RU):** «Гиена» с карманным зеркалом для самых тесных дверей

**Profile (EN):** Hyena and his pocket mirror for dangerously close doors

### `JAZZ_AME_40` — Abraham Tekle

- **Nationality:** `Ethiopia`
- **Category / CombatRole:** Hardened / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $111
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Personality:** —
- **Voice:** `IMP_male_01` → VR `IMP_male_01`
- **Appearance:** `JAZZ_AME_40` ← donor `LegionGrenadir_alt` (male; blue recolor, source не править)
- **Inventory (fixed):** Mini14 · 5.56×40 · Knife · Bandage×1

| Stat | |
| --- | ---: |
| Health | 80 |
| Agility | 70 |
| Dexterity | 70 |
| Strength | 70 |
| Wisdom | 50 |
| Will | 52 |
| Leadership | 10 |
| Marksmanship | 60 |
| Mechanical | 5 |
| Explosives | 8 |
| Medical | 5 |

**Биография (RU):** Об отступлении из эфиопских гор Абрахам Текле и его бывшие товарищи до сих пор говорят только дома. Он дышит ровно, не торопит выстрел и принимает поражение как урок, а не личное оскорбление. На ночлеге Абрахам сворачивает старую шерстяную шапку в маленькую подушку, хотя давно может позволить себе лучшую. Лицо кажется усталым, но тело и привычки сохранили больше прочности, чем обещает первый взгляд.

**Biography (EN):** A faded wool cap becomes Abraham Tekle's tiny pillow every night, a comfort kept from colder bivouacs. It followed an Ethiopian mountain campaign that ended with more men walking home than marching. Defeat made Abraham quieter rather than bitter, and he waits for a clear sight instead of demanding one. He looks worn, but hardship has left both frame and attention surprisingly difficult to shake.

**Профиль (RU):** Горный ветеран, спящий на свёрнутой шерстяной шапке

**Profile (EN):** A mountain veteran who sleeps on a folded wool cap

### `JAZZ_AME_41` — Sipho "Anvil" Khumalo

- **Nationality:** `SouthAfrica`
- **Category / CombatRole:** Hardened / Machinegunner
- **Specialization:** `HeavyWeapons`
- **Level / Salary:** 1 / $143
- **Potential (Wisdom):** Low
- **Traits (common):** `HeavyWeaponsTraining`, `AutoWeapons`
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_41` ← donor `GrandChien_Heavy` (male; blue recolor, source не править)
- **Inventory (fixed):** BAR · .30-06×80 · Knife · Bandage×1

| Stat | |
| --- | ---: |
| Health | 94 |
| Agility | 62 |
| Dexterity | 60 |
| Strength | 90 |
| Wisdom | 36 |
| Will | 58 |
| Leadership | 8 |
| Marksmanship | 50 |
| Mechanical | 0 |
| Explosives | 8 |
| Medical | 5 |

**Биография (RU):** В южноафриканском пулемётном расчёте Сифо «Наковальня» Кхумало всегда получал ту часть ноши, которую остальные делили на двоих. Он двигается тяжело, мыслит прямыми линиями и не притворяется точным мастером одиночной цели. По вечерам Сифо неловко штопает ремни крошечным напёрстком, подаренным матерью, зажимая иглу огромными пальцами. Когда требуется долго удерживать тяжёлый ствол на одном направлении, его недостатки внезапно становятся почти неважны.

**Biography (EN):** His mother's tiny brass thimble glints absurdly between Sipho “Anvil” Khumalo's enormous fingers while he repairs webbing. A South African gun crew gave every oversized burden to his shoulders. Sipho thinks in straight lines, advances without grace, and claims no gift for a fine shot. He adapts slowly, but once the heavy barrel settles, neither recoil nor argument moves him easily.

**Профиль (RU):** «Наковальня» с тяжёлым стволом и крошечным напёрстком

**Profile (EN):** Anvil, a heavy gun, and one tiny brass thimble

### `JAZZ_AME_42` — Boubacar Kane

- **Nationality:** `Senegal`
- **Category / CombatRole:** Hardened / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $107
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_42` ← donor `GrandChien_Marksman` (male; blue recolor, source не править)
- **Inventory (fixed):** STG44 · 7.92Kurz×40 · Knife · Bandage×1

| Stat | |
| --- | ---: |
| Health | 82 |
| Agility | 70 |
| Dexterity | 70 |
| Strength | 68 |
| Wisdom | 48 |
| Will | 52 |
| Leadership | 18 |
| Marksmanship | 60 |
| Mechanical | 0 |
| Explosives | 12 |
| Medical | 8 |

**Биография (RU):** Служба офицером запаса в Сенегале научила Бубакара Кане, что усталые люди лучше выполняют короткий приказ, смысл которого им объяснили. Он говорит спокойно, не тратит время на позу и сам проверяет путь, прежде чем отправить туда другого. Бубакар пишет распоряжения на внутренней стороне пустых сигаретных пачек и просит прочитавшего повторить их своими словами. Восторгов вокруг него немного, а позиции после суток рядом обычно остаются на месте.

**Biography (EN):** Reserve service in Senegal taught Boubacar Kane that exhausted people remember reasons longer than shouted commands. He explains the purpose, checks the route himself, and lets silence replace ceremony. Orders go onto the clean inside of flattened cigarette packets, then the recipient must repeat them in ordinary words. Boubacar inspires trust gradually rather than dramatically, but confusion has a way of thinning out wherever his quiet routine takes hold.

**Профиль (RU):** Офицер без театра, пишущий приказы на сигаретных пачках

**Profile (EN):** An unshowy officer writing clear orders on cigarette packets

### `JAZZ_AME_43` — Didier "Smoke" Mbemba

- **Nationality:** `Congo`
- **Category / CombatRole:** Hardened / Grenadier
- **Specialization:** `HeavyWeapons`
- **Level / Salary:** 1 / $135
- **Potential (Wisdom):** Low
- **Traits (common):** `Throwing`, `HeavyWeaponsTraining`
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_43` ← donor `GrandChien_Medic` (male; blue recolor, source не править)
- **Inventory (fixed):** Ithaca · 12g×16 · FragGrenade×2 · Knife · Bandage×1

| Stat | |
| --- | ---: |
| Health | 78 |
| Agility | 68 |
| Dexterity | 70 |
| Strength | 70 |
| Wisdom | 44 |
| Will | 48 |
| Leadership | 5 |
| Marksmanship | 58 |
| Mechanical | 5 |
| Explosives | 14 |
| Medical | 5 |

**Биография (RU):** За пылью от конголезских зарядов Дидье Мбемба исчезал так часто, что прозвище «Дым» стало неизбежным. Он не любит бегать и предпочитает заранее знать, куда отступит после громкого хлопка. В кармане Дидье лежит обгоревший коробок спичек, на котором он каждый раз рисует новую стрелку выхода. Когда тишина уже потеряна, его расчётливое спокойствие оказывается полезнее скорости.

**Biography (EN):** A scorched matchbox receives Didier “Smoke” Mbemba's fresh escape arrow before every job. The habit began in Congolese demolition work, where he repeatedly vanished behind dust of his own making. Sprinting is not among Didier's ambitions, so every loud solution starts with a chosen way out. He can be ponderous while others have options, but once silence is gone he becomes the calmest man in the noise.

**Профиль (RU):** «Дым» всегда рисует путь отхода на спичечном коробке

**Profile (EN):** Smoke always draws his exit on a scorched matchbox

### `JAZZ_AME_44` — Amina Yusuf

- **Nationality:** `Nigeria`
- **Category / CombatRole:** Hardened / Autorifleman
- **Specialization:** `Autoriflemen`
- **Level / Salary:** 1 / $123
- **Potential (Wisdom):** Medium
- **Traits (common):** `AutoWeapons`
- **Personality:** —
- **Voice:** `Jazz_AME_Female` → VR `Jazz_AME_Female`
- **Appearance:** `JAZZ_AME_44` ← donor `RebelFemaleSniper` (female; blue recolor, source не править)
- **Inventory (fixed):** Type56 · 7.62×90 · Knife · Bandage×2

| Stat | |
| --- | ---: |
| Health | 80 |
| Agility | 70 |
| Dexterity | 68 |
| Strength | 64 |
| Wisdom | 52 |
| Will | 54 |
| Leadership | 16 |
| Marksmanship | 58 |
| Mechanical | 0 |
| Explosives | 8 |
| Medical | 12 |

**Биография (RU):** Тяжёлые годы в нигерийской части оставили Амине Юсуф уважение к короткой очереди и чистой повязке. Она бережёт оружие без нежности, как вещь, которая обязана работать и не нуждается в комплиментах. Запасные бинты Амина заворачивает в вощёную бумагу и меняет свёрток после каждого дождя. Новичков смущает её холодный взгляд; рядом с кровью эта отстранённость превращается в собранность.

**Biography (EN):** Spare bandages stay sealed in Amina Yusuf's waxed paper and are inspected whenever rain enters the seams. Nigerian service taught her that ammunition, sleep, and clean cloth all require conservation. Amina treats her rifle as a duty rather than a companion and keeps every burst brief. Her reserve feels severe across a table, but beside blood it becomes the steady distance needed to help.

**Профиль (RU):** Холодный взгляд, короткая очередь и сухие бинты

**Profile (EN):** A cool gaze, measured fire, and bandages kept dry

### `JAZZ_AME_45` — Léopold Sassou

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Hardened / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $115
- **Potential (Wisdom):** Low
- **Traits (common):** —
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_45` ← donor `GrandChien_Officer` (male; blue recolor, source не править)
- **Inventory (fixed):** STG44 · 7.92Kurz×40 · Knife · Wirecutter · Bandage×1

| Stat | |
| --- | ---: |
| Health | 88 |
| Agility | 68 |
| Dexterity | 66 |
| Strength | 76 |
| Wisdom | 40 |
| Will | 56 |
| Leadership | 14 |
| Marksmanship | 60 |
| Mechanical | 28 |
| Explosives | 10 |
| Medical | 8 |

**Биография (RU):** Чужая лень и мелкая грязь испортили при Леопольде Сассу достаточно оружия, чтобы сержант Гранд-Шьен перестал верить оправданиям. Он крепок, говорит ровно и без особого удовольствия чинит простые неполадки прямо на месте. В пустой сигарной трубке Леопольд носит тонкую щётку и каплю масла, защищённую пробкой. Камера улыбки от него не получает; правильно вставший магазин иногда получает.

**Biography (EN):** A fine cleaning brush and a corked drop of oil travel inside Sergeant Léopold Sassou's empty cigar tube. Grand Chien service meant rescuing rifles from dust, neglect, and owners who swore they had changed nothing. Solid and unsentimental, Léopold knows enough about simple faults to be dangerous to excuses. People rarely earn his smile, but a magazine seating cleanly can soften his entire face.

**Профиль (RU):** Сержант с оружейной щёткой в пустой сигарной трубке

**Profile (EN):** A sergeant carrying a cleaning brush inside a cigar tube

### `JAZZ_AME_46` — Kofi Mensah

- **Nationality:** `Ghana`
- **Category / CombatRole:** Hardened / Machinegunner
- **Specialization:** `HeavyWeapons`
- **Level / Salary:** 1 / $131
- **Potential (Wisdom):** Low
- **Traits (common):** `HeavyWeaponsTraining`
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_46` ← donor `GrandChien_Recon` (male; blue recolor, source не править)
- **Inventory (fixed):** MAC2429 · 7.5French×80 · Knife · Bandage×1

| Stat | |
| --- | ---: |
| Health | 92 |
| Agility | 60 |
| Dexterity | 58 |
| Strength | 92 |
| Wisdom | 34 |
| Will | 60 |
| Leadership | 5 |
| Marksmanship | 56 |
| Mechanical | 0 |
| Explosives | 8 |
| Medical | 5 |

**Биография (RU):** От портовой лебёдки в Гане Кофи Менса перешёл к тяжёлому оружию, сменив канаты на другую ношу. Он огромен, нетороплив и не пытается догнать того, кого можно вынудить остановиться. Кофи всегда держит при себе моток грубой верёвки и чинит им ручки на ящиках, которые другие уже списали. Тонкий расчёт проходит мимо него, но вес, отдача и долгая неподвижная работа будто придуманы под его плечи.

**Biography (EN):** Coarse rope rides at Kofi Mensah's waist for repairing crate handles everyone else has abandoned. He went from a Ghanaian dock winch to guns that made ordinary men seek another pair of hands. Immensely built, Kofi changes direction slowly and never chases what can be pinned down. Subtle plans can outrun his understanding, but weight and recoil seem to arrive at his shoulders already tamed.

**Профиль (RU):** Портовый силач с мотком верёвки для сломанных ящиков

**Profile (EN):** A dockside giant with rope for every broken crate

### `JAZZ_AME_47` — Hassan "Scorpion" Ibrahim

- **Nationality:** `Mali`
- **Category / CombatRole:** Hardened / Grenadier
- **Specialization:** `HeavyWeapons`
- **Level / Salary:** 1 / $139
- **Potential (Wisdom):** Medium
- **Traits (common):** `Throwing`
- **Personality:** `Scoundrel`
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_47` ← donor `LegionRaidLeader_alt` (male; blue recolor, source не править)
- **Inventory (fixed):** HiPower · 9mm×30 · FragGrenade×2 · Molotov×1 · Knife · Bandage×1

| Stat | |
| --- | ---: |
| Health | 80 |
| Agility | 70 |
| Dexterity | 70 |
| Strength | 66 |
| Wisdom | 46 |
| Will | 50 |
| Leadership | 8 |
| Marksmanship | 60 |
| Mechanical | 5 |
| Explosives | 14 |
| Medical | 5 |

**Биография (RU):** Кличка «Скорпион» пристала к Хассану Ибрахиму в Мали за быстрые появления и неприятные сюрпризы после них. Он двигается легче большинства старых служак, бросает уверенно и разговаривает так, будто каждую фразу снабдили жалом. В его спичечном блокноте на полях нарисованы скорпионы с разным выражением морды. Хассан любит точный момент взрыва чуть сильнее, чем безопасную дистанцию, и сам считает это частью обаяния.

**Biography (EN):** Tiny scorpions with different expressions crowd Hassan “Scorpion” Ibrahim's matchbook margins. The nickname followed quick deliveries between Malian outposts once those arrivals began including explosive replies. Hassan moves lightly, throws with conviction, and keeps a sting ready for conversation. He understands timing better than caution and enjoys a well-placed blast enough to stand closer than sensible people prefer.

**Профиль (RU):** «Скорпион» рисует тёзок на полях спичечного блокнота

**Profile (EN):** Scorpion sketches namesakes in the margins of a matchbook

### `JAZZ_AME_48` — Patrick Omondi

- **Nationality:** `Kenya`
- **Category / CombatRole:** Hardened / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $119
- **Potential (Wisdom):** Medium
- **Traits (common):** `NightOps`
- **Personality:** —
- **Voice:** `IMP_male_03` → VR `IMP_male_01`
- **Appearance:** `JAZZ_AME_48` ← donor `GrandChien_Stormer` (male; blue recolor, source не править)
- **Inventory (fixed):** Mini14 · 5.56×40 · Knife · Bandage×1

| Stat | |
| --- | ---: |
| Health | 82 |
| Agility | 70 |
| Dexterity | 70 |
| Strength | 64 |
| Wisdom | 48 |
| Will | 52 |
| Leadership | 48 |
| Marksmanship | 60 |
| Mechanical | 0 |
| Explosives | 10 |
| Medical | 8 |

**Биография (RU):** По паузам между шагами Патрик Омонди научился понимать, кто идёт в кенийской темноте уверенно, а кто притворяется. После заката он говорит шёпотом, но люди всё равно наклоняются ближе и слушают. Светящийся циферблат часов Патрик закрывает лоскутом чёрной ткани, поднимая его только под ладонью. Днём он кажется просто спокойным стрелком; ночь собирает его внимание в одну ясную линию.

**Biography (EN):** Black cloth covers Patrick Omondi's luminous watch and rises only beneath a cupped hand. Years on Kenyan night posts made footsteps as distinct to him as daytime faces. Patrick speaks softly after sunset, drawing tired people closer instead of competing with the dark. In daylight he is merely composed and competent; at night, patience and quiet authority seem to arrive at the same point.

**Профиль (RU):** Ночной стрелок с часами под чёрным лоскутом

**Profile (EN):** A night shooter whose watch sleeps beneath black cloth

## Specialists

### `JAZZ_AME_49` — Dr. Fatoumata Sy

- **Nationality:** `Senegal`
- **Category / CombatRole:** Specialists / Medic
- **Specialization:** `Doctor`
- **Level / Salary:** 1 / $236
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Personality:** —
- **Voice:** `Jazz_AME_Female` → VR `Jazz_AME_Female`
- **Appearance:** `JAZZ_AME_49` ← donor `RebelFemaleSniper_1` (female; blue recolor, source не править)
- **Inventory (fixed):** HiPower · 9mm×24 · Medkit · Bandage×6 · Morphine×2 · Knife

| Stat | |
| --- | ---: |
| Health | 70 |
| Agility | 52 |
| Dexterity | 54 |
| Strength | 40 |
| Wisdom | 72 |
| Will | 28 |
| Leadership | 30 |
| Marksmanship | 24 |
| Mechanical | 8 |
| Explosives | 5 |
| Medical | 70 |

**Биография (RU):** В сенегальском полевом лазарете доктор Фатумата Си порой видела готовый операционный стол раньше подвоза чистой воды. Она говорит тихо, режет уверенно и особенно сердится на людей, считающих бинты признаком трусости. Красной перьевой ручкой Фатумата помечает карточки раненых и никогда не даёт её взаймы. Пистолет в её руке вызывает сомнение, открытая рана — точное и безжалостное решение.

**Biography (EN):** A red fountain pen marks Fatoumata Sy's casualty notes and remains the one possession she refuses to lend. Senegalese field surgery taught her that clean water can feel more precious than ammunition. Fatoumata lowers her voice when a ward grows frantic, forcing everyone nearby to listen instead of shout. A pistol brings visible reluctance, but an uncovered wound replaces hesitation with exact, unsparing purpose.

**Профиль (RU):** Полевой хирург с красной ручкой и тихим голосом

**Profile (EN):** A field surgeon with a red pen and a quiet voice

### `JAZZ_AME_50` — Grace Wanjiru

- **Nationality:** `Kenya`
- **Category / CombatRole:** Specialists / Medic
- **Specialization:** `Doctor`
- **Level / Salary:** 1 / $214
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Personality:** `Optimist`
- **Voice:** `Jazz_AME_Female` → VR `Jazz_AME_Female`
- **Appearance:** `JAZZ_AME_50` ← donor `RebelFemaleSniper_1` (female; blue recolor, source не править)
- **Inventory (fixed):** Knife · Medkit · Bandage×8 · Stim×2

| Stat | |
| --- | ---: |
| Health | 68 |
| Agility | 54 |
| Dexterity | 56 |
| Strength | 38 |
| Wisdom | 70 |
| Will | 26 |
| Leadership | 28 |
| Marksmanship | 22 |
| Mechanical | 5 |
| Explosives | 0 |
| Medical | 66 |

**Биография (RU):** Керосиновую ночь после аварии генератора Грейс Ванджиру провела у коек кенийского лазарета. Она не носит оружия и не изображает, будто человеческая кровь перестала её трогать. Складывая повязки, Грейс тихо напевает старую радиозаставку, потому что ровный ритм успокаивает и её, и пациентов. Передняя линия пугает её, а возле носилок паника обычно уступает место работе.

**Biography (EN):** An old radio jingle follows Grace Wanjiru through folded dressings until breathing around a cot matches its rhythm. Kenyan nursing taught her this during nights when the infirmary generator failed. Grace carries no gun and never pretends suffering has become ordinary. Violence aimed at her remains frighteningly unfamiliar, but beside a patient she becomes the calm pair of hands everyone was looking for.

**Профиль (RU):** Медсестра, напевающая радиозаставку над чистыми повязками

**Profile (EN):** A nurse humming an old radio tune over clean dressings

### `JAZZ_AME_51` — Dr. Emile Kabongo

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Specialists / Medic
- **Specialization:** `Doctor`
- **Level / Salary:** 1 / $257
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_51` ← donor `LegionSharpShooter` (male; blue recolor, source не править)
- **Inventory (fixed):** HiPower · 9mm×24 · Medkit · Bandage×6 · Knife

| Stat | |
| --- | ---: |
| Health | 74 |
| Agility | 50 |
| Dexterity | 52 |
| Strength | 44 |
| Wisdom | 74 |
| Will | 30 |
| Leadership | 38 |
| Marksmanship | 26 |
| Mechanical | 12 |
| Explosives | 5 |
| Medical | 68 |

**Биография (RU):** Дорожные травмы в Гранд-Шьен часто приводили к доктору Эмилю Кабонго пациентов, которых сперва перевязали добрыми, но неумелыми руками. Поэтому он учит каждого помощника простым узлам и повторяет объяснение без раздражения, пока тот не поймёт. За ухом Эмиль держит тупой плотницкий карандаш, которым рисует схемы прямо на упаковке бинтов. Оружие сковывает его, сложная рана возвращает голосу и пальцам почти молодую точность.

**Biography (EN):** A blunt carpenter's pencil sits behind Emile Kabongo's ear for sketching knots on wrappers and walls. Grand Chien road injuries often made him undo the generous mistakes of whoever reached a victim first. Emile teaches simple bandaging wherever he goes, patient with ignorance but not carelessness. Emergencies have aged his face and slowed his step, yet a difficult wound still brings remarkable clarity to hands and instructions.

**Профиль (RU):** Травматолог, рисующий спасительные узлы тупым карандашом

**Profile (EN):** A trauma doctor sketching lifesaving knots with a blunt pencil

### `JAZZ_AME_52` — Captain Amara Koné

- **Nationality:** `Mali`
- **Category / CombatRole:** Specialists / Instructor
- **Specialization:** `Leader`
- **Level / Salary:** 1 / $264
- **Potential (Wisdom):** High
- **Traits (common):** `Teacher`
- **Personality:** —
- **Voice:** `Jazz_AME_Female` → VR `Jazz_AME_Female`
- **Appearance:** `JAZZ_AME_52` ← donor `MilitiaRookie_Female_01` (female; blue recolor, source не править)
- **Inventory (fixed):** STG44 · 7.92Kurz×30 · Knife · Bandage×2

| Stat | |
| --- | ---: |
| Health | 68 |
| Agility | 48 |
| Dexterity | 50 |
| Strength | 52 |
| Wisdom | 85 |
| Will | 32 |
| Leadership | 68 |
| Marksmanship | 35 |
| Mechanical | 50 |
| Explosives | 28 |
| Medical | 35 |

**Биография (RU):** Строевой театр, красивый лишь до первого раненого, быстро надоел капитану Амаре Коне во время службы в Мали. Она разбирает ошибку жёстко, но объясняет её смысл, пока ученик не сможет повторить урок другому. Перед рассветом Амара ставит на огонь помятый чайник и заканчивает занятие лишь тогда, когда вода закипит. Сама она уже не так легка на ногах и не прячет этого; её правила переживают усталость лучше многих людей.

**Biography (EN):** A battered kettle goes on before Captain Amara Koné's dawn lessons, and its whistle closes the session. Malian service taught her to turn nervous soldiers into people who understood why a drill mattered. Amara rejects parade-ground drama, giving an error explanation rather than humiliation. Her own body no longer demonstrates every movement gracefully, yet the habits she plants keep working when fear makes clever advice disappear.

**Профиль (RU):** Капитан, чей помятый чайник отмеряет уроки до рассвета

**Profile (EN):** A captain whose battered kettle keeps time for dawn lessons

### `JAZZ_AME_53` — Sgt. Nadia Okonkwo

- **Nationality:** `Nigeria`
- **Category / CombatRole:** Specialists / Instructor
- **Specialization:** `Leader`
- **Level / Salary:** 1 / $243
- **Potential (Wisdom):** High
- **Traits (common):** `Teacher`
- **Personality:** —
- **Voice:** `Jazz_AME_Female` → VR `Jazz_AME_Female`
- **Appearance:** `JAZZ_AME_53` ← donor `MilitiaRookie_Female_02` (female; blue recolor, source не править)
- **Inventory (fixed):** STG44 · 7.92Kurz×40 · Knife · Bandage×2

| Stat | |
| --- | ---: |
| Health | 66 |
| Agility | 50 |
| Dexterity | 52 |
| Strength | 50 |
| Wisdom | 82 |
| Will | 28 |
| Leadership | 65 |
| Marksmanship | 38 |
| Mechanical | 42 |
| Explosives | 22 |
| Medical | 30 |

**Биография (RU):** Чужой промах сержант Надия Оконкво разбирает лучше, чем изображает собственную безошибочность перед начальством. В Нигерии она учила молодых солдат прицеливаться без спешки, резким голосом давая ясные объяснения. Надия носит деревянную линейку со сколом и чертит ею направление прямо на земле. В долгом бою она устаёт раньше, чем признаётся, но рядом с ней чужие руки обычно перестают торопиться.

**Biography (EN):** A chipped wooden ruler draws Sergeant Nadia Okonkwo's sight lines in dust, on tables, or across a map. Teaching troops in Nigeria revealed that she diagnoses another shooter's mistake better than she displays perfection herself. Nadia's voice carries, but the lesson beneath it is precise and free of vanity. She cannot sustain every example demanded from younger bodies, yet pupils nearby soon stop snatching at the shot.

**Профиль (RU):** Сержант с деревянной линейкой для ошибок на прицеле

**Profile (EN):** A sergeant who maps every mistake with a wooden ruler

### `JAZZ_AME_54` — Maj. Théodore Ngalula

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Specialists / Instructor
- **Specialization:** `Leader`
- **Level / Salary:** 1 / $286
- **Potential (Wisdom):** High
- **Traits (common):** `Teacher`
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_54` ← donor `Stormer_Rebels_03` (male; blue recolor, source не править)
- **Inventory (fixed):** STG44 · 7.92Kurz×30 · Knife · Bandage×3

| Stat | |
| --- | ---: |
| Health | 72 |
| Agility | 46 |
| Dexterity | 48 |
| Strength | 58 |
| Wisdom | 88 |
| Will | 34 |
| Leadership | 70 |
| Marksmanship | 32 |
| Mechanical | 55 |
| Explosives | 30 |
| Medical | 40 |

**Биография (RU):** Почему одни группы рассыпались за неделю, а другие выдерживали тяжёлый сезон, майор Теодор Нгалула изучал всю службу в Гранд-Шьен. Он объясняет долго, чинит попавшуюся под руку мелочь и не повышает голос только ради звания. Складные очки Теодора держатся на проволоке, которую он однажды заменил сам и с тех пор упрямо не меняет. Возраст спорит с ним в движении; слабое место чужого плана он замечает раньше, чем молодые успевают заскучать.

**Biography (EN):** Wire holds one arm of Major Théodore Ngalula's folding spectacles, a temporary fix kept for years. His Grand Chien career was spent teaching groups to survive after exhaustion stripped away ceremony. Théodore repeats an explanation until it works in ordinary language, often repairing a loose buckle while he talks. He moves like an older man now, but flawed plans still reveal themselves to him with uncomfortable speed.

**Профиль (RU):** Майор в починенных проволокой очках, видящий слабые планы

**Profile (EN):** A major in wire-mended spectacles who spots weak plans

### `JAZZ_AME_55` — Issa Camara

- **Nationality:** `Senegal`
- **Category / CombatRole:** Specialists / Sniper
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $200
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_55` ← donor `LegionRaidLeader` (male; blue recolor, source не править)
- **Inventory (fixed):** Gewehr98 · 7.62×20 · Knife

| Stat | |
| --- | ---: |
| Health | 54 |
| Agility | 62 |
| Dexterity | 58 |
| Strength | 48 |
| Wisdom | 58 |
| Will | 28 |
| Leadership | 8 |
| Marksmanship | 68 |
| Mechanical | 20 |
| Explosives | 5 |
| Medical | 5 |

**Биография (RU):** На севере Сенегала Исса Камара наблюдал за дорогой, где редкий выстрел был полезнее долгой перестрелки на жаре. Он бережёт дыхание, не участвует в беготне и честно предупреждает, что штурмовая работа создана для других. На ремне его винтовки висит гладкая деревянная бусина, которую Исса перекатывает пальцем во время ожидания. Хрупкое тело редко подводит его: терпение обычно заканчивает дело раньше.

**Biography (EN):** A smooth wooden bead slides beneath Issa Camara's thumb along the rifle sling during long waits. Heat on a northern Senegalese road taught him how a careful shot can end an afternoon's danger. Issa accepts his narrow frame and leaves rushing to people built for it. He suffers quickly when a position becomes a brawl, but few prevent the quiet moment from turning into one as well.

**Профиль (RU):** Терпеливый стрелок с деревянной бусиной на ремне

**Profile (EN):** A patient shooter with a wooden bead on his sling

### `JAZZ_AME_56` — Lindiwe Mokoena

- **Nationality:** `SouthAfrica`
- **Category / CombatRole:** Specialists / Sniper
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $243
- **Potential (Wisdom):** Medium
- **Traits (common):** `NightOps`
- **Personality:** `Stealthy`
- **Voice:** `IMP_female_02` → VR `IMP_female_01`
- **Appearance:** `JAZZ_AME_56` ← donor `GrandChien_CommanderFemale` (female; blue recolor, source не править)
- **Inventory (fixed):** SKS · 7.62×30 · Knife

| Stat | |
| --- | ---: |
| Health | 52 |
| Agility | 66 |
| Dexterity | 60 |
| Strength | 46 |
| Wisdom | 55 |
| Will | 30 |
| Leadership | 12 |
| Marksmanship | 70 |
| Mechanical | 15 |
| Explosives | 0 |
| Medical | 8 |

**Биография (RU):** Ночная работа в Южной Африке научила Линдиве Мокоену любить часы, когда лишний блеск выдаёт человека раньше движения. Она говорит коротко, не обещает чудес и выбирает путь, на котором не придётся бороться с собственной хрупкостью. Маленькой банкой матовой краски Линдиве закрывает свежие царапины на металле ещё до наступления темноты. Дневная суета утомляет её, зато ночью внимание становится тихим и острым.

**Biography (EN):** A tiny jar of matte black paint covers every fresh glint on Lindiwe Mokoena's metal before dusk. South African night observation taught her how a bright scratch betrays more than a careless footstep. Lindiwe is reserved and careful not to confuse courage with carrying too much. Daylight bustle drains her quickly, but darkness narrows the world into patient shapes she can read with unusual confidence.

**Профиль (RU):** Ночная наблюдательница с банкой матовой чёрной краски

**Profile (EN):** A night watcher with a tiny jar of matte black paint

### `JAZZ_AME_57` — Bakary Diarra

- **Nationality:** `Mali`
- **Category / CombatRole:** Specialists / Sapper
- **Specialization:** `ExplosiveExpert`
- **Level / Salary:** 1 / $171
- **Potential (Wisdom):** Medium
- **Traits (common):** `Throwing`
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_57` ← donor `LegionGrenadir` (male; blue recolor, source не править)
- **Inventory (fixed):** Knife · ShapedCharge×2 · TNT×1 · PipeBomb×2 · Detonator · Wirecutter

| Stat | |
| --- | ---: |
| Health | 70 |
| Agility | 48 |
| Dexterity | 52 |
| Strength | 55 |
| Wisdom | 60 |
| Will | 26 |
| Leadership | 8 |
| Marksmanship | 24 |
| Mechanical | 50 |
| Explosives | 68 |
| Medical | 8 |

**Биография (RU):** Пистолет Бакари Диарра однажды превратился в коробку хороших детонаторов для дорожных работ в Мали, и хозяин не пожалел. Провода и взрыватели понятнее ему, чем перестрелка, где опасность не ждёт разрешения. Детонаторы Бакари держит в старой сигаретной жестянке, переложенной хлопком, и перед делом стучит ногтем по крышке. Рядом с подготовленным зарядом руки у него спокойны, но летящая пуля мгновенно напоминает, насколько он не любит случайность.

**Biography (EN):** A cotton-lined cigarette tin holds Bakary Diarra's detonators and receives a nervous tap before work. He acquired them by trading away his pistol during years handling Malian road charges. Wires obey sequence while gunfire does not, a distinction Bakary takes seriously. Beside a device he understands he is composed, but uncontrolled danger exposes how much confidence depends on preparing the ground himself.

**Профиль (RU):** Дорожный подрывник с детонаторами в хлопковой жестянке

**Profile (EN):** A road blaster keeping detonators in a cotton-lined tin

### `JAZZ_AME_58` — Marie-Claire Mbala

- **Nationality:** `Congo`
- **Category / CombatRole:** Specialists / Sapper
- **Specialization:** `ExplosiveExpert`
- **Level / Salary:** 1 / $214
- **Potential (Wisdom):** Medium
- **Traits (common):** `Throwing`
- **Personality:** —
- **Voice:** `Jazz_AME_Female` → VR `Jazz_AME_Female`
- **Appearance:** `JAZZ_AME_58` ← donor `MilitiaRookie_Female_02` (female; blue recolor, source не править)
- **Inventory (fixed):** Makarov · 9x18×16 · ShapedCharge×2 · Knife · Wirecutter

| Stat | |
| --- | ---: |
| Health | 72 |
| Agility | 50 |
| Dexterity | 54 |
| Strength | 54 |
| Wisdom | 62 |
| Will | 28 |
| Leadership | 6 |
| Marksmanship | 26 |
| Mechanical | 52 |
| Explosives | 66 |
| Medical | 10 |

**Биография (RU):** Карьерные заряды в Конго приучили Мари-Клер Мбалу к сухому ремеслу, которое позже пришлось применять уже не только к камню. Она не любит поэзию вокруг взрывчатки и заставляет новичков сперва назвать путь отхода. Портновская лента Мари-Клер измеряет шнур точнее любого шага и всегда свёрнута в левом кармане. Любопытная загадка иногда подводит её слишком близко, зато после первого взгляда она редко путает опасный узел с безобидным.

**Biography (EN):** A tailor's tape coils in Marie-Claire Mbala's left pocket, measuring fuse without trusting footsteps. Congolese quarry charges taught her that explosives reward plain measurement and punish romantic language. Her manner is dry, and every newcomer must identify the exit before touching a wire. Marie-Claire leans too close when puzzled, but once a device reveals its logic, hesitation no longer wastes anyone's time.

**Профиль (RU):** Сухой характер и портновская лента для опасных узлов

**Profile (EN):** A dry wit and a tailor's tape for dangerous puzzles

### `JAZZ_AME_59` — Ousmane Fall

- **Nationality:** `Senegal`
- **Category / CombatRole:** Specialists / Mechanic
- **Specialization:** `Mechanic`
- **Level / Salary:** 1 / $157
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Personality:** —
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_59` ← donor `LegionScout_Stronger_alt` (male; blue recolor, source не править)
- **Inventory (fixed):** Wirecutter · Crowbar · Knife

| Stat | |
| --- | ---: |
| Health | 76 |
| Agility | 48 |
| Dexterity | 52 |
| Strength | 58 |
| Wisdom | 62 |
| Will | 26 |
| Leadership | 0 |
| Marksmanship | 22 |
| Mechanical | 70 |
| Explosives | 5 |
| Medical | 5 |

**Биография (RU):** Автобусы и оружие, как выяснил Усман Фалл в Сенегале, ломаются от одной компании: грязи, спешки и уверенного хозяина. Геройствовать он не хочет и в перестрелке ищет ближайшее твёрдое укрытие без малейшего стыда. Намагниченная чайная ложка Усмана собирает винты, которые иначе исчезли бы в пыли мастерской. Пока другие спорят о смелости, он возвращает в строй вещи, без которых спорщикам скоро пришлось бы идти пешком.

**Biography (EN):** A magnetised teaspoon gathers screws from the dust beside Ousmane Fall's tools. Senegalese buses taught him the same enemies later found in weapons: dirt, haste, and proud owners. Ousmane wants no heroics and finds solid cover honestly when bullets move. He looks awkward in a fight, but afterward is often the first person everyone needs and the last foolish enough to boast.

**Профиль (RU):** Автобусный мастер, собирающий винты намагниченной ложкой

**Profile (EN):** A bus-yard repairman gathering screws with a magnetised spoon

### `JAZZ_AME_60` — Jean-Pierre Kalala

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Specialists / Mechanic
- **Specialization:** `Mechanic`
- **Level / Salary:** 1 / $200
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Personality:** —
- **Voice:** `PierreMerc` → VR `PierreMerc`
- **Appearance:** `JAZZ_AME_60` ← donor `LegionRaider_Stronger_alt` (male; blue recolor, source не править)
- **Inventory (fixed):** Wirecutter · Lockpick · Knife · Bandage×1

| Stat | |
| --- | ---: |
| Health | 78 |
| Agility | 50 |
| Dexterity | 50 |
| Strength | 60 |
| Wisdom | 58 |
| Will | 28 |
| Leadership | 5 |
| Marksmanship | 24 |
| Mechanical | 68 |
| Explosives | 0 |
| Medical | 8 |

**Биография (RU):** По звуку шагов Жан-Пьер Калала узнавал клиента, который уже пытался чинить всё сам, ещё до порога гаража в Гранд-Шьен. Замки он слушает терпеливо, а оружие берёт только затем, чтобы освободить дорогу к работе. На запястье Жан-Пьера завязана синяя ветошь, которой он протирает инструменты перед тем, как убрать их по местам. Двигается он неспешно и стреляет неохотно, зато закрытая дверь редко остаётся для него последним словом.

**Biography (EN):** A blue shop rag is knotted around Jean-Pierre Kalala's wrist, wiping each tool before it returns to place. At his Grand Chien garage, footsteps revealed a customer's failed home repair before the man crossed the floor. Jean-Pierre listens to locks with the patience once reserved for stubborn engines. He is slow and uncomfortable with gunfire, but a closed mechanism seldom keeps its secrets for long.

**Профиль (RU):** Гаражный мастер с синей ветошью и терпением к замкам

**Profile (EN):** A garage master with a blue rag and patience for locks

