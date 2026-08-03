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
- Voice: Irregulars/Fighters → `Jazz_AME_Male_Low` (Legion phrases + alt `*-1.opus`); Hardened/Specialists → `Jazz_AME_Male_Hard`; female → `Jazz_AME_Female`.
- **Bio:** полная игровая проза карточки найма (RU); без мета-цифр статов/тиров.
- Nick: в основном Hardened. Grand Chien: заметная доля.

## Irregulars

### `JAZZ_AME_01` — Kwame Mensah

- **Nationality:** `Ghana`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $80
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
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

**Биография:** Кваме Менса вырос в Аккре и годы ходил в дружинном патруле, пока кому-то не надоело платить. Он крепкий, спокойный и внимательный — слушает больше, чем говорит, — а стрелять его учили урывками, между сменами. Теперь ищет нормальную работу: не очередной пост у склада, а дело, за которое не стыдно взять деньги.

### `JAZZ_AME_02` — Jean-Baptiste Okoro

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $88
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
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

**Биография:** Жан-Батист Окоро — охотник из Гранд-Шьен. Когда зверь ушёл дальше, чем позволяла лицензия, он остался с опустевшей сумкой и привычкой считать каждый выстрел. Крадётся тихо, смотрит зорко, а про шумные автоматы говорит с недоверием. Хочет снова есть регулярно — без вопросов, откуда добыча.

### `JAZZ_AME_03` — Ibrahim Touré

- **Nationality:** `Mali`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $96
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
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

**Биография:** Ибрахим Туре служил постовым в Мали: разнимал драки, выписывал протоколы и умел успокоить толпу голосом, а не дубинкой. Когда участок сократили, он ушёл с привычкой перевязывать чужие ссадины и со служебным револьвером на память. Стреляет посредственно и сам это знает — зато не паникует, когда вокруг кричат.

### `JAZZ_AME_04` — Sani Abubakar

- **Nationality:** `Nigeria`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $104
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
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

**Биография:** Сани Абубакар — новобранец без полка. Руки сильные: таскал мешки, ломал двери, помогал на стройке казармы. Нервы тоньше тела — от чужого крика сжимается раньше, чем успевает подумать. Честно говорит, что учиться придётся на ходу, и всё равно просится в дело.

### `JAZZ_AME_05` — Pierre Ndongo

- **Nationality:** `Congo`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $112
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
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

**Биография:** Пьер Ндонго молчал на блокпостах Конго так долго, что коллеги перестали ждать от него шуток. Голова варит быстрее рук: запоминает лица, маршруты, кто кому должен. Оружие сдал при увольнении, карманы пусты, взгляд цепкий. Лучше слушает, чем стреляет — пока.

### `JAZZ_AME_06` — Moussa Diop

- **Nationality:** `Senegal`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $120
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
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

**Биография:** Мусса Диоп из Сенегала ходил следами лучше, чем по асфальту. Дед оставил ему старый винчестер — и Мусса бережёт его так, будто это последний родственник. Не любит шумные компании, патроны считает заранее. Говорит, что лес его ещё не отпустил — просто теперь добыча иногда ходит на двух ногах.

### `JAZZ_AME_07` — Abel Getachew

- **Nationality:** `Ethiopia`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $128
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
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

**Биография:** Абель Гетачью сбежал с учений в Эфиопии раньше, чем успел привыкнуть к строевой. Учится быстро: один раз покажи — и уже повторяет, пусть и криво. Попадает редко — руки ещё не поймали ритм. Упрямство у него сильнее опыта: хочет доказать, что из него выйдет солдат, а не вечный дезертир.

### `JAZZ_AME_08` — Thabo Molefe

- **Nationality:** `SouthAfrica`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $136
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
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

**Биография:** Табо Молефе патрулировал фермы в Южной Африке: пугал воров, таскал мешки и спал в сарае. Корпус крепкий, шаг тяжёлый; дальше простого ружья ему ничего не выдавали — «хватит и так». У ворот стоит спокойно и от первого хлопка не бежит.

### `JAZZ_AME_09` — Daniel Kiprop

- **Nationality:** `Kenya`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $80
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
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

**Биография:** Даниэль Кипроп — егерь из Кении: глаза замечают движение раньше звука. Тело худое, выносливость охотничья, а не казарменная. О хорошей винтовке мечтал — дали то, что было. Ему важнее увидеть первым, чем носить красивую форму.

### `JAZZ_AME_10` — Emmanuel Kabongo

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $88
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
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

**Биография:** Эммануэль Кабонго водил связных по тропам Гранд-Шьен и знал, где не стоит шуметь после заката. Люди его слушают чуть-чуть — не как офицера, а как того, кто уже проводил таких же потерянных. Стрелять почти не умеет, зато тропы помнит лучше карт.

### `JAZZ_AME_11` — Aisha Hassan

- **Nationality:** `Kenya`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $96
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Voice:** `Jazz_AME_Female`
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

**Биография:** Аиша Хассан грузила ящики в кенийском порту, пока не поняла: спина ещё терпит, а нервы — уже нет. Хрупкая и вспыльчивая: любой резкий звук заставляет вздрагивать. Хочет уехать от порта подальше — даже если первая работа окажется самой грязной.

### `JAZZ_AME_12` — Amadou Keita

- **Nationality:** `Mali`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $104
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
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

**Биография:** Амаду Кейта — деревенский дружинник из Мали. Сильный, привыкший работать руками, боится взрывчатки до дрожи: однажды видел, как мина разорвала телегу, и с тех пор обходит подозрительную землю по широкой дуге. Простую работу без «сюрпризов» делает лучше многих храбрецов.

### `JAZZ_AME_13` — Chidi Okonkwo

- **Nationality:** `Nigeria`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $112
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
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

**Биография:** Чиди Оконкво провалил медкомиссию армии Нигерии — сердце «не то», бумаги «не те». Зато пальцы ловкие: вскрывал ящики улик, чинил замки, однажды утащил из архива старый служебный револьвер. Чуть понимает в механизмах, больше — в том, как не попасться.

### `JAZZ_AME_14` — Lucien Mbarga

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $120
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
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

**Биография:** Люсьен Мбарга браконьерствовал в Гранд-Шьен, пока рейнджеры не отняли ружьё и не пообещали тюрьму при следующей встрече. Осталась привычка ходить тихо. Не герой и не кается вслух — просто ищет оплату там, где никто не спрашивает про лицензии.

### `JAZZ_AME_15` — Kofi Asante

- **Nationality:** `Ghana`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $128
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
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

**Биография:** Кофи Асанте сторожил школу в Гане и читал всё, что забывали на партах. Соображает отлично — схватывает быстрее многих «настоящих» бойцов, — но руками почти не владеет. Спокойно учится на чужих ошибках, лишь бы платили и давали шанс.

### `JAZZ_AME_16` — João Domingos

- **Nationality:** `Angola`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $136
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
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

**Биография:** Жуан Домингос из Анголы один раз видел мины — и этого хватило, чтобы навсегда обходить рыхлую землю стороной. Медленный, упрямый и честно боится взрывов. Врать про храбрость не станет — и за это его иногда ценят больше, чем за смелость.

### `JAZZ_AME_17` — Wanjiku Mwangi

- **Nationality:** `Kenya`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $80
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Voice:** `Jazz_AME_Female`
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

**Биография:** Ванджику Мванги помогала егерю в Кении: чистила следы, носила воду, дежурила на опушке. Зоркая и лёгкая на ногу, без громких обещаний. Привыкла, что работа грязная, а деньги маленькие — и всё равно делает её тихо и до конца.

### `JAZZ_AME_18` — Serge Kouassi

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $88
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
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

**Биография:** Серж Куасси — сын механика из Гранд-Шьен, и отцу за него стыдно: отвёртку Серж не берёт. Голова светлая, рук нет — зато вопросы задаёт правильные. Хочет доказать, что ум тоже бывает оружием, даже если карманы пока пусты.

### `JAZZ_AME_19` — Bongani Dlamini

- **Nationality:** `SouthAfrica`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $96
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
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

**Биография:** Бонгани Дламини работал на шахтёрской дружине в Южной Африке: таскал мешки, не бегал кроссы и спал кусками между сменами. Тяжёлый, молчаливый, привыкший к пыли. У двери стоит так, что объяснять дважды не приходится.

### `JAZZ_AME_20` — Idrissa Bah

- **Nationality:** `Senegal`
- **Category / CombatRole:** Irregulars / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $104
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
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

**Биография:** Идрисса Бах регулировал движение в Сенегале лучше, чем стрелял: жестами командовал так, что даже пьяные водители иногда слушались. Не герой перестрелок — зато умеет остановить хаос на секунду дольше, чем другие.

## Fighters

### `JAZZ_AME_21` — Omar Diallo

- **Nationality:** `Senegal`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $220
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_21` ← donor `Legion_Artillery` (male; blue recolor, source не править)
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

**Биография:** Омар Диалло дезертировал из сенегальской части, когда понял, что легион зовёт громче командования. Отказался — и ушёл с привычкой целиться один раз, но точно. Не орёт, не хвастается: делает работу и считает патроны.

### `JAZZ_AME_22` — Bastien Lafontaine

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Fighters / Autorifleman
- **Specialization:** `Autoriflemen`
- **Level / Salary:** 1 / $240
- **Potential (Wisdom):** Medium
- **Traits (common):** `AutoWeapons`
- **Voice:** `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_22` ← donor `Legion_Artillery02` (male; blue recolor, source не править)
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

**Биография:** Бастьен Лафонтен служил милицейским автоматчиком в Гранд-Шьен и до сих пор пахнет машинным маслом и дешёвым табаком. Очереди для него важнее красоты ствола: улица становится тесной — и он уже на линии. Платят лучше участка — и этого ему достаточно.

### `JAZZ_AME_23` — Chukwuemeka Obi «Emeka»

- **Nationality:** `Nigeria`
- **Category / CombatRole:** Fighters / Machinegunner
- **Specialization:** `HeavyWeapons`
- **Level / Salary:** 1 / $260
- **Potential (Wisdom):** Medium
- **Traits (common):** `HeavyWeaponsTraining`, `AutoWeapons`
- **Voice:** `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_23` ← donor `Legion_Artillery03` (male; blue recolor, source не править)
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

**Биография:** Чуквуэмека Оби сидел на пулемётной точке нигерийского блокпоста, пока блокпост не стёрли с карты. Крепкий, тяжёлый, бьёт по земле увереннее, чем по мишеням — и сам над этим иногда шутит. Закрыть сектор огнём для него привычнее, чем выигрывать конкурс стрелков.

### `JAZZ_AME_24` — Michel Kabeya

- **Nationality:** `Congo`
- **Category / CombatRole:** Fighters / Grenadier
- **Specialization:** `ExplosiveExpert`
- **Level / Salary:** 1 / $250
- **Potential (Wisdom):** Medium
- **Traits (common):** `Throwing`
- **Voice:** `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_24` ← donor `Legion_Demolishion` (male; blue recolor, source не править)
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

**Биография:** Мишель Кабейа из Конго всегда любил банки больше стволов. Настоящая работа для него начинается, когда свистит чека. Шумный в баре и тихий перед броском — и не притворяется героем.

### `JAZZ_AME_25` — Juma Otieno

- **Nationality:** `Kenya`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $200
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_25` ← donor `Legion_Demolishion02` (male; blue recolor, source не править)
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

**Биография:** Джума Отиено служил на кенийской границе: лёгкий на ногу, привыкший к пыли и долгим сменам. Дальнюю винтовку ему не доверили — приказали не геройствовать. Не обижается: главное — увидеть первым. Скорость ног для него важнее красивой стойки.

### `JAZZ_AME_26` — Andile Nkosi

- **Nationality:** `SouthAfrica`
- **Category / CombatRole:** Fighters / Autorifleman
- **Specialization:** `Autoriflemen`
- **Level / Salary:** 1 / $230
- **Potential (Wisdom):** Medium
- **Traits (common):** `AutoWeapons`
- **Voice:** `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_26` ← donor `Legion_Demolishion03` (male; blue recolor, source не править)
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

**Биография:** Андиле Нкоси охранял конвои в Южной Африке и научился стрелять очередями так, чтобы охраняемый груз не превращался в решето раньше времени. Спокоен, немногословен и не любит, когда новички трогают его оружие «просто посмотреть».

### `JAZZ_AME_27` — Sekou Camara

- **Nationality:** `Mali`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $190
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_27` ← donor `Legion_Heavy` (male; blue recolor, source не править)
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

**Биография:** Секу Камара патрулировал пустыню в Мали и не считал короткий ствол унижением. Подвижный, с нервами крепче, чем у многих «настоящих» стрелков, умеет смещаться и не торчать на открытом месте. Доходит туда, куда тяжёлые ребята только собираются.

### `JAZZ_AME_28` — Pascal Ngoma

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Fighters / Machinegunner
- **Specialization:** `HeavyWeapons`
- **Level / Salary:** 1 / $270
- **Potential (Wisdom):** Medium
- **Traits (common):** `HeavyWeaponsTraining`
- **Voice:** `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_28` ← donor `Legion_Heavy02` (male; blue recolor, source не править)
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

**Биография:** Паскаль Нгома держал огневую точку в Гранд-Шьен с характером человека, который не любит бегать. Тяжёлый, упрямый: закрывает сектор и ждёт, пока сектор перестанет шевелиться. Под огнём не дёргается первым — и этим уже выигрывает время для остальных.

### `JAZZ_AME_29` — Kwesi Boateng

- **Nationality:** `Ghana`
- **Category / CombatRole:** Fighters / Grenadier
- **Specialization:** `ExplosiveExpert`
- **Level / Salary:** 1 / $255
- **Potential (Wisdom):** Medium
- **Traits (common):** `Throwing`, `HeavyWeaponsTraining`
- **Voice:** `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_29` ← donor `Legion_Heavy03` (male; blue recolor, source не править)
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

**Биография:** Квеси Боатенг из Ганы любит короткую работу и тяжёлую ладонь на банке. Взрывчатки у него немного, зато бросок уверенный — как у человека, который тренировался на пустых бутылках за складом. Улыбается редко и работает быстро: пришёл, бросил, ушёл, пока эхо ещё гуляет.

### `JAZZ_AME_30` — Tesfaye Alemu

- **Nationality:** `Ethiopia`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $210
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_30` ← donor `Legion_Jose` (male; blue recolor, source не править)
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

**Биография:** Тесфайе Алем — горный стрелок из Эфиопии. Целится аккуратно, дышит ровно и не делает вид, что ему «просто забыли» выдать лучшее оружие. Хороший глаз, скромные ожидания, готов учиться на том, что дадут.

### `JAZZ_AME_31` — Rafael dos Santos

- **Nationality:** `Angola`
- **Category / CombatRole:** Fighters / Autorifleman
- **Specialization:** `Autoriflemen`
- **Level / Salary:** 1 / $235
- **Potential (Wisdom):** Medium
- **Traits (common):** `AutoWeapons`
- **Voice:** `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_31` ← donor `Legion_Marksman` (male; blue recolor, source не править)
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

**Биография:** Рафаэль дос Сантос из Анголы учится медленнее иных, зато не ломается от первой тяжёлой недели. Очереди для него — ремесло, выученное кровью и пылью. Не обещает чудес. Обещает явиться трезвым и не бросить позицию без приказа.

### `JAZZ_AME_32` — Awa Sow

- **Nationality:** `Senegal`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $180
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Female`
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

**Биография:** Ава Соу из Сенегала попала в тесные коридоры не по любви, а по расписанию смен. Юркая и нервная, без армейской школы длинных очередей — зато живее многих «правильных» автоматчиков. Держится особняком и ненавидит, когда мужчины объясняют ей, как «правильно» стрелять.

### `JAZZ_AME_33` — Claude Mvemba

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $200
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_33` ← donor `Legion_Marksman02` (male; blue recolor, source не править)
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

**Биография:** Клод Мвемба охранял плантации в Гранд-Шьен — привык к дроби, не к оптике. Говорит мало, курит много, считает, что хороший выстрел тот, после которого никто не спорит. Работает ближе, чем любят дальние стрелки, и дальше, чем удобно трусам.

### `JAZZ_AME_34` — Emeka Nwosu

- **Nationality:** `Nigeria`
- **Category / CombatRole:** Fighters / Machinegunner
- **Specialization:** `HeavyWeapons`
- **Level / Salary:** 1 / $280
- **Potential (Wisdom):** Low
- **Traits (common):** `HeavyWeaponsTraining`, `AutoWeapons`
- **Voice:** `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_34` ← donor `Legion_Marksman03` (male; blue recolor, source не править)
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

**Биография:** Эмека Нвосу — силач с нигерийским характером: здоровье и упрямство у него заметнее меткости, и он не стесняется этого. Про него шутят, что его проще нанять, чем сдвинуть. Он не возражает — лишь бы платили вовремя.

### `JAZZ_AME_35` — Samuel Cheruiyot

- **Nationality:** `Kenya`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $215
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_35` ← donor `Legion_Recon` (male; blue recolor, source не править)
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

**Биография:** Сэмюэл Черуйот охотился в Кении раньше, чем научился читать уставы. Охотничья винтовка ему роднее любой казённой; с длинным болтом не заигрывает и без зависти. Быстрый, зоркий, с привычкой целиться перед выстрелом. Любит воздух чаще, чем порох казармы.

### `JAZZ_AME_36` — Mamadou Traoré

- **Nationality:** `Mali`
- **Category / CombatRole:** Fighters / Autorifleman
- **Specialization:** `Autoriflemen`
- **Level / Salary:** 1 / $225
- **Potential (Wisdom):** Medium
- **Traits (common):** `AutoWeapons`
- **Voice:** `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_36` ← donor `Legion_Recon02` (male; blue recolor, source не править)
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

**Биография:** Мамаду Траоре из Мали чинит стволы соседей чаще, чем хвастается своими. Отвёртка часто чужая, зато руки помнят, куда крутить. После боя ещё и собирает то, что осталось стрелять.

### `JAZZ_AME_37` — Felix Tshisekedi

- **Nationality:** `Congo`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $195
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_37` ← donor `Legion_Recon03` (male; blue recolor, source не править)
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

**Биография:** Феликс Чисекеди — человек конголезского блокпоста: перевяжет рану, закроет сектор, не будет спрашивать, почему смена опять без воды. Не гений ни в чём — зато не провал ни в чём. Командиры любят таких именно за отсутствие сюрпризов.

### `JAZZ_AME_38` — Noah van Wyk

- **Nationality:** `SouthAfrica`
- **Category / CombatRole:** Fighters / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $205
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Low`
- **Appearance:** `JAZZ_AME_38` ← donor `Legion_Shaman` (male; blue recolor, source не править)
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

**Биография:** Ноа ван Вик — фермерский стрелок из Южной Африки с голосом, к которому прислушиваются даже те, кто старше. Люди его слушают не из страха — из привычки, что он говорит по делу. Меньше позы, больше работы.

## Hardened

### `JAZZ_AME_39` — Joseph Mukendi «Hyena»

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Hardened / Autorifleman
- **Specialization:** `Autoriflemen`
- **Level / Salary:** 1 / $480
- **Potential (Wisdom):** Low
- **Traits (common):** `AutoWeapons`, `CQCTraining`
- **Voice:** `Jazz_AME_Male_Hard`
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

**Биография:** Жозефа Мукенди в Гранд-Шьен зовут «Гиена»: годами делал засады так, что жертвы узнавали кличку раньше лица. В тесноте бьёт грязно и быстро — красивой стрельбы меньше, зато чаще остаётся живым. Нервы держат. Знает себе цену и не любит, когда её занижают.

### `JAZZ_AME_40` — Abraham Tekle

- **Nationality:** `Ethiopia`
- **Category / CombatRole:** Hardened / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $420
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Hard`
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

**Биография:** Абрахам Текле — горный ветеран из Эфиопии. Дышит ровно, ждёт, бьёт; уставы помнит хуже, чем привычку к прицелу. Корпус крепче, чем кажется по лицу. Уже видел поражение — и не сломался.

### `JAZZ_AME_41` — Sipho Khumalo «Anvil»

- **Nationality:** `SouthAfrica`
- **Category / CombatRole:** Hardened / Machinegunner
- **Specialization:** `HeavyWeapons`
- **Level / Salary:** 1 / $520
- **Potential (Wisdom):** Low
- **Traits (common):** `HeavyWeaponsTraining`, `AutoWeapons`
- **Voice:** `Jazz_AME_Male_Hard`
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

**Биография:** Сифо Кхумало, «Наковальня», тащит тяжесть так, будто мир обязан подождать. Тяжёлый ствол и очереди делают своё дело — и меткость от этого страдает, он знает. Не спорит: его работа — давить сектор, а не выигрывать тир.

### `JAZZ_AME_42` — Boubacar Kane

- **Nationality:** `Senegal`
- **Category / CombatRole:** Hardened / Rifle
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $400
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Hard`
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

**Биография:** Бубакар Кане — офицер запаса из Сенегала со спокойным прицелом. С людьми получается чуть лучше, чем у многих ветеранов: объяснит задачу так, что даже усталые кивают. Не орёт. Не геройствует. За сутки на старшего позицию обычно оставляет целой.

### `JAZZ_AME_43` — Didier Mbemba «Smoke»

- **Nationality:** `Congo`
- **Category / CombatRole:** Hardened / Grenadier
- **Specialization:** `ExplosiveExpert`
- **Level / Salary:** 1 / $500
- **Potential (Wisdom):** Low
- **Traits (common):** `Throwing`, `HeavyWeaponsTraining`
- **Voice:** `Jazz_AME_Male_Hard`
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

**Биография:** Дидье Мбемба, «Дым», из Конго приходит с банками и уходит в дыму, который сам же и ставит. Не спринтер — зато сектор задымления знает наизусть. Когда тишина уже не вариант, он как раз на месте.

### `JAZZ_AME_44` — Amina Yusuf

- **Nationality:** `Nigeria`
- **Category / CombatRole:** Hardened / Autorifleman
- **Specialization:** `Autoriflemen`
- **Level / Salary:** 1 / $450
- **Potential (Wisdom):** Medium
- **Traits (common):** `AutoWeapons`
- **Voice:** `Jazz_AME_Female`
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

**Биография:** Амина Юсуф бережёт хороший автомат и бинты в кармане — ветераны дольше живут, когда не стесняются собственной крови. Очереди короткие, взгляд холодный. Про неё говорят мало и уважительно — так безопаснее.

### `JAZZ_AME_45` — Léopold Sassou

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Hardened / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $430
- **Potential (Wisdom):** Low
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Hard`
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

**Биография:** Леопольд Сассу — сержант Гранд-Шьен с тяжёлым корпусом, ровным прицелом и чуточкой механики, достаточной, чтобы ствол соседа не клинил в самый плохой момент. Не улыбается для камеры. Улыбается, когда магазин встаёт с первого раза.

### `JAZZ_AME_46` — Kofi Mensah

- **Nationality:** `Ghana`
- **Category / CombatRole:** Hardened / Machinegunner
- **Specialization:** `HeavyWeapons`
- **Level / Salary:** 1 / $490
- **Potential (Wisdom):** Low
- **Traits (common):** `HeavyWeaponsTraining`
- **Voice:** `Jazz_AME_Male_Hard`
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

**Биография:** Кофи Менса из Ганы — силач: здоровье и мощь замечают раньше, чем меткость. Не догоняет — занимает место и делает его непригодным для врага. Там, где нужна тяжесть, а не грация, он уместен.

### `JAZZ_AME_47` — Hassan Ibrahim «Scorpion»

- **Nationality:** `Mali`
- **Category / CombatRole:** Hardened / Grenadier
- **Specialization:** `ExplosiveExpert`
- **Level / Salary:** 1 / $510
- **Potential (Wisdom):** Medium
- **Traits (common):** `Throwing`
- **Voice:** `Jazz_AME_Male_Hard`
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

**Биография:** Хассана Ибрахима в Мали зовут «Скорпион»: быстрее многих ветеранов, с ухмылкой человека, который любит, когда взрыв случается вовремя. Бросок уверенный, характер ядовитый. Кличка известнее имени — и он над этим не работает.

### `JAZZ_AME_48` — Patrick Omondi

- **Nationality:** `Kenya`
- **Category / CombatRole:** Hardened / Rifle
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $440
- **Potential (Wisdom):** Medium
- **Traits (common):** `NightOps`
- **Voice:** `Jazz_AME_Male_Hard`
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

**Биография:** Патрик Омонди — ночной стрелок из Кении со спокойным голосом, к которому прислушиваются даже уставшие. Лучше видит в темноте и лучше ждёт. После заката говорит шёпотом так, что всё равно слушаются.

## Specialists

### `JAZZ_AME_49` — Dr. Fatoumata Sy

- **Nationality:** `Senegal`
- **Category / CombatRole:** Specialists / Medic
- **Specialization:** `Doctor`
- **Level / Salary:** 1 / $950
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Voice:** `Jazz_AME_Female`
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

**Биография:** Доктор Фатумата Си — полевой хирург из Сенегала. Руки лечат, не стреляют; пистолет носит скорее для страха и редкой необходимости. В лазарете говорит тихо, режет уверенно и ненавидит, когда «герои» приходят без бинтов. Считает, что живые бойцы дороже мёртвых легенд.

### `JAZZ_AME_50` — Grace Wanjiru

- **Nationality:** `Kenya`
- **Category / CombatRole:** Specialists / Medic
- **Specialization:** `Doctor`
- **Level / Salary:** 1 / $880
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Voice:** `Jazz_AME_Female`
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

**Биография:** Грейс Ванджиру — лазаретная медсестра из Кении. Ствола нет и не будет: её сила — набор, бинты и умение не паниковать, когда крови слишком много. Тихая и незаменимая в тылу; экономить на таких обычно заканчивается плохо.

### `JAZZ_AME_51` — Dr. Emile Kabongo

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Specialists / Medic
- **Specialization:** `Doctor`
- **Level / Salary:** 1 / $1000
- **Potential (Wisdom):** High
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_51` ← donor `Heavy_Rebels` (male; blue recolor, source не править)
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

**Биография:** Доктор Эмиль Кабонго — травматолог из Гранд-Шьен. Учит младших перевязывать так, чтобы раненый дожил до настоящей помощи. Голос спокойный, руки точные. Выглядит старше своих лет — так бывает с теми, кто слишком часто видел, чем кончается «ещё одна небольшая царапина».

### `JAZZ_AME_52` — Captain Amara Koné

- **Nationality:** `Mali`
- **Category / CombatRole:** Specialists / Instructor
- **Specialization:** `Leader`
- **Level / Salary:** 1 / $1200
- **Potential (Wisdom):** High
- **Traits (common):** `Teacher`
- **Voice:** `Jazz_AME_Female`
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

**Биография:** Капитан Амара Коне — инструктор из Мали с учительским характером. Учит жёстко, без театра: оставляет объяснения, которые потом спасают жизни. Считает, что один хороший учитель дешевле десяти свежих могил.

### `JAZZ_AME_53` — Sgt. Nadia Okonkwo

- **Nationality:** `Nigeria`
- **Category / CombatRole:** Specialists / Instructor
- **Specialization:** `Leader`
- **Level / Salary:** 1 / $1150
- **Potential (Wisdom):** High
- **Traits (common):** `Teacher`
- **Voice:** `Jazz_AME_Female`
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

**Биография:** Сержант Надия Оконкво из Нигерии учит прицелу так, будто это одна профессия со стрельбой: научить попадать важнее, чем самой красиво попасть на глазах у начальства. В бой идёт редко, говорит часто — и обычно по делу. Её слушают даже те, кто не любит женщин с голосом громче их собственного.

### `JAZZ_AME_54` — Maj. Théodore Ngalula

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Specialists / Instructor
- **Specialization:** `Leader`
- **Level / Salary:** 1 / $1300
- **Potential (Wisdom):** High
- **Traits (common):** `Teacher`
- **Voice:** `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_54` ← donor `Heavy_Rebels_02` (male; blue recolor, source не править)
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

**Биография:** Майор Теодор Нгалула помнит, как строить людей так, чтобы они не разваливались в первую же неделю. Мудрость и отвёртка у него рядом с привычкой объяснять до тех пор, пока не поймут. В Гранд-Шьен его ещё помнят по званию — и по тому, что скидок на работу он не любит.

### `JAZZ_AME_55` — Issa Camara

- **Nationality:** `Senegal`
- **Category / CombatRole:** Specialists / Sniper
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $780
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_55` ← donor `Heavy_Rebels_03` (male; blue recolor, source не править)
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

**Биография:** Исса Камара стреляет редко и метко. Тело хрупкое: один выстрел, не спринт. Ровное дыхание и терпение — его религия; беготня — чужая. Штурмовиком себя не считает и другим не врёт.

### `JAZZ_AME_56` — Lindiwe Mokoena

- **Nationality:** `SouthAfrica`
- **Category / CombatRole:** Specialists / Sniper
- **Specialization:** `Marksmen`
- **Level / Salary:** 1 / $820
- **Potential (Wisdom):** Medium
- **Traits (common):** `NightOps`
- **Voice:** `Jazz_AME_Female`
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

**Биография:** Линдиве Мокоена работает ночью. Хрупкая, зоркая; темнота для неё союзник, а не чужой кошмар. Не обещает чудес и не набивает цену громкими словами. Любит, когда дело заканчивается одним тихим щелчком.

### `JAZZ_AME_57` — Bakary Diarra

- **Nationality:** `Mali`
- **Category / CombatRole:** Specialists / Sapper
- **Specialization:** `ExplosiveExpert`
- **Level / Salary:** 1 / $720
- **Potential (Wisdom):** Medium
- **Traits (common):** `Throwing`
- **Voice:** `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_57` ← donor `Marksman_Rebels` (male; blue recolor, source не править)
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

**Биография:** Бакари Диарра из Мали однажды пропил пистолет на детонаторы — и не жалеет. Взрывчатку знает лучше стрельбы, и сам об этом не стесняется. Его боятся ровно настолько, насколько уважают.

### `JAZZ_AME_58` — Marie-Claire Mbala

- **Nationality:** `Congo`
- **Category / CombatRole:** Specialists / Sapper
- **Specialization:** `ExplosiveExpert`
- **Level / Salary:** 1 / $760
- **Potential (Wisdom):** Medium
- **Traits (common):** `Throwing`
- **Voice:** `Jazz_AME_Female`
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

**Биография:** Мари-Клер Мбала ставит мины в Конго без лишней поэзии. Взрывчатка для неё важнее патронов, и она это повторяет всем новичкам. Бросок уверенный, характер сухой — сначала любопытство, потом осторожность.

### `JAZZ_AME_59` — Ousmane Fall

- **Nationality:** `Senegal`
- **Category / CombatRole:** Specialists / Mechanic
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $680
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_59` ← donor `Marksman_Rebels_02` (male; blue recolor, source не править)
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

**Биография:** Усман Фалл из Сенегала чинит стволы лучше, чем держит их в бою. Желания геройствовать нет. В бой его не зовут, если есть хоть кто-то другой; после боя зовут первыми. Без него отряд разваливается быстрее, чем без лишнего героя.

### `JAZZ_AME_60` — Jean-Pierre Kalala

- **Nationality:** `GrandChien`
- **Category / CombatRole:** Specialists / Mechanic
- **Specialization:** `AllRounder`
- **Level / Salary:** 1 / $720
- **Potential (Wisdom):** Medium
- **Traits (common):** —
- **Voice:** `Jazz_AME_Male_Hard`
- **Appearance:** `JAZZ_AME_60` ← donor `Marksman_Rebels_03` (male; blue recolor, source не править)
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

**Биография:** Жан-Пьер Калала — бывший гаражный мастер из Гранд-Шьен. Замок вскроет, очередь — вряд ли. Инструменты ему роднее любого автомата. Хорошие механики не любят рекламу — его обычно находят по рекомендации.

