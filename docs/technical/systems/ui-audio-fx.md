# Интерфейс, звук и FX

## Связанные specs

- `JAZZ-HOTFIX-001` — исправление lifecycle crosshair, optional rollover controls и Thompson particle resource.
- `JAZZ-UI-CONDITION-001` — `UIWeaponDisplay.idCondText` получает процент через `GetConditionPercent()` в отдельном `SubContext`. Это устраняет чтение устаревшего `Condition` у оружия с ресурсом; исходный предмет не изменяется. Проверено Lua-harness (0/43/100), игровой UI и editor round-trip ещё не проверены. ModItem живёт в `items.lua`, отдельного companion нет; metadata и asset contract не менялись.

## Назначение и эффект для игрока

JAZZ перестраивает ключевые tactical/inventory элементы интерфейса и предоставляет собственный звуковой/FX слой для большого оружейного каталога. UI отображает новые свойства, CTH, состояния оружия/брони, Will, очередь действий и тактические предупреждения.

## Происхождение по слоям

| Слой | Вклад |
|---|---|
| Vanilla | XTemplates, crosshair, inventory UI, combat badge, rollover, styles, sound/FX preset APIs |
| CommonLib | `Unit:EnumUIActions` изменяется в `Code/TweaksUI.lua`, затем JAZZ заменяет метод в `System_OR_Unit.lua` |
| JAZZ | Крупные CrossHairUI/InventoryUI, новый Will bar, расширенный combat badge/rollovers, text styles, sound presets и 113 weapon FX modules |

## Реализация и load-state

Загружаются:

- `Code/CrossHairUI.lua` — CTH, aim и modifiers;
- `Code/InventoryUI.lua` — slots, drag/drop и rollovers;
- `Code/CombatBadge_DeathRoll.lua` — тактические статусы цели;
- `Code/WillPointsBar.lua` — шкала воли;
- `Code/AmmoRolloverHint.lua` — свойства ammo;
- `Code/ConsoleFont.lua` — console text style;
- `Code/IModeCombatAreaAim.lua` — зональное прицеливание;
- `Code/System_AimHiringFilters.lua` — AIM filtering UI logic;
- `Code/CodeSounds.lua` и 10 `CodeSounds_*` modules;
- 113 `Code/FX_*.lua` modules;
- generated 25 XTemplates и 21 TextStyle в core, плюс 4 XTemplates в maps.

`Code/NoSoundsInRooms.lua` загружается, но его содержательная логика закомментирована. Акустическое подавление звука по rooms сейчас неактивно.

## Crosshair и CTH

В обычном режиме Crosshair скрывает точный CTH и показывает у каждого breakdown modifier разное количество зелёных `+` или красных `−` в зависимости от силы эффекта: примерно один знак на 10 пунктов и не более десяти. Нулевая строка не показывается.

При активных modding/debug tools та же разбивка показывает точный итоговый CTH, процент эффекта, множитель `×factor`, `before → after` и список процентов каждой пули очереди. UI читает результат `Unit:CalcChanceToHit` и `attack_results.shot_cth`, а не вычисляет отдельную витринную формулу.

Area-aim обслуживает grenade/zone attacks и только те shotgun firing members, которые действительно объявляют cone targeting. Мета-действие `AttackShotgun` использует line targeting и обычный `IModeCombatAttack`.

Generated `ActionCameraCrosshair` не вызывает `Open` для `idContainer` из `OnContextUpdate`: lifecycle дочернего `XContextWindow` принадлежит XTemplate/XWindow framework. Повторный ручной `Open` уже открытого окна нарушает `window_state == "new"`.

Ретикл оптики (`ScopeOuter` / `idTarget2`, пути `ReticleInner`/`ReticleOuter` компонента) и подпись кратности обновляются в `CrosshairUI:UpdateAim` при смене aim-level ≥ `ScopeAimLevel` / `SmallAimLevel`, а не через повторный `Open` контейнера.

Динамические подписи увеличения оптики передаются в `T` как `Untranslated`, поэтому строка вида `1.0x` не интерпретируется как localization ID.

## Combat badge

`CombatBadge_DeathRoll.lua` показывает или учитывает:

- оставшиеся overwatch attacks;
- sight/line-of-fire и suspicion;
- ammo/reload;
- hidden state;
- queued actions;
- bandage;
- danger/death state.

Мёртвый юнит **не** держит CombatBadge (имя, HP, «вне прямой видимости»). Ваниль снимает бейдж в `OnMsg.UnitDieStart` (`DeleteBadgesFromTargetOfPreset`). После ReloadLua этот ванильный handler часто пропадает, поэтому JAZZ дублирует удаление в `JazzHideCombatBadgeForDeadUnit` (`UnitDieStart` / `UnitDied` / sweep на `ModsReloaded` и `CombatStart`) и коротко замыкает `CombatBadge:UpdateMode` / `UpdateActive`, если `unit:IsDead()`.

Иконки статусов на бейдже — **под** HP-баром (`GetUIVisibleStatusEffects`, Def-aware Shown/Icon). Party HUD в бою и на глобалке (`SquadsAndMercs*` / `idStatusEffectsContainer`) использует `JazzGetPartyPortraitStatusEffects` (`ShownSatelliteView` + fallback с CharacterEffectDefs; `WoundInfected`/bleed/BloodLoss выше в списке, контейнер MaxHeight 160). Иконка **Free Move** показывает оставшиеся ОД FM (оверлей как у стаков; тултип `ResolveValue("Description")`); карточка наёмника рядом с `16+1` дописывает `(N FM)`. Формула FM не меняется — только отображение `unit.free_move_ap` (`System_EnergyLadder.lua`).

`CombatActionBar` (`idCombatActionsContainer`) — **две строки** `HWrap` (`MaxWidth` 600, `MaxHeight` 180). Кнопки спавнит `CombatActionsToActions` из UIAction-пресетов `Action1`…`ActionN`, не из длины `ui_actions`. Ваниль даёт только `Action1`–`Action12` плюс `Action13` (remap на signature). JAZZ в `System_OR_Unit.lua` регистрирует `Action14`–`Action24` (боевые слоты) и `Action25` (remap на signature); `RecalcUIActions` кладёт боевые id в индексы 1–24 и signature на **25**. Без этих пресетов TakeCover / Overwatch с высоким SortKey попадали в `ui_actions`, но кнопки не создавались. TakeCover при отсутствии укрытия остаётся на панели (`disabled`), не `hidden`.

## Inventory и rollovers

Inventory UI визуализирует специализированные slots, resource/max resource, armor/plate, ammo modifications, weapon properties/components и ограничения экипировки. Rollover должен корректно обрабатывать отсутствующие optional properties и generated items старого save. Карточка оружия (`RolloverInventoryWeaponBase` → `RolloverPropTextRight`) показывает live ближний профиль в том же блоке, что Меткость/Настильность/Шанс клина: прирост `CloseRangeFactor` от компонентов (`resolved − base_*`, как short barrel +12); иначе штраф базы при Factor<100 (см. [accuracy-model](../weapons/accuracy-model.md)). В `AdditionalHint` / `GetRolloverHint` ближняя зона не дублируется.

`EquipInventorySlot` HeadGear/ArmorPlate в live `Inventory` при context update **перекладывает** конфликтный предмет в рюкзак только если он реально есть: шлем с `BlockFaceSlot` без NVG больше не вызывает `AddItem("Inventory", nil)` → `CheckClass` на nil (Lua error, экран загрузки). `TFormat.bullets` читает `ammo.colorStyle` только при живом `ammo`. `JazzAttachChips_Apply` больше не создаёт overlay-чипы на тайлах/HUD; старые row очищаются и скрываются, native weapon layers сохраняются (JAZZ-UI-001, 2026-10-02). Live `Inventory` OnContextUpdate не индексирует `idPartyContainer`, если его нет.

Generated `RolloverInventoryWeaponBase` обновляет icon только при наличии optional control `idIcon`; варианты template без такого control продолжают показывать тип оружия без Lua-ошибки.

Строки брони «Возможность установки плиты» / «Блокирует слот лица» — label-only: не `BindTo` boolean `CanHoldPlate` с `PercentValue` (иначе `RolloverPropTextRight:CreatePropValText` → `FormatNumberProp(true)` и `[LUA ERROR]` overlay). `Open` идёт через `XWindow.Open`, не `XPropControl.Open`.

Live `SquadsAndMercs`: внешняя VList — `idPartyLayout`; `idParty.idContainer` — mode-окно (satellite / inventory / tactical), чьи дети — `HUDMerc`. Если `idContainer` повесить на обёртку, `Inventory` OnContextUpdate обходит layout и зовёт `SetSelected` на обычном `XWindow` (`[LUA ERROR]`). Дубликат Id на родителе+ребёнке даёт `[UI WARNING] Assigning window id 'idContainer'`. Канон-проверка: `docs/tools/_check_inventory_portrait_container.py`. Неиспользуемые копии `SquadsAndMercs2` / `SquadsAndMercs_copy` в `items.lua` по-прежнему грузятся как отдельные XTemplate.

## Will bar

`WillPointsBar.lua` — крупный UI-модуль, реагирующий на `CombatEnd`, `TurnEnd` и runtime updates. Он связан с suppression/damage системой; после удаления/деспавна unit не должны оставаться orphaned controls или stale values.

## AIM hiring UI

Loaded `System_AimHiringFilters.lua` использует specialization и availability. `AimHiringScreen_Template.lua` существует, но unlisted и не активен. При диагностике UI не путать его с фактически зарегистрированным XTemplate.

## Звук

Core содержит 243 `SoundPreset` и 1283 `.opus`; units — ещё 702 `.opus` для voices. `CodeSounds.lua` и семейства `CodeSounds_AK`, `AR`, `AR15`, `BoltR`, `MG`, `Pistols`, `SHOTGUNS`, `SMG`, `SVD`, `WW2Rifles` связывают классы/оружие с sound moments/presets.

Sound IDs потребляются actions и FX. Отсутствующий `.opus` или preset может не остановить загрузку, но оставит действие без ожидаемого звука.

### FX Target для дула/ствола (`JAZZ_*`)

`FirearmBase` при выстреле берёт `fx_target` из `visual_obj.parts.Muzzle` или `.Barrel` (`Weapon.lua`). У ванильных пресетов выстрела (в т.ч. `AKSU`) `Target = "Basic"` / `"Silencer"`, а `Compensator` / `BarrelNormal` / `Suppressor` наследуют эти классы через `ActionFXInherit_Actor`.

JAZZ-компоненты (`JAZZ_Compensator`, `JAZZ_BarrelNormal`, `JAZZ_Suppressor*`, `JAZZ_Auto5_*` barrel/mag configs, …) имеют **другие** id, поэтому без inherit выстрел с дефолтным `JAZZ_Compensator` (например АКСУ) или пустым дулом Auto-5 (fx_target = `JAZZ_Auto5_Basic_NMag`) идёт без звука. Маппинг живёт в `Code/CodeSounds.lua` (`JAZZ_*` → `Basic` / `Silencer`).

`Buckshot` (и связанные shotgun fire members) ставят `fx_action = "WeaponBuckshot"`. Preset rows keyed by vanilla FX `id` must keep that Action: rewriting Auto5’s buckshot IDs as `WeaponFire` in `CodeSounds_SHOTGUNS.lua` silenced the gun. Sound bank `Auto5_shot_single` / `-room` samples live under `Sounds/Benellim4/`.

**Pellet pack (JAZZ-WEAPONS-006):** `Buckshot` / `DoubleBarrel` / `CancelShotCone` / `BuckshotBurst` делают `num_shots = BuckshotProjectiles` (×2 для двухстволки) — это **N** вызовов `Firearm:FireBullet`, не очередь. Звук/muzzle FX должен играть **один раз** на патрон: CombatAction ставит `single_fx = true`, а `Code/ExecFirearmAttacks.lua` после первого `FireBullet` обнуляет `attackArg.fx_action` (vanilla чистила только local, который `FireBullet` не читает). Без этого выстрел «размножается» ×9/×20.

`items.lua` переопределяет `AKSU_shot_single` и `AKSU_shot_single-room` 12 собственными сэмплами из `Sounds/AKSU74/`: шесть dry и шесть room `.opus`, все по путям `Mod/e6L4ECj/Sounds/AKSU74/...`. Предыдущее утверждение об отсутствующих файлах было ошибочным: сэмплы присутствуют в core-пакете и отслеживаются Git. `metadata.lua` регистрирует оба `SoundPreset`; отдельная resource-запись на каждый `.opus` для файлов внутри пакета не нужна. `AKSU_shot_auto` остаётся ванильным.

## FX

113 `FX_*.lua` покрывают конкретные модели оружия и общий ammo FX. Они загружаются из metadata индивидуально и образуют реестр moments/particles/sounds для shot, reload, casing, muzzle и других событий. В [покрытии файлов](file-coverage.md) они учитываются одной управляемой группой, но каждое добавление/удаление должно сопровождаться metadata и ресурсами.

Generated `ParticlesThompson` использует self-contained путь `Mod/e6L4ECj/ParticleTextures/Explosion_emissive.dds`; основной DDS и `ParticleTextures/Fallbacks/Explosion_emissive.dds` принадлежат core-пакету и должны поставляться вместе.

## Межпакетные зависимости

- assets: entities, states, spots, textures/materials;
- units: voice presets/files, appearances и speakers;
- maps: XTemplates, camera/setpiece и environment sound context;
- core: actions, items, effects и UI logic.

## Проверка

- keyboard/mouse/controller для crosshair, area aim и inventory;
- CTH breakdown против runtime результата;
- combat badge для hidden/suspicious/overwatch/reload/bandage/death;
- Will bar add/update/remove, turn/combat transitions;
- all inventory tabs/slots and rollovers at narrow/wide resolutions;
- AIM filters online/offline;
- по одному оружию каждого CodeSounds-family и representative FX;
- missing sound preset/file/entity/state/spot warnings;
- подтверждение, что room-sound behavior не изменился, пока файл inert.

## Сопровождение

Новый action/property/status должен получить UI presentation или явно документированное отсутствие. Новое оружие требует проверки sound family, FX module, entity states и metadata registration. Активация `NoSoundsInRooms` считается отдельным изменением системы.


## Установленные фотографии оружия (JAZZ-WEAPON-PRESENTATION-001)

В локальную установленную копию перенесены `WeaponIcons/Live/*.png`: 1739 уникальные конфигурации, RGBA 324×165 / 162×110 согласно исходному Icon. Две повторные конфигурации объединены; служебный UnderslungGrenadeLauncher без собственной entity исключён. `Code/InventoryUI.lua` содержит автоматически построенный реестр и `JazzWeaponIcon_GetCaptured`. Ключ включает class, Entity и все непустые components; false и пустая строка эквивалентны отсутствию детали. Незаполненный components не считается стандартным комплектом.

`InventoryItem:GetItemUIIcon` в `Code/System_WeaponResourceMaintenance.lua` сохраняет flat exact-match fallback. Основной `JazzWeaponIcon_BindItemImage` в `Code/InventoryUI.lua` теперь компонует 1929 нативных layer nodes для 178 активных классов из `WeaponIcons/Live/Layers/*.png`; один вырожденный host G36 является невидимым структурным узлом. Selector учитывает Entity, компоненты, реальный parent signature и наблюдаемые исключения геометрии. Например, короткий SW Model 10 не имеет боковой геометрии даже при логически установленном фонаре. Неизвестный host/component/art возвращает прежнюю иконку целиком.

XControl принадлежит исходному XImage; все цветные слои имеют общий crop по объединённому силуэту. Тёмные силуэты с обводкой рисуются до цветных частей, без внутренних швов. Сохраняются размеры 324×165/162×110, padding 8/5, scale/fit, disabled tint, десатурация и flip. Очистка выполняется при смене контекста, fallback и уничтожении окна. Нет runtime bake, нового глобального XImage wrap, записи в предмет или save fields. Крепления имеют отдельные идентичности слоёв; игровая модульность пока прежняя.

Оба `run_after` оружия в `ModItemXTemplate/UIWeaponDisplay` вызывают тот же binder. Generated delta: шесть строк `items.lua` и штатные revision/saved/code_hash/last_changes `metadata.lua`; companion у шаблона отсутствует. Выполнены официальный SaveWholeMod, UnloadItems/LoadItems и ReloadLua. Снимок до save позволил убрать постороннее форматирование и сгенерированные изменения других предметов, сохранив прежние пути и порядок metadata.code. После нормализации повторно выполнен load/reload.

Автоматические структурные имена не установлены: read-only аудит активной локализации остановился на конфликтующих переводах RussianManual.csv для одного SourceText (AnchorID 890000000020255). Таблицы переводов не изменены. Имена остаются прежними.

Проверка native layers: 446882 offline Lua/graph случаев PASS, 75606 запрещённых сочетаний отдельно исключены по BlockSlots; 9770 реальных графов (обновлён АК-103). Runtime XImage и XInventoryItem проверены на многомодульных AK74, M4A1 и DesertEagle, временные окна/предметы удалены. Это не проверка каждого сочетания в живом UI и не независимая human acceptance. Evidence: `docs/design/weapon-layer-icons/live/layer-verification.json` и `LAYERS-REPLAY.md`.


Уточнение владельца: отключённое оружие не снимать. AR15, M4Commando и MP5 (`catalog_status=excluded_disabled`) исключены из установки, основной галереи и будущих capture batches. 53 иконки удалены только из WeaponIcons/Live; staged/raw архив сохранён. Проверка селектора после фильтрации: 5281 PASS.


Коррекция масштаба v2: `icon_layout.py` формирует каждый кадр по реальному силуэту с отступом 8 px (324×165) или 5 px (162×110). Общие большие прозрачные поля устранены. Исходные кадры и размеры ячеек UI не меняются. `process_live.py` использует тот же renderer для будущих серий. 1739 установленных файлов проверяются по размеру исходной иконки, а не по единому формату 324×165.

Цвет v3 заменяет общую gamma/contrast формулу v2: `calibrate_color.py` строит фиксированный профиль яркости и насыщенности каждого оружия по старому Icon. `icon_layout.py` применяет его ко всем вариантам этого класса. Канон: `docs/design/weapon-layer-icons/live/color-profiles.json` (166 референсов; отсутствующие — явный fallback). По отдельному уточнению владельца контур усилен до 2 px, RGB 5/6/7, с alpha края исходного силуэта. Размеры и масштаб v2 сохраняются, alpha расширяется только на дополнительный пиксель обводки. `test_color_match.py` проверяет размеры, границы обводки и сближение яркости с референсами; результат в `color-verification.json`.


DesertEagle / HiPower: по замечанию владельца квантильная цветокоррекция заменена гладкой степенной кривой. Прежняя кривая усиливала отдельные диапазоны яркости в 6–13 раз и подчёркивала пятна исходных бликов. Ограничено усиление до 2; исправлены все 18 вариантов, размер и alpha сохранены. `calibrate_color.py` воспроизводит исключение; профили остальных классов и общий fallback не меняются. Сравнение: `docs/design/weapon-layer-icons/live/silver-pistols-comparison.png`; проверки: `pistol-tone-verification.json`. Потёртости, присутствующие в исходной модели/снимке, не ретушировались.


Native layers v4 используют `docs/design/weapon-layer-icons/live/layer-color-profiles.json`: 166 плавных профилей по свежим default captures и исходным Icon, 12 явных fallback классов. Это заменяет v3 только для послойной композиции; старые flat PNG сохраняют прежнюю обработку. Все 1928 видимых слоёв имеют прежние размеры/alpha, подтверждено побайтным сравнением. Runtime-пример и сравнение цвета: `layer-runtime-combinations.png`, `layer-color-profiles.png`. Источники съёмки и геометрия не менялись.

АК-103: 40/75 используют визуалы АКМ, абсолютные локальные смещения Z -30/-35 в AK103:UpdateVisualObj; quick исключён из AvailableComponents. Контур native слоя EffectPixels=6. Binder восстанавливает tint из старого color pass после ReloadLua и удаляет orphan-группы до создания новых.
