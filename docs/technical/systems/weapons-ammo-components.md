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

- `Code/System_Firearm_AddProperties.lua` — свойства firearm, расчётные helpers и `JAZZ_GetWeaponCloseRangeRolloverTexts` для строки ближней зоны на карточке;
- `Code/System_OR_Weapons.lua` — расширенная runtime-логика оружия, износ и заклинивание;
- `Code/System_EmplacementAmmo.lua` — `MachineGunEmplacement:Update` remaps cut `_50BMG_*` `ammo_template` → `JAZZ_AMMO_50BMG_*` (и generic caliber mismatch → `GetAmmosWithCaliber`); **HOTFIX-004:** wrap `Unit:EnterEmplacement` (no `SetPos(nil)` if weapon/visual missing) + delayed `LoadGame`/`EnterSector` reseat (`Jazz_ReseatMannedEmplacements`: bind weapon, HUD, Idle `MGTarget` cone);
- `Code/System_WeaponResourceMaintenance.lua` — JAZZ-WEAPONS-002 late override: resource helpers, max-wear, jam type (no `GetRolloverHint` jam append), removable `JAZZ_RemovableAttachment` create/API (`JAZZ_ResolveRemovableComponentId` vanilla↔`JAZZ_` twins; `JAZZ_CreateRemovableAttachment` prefers catalog class `Id == component id`), remove-fail break (`P=Clamp(100−resourcePct,0,95)` → ScopeParts salvage / destroy), presentation sync, **rollover title** = compatible weapon DisplayNames + component name (`JAZZ_FormatCompatibleWeaponsForTitle`), install/remove Mech = best-in-squad (`JAZZ_GetSquadMechanical`); repair debits `JAZZ_BarrelParts` + `JAZZ_ScopeParts` when remountable Scope installed; `JAZZ_IsRemovableWeaponComponent` excludes irons / MagNormal / `*SuppressorIntegrated` (integral muzzle stays on scrap); **scrap eject** clones remountables into the bag **without** `SetWeaponComponent` (loaded loot + Magazine unload/`ReloadWeapon` on `weapon.owner` aborted SCRAP ALL); **`GetSpecialScrapItems`** returns only `AdditionalCosts` of `JAZZ_BarrelParts`/`JAZZ_ScopeParts` (never `component.Cost` — that is install Parts price);
- `items.lua` `RolloverInventoryWeaponBase` — UI «Шанс Клина» (`GetDisplayJamChancePercent`) и «Ближняя зона» (`JAZZ_GetWeaponCloseRangeRolloverTexts`: resolved−base Factor boost или штраф базы);
- `Code/System_WeaponRemovableModify.lua` — ModifyWeapon/DnD remountables; fold craft filter (`*Folded` без `UnFolded` скрыт в popup); Unfolded↔Folded swap бесплатно; `GetWeaponComponentDescription` всегда показывает DisplayName и для опций без эффектов — «базовый вариант» вместо голого «Без изменений»;
- `Code/System_InventoryStacks.lua` — **HOTFIX-005:** identical remountables (same `RemovableComponentId`) stack in SquadBag/SectorStash; mixed IDs never merge (`JazzInventoryItemsCanStack`). Do not clip `Amount` to 1 on load/sort (that deleted extra bipods). Personal loadout still uses def `MaxStacks=1`;
- generated `InventoryItem/<JAZZ_*>.lua` remountable catalog (~144) + folder `RemovableAttachments` in `items.lua` (editor spawn); refresh: `docs/tools/_gen_removable_attachment_items.py --apply`; **Bobby Ray temp:** `CanAppearInShop=true` RestockWeight=10 MaxStock=1 Tier=1 via `_enable_remountable_bobby_ray.py` (skip integ suppressor);
- `InventoryItem/JAZZ_ScopeParts.lua` — детали прицелов (лом / repair surcharge);
- `Code/WeaponClasses.lua` — grenade/rocket/mortar и другие weapon class extensions;
- `Code/Systems_Compontents_FoldingStocks.lua` — свойства пары складного приклада;
- `Code/GetScrapParts.lua` — scrap-значения;
- `Code/AmmoRolloverHint.lua` — UI эффектов и модификаций патронов;
- `Code/Inventory.lua` и `Code/InventoryUI.lua` — применение предметов/боеприпасов; **`HighlightWeaponsForAmmo`** также подсвечивает совместимое оружие для `JAZZ_RemovableAttachment` (hover + drag, включая магазины);
- `Code/WeaponAttachChips.lua` — JAZZ-UI-001 path B chips на тайле/HUD; `Code/WeaponIconBake.lua` **dormant** (не в `metadata.code`, не перехватывает `g_HgnvCompressPath`);
- generated InventoryItem, Caliber, WeaponType, WeaponComponent, WeaponComponentEffect, WeaponPropertyDef и recipe ModItems.

## Снимок данных

В core-пакете зарегистрировано 558 `InventoryItem` definitions. Крупные оружейные семейства: 24 pistol, 24 SMG, 18 assault rifle, 17 sniper rifle, 14 battle rifle, 13 carbine, 13 revolver, 12 shotgun, 10 machine gun, 9 LMG, 6 autopistol и 4 grenade launcher. Также присутствуют ammo, armor, ordnance, misc/quest items и melee.

Определены 11 типов оружия: `Pistol`, `Autopistol`, `Revolver`, `SMG`, `AssaultRifle`, `Carbine`, `BattleRifle`, `Shotgun`, `LightMachineGun`, `MachineGun`, `Sniper`; 27 калибров; 236 `WeaponComponent`; 64 `WeaponComponentEffect`; 13 `WeaponPropertyDef`.

Устаревшие `CompactSMG` и `CompactSubmachineGun` удалены, а компактные образцы входят в единый класс `SMG` / `SubmachineGun`. `LightMachineGun` соответствует лёгкому пулемёту, а `MachineGun` — тяжёлому/позиционному. Назначение, компромиссы и будущие перковые действия всех классов зафиксированы в [ролях классов оружия](../weapons/class-roles.md).

Публичные weapon properties:

- `Recoil`, `MaxAimActions`;
- `BurstShots`, `AutoShots`, `WeaponMass`, `CyclicRPM`, `WeaponSizeClass`, `BurstLimiter`, `OverwatchAngle`, `CloseRange`, `CloseRangeFactor`;
- `BuckshotProjectiles` — база числа дробин на патрон для `Shotgun` (JAZZ-WEAPONS-006; ammo `CaliberModification`, не путать с `AutoShots`);
- `WeaponRange`, `BulletDropRange`, `Grouping`;
- `BaseJamChance`, `PenetrationBonus`;
- `WeaponResource`, `WeaponResourceMax`, `DegradePerShot`;
- `ReloadStyle`: `Magazine` (default), `Tube`, `Break` or `Revolver`;
- `DisposableLauncher`, `EmbeddedOrdnance` (только `RocketLauncher`: одноразовая пусковая и её встроенный ordnance);
- `WeaponName`, `WeaponIconMod`, reticle images и `UnitSubStat`.

В актуальном документальном контракте используются 12 weapon property definitions: `AimAccuracy`, `AutoShots`, `BaseDamage`, `BulletDropRange`, `BurstShots`, `Damage`, `Grouping`, `MaxAimActions`, `Noise`, `OverwatchAngle`, `Recoil`, `WeaponRange` (плюс JAZZ-only `CloseRange` / `CloseRangeFactor` / `BuckshotProjectiles` на FirearmProperties). `ModifyWeaponDlg` (`GetWeaponModifyProperties`) показывает `Recoil`/`BurstShots`/`AutoShots` при `CanBurstfire`/`CanAutofire` или authored shot counts > 0, а не только когда `GetBaseAttack` уже Auto/Burst.

В [модели стрельбы](../weapons/accuracy-model.md) `Handling` **удалён**. `Recoil` задаёт тяжесть множительного удержания точности последующих пуль и authorится из `WeaponMass` (десятые кг), `CyclicRPM` и `WeaponSizeClass`; они не читаются повторно в CTH runtime. `BurstShots`/`AutoShots` фиксированно выводятся из RPM при authoring (`/200`, `/100`) и `BurstLimiter` ограничивает только burst. Число дробин — `BuckshotProjectiles` (база 1 на стволе; картечь ×9, birdshot/salt ×20). Оптика переносит эффективную прицельную зону через aim progress, не увеличивает физическую дальность и больше не получает старые плоские CTH-effects.

Вырезанные, но всё ещё загруженные классы (`MP5`/`AR15`/`M4Commando`, vanilla `_*` ammo с `Ammopics/TEST.png`) перечислены в [вырезанном контенте](../weapons/cut-content.md). Их нельзя использовать в луте/магазине; живые калибры — только `JAZZ_Caliber_*` / `JAZZ_AMMO_*`.

## Канонический каталог

Полная таблица 164 технических weapon ID, 161 активную игроковую запись, balance-tier, характеристик и слотов находится в [каноническом каталоге оружия](../weapons/README.md). Тиры из профильных Google Sheets были использованы только для первичной миграции и выявили 25 расхождений с Lua-комментариями; после миграции источником истины является CSV. AR15, M4Commando и базовый MP5 отмечены как excluded_disabled и не публикуются в wiki.

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

`Systems_Compontents_FoldingStocks.lua` добавляет `zzFoldingPair`; runtime использует `zzStockEquipped` и actions `FoldStock`/`UnFoldStock`. Эти имена являются межфайловым контрактом generated components, UI и визуального состояния entity. В кабинете модификации сложенный half (`*Folded`, не `*UnFolded`) скрыт — крафтится разложенный; Cost Folded = UnFolded (= Light), `StockNormal` чуть дороже (см. `docs/design/stock-tiers.md`).

**UI surface (JAZZ-UI-002):** `FoldStock` / `UnFoldStock` / `FlashlightOn` / `FlashlightOff` имеют `ShowIn = false` и не входят в боевой hotbar. Чипы — вторая колонка `UIWeaponDisplay` `idButtons` (`GridX = 2`) рядом со Switch/Reload; helpers в `Code/System_WeaponCompHUD.lua`.

После JAZZ-ATTACH-001 live components больше не используют `*Handling*` или `Cumbersome` effect presets; Firearm property `Handling` удалён вместе с UI/GameTerm/CTH-modifier presets. Все модифицируемые live component IDs, созданные JAZZ, используют канонический префикс `JAZZ_`; сохранённые `vanilla_ref` stubs отражают ссылки companion-файлов без JAZZ definition и не получают выдуманных effects. Четыре pure-ergo components (`JAZZ_TacGrip`, `JAZZ_Handgrip_Ergo`, `JAZZ_SigErgoHandGrip`, `JAZZ_HandlingWrap`) теперь дают `RecoilDecrease`.

`RocketLauncher.DisposableLauncher` имеет default `false`; `EmbeddedOrdnance` определяет единственный встроенный выстрел одноразового launcher. В v1 JAZZ-WEAPONS-005 этим контрактом пользуется только `M72LAW` (`Warhead_Frag`, magazine 1); RPG-7 не имеет флага и продолжает использовать отдельный ordnance.

Magazine data uses `MagazineSizeSet` with `ModificationType = "Set"` and an absolute `MagazineSize` parameter: named magazines, drums and belts no longer use a live `MagazineSizeMultiplier`. Runtime (`Code/System_WeaponComponent_Set.lua`): engine applies `MulDivRound(base + mod_add, mod_mul, 1000)`, so Set uses `mul=1000`, `add=N−base` (not `mul=0`, which always yielded MagSize 0/1 — e.g. stock CAR-15 / Glock 18 on Vicky/IMP). `LoadGame`/`NewGame` re-seat MagSizeSet magazines and refill ammo when the broken `mul=0` modifier is detected. The former generic `JAZZ_MagLarge` was split into `_50`, `_28`, `_27`, `_25`, `_13` and `_8` variants; PSG1 no longer offers `MagLargeFine`. The barrel-specific `JAZZ_Auto5_*_LMag` multiplier remains a tracked exception.

## Inventory icons (JAZZ-UI-001)

Path **B** (chips): template `Icon` оружия не подменяется. Chip column (VList, left edge): `ChipIcon` → иначе `Icons/Upgrades/Chips/<id>.png` если файл есть → иначе `slot_*`. **Не** использовать `WeaponComponent.Icon` как chip (это art кабинета).

- Chip PNG: `Icons/Upgrades/Chips/<ComponentId>.png` → `Mod/e6L4ECj/Icons/Upgrades/Chips/<…>.png`
- Full кабинет: `Icon` (vanilla `UI/Icons/Upgrades/…` или `Icons/Upgrades/Full/`) — skill `$create-jazz-component-icons`
- Chip миниатюры — skill `$create-jazz-chip-icons`
- Runtime: `Code/WeaponAttachChips.lua` + hooks в `InventoryUI.lua`; bake (`WeaponIconBake.lua`) **dormant** — нет в `metadata.code` / `ModItemCode` (не грузится, не ставит `g_HgnvCompressPath`)
- Показ: non-default **или** default + `CanBeEmpty` + `ModificationEffects` (как `CountWeaponUpgrades` — builtin flashlight на MP5A4)
- Порядок (priority): Scope → Side* → Under → Muzzle → …; layout **VWrap** (до **3** в левом столбце, 4-й → второй столбец), size **24px**, margin −4, `JazzAttachChips_Max = 4`
- Mount* слоты не чипуются
- `w_mod` скрывается, когда показан chip column
- Scope/Sights: ChipIcon проставлен для 30 компонентов (2026-07-30)

## Ресурс, кучность и износ

`WeaponResource` (current) ограничен `WeaponResourceMax` (max); `GetFactoryResource()` — неизменяемый factory reference. Обычный ремонт может поднимать только current до max. `DegradePerShot` уменьшает current после выстрелов. Текущая `Grouping` масштабируется integer condition/repair permille multipliers, поэтому повреждение сначала ухудшает дальний CTH, а затем повышает вероятность jam/поломки.

### RepairItems: `Parts` на шкале Condition %

UI (`SectorOperation_ItemsCalcRes` в `Code/System_SectorOperations.lua`) и debit тика (`ModItemSectorOperation RepairItems` / `SectorMercsTick` в `items.lua`) считают обычные **`Parts`** по **Condition % 0..100** (`GetConditionPercent` / `current÷max`), с параметрами операции `restore_condition_per_Part=5`, `parts_per_step=1` — как vanilla tick, не по абсолютным единицам `WeaponResource` (часто 1k–10k). Регрессия remountable-волны (убрали хак `*3`, оставили absolute scale) давала сотни Parts на одно оружие (пример: ~49% при WR≈8000 → ~825). При нехватке Parts тик откатывает `WeaponResource`/`ArmorResource` к значению до тика. **`JAZZ_BarrelParts` / `JAZZ_ScopeParts`** по-прежнему через `CeilDiv(restoredPct_of_factory, 10|20)` в `System_WeaponResourceMaintenance.lua` (отдельный debit; sector-op wiring AC ещё partial). Время операции по-прежнему на absolute resource × `RepairCost` (+ `sum_stat*3` для оружия).

JAZZ-WEAPONS-002 добавляет независимый 0.5% integer-roll на каждый выстрел: при успехе max теряет не более одной единицы. При jam max теряет минимум одну единицу от 0.5% (ordinary) или 3% (critical); `P(critical|jam) = clamp(5 + wear×35/100 + max(0,100−Mechanical)×25/100, 5, 65)`. Неудачный **player** Unjam (`FirearmBase:Unjam`): −**1..3% max** (`condLoss = Clamp(DivRound(Random(100−Mechanical), 10), 1, 3)`); current clamp ≤ new max; при `max≤1` или condition%≤0 — поломка. Боевое действие `Unjam` стоит **4…1 ОД** от Mechanical (`4 - MulDivRound(Clamp(mech,0,100), 3, 100)`; `MrFixit` — perk AP). **NPC/AI** clear jam через `AIReloadWeapons` → `RepairJammed(nil)` **без** записи `WeaponResource` (раньше баг: `RepairJammed(Condition)` трактовал 0..100% как абсолютные единицы и обнулял ствол, напр. 0/9695). Runtime wave остаётся BLOCKED.

Jam использует единую шкалу **JamScore** `0..1000` (те же единицы, что `attacker:Random(1000)` в `ReliabilityCheck`). Приведённый процент для UI/ammo rollover: `DivRound(JamScore, 10)`. Окно модификации оружия показывает **Reliability**, не Jam %.

Базовый weapon score (без стрелка) уважает шкалу **Reliability 5..95**
и читает свойства через `GetProperty` (ammo/component modifiers):

```text
Reliability = clamp(Reliability, 5, 95)
if Reliability >= 95:
  base = 0                    # даже Poor/Crafted не дают базовый клин
else:
  reliability_score = max(0, 100 - Reliability)
  if BaseJamChance >= 0:
    scaled = MulDivRound(BaseJamChance, reliability_score, 95)
    base = max(reliability_score, scaled)
  else:
    base = reliability_score + BaseJamChance
base = clamp(base, 0, 100)                 # максимум 10%

condition_percent = current / max
permanent_percent = max / factory
JamScore = base
  + max(pen(condition), pen(permanent))
  + DivRound(min(pen(condition), pen(permanent)), 2)
```

При **Rel ≥ 95** платформа «вывозит» плохие патроны на базовом риске 0%;
износ ресурса по-прежнему добавляет ступени. Ниже 95 положительный
`BaseJamChance` патронов/обвеса масштабируется ненадёжностью, а не
перебивает надёжный ствол абсолютным полом. Идеальный ствол с Rel 50
(MP40) по-прежнему даёт базовые 5%.

Текущее состояние (`current/max`) и постоянный остаток ресурса
(`max/factory`) считают **одну** таблицу ступеней; в сумму идёт полный
худший штраф и **половина** второго (soft stack), чтобы mid/mid + rain ×2
не удваивали mid-риск. Середина шкалы мягче полного double-add:

| Остаток ресурса | Надбавка JamScore | Надбавка к шансу |
|---:|---:|---:|
| 100% | 0 | +0% |
| 90–99% | 10 | +1% |
| 80–89% | 50 | +5% |
| 70–79% | 55 | +5.5% |
| 60–69% | 60 | +6% |
| 50–59% | 80 | +8% |
| 40–49% | 110 | +11% |
| 30–39% | 160 | +16% |
| 20–29% | 230 | +23% |
| 10–19% | 320 | +32% |
| 1–9% | 450 | +45% |
| 0% | итог 1000 | 100% |

Если оба остатка не ниже 80%, сумма до погоды дополнительно ограничена 10%.
Затем вычитается serviceability softener
`MulDivRound(50, service², 10000)` где `service = Min(condition, permanent)`:
до **−5%** на 100% состоянии (квадратично, mid почти без скидки).
Пока оба остатка >0, raw ≤990 (display 100% только при нуле). Дождь после
этих потолков. MP40 при полном постоянном ресурсе: **0% / 2% / 7%** на
100% / 90% / 80% текущего. Mid Mosin ≈ **8%** сухо; perfect + extreme ammo ≤ **5%**.
VSS + кустарный 9×39 на 100% ≈ **1%** (было ~6% до softener).

Mechanical снижает score **пропорционально** (`MulDivRound(score, Mechanical, 120)` у мерков + малый secondary Marks/Wisdom/Level; у AI знаменатель 150). Одиночный выстрел делит score пополам через `DivRound`. `FirearmBase:GetDisplayJamChancePercent(attacker?)` отдаёт приведённый %.

`Handling` («Эргономика») удалён из Firearm / WeaponPropertyDef; CTH-модификатор отсутствует, угол overwatch берётся только из `OverwatchAngle` (`JAZZ-WEAPONS-001` / `JAZZ-ATTACH-001`).

Jam/unjam способен необратимо снизить максимальный ресурс или окончательно сломать оружие (**только** путь `FirearmBase:Unjam` с Mechanical roll). `RepairJammed(resource?, owner)`: `nil` — снять jam без износа; число — абсолютный `WeaponResource`. Карточка оружия (`RolloverInventoryWeaponBase`) выводит `GetDisplayJamChancePercent` в строке «Шанс Клина»; в `AdditionalHint` / `GetRolloverHint` jam % не дублируется. Refactor обязан сохранять шкалу 0..1000, порядок проверок, RNG и побочные изменения экземпляра.

## Боеприпасы и crafting

Ammo ModItems наследуют `Ammo`; rollover выводит модификации и effects (`BaseJamChance` как `%` через `/10`), а reload использует специализированный `AmmoInventory`. Операция CraftAmmo в UI даёт только кустарные `JAZZ_AMMO_*_Crafted` и соль (`JAZZ-INV-003`); батч = 100 Parts + порох, выход от калибра. Задумка grade: **альтернатива FMJ** — Rel/jam **между Poor и FMJ** (`Reliability` −3 / `BaseJamChance` +40; Poor винтовка ≈−4/+70, пистолет −10/+100…120), крит ≈ JHP (`CritChance` +15…25 + `Bleeding` на большинстве), pen чуть выше FMJ на пистолетах (на винтовках сейчас часто 2.0 vs FMJ 2.2). 50 `CraftOperationsRecipe` на диске включают скрытые ванильные override. 36 `RecipeDef` — главным образом преобразования брони плюс INV-004 разбор TNT/C4/PETN на порох. Категории Bobby Ray включают 10 ammo subcategories.

### Поэлементная перезарядка (JAZZ-WEAPONS-004)
`ReloadStyle=Magazine` сохраняет обычную полную смену магазина. Для `Tube`, `Break` и `Revolver` пустое оружие использует полный Reload; при `0 < ammo < MagazineSize` тот же слот Reload переключается на `Top up` / «Дозарядить» и загружает ровно один совместимый патрон (`Unit:ReloadAction` → `ReloadWeapon(..., "one_round")` → `Firearm:Reload` с `max_add=1`). Полное оружие недоступно для reload.

Стоимость дозарядки вычисляется из уже модифицированного `ReloadAP`: `max(1 AP, DivCeil(ReloadAP, MagazineSize))`. R870 (`7000`, 6) платит `2000` (2 AP); шесть дозарядок не дешевле полного reload. Tube: M1897, Ithaca, R870, Auto5, SPAS12 и Winchester1894; Break: DoubleBarrelShotgun и Stoeger; Revolver: все active revolver presets. AA12 и USAS12 не имеют authored style и остаются `Magazine`.

### Пробитие патрона (`PenetrationClass` + `PenetrationBonus`)

Контракт данных и UI (канон skill `.agents/skills/jazz-penetration-scales/SKILL.md`):

```text
tenths = DivRound(mod_mul_or_1000, 100) + mod_add_bonus
display = "W.F"   -- 9 → 0.9, 22 → 2.2
```

Боевой pen: `GetAttackPenetrationClass` = `PenetrationClass + 0.1×PenetrationBonus` — см. [броня/урон](armor-damage-wounds-will.md).

`Ammo:GetRolloverHint` склеивает оба модификатора в одну строку и передаёт **`Untranslated` строку**, не Lua float: подстановка числа в `T{}` усекает к нулю (`0.9` → `0`). Форматтер патрона: `FormatAmmoPenetrationDisplay`. Карточка заряженного оружия (`RolloverInventoryWeaponBase`, bind `PenetrationClass`) показывает ту же дробь через `FormatWeaponPenetrationDisplay` (класс + десятые `PenetrationBonus`), не сырой целый класс.

Не ставить `mod_mul = 0` на `PenetrationBonus`: `MulDivRound(base+add, 0, 1000)` зануляет add в бою (`.30 Cal` FMJ tooltip 1.6 / карабин 1.0). Соль: `mod_mul = 0` только на `PenetrationClass`. Аудит: `docs/tools/_audit_ammo_pen_mul_zero.py`.

Не делать `DivRound(mul, 100) * 10 + bonus` (двойной масштаб → 202) и не путать с jam `%` (`/10`).

### Трассерные боеприпасы

Наличие `MarkedTraccers` в `Ammo.AppliedEffects` включает shot-level правило: выбранная unit-цель получает один stack за каждый фактически произведённый выстрел, если итоговый шанс этого выстрела `shot_cth > 0`. Попадание не требуется, поэтому маркер отражает трассирующий/подавляющий огонь; при невозможном выстреле с CTH `0`, jam или отсутствии произведённого выстрела stack не добавляется.

`MarkedTraccers` исключён из обычного `hit.effects`, чтобы попадание не добавляло второй stack. Остальные ammo/body-part effects остаются hit-level и применяются только при отсутствии закрывающей брони либо при её пробитии.

## Дубли и порядок загрузки

Канонические `FirearmBase:GetScrapParts` / `ItemWithCondition:AmountOfScrapPartsFromItem` живут в `GetScrapParts.lua` (грузится после `System_OR_Weapons.lua`); late override `AmountOfScrapPartsFromItem` (resource%) и `GetSpecialScrapItems` — в `System_WeaponResourceMaintenance.lua`. Штраф Condition/resource&lt;50 (`/20`) применяется только в `AmountOfScrapPartsFromItem`. **Scrap eject** (`JAZZ_EjectRemovableAttachmentsForScrap`) копирует remountables в сумку и **не** вызывает `SetWeaponComponent` (иначе loaded loot с Magazine делает `ReloadWeapon` на `weapon.owner` и рвёт SCRAP ALL). Special scrap: сумма `AdditionalCosts` типа `JAZZ_BarrelParts`/`JAZZ_ScopeParts` при успешном Mechanical roll — **без** `component.Cost`. `GrenadeLauncher`/`RocketLauncher`/`Mortar:GetBaseDegradePerShot` в `WeaponClasses.lua` (после `System_OR_Grenade.lua`) возвращают `self.DegradePerShot or const.Weapons.DegradePerShot_*`.

## Межпакетные зависимости

- core item definitions ссылаются на entities и состояния из `jazz_assets`;
- `jazz-units` выдаёт оружие и ammo через UnitData/loot definitions;
- `jazz-maps` размещает оружие, контейнеры и loot;
- sound/FX modules связывают weapon IDs с presets и аудиоресурсами.

Переименование item, caliber, component, effect, slot или entity ID требует поиска во всех четырёх репозиториях.

## Проверка

- текущее состояние и permanent max отдельно на 100/90/80/70/60/50/40/30/20/10/0; MP40 5/6/10% на 100/90/80, Mosin `3280/6507/7000` 27–36%; сухая погода/дождь;
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
