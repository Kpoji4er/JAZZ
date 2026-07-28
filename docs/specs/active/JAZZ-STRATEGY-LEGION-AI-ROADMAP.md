---
id: JAZZ-STRATEGY-LEGION-AI-ROADMAP
status: approved
owner: project-owner
systems:
  - legion-global-ai
  - enemy-squads
  - satellite-ui
repositories:
  - jazz
  - jazz-units
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md
exclusive_resources:
  - GameVar:gv_JAZZ_LegionAI
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ Legion Global AI — roadmap после STRATEGY-002/003

Утверждённый порядок работ. Каждый пункт дальше оформляется отдельным change spec перед реализацией.  
Иконки (часть уже в `SquadsIcons/Enemy/`): REINFORCE, RETRIBUTION, RECRUITER, MANPOWER; TAX — у владельца/рисовальщика.

## Сделано

| ID | Суть |
|---|---|
| JAZZ-STRATEGY-002 | Role icons, task rollover, role EnemySquads, экономика v1 (abstract) |
| Icon bind fix | `SetImage` / pending image до `SquadSpawned` (не GetImage wrapper) |
| JAZZ-STRATEGY-003 | Start supply 50; POI/base → пул аванпоста; Major cap 5000; need-spawn; garrison не дублирует pre-placed оборону |
| JAZZ-STRATEGY-004 | Per-unit `$` prices (37 IDs) + accessors; spawn ещё на flat costs |
| JAZZ-STRATEGY-005 | Officer density (Sgt/8, Lt/15–20, Capt/30; MercCapt для T4); tiers дополняют |
| JAZZ-STRATEGY-006 | Money ledger `$` (schema v2); POI rates; flat costs in `$`; cargo `$` in task UI |

## Валюта (утверждено)

Единый ledger в **реальных деньгах ($)** игры. Abstract `supply` / «очки» после миграции не используются.

Vanilla якоря:

| Item | Cost |
|---|---:|
| TinyDiamonds | 500 (минимальная «монета» лута; округление рейса вверх до 500) |
| BigDiamond | 5000 |
| DiamondNecklace | 9000 |
| **DiamondBriefcase** | **12000** = стандартный полный конвой **аванпост → Major** (один shipment) |
| TheGreenDiamond | 50000 |

- `outpost.money` / `major.money` (имена полей — в дочернем spec; смысл: казна аванпоста и резерв Майора в $).
- Shipment I7→B28 кладёт в инвентарь носителя valuables на **сумму рейса**; полный стандартный рейс = **1× DiamondBriefcase ($12000)**; меньшие/остатки — TinyDiamonds @500 и т.п. Цена видна в UI как у vanilla DB.
- Player loot с конвоя = те же предметы/деньги.
- Major получает $ с доехавшего shipment (и аналогично отдаёт $ supply-конвоем на I7).

## Очередь

### 0. Миграция экономики на $ + POI rates → [JAZZ-STRATEGY-006](JAZZ-STRATEGY-006.md)
Целевые величины в $ (реализованы defaults Region + schema v2):

| Параметр | $ |
|---|---:|
| Outpost starting money | 12000 (≈ 1 shipment) |
| Outpost capacity | **120000** (≈ **10** Major→I7 shipments; полный пул) |
| Major capacity | 1200000 |
| Major starting money | 120000 (≥ 1× outpost fill / 10 cargo) |
| Supply convoy cargo (Major→I7) | **12000** (1 shipment; 10 рейсов = full outpost) |
| Standard diamond shipment (I7→Major) | **12000** (1× DiamondBriefcase) |
| Role costs recon/patrol/qrf/garrison (fallback до per-unit) | ~8000 / ~18000 / ~40000 / ~120000 |
| MajorResponseCost | ~50000 |

Якорь цен юнитов ([STRATEGY-004](JAZZ-STRATEGY-004.md)): один **полный дорогой** garrison ≈ весь outpost pool; без полного бака такой отряд не собирается.

Налог/доход точек (копится на точке → забирает tax collector), $/час:

| POI | $/час |
|---|---:|
| Ферма | 10 |
| Город | 50 |
| Шахта | 250 |

(Соотношение 1 : 5 : 25 сохранено; шкала подогнана под $ и суточный круг.)

Supply-конвой: start outpost ≪ 40% trigger — легален сразу; **spawn не форсить**.

### 1. Конвои (логистика Major ↔ I7)
- Стартовые условия делают supply-конвой легальным; спавн только через обычные гейты.
- Major на старте имеет money на ≥1 supply-конвой в Эрни.
- Shipment: inventory valuables = сумма рейса; полный рейс = DiamondBriefcase $12000.
- Встречные рейсы (I7→B28 и B28→I7) — когда оба гейта выполнены, без force-spawn API.
- **Task UI:** supply/shipment показывают **сумму $** в task-блоке (STRATEGY-006). Tax и будущие money-cargo роли — тем же контрактом.

### 2. Патруль по чужим секторам
- Игнорирует Side; может ходить по секторам игрока.
- Приоритет пустым (нет player squad).

### 3. Reinforce (пограничное усиление)
- Отдельная роль + `legion_REINFORCE_squad.png`.
- Триггер: «страх» / соседство с игроком; держит приграничные сектора.

### 4. Retribution (возмездие Майора)
- С B28 при пороге шума → сектор с максимальным шумом игрока.
- Не путать с локальным QRF.
- Иконка `legion_RETRIBUTION_squad.png` (текущий major/BASE — заменить или оставить рядом: решить в spec).

### 5. Разведданные
- Recon носит конкретный intel: «игрок замечен в секторе XXX».
- QRF / Retribution читают report (частично уже есть — довести контракт и тексты).

### 6. Составы отрядов: цена юнита, пулы роли, политика генерации

Сейчас `LegionGlobalAI_*` — **фиксированные** EnemySquad presets (weighted lists + min/max). Цель — разнести это в data-driven генератор.

#### 6a. Цена каждого `JAZZ_Legion_*` UnitData → [JAZZ-STRATEGY-004](JAZZ-STRATEGY-004.md)
- У каждого легион-юнита своя **цена в $** (`jazz/Code/LegionUnitPrices.lua`; не путать с Cost лута).
- Цель: `money_cost` отряда при спавне = **сумма цен выбранных юнитов** (не плоский role cost из 003) — подключение к spawn ещё не сделано.
- Плоские role costs в п.0 — fallback; **полный дорогой garrison ≈ $120000 ≈ full outpost ≈ 10 shipments**.
- Утверждённая шкала и полная таблица 37 ID — в STRATEGY-004 (Line/Specialist/Leader × T1–T4; ×10 от раннего черновика).

#### 6b. Из каких юнитов может состоять роль → [JAZZ-STRATEGY-005](JAZZ-STRATEGY-005.md) (officer + tier policy)
Для каждой strategic-роли — **allow-list / slots**, не один монолитный preset:

| Роль | Состав (контракт) | Размер (ориентир из 002) |
|---|---|---|
| recon | flanker/стрелки + офицеры по density | 8–12 |
| patrol | смешанное мобильное `JAZZ_Legion_*` | 12–18 |
| garrison | оборона + тяжёлая поддержка | 25–40 |
| qrf | тяжелее patrol (T2+), без «фармового» T1-спама | ~T2 band |
| reinforce | garrison-lite на границе | отдельный band |
| retribution | тяжёлый ударный с HQ | отдельный band |
| supply / shipment / tax / recruiter / manpower | логистика: малый escort + носители | малые составы |

Только public ID с префиксом `JAZZ_Legion_*` (как в 002), если spec не откроет иное.

**Офицеры (утверждено, STRATEGY-005):**

| Leader | Max |
|---|---|
| Sergeant | 1 / **8** чел. (`floor(n/8)`) |
| Lieutenant | 1 / **15–20** чел. (cap `floor(n/15)`) |
| Captain | 1 / **30** чел. (`floor(n/30)`) |
| MercenaryCaptain | обязателен для **T4-отрядов** (не density) |

Уровни офицеров **сосуществуют** в пределах caps (не «только один командир»).

**Class-tier complementarity:** T1…T4 **дополняют** состав; старший tier сильнее, но не вытесняет младших. Poor = больше T1/T2; full/elite **добавляет** T3/T4.

#### 6c. Политика генерации (вместо «всегда один preset»)
При спавне роли director:

1. Берёт **role recipe** (слоты: min/max, веса классов, обязательный officer и т.д.).
2. Считает бюджет: доступные `outpost.money` + `outpost.manpower` (+ caps роли).
3. Собирает состав **жадно/weighted** в пределах recipe + **balance rules** (ниже):
   - **full** — цель к max размера / нормальной кривой;
   - **poor** — к min размера, предпочитает дешёвые tier;
   - если не хватает даже на **min viable** → не спавнить.
4. `manpower_cost` = число юнитов (v1); позже можно weighting по tier.
5. Детерминизм: `InteractionRand` с устойчивым context (`role_home_serial`).

**Balance rules (анти-перекос состава)**  
Отряды не должны быть «12 пулемётчиков». Специалисты ок в разумной доле; «дыры» в саппорте допустимы.

Черновик политики (точные числа — в дочернем spec / recipe):

| Класс (пример) | Soft cap доля / count | Комментарий |
|---|---|---|
| MG / support heavy | ≤ ~25–35% состава или ≤4 в среднем отряде | 4 MG без снайпера — **норм** |
| Sniper / marksman | ≤ ~20–25% или ≤2–3 | 2–3 снайпера без MG — **норм** |
| Officer / commander | density STRATEGY-005 (Sgt/8, Lt/15–20, Capt/30; MercCapt для T4) | несколько уровней ок в пределах cap |
| Specialist (demo, med, …) | низкий soft cap | не стак одинаковых |
| Line rifle / assault | fill remainder | основа отряда |

Правила:
- Hard reject / reroll кандидата, если добавление юнита ломает soft cap класса.
- **Не** требовать полный «идеальный» микс: отсутствие снайпера при наличии MG (и наоборот) — допустимо.
- Перегиб = доминирование одного specialist-класса (пример owner: 12 MG — запрещено).
- Poor-бюджет сначала заполняет line, потом 0–few specialists в пределах cap.

Лимиты (уже частично есть + новые):

| Лимит | Смысл |
|---|---|
| RegularSquadCap / role caps | сколько отрядов роли живо |
| money / manpower | можно ли собрать min/full |
| need-gate (003) | зачем вообще спавнить |
| class soft caps | неравномерность состава |
| (опц.) regional elite cap | сколько T3 одновременно |

**Миграция с фиксированных EnemySquad:**  
v1 — несколько пресетов `_Poor` / `_Full` на роль (быстрый путь);  
v2 — runtime builder по recipe + unit price table + balance rules в `jazz-units` / static Lua.  
Owner preference: **разнести**, не держать один фиксированный состав навсегда → целевой v2; v1 допустим как ступень в том же spec-эпике.

#### 6d. Порядок внутри пункта 6
1. Таблица цен `JAZZ_Legion_*` + документы.  
2. Role recipes (allow-list + min/max + веса).  
3. Generator policy poor/full + resource gates.  
4. Подключение к spawn в `Guardpost_Patrols` (после п.0 $; manpower — с 7b).

### 7. Двухресурсная экономика: $ + люди

Два независимых контура на одних POI:

| Контур | Копится где | Кто возит на I7 | Куда | Тратится на |
|---|---|---|---|---|
| Деньги ($) | city / farm / mine | Tax collector | `outpost.money` | costs отрядов, (опц.) операции |
| Люди (manpower) | city / farm (не шахты) | Recruiter | `outpost.manpower` | размер составов |

Major держит свои пулы (`major.money`, `major.manpower`) с capacity ≫ аванпоста; подпитывает I7 конвоями, когда локально пусто.

#### 7a. Tax collector (сборщик налогов) — $
- Роль доставляет накопленное с POI **на аванпост** (в $).
- Порог выезда: **≥ $1000** суммарно к сбору.
- Не чаще **1 раза в сутки**; за рейс — **маршрут по всем** налоговым секторам региона, затем разгрузка на I7.
- Cap: **2** отряда.
- Иконка: `legion_TAX_squad.png`.

POI $/час (см. п.0): ферма 10 / город 50 / шахта 250.

#### 7b. Людской ресурс — модель

**Накопление recruits на точке**
- City и farm копят `sector.recruits` (или region-keyed stock) каждый час.
- Шахты **не** дают людей (только $).
- Черновые rates (утвердить в spec): ферма **1 чел/сутки**, город **2–3 чел/сутки** (или почасовой эквивалент); cap на точке, чтобы не бесконечно копилось без вербовщика.

**Recruiter (вербовщик)**
- Иконка `legion_RECRUITER_squad.png` (громкоговоритель / рупор; не машина).
- Зеркало tax collector по ритму (черновик, утвердить в spec):
  - cap **2**;
  - не чаще **1 раза в сутки**;
  - за рейс обходит **все** city/farm с recruits;
  - порог выезда: суммарно **≥ N** людей на точках (черновик N = **8–10**, уточнить);
  - разгрузка в `outpost.manpower`.

**Пулы**
- `outpost.manpower` + capacity (черновик: порядка **40–80**, хватит на несколько полных отрядов).
- `major.manpower` + capacity на порядок выше.
- Спавн: `manpower_cost ≈ число юнитов в выбранном составе`; `money_cost` из таблицы ролей / preset.

**Manpower convoy (Major → I7)**
- Иконка `legion_MANPOWER_squad.png` (колонна людей; не SUPPLY-грузовик).
- Условие: `outpost.manpower` ниже trigger (аналог supply % или абсолютный floor) **и** у Major хватает людей на cargo.
- Cargo (черновик): **12–20** человек за рейс.
- Spawn не форсить; только гейты.
- Обратный «избыток людей I7→Major» — non-goal v1.

**Связь со спавном (п.6)**
1. Есть нужда (role request).
2. Recipe роли + generator выбирает poor/full набор юнитов.
3. Хватает money (= сумма цен юнитов) и manpower (= число бойцов).
4. Иначе downgrade / ждать / Major шлёт manpower-конвой.

**Игрок и militia (фаза 7c, позже)**
- Тот же пул recruits на city/farm, когда сектор под игроком: vanilla Militia Training **потребляет** local recruits (или параллельный stock), вместо «бесконечных» сессий.
- Точные цифры и хук в Operation — отдельный spec после стабилизации AI-контура 7a/7b.
- Non-goal v1: ломать текущий militia UX до готового AI recruiter.

#### 7 — порядок внутри пункта
1. 7a Tax ($ delivery) после п.0 валюты.  
2. 7b Recruits + recruiter + outpost/major manpower + manpower convoy.  
3. П.6 подключить manpower-gate к spawn.  
4. 7c Player militia ↔ recruits.

## Иконки (ассеты)

| Файл | Роль |
|---|---|
| `legion_REINFORCE_squad.png` | пограничное усиление |
| `legion_RETRIBUTION_squad.png` | возмездие Майора |
| `legion_RECRUITER_squad.png` | вербовщик (громкоговоритель) |
| `legion_MANPOWER_squad.png` | конвой людей |
| `legion_TAX_squad.png` | сборщик налогов |

## Non-goals этого roadmap

- Включение Global AI вне ErnieIsland / I7 без отдельного решения.
- Смешение tax/recruiter/supply в одну роль.
- Документация с неформальной лексикой.

## Решение владельца

28 июля 2026 — порядок и параметры подтверждены, включая:

- единая валюта **$**; full shipment = **DiamondBriefcase $12000**;
- TinyDiamonds $500 как минимальная монета лута;
- POI $/ч ферма/город/шахта = 10/50/250; tax threshold **$1000**, tax cap **2**, daily full-region circuit;
- двухресурсная модель **$ + manpower**; recruiter с рупором; manpower-конвой с Major при нехватке людей;
- spawn жрёт money+manpower; **per-unit $ prices**, role recipes, poor/full generator, **anti-skew balance** (не 12 MG; 4 MG без снайпера ок и наоборот);
- player militia из того же recruit-пула — фаза 7c после AI;
- rescale пулов/costs в $; convoys без force-spawn; patrol/reinforce/retribution/recon intel как в очереди.

Черновики rates recruits / manpower caps / recruiter threshold — утвердить в дочернем spec 7b (не блочат п.0–1).

Статус roadmap: approved. Реализация — только через дочерние specs по пунктам 0→7.
