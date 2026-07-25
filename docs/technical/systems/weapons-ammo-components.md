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
- generated InventoryItem, Caliber, WeaponType, WeaponComponent, WeaponComponentEffect, WeaponPropertyDef и recipe ModItems.

## Снимок данных

В core-пакете зарегистрировано 558 `InventoryItem` definitions. Крупные оружейные семейства: 24 pistol, 24 SMG, 18 assault rifle, 17 sniper rifle, 14 battle rifle, 13 carbine, 13 revolver, 12 shotgun, 10 machine gun, 9 LMG, 6 autopistol и 4 grenade launcher. Также присутствуют ammo, armor, ordnance, misc/quest items и melee.

Определены 12 типов оружия: `AR`, `Autopistol`, `BattleRifle`, `Carbine`, `CompactSMG`, `LMG`, `MG`, `Pistol`, `Revolver`, `Shotgun`, `SMG`, `Sniper`; 27 калибров; 236 `WeaponComponent`; 64 `WeaponComponentEffect`; 14 `WeaponPropertyDef`.

Публичные weapon properties:

- `Recoil`, `MaxAimActions`;
- `BurstShots`, `AutoShots`, `OverwatchAngle`, `Handling`;
- `WeaponRange`, `BulletDropRange`, `Grouping`;
- `BaseJamChance`, `PenetrationBonus`;
- `WeaponResource`, `WeaponResourceMax`, `DegradePerShot`;
- `WeaponName`, `WeaponIconMod`, reticle images и `UnitSubStat`.

В актуальном документальном контракте используются 13 weapon property definitions: `AimAccuracy`, `AutoShots`, `BaseDamage`, `BulletDropRange`, `BurstShots`, `Damage`, `Grouping`, `Handling`, `MaxAimActions`, `Noise`, `OverwatchAngle`, `Recoil`, `WeaponRange`.

## Канонический каталог

Полная таблица 160 технических weapon ID, 157 активных игроковых записей, balance-tier, характеристик и слотов находится в [каноническом каталоге оружия](../weapons/README.md). Тиры из профильных Google Sheets были использованы только для первичной миграции и выявили 25 расхождений с Lua-комментариями; после миграции источником истины является CSV. AR15, M4Commando и базовый MP5 отмечены как excluded_disabled и не публикуются в wiki.

## Компоненты

64 effects покрывают:

- barrel/range/grouping/handling/recoil и base damage;
- bipod setup и позиционную эффективность;
- BMG/caliber и penetration;
- burst/automatic/run-and-gun варианты;
- aim actions, aim accuracy и максимальное прицеливание;
- число выстрелов и AP-стоимость;
- магазины, scopes, lasers, silencers и muzzle devices;
- folding stock и two-handed состояние.

`Systems_Compontents_FoldingStocks.lua` добавляет `zzFoldingPair`; runtime использует `zzStockEquipped` и actions `FoldStock`/`UnFoldStock`. Эти имена являются межфайловым контрактом generated components, UI и визуального состояния entity.

## Ресурс, кучность и износ

`WeaponResource` ограничен `WeaponResourceMax`. `DegradePerShot` уменьшает состояние после выстрелов. Текущая `Grouping` масштабируется состоянием и repair multiplier, поэтому повреждение сначала ухудшает дальний CTH, а затем повышает вероятность jam/поломки.

Базовая часть jam chance:

```text
raw_jam = ((100 - Reliability) + BaseJamChance) × degrade_multiplier
```

`degrade_multiplier` меняется ступенчато и резко усиливается при состоянии не выше 80, 60, 40 и 15. Дождь добавляет модификатор; навык стрелка и Mechanical уменьшают риск. Jam/unjam способен необратимо снизить максимальный ресурс или окончательно сломать оружие. Поэтому refactor обязан сохранять не только итоговый процент, но и порядок проверок, RNG и побочные изменения экземпляра.

## Боеприпасы и crafting

Ammo ModItems наследуют `Ammo`; rollover выводит модификации и effects, а reload использует специализированный `AmmoInventory`. Зарегистрированы 49 `CraftOperationsRecipe` для боеприпасов и mortar/ordnance и 33 `RecipeDef`, главным образом преобразования брони. Категории Bobby Ray включают 10 ammo subcategories.

## Дубли и порядок загрузки

Внутри JAZZ повторно определяются `FirearmBase:GetScrapParts` и связанные методы состояния. `GrenadeLauncher:GetBaseDegradePerShot`, `RocketLauncher:GetBaseDegradePerShot` и `Mortar:GetBaseDegradePerShot` сначала появляются в `System_OR_Grenade.lua`, затем в `WeaponClasses.lua`; итог задаёт более поздний файл metadata. Это намеренная зона осторожного рефакторинга: сначала зафиксировать реально активное тело, затем переносить без изменения поведения.

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
- scrap и crafting recipes;
- save/load экземпляра с неполным и уменьшенным максимальным ресурсом;
- AI с модифицированным оружием.

## Сопровождение

При изменении свойств, component effects, калибров, jam/degrade или generated items обновлять эту страницу, [гайд по оружию и боеприпасам](../../wiki/weapons-and-ammo.md), соответствующие таблицы data snapshot и тесты. Для изменений duplicated methods обязательно проверить `metadata.lua`.
