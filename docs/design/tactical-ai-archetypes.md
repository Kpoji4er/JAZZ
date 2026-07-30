# Тактический AI: роли, политики, триггеры и развитие

Design-only. Код не меняет. Runtime-контракт: [`ai-awareness.md`](../technical/systems/ai-awareness.md). Таксономия Легиона: [`legion-units-equipment-tiers.md`](../technical/systems/legion-units-equipment-tiers.md). Human source таксономии: [JAZZ Units.drawio](https://app.diagrams.net/#G1ACFcxt5YuT-Ekw40XstiJiFLh3y6_Vah).

Статус: предложение + зафиксированные решения владельца (28 июля 2026). Реализация — только через approved change specs.

---

## 0. Зафиксированные решения владельца

| # | Решение |
| --- | --- |
| F1 | Вводим **`Legion_Flanker` / `Rebels_Flanker`** как public archetype ID. |
| F2 | **Разведчики (Flanker\*):** default = Flanker; в Press/push — ситуативно Assaulter. **Пушеры (Assault\*):** default = Assaulter; ситуативно Flanker, когда выгоден охват. |
| F3 | **Panic/Deserter:** лоутир Легиона (T1–T2) — основной контингент; хайтир (T3–T4 / elite) — только очень низкий шанс. |
| F4 | **Melee при ноже во 2-м слоте** — сохраняем намерение нынешних PickCustom: враг близко → сменить на Melee и резать. Вынести в shared helper, не копипастить. |
| F5 | Разные поведения **в городе / по условиям** — да; сначала каталог **триггеров**, потом веса. |
| F6 | Командирские ауры, «свита лидера», «прикрытие снайпера», anti-peek overwatch, дымы, правка policies/cover, аудит Medic freeze — в scope дизайна; нарезка specs ниже. |
| F7 | **Urban:** если получится — эвристика по **доле indoor slabs / помещений на карте** (не только `City=`). |
| F8 | **Aura radius:** Sergeant **15** тайлов; Lieutenant **25**; Captain / MercCaptain — **вся карта**. |
| F9 | **Melee engage:** не фиксированные 8/10 тайлов, а «хватит AP **добрести и ударить хотя бы раз**». |
| F10 | **Medic:** лечить **как можно раньше**; кровотечение — приоритетнее HP%. |
| F12 | **Night ≠ Fog:** ночью снайперы AI **держат позицию**, пока союзники не подсветят flare; Fog/Dust — без схемы «ждать свет». |

---

## 1. Текущее состояние (кратко)

### Три боевые роли vs preset ID

| Роль | UnitData | Базовый archetype сейчас |
| --- | --- | --- |
| Assaulter | `JAZZ_Legion_AssaultT*` | `Legion_Assaulter` |
| Frontliner | `JAZZ_Legion_FrontT*` | `Legion_Frontliner` |
| Flanker | `JAZZ_Legion_FlankerT*` | **`Legion_Flanker`** (ROLE-001) | `Flank`, `RunAndGun`, `CQB` |
| (спец) MG | `JAZZ_Legion_GunnerT*` | `Legion_Machinegunner` |

Rebels: `RebelFlanker` → **`Rebels_Flanker`**.

`*_Machinegunner` ≠ Flanker. Situational Press/Flank switch и чистка PickCustom — ROLE-002.

### PickCustomArchetype — зачем оно было

Реальные намерения (сохранить при рефакторе):

1. **Близкий враг + нож/melee во 2-м слоте** → ChangeWeapon + melee push (Roughneck и т.п.).
2. **Близкий враг у стрелка** → ситуативный Assaulter / sidearm (сейчас сломан тройным if).
3. **Раненый союзник у Bonemaker** → `Medic`.
4. **Panic** → `Deserter` (сейчас почти мёртв из‑за `local panicshance` shadowing).
5. **Stealth** у фланкеров → `Hide()` (side-effect не должен жить в PickCustom).

Проблема не в намерении «пойти резать», а в том, что логика размазана, бажная и смешивает stance / weapon / voice / hide.

### Drawio → поведения

Диаграмма задаёт **семьи + тиры + кит**, не runtime AI. Приближение по поведениям:

| Семья на диаграмме | Default role archetype | Ситуативные stance |
| --- | --- | --- |
| Assault / Stormer / demo | Assaulter | Flank (охват), Melee (нож во 2-м), Fallback (редко) |
| Front / Marksman / Soldier / Sniper | Frontliner | Assaulter только CQB+sidearm; Sniper Hold жёстче |
| Flanker / Recon / Scout | **Flanker** (новый) | Press → Assaulter |
| Gunner | Machinegunner | никогда Melee/Flank-default |
| Leader / Commander | Frontliner (+ aura) | Hold / Directive |
| Heavy / Arty | Artillery / Assaulter | без CQB-melee |
| Medic (Bonemaker) | Frontliner | Support → Medic |

Тир на диаграмме = stats/loot/perks, **не** отдельный archetype на каждый box.

---

## 2. Модель: Role + Stance + Shared scripts

### 2.1. Role archetypes

| ID | Default для |
| --- | --- |
| `Legion_Assaulter` / `Rebels_Assaulter` | Assault* |
| `Legion_Frontliner` / `Rebels_Frontliner` | Front*, leaders линии |
| **`Legion_Flanker` / `Rebels_Flanker`** | Flanker*, RebelFlanker |
| `*_Machinegunner`, `Artillery`, `Medic`, `Deserter`, `Melee` | specialists / states |

Из Assaulter/Frontliner **вынести** Flank-only PositioningAI с огромным Weight в Flanker preset.

### 2.2. Асимметрия Flank ↔ Press (решение F2)

```
Scout/Flanker unit:
  default → Legion_Flanker
  if NeedPush(context) → Legion_Assaulter   # мало AP у цели, численный перевес, узкий коридор

Assault/Pusher unit:
  default → Legion_Assaulter
  if NeedFlank(context) → Legion_Flanker    # фронт забит, есть flank threat path, ally уже Press
```

`NeedPush` / `NeedFlank` — детерминированные проверки на team context (не новый RNG каждый if). Voice Angry только при смене stance.

### 2.3. Melee / нож во 2-м слоте (F4 + F9)

Shared pre-think (вместо PickCustom):

```
if HasMeleeInSecondary(unit) and not NeverMelee(unit) then
  local reach = CanReachMeleeAndAttackOnce(unit, nearest_enemy)
  -- reach = существует dest в melee range с dest_ap >= cost(melee attack)
  if reach then
    EnsureActiveWeapon(Melee)
    return "Melee" / Assaulter+Melee behavior
  end
end
```

Не фикс «8 тайлов»: порог = **AP-reachability**. Не включать для Sniper/MG/Artillery без flag. Rebels: только при реальном melee secondary / CQB, не universal dist&lt;10.

### 2.4. Panic (F3 + F11)

| Тир | Panic |
| --- | --- |
| Legion T1–T2 | полная формула wounds/HP%/Will% |
| Legion T3 | сильно сниженный cap (например max 5–10%) |
| Legion T4 / elite / immortal | почти 0 (опц. hard off) |
| **Rebels** | **спокойнее** Legion low-tier (отдельный множитель &lt; 1) |

Починить shadowing `local panicshance`. Один helper на всех.

### 2.5. UnitData после рефактора

Хранит: `archetype`, `AIKeywords`, флаги (`AllowPanic`, `PanicTier`, `AllowMedicSwitch`, `MeleeSecondary`, `NeverMelee`, `RoleFamily=Scout|Pusher|Line|…`).  
**Не** хранит 60 строк inline Lua.

---

## 3. Триггеры контекста (город / условия)

Пока AI почти не различает «уличная перестрелка в городе» vs «джунгли» vs «ночь». Доступные **сигналы** (уже есть в JA3/JAZZ) и как их использовать:

### 3.1. Каталог триггеров

| Триггер | Источник | Что менять |
| --- | --- | --- |
| **Indoors** | `AICheckIndoors(dest)` / `AIPolicyIndoorsOutdoors` | CQB↑, grenade/smoke осторожнее, range-окна уже; Flanker меньше «длинного обхода» |
| **City / urban sector** | `gv_Sectors[id].City ~= "none"` (+ опц. map marker `UrbanFight`) | выше Cover weight, выше Overwatch/Control, ниже открытый Press; больше дыма на перебежки |
| **Night / Underground / Fog / Dust** | `GameState.*` (уже режет range в CombatAI) | Flare bias↑; Flanker stealth↑; Frontliner Hold; меньше длинных reposition |
| **RainHeavy** | `GameState.RainHeavy` | noise/awareness уже; AI: чуть выше TakeCover, ниже MobileShot |
| **Heat / raised alarm** | UnitAwareness JAZZ | после alarm — меньше Scout Hold Fire, больше Press |
| **Death zones** | `AIPolicyAvoidDeathZones` | уже есть; усилить в city doorways |
| **Last attack pos / peek pattern** | `enemy.last_attack_pos` + счётчик (новый) | anti-peek overwatch (§7) |
| **Officer alive in radius** | Leader keyword + Dist | aura directives (§6) |
| **Ally downed / HP&lt;X** | team scan | Medic Support |
| **Enemy surrounded / flank delta** | `AIPolicyFlanking` / `GetFlankThreat` | NeedFlank для пушеров |

### 3.2. Как подключать (без спама archetype)

Не плодить `Legion_Assaulter_City`. Один role archetype + **context multipliers** на Weight policies / signature BiasId:

```
context_profile = ResolveProfile(unit)  -- Urban / Jungle / Indoor / Night
ApplyProfileToStanceWeights(profile)
```

Map marker / EnemySquad doctrine (опц.) перекрывает sector default.

### 3.3. Что считать «городом» в тактике (F7)

Не каждый sector с `City=` (wilderness tiles тоже бывают помечены). Для tactical AI:

1. **Предпочтительно:** посчитать **долю indoor slabs / помещений на карте** (`AICheckIndoors` / pass slabs с indoor flag) при загрузке боя → `UrbanCombat` если доля выше порога (порог утвердить в CTX-001, ориентир ~25–40%).
2. Опционально усилить marker’ом / GuardArea.
3. Sector `City=` — только слабый hint, не единственный сигнал.
4. Не смешивать с satellite tax/recruit economic POI.

### 3.4. Плохая видимость (отдельный профиль)

См. §15. Триггеры: `GameState.Night`, `Fog`, `DustStorm`, `FireStorm`, `Underground`, плюс rain/smoke через `GetSightRadius` ([visibility-weather-appearance.md](../technical/systems/visibility-weather-appearance.md)).

---

## 4. AIPolicy: что не так и как улучшить

Активные замены JAZZ: `AIPolicy.lua` + куски в `AiActions.lua`. Ядро scoring — `AIScoreDest` (vanilla × Weight).

### 4.1. `AIPolicyTakeCover` — почему «плохо выбирает укрытия»

Текущая логика: для каждого **видимого** врага берёт `GetCoverFrom` + `GetCoverPercentage`; если coverage &lt; 30 → `base * 0.1`; иначе `base + bonus`; **усредняет** по врагам.

Слабые места:

1. **Низкий Weight в archetype** (часто 10–30) против `DealDamage` 300 → cover почти не влияет на выбор dest.
2. **Average по всем врагам** размывает «укрытие от того, кто реально стреляет»; юнит встаёт «средне плохо» ото всех.
3. Не учитывает **shoot-from-cover**: позиция с идеальным cover, но без LOS/атаки на приоритетную цель, должна проигрывать «чуть хуже cover + shot».
4. Не штрафует **уже раскрытые** peek-позиции (`last_attack_pos` игрока / свой предыдущий shot voxel).
5. `visibility_mode = "team"` vs `"self"` используется непоследовательно между behaviors.
6. После атаки bunker/disengage есть, но **Think** всё ещё может выбрать открытый OptLoc из‑за damage weight.

Предлагаемые улучшения (отдельный policy-spec):

| Изменение | Суть |
| --- | --- |
| **Threat-weighted cover** | вес врага ∝ threat (LOS, aim, last damage dealer, distance) |
| **Cover×Shot composite** | `score = cover_term * (0.5 + 0.5 * can_attack_best)` или два policy Required |
| **Hard floor** | Frontliner/Sniper: dest без cover vs visible shooter → сильный penalty / Required soft |
| **Weight rebalance** | Frontliner EndTurn/OptLoc: TakeCover 80–150; Assaulter 20–40; Flanker cover низкий, flank высокий |
| **Stance-aware** | уже есть stance в dest; явно бустить Crouch+Low / Prone+open отдельно (частично есть в bunker) |

### 4.2. `AIPolicyFlanking`

Считает Δ flank threat с учётом planned ally positions; кэш. Ок как ядро. Улучшения:

- для **Flanker archetype** — основной OptLoc (Weight 200–1000);
- для **Pusher situational Flank** — тот же policy, но с `ReserveAttackAP`;
- не держать Flank Weight 1000 внутри Assaulter default — иначе все с keyword Flank ведут себя одинаково.

### 4.3. `AIPolicyProximity` — критично для «свиты» и кластеров

Сейчас возвращает **дистанцию** (больше = выше score) при комментарии «меньше = лучше». С положительным Weight это **поощряет отдаление** от союзников, если MinScore пройден. Для retinue / CloseToTeammates это опасно и/или работает «случайно» через другие constraints.

Предложение:

- явное `ScoreMode = "closer_better" | "farther_better"`;
- closer_better → utility `K / (1 + dist)` или `max(0, MaxDist - dist)`;
- **Leader retinue:** allies с keyword Soldier/CQB → closer_better к Leader;
- **Sniper spacing:** farther_better от своего кластера штурма, но closer_better к 1–2 «щитам».

### 4.4. Прочие policies

| Policy | Оценка | Улучшение |
| --- | --- | --- |
| `AIPolicyAttackAP` | ок (reserve AP на атаку) | Frontliner: выше weight; после peek — ещё выше |
| `AIPolicyHighGround` | есть + anti-stack | Sniper Required soft; не для CQB Assaulter |
| `AIPolicyIndoorsOutdoors` | 100/0 | City profile: Indoors weight↑ |
| `AIPolicyAvoidDeathZones` | ок | doorway/city: radius↑ |
| `AIPolicyDealDamage` | доминирует | не убирать, но балансировать с cover |
| `AIPolicyWeaponRange` | ок по keywords | Flanker/Assaulter/Front окна развести жёстче |
| `AIPolicyHealingRange` | Medic only | см. §8 freeze |
| `AITargetingEnemyWill` | есть | Assaulter Press на низкий Will |
| **Новый: `AIPolicyAllyRoleAnchor`** | — | dest score относительно юнита с role=Sniper/Leader (прикрытие / свита) |
| **Новый: `AIPolicyAvoidPeekVoxel`** | — | штраф за voxel = свой/вражеский last_attack_pos |

---

## 5. Позиции уровня «у снайпера прикрытие, у лидера свита»

Это не отдельный pathfinding за весь отряд, а **якоря в OptLoc**:

### 5.1. Sniper cover screen

1. Юнит с `Sniper`/`Marksman` выбирает high ground + cover + range (уже частично в Frontliner).
2. 1–2 ближайших Soldier/Assaulter получают OptLoc bias: **между снайпером и ближайшим вражеским кластером** (проксимити к линии снайпер→враг) + свой cover.
3. Реализация: team context `anchors.sniper = unit`; policy `AllyRoleAnchor{ Role="Sniper", Mode="screen" }`.

### 5.2. Leader retinue

1. Leader пишет `anchors.leader = unit`.
2. Allies с флагом retinue / keyword Soldier в радиусе R: Proximity closer_better к leader + TakeCover.
3. Leader сам: не на острие — выше cover, ниже DealDamage weight, чем у Assaulter.
4. Aura (§6) усиливает Hold у свиты, пока лидер жив.

Порядок хода: Early/Normal уже есть; якоря читать из **уже сходивших** `ai_destination` + текущих позиций (как Flanking AllyPlannedPosition).

---

## 6. Командирские тактики (aura)

Leader (`JAZZ_Legion_Leader*`, RebelSergeant, keyword `Leader`) раз в ход (или при StartAI первого офицера) пишет в **map/team ephemeral context** (не GameVar, если не нужен save — уточнить в spec).

**Радиус ауры (F8):**

| Офицер | Radius |
| --- | --- |
| Sergeant (`LeaderT1`) | **15** тайлов |
| Lieutenant (`LeaderT2`) | **25** тайлов |
| Captain / MercCaptain (`LeaderT3`/`T4`) | **вся карта** (все allies команды) |

| Directive | Условие | Эффект в радиусе |
| --- | --- | --- |
| `HoldLine` | город / хорошие cover / численный паритет | Frontliner cover↑, Overwatch bias↑, Assaulter Press↓ |
| `Push` | перевес / низкий Will врагов / после smoke | Assaulter NeedPush, Flanker может Press |
| `Envelop` | фланг доступен | Pushers NeedFlank↑, Scouts остаются Flanker |
| `FallBack` | потери / death zones | smoke bias↑, Deserter только low-tier |
| `FocusFire` | одна цель низкий HP | targeting bias на session_id |
| `LowVisHold` | Night/Fog/Dust (§15) | flare↑, OW↑, Press↓, Flanker stealth |

Офицер **не** pathfind’ит за всех: только множители Weight / stance hints. Без офицера — локальные default stance. При нескольких офицерах — более высокий ранг / больший радиус побеждает (Captain перекрывает Sgt).

Leaders сейчас имеют **пустой** PickCustom — как раз место для aura writer, а не для copy-paste panic.

---

## 7. Anti-peek: овервотч против «выйти–выстрелить–спрятаться»

Сигнал уже почти есть: `enemy.last_attack_pos`, scout на last location, ThrowFlare/grenade `TargetLastAttackPos`.

Предложение:

1. **Счётчик peek** на врага (ephemeral в combat): если юнит игрока атаковал и в том же/следующем вражеском ходе снова в cover вне LOS — `peek_streak++`.
2. При `peek_streak >= 2` у видимой команды AI:
   - Frontliner/`Control`/`Soldier`: Weight Overwatch↑, aim на `last_attack_pos` / коридор выхода;
   - MG: setup cone на этот voxel;
   - Flanker: обход, не лобовой trade.
3. Signature `AIConeAttack` Overwatch уже в archetype — поднять min_score/bias динамически через BiasId `AntiPeekOW`.
4. Fallback overwatch (`AIPlaceFallbackOverwatch`) — только если нет sight; anti-peek наоборот когда sight **пропал** после выстрела с известной позиции.

Не нужен полный player-intent ML: достаточно «стрелял отсюда и скрылся».

---

## 8. Дымы (Smoke policy)

**Доктрина (JAZZ-AI-ACT-002, owner 2026-07-30):**

| Ситуация | Куда кидать | Условие |
| --- | --- | --- |
| Выход под OW | **занавес** на угол / отрезок `OW origin → ally exit` | союзник с planned `ai_destination` или fire lane |
| Самоприкрытие | прямо на / у своих | только если союзник **уже сходил** (`JazzAI_TeamActed`) |
| Не кидать | шапка на ещё не ходивших; толпа врагов под свой огонь; пустота без LOS/OW | |

Механика: выстрелы сквозь дым → незначительные попадания; sight на линии `IsLineInSmoke` **−70**. Дым = curtain, не «шапка на головы» до хода союзника.

Preset signature `BiasId = "SmokeGrenade"` (Assaulter/Frontliner/Flanker/MG): `AllowedAoeTypes = { smoke }`, bias disable после броска. Runtime scoring в `JazzAI_ScoreSmokeZone` / `JazzAI_CollectSmokeCurtainTargets` **перекрывает** preset `enemy −100 / team +100 / self +1000`.

Team context: acted после `AIPlayAttacks`; exit из `ai_destination`; угроза из `g_Overwatch` (+ soft `last_attack_pos`).

Keyword `Smoke` желателен на доверенных носителях (Bonemaker); у штурма entry без keyword gate.

---

## 9. AI Actions — обзор и доработки

| Action (JAZZ/vanilla в archetype) | Сейчас | Предложение |
| --- | --- | --- |
| `AIActionBasicAttack` | patched Precalc | ок |
| `AIActionThrowGrenade` | multi-slot, smoke/fire grid | раздельный smoke score; bias disable после броска |
| `AIActionThrowFlare` | night/underground | связка flare→Press на last pos |
| `AIActionCharge` / MobileShot / RunAndGun | по keywords | Assaulter/Flanker; не Front sniper |
| `AIConeAttack` Overwatch | Control/Soldier | anti-peek bias (§7) |
| `AIActionMGSetup` / burst | Machinegunner | не Melee-switch; cone на peek voxel |
| `AIActionHeavyWeaponAttack` | Ordnance | без CQB melee |
| `AIActionBandage` / Stim | Medic | §10 |
| `AIActionShootLandmine` | есть | city doorways↑ |
| `AIActionCancelShot` | Control | оставить |
| Disengage/Bunker (`AIPlayAttacks`) | Commit→Dump→Bunker | усилить связь с TakeCover policy в Think |

Новые не плодить без нужды; сначала scoring/biases существующих.

---

## 10. Medic (F10) + freeze

**Дизайн (F10):** лечить **как можно раньше**; **Bleeding** важнее процента HP. Не поднимать порог «чтобы реже лечил» — наоборот ранний Support. Freeze чинить fail-safe’ами, не отказом от раннего heal.

Bonemaker сейчас: любой союзник &lt;70% HP → `Medic`. У `Medic`: Healer Late + Priority Bandage + `BleedingWeight` 300 в OptLoc HealingRange.

Статические риски фриза:

1. Bandage unreachable → wait `IsIdleCommand` / `WaitMsg("Idle")`.
2. restart + Priority Bandage без прогресса; wait `IsGettingDowned`.
3. Два Bandage signature (behavior + archetype).
4. OptLocSearchRadius 80 + постоянный Medic stance.
5. `InfiniteLoopFix` маскирует долгий ход.

План MED-001: repro + fail-safe «Bandage fail → revert Frontliner этот ход»; один Bandage entry; timeout Idle; приоритет цели: Bleeding → downed → lowest HP%; Early/Normal phase для bleed, не только Late.

---

## 11. План specs (обновлённый)

| Spec | Суть |
| --- | --- |
| **JAZZ-AI-ROLE-001** | `Legion_Flanker` / `Rebels_Flanker` presets; вынос flank behaviors; таблица role→UnitData |
| **JAZZ-AI-ROLE-002** | Shared stance + melee-secondary + panic tiers (F2–F4); миграция Legion PickCustom |
| **JAZZ-AI-POL-001** | TakeCover threat-weight + cover×shot; Proximity closer/farther modes; Weight rebalance трёх ролей |
| **JAZZ-AI-POL-002** | AllyRoleAnchor (sniper screen / leader retinue); AvoidPeekVoxel |
| **JAZZ-AI-CTX-001** | Urban (indoor ratio) + **LowVis** (Night/Fog/Dust/Fire/Underground/Rain) profiles; множители Weight; flare/OW gates |
| **JAZZ-AI-CMD-001** | Officer aura (15/25/map) + directives вкл. `LowVisHold` |
| **JAZZ-AI-ACT-001** | Smoke LOS-break score; anti-peek overwatch; flare→push; LowVis min_score OW |
| **JAZZ-AI-MED-001** | Medic freeze repro + fail-safes; early heal; bleed-first |
| **JAZZ-AI-ROLE-003** | Rebels на ту же схему |
| **JAZZ-AI-REG-001** | Isolated Legion → `Legion_Regroup` к дальнему ally cluster |
| **JAZZ-AI-POL-003** | Anti-stack: hard same-voxel dibs + soft ally spacing in AIScoreDest |

Рекомендуемый порядок: **001 → POL-001 → 002 → MED-001** (быстрый playfeel + не убить бой медиком), затем CTX/CMD/ACT.

---

## 12. Критерии playfeel

1. Scout обходит; в Push — давит; pusher в основном давит, иногда заходит с фланга.
2. Юнит с ножом во 2-м слоте при враге в упор **реально** идёт в melee (если оружие есть).
3. Low-tier Legion дезертирует заметно; T4 — почти никогда.
4. В городе чаще cover/OW/smoke; ночью — flare и осторожный flank.
5. Снайпер не один в чистом поле без «экрана»; лидер не на острие без свиты.
6. После 2+ peek игрока — OW/MG cone на выход.
7. Дым бьёт LOS перебежки, а не «рандом в толпу».
8. Медик не вешает ход; лечит рано, bleed первым.
9. **Night:** снайперы AI держат позицию, пока свои жгут светилки, потом стрельба/Press. **Fog/Dust:** без flare-схемы — cover/indoors/smoke/OW на last known.
10. Replay/seed стабилен.
11. Одиночный/пара Legion далеко от толпы (≥3 своих ≥18 тайлов) бежит к кластеру (`Legion_Regroup`), не на exit.
12. AI не толкутся в одну клетку / shoulder-to-shoulder на одном cover (POL-003).

---

## 13. Связь docs

- После ROLE-001/002: обновить faction templates в `ai-awareness.md` (добавить Flanker; MG ≠ Flank).
- После смены archetype у Flanker*: колонка в `legion-units-equipment-tiers.md`.
- Visibility/sight const: [`visibility-weather-appearance.md`](../technical/systems/visibility-weather-appearance.md).
- STRATEGY-* не смешивать; составы отрядов должны содержать все три роли, иначе doctrine/aura не читаются.
- Drawio остаётся human taxonomy; эта статья — tactical behavior bridge.

---

## 14. Решения F7–F11 (закрыто)

| # | Ответ |
| --- | --- |
| Urban | Доля indoor/помещений на карте, если получится посчитать |
| Aura | Sgt 15 / Lt 25 / Capt+ вся карта |
| Melee | AP: добежать и ударить ≥1 раз |
| Medic | Как можно раньше; bleed приоритет |
| Rebels panic | Спокойнее Legion low-tier |

Открытых вопросов по этим пунктам нет.

---

## 15. Политики в плохой видимости (Night / Fog / Dust / Fire / Underground)

Отдельный context profile `LowVis` (и подтипы). Не новые archetype ID.

### 15.1. Что уже делает runtime

| Механика | Где | Эффект |
| --- | --- | --- |
| Sight mods | `GetSightRadius` / EnvEffects | Night ≈ −65, Fog −30, Dust −40, smoke линии −70, rain −5/−15 ([visibility doc](../technical/systems/visibility-weather-appearance.md)) |
| `EffectiveRange` clamp | `CombatAI` `AICreateContext` | при Dust/Fire/Underground/Night/Fog firearm range = `Min(sight_tiles, EffectiveRange)` |
| Dest LOS cache | `AIUpdateDestLosCache` | LOS на `unit:GetSightRadius()` — в low-vis меньше видимых dest↔enemy |
| `AIActionThrowFlare` | `AiAction_ThrowFlare.lua` | доступен только `Night` или `Underground`; цели: last_attack_pos, noise; score по юнитам в Darkness |
| Exploration suspicion | UnitAwareness | Darkness/projector уже влияют |

Итог: AI **уже стреляет ближе**, но **архетипы не меняют доктрину** (всё ещё могут Press в открытое, слабо бустят flare/OW).

### 15.2. Night ≠ Fog (зафиксировано владельцем)

Ночной бой **не** копирует туман: ночью есть illumination (flare), и роль линии/снайпера другая.

| | **Night** (и Underground с flare) | **Fog** (и Dust без illumination) |
| --- | --- | --- |
| Освещение | Свои кидают **светилки**; после подсвета — Press/стрельба по illuminated | Flare **не** доступен (`AIActionThrowFlare` только Night/Underground) |
| **Снайпер / Marksman AI** | Может **сидеть на позиции** (Hold + high ground/cover + OW), пока остальные не подсветят; не лезть в Press «в темноту» | Нет схемы «ждём подсвет»; короче range, cover/OW на last known, без дальнего снайперского окна |
| Assaulter / Flanker | Flare carriers / CQB push после light; Flanker stealth до контакта | Smoke-перебежки, короткий advance, не ExtremeRange |
| Лидер | `LowVisHold` + приоритет flare у носителей | `LowVisHold` без flare-gate |

Итог: Night = **Illuminate → затем действуй**; Fog/Dust = **сжимай дистанцию / укрывайся**, без ожидания света.

### 15.3. Целевая доктрина по условиям

| Условие | Stance bias | Policies | Actions |
| --- | --- | --- | --- |
| **Night** | Sniper/Marksman **Hold на позиции**; остальные LowVisHold/flare; Press↓ до illumination | TakeCover↑ у линии; WeaponRange уважает sight; Sniper RangeMin не требовать выше sight | **Flare** Weight↑ (не-снайперы) + last_attack/noise; после flare Bias → Press 1 ход; Sniper OW на last known / illuminated; MobileShot↓ |
| **Fog** | Hold у всех; **нет** «снайпер ждёт свет» | Cover↑; Flanking осторожнее | Smoke перебежки↑; OW на last_attack; не гнаться за ExtremeRange; **без flare** |
| **DustStorm** | Hold; меньше reposition | Cover↑; Indoors↑ | Indoors OptLoc; flare нет; CQB к зданиям |
| **FireStorm** | Avoid fire voxels уже в `AIScoreDest`; Hold | AvoidDeathZones/fire weight↑ | Не Press через горящие зоны |
| **Underground** | как Night + Indoors (flare есть) | Indoors↑; range коротко | Flare↑; снайпер может Hold до light; CQB↑ |
| **RainHeavy** | лёгкий Hold | TakeCover чуть↑ | MobileShot↓; jam уже в weapon env |
| **Smoke на линии** | локально | dest в своём дыму ок для Fallback; не стоять в токсике | Smoke scoring LOS-break (§8) |

### 15.4. Конкретные правки policies под LowVis

| Policy | LowVis изменение |
| --- | --- |
| `AIPolicyTakeCover` | множитель Weight ×1.5–2 для Frontliner/Leader; threat-weight важнее (мало видимых = каждый видимый критичен) |
| `AIPolicyWeaponRange` | не расширять окна вручную — уважать уже сжатый `EffectiveRange`; для Sniper в Night не требовать RangeMin 50, если sight ~16 |
| `AIPolicyLosToEnemy` | Required soft осторожнее: в Fog часто нет LOS → иначе все dest fail; использовать last known / noise pos |
| `AIPolicyFlanking` | снизить Weight у не-Flanker; у Flanker оставить, но ReserveAttackAP |
| `AIPolicyProximity` | closer_better к своему кластеру (не разбегаться в тумане) |
| `AIPolicyHighGround` | **Night sniper:** оставить/усилить (сидеть на позиции). Fog: слабее. Dust: indoors важнее height |
| `AIPolicyIndoorsOutdoors` | Dust/Fire/Rain: Indoors score↑ |
| `AIPolicyAttackAP` | выше — не тратить всё на бег к невидимой цели |
| **Новый hint** `AIPolicyLastEnemyPos` | уже есть у Medic SeekEnemy — включить в LowVis Front/Flank EndTurn |

### 15.5. Actions под LowVis

| Action | Поведение |
| --- | --- |
| `AIActionThrowFlare` | **Night/Underground only**; Weight↑ у не-снайперов (Assaulter/Flanker/Soldier); после flare Bias → Assaulter Press на illuminated voxel (1 ход). Снайпер flare не обязан кидать |
| `AIConeAttack` Overwatch | Night: снайпер на позиции — OW на last known / corridor; LowVis+peek: min_score снизить если мало видимых |
| `AIActionThrowGrenade` smoke | Fog/Dust перебежки; ночью не заменяет flare |
| `AIActionMobileShot` / RunAndGun | Weight↓ в low-vis |
| Basic attack | Night sniper: стрелять после illumination / при контакте; не dump в темноту |
| MGSetup | cone на last known / corridor |

### 15.6. Роли в LowVis

| Роль | Night | Fog / Dust |
| --- | --- | --- |
| Frontliner Sniper/Marksman | **Hold на позиции**, ждать подсвет союзников; OW | Cover + короткий range; без «ждать свет» |
| Frontliner Soldier | Flare если есть; cover; OW | Cover; smoke-assist |
| Assaulter | Flare/CQB; Press после light | Короткий push / buildings (Dust) |
| Flanker | Stealth до контакта; не ломать снайперский Hold | Обход короткий; smoke |
| MG | Setup на коридор last known | То же |
| Leader | `LowVisHold` + flare priority у носителей | `LowVisHold` без flare |
| Medic | heal как обычно; путь осторожнее | то же |

### 15.7. Spec

Вынести в **JAZZ-AI-CTX-001** / **CTX-LOWVIS**: отдельно ветки Night (Illuminate→Act, sniper Hold) и Fog/Dust (no flare). Runtime: Night Ernie + Fog отдельно.

---

## 16. Конвейер выбора позиции (как работает сейчас)

Статический разбор `jazz/Code/CombatAI.lua` + policies. Нужен для POL-001.

```
StartAI → archetype (+ PickCustom)
  → AICreateContext (EffectiveRange, enemies, sight…)
  → Behavior.Think:
       AIFindDestinations          # reachable + AP reserve + soft disengage
       AIEnumValidDests            # OptLoc radius (часто 80) + collapse
       AIFindOptimalLocation       # OptLocPolicies → best_dest
       AIScoreReachableVoxels      # EndTurnPolicies → ai_destination
       AIChooseMovementAction / signature
  → Play → AIPlayAttacks (dump → disengage/bunker → optional fallback OW)
```

| Шаг | Функция | Что решает |
| --- | --- | --- |
| Reachable set | `AIFindDestinations` | пути с урезанным AP (reserve атака + 2 AP soft-disengage); если команда **не видит** врагов — фильтр «только cover / crouch-prone» |
| Auto-crouch | тот же | low cover → dest в Crouch с вычетом stance AP |
| OptLoc pool | `AIEnumValidDests` | все pass slabs в `OptLocSearchRadius` (не только reachable!) |
| OptLoc score | `AIFindOptimalLocation` + `AIScoreDest` | сумма `EvalDest * Weight/100`; `Required` и ≤0 → dest score 0; fire/gas/bombard/bias markers |
| Threshold | `const.AIDecisionThreshold = 80` | в shortlist dest ≥ 80% от best; если старт в shortlist — остаются; иначе path к collapsed set |
| End-turn dest | `AIScoreReachableVoxels` | только **reachable**; EndTurnPolicies + OptLocWeight тяга к best_dest |
| Post-attack | bunker/disengage | TakeCover action / crouch / prone — **не** пересчёт OptLoc |

Почему cover «не чувствуется»: OptLoc/EndTurn часто `DealDamage` ≫ `TakeCover`; OptLoc смотрит на 80 тайлов включая **недостижимые** идеальные укрытия; EndTurn уже не может туда дойти и выбирает «лучший reachable damage».

---

## 17. Каталог AIPolicy / AIAction (Legion & Rebels templates)

Фактически в faction archetypes сейчас:

**Policies:** TakeCover, DealDamage, Flanking, WeaponRange, LosToEnemy, Proximity, IndoorsOutdoors, AvoidDeathZones, HighGround (+ AttackAP/HealingRange/LastEnemyPos у Medic; EnemyWill у MG).

**Actions:** BasicAttack, ThrowGrenade (вкл. Smoke entry), ThrowFlare×2, ConeAttack Overwatch, Charge, MobileShot/RunAndGun, ShootLandmine, CancelShot, HeavyWeapon (Front), MGSetup/MGBurst (MG), Bandage/Stim (Medic).

### 17.1. Policies — audit notes

| Policy | JAZZ override? | Планируем юзать | Заметка |
| --- | --- | --- | --- |
| TakeCover | да | **да, ядро** | §4.1 + LowVis ×Weight |
| DealDamage | vanilla | да | балансировать, не выкидывать |
| Flanking | да | **да** Flanker/NeedFlank | вынести из Assaulter default |
| WeaponRange | vanilla | да | LowVis: не требовать min выше sight |
| LosToEnemy | vanilla | да | soft в LowVis |
| Proximity | да | **да** свита/кластер | closer/farther mode |
| IndoorsOutdoors | да (raw 100) | да Urban/Dust | |
| AvoidDeathZones | да (new) | да | |
| HighGround | да | Sniper | слабее в Fog/Night |
| AttackAP | да | Front/Hold | |
| HealingRange | vanilla? | Medic | bleed weight |
| LastEnemyPos | vanilla | LowVis / Seek | |
| EnemyWill targeting | да | Assaulter/MG | |

### 17.2. Actions — audit notes

| Action | JAZZ | Заметка |
| --- | --- | --- |
| BasicAttack | Precalc patch | |
| ThrowGrenade | multi-slot + smoke grid | Smoke entry уже с self-favor score; нужен LOS-break score |
| ThrowFlare | отдельный файл | только Night/Underground; дубли в archetype |
| ConeAttack→Overwatch | cone zones + CTH filter | min_score **300** — высокий барьер; Assaulter Weight 50 + keyword Soldier/Control; Front Weight 20 + Control/Soldier disable |
| RunAndGun / MobileShot | Bias disable | LowVis↓; Assaulter/Flanker |
| Charge | Melee keyword | связка F9 |
| MGSetup | ACT-003 halfcover | crouch+bipod behind CoverLow; else Prone; dest +45 |
| Bandage | Priority | MED-001 |
| Fallback OW | `AIPlaceFallbackOverwatch` | только no-sight после bunker fail |

### 17.3. Overwatch — как устроен и куда крутить

1. **Signature:** `AIConeAttack` с `action_id = "Overwatch"` → `AIPrecalcConeTargetZones` строит зоны по target points (враги, last_attack_pos, midpoints) → EvalZones (enemy/team scores) → нужен score ≥ min_score (300).
2. **Keywords:** часто `Soldier` или `Control` — без них entry не матчится.
3. **Team Bias:** OverwatchAssault −50 ApplyTo Team / disable Period 2 — команда не спамит OW каждый ход.
4. **После хода:** если `FallbackAction = overwatch` и нет sight после bunker — `AIPlaceFallbackOverwatch`.
5. **Runtime interrupt:** `ProvokeOpportunityAttack_Overwatch` в Unit — отдельный слой от AI Think.
6. **OpeningAttackType = Overwatch`** на многих UnitData — opening, не Think signature.

**Проблемы для anti-peek / LowVis:**

- min_score 300 при малом числе видимых врагов → OW редко выбирается именно когда нужен;
- цели зон слабо приоритизируют `last_attack_pos` игрока-пикера;
- Assaulter и Front делят BiasId по-разному; нет `AntiPeekOW` bias;
- fallback OW срабатывает при **отсутствии** sight, anti-peek нужен когда sight **пропал после выстрела** с известной клетки.

**План ACT-001:** динамический min_score в LowVis/peek; target_pts вес на last_attack_pos; BiasId AntiPeek; не ломать team anti-spam полностью.

---

## 18. Параллельный audit track

Пока идут ROLE-001 / POL-001, вести чеклист (design → evidence):

- [x] TakeCover: threat-weight + cover×shot в `AIPolicy.lua` (POL-001); Weights Front 80–120 / Assault ~40 / Flank OptLoc 15
- [x] Proximity: `ScoreMode` closer_better / farther_better; шесть faction templates → closer_better
- [x] ROLE-002/003: `AICombatStance.lua` + thin PickCustom Legion/Rebel
- [x] Smoke LOS-break / OW LowVis / flare→Push (ACT-001)
- [x] LowVis + Urban profiles (CTX-001)
- [x] Medic Bandage fail-safe + early bleed (MED-001)
- [x] Officer aura / AllyRoleAnchor / AvoidPeek (CMD-001 / POL-002)
- [x] Isolated Legion Regroup (REG-001)
- [x] Ally anti-stack spacing (POL-003)

Fog/Dust **без** flare — осознанный gap: либо принять «только Night/Underground illumination», либо отдельный design на сигнальные/шумные маркеры.
