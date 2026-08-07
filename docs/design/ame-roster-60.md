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
- **Appearance:** на слот свой клон `JAZZ_AME_NN` (donor Rebels/Legion/Militia; Hardened/Spec — ещё GrandChien). Красное → синее; кожа с пресета. Карта: [`ame-appearance-map.json`](ame-appearance-map.json).
- **Кит:** Irr ≤ **1-2**; Fight ≤ **1-3**; Hard/Spec ≤ **2-1**. **`Type56` — потолок AR, только Hardened.** `SKS`/bolt — только Sniper.
- **ПП:** винтаж T1 — `Thompson` / `M3GreaseGun` / `PPS43` / `PPSH` / `MP40` / `MAT49` / `Sterling`. **`UZI` и прочий T2 ПП в стартовых китах нет.**
- **Бинты:** Fighters ~40%; Hardened всегда. **Sapper:** часть с `PipeBomb`.
- Voice pool: Jazz remesh majority (`Jazz_AME_Male_Low` / `Male_Hard` / `Female`) + `PierreMerc` variety (~1/8 males on bucket) + small IMP minority (~1/8; VR → `IMP_male_01` / `IMP_female_01`).
- **Bio canon:** самостоятельные RU+EN биографии и двуязычные profile blurbs; без мета-цифр статов/тиров.
- Nick: в основном Hardened. Grand Chien: заметная доля.

## Irregulars

### `JAZZ_AME_01` — Kwame Mensah

- **Nationality:** `Ghana`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $7
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_01` ← donor `MilitiaRookie_Male_01` (male; blue recolor, source не править)
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
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_02` ← donor `MilitiaRookie_Male_02` (male; blue recolor, source не править)
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

**Биография (RU):** Охота в Гранд-Шьен кормила Жан-Батиста Окоро, пока зверь не ушёл за границу его лицензии, а вместе с ним и заработок. Он не любит суеты и заранее выбирает место, где не придётся делать второй выстрел. В потрёпанном кожаном подсумке Окоро хранит горсть старых гильз, напоминающих об особенно долгих зимах. С шумным оружием он обращается настороженно, зато умеет ждать так долго, что окружающие начинают говорить шёпотом.

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
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_03` ← donor `Militia_Artillery` (male; blue recolor, source не править)
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

**Биография (RU):** На малийском посту Ибрахиму Туре чаще приходилось разнимать уличные ссоры, чем доставать револьвер. Он умеет понизить голос именно тогда, когда все вокруг начинают кричать, и обычно этим выигрывает нужную минуту. После закрытия участка Ибрахим оставил себе потёртый жетон и привычку складывать чистый платок в аккуратный квадрат для чужих ссадин. Стреляет он без блеска, зато в толчее не забывает, кто нуждается в помощи первым.

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
- **Voice:** `PierreMerc` → VR `PierreMerc`
- **Appearance:** `JAZZ_AME_04` ← donor `Militia_Demolition` (male; blue recolor, source не править)
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
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_05` ← donor `Militia_Heavy` (male; blue recolor, source не править)
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
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_06` ← donor `Militia_Marksman` (male; blue recolor, source не править)
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

**Биография (RU):** Сенегальские тропы долго кормили Муссу Диопа за умение заметить след раньше других. Старый винчестер достался ему от деда, и после каждого выхода Мусса протирает приклад кусочком льняной ткани. В компании он угрюм, зато в одиночестве двигается легко и без лишнего шума. Патроны считает заранее, потому что терпеть не может исправлять спешку вторым выстрелом.

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
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_07` ← donor `Militia_Medic` (male; blue recolor, source не править)
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
- **Voice:** `IMP_male_02` → VR `IMP_male_01`
- **Appearance:** `JAZZ_AME_08` ← donor `Militia_Officer` (male; blue recolor, source не править)
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

**Биография (RU):** Табо Молефе сторожил южноафриканские фермы, спал в сараях и отгонял воров старым двуствольным ружьём. Он двигается без спешки, зато у ворот стоит так спокойно, что хозяева забывали проверять замок. Его единственная прихоть — зелёная эмалированная кружка, из которой Табо пьёт даже холодную воду. Сложные приёмы даются ему не сразу, но первый хлопок никогда не срывает его с места.

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
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_09` ← donor `Militia_Recon` (male; blue recolor, source не править)
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
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_10` ← donor `Militia_Soldier` (male; blue recolor, source не править)
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

**Биография (RU):** Когда прямые дороги Гранд-Шьен стали слишком заметны, Эммануэль Кабонго повёл связных по тропам. Он не командует голосом, но растерянные люди почему-то держатся ближе к его плечу. В рубашке Эммануэль носит сложенный лист, где углём отмечены ручьи, колючие заросли и места для короткого сна. С оружием он неловок, зато ни разу не вывел спутника к неправильной развилке.

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
- **Voice:** `PierreMerc` → VR `PierreMerc`
- **Appearance:** `JAZZ_AME_12` ← donor `Militia_Stormer` (male; blue recolor, source не править)
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

**Биография (RU):** Амаду Кейта защищал родную деревню в Мали и привык чинить руками то, что другим казалось слишком тяжёлым. Однажды мина разнесла телегу рядом с ним, и с тех пор рыхлая земля заставляет его менять дорогу. Амаду носит длинную ореховую палку и проверяет ею каждый подозрительный край тропы, не скрывая причины. Он не любит сюрпризов, зато простую опасную работу выполняет без хвастовства и до конца.

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
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_14` ← donor `Artillery_Rebels_02` (male; blue recolor, source не править)
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
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_15` ← donor `Artillery_Rebels_03` (male; blue recolor, source не править)
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

**Биография (RU):** Жуан Домингос состоял в ангольской дружине, где одна встреча с минами заменила ему все последующие уроки храбрости. Он идёт медленно, внимательно смотрит под ноги и никогда не смеётся над чужой осторожностью. В ладони Жуан часто перекатывает гладкий болт от той самой разбитой телеги, напоминая себе не спешить. Скрытая угроза сковывает его, зато перед видимой он остаётся упрямым и прямым.

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

**Биография (RU):** Над гаражом отца в Гранд-Шьен Серж Куасси с детства раздражал его отказом брать отвёртку правильно. С железом Серж спорит до сих пор, зато быстро замечает, когда чужое объяснение не сходится. Он носит промасленный блокнот из мастерской и записывает туда не детали, а вопросы. Пустые руки его смущают меньше, чем пустая голова, хотя на деле одной догадки часто недостаточно.

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
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_19` ← donor `Demolitions_Rebels_02` (male; blue recolor, source не править)
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
- **Voice:** `PierreMerc` → VR `PierreMerc`
- **Appearance:** `JAZZ_AME_20` ← donor `Demolitions_Rebels_03` (male; blue recolor, source не править)
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

**Биография (RU):** На сенегальском перекрёстке Идрисса Бах мог одним жестом распутать движение, которое уже считало себя безнадёжным. В перестрелке ему неуютно, зато видимый порядок возвращает ему самообладание. Идрисса сам стирает белые перчатки по воскресеньям и сушит их на спинке единственного стула. Люди не всегда слышат его с первого раза, но руки у него говорят достаточно ясно, чтобы хаос сделал короткую паузу.

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
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_21` ← donor `Heavy_Rebels` (male; blue recolor, source не править)
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

**Биография (RU):** Омар Диалло ушёл из сенегальской части, когда понял, что очередной приказ заведёт его людей туда, откуда их не собираются возвращать. Теперь он говорит мало и долго выбирает момент, прежде чем приложить к плечу старый винчестер. После каждого выхода Омар ставит карандашную черту на внутренней стороне патронной коробки, считая не победы, а потраченные выстрелы. Решительность приходит к нему не сразу, зато принятое решение он уже не украшает словами.

**Biography (EN):** Omar Diallo deserted a Senegalese unit after one order too many treated lives as replaceable supplies. He keeps his distance from uniforms now, speaking only after he has watched a room settle. The inside of his cartridge box is covered with pencil marks, each one accounting for a round that did not return. Omar can hesitate over the path forward, but once the rifle reaches his shoulder he wastes neither motion nor breath.

**Профиль (RU):** Дезертир, считающий каждый выстрел карандашной чертой

**Profile (EN):** A deserter who accounts for every shot in pencil

### `JAZZ_AME_22` — Bastien Lafontaine

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Fighters / Autorifleman
- **Specialization:** `Autoriflemen`
- **Level / Salary:** 1 / $92
- **Potential (Wisdom):** Medium
- **Traits (common):** `AutoWeapons`
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

**Биография (RU):** Бастьен Лафонтен служил в местной милиции Гранд-Шьен с автоматическим оружием и чаще видел тесные улицы, чем открытое поле. От него пахнет машинным маслом и дешёвым табаком, хотя курит он только после работы. Бастьен заворачивает самокрутку в промасленную тряпицу и сердится, если кто-то без спроса трогает его оружие. Он не ищет красивого ракурса, зато хорошо чувствует минуту, когда узкий проход нужно наполнить шумом.

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
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_23` ← donor `Heavy_Rebels_03` (male; blue recolor, source не править)
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

**Биография (RU):** Чуквуэмека «Эмека» Оби держал пулемётную точку на нигерийском блокпосту, пока однажды утром от поста не осталось ничего, кроме мешков и пыли. Он велик, тяжёл и шутит, что земля — единственная мишень, которая никогда не уклоняется. Эмека пьёт чай из банки с вмятиной от осколка и не разрешает её выпрямлять. Отдельную цель он может проводить неровно, зато под его долгим грохотом чужие головы быстро учатся не подниматься.

**Biography (EN):** Chukwuemeka “Emeka” Obi survived the erasure of a Nigerian checkpoint where he had spent months behind a machine gun. He is built for weight rather than delicacy and laughs first when a careful shot goes astray. Tea comes from a shrapnel-dented tin cup that nobody is allowed to repair. Emeka may not pick a single point from the landscape with elegance, but he knows how to make an entire stretch of ground feel unwelcoming.

**Профиль (RU):** Тяжёлый ствол и осколочная вмятина на кружке

**Profile (EN):** A checkpoint survivor with a shrapnel dent in his cup

### `JAZZ_AME_24` — Michel Kabeya

- **Nationality:** `Congo`
- **Category / CombatRole:** Fighters / Grenadier
- **Specialization:** `HeavyWeapons`
- **Level / Salary:** 1 / $95
- **Potential (Wisdom):** Medium
- **Traits (common):** `Throwing`
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

**Биография (RU):** Мишель Кабейа разгружал речные баржи в Конго и развлекал смену, забрасывая пустые банки в узкие щели между ящиками. Позже оказалось, что тот же глазомер полезен для предметов, которые лучше не возвращать обратно. В баре Мишель шумен, но перед броском всегда замолкает и один раз касается большого пальца медного кольца на чеке. Он двигается охотно, хотя близость собственного взрыва уважает сильнее, чем показывает друзьям.

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
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_25` ← donor `Marksman_Rebels_02` (male; blue recolor, source не править)
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

**Биография (RU):** Джума Отиено служил на кенийской границе, где пыль появлялась раньше машин и часто была единственным предупреждением. Он привык быстро менять место и не обижается на приказ не изображать героя. Перед выходом Джума завязывает на лице выцветший клетчатый платок, сохранивший запах дорожного мыла. Тяжёлое снаряжение утомляет его быстрее долгого пути, зато первым увидеть движение на горизонте для него почти личная обязанность.

**Biography (EN):** Juma Otieno watched a Kenyan border where a ribbon of dust could announce company minutes before an engine arrived. He learned to relocate before a position became a trap and has little patience for theatrical last stands. A faded checked scarf covers his mouth on the road, still faintly scented with the soap his sister used. Juma carries weight poorly, but open ground seems to sharpen his attention and quicken every choice.

**Профиль (RU):** Пограничник в выцветшем платке, читающий дорожную пыль

**Profile (EN):** A border runner who reads the dust through a faded scarf

### `JAZZ_AME_26` — Andile Nkosi

- **Nationality:** `SouthAfrica`
- **Category / CombatRole:** Fighters / Autorifleman
- **Specialization:** `Autoriflemen`
- **Level / Salary:** 1 / $87
- **Potential (Wisdom):** Medium
- **Traits (common):** `AutoWeapons`
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

**Биография (RU):** Андиле Нкоси охранял конвои в Южной Африке и научился отвечать на засаду, не превращая груз за спиной в решето. Он спокоен, немногословен и раздражается, когда новички берут его оружие просто из любопытства. На ремне Андиле закреплена полоска синей изоленты с номером первой машины, которую он довёл целой. Неожиданные перемены ему не нравятся, зато в знакомом ритме он расходует шум коротко и бережно.

**Biography (EN):** Andile Nkosi escorted South African convoys, where careless fire could ruin the cargo before any attacker reached it. He prefers routine, short instructions, and people who keep their hands to themselves. Blue electrical tape around his sling bears the plate number of the first truck he brought through untouched. Sudden improvisation can leave Andile a step behind, but once a pattern reveals itself he controls his weapon with disciplined restraint.

**Профиль (RU):** Конвойный стрелок с синей лентой первой спасённой машины

**Profile (EN):** A convoy guard marked by one safely delivered truck

### `JAZZ_AME_27` — Sekou Camara

- **Nationality:** `Mali`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $60
- **Potential (Wisdom):** Medium
- **Traits (common):** —
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

**Биография (RU):** Секу Камара патрулировал малийскую пустыню и рано понял, что неподвижная фигура на светлом фоне долго не живёт. Он постоянно смещается, выбирает низины и терпеть не может ждать на месте только ради чужой важности. Компас Секу треснул много лет назад, но стрелка всё ещё находит север, если постучать по стеклу ногтем. Его короткое оружие не прощает дальних амбиций, зато ноги часто уносят его туда, где тяжёлые товарищи ещё ищут удобный путь.

**Biography (EN):** Sekou Camara patrolled the Malian desert, learning that an upright man against a pale horizon becomes everyone's landmark. Restlessness serves him well in open country, though it can make patient companions grind their teeth. His compass has a cracked face and needs one sharp tap before the needle remembers north. Sekou lacks the reach for distant contests, but he crosses exposed ground with a speed that gives slower people room to breathe.

**Профиль (RU):** Пустынный патрульный с треснувшим, но верным компасом

**Profile (EN):** A desert patrolman guided by a cracked but faithful compass

### `JAZZ_AME_28` — Pascal Ngoma

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Fighters / Machinegunner
- **Specialization:** `HeavyWeapons`
- **Level / Salary:** 1 / $104
- **Potential (Wisdom):** Medium
- **Traits (common):** `HeavyWeaponsTraining`
- **Voice:** `PierreMerc` → VR `PierreMerc`
- **Appearance:** `JAZZ_AME_28` ← donor `Medic_Rebels_02` (male; blue recolor, source не править)
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

**Биография (RU):** Паскаль Нгома много месяцев держал огневую точку в Гранд-Шьен и полюбил места, откуда не нужно никуда бежать. Он упрям, тяжёл и воспринимает движение скорее как уступку обстоятельствам. Под вещами Паскаля всегда привязан крошечный складной табурет, вызывающий смех ровно до первой долгой ночи. Быстрой смены плана от него не дождёшься, зато вокруг выбранной позиции постепенно становится тихо.

**Biography (EN):** Pascal Ngoma spent enough time on a fixed gun in Grand Chien to regard running as evidence of poor planning. He is stubborn, durable, and happiest when a patch of ground has clearly become his responsibility. A ridiculous folding stool is strapped beneath his pack and appears whenever waiting stretches past an hour. Pascal reacts slowly to a new direction, but incoming noise rarely persuades him to leave the old one.

**Профиль (RU):** Упрямый хозяин позиции с крошечным складным табуретом

**Profile (EN):** A stubborn position keeper with a tiny folding stool

### `JAZZ_AME_29` — Kwesi Boateng

- **Nationality:** `Ghana`
- **Category / CombatRole:** Fighters / Grenadier
- **Specialization:** `HeavyWeapons`
- **Level / Salary:** 1 / $98
- **Potential (Wisdom):** Medium
- **Traits (common):** `Throwing`, `HeavyWeaponsTraining`
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

**Биография (RU):** Квеси Боатенг работал у склада в Гане и после смены часами бросал пустые бутылки в меловой круг на стене. Эта забава сделала его уверенным с предметами, которые звенят куда опаснее стекла. Квеси собирает крышки в табачную коробку и встряхивает её перед выходом, проверяя спокойствие руки. Он действует быстро и улыбается редко, а после громкого результата предпочитает уже быть в другом месте.

**Biography (EN):** Behind a Ghanaian warehouse, Kwesi Boateng taught himself to hit a chalk circle with empty bottles after work. The pastime translated neatly to heavier objects with shorter fuses. Bottle caps fill an old tobacco tin, and he shakes it once before moving out to hear whether his hand is steady. Kwesi commits quickly but dislikes the seconds after impact, when the echo seems to search for whoever caused it.

**Профиль (RU):** Бросок в меловой круг и крышки в табачной коробке

**Profile (EN):** A chalk target and bottle caps rattling in a tobacco tin

### `JAZZ_AME_30` — Tesfaye Alemu

- **Nationality:** `Ethiopia`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $75
- **Potential (Wisdom):** Medium
- **Traits (common):** —
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

**Биография (RU):** Тесфайе Алему вырос в эфиопских горах и научился успокаивать дыхание раньше, чем получил оружие, достойное этого умения. Он худощав, терпелив и без зависти принимает то, что оказалось под рукой. Перед выстрелом Тесфайе сжимает гладкий серый камень, когда-то поднятый у дома, а затем убирает его в карман. Долгая драка быстро истощает его, зато первый спокойный миг он использует редко хуже других.

**Biography (EN):** Tesfaye Alemu learned to shoot in the Ethiopian highlands, where a hurried breath could carry farther than a footstep. Better rifles always seemed to belong to somebody else, a fact he accepts without bitterness. A smooth grey stone from his home valley rests in his palm while he settles himself, then disappears before the shot. Tesfaye is not made for prolonged punishment, but patience often lets him finish before endurance becomes the question.

**Профиль (RU):** Горный стрелок, успокаивающий дыхание серым камнем

**Profile (EN):** A highland shooter who steadies himself with a grey stone

### `JAZZ_AME_31` — Rafael dos Santos

- **Nationality:** `Angola`
- **Category / CombatRole:** Fighters / Autorifleman
- **Specialization:** `Autoriflemen`
- **Level / Salary:** 1 / $89
- **Potential (Wisdom):** Medium
- **Traits (common):** `AutoWeapons`
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_31` ← donor `Recon_Rebels_02` (male; blue recolor, source не править)
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

**Биография (RU):** Рафаэль дос Сантос сопровождал дорожные бригады в Анголе и осваивал каждое новое дело медленнее тех, кто любил давать советы. Он не спорил, а повторял движение до тех пор, пока оно не становилось привычкой. Вокруг запястья Рафаэля намотан запасной шнурок, потому что однажды порванный ботинок задержал всю колонну. С внезапной выдумкой он дружит плохо, зато приходит трезвым, держит заданный порядок и не исчезает после тяжёлого дня.

**Biography (EN):** Rafael dos Santos guarded Angolan road crews and was rarely the quickest man to understand a new drill. Instead of pretending, he repeated it until the motion belonged to him. A spare bootlace circles his wrist, recalling the day one broken lace delayed an entire column. Rafael can be rigid when plans change without warning, but fatigue and dust do little to loosen a promise he has already made.

**Профиль (RU):** Упрямый ученик со шнурком на запястье

**Profile (EN):** A persistent learner with a spare bootlace around his wrist

### `JAZZ_AME_32` — Awa Sow

- **Nationality:** `Senegal`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $57
- **Potential (Wisdom):** Medium
- **Traits (common):** —
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

**Биография (RU):** Ава Соу ночами охраняла склад у сенегальской пристани, где узкие коридоры вынуждали встречать неприятности почти вплотную. Она быстра, колка и слишком хорошо слышит каждый неожиданный скрип за дверью. От старого склада у Авы остался погнутый ключ, которым она постукивает по бедру, когда кто-то начинает поучать её снисходительным тоном. Долгая пальба расшатывает ей нервы, зато в тесноте она исчезает с чужой линии раньше, чем там становится опасно.

**Biography (EN):** Awa Sow worked night security in a Senegalese dockside storehouse whose passages left no room for grand gestures. She learned to slip around trouble quickly, while never learning to enjoy the sound of it arriving. The bent key to that vanished job taps against her thigh whenever a man begins explaining her own work to her. Sustained noise wears at Awa's composure, but close walls give her speed somewhere useful to go.

**Профиль (RU):** Быстрый шаг, погнутый ключ и нетерпение к поучениям

**Profile (EN):** Quick feet, a bent key, and no patience for lectures

### `JAZZ_AME_33` — Claude Mvemba

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $69
- **Potential (Wisdom):** Medium
- **Traits (common):** —
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

**Биография (RU):** Клод Мвемба охранял плантации Гранд-Шьен и привык решать споры на расстоянии, удобном для дробовика. Он говорит мало, курит много и считает лишний шаг навстречу таким же расточительством, как лишнее слово. Серебристый портсигар Клода давно смят каблуком, но закрывается с приятным щелчком. Открытый простор не даёт ему уверенности, зато среди изгородей и сараев он безошибочно чувствует собственную дистанцию.

**Biography (EN):** Claude Mvemba guarded Grand Chien plantations with a shotgun and a firm belief that most trouble should be allowed to come closer. Conversation bores him; cigarettes do not. His crushed silver-coloured case still shuts with a satisfying click, though opening it now requires a thumbnail. Claude has little enthusiasm for distant contests, but among sheds, fences, and rows of cane he judges space with the ease of long habit.

**Профиль (RU):** Молчаливый сторож со смятым портсигаром и дробовиком

**Profile (EN):** A taciturn guard with a crushed cigarette case

### `JAZZ_AME_34` — Emeka Nwosu

- **Nationality:** `Nigeria`
- **Category / CombatRole:** Fighters / Machinegunner
- **Specialization:** `HeavyWeapons`
- **Level / Salary:** 1 / $107
- **Potential (Wisdom):** Low
- **Traits (common):** `HeavyWeaponsTraining`, `AutoWeapons`
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_34` ← donor `Soldier_Rebels` (male; blue recolor, source не править)
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

**Биография (RU):** Эмека Нвосу таскал груз в нигерийском порту, а затем оказался за пулемётом, потому что никто другой не хотел носить его достаточно долго. Он силён, упрям и не обижается на шутку, если успел рассказать её первым. Пустую патронную коробку Эмека использует как стул и подписал снизу: «не сдвигать вместе с хозяином». Тонкая работа ему чужда, зато тяжесть и долгий шум кажутся почти естественным продолжением его самого.

**Biography (EN):** Emeka Nwosu moved cargo on a Nigerian quay before someone noticed he could carry a machine gun farther than anyone else. Finesse never followed, but good humour did, especially when the joke concerns his immovable size. He sits on an empty ammunition box labelled underneath, “Do not relocate with owner.” Emeka struggles with delicate choices at distance, yet weight, recoil, and a stubborn patch of ground suit him perfectly.

**Профиль (RU):** Портовый силач на собственной патронной коробке

**Profile (EN):** A dockside strongman seated on his own ammunition box

### `JAZZ_AME_35` — Samuel Cheruiyot

- **Nationality:** `Kenya`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $78
- **Potential (Wisdom):** Medium
- **Traits (common):** —
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

**Биография (RU):** Сэмюэл Черуйот охотился в Кении задолго до того, как кто-то попытался научить его строевым словам. В лесу он лёгок, внимателен и предпочитает сделать паузу, а не исправлять поспешность новым выстрелом. На ремне его винчестера пришита пуговица из полированного рога, оставшаяся от первой куртки. Казарменная теснота быстро делает Сэмюэла раздражительным, зато на открытом воздухе он будто заранее знает, откуда появится движение.

**Biography (EN):** Samuel Cheruiyot learned Kenyan hunting trails before regulations, formations, or military vocabulary entered his life. Outdoors he is quick and watchful, taking the extra breath that impatient shooters resent. A polished horn button from his first hunting coat is sewn into the rifle sling. Barracks make Samuel restless and sharp-tongued, but give him a horizon and he seems to notice movement while everyone else is still deciding where to look.

**Профиль (RU):** Охотник, пришивший к ремню память о первой куртке

**Profile (EN):** A hunter carrying his first coat's button on the sling

### `JAZZ_AME_36` — Mamadou Traoré

- **Nationality:** `Mali`
- **Category / CombatRole:** Fighters / Autorifleman
- **Specialization:** `Autoriflemen`
- **Level / Salary:** 1 / $84
- **Potential (Wisdom):** Medium
- **Traits (common):** `AutoWeapons`
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

**Биография (RU):** Мамаду Траоре служил в малийском дорожном патруле и после смены разбирал соседские стволы, пока остальные спорили о вчерашней стрельбе. Он не мастер, но терпеливо запоминает, какая пружина куда возвращается, и редко выдаёт догадку за знание. Чужая отвёртка, обмотанная красной тканью, всегда лежит у него рядом с кусачками. Мамаду не схватывает ремонт мгновенно, зато после него простая неисправность обычно перестаёт повторяться.

**Biography (EN):** Mamadou Traoré began tending other men's weapons during quiet hours with a Malian road patrol. He is no gifted engineer, merely patient enough to remember which small part caused trouble last time. A mismatched screwdriver wrapped in red cloth shares his pocket with a wire cutter, both returned cleaner than received. Mamadou learns machinery by repetition rather than insight, but uncomplicated faults tend to stay fixed once his careful hands have visited.

**Профиль (RU):** Патрульный с чужой отвёрткой в красной ткани

**Profile (EN):** A patrolman with a borrowed screwdriver wrapped in red cloth

### `JAZZ_AME_37` — Felix Tshisekedi

- **Nationality:** `Congo`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $63
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low` → VR `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_37` ← donor `Soldier_Rebels_04` (male; blue recolor, source не править)
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

**Биография (RU):** Феликс Чисекеди провёл несколько лет на конголезском блокпосту, где одна смена редко оставляла другой воду, бинты или внятные объяснения. Он привык закрывать чужие мелкие промахи без жалоб и не считает это подвигом. В кармане Феликс носит обмылок в жестяной крышке, чтобы после перевязки руки не пахли железом. Ни одно дело не даётся ему блестяще, зато в плохой день он остаётся тем человеком, о котором не приходится тревожиться отдельно.

**Biography (EN):** Felix Tshisekedi served at a Congolese checkpoint where every shift inherited somebody else's empty canteen and unfinished chores. He became the man who tied a bandage, watched the road, and asked for the explanation later. A sliver of soap rides in a tin lid so he can scrub the iron smell from his hands. Felix offers no remarkable flourish, but difficult days improve simply because he does not become another problem to solve.

**Профиль (RU):** Надёжный человек блокпоста с обмылком в жестяной крышке

**Profile (EN):** A dependable checkpoint hand carrying soap in a tin lid

### `JAZZ_AME_38` — Noah van Wyk

- **Nationality:** `SouthAfrica`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $72
- **Potential (Wisdom):** Medium
- **Traits (common):** —
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

**Биография (RU):** Ноа ван Вик вырос на южноафриканской ферме, где соседи приходили к нему решать споры о воде и заблудившемся скоте. Он не повышает голос и не торопит ответ, поэтому даже старшие часто замолкают, когда Ноа начинает говорить. В карманном журнале рядом с датами посева он записывает обещания, данные людям. Стреляет он без показного блеска, но рядом с его спокойным порядком усталые товарищи реже делают глупости.

**Biography (EN):** Noah van Wyk was a South African farmer before neighbours began bringing him quarrels about water, fences, and wandering cattle. He speaks without hurry, leaving silence to do the pushing that louder men attempt themselves. His pocket ledger mixes planting dates with promises made to people, every fulfilled one neatly crossed through. Noah is a capable rather than dazzling shot, but tired companions often recover their sense when his plain voice gives the next step.

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

**Биография (RU):** Жозеф Мукенди получил кличку «Гиена» в Гранд-Шьен, устраивая засады, после которых противники сперва слышали смешок и лишь потом видели лицо. В тесном месте он действует быстро, грязно и без интереса к красивым правилам. Жозеф носит помятое карманное зеркальце и проверяет им дверные углы, прежде чем сунуться вперёд. Его решительность спасает чаще, чем осторожность, но иногда эти два слова он явно путает.

**Biography (EN):** In Grand Chien, Joseph “Hyena” Mukendi built ambushes so close that survivors remembered the laugh before the face. He fights with quick, practical cruelty and considers elegance a luxury for safer rooms. A dented pocket mirror lets him inspect a doorway without offering it his head. Joseph's nerve carries him through ugly moments, though the same appetite for nearness can place him where a wiser man would never have gone.

**Профиль (RU):** «Гиена» с карманным зеркалом для самых тесных дверей

**Profile (EN):** Hyena and his pocket mirror for dangerously close doors

### `JAZZ_AME_40` — Abraham Tekle

- **Nationality:** `Ethiopia`
- **Category / CombatRole:** Hardened / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $111
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `IMP_male_01` → VR `IMP_male_01`
- **Appearance:** `JAZZ_AME_40` ← donor `GrandChien_Demolition` (male; blue recolor, source не править)
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

**Биография (RU):** Абрахам Текле воевал в эфиопских горах и пережил отступление, о котором его бывшие товарищи до сих пор говорят только дома. Он дышит ровно, не торопит выстрел и принимает поражение как урок, а не личное оскорбление. На ночлеге Абрахам сворачивает старую шерстяную шапку в маленькую подушку, хотя давно может позволить себе лучшую. Лицо кажется усталым, но тело и привычки сохранили больше прочности, чем обещает первый взгляд.

**Biography (EN):** Abraham Tekle came out of an Ethiopian mountain campaign that ended with more men walking home than marching. Defeat made him quieter rather than bitter, and he waits for a clear sight instead of demanding one. His faded wool cap becomes a tiny pillow every night, a comfort kept from colder bivouacs. Abraham looks worn at first meeting, but hardship has left his frame and attention surprisingly difficult to shake.

**Профиль (RU):** Горный ветеран, спящий на свёрнутой шерстяной шапке

**Profile (EN):** A mountain veteran who sleeps on a folded wool cap

### `JAZZ_AME_41` — Sipho "Anvil" Khumalo

- **Nationality:** `SouthAfrica`
- **Category / CombatRole:** Hardened / Machinegunner
- **Specialization:** `HeavyWeapons`
- **Level / Salary:** 1 / $143
- **Potential (Wisdom):** Low
- **Traits (common):** `HeavyWeaponsTraining`, `AutoWeapons`
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

**Биография (RU):** Сифо «Наковальня» Кхумало служил в южноафриканском пулемётном расчёте и всегда получал ту часть ноши, которую остальные делили на двоих. Он двигается тяжело, мыслит прямыми линиями и не притворяется точным мастером одиночной цели. По вечерам Сифо неловко штопает ремни крошечным напёрстком, подаренным матерью, зажимая иглу огромными пальцами. Когда требуется долго удерживать тяжёлый ствол на одном направлении, его недостатки внезапно становятся почти неважны.

**Biography (EN):** Sipho “Anvil” Khumalo served on a South African gun crew where every oversized burden somehow found his shoulders. He thinks in straight lines, advances without grace, and knows better than to advertise himself as a fine shot. At camp he repairs webbing with his mother's tiny brass thimble, an absurd glint between enormous fingers. Sipho is slow to adapt, but once the heavy barrel settles, neither recoil nor argument moves him easily.

**Профиль (RU):** «Наковальня» с тяжёлым стволом и крошечным напёрстком

**Profile (EN):** Anvil, a heavy gun, and one tiny brass thimble

### `JAZZ_AME_42` — Boubacar Kane

- **Nationality:** `Senegal`
- **Category / CombatRole:** Hardened / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $107
- **Potential (Wisdom):** Medium
- **Traits (common):** —
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

**Биография (RU):** Бубакар Кане был офицером запаса в Сенегале и понял, что усталые люди лучше выполняют короткий приказ, смысл которого им объяснили. Он говорит спокойно, не тратит время на позу и сам проверяет путь, прежде чем отправить туда другого. Бубакар пишет распоряжения на внутренней стороне пустых сигаретных пачек и просит прочитавшего повторить их своими словами. Он не собирает вокруг себя восторгов, зато после суток рядом с ним позиции обычно остаются на месте.

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

**Биография (RU):** Дидье Мбемба по прозвищу «Дым» работал со взрывными зарядами в Конго и не раз исчезал из чужого поля зрения за пылью собственного дела. Он не любит бегать и предпочитает заранее знать, куда отступит после громкого хлопка. В кармане Дидье лежит обгоревший коробок спичек, на котором он каждый раз рисует новую стрелку выхода. Когда тишина уже потеряна, его расчётливое спокойствие оказывается полезнее скорости.

**Biography (EN):** Didier “Smoke” Mbemba earned his name around Congolese demolition work, repeatedly vanishing behind dust of his own making. Sprinting is not among his ambitions, so every loud solution begins with a carefully chosen way out. A scorched matchbox in his pocket receives a fresh escape arrow before each job. Didier can be ponderous while others still have options, but once silence is gone he becomes the calmest man in the noise.

**Профиль (RU):** «Дым» всегда рисует путь отхода на спичечном коробке

**Profile (EN):** Smoke always draws his exit on a scorched matchbox

### `JAZZ_AME_44` — Amina Yusuf

- **Nationality:** `Nigeria`
- **Category / CombatRole:** Hardened / Autorifleman
- **Specialization:** `Autoriflemen`
- **Level / Salary:** 1 / $123
- **Potential (Wisdom):** Medium
- **Traits (common):** `AutoWeapons`
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

**Биография (RU):** Амина Юсуф прошла несколько тяжёлых лет в нигерийской части и вынесла оттуда уважение к короткой очереди и чистой повязке. Она бережёт оружие без нежности, как вещь, которая обязана работать и не нуждается в комплиментах. Запасные бинты Амина заворачивает в вощёную бумагу и меняет свёрток после каждого дождя. Её холодный взгляд смущает новичков, зато рядом с кровью она остаётся собраннее многих разговорчивых ветеранов.

**Biography (EN):** Amina Yusuf learned soldiering in Nigeria through long weeks when ammunition, sleep, and clean cloth all had to be conserved. She treats her rifle as a duty rather than a companion and keeps every burst brief. Spare bandages remain sealed in waxed paper, inspected again whenever rain gets through the seams. Amina's reserve can feel severe across a table, but when somebody starts bleeding it becomes the steady distance needed to help.

**Профиль (RU):** Холодный взгляд, короткая очередь и сухие бинты

**Profile (EN):** A cool gaze, measured fire, and bandages kept dry

### `JAZZ_AME_45` — Léopold Sassou

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Hardened / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $115
- **Potential (Wisdom):** Low
- **Traits (common):** —
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

**Биография (RU):** Леопольд Сассу служил сержантом в Гранд-Шьен и слишком часто видел, как исправное оружие портят чужая лень и мелкая грязь. Он крепок, говорит ровно и без особого удовольствия чинит простые неполадки прямо на месте. В пустой сигарной трубке Леопольд носит тонкую щётку и каплю масла, защищённую пробкой. Для камеры он не улыбается, зато правильно вставший магазин способен вызвать у него редкое настоящее довольство.

**Biography (EN):** Sergeant Léopold Sassou spent his Grand Chien service rescuing rifles from dust, neglect, and owners who swore they had changed nothing. He is solid, unsentimental, and just skilled enough with simple faults to be dangerous to excuses. A fine cleaning brush and a corked drop of oil travel inside an empty cigar tube. Léopold rarely smiles for people, but a magazine seating cleanly on the first attempt can soften his entire face.

**Профиль (RU):** Сержант с оружейной щёткой в пустой сигарной трубке

**Profile (EN):** A sergeant carrying a cleaning brush inside a cigar tube

### `JAZZ_AME_46` — Kofi Mensah

- **Nationality:** `Ghana`
- **Category / CombatRole:** Hardened / Machinegunner
- **Specialization:** `HeavyWeapons`
- **Level / Salary:** 1 / $131
- **Potential (Wisdom):** Low
- **Traits (common):** `HeavyWeaponsTraining`
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

**Биография (RU):** Кофи Менса работал у портовой лебёдки в Гане, а затем носил тяжёлое оружие там, где раньше таскал канаты. Он огромен, нетороплив и не пытается догнать того, кого можно вынудить остановиться. Кофи всегда держит при себе моток грубой верёвки и чинит им ручки на ящиках, которые другие уже списали. Тонкий расчёт проходит мимо него, но вес, отдача и долгая неподвижная работа будто придуманы под его плечи.

**Biography (EN):** Kofi Mensah went from a Ghanaian dock winch to carrying guns that made ordinary men search for a second pair of hands. He is immensely built, slow to change direction, and uninterested in chasing what can be pinned down. Coarse rope rides at his waist for repairing crate handles everyone else has abandoned. Subtle plans can outrun Kofi's understanding, but weight and recoil seem to arrive at his shoulders already tamed.

**Профиль (RU):** Портовый силач с мотком верёвки для сломанных ящиков

**Profile (EN):** A dockside giant with rope for every broken crate

### `JAZZ_AME_47` — Hassan "Scorpion" Ibrahim

- **Nationality:** `Mali`
- **Category / CombatRole:** Hardened / Grenadier
- **Specialization:** `HeavyWeapons`
- **Level / Salary:** 1 / $139
- **Potential (Wisdom):** Medium
- **Traits (common):** `Throwing`
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_47` ← donor `GrandChien_Soldier` (male; blue recolor, source не править)
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

**Биография (RU):** Хассан Ибрахим получил кличку «Скорпион» в Мали за привычку появляться быстро и оставлять после себя неприятный сюрприз. Он двигается легче большинства старых служак, бросает уверенно и разговаривает так, будто каждую фразу снабдили жалом. В его спичечном блокноте на полях нарисованы скорпионы с разным выражением морды. Хассан любит точный момент взрыва чуть сильнее, чем безопасную дистанцию, и сам считает это частью обаяния.

**Biography (EN):** Hassan “Scorpion” Ibrahim carried messages between Malian outposts until his quick arrivals began including explosive replies. He moves lightly, throws with conviction, and keeps a sting ready for nearly every conversation. Tiny scorpions with different expressions crowd the margins of his matchbook notebook. Hassan understands timing better than caution and enjoys a well-placed blast enough to stand a little closer than sensible people prefer.

**Профиль (RU):** «Скорпион» рисует тёзок на полях спичечного блокнота

**Profile (EN):** Scorpion sketches namesakes in the margins of a matchbook

### `JAZZ_AME_48` — Patrick Omondi

- **Nationality:** `Kenya`
- **Category / CombatRole:** Hardened / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $119
- **Potential (Wisdom):** Medium
- **Traits (common):** `NightOps`
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

**Биография (RU):** Патрик Омонди много лет нёс ночную службу в Кении и научился различать по паузам, кто идёт в темноте уверенно, а кто притворяется. После заката он говорит шёпотом, но люди всё равно наклоняются ближе и слушают. Светящийся циферблат часов Патрик закрывает лоскутом чёрной ткани, поднимая его только под ладонью. Днём он кажется просто спокойным стрелком, зато ночь собирает его внимание в одну ясную линию.

**Biography (EN):** Patrick Omondi kept night posts in Kenya until footsteps became as distinct to him as daytime faces. He speaks softly after sunset, drawing tired people closer instead of competing with the dark. A strip of black cloth covers his luminous watch, lifted only beneath a cupped hand. In daylight Patrick is merely composed and competent; at night, patience, eyesight, and his quiet authority seem to arrive at the same point.

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

**Биография (RU):** Доктор Фатумата Си работала полевым хирургом в Сенегале, где операционный стол иногда собирали быстрее, чем подвозили чистую воду. В лазарете она говорит тихо, режет уверенно и особенно сердится на людей, считающих бинты признаком трусости. Красной перьевой ручкой Фатумата помечает карточки раненых и никогда не даёт её взаймы. Пистолет в её руке остаётся последней необходимостью, зато возле открытой раны сомнений у неё заметно меньше.

**Biography (EN):** Fatoumata Sy practised field surgery in Senegal through shortages that made clean water feel more precious than ammunition. Her voice drops when a ward grows frantic, forcing everyone nearby to listen instead of shout. A red fountain pen marks casualty notes and is the one possession she refuses to lend. Fatoumata handles a pistol with visible reluctance, but the moment a wound is uncovered her hesitation gives way to exact, unsparing purpose.

**Профиль (RU):** Полевой хирург с красной ручкой и тихим голосом

**Profile (EN):** A field surgeon with a red pen and a quiet voice

### `JAZZ_AME_50` — Grace Wanjiru

- **Nationality:** `Kenya`
- **Category / CombatRole:** Specialists / Medic
- **Specialization:** `Doctor`
- **Level / Salary:** 1 / $214
- **Potential (Wisdom):** High
- **Traits (common):** —
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

**Биография (RU):** Грейс Ванджиру была медсестрой в кенийском лазарете и однажды провела целую ночь при свете керосиновой лампы после аварии генератора. Она не носит оружия и не изображает, будто человеческая кровь перестала её трогать. Складывая повязки, Грейс тихо напевает старую радиозаставку, потому что ровный ритм успокаивает и её, и пациентов. В передней линии ей тесно и страшно, зато возле носилок паника обычно уступает место работе.

**Biography (EN):** Grace Wanjiru learned nursing in a Kenyan infirmary whose generator chose the busiest nights to fail. She has no interest in carrying a gun and no need to pretend that suffering has become ordinary. While folding dressings, Grace hums an old radio jingle until breathing around the cot begins to match its rhythm. Violence directed at her is frighteningly unfamiliar, but beside a patient she becomes the calm pair of hands everyone was looking for.

**Профиль (RU):** Медсестра, напевающая радиозаставку над чистыми повязками

**Profile (EN):** A nurse humming an old radio tune over clean dressings

### `JAZZ_AME_51` — Dr. Emile Kabongo

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Specialists / Medic
- **Specialization:** `Doctor`
- **Level / Salary:** 1 / $257
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_51` ← donor `Stormer_Rebels_02` (male; blue recolor, source не править)
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

**Биография (RU):** Доктор Эмиль Кабонго лечил дорожные травмы в Гранд-Шьен и слишком часто принимал пациентов, которых сперва перевязали добрыми, но неумелыми руками. Поэтому он учит каждого помощника простым узлам и повторяет объяснение без раздражения, пока тот не поймёт. За ухом Эмиль держит тупой плотницкий карандаш, которым рисует схемы прямо на упаковке бинтов. Оружие делает его скованным, зато сложная рана возвращает голосу и пальцам почти молодую точность.

**Biography (EN):** Emile Kabongo treated road injuries in Grand Chien, often undoing the generous mistakes of whoever reached the victim first. He began teaching simple bandaging wherever he went, patient with ignorance but not with carelessness. A blunt carpenter's pencil sits behind his ear for sketching knots on wrappers and walls. Years of emergencies have aged his face and slowed his step, yet a difficult wound still brings remarkable clarity to both his hands and instructions.

**Профиль (RU):** Травматолог, рисующий спасительные узлы тупым карандашом

**Profile (EN):** A trauma doctor sketching lifesaving knots with a blunt pencil

### `JAZZ_AME_52` — Captain Amara Koné

- **Nationality:** `Mali`
- **Category / CombatRole:** Specialists / Instructor
- **Specialization:** `Leader`
- **Level / Salary:** 1 / $264
- **Potential (Wisdom):** High
- **Traits (common):** `Teacher`
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

**Биография (RU):** Капитан Амара Коне обучала солдат в Мали и быстро потеряла терпение к строевому театру, который красиво выглядит только до первого раненого. Она разбирает ошибку жёстко, но объясняет её смысл, пока ученик не сможет повторить урок другому. Перед рассветом Амара ставит на огонь помятый чайник и заканчивает занятие лишь тогда, когда вода закипит. Сама она уже не так легка на ногах и не прячет этого, зато её правила переживают усталость лучше многих людей.

**Biography (EN):** Captain Amara Koné spent her Malian service turning nervous recruits into people who understood why a drill mattered. She has no patience for parade-ground drama, but an error receives explanation rather than humiliation. A battered kettle goes on before dawn lessons, and nobody leaves until its whistle closes the session. Amara's own body no longer demonstrates every movement gracefully, yet the habits she plants continue working when fear makes clever advice disappear.

**Профиль (RU):** Капитан, чей помятый чайник отмеряет уроки до рассвета

**Profile (EN):** A captain whose battered kettle keeps time for dawn lessons

### `JAZZ_AME_53` — Sgt. Nadia Okonkwo

- **Nationality:** `Nigeria`
- **Category / CombatRole:** Specialists / Instructor
- **Specialization:** `Leader`
- **Level / Salary:** 1 / $243
- **Potential (Wisdom):** High
- **Traits (common):** `Teacher`
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

**Биография (RU):** Сержант Надия Оконкво в Нигерии учила молодых солдат прицеливаться без спешки и никогда не путала преподавательский талант с собственной безошибочностью. Голос у неё резкий, объяснения ясные, а промах ученика интересует сильнее удачного выстрела перед начальством. Надия носит деревянную линейку со сколом и чертит ею направление прямо на земле. В долгом бою она устаёт раньше, чем признаётся, но рядом с ней чужие руки обычно перестают торопиться.

**Biography (EN):** Sergeant Nadia Okonkwo began teaching troops in Nigeria after discovering she could diagnose another shooter's mistake better than display perfection herself. Her voice carries, but the lesson beneath it is precise and free of vanity. A chipped wooden ruler draws sight lines in dust, on tables, or across the back of a map. Nadia cannot sustain every example she demands from younger bodies, yet pupils around her soon stop snatching at the moment of a shot.

**Профиль (RU):** Сержант с деревянной линейкой для ошибок на прицеле

**Profile (EN):** A sergeant who maps every mistake with a wooden ruler

### `JAZZ_AME_54` — Maj. Théodore Ngalula

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Specialists / Instructor
- **Specialization:** `Leader`
- **Level / Salary:** 1 / $286
- **Potential (Wisdom):** High
- **Traits (common):** `Teacher`
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

**Биография (RU):** Майор Теодор Нгалула обучал подразделения Гранд-Шьен и помнит, почему одни группы рассыпались через неделю, а другие выдерживали тяжёлый сезон. Он объясняет долго, чинит попавшуюся под руку мелочь и не повышает голос только ради звания. Складные очки Теодора держатся на проволоке, которую он однажды заменил сам и с тех пор упрямо не меняет. В движении возраст уже спорит с ним, зато в чужом плане он замечает слабое место раньше, чем молодые успевают заскучать.

**Biography (EN):** Major Théodore Ngalula spent his Grand Chien career teaching units how to remain a group after exhaustion stripped away ceremony. He repeats an explanation until it survives in ordinary language, often repairing some loose buckle while he talks. Wire holds one arm of his folding spectacles, a temporary fix he has refused to replace for years. Théodore moves like an older man now, but flawed plans still reveal themselves to him with uncomfortable speed.

**Профиль (RU):** Майор в починенных проволокой очках, видящий слабые планы

**Profile (EN):** A major in wire-mended spectacles who spots weak plans

### `JAZZ_AME_55` — Issa Camara

- **Nationality:** `Senegal`
- **Category / CombatRole:** Specialists / Sniper
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $200
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_55` ← donor `Legion_Jose` (male; blue recolor, source не править)
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

**Биография (RU):** Исса Камара нёс наблюдение на севере Сенегала, где редкий выстрел был полезнее долгой перестрелки на жаре. Он бережёт дыхание, не участвует в беготне и честно предупреждает, что штурмовая работа создана для других. На ремне его винтовки висит гладкая деревянная бусина, которую Исса перекатывает пальцем во время ожидания. Тело у него хрупкое, зато терпение позволяет закончить дело прежде, чем оно успеет потребовать от него лишнего.

**Biography (EN):** Issa Camara watched a northern Senegalese road where heat punished movement and one careful shot could end an afternoon's danger. He accepts his narrow frame without shame and leaves rushing to people built for it. A smooth wooden bead slides along the rifle sling beneath his thumb during long waits. Issa suffers quickly when a position turns into a brawl, but few men are better at preventing the quiet moment from becoming one.

**Профиль (RU):** Терпеливый стрелок с деревянной бусиной на ремне

**Profile (EN):** A patient shooter with one wooden bead on his sling

### `JAZZ_AME_56` — Lindiwe Mokoena

- **Nationality:** `SouthAfrica`
- **Category / CombatRole:** Specialists / Sniper
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $243
- **Potential (Wisdom):** Medium
- **Traits (common):** `NightOps`
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

**Биография (RU):** Линдиве Мокоена работала ночным наблюдателем в Южной Африке и полюбила часы, когда лишний блеск выдаёт человека раньше движения. Она говорит коротко, не обещает чудес и выбирает путь, на котором не придётся бороться с собственной хрупкостью. Маленькой банкой матовой краски Линдиве закрывает свежие царапины на металле ещё до наступления темноты. Дневная суета утомляет её, зато ночью внимание становится тихим и острым.

**Biography (EN):** Lindiwe Mokoena learned night observation in South Africa, where a bright scratch could betray more than a careless footstep. She is reserved, realistic, and careful not to confuse courage with carrying too much. A tiny jar of matte black paint comes out before dusk to cover every fresh glint on metal. Daylight bustle drains Lindiwe quickly, but darkness narrows the world into patient shapes she can read with unusual confidence.

**Профиль (RU):** Ночная наблюдательница с банкой матовой чёрной краски

**Profile (EN):** A night watcher with a tiny jar of matte black paint

### `JAZZ_AME_57` — Bakary Diarra

- **Nationality:** `Mali`
- **Category / CombatRole:** Specialists / Sapper
- **Specialization:** `ExplosiveExpert`
- **Level / Salary:** 1 / $171
- **Potential (Wisdom):** Medium
- **Traits (common):** `Throwing`
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_57` ← donor `Legion_Artillery` (male; blue recolor, source не править)
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

**Биография (RU):** Бакари Диарра работал с дорожными зарядами в Мали и однажды променял пистолет на коробку хороших детонаторов, о чём не пожалел. Провода и взрыватели понятнее ему, чем перестрелка, где опасность не ждёт разрешения. Детонаторы Бакари держит в старой сигаретной жестянке, переложенной хлопком, и перед делом стучит ногтем по крышке. Рядом с подготовленным зарядом руки у него спокойны, но летящая пуля мгновенно напоминает, насколько он не любит случайность.

**Biography (EN):** Bakary Diarra cleared and placed road charges in Mali before trading away his pistol for detonators he considered far more useful. Wires obey sequence; gunfire does not, and that distinction matters to him. His detonators rest in a cotton-lined cigarette tin whose lid receives one nervous tap before work. Bakary is composed beside a device he understands, but uncontrolled danger exposes how much of his confidence depends on having prepared the ground himself.

**Профиль (RU):** Дорожный подрывник с детонаторами в хлопковой жестянке

**Profile (EN):** A road blaster keeping detonators in a cotton-lined tin

### `JAZZ_AME_58` — Marie-Claire Mbala

- **Nationality:** `Congo`
- **Category / CombatRole:** Specialists / Sapper
- **Specialization:** `ExplosiveExpert`
- **Level / Salary:** 1 / $214
- **Potential (Wisdom):** Medium
- **Traits (common):** `Throwing`
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

**Биография (RU):** Мари-Клер Мбала работала с карьерными зарядами в Конго, а затем перенесла своё сухое ремесло туда, где камень отвечал реже людей. Она не любит поэзию вокруг взрывчатки и заставляет новичков сперва назвать путь отхода. Портновская лента Мари-Клер измеряет шнур точнее любого шага и всегда свёрнута в левом кармане. Любопытная загадка иногда подводит её слишком близко, зато после первого взгляда она редко путает опасный узел с безобидным.

**Biography (EN):** Marie-Claire Mbala began around Congolese quarry charges, learning that explosives reward plain measurements and punish romantic language. Her manner is dry, her questions direct, and every newcomer must identify the exit before touching a wire. A tailor's tape coils in her left pocket for measuring fuse instead of trusting footsteps. Marie-Claire can lean too close when a device puzzles her, but once she understands its logic, hesitation no longer wastes anyone's time.

**Профиль (RU):** Сухой характер и портновская лента для опасных узлов

**Profile (EN):** A dry wit and a tailor's tape for dangerous puzzles

### `JAZZ_AME_59` — Ousmane Fall

- **Nationality:** `Senegal`
- **Category / CombatRole:** Specialists / Mechanic
- **Specialization:** `Mechanic`
- **Level / Salary:** 1 / $157
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Hard` → VR `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_59` ← donor `Legion_Artillery02` (male; blue recolor, source не править)
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

**Биография (RU):** Усман Фалл чинил автобусы в Сенегале, а затем обнаружил, что оружие ломается по тем же причинам: грязь, спешка и уверенный хозяин. Геройствовать он не хочет и в перестрелке ищет ближайшее твёрдое укрытие без малейшего стыда. Намагниченная чайная ложка Усмана собирает винты, которые иначе исчезли бы в пыли мастерской. Пока другие спорят о смелости, он возвращает в строй вещи, без которых спорщикам скоро пришлось бы идти пешком.

**Biography (EN):** Ousmane Fall repaired Senegalese buses before turning to weapons, discovering the same enemies in both trades: dirt, haste, and proud owners. He wants no part in heroics and finds solid cover with admirable honesty when bullets start moving. A magnetised teaspoon gathers screws from the dust beside his tools. Ousmane looks awkward in a fight, but after one he is often the first person everyone needs and the last one foolish enough to boast.

**Профиль (RU):** Автобусный мастер, собирающий винты намагниченной ложкой

**Profile (EN):** A bus-yard repairman gathering screws with a magnetised spoon

### `JAZZ_AME_60` — Jean-Pierre Kalala

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Specialists / Mechanic
- **Specialization:** `Mechanic`
- **Level / Salary:** 1 / $200
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `PierreMerc` → VR `PierreMerc`
- **Appearance:** `JAZZ_AME_60` ← donor `Legion_Artillery03` (male; blue recolor, source не править)
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

**Биография (RU):** Жан-Пьер Калала держал гараж в Гранд-Шьен и научился распознавать клиента, который уже пытался чинить всё сам, ещё по звуку шагов. Замки он слушает терпеливо, а оружие берёт только затем, чтобы освободить дорогу к работе. На запястье Жан-Пьера завязана синяя ветошь, которой он протирает инструменты перед тем, как убрать их по местам. Двигается он неспешно и стреляет неохотно, зато закрытая дверь редко остаётся для него последним словом.

**Biography (EN):** Jean-Pierre Kalala ran a Grand Chien garage and could identify a customer's failed home repair before the man finished crossing the floor. He listens to locks with the same patience once reserved for stubborn engines. A blue shop rag is knotted around his wrist, used to wipe every tool before it returns to its place. Jean-Pierre is slow and thoroughly uncomfortable with gunfire, but a closed mechanism seldom keeps its secrets from him for long.

**Профиль (RU):** Гаражный мастер с синей ветошью и терпением к замкам

**Profile (EN):** A garage master with a blue rag and patience for locks

