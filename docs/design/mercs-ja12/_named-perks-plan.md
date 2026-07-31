# Именные перки мерков JA12 — каталог и план уточнения

> Spec реализации Wave A: [`docs/specs/active/JAZZ-UNITS-003.md`](../../specs/active/JAZZ-UNITS-003.md). Источники каталога: `docs/design/mercs-ja12/*.md`, `CharacterEffect/Jazz_Perk_*.lua`, `Code/System_OR_*.lua`, showcase `docs/showcase/ru/perks.md`.
>
> Цель документа: выписать уже написанные перки (старые эталоны + волна), зафиксировать runtime-реальность, уточнить механики и предложить реализуемый план волн. **Wave A (EASY) — в коде по JAZZ-UNITS-003.**

## 1. Снимок состояния

| Слой | Факт |
| --- | --- |
| Статей мерков | 48 (lynx/tosca/spider/spouke + 44 волны JAZZ-UNITS-002) |
| Companion `Jazz_Perk_*` | есть почти у всех; иконки в `Perks/Personal/` |
| Полностью/частично в runtime | **5** именных: Фраг, Тоска, Рысь, Паук, Колби (+ AI `OfficerAura*`, vanilla/JAZZ Grizzly/Grunty) |
| Заглушки | **~43** — `unit_reactions = {}`, WIP-текст, нет gameplay-refs в `Code/` |
| Орфан | `Jazz_Perk_44840` («Тюремная выдержка») — дубль Eskimo, **не** в metadata/items |
| Известный UX-баг | HUD-кнопки Lynx/Buzz/Spider/Colby ошибочно копируют toggle `Jazz_Perk_00` (пассив при этом может работать) |
| UnitData волны | пакет `jazz-units` (в этом checkout только `UnitData/Ivan.lua`) — StartingPerks канон = статьи |

Спека волны уже помечает AC-004 как `PARTIAL`: Colby wired, остальные stubs. Это документ уточнения **следующей** волны перков, не переписывание JAZZ-UNITS-002 без отдельного approve.

## 2. Сводка каталога

Feasibility — инженерная оценка «как делать», не баланс-оценка силы:

| Тег | Смысл | Типичный путь |
| --- | --- | --- |
| **SHIPPED** | Уже в runtime (полностью или с известным gap) | добить gap / выровнять текст |
| **EASY** | Достаточно `unit_reactions` на известных Event + существующие статусы | companion CharacterEffect |
| **MEDIUM** | Нужен точечный hook в уже существующем `Code/System_*` / combat action | companion + 1–2 Code-точки |
| **HARD** | Новая sector operation, economy, satellite travel, militia pipeline, multi-trainer rules | отдельный mini-spec / отложить или упростить |

| Slug | Nick | UnitData | Pri | Role | Affil. | Named perk | Type | Feas. | Runtime |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `blade` | Бритва | `Jazz_Blade` | high | Scout | MERC | `Jazz_Perk_Blade` · Ураган клинков | passive | MEDIUM | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `colby` | Колби | `Jazz_Colby` | high | Demolitions | AIM | `Jazz_Perk_Colby` · Цепная паника | passive | SHIPPED | WIRED — panic `OnCalcDamageAndEffects` + grenade +20% AoE; traps AoE gap |
| `conrad` | Конрад | `Jazz_Conrad` | high | Commander | MERC | `Jazz_Perk_Conrad` · Строгий инструктор | passive | HARD | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `dimitri` | Димитрий | `Jazz_Dimitri` | high | Thrower | Locals | `Jazz_Perk_Dimitri` · Точильщик | passive | MEDIUM | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `grom` | Гром | `Jazz_Grom` | high | HeavyWeapons | Locals | `Jazz_Perk_Grom` · Артподготовка | passive | MEDIUM | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `ira` | Айра | `Jazz_Ira` | high | Commander | Locals | `Jazz_Perk_Ira` · Народный командир | passive | HARD | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `lynx` | Рысь | `Jazz_Lynx` | high | Sniper | AIM | `Jazz_Perk_Lynx` · Рысий взгляд | passive | SHIPPED | PARTIAL — Code sight +8; CTH-range text not wired; `unit_reactions={}` |
| `madman` | Бешеный | `Jazz_Madman` | high | Mechanic | MERC | `Jazz_Perk_Madman` · Штурм в упор | passive | MEDIUM | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `mike` | Майк | `Jazz_Mike` | high | AllRounder | AIM | `Jazz_Perk_Mike` · Быстрая реакция | passive | MEDIUM | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `spider` | Паук | `Jazz_Spider` | high | Doctor | AIM | `Jazz_Perk_Spider` · Полевая хирургия | passive | SHIPPED | WIRED — `System_SectorOperations` Medical×2; empty reactions |
| `spouke` | Фраг | `JAZZ_Merc_Spouke` | high | Demolitions | AIM | `Jazz_Perk_00` · 00:00 | passive (timer interaction) | SHIPPED | WIRED — toggle effect value + traps timer + `OnCombatEnd` clear |
| `tosca` | Тоска | `Jazz_Buzz` | high | Autorifleman | AIM | `Jazz_Perk_Buzz` · Свинцовый дождь | passive | SHIPPED | WIRED — `items.lua` autofire +50%; empty reactions |
| `allik` | Знаток | `Jazz_Allik` | medium | AllRounder | AIM | `Jazz_Perk_Allik` · Знаток дела | passive | MEDIUM | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `biff` | Бифф | `Jazz_Biff` | medium | Commander | MERC | `Jazz_Perk_Biff` · Вербовка MERC | operation | HARD | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `cougar` | Пума | `Jazz_Cougar` | medium | Autorifleman | MERC | `Jazz_Perk_Cougar` · Мягкая лапа | passive | MEDIUM | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `dynamo` | Динамо | `Jazz_Dynamo` | medium | Mechanic | MERC | `Jazz_Perk_Dynamo` · Вилкой в глаз | passive | MEDIUM | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `flo` | Фло | `Jazz_Flo` | medium | Support | MERC | `Jazz_Perk_Flo` · Барахольщица | passive | HARD | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `gamos` | Гамос | `Jazz_Gamos` | medium | Scout | Locals | `Jazz_Perk_Gamos` · Тропы джунглей | passive | HARD | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `gaston` | Гастон | `Jazz_Gaston` | medium | Sniper | MERC | `Jazz_Perk_Gaston` · Крыша | passive | MEDIUM | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `henning` | Хеннинг | `Jazz_Henning` | medium | Commander | AIM | `Jazz_Perk_Henning` · Кабинетный генерал | passive | EASY | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `horg` | Сигара | `Jazz_Horg` | medium | HeavyWeapons | MERC | `Jazz_Perk_Horg` · Тяжёлая рука | passive | MEDIUM | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `manuel` | Мануэль | `Jazz_Manuel` | medium | Scout | Locals | `Jazz_Perk_Manuel` · Под прикрытием | passive | MEDIUM | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `miguel` | Мигель | `Jazz_Miguel` | medium | Commander | Locals | `Jazz_Perk_Miguel` · Команданте | passive | HARD | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `monk` | Монк | `Jazz_Monk` | medium | Scout | AIM | `Jazz_Perk_Monk` · Маскировка | passive | MEDIUM | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `nervous` | Нервный | `Jazz_Nervous` | medium | Autorifleman | MERC | `Jazz_Perk_Nervous` · Суперочередь | passive | EASY | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `quinten` | Дэнни | `Jazz_Quinten` | medium | Doctor | AIM | `Jazz_Perk_Quinten` · Полевой реаниматор | passive | MEDIUM | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `rothman` | Ротман | `Jazz_Rothman` | medium | Commander | AIM | `Jazz_Perk_Rothman` · Шахтёрский надзор | operation | HARD | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `vicious` | Злобный | `Jazz_Vicious` | medium | AllRounder | AIM | `Jazz_Perk_Vicious` · Дамский угодник | passive | MEDIUM | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `biggens` | Биггенс | `Jazz_Biggens` | low | Demolitions | Locals | `Jazz_Perk_Biggens` · Старая школа | passive | HARD | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `bull` | Бык | `Jazz_Bull` | low | Melee | AIM | `Jazz_Perk_Bull` · Грудная клетка | passive | MEDIUM | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `carlos` | Карлос | `Jazz_Carlos` | low | Scout | Locals | `Jazz_Perk_Carlos` · Тихая тень | passive | MEDIUM | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `cord` | Кардан | `Jazz_Cord` | low | Mechanic | MERC | `Jazz_Perk_Cord` · Тихий ремонт | passive | HARD | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `devin` | Девин | `Jazz_Devin` | low | Demolitions | Locals | `Jazz_Perk_Devin` · IRA | passive | MEDIUM | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `eskimo` | Эскимо | `Jazz_Eskimo` | low | Sniper | Locals | `Jazz_Perk_Eskimo` · Тюремная выдержка | passive | EASY | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `grace` | Грейс | `Jazz_Grace` | low | Thrower | AIM | `Jazz_Perk_Grace` · Точный бросок | passive | MEDIUM | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `highball` | Скала | `Jazz_Highball` | low | Doctor | AIM | `Jazz_Perk_Highball` · Полевой химик | passive | HARD | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `hitman` | Убийца | `Jazz_Hitman` | low | Sniper | Locals | `Jazz_Perk_Hitman` · Вырубить | active | MEDIUM | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `hobbit` | Хоббит | `Jazz_Hobbit` | low | Demolitions | MERC | `Jazz_Perk_Hobbit` · Несу вас | passive | HARD | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `kulba` | Кульба | `Jazz_Kulba` | low | Autorifleman | Locals | `Jazz_Perk_Kulba` · Оружейник старой закалки | passive | MEDIUM | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `laura` | Лора | `Jazz_Laura` | low | Doctor | AIM | `Jazz_Perk_Laura` · Скрытный врач | passive | EASY | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `lucky` | Лаки | `Jazz_Lucky` | low | Autorifleman | AIM | `Jazz_Perk_Lucky` · Второе дыхание | passive | MEDIUM | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `meat` | Мясо | `Jazz_Meat` | low | Demolitions | MERC | `Jazz_Perk_Meat` · Толстокожий | passive | MEDIUM | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `ricochet` | Рикошет | `Jazz_Ricochet` | low | Melee | MERC | `Jazz_Perk_Ricochet` · Рикошет | passive | MEDIUM | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `shank` | Шенк | `Jazz_Shank` | low | Thrower | MERC | `Jazz_Perk_Shank` · Не трогай меня | passive | EASY | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `static` | Статик | `Jazz_Static` | low | Mechanic | AIM | `Jazz_Perk_Static` · Экономия запчастей | passive | HARD | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `steiger` | Штайгер | `Jazz_Steiger` | low | Commander | AIM | `Jazz_Perk_Steiger` · Ночной инструктор | passive | EASY | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `vilde` | Зануда | `Jazz_Vilde` | low | Autorifleman | AIM | `Jazz_Perk_Vilde` · Ночной автоматчик | passive | EASY | STUB — `unit_reactions={}`, WIP description in CharacterEffect |
| `vince` | Винс | `Jazz_Vince` | low | Doctor | Locals | `Jazz_Perk_Vince` · Полевой наставник | passive | EASY | STUB — `unit_reactions={}`, WIP description in CharacterEffect |

## 3. Паттерны реализации (как делать)

Уже проверенные в JAZZ схемы:

| Паттерн | Эталон | Когда использовать |
| --- | --- | --- |
| A. `unit_reactions` Event | Colby `OnCalcDamageAndEffects` → `Panicked` | proc на хит/урон/ход/CTH |
| B. `HasPerk` в `Code/` | Lynx sight, Spider heal, Colby AoE, Spouke timer | когда Event не отдаёт нужный контекст |
| C. CombatAction / items hook | Buzz `GetAutofireShots` в `items.lua` | изменение числа пуль / action params |
| D. Toggle + effect value | Spouke `Jazz_Perk_00` | активный личный toggle |
| E. Status/aura marker | `Jazz_Perk_OfficerAura*` | ауры; не AIM StartingPerk |

Доступные `UnitReaction` Event (уже встречаются в `CharacterEffect/`):  
`OnCalcChanceToHit`, `OnModifyCTHModifier`, `GatherCTHModifications`, `OnCalcDamageAndEffects`, `OnCalcCritChance`, `OnCalcAPCost`, `OnCalcStartTurnAP`, `OnCalcFreeMove`, `OnCalcStealthKillChance`, `OnCalcStealthKillMinChance`, `OnCalcSightModifier`, `OnBeginTurn`, `OnEndTurn`, `OnCombatStarted`/`Starting`/`End`, `OnUnitAttack`, `OnFirearmAttackStart`, `OnHeal`, `OnUnitBandaged`, `OnCalcPersonalMorale`, `OnSatelliteTick`, …

Правила волны перков:

1. Один именной id на мерка (`Jazz_Perk_<Id>`), Tier=`Personal`, иконка уже есть.
2. Пассив по умолчанию — **без** HUD-кнопки; кнопку не копировать с `Jazz_Perk_00`.
3. Сначала упростить Mechanics до одного чёткого эффекта; второй эффект — только если EASY.
4. Не плодить новые status id, пока хватает vanilla/`Inspired`/`Panicked`/`Blinded`/`Suppressed`/`Unconscious`/`Burning`.
5. HARD не тащить «заодно» с EASY-волной — либо упростить, либо отдельный spec.
6. Loc RU+EN и sync generated data в том же change set, что и hook.
7. До кода — approve уточнённых Mechanics (этот документ → правка статей → spec follow-up).

## 4. Уточнения по shipped (старые + Colby)

| Id | Мерк | Сейчас | Уточнение / добить |
| --- | --- | --- | --- |
| `Jazz_Perk_00` | Фраг | Toggle таймерных взрывов на ход врага | Оставить. Не использовать как шаблон кнопки для чужих перков. |
| `Jazz_Perk_Buzz` | Тоска | +50% пуль autofire в `items.lua` | Оставить. Опционально перенести проверку ближе к `FirearmBase:GetAutofireShots`, чтобы не плодить копии в items. |
| `Jazz_Perk_Lynx` | Рысь | +8 sight; текст обещает ещё снижение дальнего CTH-штрафа | **Решение нужно:** (а) дописать CTH-часть через `OnModifyCTHModifier`/`GatherCTHModifications`, или (б) сузить Description до факта «+обзор». Рекомендация: (а) малый flat/range-mod, чтобы текст не врал. |
| `Jazz_Perk_Spider` | Паук | Medical×2 в sector heal | Оставить as-shipped; не обещать combat heal buff без отдельного дизайна. |
| `Jazz_Perk_Colby` | Колби | +20% grenade AoE + 20% panic по раненым | Добить traps/weapons AoE (`System_OR_Traps` gap из queue). Panic-ветку не трогать. |

## 5. Предлагаемые уточнения механик (stubs)

Ниже — **рекомендуемый уточнённый контракт** для реализации. Где статья слишком широкая, режем до одного проверяемого эффекта. Числа из статей сохраняем, если не отмечено иначе.

### 5.1 Волна A — EASY (unit_reactions first)

| Мерк | Перк | Уточнённая механика | Как |
| --- | --- | --- | --- |
| Бритва | Ураган клинков | **v1:** Rampage/melee follow-up +20% CTH, crit chance forced 0. Charge +2 плитки — v2 если найдётся единая точка charge range. | `OnCalcChanceToHit` / `OnModifyCTHModifier` + `OnCalcCritChance`; charge — отдельный follow-up |
| Бешеный | Штурм в упор | Kill на range ≤1 → `Inspired` 2 хода | `OnCalcDamageAndEffects` / kill path + `AddStatusEffect("Inspired")` |
| Нервный | Суперочередь | Autofire: +2 пули **или** −20% AP (не оба в v1). Рекомендация v1: +2 пули по образцу Buzz | `HasPerk` рядом с Buzz / `GetAutofireShots` |
| Хеннинг | Кабинетный генерал | Союзники ≤5 плиток: +5 CTH на их следующую атаку в этот ход (статус-маркер 1 ход) | `OnBeginTurn` раздать temp status; статус даёт CTH через `OnCalcChanceToHit` |
| Злобный | Дамский угодник | v1: в старте боя +1 AP за каждую женщину в отряде (cap 3). Удвоение Fox/Spider/Ira и melee-kill +2 AP — v2 | `OnCombatStarted` / `OnCalcStartTurnAP` |
| Динамо | Вилкой в глаз | v1: headshot → 25% `Blinded` 1 ход. Groin/self-berserk — v2 | `OnCalcDamageAndEffects` body part |
| Эскимо | Тюремная выдержка | CTH rifles не режется `Wounded`; иммунитет `Panicked` при HP&lt;50% | `GatherCTHModifications` / `OnCalcChanceToHit` + блок/снятие Panic |
| Лаки | Второе дыхание | 1×/бой: первый miss → hit (min success). | attack resolve hook / `OnCalcChanceToHit` force |
| Лора | Скрытный врач | Heal/revive не снимает Hidden с Лоры | `OnHeal` / bandage path + stealth preserve |
| Винс | Полевой наставник | 1×/бой: первый heal/revive цели → +4 AP | `OnHeal`/`OnUnitBandaged` + AP grant |
| Шенк | Не трогай меня | Враги в melee по Шенку: −50% CTH | target-side `OnCalcChanceToHit` |
| Вильде | Ночной автоматчик | Ночью Full-Auto/Burst +15% CTH | `OnCalcChanceToHit` + Night check |

*В сводной таблице Blade/Madman могут стоять как MEDIUM из‑за составных Mechanics статьи; для Wave A берём только v1 из этой колонки.*

### 5.2 Волна B — MEDIUM (точечный Code)

| Мерк | Перк | Уточнённая механика | Куда hook |
| --- | --- | --- | --- |
| Гром | Артподготовка | 1×/ход: первый успешный HeavyWeapons/throw explosive hit → `Suppressed` всем врагам в AoE оружия | damage/AoE apply path (рядом с Colby/suppression) |
| Майк | Быстрая реакция | Упростить: при старте боя, если Майк — первый в initiative среди отряда, +1 действие / +AP на первый ход (вместо «detection вне боя») | `OnCombatStarted` / `OnCalcStartTurnAP` — **упрощение статьи обязательно** |
| Димитрий | Точильщик | Упростить: throws с ножом +20 к броску **без** отдельного restock-пула (пул — v2 loot) | throw CTH/skill check |
| Пума | Мягкая лапа | v1: +12 pp stealth-kill chance (`OnCalcStealthKillChance`). Noise×0.5 и AP refund — v2 | Stealthy-подобные reactions + noise code |
| Гастон | Крыша | +15 CTH с elevated tile; night visibility ignore — v2 | elevation check в CTH |
| Сигара | Тяжёлая рука | v1: игнор Strength requirement penalty на HeavyWeapons. Recoil −30% — v2 | AP/CTH heavy path |
| Кульба | Оружейник | v1: первая пуля burst +10% CTH. Jam −50% — v2 | CTH first bullet + jam roll |
| Карлос | Тихая тень | Stealth-kill thrown knife: не ломает Hidden отряда | stealth-break path |
| Грейс | Точный бросок | Первый knife throw за ход ≤4 плиток — auto-hit (graze/armor как обычно) | throw attack resolve |
| Рикошет | Рикошет | Kill thrown knife/axe → 40% bounce 50% dmg в случайного врага ≤3 | post-kill projectile |
| Бык | Грудная клетка | Melee torso: 15% Off-Balance **или** (если нет статуса) −1 reaction; KO 5% — только если `Unconscious` уже ок в балансе | `OnCalcDamageAndEffects` |
| Девин | IRA | v1: 25% `Burning` в blast. Structure +100% — v2 (нужен structure damage path) | explosion effects |
| Мясо | Толстокожий | Floor Will = 50 vs morale/panic modifiers | `OnCalcPersonalMorale` / Will clamp |
| Квинт | Полевой реаниматор | Heal снимающий дебафф / revive → цели +2 AP. FreeMove cap +20% — отдельный MEDIUM, можно выкинуть из v1 | `OnHeal` |
| Хо́бит→см. HARD | — | — | — |
| Биггенс | Старая школа | Mines/charges: −25% detection **или** −25% arm time (один эффект v1) | traps place/detect |
| Корд | Тихий ремонт | Repair −15% time **или** −10% Parts (один эффект v1) | `System_SectorOperations` repair |
| Аллик | Знаток дела | +15% XP с успешных non-combat Mechanical/Explosives/Medical checks | XP grant path |
| Монк | Маскировка | v1: первый выстрел боя из cover +20% CTH. Detection half-range — v2 | `OnCalcChanceToHit` + combat flag |
| Хитман | Вырубить | Active 1×/миссию: следующий hit винтовки → `Unconscious` вместо урона; recharge после lethal kill | CombatAction + effect value (как Spouke toggle pattern, но отдельный action) |

### 5.3 Волна C — HARD (упростить или отдельный spec)

Эти перки **тематически подходят** меркам, но текущая формулировка тянет strategy/economy. Предложение: не блочить волну A/B; для каждого выбрать путь **Simplify** или **Defer**.

| Мерк | Статья | Рекомендация |
| --- | --- | --- |
| Бифф | MERC recruitment operation | **Simplify:** пока Бифф в секторе с militia training — +1 уровень/скорость militia **или** бесплатный veteran militia раз в N дней. Полный MERC-trooper unit — Defer. |
| Ротман | Mine overseer operation | **Simplify:** garrison в mine sector → +15% income (пассив, без новой operation). Полная 2-day op — Defer. |
| Айра | Militia training ×2 | **Simplify:** `Teacher` + flat militia training speed в секторе присутствия (hook в `MilitiaTraining`), без отдельного «Locals only» ветвления если дорого. |
| Конрад | Exempt от Teacher stacking penalty | **Defer** или найти vanilla stacking и точечно патчить — высокий risk/low visibility. **Simplify alt:** Conrad даёт +X% training speed personally. |
| Мигель | Militia HP/Marksmanship aura + combat AP | **Simplify v1:** в бою с militia — militia +1 AP на старте. Garrison aura — Defer. |
| Фло | Shop ±12% | **Simplify:** усилить/заменить на больший `Negotiator`-like sector ops discount; shop buy/sell требует price pipeline audit. |
| Гамос | Jungle travel −40% | **Defer** (satellite travel tags) **или Simplify:** в jungle sectors +free move / stealth в бою. |
| Мануэль | Stealth near unspotted enemies | Близко к MEDIUM: `OnCalcSightModifier` / detection — можно спустить в B после прототипа. |
| Штайгер | Night ally +5% CTH aura | По сути EASY/MEDIUM aura как Хеннинг, но night-gated — перенести в A. |
| Статик | Parts −5%/level | MEDIUM в repair/craft cost; не HARD если есть одна точка Parts cost. |
| Хайболл | Craft CombatStim/day без bag | **Defer** (craft UI) **или Simplify:** 1×/день free bandage potency / stim status без крафта. |
| Хоббит | Squad uses Hobbit Explosives skill | **Simplify:** рядом стоящий союзник получает Explosives floor = Hobbit при place mine — иначе Defer. |
| Гром | (если AoE suppress окажется толстым) | Держать в B; при блокере — Simplify до «первая тяжёлая атака хода накладывает Suppressed на основную цель». |

## 6. Что подходит «новым» меркам (роль-фит)

Критерий: именной перк усиливает **роль + StartingPerks**, не дублирует их 1:1 и читается в одном предложении.

| Роль-кластер | Мерки | Перк должен давать | Не должен |
| --- | --- | --- | --- |
| Explosives | Colby✓, Spouke✓, Grom, Devin, Biggens, Hobbit, Dimitri | blast control / panic / suppress / place | общий +damage всему |
| Auto/MG | Buzz✓, Nervous, Kulba, Vilde, Cougar, Lucky | bullets / first-bullet CTH / night auto | второй «Buzz +50%» без отличия |
| Sniper/Marksman | Lynx✓, Gaston, Hitman, Eskimo | sight/elevated/wound-ignore/utility KO | ещё один deadeye-клон |
| Melee/Throw | Blade, Madman, Bull, Shank, Grace, Ricochet, Carlos | reliability / AP on kill / throw tricks | бесконечные ножи без лута |
| Doctor | Spider✓, Quinten, Vince, Laura, Highball | heal AP / stealth heal / satellite heal | боевой DPS |
| Mechanic | Cord, Static, Dynamo, Allik | repair/parts/XP/skill shots | combat nuke |
| Commander/Lead | Ira, Conrad, Miguel, Henning, Steiger, Biff, Rothman | train/militia/aura CTH | личный sniper perk |
| Scout/Stealth | Monk, Manuel, Gamos, Cougar, Carlos | first shot / detection / noise | heavy weapons |
| Support/Trade | Flo, Vicious (flavor AP) | economy **или** squad AP fantasy | combat crit machine |

## 7. План поставки (без оценок в днях)

### Фаза 0 — гигиена (до новых эффектов)

1. Выкинуть/не регистрировать орфан `Jazz_Perk_44840` (оставить `Jazz_Perk_Eskimo`).
2. Убрать ошибочные HUD-кнопки у пассивов (не копировать `Jazz_Perk_00`).
3. Зафиксировать в статьях уточнения §5 (этот документ → PR в статьи после approve владельца).
4. Follow-up spec (например `JAZZ-UNITS-003` named-perks wave) — только после выбора Simplify/Defer по HARD.

### Фаза 1 — Wave A (EASY), приоритет High→читаемый combat fantasy

Порядок предложения:

1. Madman, Blade (v1), Nervous  
2. Henning, Vicious (v1), Dynamo (v1)  
3. Eskimo, Lucky, Shank, Vilde  
4. Laura, Vince  
5. Steiger (aura night — из HARD↓EASY)

DoD на перк: Description = фактический эффект; `unit_reactions` или `HasPerk` hook; RU/EN; smoke в редакторе/бое.

### Фаза 2 — Wave B (MEDIUM) High leftovers + сильные Medium

1. Grom, Mike (**с упрощением**), Dimitri (без пула)  
2. Cougar (stealth-kill only), Gaston (elevated), Horg (str ignore)  
3. Grace, Ricochet, Carlos, Bull  
4. Kulba, Devin (Burning), Meat, Quinten (AP only), Monk  
5. Hitman (active), Allik, Cord/Static/Biggens — по одной cost/detect точке

### Фаза 3 — Wave C (HARD) после отдельного approve

Biff / Rothman / Ira / Miguel / Flo / Gamos / Conrad / Hobbit / Highball — только в Simplify-форме из §5.3 или полным operation-spec.

### Фаза 4 — shipped polish

Lynx CTH text vs code; Colby traps AoE; опциональный рефактор Buzz hook.

## 8. Карта StartingPerks (vanilla слой)

Именной перк **дополняет**, не заменяет лист. Повторяющиеся якоря волны:

| Vanilla perk | Часто у | Зачем рядом с именным |
| --- | --- | --- |
| `Teacher` | Ira, Conrad, Miguel, Rothman, Steiger, Vince | train/militia fantasy |
| `DesignerExplosives` / `BreachAndClear` / `Throwing` | Colby, Spouke, Grom, Hobbit, Devin… | blast identity |
| `AutoWeapons` | Buzz, Nervous, Kulba, Vilde, Cougar… | bullet perks |
| `Stealthy` / `NightOps` | Spider, Cougar, Monk, Manuel, Eskimo… | stealth/night named |
| `MeleeTraining` / `CQCTraining` | Blade, Madman, Bull, Vicious… | melee named |
| `MrFixit` / `JackOfAllTrades` | Cord, Static, Allik, Dynamo, Colby… | repair/XP named |
| `Negotiator` / `Scoundrel` | Flo, Biff, Cord… | economy |
| `Psycho` / `Hotblood` | Blade, Buzz, Dynamo, Nervous, Lucky… | aggression flavor |
| `Savior` | Quinten, Highball | doctor |
| `Loner` | Mike, Quinten, Monk, Manuel, Ricochet | solo fantasy |

Полные листы StartingPerks — в §9.

## 9. Полные карточки (статья = канон дизайна)

### Бритва (`blade` / `Jazz_Blade`)

- **Priority / role / affiliation:** high · Scout · MERC
- **StartingPerks:** `Jazz_Perk_Blade`, `Psycho`, `MeleeTraining`, `CQCTraining`, `Berserker`, `Hotblood`
- **Named:** `Jazz_Perk_Blade` — Ураган клинков / Blade Storm
- **Type / feasibility / runtime:** passive · **MEDIUM** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Заряд клинком достаёт дальше; атаки бойни получают +20% к шансу попадания, но не могут критовать / Knife Charge reaches farther; Rampage attacks gain +20% chance to hit but cannot score critical hits
- **Mechanics (article):** (1) Charge attack range with any bladed melee weapon extended by 2 tiles; (2) Rampage (free follow-up melee attacks) gets +20% CTH and 0% crit chance — trades burst crit damage for reliability. Ties into Psycho/Berserker/Hotblood quirks already on the sheet.

### Колби (`colby` / `Jazz_Colby`)

- **Priority / role / affiliation:** high · Demolitions · AIM
- **StartingPerks:** `Jazz_Perk_Colby`, `MrFixit`, `Throwing`, `BreachAndClear`, `HitTheDeck`, `DesignerExplosives`
- **Named:** `Jazz_Perk_Colby` — Цепная паника / Chain Panic
- **Type / feasibility / runtime:** passive · **SHIPPED** · WIRED — panic `OnCalcDamageAndEffects` + grenade +20% AoE; traps AoE gap
- **Description:** Взрывы Колби сеют панику: +20% к радиусу и 20% шанс паники у раненых врагов в зоне / Colby's blasts sow panic: +20% blast radius and 20% chance to panic wounded enemies in the blast
- **Mechanics (article):** Каждый взрыв, инициированный Колби (граната/миномёт/C4/бочка/мина/чужая бомба выстрелом): 20% шанс паники у раненых врагов в радиусе; +20% к радиусу взрывов.

### Конрад (`conrad` / `Jazz_Conrad`)

- **Priority / role / affiliation:** high · Commander · MERC
- **StartingPerks:** `Jazz_Perk_Conrad`, `Teacher`, `TakeAim`, `SteadyBreathing`, `ShoulderToShoulder`
- **Named:** `Jazz_Perk_Conrad` — Строгий инструктор / The Strict Instructor
- **Type / feasibility / runtime:** passive · **HARD** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Конрад всегда тренирует на полной скорости и не теряет темп рядом с другими инструкторами / Conrad always trains at full speed and never loses pace next to other trainers
- **Mechanics (article):** Resolves the vanilla multi-`Teacher` stacking penalty for Conrad specifically: when two or more `Teacher`-perk mercs share a squad/sector, Conrad's own training contribution is exempt from the diminishing-return halving that would otherwise apply to the second-and-later trainer. Other trainers in the same squad are unaffected and still halve normally.

### Димитрий (`dimitri` / `Jazz_Dimitri`)

- **Priority / role / affiliation:** high · Thrower · Locals
- **StartingPerks:** `Jazz_Perk_Dimitri`, `Throwing`, `MrFixit`, `CQCTraining`
- **Named:** `Jazz_Perk_Dimitri` — Точильщик / The Whetstone
- **Type / feasibility / runtime:** passive · **MEDIUM** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Носит с собой запас доведённых до остроты бритвы метательных ножей: +20 к проверке ведущего навыка броска / Carries a finite stock of razor-honed throwing knives: +20 to the governing throw skill check
- **Mechanics (article):** Finite consumable knives (not an infinite-ammo effect like `Blood`'s knife perk); each combat start restocks a fixed pool of `Knife_Balanced`/`Knife_Sharpened` in a dedicated slot, and throws with those knives get +20 to the throw check.

### Гром (`grom` / `Jazz_Grom`)

- **Priority / role / affiliation:** high · HeavyWeapons · Locals
- **StartingPerks:** `Jazz_Perk_Grom`, `HeavyWeaponsTraining`, `Throwing`, `Hardened`
- **Named:** `Jazz_Perk_Grom` — Артподготовка / Softening Barrage
- **Type / feasibility / runtime:** passive · **MEDIUM** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Первое попадание из тяжёлого оружия или бросок в ходе применяет статус «Подавление» ко всем врагам в радиусе поражения / The first heavy-weapon hit or throw each turn applies Suppressed to every enemy caught in the blast radius
- **Mechanics (article):** Once per Grom's turn, the first successful hit from a `HeavyWeapons`-category weapon (RPG-7, launchers) or thrown explosive applies the `Suppressed` status to all enemies inside the weapon's `AreaOfEffect`, on top of normal damage/effects — reinforces `HeavyWeaponsTraining` + `Throwing` already on the sheet.

### Айра (`ira` / `Jazz_Ira`)

- **Priority / role / affiliation:** high · Commander · Locals
- **StartingPerks:** `Jazz_Perk_Ira`, `Teacher`, `ShoulderToShoulder`, `MinFreeMove`
- **Named:** `Jazz_Perk_Ira` — Народный командир / People's Commander
- **Type / feasibility / runtime:** passive · **HARD** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Пока Айра стоит гарнизоном в секторе, обучение местного ополчения там идёт вдвое быстрее / While Ira is garrisoned in a sector, militia training there completes in half the normal time
- **Mechanics (article):** Stacks additively with the base `Teacher` perk: militia training speed +50% in Ira's home sector (implementation detail — final numeric tuning happens at code time, but the design intent and floor value are fixed here so there is no open balance question). Applies only to Locals-affiliated squads, not to AIM/MERC training.

### Рысь (`lynx` / `Jazz_Lynx`)

- **Priority / role / affiliation:** high · Sniper · AIM
- **StartingPerks:** `AutoWeapons`, `NightOps`, `MrFixit`, `Jazz_Perk_Lynx`, `Pessimist`, `Deadeye`, `Killzone`, `Counterfire`
- **Named:** `Jazz_Perk_Lynx` — Рысий взгляд / Lynx's Eye
- **Type / feasibility / runtime:** passive · **SHIPPED** · PARTIAL — Code sight +8; CTH-range text not wired; `unit_reactions={}`
- **Description:** Дальность видимости днем повышена, а штрафы за дальность - понижены
- **Mechanics (article):** As-shipped CharacterEffect; day visibility bonus (see `docs/technical/systems/visibility-weather-appearance.md`)

### Бешеный (`madman` / `Jazz_Madman`)

- **Priority / role / affiliation:** high · Mechanic · MERC
- **StartingPerks:** `Jazz_Perk_Madman`, `Psycho`, `MrFixit`, `MeleeTraining`, `CQCTraining`, `Ironclad`
- **Named:** `Jazz_Perk_Madman` — Штурм в упор / Point-Blank Fury
- **Type / feasibility / runtime:** passive · **MEDIUM** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Убийство в упор (оружием ближнего боя или выстрелом почти в упор) даёт Воодушевление / A point-blank kill (melee or near point-blank shot) grants Inspired
- **Mechanics (article):** On a kill at range ≤1 tile (melee weapon or point-blank firearm shot), Madman gains the `Inspired` status effect for 2 turns (extra AP-equivalent morale buff, matching the existing Inspiration system used elsewhere in JAZZ). Synergizes with `MeleeTraining`/`CQCTraining` on the sheet.

### Майк (`mike` / `Jazz_Mike`)

- **Priority / role / affiliation:** high · AllRounder · AIM
- **StartingPerks:** `Jazz_Perk_Mike`, `Loner`, `NightOps`, `AutoWeapons`, `TakeAim`, `Counterfire`
- **Named:** `Jazz_Perk_Mike` — Быстрая реакция / Quick Reaction
- **Type / feasibility / runtime:** passive · **MEDIUM** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Первым замечает угрозу и получает свободное действие при обнаружении врага вне боя / First to spot a threat: gains a free action the instant an enemy is detected outside of combat
- **Mechanics (article):** When Mike (not the squad) is the unit that triggers enemy detection outside active combat, he immediately receives 4000 AP worth of free action (equivalent to one extra move/attack tick) before initiative order is rolled — mechanically distinct from `Counterfire`/`NightOps` already on the sheet, which cover the reactive/vision side.

### Паук (`spider` / `Jazz_Spider`)

- **Priority / role / affiliation:** high · Doctor · AIM
- **StartingPerks:** `Jazz_Perk_Spider`, `NightOps`, `Stealthy`
- **Named:** `Jazz_Perk_Spider` — Полевая хирургия / Field Surgery
- **Type / feasibility / runtime:** passive · **SHIPPED** · WIRED — `System_SectorOperations` Medical×2; empty reactions
- **Description:** Удваивает значение навыка медицины при лечении на глобальной карте
- **Mechanics (article):** Satellite medical skill ×2 (`System_SectorOperations.lua`)

### Фраг (`spouke` / `JAZZ_Merc_Spouke`)

- **Priority / role / affiliation:** high · Demolitions · AIM
- **StartingPerks:** `Jazz_Perk_00`, `BreachAndClear`, `Throwing`, `HitTheDeck`, `HeavyWeaponsTraining`, `BreachAndClear`
- **Named:** `Jazz_Perk_00` — 00:00
- **Type / feasibility / runtime:** passive (timer interaction) · **SHIPPED** · WIRED — toggle effect value + traps timer + `OnCombatEnd` clear
- **Description:** При активации взрывчатка с таймером, кинутая Споуком, взорвётся в начале вражеского хода.
- **Mechanics (article):** As-shipped; clears effect value OnCombatEnd

### Тоска (`tosca` / `Jazz_Buzz`)

- **Priority / role / affiliation:** high · Autorifleman · AIM
- **StartingPerks:** `Jazz_Perk_Buzz`, `HeavyWeaponsTraining`, `AutoWeapons`, `Psycho`, `StressManagement`, `ShockAndAwe`, `LastWarning`
- **Named:** `Jazz_Perk_Buzz` — Свинцовый дождь / Lead Rain
- **Type / feasibility / runtime:** passive · **SHIPPED** · WIRED — `items.lua` autofire +50%; empty reactions
- **Description:** Увеличивает длину очереди на 50%
- **Mechanics (article):** Burst/auto bullet count +50% (see combat-actions docs)

### Знаток (`allik` / `Jazz_Allik`)

- **Priority / role / affiliation:** medium · AllRounder · AIM
- **StartingPerks:** `Jazz_Perk_Allik`, `MrFixit`, `DesignerExplosives`, `TrueGrit`
- **Named:** `Jazz_Perk_Allik` — Знаток дела / Jack of All Trades
- **Type / feasibility / runtime:** passive · **MEDIUM** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Быстрее прокачивается благодаря разностороннему опыту / Levels up faster thanks to well-rounded experience
- **Mechanics (article):** Allik gains +15% experience from any non-combat skill check he succeeds (Mechanical, Explosives, Medical), on top of normal combat XP, reflecting his balanced stat spread and engineer's mindset.

### Бифф (`biff` / `Jazz_Biff`)

- **Priority / role / affiliation:** medium · Commander · MERC
- **StartingPerks:** `Jazz_Perk_Biff`, `Negotiator`, `ShoulderToShoulder`
- **Named:** `Jazz_Perk_Biff` — Вербовка MERC / MERC Recruitment Drive
- **Type / feasibility / runtime:** operation · **HARD** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Пока Бифф гарнизоном стоит в секторе с активным набором ополчения, он может провести спецоперацию, вербующую бойца MERC вместо обычного ополченца / While Biff is garrisoned in a sector actively training militia, he can run a special operation that produces a MERC trooper instead of a standard militia recruit
- **Mechanics (article):** Sector operation, usable once every 7 days while Biff is garrisoned in a sector with an active militia-training slot. Converts that training slot's output into 1 MERC trooper unit at the same resource/time cost as a normal militia recruit. Does not stack with itself in the same sector.

### Пума (`cougar` / `Jazz_Cougar`)

- **Priority / role / affiliation:** medium · Autorifleman · MERC
- **StartingPerks:** `Jazz_Perk_Cougar`, `Stealthy`, `AutoWeapons`, `Flanker`
- **Named:** `Jazz_Perk_Cougar` — Мягкая лапа / Soft Paw
- **Type / feasibility / runtime:** passive · **MEDIUM** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Шум от выстрелов Пумы вдвое тише; выше шанс скрытного убийства / Cougar's gunfire is half as loud; higher chance of a stealth-kill
- **Mechanics (article):** Noise generated by Cougar's own shots is halved (×0.5). Stealth-kill chance is increased by +12 percentage points, and a successful stealth kill refunds the AP spent on the opening attack.

### Динамо (`dynamo` / `Jazz_Dynamo`)

- **Priority / role / affiliation:** medium · Mechanic · MERC
- **StartingPerks:** `Jazz_Perk_Dynamo`, `MrFixit`, `Psycho`, `OptimalPerformance`
- **Named:** `Jazz_Perk_Dynamo` — Вилкой в глаз / Fork to the Eye
- **Type / feasibility / runtime:** passive · **MEDIUM** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Особые эффекты от ранений в конкретные зоны / Special effects from wounds to specific body parts
- **Mechanics (article):** When Dynamo lands a headshot, the target has a 25% chance to gain `Blinded` for 1 turn on top of normal headshot effects. When he lands a groin-area hit, the target has a 25% chance to gain a panic/flee status instead of the normal groin effect. If Dynamo himself is hit in the groin, he instead gains a berserk-style +20% damage buff for 2 turns rather than the normal debuff, reflecting his high pain tolerance.

### Фло (`flo` / `Jazz_Flo`)

- **Priority / role / affiliation:** medium · Support · MERC
- **StartingPerks:** `Jazz_Perk_Flo`, `Negotiator`, `Scoundrel`, `CancelShotPerk`
- **Named:** `Jazz_Perk_Flo` — Барахольщица / The Bargain Hunter
- **Type / feasibility / runtime:** passive · **HARD** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Скидки у торговцев на покупку и продажу / Shop discounts on both buying and selling
- **Mechanics (article):** −12% to buy prices and +12% to sell prices at all shops while Flo is in the active squad (stacks with the base `Negotiator` perk's own bonus, does not multiply with it).

### Гамос (`gamos` / `Jazz_Gamos`)

- **Priority / role / affiliation:** medium · Scout · Locals
- **StartingPerks:** `Jazz_Perk_Gamos`, `Stealthy`, `Flanker`, `TrueGrit`
- **Named:** `Jazz_Perk_Gamos` — Тропы джунглей / Jungle Trails
- **Type / feasibility / runtime:** passive · **HARD** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Быстрее передвигается вне дорог по джунглям и болотам / Moves faster off-road through jungle and marsh terrain
- **Mechanics (article):** −40% satellite-map travel time for squads led by Gamos when moving through sectors tagged `Jungle`, `Marshlands`, or `CursedForest` (matches the terrain GameStates already used by vanilla AppearancesList tagging). No effect on road/city travel.

### Гастон (`gaston` / `Jazz_Gaston`)

- **Priority / role / affiliation:** medium · Sniper · MERC
- **StartingPerks:** `Jazz_Perk_Gaston`, `TakeAim`, `Deadeye`, `NightOps`, `SteadyBreathing`
- **Named:** `Jazz_Perk_Gaston` — Крыша / The Rooftop
- **Type / feasibility / runtime:** passive · **MEDIUM** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Бонус к попаданию со стрельбы с крыш ночью / Accuracy bonus for rooftop shots at night
- **Mechanics (article):** +15 to CTH when Gaston fires from an elevated tile (roof or 2nd floor and above). At night, he additionally ignores the reduced-visibility accuracy penalty entirely while positioned on such an elevated tile.

### Хеннинг (`henning` / `Jazz_Henning`)

- **Priority / role / affiliation:** medium · Commander · AIM
- **StartingPerks:** `Jazz_Perk_Henning`, `AutoWeapons`, `HeavyWeaponsTraining`, `LeadFromTheFront`
- **Named:** `Jazz_Perk_Henning` — Кабинетный генерал / The Cabinet General
- **Type / feasibility / runtime:** passive · **EASY** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Приказы Хеннинга усиливают ближайших союзников / Henning's orders strengthen nearby allies
- **Mechanics (article):** At the start of each of Henning's turns, all allied units within 5 tiles gain +5 to CTH for their next attack this turn, reflecting his aristocratic command presence — stacks with `LeadFromTheFront` for a genuine battlefield-commander archetype.

### Сигара (`horg` / `Jazz_Horg`)

- **Priority / role / affiliation:** medium · HeavyWeapons · MERC
- **StartingPerks:** `Jazz_Perk_Horg`, `HeavyWeaponsTraining`, `Hardened`, `ShoulderToShoulder`
- **Named:** `Jazz_Perk_Horg` — Тяжёлая рука / Heavy Hand
- **Type / feasibility / runtime:** passive · **MEDIUM** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Меньше отдачи и штрафов точности от тяжёлого оружия / Reduced recoil and accuracy penalties from heavy weapons
- **Mechanics (article):** Horg's `HeavyWeapons`-category attacks (grenade launchers, RPGs, machineguns) get -30% to the normal recoil/CTH penalty they apply to his next shot, and he ignores the Strength requirement penalty for heavy weapons entirely (treated as if he always met the Strength threshold).

### Мануэль (`manuel` / `Jazz_Manuel`)

- **Priority / role / affiliation:** medium · Scout · Locals
- **StartingPerks:** `Jazz_Perk_Manuel`, `Stealthy`, `Loner`, `Flanker`
- **Named:** `Jazz_Perk_Manuel` — Под прикрытием / Undercover
- **Type / feasibility / runtime:** passive · **MEDIUM** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Опыт разведки под прикрытием даёт бонус к скрытности вблизи вражеских патрулей / Undercover experience grants a stealth bonus near enemy patrols
- **Mechanics (article):** +15% to Manuel's stealth detection-avoidance chance while within 2 tiles of an enemy unit that has not yet spotted him, reflecting his training at slipping past patrols undetected inside the Arulco army.

### Мигель (`miguel` / `Jazz_Miguel`)

- **Priority / role / affiliation:** medium · Commander · Locals
- **StartingPerks:** `Jazz_Perk_Miguel`, `Teacher`, `LeadFromTheFront`, `NightOps`, `MeleeTraining`
- **Named:** `Jazz_Perk_Miguel` — Команданте / El Comandante
- **Type / feasibility / runtime:** passive · **HARD** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Пока Мигель гарнизоном стоит в секторе с ополчением, оно получает бонус к прочности и меткости; при бою вместе с ополчением все ополченцы получают дополнительное очко действия в начале боя / While Miguel is garrisoned in a sector with militia, that militia gains bonus durability and accuracy; when he fights alongside militia, all militia in that fight gain an extra AP at combat start
- **Mechanics (article):** Aura effect: militia stationed in Miguel's home sector gain +10 max HP and +5 Marksmanship for as long as he remains garrisoned there (ends when he leaves). Separately, if Miguel is present in a combat encounter alongside militia, every militia unit on his side gets +1 free AP-equivalent action at the very start of that combat.

### Монк (`monk` / `Jazz_Monk`)

- **Priority / role / affiliation:** medium · Scout · AIM
- **StartingPerks:** `Jazz_Perk_Monk`, `Stealthy`, `Loner`, `NightOps`
- **Named:** `Jazz_Perk_Monk` — Маскировка / Camouflage
- **Type / feasibility / runtime:** passive · **MEDIUM** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Бонус к скрытности и точности при первом выстреле из укрытия / Stealth and first-shot accuracy bonus while camouflaged in cover
- **Mechanics (article):** While in any cover (Low or High) and unspotted, Monk gets +20% CTH on his first shot of a combat, and enemies must be within half their normal detection range to spot him — reinforces `Stealthy` for a genuine ambush specialist.

### Нервный (`nervous` / `Jazz_Nervous`)

- **Priority / role / affiliation:** medium · Autorifleman · MERC
- **StartingPerks:** `Jazz_Perk_Nervous`, `Psycho`, `AutoWeapons`, `Flanker`
- **Named:** `Jazz_Perk_Nervous` — Суперочередь / Super Burst
- **Type / feasibility / runtime:** passive · **EASY** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Автоматная очередь Нервного длиннее и дешевле по ОД / Nervous's autofire bursts are longer and cheaper in AP
- **Mechanics (article):** Auto attacks fire 2 extra bullets per burst compared to the base weapon's autofire count, and cost −20% AP. Accuracy penalty for the extra bullets follows the normal autofire falloff curve — no free accuracy.

### Дэнни (`quinten` / `Jazz_Quinten`)

- **Priority / role / affiliation:** medium · Doctor · AIM
- **StartingPerks:** `Jazz_Perk_Quinten`, `Loner`, `Ambidextrous`, `Savior`, `StressManagement`
- **Named:** `Jazz_Perk_Quinten` — Полевой реаниматор / Field Resuscitator
- **Type / feasibility / runtime:** passive · **MEDIUM** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Снятие негативного эффекта или подъём упавшего товарища даёт цели +2 ОД; акробатический freemove-бонус ограничен +20% вместо обычных +50% / Removing a negative status effect or reviving a downed ally grants the target +2 AP; parkour-style freemove bonus is capped at +20% instead of the usual +50%
- **Mechanics (article):** On successful use of a medical action that removes a negative status effect (Bleeding, Wounded, Unconscious, etc.) or wakes a Downed ally, the target immediately gains +2 AP that turn. To keep Quinten's mobility in line with a Doctor tier, his innate parkour/freemove bonus from Agility is explicitly capped at +20% rather than the higher values other high-Agility mercs can reach.

### Ротман (`rothman` / `Jazz_Rothman`)

- **Priority / role / affiliation:** medium · Commander · AIM
- **StartingPerks:** `Jazz_Perk_Rothman`, `Teacher`, `ShoulderToShoulder`, `DesignerExplosives`, `HoldPosition`
- **Named:** `Jazz_Perk_Rothman` — Шахтёрский надзор / The Mine Overseer
- **Type / feasibility / runtime:** operation · **HARD** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Пока Ротман гарнизоном стоит в секторе с шахтой, он может провести спецоперацию, ловящую ворующих штейгеров и временно поднимающую доход шахты / While Rothman is garrisoned in a sector with an active mine, he can run a special operation that catches embezzling foremen and temporarily boosts that mine's income
- **Mechanics (article):** New sector operation, available only in sectors with an active mine while Rothman is garrisoned there. Duration 2 days; on success grants +25% income from that mine for the following 7 days (does not stack with itself — a fresh run simply refreshes the duration). No resource cost beyond Rothman's time in the sector.

### Злобный (`vicious` / `Jazz_Vicious`)

- **Priority / role / affiliation:** medium · AllRounder · AIM
- **StartingPerks:** `Jazz_Perk_Vicious`, `MeleeTraining`, `CQCTraining`, `Hotblood`
- **Named:** `Jazz_Perk_Vicious` — Дамский угодник / Ladies' Man
- **Type / feasibility / runtime:** passive · **MEDIUM** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Растущий бонус ОД за каждую женщину в отряде; удваивается, если в отряде Лиска, Паук или Айра; убийство в ближнем бою даёт +2 ОД / Escalating AP bonus per woman in the squad; doubled if Fox, Spider, or Ira is present; a melee kill grants +2 AP
- **Mechanics (article):** At the start of combat, Vicious gains +1 AP for each female merc in the active squad (max 5 stacks / +5 AP). If Fox, `Jazz_Spider`, or `Jazz_Ira` is in the squad, this per-woman bonus is doubled for that combat. Any melee kill by Vicious grants an immediate +2 AP on top.

### Биггенс (`biggens` / `Jazz_Biggens`)

- **Priority / role / affiliation:** low · Demolitions · Locals
- **StartingPerks:** `Jazz_Perk_Biggens`, `Optimist`, `DesignerExplosives`, `NightOps`
- **Named:** `Jazz_Perk_Biggens` — Старая школа / Old School
- **Type / feasibility / runtime:** passive · **HARD** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Заряды Биггенса труднее обнаружить и они быстрее взводятся / Biggens's charges are harder to spot and arm faster
- **Mechanics (article):** Explosive charges and mines placed by Biggens are 25% harder for enemies to detect and take 25% less time to arm.

### Бык (`bull` / `Jazz_Bull`)

- **Priority / role / affiliation:** low · Melee · AIM
- **StartingPerks:** `Jazz_Perk_Bull`, `MeleeTraining`, `CQCTraining`, `TrueGrit`
- **Named:** `Jazz_Perk_Bull` — Грудная клетка / Iron Ribcage
- **Type / feasibility / runtime:** passive · **MEDIUM** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Ближний бой Быка может сбить дыхание или вырубить противника / Bull's melee attacks can knock the wind out of a target or knock them out cold
- **Mechanics (article):** Unarmed and knife melee attacks by Bull against Torso have a 15% chance to inflict Off-Balance (target loses its next reaction) and a separate 5% chance to apply Unconscious for 1 turn.

### Карлос (`carlos` / `Jazz_Carlos`)

- **Priority / role / affiliation:** low · Scout · Locals
- **StartingPerks:** `Jazz_Perk_Carlos`, `Pessimist`, `Stealthy`, `Throwing`
- **Named:** `Jazz_Perk_Carlos` — Тихая тень / Silent Shadow
- **Type / feasibility / runtime:** passive · **MEDIUM** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Скрытное убийство ножом не выдаёт позицию и возвращает потраченные ОД / A stealth kill with a thrown knife doesn't break the squad's stealth and refunds the AP spent
- **Mechanics (article):** When Carlos scores a stealth kill using a thrown knife, the squad's Hidden/stealth state is not broken and the AP spent on the throw is refunded.

### Кардан (`cord` / `Jazz_Cord`)

- **Priority / role / affiliation:** low · Mechanic · MERC
- **StartingPerks:** `Jazz_Perk_Cord`, `MrFixit`, `JackOfAllTrades`, `Scoundrel`
- **Named:** `Jazz_Perk_Cord` — Тихий ремонт / Quiet Repair
- **Type / feasibility / runtime:** passive · **HARD** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Ремонт обходится быстрее и дешевле / Repairs go faster and cost less
- **Mechanics (article):** Repair actions performed by Cord cost 15% less time and 10% fewer Parts.

### Девин (`devin` / `Jazz_Devin`)

- **Priority / role / affiliation:** low · Demolitions · Locals
- **StartingPerks:** `Jazz_Perk_Devin`, `Loner`, `DesignerExplosives`, `BreachAndClear`
- **Named:** `Jazz_Perk_Devin` — IRA / IRA
- **Type / feasibility / runtime:** passive · **MEDIUM** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Взрывы Девина крушат укрытия и поджигают всё вокруг / Devin's explosions wreck cover and set the area on fire
- **Mechanics (article):** Any explosion triggered by Devin deals +100% damage to structures/cover and has a 25% chance to apply Burning to units caught inside the blast radius.

### Эскимо (`eskimo` / `Jazz_Eskimo`)

- **Priority / role / affiliation:** low · Sniper · Locals
- **StartingPerks:** `Jazz_Perk_Eskimo`, `Stealthy`, `SteadyBreathing`, `TrueGrit`
- **Named:** `Jazz_Perk_Eskimo` — Тюремная выдержка / Prison-Hardened
- **Type / feasibility / runtime:** passive · **EASY** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Годы в тюрьме Альмы закалили Эскимо: он не паникует и стреляет метко даже раненым / Years in the Alma prison hardened Eskimo — he doesn't panic and stays accurate even wounded
- **Mechanics (article):** Eskimo's CTH with rifles is not reduced by the Wounded status, and he is immune to Panicked while below 50% health.

### Грейс (`grace` / `Jazz_Grace`)

- **Priority / role / affiliation:** low · Thrower · AIM
- **StartingPerks:** `Jazz_Perk_Grace`, `Throwing`, `Pessimist`, `FirstThrow`
- **Named:** `Jazz_Perk_Grace` — Точный бросок / Precise Toss
- **Type / feasibility / runtime:** passive · **MEDIUM** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Первый брошенный за ход нож никогда не промахивается по ближней цели / The first knife Grace throws each turn never misses a nearby target
- **Mechanics (article):** The first thrown-knife attack Grace makes each of her turns against a target within 4 tiles cannot miss (auto-hit), though it can still be Grazed by cover/armor as normal.

### Скала (`highball` / `Jazz_Highball`)

- **Priority / role / affiliation:** low · Doctor · AIM
- **StartingPerks:** `Jazz_Perk_Highball`, `Savior`, `OldDog`, `JackOfAllTrades`
- **Named:** `Jazz_Perk_Highball` — Полевой химик / Field Chemist
- **Type / feasibility / runtime:** passive · **HARD** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Может скрафтить стимулятор из бинтов без доступа к сумке врача — раз в игровой день / Can craft a combat stimulant from Meds without access to a Doctor's Bag facility — once per in-game day
- **Mechanics (article):** Once per in-game day, while in any sector, Highball may craft one `CombatStim` from 3× `Meds` using a Medical skill check (succeeds automatically at Medical ≥50); no Doctor's Bag facility or workbench required.

### Убийца (`hitman` / `Jazz_Hitman`)

- **Priority / role / affiliation:** low · Sniper · Locals
- **StartingPerks:** `Jazz_Perk_Hitman`, `TakeAim`, `SteadyBreathing`, `DedicatedCamper`
- **Named:** `Jazz_Perk_Hitman` — Вырубить / Knock Out
- **Type / feasibility / runtime:** active · **MEDIUM** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Раз за миссию выстрел из винтовки вырубает вместо убийства / Once per mission, a rifle shot knocks the target out instead of killing them
- **Mechanics (article):** Active ability, once per mission: Hitman's next rifle shot that would hit applies Unconscious to the target instead of dealing damage. The ability recharges after Hitman scores a normal (lethal) kill.

### Хоббит (`hobbit` / `Jazz_Hobbit`)

- **Priority / role / affiliation:** low · Demolitions · MERC
- **StartingPerks:** `Jazz_Perk_Hobbit`, `Pessimist`, `DesignerExplosives`, `BreachAndClear`
- **Named:** `Jazz_Perk_Hobbit` — Несу вас / I'll Carry You
- **Type / feasibility / runtime:** passive · **HARD** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Товарищи по отряду ставят взрывчатку и мины так же хорошо, как Хоббит / Squadmates plant explosives and mines as well as Hobbit does
- **Mechanics (article):** While Hobbit is present in the same active squad and sector, any other merc placing an explosive device, mine, or trap uses Hobbit's Explosives skill for that action whenever their own is lower.

### Кульба (`kulba` / `Jazz_Kulba`)

- **Priority / role / affiliation:** low · Autorifleman · Locals
- **StartingPerks:** `Jazz_Perk_Kulba`, `AutoWeapons`, `MrFixit`, `OldDog`
- **Named:** `Jazz_Perk_Kulba` — Оружейник старой закалки / Old-School Gunsmith
- **Type / feasibility / runtime:** passive · **MEDIUM** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Автоматическое оружие Кульбы стреляет точнее и реже заклинивает / Kulba's automatic weapons hit harder and jam less
- **Mechanics (article):** Full-Auto and burst attacks fired by Kulba gain +10% CTH on the first bullet of the burst, and any automatic weapon he carries has a 50% reduced chance to jam.

### Лора (`laura` / `Jazz_Laura`)

- **Priority / role / affiliation:** low · Doctor · AIM
- **StartingPerks:** `Jazz_Perk_Laura`, `Stealthy`, `DesignerExplosives`, `TrueGrit`
- **Named:** `Jazz_Perk_Laura` — Скрытный врач / Silent Medic
- **Type / feasibility / runtime:** passive · **EASY** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Лечение и подъём союзников не выдают позицию Лоры / Healing or reviving an ally doesn't break Laura's stealth
- **Mechanics (article):** If Laura is Hidden, healing a wounded ally or reviving a Downed ally does not reveal her position or end her Hidden status.

### Лаки (`lucky` / `Jazz_Lucky`)

- **Priority / role / affiliation:** low · Autorifleman · AIM
- **StartingPerks:** `Jazz_Perk_Lucky`, `AutoWeapons`, `MartialArts`, `Hotblood`
- **Named:** `Jazz_Perk_Lucky` — Второе дыхание / Second Wind
- **Type / feasibility / runtime:** passive · **MEDIUM** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Раз за бой промах Лаки превращается в попадание / Once per combat, a Lucky miss becomes a hit
- **Mechanics (article):** Once per combat, the first time an attack roll made by Lucky would miss, it is instead treated as a hit (rolled at minimum-success damage). Recharges at the start of the next combat.

### Мясо (`meat` / `Jazz_Meat`)

- **Priority / role / affiliation:** low · Demolitions · MERC
- **StartingPerks:** `Jazz_Perk_Meat`, `DesignerExplosives`, `MeleeTraining`, `TrueGrit`
- **Named:** `Jazz_Perk_Meat` — Толстокожий / Thick-Skinned
- **Type / feasibility / runtime:** passive · **MEDIUM** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Волю Мяса ничем не сломить ниже определённого порога / Meat's Will can't be broken below a certain floor
- **Mechanics (article):** Meat's effective Will can never be reduced below 50 by negative status effects, panic checks, or morale penalties — a brute too dim to know real fear.

### Рикошет (`ricochet` / `Jazz_Ricochet`)

- **Priority / role / affiliation:** low · Melee · MERC
- **StartingPerks:** `Jazz_Perk_Ricochet`, `Loner`, `Throwing`, `MeleeTraining`
- **Named:** `Jazz_Perk_Ricochet` — Рикошет / Ricochet
- **Type / feasibility / runtime:** passive · **MEDIUM** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Смертельный бросок ножа может отскочить на второго врага / A lethal thrown-knife kill can bounce to strike a second enemy
- **Mechanics (article):** When a thrown knife or axe thrown by Ricochet kills its target, there is a 40% chance the blade ricochets to a second random enemy within 3 tiles of the target, dealing 50% of the weapon's normal damage.

### Шенк (`shank` / `Jazz_Shank`)

- **Priority / role / affiliation:** low · Thrower · MERC
- **StartingPerks:** `Jazz_Perk_Shank`, `Optimist`, `Throwing`, `MeleeTraining`
- **Named:** `Jazz_Perk_Shank` — Не трогай меня / Don't Touch Me
- **Type / feasibility / runtime:** passive · **EASY** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Врагам сложнее попасть по Шенку в ближнем бою / Enemies have a harder time landing melee hits on Shank
- **Mechanics (article):** Enemies making a melee attack against Shank suffer −50% CTH for that attack — he's too scrawny and jumpy to pin down.

### Статик (`static` / `Jazz_Static`)

- **Priority / role / affiliation:** low · Mechanic · AIM
- **StartingPerks:** `Jazz_Perk_Static`, `MrFixit`, `JackOfAllTrades`, `Scoundrel`
- **Named:** `Jazz_Perk_Static` — Экономия запчастей / Parts Saver
- **Type / feasibility / runtime:** passive · **HARD** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Ремонт и крафт обходятся дешевле по запчастям — бонус растёт с уровнем Статика / Repairing and crafting cost fewer Parts, and the discount grows with Static's level
- **Mechanics (article):** Repair and craft actions performed by Static cost 5% fewer Parts per Static's current level (level 4 = −20%), capped at −25% at level 5+.

### Штайгер (`steiger` / `Jazz_Steiger`)

- **Priority / role / affiliation:** low · Commander · AIM
- **StartingPerks:** `Jazz_Perk_Steiger`, `NightOps`, `Teacher`, `LeadFromTheFront`
- **Named:** `Jazz_Perk_Steiger` — Ночной инструктор / Night Instructor
- **Type / feasibility / runtime:** passive · **EASY** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Ночью Штайгер обучает соседних союзников лучше стрелять / At night, Steiger's coaching sharpens nearby allies' aim
- **Mechanics (article):** During Nighttime missions, allies within 5 tiles of Steiger gain +5% CTH, reflecting his career as a night-operations instructor.

### Зануда (`vilde` / `Jazz_Vilde`)

- **Priority / role / affiliation:** low · Autorifleman · AIM
- **StartingPerks:** `Jazz_Perk_Vilde`, `AutoWeapons`, `NightOps`, `LeadFromTheFront`
- **Named:** `Jazz_Perk_Vilde` — Ночной автоматчик / Night Gunner
- **Type / feasibility / runtime:** passive · **EASY** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Ночью автоматный огонь Вильде точнее / At night, Vilde's automatic fire is more accurate
- **Mechanics (article):** During Nighttime missions, Full-Auto and burst attacks fired by Vilde gain +15% CTH and his Perception range for spotting is not reduced by darkness.

### Винс (`vince` / `Jazz_Vince`)

- **Priority / role / affiliation:** low · Doctor · Locals
- **StartingPerks:** `Jazz_Perk_Vince`, `Claustrophobic`, `Ambidextrous`, `Teacher`
- **Named:** `Jazz_Perk_Vince` — Полевой наставник / Field Mentor
- **Type / feasibility / runtime:** passive · **EASY** · STUB — `unit_reactions={}`, WIP description in CharacterEffect
- **Description:** Раз за бой лечение или подъём товарища возвращает ему ОД / Once per combat, healing or reviving an ally snaps them back into the fight with bonus AP
- **Mechanics (article):** Once per combat, the first time Vince heals a wounded ally or revives a Downed ally, that ally immediately gains +4 AP that turn.


## 10. Решения владельца (зафиксировать ответом на этот документ)

Не блокируют чтение каталога; блокируют старт кода Wave A/B:

1. Lynx: дописать CTH-range или сузить текст?
2. Принять Simplify-таблицу §5.1–5.3 как контракт реализации (да/править числа)?
3. HARD (§5.3): Simplify сейчас или полный Defer до отдельного strategy-spec?
4. Mike: ок ли замена «detection вне боя» на «bonus first-turn AP»?
5. Nervous vs Buzz: +2 bullets ок рядом с +50% Buzz, или Nervous только −AP?
6. Нужен ли follow-up spec `JAZZ-UNITS-003` перед кодом, или правки статей + точечные AC достаточно?

## 11. Связанные файлы

- Статьи: `docs/design/mercs-ja12/<slug>.md`
- Очередь gaps: `docs/design/mercs-ja12/_generation-queue.md`
- Spec волны генерации: `docs/specs/active/JAZZ-UNITS-002.md`
- Player-facing срез: `docs/showcase/ru/perks.md` / `en/perks.md`
- Runtime hooks: `Code/System_OR_Grenade.lua`, `System_OR_Traps.lua`, `System_OR_Unit.lua`, `System_SectorOperations.lua`, `items.lua` (Buzz)
- Companions: `CharacterEffect/Jazz_Perk_*.lua`
- Иконки: `Perks/Personal/*.png`
