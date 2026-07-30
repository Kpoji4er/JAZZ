# Вырезанный / отключённый контент оружия и патронов

Канон для разработчика: какие `InventoryItem` **оставлены в пакете**, но **не должны** попадать в магазин, лут, стартовые киты и player-facing wiki.

Снимок: static по `InventoryItem/*.lua` и `docs/technical/weapons/data/weapons.csv` (2026-07-30).

## Зачем классы остаются

Vanilla ID нельзя просто удалить: сохранения, map containers, LootDef и чужие моды могут ссылаться на `MP5`, `_9mm_Basic` и т.п. JAZZ **переопределяет** класс (`UndefineClass` → `DefineClass`), помечает его как вырезанный и подменяет игровой контент живыми ID (`MP5A2`, `JAZZ_AMMO_9x19_FMJ`, …).

Если такой предмет всё же оказался в инвентаре — это дефект wiring/лута (типичный пример: [nomaps playtest](../bugs/nomaps-playtest-2026-07-30.md)), а не «пропавшая иконка».

## Как помечено

| Признак | Где | Смысл |
| --- | --- | --- |
| `comment = "Убираем"` | оружие | намеренно выведено из мода |
| `DisplayName` / plural = `ОТКЛЮЧЕНО` (иногда с префиксом имени) | оружие и часть ammo | UI-метка «не использовать» |
| `Icon = "Mod/e6L4ECj/Ammopics/TEST.png"` | vanilla ammo `_*` | **осознанная** метка неиспользуемых патронов (жёлтый квадрат `test`) |
| `Caliber` = vanilla (`9mm`, `556`, `762WP`, …) | cut ammo / cut оружие | не `JAZZ_Caliber_*` |
| `catalog_status = excluded_disabled` | `weapons.csv` | не публикуется в `docs/wiki/weapons/` |

Живые предметы используют `Mod/e6L4ECj/WeaponIcons/…` / нормальные `Ammopics/…` и калибры `JAZZ_Caliber_*`.

## Оружие (`excluded_disabled`)

| ID | Класс | Старый калибр | Чем пользоваться вместо |
| --- | --- | --- | --- |
| `MP5` | `SubmachineGun` | `9mm` | `MP5A2`, `MP5A4`, `MP5K`, `MP5SD` |
| `AR15` | `AssaultRifle` | `556` | линейка `M16A1` / `M16A2` / `M16A4`, карабины `M4A1`, `CAR15`, … |
| `M4Commando` | `SubmachineGun` | `556` | `M4A1` и прочие живые 5.56 карабины/AR |

Файлы: `InventoryItem/MP5.lua`, `AR15.lua`, `M4Commando.lua`. В каталоге CSV те же три строки с `excluded_disabled` (см. [weapons/README.md](README.md)).

**Не путать:** `MP5A2` / `MP5A4` — активный контент JAZZ; вырезан только безымянный vanilla `MP5`.

## Патроны (`Ammopics/TEST.png`)

Все перечисленные классы загружены, но **не часть** боеприпасной экономики JAZZ. Замена — семейство `JAZZ_AMMO_*` на `JAZZ_Caliber_*`.

### По семействам vanilla → JAZZ

| Vanilla prefix / IDs | Vanilla `Caliber` | Актуальный калибр JAZZ | Пример живых ID |
| --- | --- | --- | --- |
| `_9mm_*` (7 шт.) | `9mm` | `JAZZ_Caliber_9x19` | `JAZZ_AMMO_9x19_FMJ`, `_AP`, `_JHP`, `_Match`, `_Poor`, `_Crafted`, `_APP` |
| `_556_*` (5 шт.) | `556` | `JAZZ_Caliber_556` | `JAZZ_AMMO_556_FMJ`, `_AP`, `_Match`, `_Tracer`, `_Army`, … |
| `_762NATO_*` (5 шт.) | `762NATO` | `JAZZ_Caliber_762x51` | `JAZZ_AMMO_762x51_FMJ`, `_AP`, `_Match`, `_Tracer`, … |
| `_762WP_*` (6 шт.) | `762WP` | `JAZZ_Caliber_762x39` | `JAZZ_AMMO_762x39_FMJ`, `_US`, `_Tracer`, `_Army`, … |
| `_44CAL_*` (5 шт.) | `44CAL` | `JAZZ_Caliber_44CAL` | `JAZZ_AMMO_44CAL_FMJ`, `_JHP`, `_Match` |
| `_50BMG_*` (4 шт.) | `50BMG` | `JAZZ_Caliber_50BMG` | `JAZZ_AMMO_50BMG_Basic`, `_APIT`, `_API_HEI` |
| `_12gauge_*` (5 шт.) | `12gauge` | `JAZZ_Caliber_12gauge` | `JAZZ_AMMO_12gauge_Buckshot`, `_Slug`, `_APSlug`, `_Saltshot`, `_Birdshot` |
| `_40mmFlashbangGrenade` | `40mmGrenade` | `JAZZ_Caliber_40mmGrenade` | `JAZZ_AMMO_40mmFlashbangGrenade`, `JAZZ_AMMO_40mmFragGrenade` |

### Полный список cut ammo (38)

| ID | DisplayName (как в Lua) |
| --- | --- |
| `_9mm_Basic` | 9х19 мм, FMJ |
| `_9mm_AP` | 9х19 мм, ББ |
| `_9mm_HP` | 9х19 мм, JHP |
| `_9mm_Match` | 9х19 мм, Match |
| `_9mm_Shock` | 9mm ShockОТКЛЮЧЕНО |
| `_9mm_Subsonic` | 9mmSubsonicОТКЛЮЧЕНО |
| `_9mm_Tracer` | 9mmTracerОТКЛЮЧЕНО |
| `_556_Basic` | 5,56мм, FMJ |
| `_556_AP` | 5,56 мм, M855 |
| `_556_HP` | 5,56 мм, Mk262 |
| `_556_Match` | 556Match ОТКЛЮЧЕНО |
| `_556_Tracer` | 5,56 мм, M856 |
| `_762NATO_Basic` | 7.62х51мм НАТО, M80 |
| `_762NATO_AP` | 7.62х51мм НАТО, M61 |
| `_762NATO_HP` | 7.62х51мм НАТО, FMJ |
| `_762NATO_Match` | 7.62х51мм НАТО, M118LR |
| `_762NATO_Tracer` | 7.62х51мм НАТО, M62 |
| `_762WP_Basic` | 7,62х39мм, ПС |
| `_762WP_AP` | 7,62 мм СССР, Отключено |
| `_762WP_HP` | 7,62х39мм, FMJ |
| `_762WP_Match` | 7.62 mm WP Match |
| `_762WP_Subsonic` | 7,62х39мм, УС |
| `_762WP_Tracer` | 7.62 mm WP Tracer |
| `_44CAL_Basic` | .44, FMJ |
| `_44CAL_AP` | .44, ББ Отключено |
| `_44CAL_HP` | .44, JHP |
| `_44CAL_Match` | .44, Match |
| `_44CAL_Shock` | .44, ШОК Отключено |
| `_50BMG_Basic` | .50 Standard |
| `_50BMG_HE` | .50 Explosive |
| `_50BMG_Incendiary` | .50 Frag |
| `_50BMG_SLAP` | .50 SLAP |
| `_12gauge_Buckshot` | 12-й калибр, дробь |
| `_12gauge_APSlug` | 12-й калибр, ББ Пуля |
| `_12gauge_Breacher` | 12-й калибр, Картечь |
| `_12gauge_Flechette` | 12-й калибр, Пуля |
| `_12gauge_Saltshot` | 12-gauge Saltshot |
| `_40mmFlashbangGrenade` | 40 mm Flashbang |

Итого: **3** оружия + **38** ammo = **41** помеченных cut-классов в этом контракте.

## Правила для кода и лута

1. Не класть cut ID в LootDef, shop, `PlaceInventoryItem`, EnemySquad loot, nomaps packs/fallback.
2. Для калибра оружия всегда брать `JAZZ_AMMO_*` через `GetAmmosWithCaliber(weapon.Caliber, …)`, не `_9mm_Basic`.
3. При появлении жёлтого `test` в инвентаре — искать, **кто** создал класс из таблицы выше; иконку `TEST.png` «чинить» не нужно.
4. Новое вырезание: тот же набор меток + строка `excluded_disabled` в `weapons.csv` (для оружия) + обновление этой страницы в том же change set.
5. Player wiki / showcase cut ID не описывают (уже исключены генератором каталога для трёх оружий).

## Связанные страницы

- [Оружие, боеприпасы и компоненты](../systems/weapons-ammo-components.md)
- [Канонический каталог оружия](README.md) — `catalog_status`
- [Nomaps playtest 2026-07-30](../bugs/nomaps-playtest-2026-07-30.md) — inject cut ammo/`MP5`
