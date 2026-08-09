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
Иконки (в `SquadsIcons/Enemy/<faction>/`): REINFORCE, SUPPORT, RETRIBUTION, RECRUITER, MANPOWER, TAX, …

## Сделано

| ID | Суть |
|---|---|
| JAZZ-STRATEGY-002 | Role icons, task rollover, role EnemySquads, экономика v1 (abstract) |
| Icon bind fix | `SetImage` / pending image до `SquadSpawned` (не GetImage wrapper) |
| JAZZ-STRATEGY-003 | Start supply 50; POI/base → пул аванпоста; Major cap 5000; need-spawn; garrison не дублирует pre-placed оборону |
| JAZZ-STRATEGY-004 | Per-unit `$` prices (37 IDs) + accessors; spawn ещё на flat costs |
| JAZZ-STRATEGY-005 | Officer density (Sgt/8, Lt/15–20, Capt/30; MercCapt для T4); tiers дополняют |
| JAZZ-STRATEGY-006 | Money ledger `$` (schema v2); POI rates; flat costs in `$`; cargo `$` in task UI |
| JAZZ-STRATEGY-007 | Convoys valuables + boatless routes; patrol into player sectors; reinforce; retribution icon/targeting; recon intel text; role recipes data |
| JAZZ-STRATEGY-008 | Composition generator + per-unit `$` spawn costs for combat roles |
| JAZZ-STRATEGY-009 | Tax collector: city/farm `$` → poi_money → outpost via TAX role |
| JAZZ-STRATEGY-010 | Manpower schema v3; recruiter; manpower convoy; spawn manpower gate |
| JAZZ-STRATEGY-011 | Player recruit accrual + militia API (Operation hook morning Q) |
| JAZZ-STRATEGY-012 | Base refit / wounded retreat / idle top-up for regular combat roles |
| JAZZ-STRATEGY-013 | Persistent squads (no despawn); mission-budget rest 12–36h; patrol sector dwell; recon/QRF idle garrison assist |
| JAZZ-STRATEGY-015 | Medic density: Bonemaker reserved ~1 / 10–20 (min 1 at n≥10, `floor(n/15)`) in combat generator |
| JAZZ-STRATEGY-016 | Early→mature squad sizes (B+C); diamond/`$` income ×0.25 (÷4); slower cadence; **NoMaps smaller size table** |
| JAZZ-STRATEGY-017 | Tagged money cargo in inventory for tax/shipment/supply; survives loot regen; live resync |
| JAZZ-STRATEGY-020 | Maps: `PortCacaoEnvirons` / `P17` (approved; runtime playtest open) |
| JAZZ-STRATEGY-021 | `GreatDesert` / `E10` + late-awaken ≤T2-1 + Major neediest supply |
| JAZZ-STRATEGY-022 | `LaBarrier` / L15 + export patrol / garrison bonus / Major priority |
| JAZZ-STRATEGY-023 | `GreatForest` / G22+K21 + shared multi-outpost resources + orphan rehome |
| JAZZ-STRATEGY-024 | Legion `support` role (sniper/MG/mortar specialists, 4–7) |
| JAZZ-STRATEGY-025 | Local rest at city/bunker/outpost (nearest); outpost trip for top-up only when affordable |

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

### 0–5. Экономика $ + логистика + patrol/reinforce/retribution/intel → [JAZZ-STRATEGY-006](JAZZ-STRATEGY-006.md), [JAZZ-STRATEGY-007](JAZZ-STRATEGY-007.md)

Сделано в коде (runtime smoke — за владельцем):

- Schema v2 money ledger; POI $/h; cargo `$` в task UI.
- Enemy routes: `land_water_boatless`.
- Shipment inventory = сумма рейса (DB @$12000 + TinyDiamonds @$500).
- Supply и shipment могут идти навстречу в одном командном окне (оба гейта, без force-spawn).
- Patrol: player Side + приоритет пустых.
- Reinforce: роль, иконка, cap/cost, border trigger.
- Retribution: RETRIBUTION icon; report / max player noise.
- Recon return text называет spotted sector; QRF/retribution consume reports.
- `JAZZ_LegionRoleRecipes` allow-lists (data only).

### 6. Составы отрядов: цена юнита, пулы роли, политика генерации

Сейчас `LegionGlobalAI_*` — **фиксированные** EnemySquad presets (weighted lists + min/max). Цель — разнести это в data-driven генератор.

#### 6a. Цена каждого `JAZZ_Legion_*` UnitData → [JAZZ-STRATEGY-004](JAZZ-STRATEGY-004.md)
- У каждого легион-юнита своя **цена в $** (`jazz/Code/LegionUnitPrices.lua`; не путать с Cost лута).
- Цель: `money_cost` отряда при спавне = **сумма цен выбранных юнитов** (не плоский role cost из 003) — подключение к spawn ещё не сделано.
- Плоские role costs в п.0 — fallback; **полный дорогой garrison ≈ $120000 ≈ full outpost ≈ 10 shipments**.
- Утверждённая шкала и полная таблица 37 ID — в STRATEGY-004 (Line/Specialist/Leader × T1–T4; ×10 от раннего черновика).

#### 6b. Из каких юнитов может состоять роль → [JAZZ-STRATEGY-005](JAZZ-STRATEGY-005.md) + recipes в [007](JAZZ-STRATEGY-007.md)
Для каждой strategic-роли — **allow-list / slots** (`JAZZ_LegionRoleRecipes`, data only; generator ещё не подключён):

| Роль | Состав (контракт) | Размер (ориентир из 002) |
|---|---|---|
| recon | flanker/стрелки + офицеры по density | 8–12 |
| patrol | смешанное мобильное `JAZZ_Legion_*` | 12–18 |
| garrison | оборона + тяжёлая поддержка | 25–40 |
| qrf | тяжелее patrol (T2+), без «фармового» T1-спама | ~T2 band |
| reinforce | garrison-lite на границе | отдельный band |
| support | малая спецгруппа sniper/MG/mortar (T3–T4) к существующей обороне | **4–7** fixed ([STRATEGY-024](JAZZ-STRATEGY-024.md)) |
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

**Медики (утверждено, STRATEGY-015):** `JAZZ_Legion_FrontT1_Bonemaker` — при `n≥10` минимум 1, иначе/`далее` `floor(n/15)` (≈1 на 10–20). Reserved slots в combat generator; не random line-spam.

**Class-tier complementarity:** T1…T4 **дополняют** состав; старший tier сильнее, но не вытесняет младших. Poor = больше T1/T2; full/elite **добавляет** T3/T4.

#### 6c. Политика генерации → [JAZZ-STRATEGY-008](JAZZ-STRATEGY-008.md)

Реализовано: `JAZZ_GenerateLegionSquadComposition` + soft caps + poor/full auto; combat spawn списывает сумму цен. Manpower gate — с 010.

#### 6d. Порядок внутри пункта 6
1. Таблица цен `JAZZ_Legion_*` + документы.  
2. Role recipes (allow-list + min/max + веса).  
3. Generator policy poor/full + resource gates.  
4. Подключение к spawn в `Guardpost_Patrols` (после п.0 $; manpower — с 7b).

### 7. Двухресурсная экономика: $ + люди

Два независимых контура на одних POI:

| Контур | Копится где | Кто возит на I7 | Куда | Тратится на |
|---|---|---|---|---|
| Деньги ($) | city / farm → `poi_money` (пульс 72h); mine → diamond_stock | Tax collector / shipment | `outpost.money` | costs отрядов, (опц.) операции |
| Люди (manpower) | city / farm / guardpost / port → `poi_recruits` (не шахты) | Recruiter | `outpost.manpower` | размер составов |

Major держит свои пулы (`major.money`, `major.manpower`) с capacity ≫ аванпоста; подпитывает I7 конвоями, когда локально пусто.

#### 7a. Tax collector (сборщик налогов) — $ → [JAZZ-STRATEGY-009](JAZZ-STRATEGY-009.md)

Реализовано: economic POI → `poi_money` пульсом раз в 3 суток; tax circuit; cap 1; cargo max $12000; threshold 1000; cooldown 24h; TAX icon. Mine остаётся в shipment stock.

#### 7b. Людской ресурс — модель → [JAZZ-STRATEGY-010](JAZZ-STRATEGY-010.md)

Реализовано (locked defaults / playtest): farm +2 / city +3 recruits **per 72h pulse**; outpost 20/32; Major 80/600; recruiter threshold 8 / cap **1** / 24h; manpower convoy cargo 16, Major→outpost **только при manpower=0**; overflow → outbound to Major. Spawn combat списывает manpower.

#### 7c. Player militia ↔ recruits → [JAZZ-STRATEGY-011](JAZZ-STRATEGY-011.md)

Частично: player city/farm копят тот же `poi_recruits`; API get/consume; optional soft gate если найден `MilitiaTraining`/`TrainMilitia`. Полный Operation contract — [morning questions](JAZZ-GLOBAL-AI-MORNING-QUESTIONS.md).

### 8. Faction overlay → implemented [JAZZ-STRATEGY-014](JAZZ-STRATEGY-014.md)

JA3 не имеет матрицы фракций и faction-vs-faction войны. Контракт (owner 2026-08-02, **implemented** static; runtime AC open):

- Фракции: Legion / Adonis / Army / Rebels (+ player); **Smugglers** — минифракция (иконка есть, director later).
- Темы/цвета щитов: `SquadsIcons/Enemy/_shields/{legion,army,adonis,rebels,smugglers}.png` — таблица hex в STRATEGY-014.
- Rebels — союз игроку; **всегда** враг остальным AI-фракциям.
- Adonis ↔ Army — мир; оба **враг Легиону**.
- Adonis/Army → player: **нейтрал до World Flip**, враг после.
- Аванпост: **кто захватил — тот владеет**; Flip не возвращает форт Легиону автоматически.
- **Одна матрица sat+tactical:** hostile на стратегии ⇒ воюют на тактической карте / autoresolve; ally/neutral — нет (не «все красные = одна сторона»).
- Реализация = overlay + ownership + sat capture + tactical hostility wiring — с нуля, не «включить vanilla factions».

### 9. Pathing vs player territory → implemented [JAZZ-STRATEGY-018](JAZZ-STRATEGY-018.md)

Discord (Sergej) / owner 2026-08-02 (**implemented** static; runtime AC open):

- `recon` / scout / `patrol` — можно по player-controlled секторам.
- `retribution` — можно, **приоритет** на player territory.
- `shipment` / `supply` / `tax` / `manpower` / `recruiter` — обход; нет пути → **не спавнить**; существующие оставить; mid-route → **доехать**.
- `reinforce` — обход; нет пути → **спавнить, но не идти** (hold).

### 10. Gradual logistics + global spawn pool → implemented [JAZZ-STRATEGY-019](JAZZ-STRATEGY-019.md)

Owner 2026-08-02 (**implemented** static; runtime AC open):

- Tax/recruiter: новые аванпосты ждут **72h** перед первым выездом.
- Глобальный пул новых managed-спавнов / **24h**: tier I/II/III → **1/2/3**.
- Командное окно: tax → recruiter → combat → потом supply/shipment/manpower.

### 11. Maps Port Cacao region → approved [JAZZ-STRATEGY-020](JAZZ-STRATEGY-020.md)

Owner 2026-08-05: второй managed Region `PortCacaoEnvirons` (outpost `P17`, Major `B28`, сектора P8–P20 / O10–O20 / N11–N16).

### 12. GreatDesert + mainland late-awaken → approved [JAZZ-STRATEGY-021](JAZZ-STRATEGY-021.md)

Owner 2026-08-05: `GreatDesert` / `E10`; `LateAwakenMinTier=21` (÷10 economy, ×10 spawn gate, no QRF, recruiter after Major delivery); Major neediest-first supply.

### 13. GreatForest dual-outpost + shared resources → approved [JAZZ-STRATEGY-023](JAZZ-STRATEGY-023.md)

Owner 2026-08-05: `GreatForest` / G22+K21; shared `$`/manpower/diamond across ManagedOutposts; orphan rehome to sibling when one outpost falls.

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
- POI pulse **72h**: city/farm `$` 2500/800 на economic POI; tax threshold **$1000**, tax cap **1**, cargo max **$12000**;
- двухресурсная модель **$ + manpower**; recruiter с рупором; manpower-конвой Major→outpost **только при manpower=0**; overflow recruits → outbound to Major;
- spawn жрёт money+manpower; **per-unit $ prices**, role recipes, poor/full generator, **anti-skew balance** (не 12 MG; 4 MG без снайпера ок и наоборот);
- player militia из того же recruit-пула — фаза 7c после AI;
- rescale пулов/costs в $; convoys без force-spawn; patrol/reinforce/retribution/recon intel как в очереди.

Locked manpower rates: farm/city recruits **2/3 per 72h pulse**, caps 8/16; RecruiterCap **1**; outpost manpower capacity **32** (см. morning questions + 010).

Статус roadmap: approved. Реализация — только через дочерние specs по пунктам 0→7.
