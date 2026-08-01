# Playtest bug report: `jazz-nomaps` (Discord, 2026-07-30)

**Статус:** fixed in jazz-nomaps **0.5** (PR #1) + **0.6** armor remap + **0.7–0.9** Global AI; **B9 Bastien remap** fixed in nomaps code (named suffix skip); runtime smoke on I1 Bastien / I2 loot still recommended  
**Профиль:** `jazz_assets` + `jazz-units` + **`jazz-nomaps`** (`7MsJ2Eq`) + `jazz` (+ CommonLib), без `jazz-maps`  
**Источник:** Discord playtest (Sergej 1973 / Kpoji4er), скрины инвентаря сектор **I2**; follow-up Discord 2026-07-31 (броня с оригинала)  
**Спека:** [JAZZ-COMPAT-002](../../specs/active/JAZZ-COMPAT-002.md)  
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

## Evidence

- Discord скрины: инвентарь отряда «Чарли», схрон/трупы/сундук сектор I2.
- Static: `jazz-nomaps` LootDef/fallback; `InventoryItem/_9mm_Basic.lua` → `TEST.png`; `MP5.lua` / `AR15.lua` → «Убираем».
- Static: `HiPower.Caliber = JAZZ_Caliber_9x19`.
