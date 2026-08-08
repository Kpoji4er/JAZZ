---
id: JAZZ-UNITS-005
status: approved
owner: project-owner
systems:
  - units-progression-specializations
  - localization
  - merc-portraits
  - assets-and-ui
repositories:
  - jazz
  - jazz-units
  - jazz_assets
risk: high
generated_data: true
runtime_validation: required
write_set:
  - Code/System_AME_*.lua
  - Code/System_AimHiringFilters.lua
  - Code/SatelliteSquad.lua
  - items.lua
  - metadata.lua
  - English.csv
  - Russian.csv
  - Icons/Flags/
  - docs/design/ame-mercenary-exchange.md
  - docs/tools/_ame_copy_bank.py
  - docs/tools/_gen_ame_roster_60.py
  - docs/tools/_gen_ame_unitdata.py
  - docs/tools/_audit_ame_copy.py
  - docs/technical/systems/units-progression-specializations.md
  - docs/technical/systems/file-coverage.md
  - docs/wiki/
  - docs/showcase/
  - ../jazz-units/UnitData/JAZZ_AME_*.lua
  - ../jazz-units/items.lua
  - ../jazz-units/metadata.lua
  - ../jazz-units/MercPortraits/
  - ../jazz_assets/
  - ../jazz_assets/**/Flags/**
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz-units/items.lua
  - jazz-units/metadata.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-UNITS-005: African Mercenary Exchange (локальный рынок наёмников)

## Проблема

После найма AIM/MERC в длинной кампании JAZZ не хватает **массового локального кадрового рынка**: дешёвых обучаемых бойцов с живой ротацией. Простой пул «40 слабых местных» без отдельной экономики/UI рискует читаться как расовый стереотип и дублирует AIM. Нужна асимметрия к AIM: отдельный PDA-сайт, категории по опыту (якорь — тиры Легиона), акцент на **росте**, специалисты как дефицит, живой рынок труда.

## Цели

- Отдельный PDA browser **African Mercenary Exchange (AME)** — сайт «как AIM, чуть другой», не вкладка внутри AIM.
- Два рынка: **AIM** = готовые профессионалы; **AME** = местные бойцы с потенциалом роста.
- Категории качества, привязанные к Legion class tiers (не к «элите AIM»).
- Живая витрина: не весь пул сразу; периодическая ротация (уход / гибель / уход в Легион / найм другими).
- Specialist floor в пуле; специалисты — самые дорогие на AME, но дешевле сопоставимого AIM.
- Статы и цены по контракту ниже; Wisdom у дешёвых тиров выше, чем у Legion T1 (рост).
- **Новые Nationality** (африканский пул) **включая флаги** в UI (`MercFlagImage` / hiring card) — в скоупе JAZZ, без зависимости от внешних nationality-lib модов.

## Non-goals

- Восточноевропейский / латиноамериканский рынки (заложить multi-market API, не реализовывать второй регион).
- Отдельный messenger / свой contract protocol (reuse vanilla `MercCanContact` / `StartMercChat` / `HireMerc`).
- 40 handcrafted именных перков и уникальных AIM-чатов уровня JA12.
- Клон Legion T4 Merc\* / полный AIM Elite-пакет на AME.
- Изменение баланса самих Legion enemy UnitData.
- Quest-gated unlock первой вкладки AME (v1: сайт доступен с начала кампании как AIM).
- Запись новых neural voice banks (v1 = remesh + Legion alt `*-1.opus`).
- Полный ISO-набор всех стран мира (только AME-пул ниже + reuse ванильных).
- Обязательная зависимость от Workshop «all nationalities lib».

## Требования

### Сайт и найм

- `JAZZ-UNITS-005-REQ-001` — новый PDA browser mode `ame` с вкладкой в `PDABrowser` / `PDABrowserTabState`; URL/chrome RU+EN «African Mercenary Exchange» / «Африканская биржа наёмников».
- `JAZZ-UNITS-005-REQ-002` — root dialog class — **subclass** `PDAAIMBrowser` (сохранить post-hire / messenger совместимость); отдельный XTemplate skin (не замена mode `aim`). На AME Loadout **нет** блока Traits/Perks («Черты») — только Equipment/Backpack; AIM browser без изменений.
- `JAZZ-UNITS-005-REQ-003` — найм/продление/увольнение через существующий pipeline (`MercCanContact` → chat → `NetSyncEvent("HireMerc")` / JAZZ `LocalHireMerc`); без нового network event.
- `JAZZ-UNITS-005-REQ-004` — пул AME **не** проходит фильтры AIM (`IsMetAIMMerc` / specialization tabs AIM). AIM «My Team» может показывать нанятых AME как уже нанятых игроком (как сейчас любой Hired).
- `JAZZ-UNITS-005-REQ-005` — AME-наймы **не** считаются в AIM contact-cap (`Affiliation == "AIM"`). Отдельного жёсткого cap на число AME-контрактов в v1 нет (баланс ценой и ротацией).

### Организация и данные

- `JAZZ-UNITS-005-REQ-006` — публичный org id: `AME`. UnitData слотов: `JAZZ_AME_01`…`JAZZ_AME_60` (`IsMercenary = true`). Поле `Affiliation = "AME"`. `Affiliation = "Legion"` запрещён для hireable AME.
- `JAZZ-UNITS-005-REQ-007` — пул = **60** слотов. Одновременно **14–16** hireable Available (цель ~15). **Видимость в магазине AME:**
  1. **Available** — можно нанять;
  2. **Unavailable / gone** — уже нельзя нанять, но карточка **остаётся в UI** (серая / disabled): минимум причины `JoinedLegion` и `Killed` (погиб); опционально тот же UX для `HiredElsewhere`, если слот считаем окончательно потерянным для найма;
  3. **Hired игроком** — в My Team / эквиваленте, как у AIM;
  4. **`NotListed`** (ещё не появлялся на рынке) — **не виден** никогда, пока tick не выведет слот в Available.
  Не показывать «будущих» бойцов заранее.
- `JAZZ-UNITS-005-REQ-008` — слот задаётся **design-roster** [`docs/design/ame-roster-60.md`](../../design/ame-roster-60.md) (или эквивалент generator→тот же контракт): имя (REQ-029), категория, CombatRole, статы, 0–2 **common** traits, **опционально 1 Personality-tier perk** (см. REQ-032), specialization, `Nationality`, appearance, portrait, `VoiceResponseId`, salary, **один фиксированный** starting kit, полная игровая `Bio` RU/EN (проза карточки найма). **`Randomization` инвентаря/лута найма выключен** — один вариант на слот, без invent-roll. **Кит по `tier_label` (потолки):** **Irregulars ≤ 1-2**; **Fighters ≤ 1-3**; **Hardened ≤ 2-1**; Specialists ≤ 2-1. T2-2+ (`AK47`, `RPK`/`RPK74`, …) запрещены всем. T2-1 sidearm/carbine/SG (`HiPower`, `Mini14`, `Ithaca`) — Hardened/Specialists, не Fighters. **ПП в стартовых китах — винтаж T1:** `Thompson`, `M3GreaseGun`, `PPS43`, `PPSH`, `MP40`, `MAT49`, `Sterling` (не `UZI`/T2 compact). **`Type56` — потолок штурмовика AME и только у Hardened** (не Fighters, не Specialists). **`SKS` и T1 bolt (`Gewehr98`) — только Sniper.** Irregulars: нож/мачете/пусто + scrap ≤1-2 (револьверы, `DoubleBarrelShotgun`, редко `Winchester1894`). Fighters: Winchester / `M1897`/`Auto5` / `STG44` / T1 ПП / `Colt1911` — без СКС/bolt и без T2-1. Machinegunner → `MAC2429` / `BAR`. **Бинты:** Fighters ~40%; Hardened всегда. **Sapper:** часть `PipeBomb` (+ `Detonator`). Биография объясняет ключевые статы.
- `JAZZ-UNITS-005-REQ-032` — **sparse personality:** ровно **12 из 60** слотов (`~20%`) получают **ровно одну** Personality-tier perk в `StartingPerks` рядом с common traits. Разрешённый пул: `Negotiator`, `Scoundrel`, `Psycho`, `Stealthy`, `Optimist`, `Pessimist`, `Loner`. **Запрещены** на AME: `Jazz_Perk_Mimicry`, `Jazz_Perk_Veteran`, signature/named perks, Bronze/Silver trees. Канон слотов: `01 Negotiator`, `03 Negotiator`, `06 Loner`, `11 Psycho`, `14 Scoundrel`, `21 Pessimist`, `32 Stealthy`, `38 Optimist`, `39 Psycho`, `47 Scoundrel`, `50 Optimist`, `56 Stealthy` (карта в `_gen_ame_roster_60.py` / `_apply_ame_personality_traits.py`). Остальные 48 слотов — **без** Personality. REQ-002 сохраняется: AME Loadout **не** показывает Traits strip (personality видна после hire / в unit UI, не на полке AME).
- `JAZZ-UNITS-005-REQ-009` — после первого hire слот **фиксируется** (статы/имя/портрет/kit baseline) до конца кампании; ротация его не переписывает, пока `HireStatus` связан с игроком (Hired / Available после dismiss с тем же identity).

### Категории (асимметрия к Легиону)

- `JAZZ-UNITS-005-REQ-010` — четыре категории качества (фильтры сайта):

| id | UI EN | UI RU | Якорь |
|---|---|---|---|
| `Irregulars` | Irregulars | Новобранцы | ниже T1 / ≈ Recruit− |
| `Fighters` | Fighters | Бойцы | Legion T1 |
| `Hardened` | Hardened | Закалённые | Legion T2–T3 line |
| `Specialists` | Specialists | Специалисты | role peak, не T4 AIM-клон |

**Specialists — одна вкладка** (без подфильтров Medic/Instructor/Sniper/Sapper). Роль видна на карточке (`CombatRole` / specialization), не отдельным табом.

- `JAZZ-UNITS-005-REQ-027` — внутри **Fighters** и **Hardened** часть слотов — боевые подроли (не Specialists-filter):

| CombatRole | Specialization (типично) | Common traits (не signature abilities) |
|---|---|---|
| Rifle / general | Marksmen / AllRounder | 0–1 common perk |
| Autorifleman | Autoriflemen | часто `AutoWeapons` |
| Machinegunner | HeavyWeapons | часто `HeavyWeaponsTraining` и/или `AutoWeapons` |
| Grenadier | HeavyWeapons | часто `Throwing` и/или `HeavyWeaponsTraining` |

**Specialization icons (карточка найма):** у Irregulars / Fighters / Hardened только квартет `AllRounder` · `Autoriflemen` · `HeavyWeapons` · `Marksmen`. Роли `Doctor` / `Mechanic` / `ExplosiveExpert` / `Leader` — **только** у Specialists (Medic / Mechanic / Sapper / Instructor). Sniper-Specialists — `Marksmen`.

Целевая доля в сумме Fighters+Hardened пула: **не менее ~30%** слотов с CombatRole ∈ {Autorifleman, Machinegunner, Grenadier}. Kit и specialization согласованы с ролью. Signature abilities / именные Jazz_Perk_* на эти слоты не выдаются.

### Живой рынок

- `JAZZ-UNITS-005-REQ-011` — каждые **14** дней campaign time (2 weeks) детерминированный market tick (`Game.id` + day + slot seed; runtime `AME_TICK_DAYS = 14`):
  - часть Available уходит в terminal/unavailable: `JoinedLegion` / `Killed` (и при необходимости `HiredElsewhere`) — карточка **остаётся видимой**, но Contact/hire disabled + reason UI (REQ-007);
  - `Missing` может быть временным Away (снова Available позже) или terminal — зафиксировать при implement; по умолчанию temporary и **скрыт**, пока снова не Available;
  - на витрину выходят новые слоты из `NotListed` до **14–16** hireable Available (unavailable-карточки не съедают этот бюджет hireable);
  - Hired игроком не ротируются;
  - `NotListed` нельзя увидеть и нельзя нанять.
- `JAZZ-UNITS-005-REQ-012` — specialist soft-guarantee: ни одна из ролей Medic / Instructor / Sniper не держится **0 Available на витрине и 0 PendingArrival** дольше **одного tick cycle (~14 дней)** подряд; следующий tick обязан выставить минимум одного слота этой роли (из пула или reroll свободного Away-слота).

### Specialist floor и цена

- `JAZZ-UNITS-005-REQ-013` — в пуле 60 слотов одновременно выполняются минимумы ролей (после init и после каждого полного rebuild пула):

| Role | Count |
|---|---:|
| Medic | 2–3 |
| Instructor | 2–3 |
| Sniper | 2 |
| Sapper | 1–2 |
| Mechanic | 2 |

Остальные слоты — Irregulars / Fighters / Hardened (целевая плотность витрины: Irregulars ~40%, Fighters ~35%, Hardened ~20%, Specialists ~5–8% видимых).

- `JAZZ-UNITS-005-REQ-014` — лестница зарплат AME (owner weekly bands, playtest 2026-08-05):  
  `Irregulars < Fighters < Hardened ≪ Specialists`. JA3 hire week ≈ `StartingSalary × 7`.  
  Ориентиры **$/week → daily `StartingSalary`**: floor cheap Irregulars ~**$50**/wk (~7); Irregulars **50–350**/wk (**7–50**); Fighters **400–750**/wk (**57–107**); Hardened **750–1000**/wk (**107–143**); Specialists **1100–2000**/wk (**157–286**). Specialists stay **below** Igor/Barry weekly (~$3150 / $3290). Apply: `_apply_ame_weekly_salaries.py` / `_sync_ame_salary_items.py`.
- `JAZZ-UNITS-005-REQ-015` — Instructor: обязательный perk `Teacher` + статы Instructor-band (REQ-016); цена в верхнем диапазоне Specialists (дороже Medic того же пула при прочих равных).

### Статы (нормативные диапазоны)

- `JAZZ-UNITS-005-REQ-016` — генератор бросает статы в диапазонах (inclusive). Primary: Health, Agility, Dexterity, Strength, Will, Marksmanship, Wisdom. Soft skills по роли.

Лестница боевых статов: Agi / Dex **медиана ≈60 / 65 / 70**; Marks **≈45 / 55 / 60** для Irregulars / Fighters / Hardened (novice Marks −15 от прежней лестницы, остальные −10). **Health и Strength** — широкий разброс (могут отклоняться сильнее медианы категории). Потолок Agi/Dex пула **70**. Perk tax: сильные комбо (`HeavyWeaponsTraining`+`AutoWeapons`, dual combat perks) режут Marks ниже медианы категории.

**Irregulars**

| Stat | Min–Max |
|---|---|
| Health | **75–95** (широкий разброс; часто высокий) |
| Agility | **медиана ≈60** (band ≈54–68; потолок пула 70) |
| Dexterity | **медиана ≈60** (band ≈50–66) |
| Strength | **42–80** (широкий разброс) |
| Will | 20–40 |
| Marksmanship | **медиана ≈45**; слабые стрелки (empty hands / «не умеет») **≈30–35**; остальные ≈41–49 |
| Wisdom | 50–80 |
| Leadership | 0–15 |
| Mechanical | **обычно 0** (0–5); редкие исключения до 20 |
| Explosives | **обычно 0** (0–5); редкие исключения до 25 |
| Medical | 0–15 |

**Fighters**

| Stat | Min–Max |
|---|---|
| Health | **70–90** (широкий разброс) |
| Agility | **медиана ≈65** (band ≈54–70; потолок пула 70) |
| Dexterity | **медиана ≈65** (band ≈52–66) |
| Strength | **48–80** (широкий разброс) |
| Will | 20–40 |
| Marksmanship | **медиана ≈55** (ниже Hardened; perk tax HW/Auto → ~48–54) |
| Wisdom | 45–75 |
| Leadership | **обычно 0–15**; в пуле Fighters+Hardened суммарно **1–2** слота с Leadership **≈50** |
| Mechanical | **обычно 0** (0–5); в пуле Fighters+Hardened суммарно **1–2** слота с Mechanical **≈30** |
| Explosives | **обычно 0** (0–10); **2** слота Fighters с Explosives **≈30** |
| Medical | 0–20 |

**Hardened** (ветераны — единственная категория со средним Will)

| Stat | Min–Max |
|---|---|
| Health | **78–94** (широкий разброс) |
| Agility | **медиана ≈70** (band ≈58–70; у потолка пула) |
| Dexterity | **медиана ≈70** (band ≈56–70) |
| Strength | **64–92** (широкий разброс) |
| Will | 45–65 |
| Marksmanship | **медиана ≈60, потолок ≈60** (perk tax HW+Auto / dual → ниже; Sniper-спецы ≤70) |
| Wisdom | 35–65 |
| Leadership | **обычно 0–20**; делит с Fighters пул **1–2** слотов Leadership **≈50** (REQ выше) |
| Mechanical | **обычно 0** (0–5); делит с Fighters пул **1–2** слотов Mechanical **≈30** |
| Explosives | **обычно 10–20**; **2** слота Hardened с Explosives **30–40** |
| Medical | 0–25 |

Hardened не может одновременно иметь Marksmanship ≥ 90 и Wisdom ≥ 70.

**Medic**

| Stat | Min–Max |
|---|---|
| Medical | **60–70** (потолок AME Medical **70**; не AIM 85+) |
| Marksmanship | **20–30** (боевой dump) |
| Wisdom | 60–85 |
| Will | 20–40 |
| Leadership | 20–50 |
| Health | 60–85 |
| Agility | 45–60 |
| Dexterity | 45–60 |
| Strength | 35–55 |
| Explosives | 0–25 |
| Mechanical | 0–25 |

**Instructor**

| Stat | Min–Max |
|---|---|
| Leadership | **55–70** (потолок AME Leadership **70**; не AIM 85+) |
| Wisdom | 75–95 |
| Marksmanship | **30–40** (навыки ↑, бой ↓) |
| Health | 60–75 |
| Agility | 45–55 |
| Dexterity | 45–55 |
| Strength | 48–60 |
| Will | 20–40 |
| Medical | 20–50 |
| Mechanical | 30–70 |
| Explosives | 20–50 |

**Sniper**

| Stat | Min–Max |
|---|---|
| Marksmanship | **61–70** (потолок AME Marks; не AIM 90+) |
| Agility | 55–70 |
| Dexterity | 55–65 |
| Wisdom | 45–75 |
| Will | 20–40 |
| Health | **45–60** (высокая меткость → хрупкое тело) |
| Strength | 40–55 |
| Leadership | 0–25 |
| Mechanical | 20–50 |
| Explosives | 0–20 |
| Medical | 0–20 |

**Sapper**

| Stat | Min–Max |
|---|---|
| Explosives | **60–69** (потолок AME Explosives **<70**; не AIM 85+) |
| Marksmanship | 20–30 |
| Dexterity | 70–88 |
| Wisdom | 50–80 |
| Will | 20–40 |
| Health | 55–75 |
| Agility | 65–80 |
| Strength | 50–75 |
| Mechanical | 40–70 |
| Medical | 0–25 |
| Leadership | 0–25 |

**Mechanic**

| Stat | Min–Max |
|---|---|
| Mechanical | **60–70** (потолок AME Mechanical **70**; не AIM 85+) |
| Marksmanship | **20–30** (боевой dump) |
| Wisdom | 50–70 |
| Will | 20–40 |
| Health | 60–85 |
| Agility | 45–55 |
| Dexterity | 45–55 |
| Strength | 50–65 |
| Leadership | 0–15 |
| Explosives | 0–15 |
| Medical | 0–15 |

AME soft-skill peaks (Medical / Leadership / Mechanical / Marksmanship) **≤70**; Explosives **<70**. Не AIM-уровень 85–100.

- `JAZZ-UNITS-005-REQ-017` — UI карточки показывает категорию и **Potential** label от Wisdom: Low (ниже 45), Medium (45–64), High (65 и выше). Отдельного UnitData-поля Potential в v1 нет.
- `JAZZ-UNITS-005-REQ-018` — `StartingLevel = 1` у всех 60 слотов. Категория задаёт исходный stat/kit/experience profile, но не бесплатные уровни: AME продаёт потенциал роста на службе.

### Внешность, голос, контент

- `JAZZ-UNITS-005-REQ-019` — appearance: **уникальный клон на слот** `JAZZ_AME_01`…`60` (`ModItemAppearancePreset`, group `AME`). Donor — Rebels / Militia / Legion; Hardened/Specialists могут брать **GrandChien**. Карта слот→donor: [`ame-appearance-map.json`](../../design/ame-appearance-map.json) + поле на карточке roster. **Ровно один AME-синий акцент** (Hat → Hat2 → Shirt → BodyC2; **не** Pants/ботинки); прочий Legion-red / лишний blue → muted slate. **Кожа рук** (`BodyColor` EditableColor1) — тёмный African bank; **`HeadColor` = (0,0,0)** как vanilla. **Голова:** без `Faction_Legion_Head_*` (war-paint); Ca/As/AIM/`Male_Head`/Legion painted → named Af (Chimurenga/Pierre/Magic/…) / `Head_F_Af_NPC_*` / `Head_M_IMP_01`. Исходные presets **не править**. Female: Af head. Tooling: `_gen_ame_appearances.py`.
- `JAZZ-UNITS-005-REQ-020` — голос (Jazz remesh majority + `PierreMerc` + small IMP minority):
  - ~7/8 слотов → Jazz remesh (`Jazz_AME_Male_Low` / `Male_Hard` / `Female`) или `PierreMerc` (полный hireable Af bank); ~1/8 → IMP pool (cycle 01..03 по полу; VR → `IMP_male_01` / `IMP_female_01`);
  - bucket `(slot-1)%8`: `7` → IMP; `3` → `PierreMerc` (males); иначе Jazz remesh (Hardened/Specialists и bucket 1/5 → `Male_Hard`);
  - `FallbackMissingVR`: IMP/`PierreMerc` → тот же VR; remesh → `LegionRaider` / `ArmySoldier` / `AnneLeMitrailleur` — **не** Ice/Fox.
  Calm slots на remesh **не** из `BecomeAware` → тишина; faction-specific Legion/Major/Grand Chien takes не входят в shared hireable banks. EN subtitle совпадает с audible donor line, RU переводит услышанную реплику, а не имя reused gameplay slot. `_import_legion_raider_alt_voices.py` + `_gen_ame_voice_responses.py` + `_apply_ame_voice_remap.py`; назначение `_gen_ame_roster_60.py`.
- `JAZZ-UNITS-005-REQ-021` — портреты: банк ≥ **16** уникальных лиц в `jazz-units/MercPortraits` (AME); reuse банка между слотами разрешён; специалисты стремятся к меньшей коллизии лиц на одной витрине.
- `JAZZ-UNITS-005-REQ-022` — у каждого слота **полная игровая биография** (поле `Bio` на карточке найма) RU+EN: короткий живой портрет от 3-го лица — прошлое, темперамент, одна человеческая деталь и мягко вплетённая сильная или слабая сторона; без мета-цифр, названий статов/тиров и пересказа анкеты. RU и EN редактируются как самостоятельная естественная проза, а не построчная калька; канон обеих версий хранит `_ame_copy_bank.py` и показывает design-roster. Hire chat — шаблонные фразы по категории/роли.
- `JAZZ-UNITS-005-REQ-023` — background flavor tags в bio (не отдельный filter v1): ex-army / militia / police / hunter / rebel — без привязки «дешёвый = раса».
- `JAZZ-UNITS-005-REQ-028` — **происхождение / Nationality + флаги (в скоупе)**:
  1. Слоты AME получают `Nationality` из африканского пула; доля **Grand Chien** **~20–35%**.
  2. **Reuse ванильных** id, где уже есть: как минимум `GrandChien`, `SouthAfrica` (и другие vanilla African/Caribbean id только если осознанно нужны).
  3. **Сгенерировать новые Nationality** для AME-пула (ModItem / preset registration в комплекте JAZZ) с display name RU+EN и **флаг-иконкой**, чтобы `<MercFlagImage()>` / карточка найма показывали флаг, а не пустоту.
  4. Минимальный набор **новых** id v1 (public IDs): `Nigeria`, `Kenya`, `Angola`, `Mali`, `Congo`, `Ghana`, `Senegal`, `Ethiopia`. Дополнительные африканские id можно добавить в том же change set, не сужая этот минимум.
  5. Flag assets — PNG (или формат, который принимает UI флагов JA3) в declared write set (`Icons/Flags/` и/или `jazz_assets`); путь зарегистрирован в nationality preset.
  6. Не-африканское меньшинство допустимо редко, не как норма витрины.
  7. Без обязательной зависимости от внешних nationality workshop-модов.
- `JAZZ-UNITS-005-REQ-029` — **имена**: африканские first/last (или single given name) из AME name pools (можно опереться на пулы Legion/Rebels/`EliteEnemyNames`, без US/EU AIM-roster). Поле **`Name`** = полное формальное имя (карточка/био). Поле **`Nick`** = короткое отображаемое в hire list / chat / URL: явная кличка если есть (Hardened), иначе **только given name** (без фамилии; титулы `Dr.`/`Captain` снимаются). Дефисные given (`Jean-Baptiste`) → первая часть (`Jean`); длина Nick **≤9** (тайл списка обрезает). **RU+EN:** Name/Nick/AllCapsNick в обеих таблицах (`docs/tools/_ame_names_ru.py` + generator); RU — кириллическая транслитерация (как в био). Owner UX 2026-08-03: не дублировать полное `Name` в `Nick`.

### Docs / loc

- `JAZZ-UNITS-005-REQ-024` — design companion `docs/design/ame-mercenary-exchange.md` с таблицами категорий/статов/цен (зеркало контракта).
- `JAZZ-UNITS-005-REQ-025` — player-facing: `docs/wiki/` + `docs/showcase/ru|en` (mercenaries / новый slug при необходимости); technical: `units-progression-specializations.md` + `file-coverage.md`.
- `JAZZ-UNITS-005-REQ-026` — все новые UI/bio строки в `Russian.csv` и `English.csv` (audit needs=0).

## Инварианты и ограничения

- Не ломать AIM browser, IMP, Bobby Ray, existing Jazz_* mercs.
- Deterministic rolls: тот же `Game.id` + campaign day + slot → тот же tick результат на всех клиентах.
- Save/load: market state (`PDABrowserTabState.ame`, per-slot roll identity, Away reasons, next tick time) сериализуется; old saves без AME получают init на load.
- Co-op: hire остаётся на sync path HireMerc.
- AME UnitData не используют enemy AI archetype как обязательный combat brain для player mercs.
- Generated data: sync `UnitData` companions + `items.lua` + `metadata.lua` jazz-units; XTemplate/tab data в jazz.
- Не пушить без отдельного одобрения.

## Acceptance criteria

- `JAZZ-UNITS-005-AC-001` — static: spec Schema OK; design companion присутствует; public ids `ame` / `AME` / `JAZZ_AME_01..60` задокументированы.
- `JAZZ-UNITS-005-AC-002` — static/editor: PDA mode `ame` зарегистрирован; XTemplate loads; AIM mode `aim` не заменён AME skin.
- `JAZZ-UNITS-005-AC-003` — runtime: AME показывает 14–16 hireable Available + visible disabled карточки `JoinedLegion`/`Killed` (найм недоступен); `NotListed` отсутствуют в UI; Hired игрока в My Team; фильтры категорий работают; AIM roster не содержит Available AME.
- `JAZZ-UNITS-005-AC-004` — runtime: hire AME → squad/arrival как AIM; rehire/dismiss; co-op sync hire (если net test доступен).
- `JAZZ-UNITS-005-AC-005` — static: пул 60; specialist counts в диапазонах REQ-013; статы sample слотов внутри REQ-016; ≥30% Fighters+Hardened с CombatRole autorifle/MG/GL; Lead≈50 и Mech≈30 counts 1–2; bio+Nationality заполнены; доля Grand Chien в ориентире REQ-028; все новые id из REQ-028 зарегистрированы с флаг-ассетом; имена африканские (REQ-029); Nick преимущественно у Hardened.
- `JAZZ-UNITS-005-AC-011` — static: ровно **12** AME UnitData содержат одну Personality-tier perk из пула REQ-032; остальные 48 — без Personality; common traits на personality-слотах сохранены; Mimicry/Veteran отсутствуют на AME.
- `JAZZ-UNITS-005-AC-010` — runtime/human: на карточке AME-мерка с новым Nationality (например Nigeria/Kenya) виден флаг через тот же UI path, что AIM (`MercFlagImage` / equivalent); `GrandChien` / `SouthAfrica` тоже корректны.
- `JAZZ-UNITS-005-AC-006` — runtime: после +14d market tick меняет витрину детерминированно; Hired игроком сохраняются; soft-guarantee специалиста срабатывает при искусственном нуле.
- `JAZZ-UNITS-005-AC-007` — runtime/human: Instructor имеет `Teacher`; salary Specialists выше Hardened; Instructor не дешевле Medic в сопоставимой выборке.
- `JAZZ-UNITS-005-AC-008` — static: loc needs Russian=0, English=0 для AME строк; wiki + showcase RU/EN обновлены.
- `JAZZ-UNITS-005-AC-009` — human: карточка показывает category + Potential; рост дешёвого Fighter за длительную кампанию ощутим относительно стартового Marks (playtest owner).

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: патч `PDABrowser` tabs/modes; новый subclass/template; UnitData wave в jazz-units; возможные appearance presets; loc.
- Saves: `[new game recommended]` для чистого рынка; mid-save получает init AME state без wipe AIM roster.
- Network/determinism: market tick и slot rolls только sync/deterministic RNG.
- Generated data: да (units items/metadata, jazz XTemplate/metadata).
- Cross-package: jazz UI/runtime ↔ jazz-units UnitData/portraits; jazz_assets только если понадобятся texture overrides для blue presets (иначе none).
- Rollback: выключить tab + не грузить AME UnitData / revert commits.

## План и ownership

- Пакет-владелец: jazz (PDA site, market tick, filters, loc/docs), jazz-units (UnitData/portraits/appearance), jazz_assets (только при baked-red blockers).
- Исполнитель: agent / project-owner.
- Reviewer: project-owner.
- Рекомендуемый slice до bulk: mode `ame` + 8 слотов (покрыть все 4 категории + 4 specialist roles) → tick → hire → затем расширить до 60.
- Declared write set: frontmatter.
- Exclusive resources: frontmatter.

## Решение владельца

- Статус: approved (code+data+docs shipped; formal `-Phase Done` blocked until runtime/human AC-003/004/006/007/009/010)
- Кто подтвердил: project-owner
- Дата: 2026-08-03 (implement order: ship full DoD — site + 60 mercs + portraits; unique faces for all 60)
- Уточнение 2026-08-07: owner оставил всем AME `StartingLevel = 1`; soft-guarantee при этом остаётся отдельной для Medic / Instructor / Sniper.

## Evidence

- `JAZZ-UNITS-005-AC-001`: `PASS` (static) — design companion + public ids `ame`/`AME`/`JAZZ_AME_01..60` в spec/docs/code.
- `JAZZ-UNITS-005-AC-002`: `PASS` (static/editor) — `System_AME_Browser*.lua` + metadata code; AIM `aim` path не заменён.
- `JAZZ-UNITS-005-AC-003`: `BLOCKED` (runtime) — код market/filters готов; нужен JA3 playtest витрины.
- `JAZZ-UNITS-005-AC-004`: `BLOCKED` (runtime) — hire wrap static-present; нужен playtest hire→squad.
- `JAZZ-UNITS-005-AC-005`: `PASS` (static) — 60 companions/loot; categories 20/18/10/12; flags `Icons/Flags/f_*.png` + `System_AME_Nationalities.lua`; 60 unique portraits (sha1); kit audit `_audit_ame_kit_tiers.py` violations=0.
- `JAZZ-UNITS-005-AC-011`: `PASS` (static) — `_apply_ame_personality_traits.py` map 12/60; companions+items StartingPerks include mapped Personality; no Mimicry/Veteran on AME.
- `JAZZ-UNITS-005-AC-006`: `BLOCKED` (runtime), `PASS` (targeted static-runtime) — `_test_ame_contract.py` подтверждает deterministic 15-slot window, Hired protection и отдельную guarantee Medic/Instructor/Sniper; нужен +14d live playtest.
- `JAZZ-UNITS-005-AC-007`: `BLOCKED` (runtime/human) — roster salaries/traits static; нужен human card check.
- `JAZZ-UNITS-005-AC-008`: `PASS` (static) — AME loc block in RU/EN CSV; `_audit_ame_copy.py` подтверждает 60 самостоятельных RU/EN bio + profile и точную runtime-проекцию; wiki `african-mercenary-exchange.md`; showcase `ru|en/ame.md` + pages.json.
- `JAZZ-UNITS-005-AC-009`: `BLOCKED` (human) — owner playtest Potential/growth.
- `JAZZ-UNITS-005-AC-010`: `BLOCKED` (runtime/human) — flag assets wired; UI visibility needs in-game card check.

## Documentation delta

- `docs/design/ame-mercenary-exchange.md`, `docs/design/ame-roster-60.md`
- `docs/technical/systems/units-progression-specializations.md`, `file-coverage.md`
- `docs/wiki/african-mercenary-exchange.md`
- `docs/showcase/ru|en/ame.md`, `mercenaries.md`, `pages.json`
- Tools: `_ame_copy_bank.py`, `_audit_ame_copy.py`, `_test_ame_contract.py`, `_gen_ame_unitdata.py`, `_gen_ame_flags.py`, `_gen_ame_portrait_prompts.py`, `_process_ame_portraits.py`, `_apply_ame_personality_traits.py`, `_gen_ame_roster_60.py` (personality map)
