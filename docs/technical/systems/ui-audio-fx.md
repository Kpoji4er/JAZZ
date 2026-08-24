# Интерфейс, звук и FX

## Связанные specs

- `JAZZ-HOTFIX-001` — исправление lifecycle crosshair, optional rollover controls и Thompson particle resource.

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

Generated `RolloverInventoryWeaponBase` обновляет icon только при наличии optional control `idIcon`; варианты template без такого control продолжают показывать тип оружия без Lua-ошибки.

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