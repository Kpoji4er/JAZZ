# Инвентарь, предметы, loot и crafting

## Назначение и эффект для игрока

JAZZ расширяет инвентарь специализированными слотами и вкладками, перерабатывает перемещение/перезарядку, контейнеры и squad bag, добавляет сотни предметов, таблицы добычи и рецепты. Система соединяет все четыре пакета: core определяет классы и предметы, units — loadouts/loot, maps — размещение, assets — entities/icons.

## Происхождение по слоям

| Слой | Вклад |
|---|---|
| Vanilla | Inventory, item classes, slots, drag/drop, reload, containers, squad bag, loot и crafting APIs |
| CommonLib | Изменяет `Unit:EnumUIActions`, который затем заменяет JAZZ; это влияет на доступные inventory/combat UI actions |
| JAZZ | Заменяет части Inventory/InventoryUI, добавляет слоты/ограничения, контейнерные NetSync events, loot schemas, drops, recipes и UI |

## Реализация и load-state

Загружаются:

- `Code/Inventory.lua` — крупная модификация vanilla Inventory;
- `Code/InventoryUI.lua` — UI, rollover и drag/drop;
- `Code/System_UnitInventory.lua` — slot schema, вместимость и ограничения;
- `Code/System_Vest.lua` — vest classes при неактивном отдельном Vest slot;
- `Code/System_OR_ItemContainer.lua` — контейнеры, открытие и NetSync;
- `Code/System_OR_SquadBag.lua` — squad bag и перенос при изменении состава;
- `Code/System_LootDef.lua` — расширения loot definitions;
- `Code/System_LootDrops.lua` — runtime выпадения;
- `Code/GetScrapParts.lua` — разбор оружия;
- `Code/AmmoRolloverHint.lua` — ammo tooltip;
- generated InventoryItem, InventoryTab, LootDef, RecipeDef и CraftOperationsRecipe.

## Слоты и вместимость

Unit inventory schema включает:

- общие: `Inventory`, `InventoryDead`, `Pick`;
- руки: `Handheld A`, `Handheld B`;
- экипировку: `Head`, `HeadGear`, `ArmorPlate`, `Torso`, `Legs`, `SetpieceWeapon`;
- специализированные: `AmmoInventory`, `GrenadesInventory`, `OrdnanceInventory`, `MedicalInventory`, `PocketInventory`, `KnifeInventory`.

Вместимость части слотов вычисляется из характеристик и perks. Reload берёт патроны только из `AmmoInventory`; наличие ammo в другом допустимом контейнере не гарантирует возможность перезарядки. Четыре `InventoryTab`: `Grenades`, `Meds`, `Melee`, `resources`.

`InventoryVest` существует, однако Vest slot закомментирован. Его нельзя документировать как активную пользовательскую ячейку до изменения metadata/code и save migration.

## Предметный каталог

Snapshot core содержит 558 InventoryItem definitions:

- 135 Ammo;
- 129 Armor;
- 25 MiscItem;
- крупные оружейные семейства, перечисленные в [оружейной системе](weapons-ammo-components.md);
- 15 Ordnance, 13 QuestItem, 12 ArmorPlate, 10 ThrowableTrap, 8 GrenadeItem, 5 Machete и другие классы.

Схема предмета может включать custom weapon/armor resource, stats, component slots, entity, icon, sound/FX IDs, loot category, repair/craft behavior и localization. Изменение ID требует поиска по четырём пакетам.

## Loot

В `jazz-units` зарегистрировано 1257 `LootDef`; они формируют loadouts и drops для 179 UnitData и squads. В `jazz-maps` есть 18 map/campaign loot definitions и размещённые контейнеры. Core добавляет классы и runtime выпадения.

`System_OR_ItemContainer.lua` реагирует на `LockpickableBrokeOpen` и `DamageDone`, а открытие проходит через NetSync event `OpenContainer`. `System_OR_SquadBag.lua` реагирует на `MercHireStatusChanged` и `PreSquadDespawned`, поэтому изменение переноса предметов затрагивает найм, увольнение, смерть/деспавн и сетевую синхронизацию.

`UtilityFunc.lua` при открытии satellite view регенерирует loot Legion; это cross-cutting стратегический side effect и должно проверяться вместе со strategy docs.

## Crafting и разбор

Зарегистрировано 49 `CraftOperationsRecipe`, преимущественно для ammo и mortar/ordnance, и 33 `RecipeDef`, преимущественно armor transformations. Scrap зависит от weapon methods; внутри JAZZ есть несколько определений `FirearmBase:GetScrapParts`, поэтому итоговое поведение задаётся load order.

## Runtime flow контейнера

1. Карта или unit loot создаёт item instances из definitions.
2. Container/squad inventory хранит экземпляры и состояние ресурса.
3. UI проверяет тип, slot rules, вместимость и conflicts.
4. Перемещение/открытие, когда требуется, синхронизируется NetSync event.
5. Damage, death, despawn, hire-status и переходы карты могут переносить или выбрасывать содержимое.
6. Savegame сериализует экземпляры и их custom properties.

## Совместимость

- Inventory и InventoryUI — крупные изменённые vanilla-файлы.
- `Unit:EnumUIActions` имеет цепочку vanilla → CommonLib → JAZZ.
- Slot names и instance properties являются savegame surface.
- Generated definitions нельзя править только в одной сериализованной копии.
- Неполная установка четырёх пакетов даёт отсутствующие entity/item/loot references.

## Проверка

- drag/drop между каждой парой совместимых/несовместимых слотов;
- reload при ammo в правильном и неправильном slot;
- вместимость при разных stats/perks;
- head/face/plate conflicts и разрушение plate;
- контейнер: lockpick, break, damage, open, multiplayer;
- squad bag при найме, увольнении, смерти, split/join и despawn;
- loot unit/map, Legion regeneration, новый game и existing save;
- craft/scrap с сохранением item resource и components;
- rollover для ammo/armor/weapon.

## Сопровождение

Новый item, slot, recipe или LootDef должен получить владельца в этой странице или профильной системе. Любое изменение схемы экземпляра/слотов обновляет compatibility и save/load tests.