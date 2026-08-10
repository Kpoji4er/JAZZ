# Ernie garrison baseline (pre-rework)

Snapshot before full Ernie / Legion squad rework. **Do not treat as target design.**

## Locked targets (owner 2026-08-10)

### Pack taxonomy (size × class band × Extra)

Обычные отряды — не «один N на остров», а **каталог паков**:

**1. Size tier × difficulty (Normal = authored base)**

| Size | Easy | Normal | Hard | Role |
| --- | ---: | ---: | ---: | --- |
| **Small** | **5** | **10** | **15** | пост / sentry / spice / thin road |
| **Medium** | **20** | **25** | **40** | обычный гарнизон / forest / coastal / road Init |
| **Large** | **30** | **40** | **70** | людный узел (не hub-исключения) |

**Easy/Hard = сразу в authored packs (owner 2026-08-10):** цели headcount по таблице выше — **в scope UNITS-007**, не follow-up.  
В пресете `EnemySquads` нет отдельных полей EasyAmount/HardAmount: слот считает `UnitCountMin`/`UnitCountMax` через `InteractionRandRange` (это **variance**, не game difficulty). Чтобы Easy/Normal/Hard давали **разные** суммы, на телесных ролях — **difficulty-gated слоты** (`conditions` / `Difficulty Easy|Normal|Hard` на `weightedList`, пустой list → слот пропускается) с count = E/N/H цели роли; якоря по-прежнему Min=Max и обычно на всех сложностях. Альтернатива — тонкий JAZZ-wrap `GenerateRandEnemySquadUnits` (только если gated slots окажутся слишком шумными).  
**Slot count variance (owner):** внутри одной сложности на телесных слотах допустим рандом **±10…20%** вокруг цели роли этой сложности. Якоря (officer/medic/mortar/RPG/named/≤1 GL) — **фиксированные** Min=Max.  
**Исключения (уже locked, не эта шкала):** I5 XL **60**, J5 **40**, villa Sentry+Attackers 22–26, quest packs.  
Quest / story между тирами ок (CounterAttack 30, Wave2 ~25), если роль ясна.

Старый глобальный «Easy = base−10 / Hard = base+10» для Init Эрни **superseded** этой таблицей (для Small/Medium/Large). Medic Easy+/Hard− (STRATEGY-015) — отдельно, не путать с body count.

**2. Class band (UnitData T1–T4 experience — не gear `JAZZ_Legion_Tier`)**

Каждый пак явно в одной полосе; пулы слотов не вылезают за неё (якоря story/T4 — только если band это допускает).

| Band | Mix | Feel |
| --- | --- | --- |
| **A** | predominantly **T1–T2** | мясо / рекруты / ранний остров |
| **B** | **T1–T2–T3** | обычный гарнизон с щепоткой ветеранов |
| **C** | **T2–T3** | кадровые, без зелени |
| **D** | **T2–T3–T4** | жёсткий узел / элита лагеря |
| **E** | **T3–T4** | редкий elite / story spend |

Island budget: большинство Init — **A/B**; C–E точечно. **T4** не размазывать: 1–2 на весь остров вне story, плюс явные story packs (I7 Pierre Headsman suite, L5 Headsman, …).

**Role gradient (owner):** Init в сумме покрывают **все T1–T2 роли**. Дальше от I7 → T1-lean; ближе к форту/аванпосту → T2-lean. Редкие T3 — только сложные сектора (I2/L1/L6_UG/I7). `FlankerT3_Recon` (не T1) — якорь flank на FortressDefenders.

**3. Усиления (Extra)**

Отдельные добор-паки **5–10** чел. Init = **`база` + 0…1 Extra**.

**Специализированные Extra** (узкий фокус):

| Id (план) | Specialty |
| --- | --- |
| `LegionExtra_Ernie_Gunners` | MG / GMPG |
| `LegionExtra_Ernie_Marksmen` | Marksman / Sniper (мало T3) |
| `LegionExtra_Ernie_Grenadiers` | throwers / light demo |
| `LegionExtra_Ernie_Veterans` | Raider / Veteran / Shock (band A–B) |
| `LegionExtra_Ernie_Melee` | Crusher / Pillager / flank melee |
| `LegionExtra_Ernie_Flankers` | Scout / Warden / Ambusher |

**Универсальный Extra:** `LegionExtra_Ernie_Mixed` (6–9) — **по одному роллу на юнита** из пула специальностей (gunner / marksman / grenadier / raider / crusher / scout). Не один `EnemySquadUnit` 6–9: ванильный `GenerateRandEnemySquadUnits` иначе берёт тип один раз и клонирует → монотип в UI. Без офицеров/медиков. Один ID на много секторов.

Правила: Extra не = второй Medium; ставить где карта велика относительно base; **не** 2×Extra. Старый `LegionExtraSquadFireArms`(15) на Эрни Init — заменить на эти 5–10 packs.  
**UNITS-007 retire:** старые overflow-стеки (`*_Easy` Attackers/Defenders, толстые ExtraFireArms…), после смены Init и zero refs — в jazz-units `ModItemFolder` **Deprecated** (Id не hard-delete, если ещё referenced).

**4. Terrain / site presets (роль локации)**

Один и тот же size+band **не** значит один состав. Пресет задаёт **какие роли** в пулах (лес ≠ город ≠ аванпост):

| Preset | Где | Упор в составе |
| --- | --- | --- |
| **Forest / bush** | дебри, река, непроходимое (L2…) | flankers, Ambusher, Scout/Warden, melee/crush, меньше open MG |
| **Urban / village** | I5, J5, прибрежные посёлки | line rifle/marauder, Recruit/meat, Pillager/Shock в улицах, medic |
| **Outpost / camp** | villa camps, guard posts, M4 Outlook | sentry/flank perimeter, MG, marksman, NCO; меньше чистого мяса |
| **Fort / bunker** | I7, L6_UG… | entrenched: mortar/RPG/GL cap, gunners, officers — по story lock |
| **Coast / road** (optional) | M5–M6, I3–I4 | thin patrol / filler; чаще S–M, band A/B |

Пресет + band вместе: например Forest/**A** = зелёное мясо в кустах; Outpost/**C** = кадровый периметр без рекрутов. Не копировать Urban XL на лесной сектор.

**Difficulty:** body count по size-таблице Small/Medium/Large выше. Class band / preset не сдвигаются Easy/Hard. Medic count — Easy+1 / Hard−1 (STRATEGY-015), отдельно от body.

**Variance (owner lock — strong):** базовые отряды должны быть **очень вариативны по классам** (рандом внутри band+preset). Не «слот = один unitType», а **широкие weighted pools** siblings одной роли. Плюс **±10…20%** по числу тел на не-якорных слотах (`UnitCountMin`/`Max`). Стабильны только **role mean** и **якоря** (named story, officer/NCO/medic **по density**, mortar/RPG, ≤1 HeavyT2_GL, key sniper если band/preset требует). Extra-доборы тоже с пулами, разброс уже узже базы ок.

**Leaders / medics = Legion Global AI density (STRATEGY-005 / 015):** authored **Init** на Эрни считает якоря **так же**, как `JAZZ_GetLegionMax*` в `Code/LegionSquadComposition.lua` (не «1 сержант на сектор»). Уровни **сосуществуют** в пределах caps. **Quest packs — исключение** (см. ниже).

| Role | Formula | Unit |
| --- | --- | --- |
| Sergeant | `floor(n / 8)` | `LeaderT1_Sergeant` |
| Lieutenant | `floor(n / 15)` (band ~15–20) | `LeaderT2_Lieutenant` |
| Captain | `floor(n / 30)` | `LeaderT3_Captain` |
| MercCaptain | обязателен только для **band E / T4-squad**, не density | `LeaderT4_MercenaryCaptain` |
| Medic (Normal) | `n < 10` → 0; else `max(1, floor(n / 15))` | `FrontT1_Bonemaker` |

**Medic × difficulty (owner lock — loot):** Bonemaker = основной источник медикаментов. Сдвиг **обратный** body-count: **Easy больше медиков**, **Hard меньше**. Wired в Global AI: `JAZZ_GetLegionMaxMedics` / STRATEGY-015 (`Easy +1` / `Hard −1`; при `n≥10` не ниже 1). Пример n=60 → **5 / 4 / 3**; n=40 → **3 / 2 / 1**. Authored Init на Эрни: medic anchors тоже Easy+/Hard− (тот же сдвиг), вместе с body E/N/H gated slots.

Примеры размера (Normal): **n=10** → 1 SGT, 0 LT, 0 CPT, 1 medic · **n=20** → 2 SGT, 1 LT, 0 CPT, 1 medic · **n=40** → 5 SGT, 2 LT, 1 CPT, 2 medic · **n=60** → 7 SGT, 4 LT, 2 CPT, 4 medic. Named story bosses (Pierre, Headsman suite) **сверх** / вместо density, если sector lock так говорит.

Текущие I5/J5 packs по офицерам **не** подтягиваем под AI density — **исключение** (owner): authored meat/rifle hubs. **Медики Init** на прочих секторах — по AI density; I5 уже 4 Bonemaker.

**Quest packs = исключение** из officer/medic density (свой authored состав). `ErnieCounterAttack` и villa siege waves не обязаны совпадать с `floor(n/8)` и т.п.; у CounterAttack медики уже есть (3× Bonemaker) — ок как quest exception. Difficulty-сдвиг медиков на quest — по желанию отдельно, не автоматом.

| Special | N / note |
| --- | --- |
| M1–M3 | **исключение:** 0 Init (map markers); Roughneck→Recruit — отдельный pass |
| J4 | **исключение Init:** дорога J5↔I4; ~map markers only (нет sat InitialSquads) |
| J6 | **исключение Init:** аванпост контрабандистов; большой map fight (~50+ markers), не Legion Init pack |
| I5 / J5 officers | **исключение** density STRATEGY-005 |
| I7 maps | FortressPierre + `FortressDefenders` (~48); no Ordnance / deleted `LegionFortressDefenders` stack |
| `FortressDefenders_NoMaps` | ~16 for NoMaps remap only |
| `LegionFortressDefenders` | **Deleted** |

**Class tier ≠ gear tier:** `JAZZ_Legion_*T1…T4*` = experience / archetype / role kit. Campaign `JAZZ_Legion_Tier` = loot/equipment progression only.

**I7 Init target shape (LOCKED):** only `FortressPierre` (Pierre + Headsman suite) + **`FortressDefenders` (base 48)**. **Do not** stack `LegionFortressDefenders` or `LegionAttackers_Ordnance_Easy` — the locked Defenders pack already covers balanced fort defense (incl. mortar / RPG / single GL).

### Assigned so far (taxonomy tags)

| Pack / sector | Size | Band | Preset | Notes |
| --- | --- | --- | --- | --- |
| I5 `LegionErnieVillage` | XL ~60 | **A** | **Urban** | Recruit+Pillager meat; no Extra |
| J5 `Shooters_Easy_Ernie` | L ~40 | **A/B** | **Urban** | farms/village rifle; no Extra |
| Villa Sentry | S ~10 | A/B | **Outpost** | stays on camp |
| VillaAttackers_* | S–M 12–16 | varies | **Outpost** | siege waves; Ranger→Headsman |
| `ErnieCounterAttack` | ~30 | B | Urban→I5 | quest I7→I5 (maps) |
| `ErnieCounterAttack_NoMaps` | **20**, no mortar | B | Urban→I5 | NoMaps remap of quest pack |
| `FortressDefenders` | ~48 | B/C | **Fort** | I7 maps; **applied** UNITS-007 (E/N/H 38/48/58) |

Remaining Init — тег **size × band × preset × Extra?**; перегибы → [`JAZZ-UNITS-007`](../specs/active/JAZZ-UNITS-007.md).

### UNITS-007 overflow targets (Normal; band A unless noted)

Size = Small/Medium/Large per owner table (E/N/H = 5–10–15 / 20–**25**–40 / 30–**40**–70).

| Sector | Target Normal | Size | Band | Preset | Extra (0…1, 5–10) |
| --- | ---: | --- | --- | --- | --- |
| M4 | **25** | Medium | A | Outpost | `Marksmen` (смотровая) |
| M5 | **25** | Medium | A | Coast | `Mixed` (скалы/заброс, карта тянет) |
| M6 | **25** | Medium | A | Coast/port | `Gunners` (порт) |
| I2 | **25+Veterans** | Medium+Extra | **B** | Outpost | `Veterans` **light** (5–7, не жирный 10) → сумма ~30–32 |
| I3 | **25+Flankers** | Medium+Extra | A | Road | `Flankers` (мост) |
| I4 | **25** | Medium | A | Road | `Mixed` (длинный обрыв) |
| L1 | **40** | Large | **B** | Outpost | — (Large сам по себе) |
| L2 | **25** | Medium | A | Forest | `Melee` (гора/дебри) |
| L6 | **25** | Medium | A | Forest | `Flankers` |
| L6_UG | **25** | Medium | A/B | Fort | `Grenadiers` или `Gunners` |
| I7 | Pierre+48 | Fort | **B** | Fort | — (Defenders covers) |

Island: mostly **A**; keys **B** with little T3. Apply pending UNITS-007.

### LOCKED `ErnieCounterAttack` (quest I7→I5; Normal base **30**; owner 2026-08-10)

Soft-nerf vs old ~37 (NoMaps complaints: too big/strong). Easy **20** / Hard **40** — same gated-slot approach as UNITS-007 (quest exception on officers/medics density).

| N | Unit |
|--:|---|
| 1 | `LeaderT1_Sergeant` (was 2) |
| 3 | Roughneck |
| 6 | ShockTrooper (was 8) |
| 2 | Ambusher |
| 2 | ShockTrooper (was 3) |
| 6 | Raider (was 8) |
| 2 | AssaultT1_Grenadier |
| 1 | Mortarman |
| 2 | GMPG (was 3) |
| 1 | Rocketeer |
| 1 | FrontT3_Veteran |
| 3 | Bonemaker |

**Total 30.** Keep: 3 medics, 1 mortar, 1 RPG, 2 thrower grenadiers. No HeavyT2_Grenadier.

### LOCKED `FortressDefenders` composition (Normal base **48**; owner 2026-08-10)

| N | Role | Units |
|--:|---|---|
| 1 | Officer | `LeaderT2_Lieutenant` |
| 2 | NCOs | `LeaderT1_Sergeant` ×2 |
| 2 | Medics | `FrontT1_Bonemaker` ×2 |
| 1 | Mortar | `HeavyT3_Mortarman` |
| 1 | RPG | `HeavyT1_Rocketeer` |
| 1 | GL | `HeavyT2_Grenadier` ×1 (**hard cap**) |
| 4 | MG | 2× `GunnerT2_GMPG` + 1× `GunnerT1_Gunner` + 1× `GunnerT2_AssaultGunner` |
| 3 | Precision | 2× `FrontT3_Sniper` + 1× `FrontT2_Marksman` |
| 2 | Ambush | `FrontT2_Ambusher` |
| 6 | Flank | 2× Warden + 2× Scout + 1× Skirmisher + 1× Recon |
| 8 | Line | 3× Raider + 2× Rifleman + 2× Marauder + 1× `FrontT3_Veteran` |
| 8 | Assault | 2× Shock + 2× AssaultT1_Grenadier + 2× Crusher + 1× Pillager + 1× Pyro |
| 6 | Meat | 3× Roughneck + 3× Marauder/Rifleman pool |
| 3 | Little T3 | 1× Punisher + 1× SkullCrusher + 1× `FrontT3_Veteran` (or 2nd Punisher). **No `GunnerT3_VeteranGunner`** |

**Total 48.** Easy 38 / Hard 58. Variance: weighted pools on line / assault / flank / meat / little-T3; anchors fixed (LT, 2 SGT, 2 Bonemaker, Mortar, RPG, 1 GL, 2 Sniper). Implementation deferred until Ernie squads change-spec is approved — this table is the contract for `FortressDefenders`.

### LOCKED Villa camps K3/K5/L3/L4/L5 (owner 2026-08-10)

Shared `JAZZ_Legion_SentrySquad_AroundVilla` **base 10** (camp guard; stays) + sector `VillaAttackers_*` (**movable siege waves** for `Jazz_VillaCounterAttack`). Sector Init totals Normal **22 / 23 / 24 / 25 / 26**. Easy/Hard ±10 later.

| Sector | Sentry | Attacker | Normal | Easy | Hard |
| --- | ---: | ---: | ---: | ---: | ---: |
| K3 | 10 | K3=12 (Ranger) | 22 | 12 | 32 |
| K5 | 10 | K5=13 (Captain) | 23 | 13 | 33 |
| L3 | 10 | L3=14 (LT) | 24 | 14 | 34 |
| L4 | 10 | L4=15 (SGT + RPG) | 25 | 15 | 35 |
| L5 | 10 | L5=16 (Headsman + mortar) | 26 | 16 | 36 |

**Siege (`JAZZ-QUESTS-003`):** after `FlagHill_Emma_1` Guests → route surviving Attackers + always `JAZZ_Legion_VillaAttackers_Ernie` (30) → K4; AdvanceTo Emma; Wave2 ~25 on CombatTurn≥3; late columns dump. K4 map HouseAmbushers+Legion AdvanceTo **purged**.

Applied camp sizes via `docs/tools/_tighten_villa_squads.py`. Counts fixed (Min=Max); role variance stays in weighted pools.

### LOCKED `LegionErnieVillage` (I5; Normal base **60**; owner 2026-08-10)

Meat hub — largest island Init. Mostly T1 + Recruit; up to **10 Pillager**; few pyro; little T2–T3 spice. Init = this pack only (no Extra stacking). Easy 50 / Hard 70 later.

| N | Unit |
|--:|---|
| 1 | `LeaderT1_Sergeant` |
| **4** | **`FrontT1_Bonemaker`** (AI density `floor(60/15)`) |
| 12 | `JAZZ_Legion_Recruit` |
| 8 | `AssaultT1_Roughneck` |
| 6 | Marauder / Rifleman pool |
| 6 | Crusher (SkullCrusher low weight) |
| **10** | **`AssaultT2_Pillager`** |
| 2 | `AssaultT1_Grenadier` |
| 2 | `FrontT2_Raider` |
| 2 | Shock / Pillager pool |
| 1 | `AssaultT2_Pyro` |
| 2 | Marksman / Rifleman |
| 2 | Ambusher (Sniper low weight) |
| 2 | Gunner / GMPG |

**Total 60.** Applied via `docs/tools/_rewrite_legion_ernie_village.py`.

### LOCKED `LegionDefenders_Shooters_Easy_Ernie` (J5 farms; Normal base **40**)

Second-largest island Init. More rifle line than I5; still meat+Recruit. J5 Init = this pack only. Easy 30 / Hard 50 later. Same apply script.

Policy: with Legion Global AI, static `InitialSquads` = starting garrisons or quest packs — not the living army. Living pressure = AI (patrol / reinforce / QRF).

## Owner sector map (Ernie grid, 2026-08-10)

Канон описаний владельца (для preset/ролей). Где `display_name` в `jazz-maps` расходится — в скобках факт items.

| | I | J | K | L | M |
| --- | --- | --- | --- | --- | --- |
| **2** | I2 жильё доктора / бывшие укр. | — море — | — | L2 гора, водопад, оттоки | M2 скалистый берег / побережье |
| **3** | I3 мост/дорога над рекой | — | K3 лагерь Легиона 1 | L3 лагерь Легиона 2 | M3 **водопад** (актуально) |
| **4** | I4 филер дорога Эрни–мост, обрыв | J4 дорога J5→I4 | K4 Флаговый холм | L4 лагерь Легиона 3 | M4 смотровая |
| **5** | I5 деревня Эрни (берег) | J5 фермы / деревня без берега | K5 лагерь Легиона 5 | L5 лагерь Легиона 4 | M5 заброс, скалы |
| **6** | I6 Жестянка | J6 дорога контрабандистов *(OK)* | K6 резерв. лагерь контрабандистов | L6 бункер (+UG) | M6 **Старый порт** |
| **7** | I7 Форт Ло-Блё | J7 Изумрудный берег | K7 сожж. деревня / скалистый берег | L7 малая береговая деревня | — заглушка — |
| **1** | — | — | — | L1 лагерь повстанцев | M1 зона высадки |

**Init scope:** перегибы UNITS-007 = M4–M6, I2–I4, L1–L2, L6/UG, I7.  
**Исключения Init:** M1–M3 map-only; J4/J6 map-only; I5/J5 size+officers locked/exception; villa K3/K5/L3–L5 locked; I6/J7/K6/K7/L7 — отдельно (часто 0 Init или non-Legion map).

## Counts by sector

| Sector | Name | Init sum | Init packs | Patrol/Strong/Extra | Map enemies≈ | Notes |
| --- | --- | ---: | --- | --- | ---: | --- |
| M1 | Зона высадки | 0 | — | — | 1 | Стартовый берег; map-only enemies |
| M2 | Скалистый берег | 0 | — | — | 24 | map-only |
| M3 | Водопад | 0 | — | — | 33 | map-only; водопад здесь |
| M4 | The Outlook | 30 | LegionOutlook_Easy(30) | — | 0 | Смотровая |
| M5 | Береговая линия | 53 | … | — | 0 | UNITS-007 Medium → **25** |
| M6 | Старый порт | 54 | … | — | 0 | UNITS-007 Medium → **25** |
| I2 | Лечебница в маяке | 32 | Marksmen / Balanced / Mobile stacks | — | 0 | жильё доктора / бывш. укр.; UNITS-007 B ~20–22 |
| I3 | Дорога к маяку | 8 | Balanced_Easy stack | — | 0 | Medium → **25** |
| I4 | Дорога на маяк | 8 | Entrenched_Easy stack | — | 0 | Medium → **25** |
| I5 | Village of Ernie | **60** | LegionErnieVillage(60) | — | 10 | LOCKED meat hub; берег |
| I6 | The Rust | 0 | — | — | 0 | Жестянка |
| I6_Underground | Bunker FB45-68 | 0 | — | — | 0 | Бункер_Жестянки |
| I7 | Fort L'Eau Bleu | (pre-rework) | Pierre + Defenders + Ordnance… | — | 0 | Target: Pierre + Defenders(48); drop Ordnance |
| J4 | Дорога в Эрни | 0 | — | — | 4 | J5→I4; map-only |
| J5 | Фермы Эрни | **40** | Shooters_Easy_Ernie(40) | — | 0 | LOCKED; деревня без берега |
| J6 | Аванпост контрабандистов | 0 | — | — | 55 | дорога контрабандистов; map-only; **owner OK — не трогать** |
| J7 | Emerald Coast | 0 | — | — | 0 | Изумрудный берег |
| K3 | Походный лагерь Легиона | **22** | Sentry(10)+Attackers_K3(12) | — | 0 | лагерь 1; LOCKED |
| K4 | Flag Hill | (map Raiders) | — | — | ~24 | Флаговый холм; siege QUESTS-003 |
| K5 | Походный лагерь Легиона | **23** | Sentry+Attackers_K5 | — | 2 | лагерь 5; LOCKED |
| K6 | Запасной лагерь Контрабандистов | 0 | — | — | 91 | резервный лагерь; map-only |
| L1 | База партизан | 65 | Raid+Heavy+JAZZT2+Extra | — | 0 | Large → **40** |
| L2 | Непроходимая местность | 27 | Melee+Raid | — | 0 | Forest Medium → **25** (E20/H40) |
| L3 | Походный лагерь Легиона | **24** | Sentry+Attackers_L3 | — | 0 | лагерь 2; LOCKED |
| L4 | Походный лагерь Легиона | **25** | Sentry+Attackers_L4 | — | 1 | лагерь 3; LOCKED |
| L5 | Походный Лагерь Легиона | **26** | Sentry+Attackers_L5 | — | 1 | лагерь 4; LOCKED |
| L6 | Вход в бункер | 30 | Patrol+Melee | — | 0 | Medium → **25** |
| L6_Underground | Бункер партизан | 31 | FireArms+Raid+Melee | — | 0 | Medium → **25** |
| L7 | Рыбацкая деревня | 0 | — | — | 0 | малая береговая деревня |

## Notes on measurement

- **Init sum** = sum of `UnitCountMin` over referenced `ModItemEnemySquads` in `jazz-units` (fallback: vanilla `EnemySquads.lua` if ID not in jazz-units).
- **Map enemies≈** = `UnitMarker` with enemy-ish Side / Legion-like UnitData on the sector map dump (approximate; triggers/spawns may add more).
- I7 Patrol/Strong/Extra are **pools**, not all spawned at once — do not add them to Init sum.
- Regenerated by `docs/tools/_ernie_garrison_baseline.py`.

