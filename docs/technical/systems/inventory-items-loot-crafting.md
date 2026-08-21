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
- `Code/InventoryUI.lua` — UI, rollover и drag/drop; `XInventorySlot:InternalDragStop` / `OnCaptureLost` clear drag ghost when a handled drop (`true`) or capture loss would otherwise leave the floating item icon on `XDesktop` (vanilla: failed give/use-too-far on big portrait);
- `Code/System_UnitInventory.lua` — slot schema, вместимость и ограничения;
- `Code/System_Vest.lua` — vest classes при неактивном отдельном Vest slot;
- `Code/System_OR_ItemContainer.lua` — контейнеры, открытие и NetSync;
- `Code/System_OR_SquadBag.lua` — squad bag и перенос при изменении состава;
- `Code/System_InventoryStacks.lua` — dual stack limits (storage vs loadout, JAZZ-INV-001);
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

Вместимость специализированных слотов мерка (`UnitProperties:GetInventoryMaxSlots` в `Code/System_UnitInventory.lua`) — от характеристик/perks, без blanket floor:

| Slot | Merc formula |
|---|---|
| `Inventory` | `Max(4, (Strength-30)/5)` |
| `AmmoInventory` | `Max(1, (Marksmanship+Strength-60)/30)` +2 AutoWeapons / +2 HeavyWeaponsTraining |
| `GrenadesInventory` | `Max(0, (Explosives-10)/20)` |
| `OrdnanceInventory` | `Max(0, (Explosives-70)/10)` |
| `MedicalInventory` | `Max(0, (Medical-20)/20)` — медик-роль; 0 у низкого Medical |
| `PocketInventory` | `Max(0, (Mechanical-30)/20)` |
| `KnifeInventory` | +1 NightOps/Stealthy, +1 Throwing |

`EquipStartingGear` делает несколько `TryEquip` в эти ряды, но **не** расширяет вместимость: лишние Medicine/ToolItem уходят в общий `Inventory`. Стеки `JazzStackableMedicine`: Bandage **30**, Morphine **10**, Small Medkit **5**, Medium Medkit **10**, Large Medkit **15** (1 юз = 1 штука).

Reload берёт патроны только из `AmmoInventory`; наличие ammo в другом допустимом контейнере не гарантирует возможность перезарядки. Выстрелы RPG-7 (`Warhead_Frag`) лежат в рюкзаке (`Inventory`), не в `OrdnanceInventory` (тот ряд — только ловушки/C4). Опустошённый стек снимается из фактического слота (`GetItemSlot`); `Amount<=0` не даёт Reload и не тратит ОД. Четыре `InventoryTab`: `Grenades`, `Meds`, `Melee`, `resources`.

`InventoryVest` существует, однако Vest slot закомментирован. Его нельзя документировать как активную пользовательскую ячейку до изменения metadata/code и save migration.

### Stack limits (JAZZ-INV-001)

| Контейнер | Effective max | UI на тайле |
|---|---|---|
| Unit slots / разгрузка | personal `MaxStacks` (InventoryItem def) | `Amount/MaxStacks` |
| `SquadBag`, `SectorStash` | `const.JazzStorageStackMax` = `10000` | только `Amount` (без `/max`) |

Реализация: `Code/System_InventoryStacks.lua` (`JazzGetStackMax` / `JazzApplyStackContext` / `JazzInventoryItemsCanStack`) + merge/`CanAddItem`/bag-sort/AddItem hooks. Файл должен быть **и** `ModItemCode` в `items.lua`, **и** в `metadata.code`: иначе editor `SaveDef` выкидывает его (Steam 0.19-6183 → assert `JazzApplyStackContext`). В storage instance `MaxStacks` поднимается до storage cap (чтобы vanilla `MoveItem` считал стек верно); при переносе в unit восстанавливается personal max. Перенос склад→мерк заливает до personal max, остаток остаётся на складе. Если стек в разгрузке всё же шире personal max (`160/120`), лишнее **уходит в сумку отряда**, а не удаляется (`JazzSpillPersonalStackExcess` на LoadGame / AddItem / MoveItem). `InventoryStack:MergeStack` в разгрузке всегда режет по personal max, даже если у instance застрял складской cap 10000. UI amount-only также в `InventoryStack:GetItemSlotUI` (`System_OR_Weapons.lua`): `JazzIsStorageStackUI` смотрит фактическое членство в bag/stash, не сырой `MaxStacks==10000`.

**HOTFIX-005 (remountable stacks):** одинаковые съёмные модули (один `RemovableComponentId`, напр. несколько `JAZZ_Bipod`) стекаются в SquadBag/SectorStash. Разные ID (коллиматор + компенсатор, даже на generic class) не сливаются. `JazzMarkSquadBagData` / `JAZZ_NormalizeRemovableAttachmentStack` **не** обрезают `Amount` до 1 — раньше сортировка сумки склеивала N сошек в один стек, затем клип удалял N−1. Уже потерянные в старых сейвах предметы не восстанавливаются. На мерке personal `MaxStacks=1` (по def).

Known issue (не data loss): плавающее **визуальное** пропадание тайлов в SquadBag до регенерации UI bag; данные `squad_bag` сохраняются.

### Reload: return ejected ammo

Вынутый магазин: merge в стеки `AmmoInventory`/`OrdnanceInventory` мерка; остаток — `GetDropContainer` под ноги (не squad bag). Satellite без tactical unit — sector inventory. Дозарядка берёт стеки того же класса по убыванию `Amount`.

### Combat HUD: change ammo type

Vanilla `GetQuickReloadWeaponAndAmmo` отключает quick-reload при полном магазине, если есть другой тип (`FullClipHaveOther`). JAZZ (`Code/InventoryUI.lua` + `UIWeaponDisplay`): кнопка Reload активна; клик открывает тот же текстовый `InventoryContextSubMenu`, что и в инвентаре (`<ammo_type>(<count>)`), якорь — над оружием / кнопкой Reload.

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

`UtilityFunc.lua` при открытии satellite view регенерирует loot Legion; это cross-cutting стратегический side effect и должно проверяться вместе со strategy docs. Боевые Legion starting LootDef после JAZZ-UNITS-003 владеет generator `jazz/scripts/legion-loadouts/` → `jazz-units/items.lua` (см. [`legion-units-equipment-tiers.md`](legion-units-equipment-tiers.md)).

## Crafting и разбор

Зарегистрировано 49 `CraftOperationsRecipe`, преимущественно для ammo и mortar/ordnance, и 33 `RecipeDef`, преимущественно armor transformations. Scrap зависит от weapon methods; внутри JAZZ есть несколько определений `FirearmBase:GetScrapParts`, поэтому итоговое поведение задаётся load order. `ScrapItem` перед уничтожением ствола вызывает `JAZZ_EjectRemovableAttachmentsForScrap`: съёмные модули копируются в сумку отряда **без** `SetWeaponComponent` (иначе SCRAP ALL по заряженному луту падает на `ReloadWeapon`).

`JAZZ_BarrelParts` — stackable `ResourceItem` для barrel install/repair; `JAZZ_ScopeParts` — repair surcharge при remountable Scope + salvage при break на провале снятия. Runtime resource registry добавляет оба как additional sector resources. Quoted craft/`AdditionalCosts` в `items.lua` уже remapped (`FineSteelPipe`→`JAZZ_BarrelParts`, `OpticalLens`/`Microchip`→`Parts`). Legacy ModItem defs оставлены dormant (`CanAppearInShop = false`) для load-migrate стеков; companions синхронизированы. Полное удаление defs — editor purge после wave acceptance.

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
- `const.InventoryGiveDistance` = `4800` (`voxelSizeX`) — намеренно короче vanilla `24000`.
- XTemplate `SquadsAndMercs` (активный party panel для `Inventory`): `OnDrop` на HUDMerc только `SelectUnit()` — не подменять логикой «use item» с большого портрета.

## Проверка

- drag/drop предмета на иконку другого мерка в party panel (`SquadsAndMercs`): runtime PASS (owner, 2026-07-30) — `OnDrop` = `SelectUnit()` only; `InventoryGiveDistance` = `4800`;
- failed give/use (too far / disabled) must not leave a floating item icon on the tactical view — `InternalDragStop` clears on handled `true` drops that skip `OnDragDrop`; `OnCaptureLost` uses `CancelDragging` instead of bare `StopDrag`;
- drag/drop между каждой парой совместимых/несовместимых слотов;
- reload при ammo в правильном и неправильном slot;
- вместимость при разных stats/perks;
- head/face/plate conflicts и разрушение plate;
- контейнер: lockpick, break, damage, open, multiplayer;
- squad bag при найме, увольнении, смерти, split/join и despawn;
- HOTFIX-005: несколько одинаковых сошек в имуществе отряда переживают sort + save/load; коллиматор и компенсатор не сливаются;
- loot unit/map, Legion regeneration, новый game и existing save;
- craft/scrap с сохранением item resource и components;
- rollover для ammo/armor/weapon.

## Сопровождение

Новый item, slot, recipe или LootDef должен получить владельца в этой странице или профильной системе. Любое изменение схемы экземпляра/слотов обновляет compatibility и save/load tests.