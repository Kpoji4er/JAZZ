# Оружие, боеприпасы и компоненты

## Назначение и эффект для игрока

JAZZ превращает оружие из набора vanilla-статов в систему индивидуальной баллистики, ресурса состояния, надёжности и компонентов. Кучность, дальность, recoil, число выстрелов, стоимость действий, углы overwatch и модификации зависят от класса и конфигурации конкретного экземпляра.

## Происхождение по слоям

| Слой | Вклад |
|---|---|
| Vanilla | `Firearm`, `Weapon`, `Ammo`, component slots/effects, jam/degrade, attack API и InventoryItem serialization |
| CommonLib | Даёт общие mod helpers и исправления, но в проверенном срезе нет подтверждённой одноимённой коллизии с центральными weapon-resource методами JAZZ |
| JAZZ | Добавляет свойства, классы, калибры, предметы, component effects, ресурс/износ, собственную jam-формулу, scrap и рецепты |

## Реализация и load-state

Загружаемые файлы `jazz`:

- `Code/System_Firearm_AddProperties.lua` — свойства firearm и расчётные helpers;
- `Code/System_OR_Weapons.lua` — расширенная runtime-логика оружия, износ и заклинивание;
- `Code/WeaponClasses.lua` — grenade/rocket/mortar и другие weapon class extensions;
- `Code/Systems_Compontents_FoldingStocks.lua` — свойства пары складного приклада;
- `Code/GetScrapParts.lua` — scrap-значения;
- `Code/AmmoRolloverHint.lua` — UI эффектов и модификаций патронов;
- `Code/Inventory.lua` и `Code/InventoryUI.lua` — применение предметов/боеприпасов;
- `Code/WeaponIconBake.lua` — JAZZ-UI-001 side-view bake иконок оружия с аттачами (`GetItemUIIcon`, fingerprint cache);
- generated InventoryItem, Caliber, WeaponType, WeaponComponent, WeaponComponentEffect, WeaponPropertyDef и recipe ModItems.

## Снимок данных

В core-пакете зарегистрировано 558 `InventoryItem` definitions. Крупные оружейные семейства: 24 pistol, 24 SMG, 18 assault rifle, 17 sniper rifle, 14 battle rifle, 13 carbine, 13 revolver, 12 shotgun, 10 machine gun, 9 LMG, 6 autopistol и 4 grenade launcher. Также присутствуют ammo, armor, ordnance, misc/quest items и melee.

Определены 11 типов оружия: `Pistol`, `Autopistol`, `Revolver`, `SMG`, `AssaultRifle`, `Carbine`, `BattleRifle`, `Shotgun`, `LightMachineGun`, `MachineGun`, `Sniper`; 27 калибров; 236 `WeaponComponent`; 64 `WeaponComponentEffect`; 13 `WeaponPropertyDef`.

Устаревшие `CompactSMG` и `CompactSubmachineGun` удалены, а компактные образцы входят в единый класс `SMG` / `SubmachineGun`. `LightMachineGun` соответствует лёгкому пулемёту, а `MachineGun` — тяжёлому/позиционному. Назначение, компромиссы и будущие перковые действия всех классов зафиксированы в [ролях классов оружия](../weapons/class-roles.md).

Публичные weapon properties:

- `Recoil`, `MaxAimActions`;
- `BurstShots`, `AutoShots`, `OverwatchAngle`, `CloseRange`, `CloseRangeFactor`;
- `WeaponRange`, `BulletDropRange`, `Grouping`;
- `BaseJamChance`, `PenetrationBonus`;
- `WeaponResource`, `WeaponResourceMax`, `DegradePerShot`;
- `WeaponName`, `WeaponIconMod`, reticle images и `UnitSubStat`.

В актуальном документальном контракте используются 12 weapon property definitions: `AimAccuracy`, `AutoShots`, `BaseDamage`, `BulletDropRange`, `BurstShots`, `Damage`, `Grouping`, `MaxAimActions`, `Noise`, `OverwatchAngle`, `Recoil`, `WeaponRange` (плюс JAZZ-only `CloseRange` / `CloseRangeFactor` на FirearmProperties).

В [модели стрельбы](../weapons/accuracy-model.md) `Handling` **удалён**. `Recoil` задаёт тяжесть множительного удержания точности последующих пуль. Оптика переносит эффективную прицельную зону через aim progress, не увеличивает физическую дальность и больше не получает старые плоские CTH-effects.

Вырезанные, но всё ещё загруженные классы (`MP5`/`AR15`/`M4Commando`, vanilla `_*` ammo с `Ammopics/TEST.png`) перечислены в [вырезанном контенте](../weapons/cut-content.md). Их нельзя использовать в луте/магазине; живые калибры — только `JAZZ_Caliber_*` / `JAZZ_AMMO_*`.

## Канонический каталог

Полная таблица 160 технических weapon ID, 157 активных игроковых записей, balance-tier, характеристик и слотов находится в [каноническом каталоге оружия](../weapons/README.md). Тиры из профильных Google Sheets были использованы только для первичной миграции и выявили 25 расхождений с Lua-комментариями; после миграции источником истины является CSV. AR15, M4Commando и базовый MP5 отмечены как excluded_disabled и не публикуются в wiki.

## Компоненты

Канонические связи компонентов и эффектов находятся в `docs/technical/weapons/data/weapon-components.csv` и `weapon-component-effects.csv`. Runtime сначала использует resolved свойства оружия, поэтому component modifier `Recoil` не умножается второй раз при построении recoil profile.

Текущий working-tree snapshot содержит 50 mod-owned `WeaponComponentEffect` и 190 component records (включая 13 `vanilla_ref` stubs, нужных для join каталога). Живые JAZZ components и effects выгружаются из `items.lua`, а их option wiring — из `InventoryItem/*.lua`.

Эффекты покрывают:

- barrel/range/grouping/recoil, базовый урон и `CloseRange*`;
- bipod setup и позиционную эффективность;
- BMG/caliber и penetration;
- burst/automatic/run-and-gun варианты;
- aim actions, aim accuracy и максимальное прицеливание;
- число выстрелов и AP-стоимость;
- магазины, scopes, lasers, silencers и muzzle devices;
- folding stock и two-handed состояние.

`Systems_Compontents_FoldingStocks.lua` добавляет `zzFoldingPair`; runtime использует `zzStockEquipped` и actions `FoldStock`/`UnFoldStock`. Эти имена являются межфайловым контрактом generated components, UI и визуального состояния entity.

После JAZZ-ATTACH-001 live components больше не используют `*Handling*` или `Cumbersome` effect presets; Firearm property `Handling` удалён вместе с UI/GameTerm/CTH-modifier presets. Все модифицируемые live component IDs, созданные JAZZ, используют канонический префикс `JAZZ_`; сохранённые `vanilla_ref` stubs отражают ссылки companion-файлов без JAZZ definition и не получают выдуманных effects. Четыре pure-ergo components (`JAZZ_TacGrip`, `JAZZ_Handgrip_Ergo`, `JAZZ_SigErgoHandGrip`, `JAZZ_HandlingWrap`) теперь дают `RecoilDecrease`.

## Inventory icons (JAZZ-UI-001)

Path **B** (chips): template `Icon` оружия не подменяется. Chip column (VList, left edge): `ChipIcon` → иначе `Icons/Upgrades/Chips/<id>.png` если файл есть → иначе `slot_*`. **Не** использовать `WeaponComponent.Icon` как chip (это art кабинета).

- Chip PNG: `Icons/Upgrades/Chips/<ComponentId>.png` → `Mod/e6L4ECj/Icons/Upgrades/Chips/<…>.png`
- Full кабинет: `Icon` (vanilla `UI/Icons/Upgrades/…` или `Icons/Upgrades/Full/`) — skill `$create-jazz-component-icons`
- Chip миниатюры — skill `$create-jazz-chip-icons`
- Runtime: `Code/WeaponAttachChips.lua` + hooks в `InventoryUI.lua`; bake (`WeaponIconBake.lua`) dormant (`JazzWeaponIcon_BakeEnabled = false`)
- Показ: non-default **или** default + `CanBeEmpty` + `ModificationEffects` (как `CountWeaponUpgrades` — builtin flashlight на MP5A4)
- Порядок (priority): Scope → Side* → Under → Muzzle → …; layout **VWrap** (до **3** в левом столбце, 4-й → второй столбец), size **24px**, margin −4, `JazzAttachChips_Max = 4`
- Mount* слоты не чипуются
- `w_mod` скрывается, когда показан chip column
- Scope/Sights: ChipIcon проставлен для 30 компонентов (2026-07-30)

## Ресурс, кучность и износ

`WeaponResource` ограничен `WeaponResourceMax`. `DegradePerShot` уменьшает состояние после выстрелов. Текущая `Grouping` масштабируется integer condition/repair permille multipliers, поэтому повреждение сначала ухудшает дальний CTH, а затем повышает вероятность jam/поломки.

Jam использует единую шкалу **JamScore** `0..1000` (те же единицы, что `attacker:Random(1000)` в `ReliabilityCheck`). Приведённый процент для UI/ammo rollover: `DivRound(JamScore, 10)`. Окно модификации оружия показывает **Reliability**, не Jam %.

Базовый weapon score (без стрелка):

```text
base = max(0, (100 - Reliability) + BaseJamChance)
JamScore = clamp(base × degrade_multiplier [× rain], 0, 1000)
```

`BaseJamChance` — единицы JamScore (10 ≈ 1% в rollover). `degrade_multiplier` через `elseif` по condition % от weighted resource:

| Condition % | Multiplier |
|---|---|
| > 80 | ×1 |
| ≤ 80 | ×4 |
| ≤ 60 | ×8 |
| ≤ 40 | ×16 |
| ≤ 15 | ×24 |

Mechanical снижает score **пропорционально** (`MulDivRound(score, Mechanical, 120)` у мерков + малый secondary Marks/Wisdom/Level; у AI знаменатель 150). Одиночный выстрел делит score пополам через `DivRound`. `FirearmBase:GetDisplayJamChancePercent(attacker?)` отдаёт приведённый %.

`Handling` («Эргономика») удалён из Firearm / WeaponPropertyDef; CTH-модификатор отсутствует, угол overwatch берётся только из `OverwatchAngle` (`JAZZ-WEAPONS-001` / `JAZZ-ATTACH-001`).

Jam/unjam способен необратимо снизить максимальный ресурс или окончательно сломать оружие. Refactor обязан сохранять шкалу 0..1000, порядок проверок, RNG и побочные изменения экземпляра.

## Боеприпасы и crafting

Ammo ModItems наследуют `Ammo`; rollover выводит модификации и effects (`BaseJamChance` как `%` через `/10`), а reload использует специализированный `AmmoInventory`. Зарегистрированы 49 `CraftOperationsRecipe` для боеприпасов и mortar/ordnance и 33 `RecipeDef`, главным образом преобразования брони. Категории Bobby Ray включают 10 ammo subcategories.

### Пробитие патрона (`PenetrationClass` + `PenetrationBonus`)

Контракт данных и UI (канон skill `.agents/skills/jazz-penetration-scales/SKILL.md`):

```text
tenths = DivRound(mod_mul_or_1000, 100) + mod_add_bonus
display = "W.F"   -- 9 → 0.9, 22 → 2.2
```

Боевой pen: `GetAttackPenetrationClass` = `PenetrationClass + 0.1×PenetrationBonus` — см. [броня/урон](armor-damage-wounds-will.md).

`Ammo:GetRolloverHint` склеивает оба модификатора в одну строку и передаёт **`Untranslated` строку**, не Lua float: подстановка числа в `T{}` усекает к нулю (`0.9` → `0`). Форматтер: `FormatAmmoPenetrationDisplay`.

Не делать `DivRound(mul, 100) * 10 + bonus` (двойной масштаб → 202) и не путать с jam `%` (`/10`).

### Трассерные боеприпасы

Наличие `MarkedTraccers` в `Ammo.AppliedEffects` включает shot-level правило: выбранная unit-цель получает один stack за каждый фактически произведённый выстрел, если итоговый шанс этого выстрела `shot_cth > 0`. Попадание не требуется, поэтому маркер отражает трассирующий/подавляющий огонь; при невозможном выстреле с CTH `0`, jam или отсутствии произведённого выстрела stack не добавляется.

`MarkedTraccers` исключён из обычного `hit.effects`, чтобы попадание не добавляло второй stack. Остальные ammo/body-part effects остаются hit-level и применяются только при отсутствии закрывающей брони либо при её пробитии.

## Дубли и порядок загрузки

Канонические `FirearmBase:GetScrapParts` / `ItemWithCondition:AmountOfScrapPartsFromItem` живут в `GetScrapParts.lua` (грузится после `System_OR_Weapons.lua`). Штраф Condition&lt;50 (`/20`) применяется только в `AmountOfScrapPartsFromItem`. `GrenadeLauncher`/`RocketLauncher`/`Mortar:GetBaseDegradePerShot` в `WeaponClasses.lua` (после `System_OR_Grenade.lua`) возвращают `self.DegradePerShot or const.Weapons.DegradePerShot_*`.

## Межпакетные зависимости

- core item definitions ссылаются на entities и состояния из `jazz_assets`;
- `jazz-units` выдаёт оружие и ammo через UnitData/loot definitions;
- `jazz-maps` размещает оружие, контейнеры и loot;
- sound/FX modules связывают weapon IDs с presets и аудиоресурсами.

Переименование item, caliber, component, effect, slot или entity ID требует поиска во всех четырёх репозиториях.

## Проверка

- состояние 100/80/60/40/15 и ниже; сухая погода/дождь;
- single/burst/auto, unjam, repair и окончательная поломка;
- деградация Grouping и совпадение CTH UI;
- установка/снятие каждого класса компонентов, folded/unfolded визуал;
- reload из правильного ammo slot и отказ для неподходящего калибра;
- ammo rollover: Penetration = `(mod_mul/1000) + (PenetrationBonus/10)` (не целое ×100), jam `%` через `/10`;
- трассерный одиночный/серийный огонь: попадание и промах при CTH больше нуля, CTH `0`, jam и нехватка патронов;
- обычные ammo effects при непробитой и пробитой броне;
- scrap и crafting recipes;
- save/load экземпляра с неполным и уменьшенным максимальным ресурсом;
- AI с модифицированным оружием.

## Сопровождение

При изменении свойств, component effects, калибров, jam/degrade или generated items обновлять эту страницу, соответствующие таблицы data snapshot и тесты. Для изменений duplicated methods обязательно проверить `metadata.lua`. Наблюдаемый игроком current-state контракт фиксируется на этой technical-странице; target behavior — в связанной spec.
