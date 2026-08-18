# Playtest bug report: `jazz-nomaps` (Discord, 2026-07-30)

**Статус:** fixed in jazz-nomaps **0.5** (PR #1) + **0.6** armor remap + **0.7–0.9** Global AI; **B9 Bastien remap** fixed in nomaps code (named suffix skip); **B21–B23** (A2/F5/G6, Discord Firestarter 2026-08-18) — COMPAT-010 class-remap skip + Pierrot `conflict_ignore` (runtime smoke still open)  
**Профиль:** `jazz_assets` + `jazz-units` + **`jazz-nomaps`** (`7MsJ2Eq`) + `jazz` (+ CommonLib), без `jazz-maps`  
**Источник:** Discord playtest (Sergej 1973 / Kpoji4er), скрины инвентаря сектор **I2**; follow-up Discord 2026-07-31 (броня с оригинала); Discord Firestarter 2026-08-18 (A2/F5/G6)  
**Спека:** [JAZZ-COMPAT-002](../../specs/active/JAZZ-COMPAT-002.md), [JAZZ-COMPAT-010](../../specs/active/JAZZ-COMPAT-010.md)  
**Пакет-владелец фикса:** `jazz-nomaps` (лут/sanitize/remap); cut-реестр — [weapons/cut-content.md](../weapons/cut-content.md)

## Краткий вердикт

Профиль NoMaps стартует, но лут и часть спавнов тянут **вырезанный / неиспользуемый vanilla-контент** и **старые архетипы**. Жёлтые иконки с надписью `test` — не «битый asset», а намеренная метка `Ammopics/TEST.png` на патронах, которые JAZZ не использует.

## Симптомы (наблюдение)

| # | Симптом | Где |
| --- | --- | --- |
| S1 | Жёлтые тайлы с текстом `test`, иногда с аномально большим числом под слотом (~1.4M–4.8M) | Схрон / контейнеры / трупы, сектор I2 |
| S2 | В сундуках и на трупах ванильный или «полуванильный» лут; часть предметов бесполезна | I2, контейнеры и трупы |
| S3 | У врагов «новое» оружие + «старая» броня | Бой / лут трупов |
| S4 | К Hi-Power выпадают `.45` или `9x18`, к «калашу» — нормальные патроны | Лут / инвентарь врагов |
| S5 | Нет новых архетипов: головорезы, мародёры, снайпер | Состав отрядов на карте |

## Что это НЕ является

- **Не missing Icon / missing loc string.** Owner: патроны с `Icon = Mod/e6L4ECj/Ammopics/TEST.png` — осознанная пометка **неиспользуемых** vanilla ammo. Полный реестр: [вырезанный контент](../weapons/cut-content.md).
- **Не баг MP5A2/MP5A4.** Базовый класс `MP5` (и `AR15`, `M4Commando`) — `Убираем` / `ОТКЛЮЧЕНО`. Живые варианты — `MP5A2` / `MP5A4` / `MP5K` / `MP5SD`.

## Корневые причины (static)

### B1 — LootDef / fallback nomaps ссылаются на cut ammo и cut `MP5`

В `jazz-nomaps` (`items.lua` + `Code/NoMaps_Autonomy.lua`):

- Packs `JAZZ_NoMaps_Container_Ammo` → `_9mm_Basic`, `_556_Basic`, `_762NATO_Basic`, `_762WP_Basic`, `_12gauge_Buckshot` (все с `TEST.png`, калибры vanilla `9mm`/`556`/…).
- Pack `JAZZ_NoMaps_Container_Weapon` и `LOOT_POOLS_FALLBACK.weapons` включают **`MP5`** (ОТКЛЮЧЕНО), рядом с живыми `AK47`, `UZI`, `Galil`, `FAMAS`, `Glock18`.

Inject на `ExplorationStart` / `CombatStart` кладёт эти классы в vanilla `ItemContainer` поверх (или вместо ожидаемого JAZZ-лута).

**Ожидание:** только актуальные `JAZZ_AMMO_*` / живые weapon IDs (например `MP5A2` вместо `MP5`).

### B2 — Vanilla map loot и corpse inventory не вычищаются

Даже без inject vanilla HotDiamonds контейнеры и дроп юнитов остаются. Без maps authored loot tables игрок видит смесь: ваниль + inject cut-ammo. Скрин с MP5 в сундуке согласуется с B1 (и/или vanilla container contents).

### B3 — Remap отрядов не покрывает весь InitialSquad / состав

`SQUAD_REMAP` + wrap `GenerateEnemySquad` переписывают известные Legion/WorldFlip ID на jazz defs, но:

- не все vanilla `InitialSquads` / локальные списки секторов попадают в matrix;
- playtest видит старые роли (головорезы / мародёры / снайпер) → UnitData и loot tables не из jazz-units tier kit.

`lRefreshEnemyLoadouts` делает strip + `CreateStartingEquipment` один раз на unit id, но только для Affiliation Legion/Army/Adonis/Rebel и только если юнит ещё не `geared`. На **ванильном** UnitData это даёт JAZZ-переопределённые классы оружия (тот же `HiPower` → `JAZZ_Caliber_9x19`) при **старых** броне/лут-таблицах патронов → S3/S4.

### B4 — Несовпадение калибра Hi-Power vs выпавшие патроны

`InventoryItem/HiPower.lua`: `Caliber = "JAZZ_Caliber_9x19"`.  
`.45` / `9x18` к Hi-Power — чужой калибр (другие пистолеты JAZZ: USP/1911 → `.45ACP`, APS/PB/Scorpion → `9x18`).

Вероятный путь: ванильный archetype + старый ammo loot / не тот `GetAmmosWithCaliber` fallback, либо в инвентаре лежат cut `_9mm_*` / чужие `JAZZ_AMMO_*`, пока ствол уже на `JAZZ_Caliber_9x19`. Калаш на `JAZZ_Caliber_762x39` чаще совпадает с живым пулом → «к калашу нормальные».

### B5 — Аномальные числа под `test`-тайлом

На скринах под жёлтым `TEST.png` видны величины порядка миллионов. У cut ammo `MaxStacks` обычно ≤ 120 — это **не** объясняет Amount ~4.8M само по себе. Открытый вопрос runtime: битый `Amount`, другой предмет в том же слоте, или UI-артефакт. Нужен hover / dump class id.

## Связь с COMPAT-002 AC

| AC | Следствие playtest |
| --- | --- |
| AC-002 regions / Legion tick | не опровергнут этими скринами |
| AC-005 spawn/remap + container loot | **FAIL (human):** loot packs отдают cut ammo/`MP5`; remap/archetypes неполные |
| AC-007 human profile start | профиль стартует (частичный PASS), экономика лута/отрядов — нет |

## Fix set (merged)

**jazz-nomaps 0.4–0.5** ([PR #1](https://github.com/Kpoji4er/JAZZ-nomaps/pull/1)):

1. LootDef + `LOOT_POOLS_FALLBACK` → `JAZZ_AMMO_*` / `MP5A2` (без `_9mm_*` / cut `MP5`).
2. Deny cut/`_*`/`TEST.png` при inject (`lItemAllowed` / `lAddItemsToContainer`).
3. После `CreateStartingEquipment` — `lSanitizeUnitAmmo` (+ strip cut firearms).
4. Расширен `SQUAD_REMAP` (`LegionRaidSquad_01/02/03`, hard variants, `LegionFortressDefenders`, …).
5. `lScrubContainerCutItems` на Exploration/Combat — вычищает cut из vanilla контейнеров до inject.

### B6 — Legacy armor stubs after gear refresh (Discord 2026-07-31)

`CreateStartingEquipment` на ванильных архетипах кладёт `FlakVest` / `KevlarVest` / `HeavyArmor*` / `*Leggings` / `*Helmet`. В JAZZ эти ID — неполные stubs **без `ArmorRating`**, поэтому:

- бой «как без брони»;
- предметы нельзя нормально найти/снять в JAZZ inventory (нет полноценного JazzArmor-контракта).

Оружие после CSE+ammo sanitize уже живое (вопрос «Оружие норм?» — да, путь оружия ок).

**Fix (nomaps 0.6):** `ARMOR_REMAP` light→`JazzArmor_Flak*`, medium→`JazzArmor_GuardianMedium` / PASGT / GuardianLegs, heavy→Guardian Full/Heavy; `GEAR_REV=2` перегоняет уже `geared` юнитов только на armor sanitize; pack `JAZZ_NoMaps_Container_Armor` + scrub remap в контейнерах.

**Остаётся (human):** smoke I2 — нет `TEST.png` / `MP5` (ОТКЛЮЧЕНО); Hi-Power только с `JAZZ_Caliber_9x19` ammo; враги/сундуки носят `JazzArmor_*`, не `FlakVest`/`KevlarVest`.

### B7 — Global AI «заморожен» (Discord 2026-07-31)

Симптом: на NoMaps не появляются managed отряды / нет tax–recruiter цикла.

Static root cause (до 0.7):

1. `JAZZ_Auto_*` стартовали с `StartingManpower=12` при garrison `size_min=25` → composition generator отказывает;
2. `TaxCap=0` / `RecruiterCap=0` → manpower не восстанавливается;
3. disabled `ErnieIsland` оставлял `Sectors` (I2–I7…), совпадающие с HotDiamonds → `GetRegionForSector` мог вернуть disabled region.

**Fix (nomaps 0.7 + jazz COMPAT-003):** manpower 40 / Tax+Recruiter on / clear Sectors / `ai_economy_rev` migrate; jazz `GetRegionForSector` предпочитает `LegionAIEnabled`. Patch kit: `docs/patches/jazz-nomaps-0.4/`.

**Reopen (COMPAT-004):** economy defaults были в 0.8, но AI всё ещё выглядел мёртвым:

1. jazz `NewGame` EnsureState latch'ил `major.hq_sector=B28` (Ernie) до nomaps disable → logistics на воду;
2. HotDiamonds InitialSquads блокировали `lGarrisonTarget` (defense already present), а managed outpost глушил vanilla spawn;
3. пустой POI stock / долгий pulse → tax/recruiter не стартовали.

**Fix (nomaps 0.9 + jazz COMPAT-004):** `JAZZ_LegionAIForceMajorHQ(A20)`; Ernie HQ skip при NoMaps-профиле; `JAZZ_LegionAIAdoptOutpostDefenders`; `JAZZ_LegionAISeedPoiEconomy`; UnitData remap + tiered container loot. Runtime AC всё ещё нужны (`JAZZ_LegionAIPrintEconomy` → HQ=A20; managed squad в sat-view).

### B8 — Gear refresh пропускал отряды (`ipairs` по sparse `gv_Squads`)

`lRefreshEnemyLoadouts` обходил `gv_Squads` через `ipairs`. После despawn появляются дыры в id-map → refresh обрывался, часть врагов без ammo sanitize / armor remap.

**Fix (nomaps 0.8):** `sorted_pairs(gv_Squads)`; refresh также на Exploration/Combat; Affiliation `Thugs`; one-shot log missing EnemySquadDef; expand remap + prefix heuristic; after bootstrap зовёт `JAZZ_UpdateLegionTierForNoMaps` (гонка Load/NewGame с jazz).

### B9 — Bastien → «Мародёр» на пляже I1 (Discord 2026-08-01)

Симптом: на стартовом пляже вместо Бастьена (`LegionRaider_Jose`) ходит юнит с именем **Мародёр** (`JAZZ_Legion_FrontT1_Marauder`). Квест «Встреча с клиентом» / I1.

**Root cause:** COMPAT-004 UnitData remap (`lMatchUnitFamily`) матчил по префиксу stem (`LegionRaider` ⊆ `LegionRaider_Jose`) → пул `front` T1. Spec REQ-004 уже требовал named/Hyena skip, но суффикс не проверялся.

**Fix (nomaps code):** `UNIT_GENERIC_SUFFIX` allowlist (`""`, `_Stronger`, `_Elite`, …); `LegionRaider_Jose` / Hyena / Kidnapper не ремапятся. Static: `docs/tools/_verify_nomaps_unit_remap_named_skip.py`.

### B10 — Tutorial Flag Hill «Головорезы» → «Мародёры» (Discord 2026-08-01)

Симптом: стартовые ослабленные леги на Flag Hill / tutorial выглядят как **Мародёр**.

**Root cause:** ванильный `LegionRaider_WeakFlagHill` имеет display Name **Goon/Головорез**, но ID на stem `LegionRaider` → пул `front` → `JAZZ_Legion_FrontT1_Marauder`.

**Fix:** `UNIT_FAMILY_OVERRIDE[LegionRaider_WeakFlagHill]=assault` → T1 Roughneck (Головорез); `*_Tutorial` / WeakFlagHill всегда **tier 1**; stem `LegionMarauder` для `LegionMarauder_Tutorial` → front T1. Bastien (`_Jose`) по-прежнему skip.

### B11 — Стрелок без оружия (Discord 2026-08-01)

Симптом: `JAZZ_Legion_FrontT1_Rifleman` (ник «Безграмотный стрелок») живой без ствола; труп — шлем/штаны/маска, без firearm.

**Root cause:** `QuestIsVariableNum` читает `rawget(quest, JAZZ_Legion_Tier)` — metatable default `11` не виден до `SetQuestVar`. Bootstrap делал `lRefreshEnemyLoadouts` **до** tier update; CSE мог собрать броню/misc без primary; `GEAR_REV` лочил состояние; live `g_Units` не синхронизировался с `gv_UnitData`.

**Fix (nomaps GEAR_REV=3 + jazz LegionTierProgression):** rawset tier перед refresh; strip+CSE+`lEnsureFirearm(SKS)` на unitdata **и** live Unit; UpdateLegionTier rawset'ит даже при `computed==current` если raw nil.

### B12 — Засадник только с сигнальным пистолетом (Discord 2026-08-01)

Симптом: `JAZZ_Legion_FrontT2_Ambusher` без боевого ствола; в руках FlareHandgun.

**Root cause:** sniper T1 pool включал Ambusher; при miss primary night-loot `JAZZ_Gen_FlareGun` остаётся единственным Firearm; `lEnsureFirearm` считал FlareGun «стволом».

**Fix (GEAR_REV=4):** sniper T1 → только Rifleman; `lIsCombatFirearm` excludes FlareGun/HeavyWeapon.

### B13 — Ранние пластины 3 класса у стрелка/мародёра (Discord 2026-08-01)

Симптом: в деревне у Rifleman / Marauder уже **стальные пластины 3 класса** — слишком рано.

**Root cause:** Middle-пакеты `TireArmor_ScrapPlate` / `TireArmor_KevlarPlate` (tier ≥12 / ≥13) по ошибке клали `JazzArmorPlates_Steel3` вместо Scrap / Kevlar. Light (`LeatherArmor_*`) был корректен. Steel3 по дизайну — major T2 (`TireArmor_SteelPlate`, ≥21).

**Fix (jazz-units):** ScrapPlate → `JazzArmorPlates_Scrap`, KevlarPlate → `JazzArmorPlates_Kevlar`.

### B15 — Assert «Attempt to create a new global» + HQ=B28 (2026-08-02)

Симптом: при закрытии Mod Manager / NewGame / LoadGame — Assert на `g_JAZZ_NoMapsGenerateEnemySquadWrapped`, `…WorldFlipGuarded`, `JAZZ_NoMaps_CreateUnitDataWrapped`, `…UnitMarkerWrapped`; затем `Groups` boolean при `SetQuestVar` из tier rawset. В консоли `JAZZ_NoMapsIsActive()=true`, но `Major HQ=B28`, outpost только `I7` disabled — глобалка «мертва».

**Root cause:** wrap flags писались в `_G` из `OnMsg` без предварительного объявления (strict globals). Bootstrap обрывался до `ForceMajorHQ(A20)` / auto-regions. `SetQuestVar` на early NewGame гонял TCE при `Groups` ещё boolean.

**Fix (nomaps 0.9.9 + jazz LegionTierProgression):** top-level predeclare + `rawset` для wrap flags; `lQuestVarSafeSet` / safe `lSetTier`. Skill: `.agents/skills/jazz-lua-globals/SKILL.md`.

### B16 — SeedPoiEconomy: undefined `lSectorIsSurface` (2026-08-02)

Симптом: после globals-fix bootstrap всё ещё мог оставить `HQ=false` / пустые auto-regions; в логе `Attempt to use an undefined global 'lSectorIsSurface'` (`Guardpost_Patrols.lua` ~740). Параллельно: `InventoryItem class Mas36 not found` при спавне loot.

**Root cause:** `JAZZ_LegionAISeedPoiEconomy` вызывал local `lSectorIsSurface` *выше* объявления (Lua → global lookup → Assert); ошибка рвала хвост NoMaps bootstrap. Loot UNITS-003 писал CSV slug `Mas36`, а класс оружия — `MAS36`.

**Fix:** inline surface check в Seed; `bootstrapped=true` только после healthy `JAZZ_Auto_*`; loot `item="MAS36"`; generator резолвит DefineClass из companion. Soft-bootstrap при пустых auto-regions больше не early-return (регресс HQ=false / только I7). Audit: `docs/tools/_audit_loot_item_case.py`.

### B14 — Жестянка day-1 «другая весовая» (Discord 2026-08-02)

Симптом: NoMaps, день 1, I6 Жестянка — враги уже другой весовой категории. Подозревали ускоренный gear tier; на дне 1 major I должен оставаться.

**Root cause:** `SQUAD_REMAP` вёл в `LegionJAZZSquadT1` (mixed T2–T4); UnitData remap поднимал Stronger/Elite / `Stronger_Elite`→T4 даже при gear major I.

**Fix (COMPAT-005):** `LegionJAZZSquadT1_Early` (только T1); NoMaps alias + tiered resolve; class-tier cap на major I. Static: `docs/tools/_verify_nomaps_early_squad.py`.

### B17 — Auto-regions огромные / чужие Guardpost в Sectors (playtest 2026-08-02)

Симптом: save `31(3)`, NoMaps — на сат-карте округа выглядят как «мега-регионы»; DAP: 8× `JAZZ_Auto_*`, `mop=1`, но `#Sectors` 53…132 и `foreign_gp` 3…6.

**Root cause:** Chebyshev R=8 + soft `lRefreshTrackedAutoRegions` вызывал assign **по одному** outpost (без Voronoi-конкуренции).

**Fix (COMPAT-006):** `AUTO_REGION_RADIUS=3`; multi-outpost Voronoi refresh; `ai_region_rev` rebuild. Static: `docs/tools/_verify_nomaps_region_radius.py`.

### B18 — Auto-regions orphans after COMPAT-006 R=3 (playtest 2026-08-02)

Симптом: после shrink на сат-карте сектора без округа; DAP: surface=151, covered=125, orphans=26 (периферия `A*`/`B*`/`J*`/`K*`/`L*`), foreign_gp=0.

**Root cause:** hard Chebyshev `best_dist ≤ 3` не покрывает клетки дальше R от любого Guardpost.

**Fix (COMPAT-007):** unbounded nearest-outpost Voronoi (`AUTO_REGION_RADIUS=false`); `AI_REGION_REV=2`. Static: `docs/tools/_verify_nomaps_region_radius.py`.

### B19 — Shipment/tax UI `$` without lootable diamonds (2026-08-02)

Симптом: «АЛМАЗНЫЙ КОНВОЙ — ВЕЗЁТ $12000» / tax `$` в задаче, но после боя нет `DiamondBriefcase`/`TinyDiamonds`. DAP: `payload.money` + `diamond_briefcase=true`, inventory DB=0.

Root: (1) tax collect не звал cargo ensure; (2) `lEnsureMoneyCargo` мог выставить flag без успешного `AddItem`; (3) `_RegenerateLegionLoot` / gear refresh **стирает** весь Legion inventory → cargo пропадает, UI `$` остаётся.

**Fix (STRATEGY-017):** tagged `jazz_legion_ai_cargo` sync (`lSyncMoneyCargo`); multi-carrier; tax collect + supply/shipment spawn; clear on delivery; resync hourly / `ConflictStart` / after loot regen; console `JAZZ_LegionAIResyncMoneyCargo()`. Live save retrofitted via DAP evaluate (18 squads).

### B20 — Early mobile density too high / diamond income flood (2026-08-02)

Симптом: logistics escorts **[19]** day-1; `$`/mine income слишком быстрый.

**Fix (STRATEGY-016):** early→mature size curve (time/heat/tier); logistics composition escorts; `JAZZ_LegionEconomyScalePct=25` (÷4); cadence 12h command / 48h tax·recruiter·combat spawn / 96h POI. Existing fat squads not shrunk; new spawns only.

### B21 — A2 Diamond Red: 0 surviving miners (Discord Firestarter 2026-08-18)

Симптом: убийство Graaf до выстрела, журнал «выживших рабочих 0»; доход шахты 50%.

**Root cause:** `DiamondRedSquad` class-remap → `JAZZ_Legion_*` рядом с гражданскими `Miners`; ванильный TCE Graaf/Legion target miners.

**Fix (COMPAT-010):** `STORY_SQUAD_KEEP_VANILLA_UNITS.DiamondRedSquad` — не ремапить class. Уже зафиксированный `MinersAlive` в save не откатывается.

### B22 — F5 капитан Пьеро пропал, порт не открыть (Discord Firestarter 2026-08-18)

Симптом: нет Пьеро, нельзя спустить лодку / открыть порт Côte d'Azur.

**Root cause:** ForceConflict + `neutral_retaliate`; стартовый `LegionDefenders_Balanced_Easy` после remap бьёт как JAZZ T1. Ваниль при смерти `NPC_CaptainPierrot` снимает `AbandonedBeach_EnablePort`.

**Fix (COMPAT-010):** skip class-remap только F5+`LegionDefenders_Balanced_Easy`; `conflict_ignore` на живом Пьеро. Уже мёртвый Пьеро в save не воскрешается.

### B23 — G6 колодец: радио + конфликт, отряда нет (Discord Firestarter 2026-08-18)

Симптом: закат, радио, Satellite conflict, на тактике пусто.

**Root cause:** vanilla `WaterWell` conflict без satellite-сквада (`no_exploration_resolve`); remap `LegionWaterWell` маркеров сбрасывает квестовую группу.

**Fix (COMPAT-010):** не ремапить marker group `LegionWaterWell`. Пустой текущий визит — выйти и зайти на следующем закате.

### Quality / named-veteran early (Sergej) — deferred

Owner 2026-08-02: «выходит из 2» — **no separate heavy-gate track**. Cargo/logistics clarity (B19) is enough for now; quality complaints may mix transporter vs combat.

## Evidence

- Discord скрины: инвентарь отряда «Чарли», схрон/трупы/сундук сектор I2.
- Static: `jazz-nomaps` LootDef/fallback; `InventoryItem/_9mm_Basic.lua` → `TEST.png`; `MP5.lua` / `AR15.lua` → «Убираем».
- Static: `HiPower.Caliber = JAZZ_Caliber_9x19`.
- DAP 2026-08-02: shipment id=96 `$12000` DB=0→DB=1 after inline resync; tax `$2500` → 5×TinyDiamonds.