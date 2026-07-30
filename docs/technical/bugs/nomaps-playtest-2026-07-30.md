# Playtest bug report: `jazz-nomaps` (Discord, 2026-07-30)

**Статус:** open (human playtest)  
**Профиль:** `jazz_assets` + `jazz-units` + **`jazz-nomaps`** (`7MsJ2Eq`) + `jazz` (+ CommonLib), без `jazz-maps`  
**Источник:** Discord playtest (Sergej 1973 / Kpoji4er), скрины инвентаря сектор **I2**  
**Спека:** [JAZZ-COMPAT-002](../../specs/active/JAZZ-COMPAT-002.md)  
**Пакет-владелец фикса:** в основном `jazz-nomaps`; cut-контент и калибры — `jazz` / `jazz-units`

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

- **Не missing Icon / missing loc string.** Owner: патроны с `Icon = Mod/e6L4ECj/Ammopics/TEST.png` — осознанная пометка **неиспользуемых** vanilla ammo (`_9mm_*`, `_556_*`, `_762WP_*`, `_762NATO_*`, `_44CAL_*`, `_12gauge_*`, `_50BMG_*`, …).
- **Не баг MP5A2/MP5A4.** Базовый класс `MP5` (и аналогично `AR15`, `M4Commando`) помечен `comment = "Убираем"`, `DisplayName = "ОТКЛЮЧЕНО"`, старый калибр (`9mm` / `556`). Живые варианты — `MP5A2` / `MP5A4` / `MP5K` / `MP5SD`.

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

## Предлагаемый fix set (не в этом коммите)

1. **`jazz-nomaps` items + `LOOT_POOLS_FALLBACK`:** заменить все `_9mm_Basic`/… на актуальные `JAZZ_AMMO_*`; `MP5` → `MP5A2` (или убрать); не включать `AR15` / `M4Commando`.
2. Расширить `SQUAD_REMAP` / wiring `InitialSquads` под vanilla HotDiamonds sector lists → jazz-units defs.
3. Ужесточить gear refresh: ammo к `weapon.Caliber` через `GetAmmosWithCaliber`, не оставлять ванильный ammo loot.
4. Опционально: фильтр контейнеров — не добавлять классы с `comment = "Убираем"` / `Icon` → `TEST.png` / `DisplayName` ОТКЛЮЧЕНО.
5. Runtime: один проход I2 — выписать `item.class` для `test`-тайлов и для Hi-Power ammo.

## Evidence

- Discord скрины: инвентарь отряда «Чарли», схрон/трупы/сундук сектор I2.
- Static: `jazz-nomaps` LootDef/fallback; `InventoryItem/_9mm_Basic.lua` → `TEST.png`; `MP5.lua` / `AR15.lua` → «Убираем».
- Static: `HiPower.Caliber = JAZZ_Caliber_9x19`.
