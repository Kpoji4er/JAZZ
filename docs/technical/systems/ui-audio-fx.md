# Интерфейс, звук и FX

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

Crosshair показывает доступность действия, AP/aim, CTH и breakdown modifiers. Он должен использовать тот же runtime pipeline, что `Unit:CalcChanceToHit`; отдельный UI-пересчёт создаст расхождение показанного и фактического шанса.

Area-aim обслуживает shotgun/grenade/zone attacks. Проверять границы зоны, mouse/controller input, selection cancel, препятствия и friendly targets.

## Combat badge

`CombatBadge_DeathRoll.lua` показывает или учитывает:

- оставшиеся overwatch attacks;
- sight/line-of-fire и suspicion;
- ammo/reload;
- hidden state;
- queued actions;
- bandage;
- danger/death state.

Это модифицированная tactical UI часть, чувствительная к новым vanilla status fields и action lifecycle.

## Inventory и rollovers

Inventory UI визуализирует специализированные slots, resource/max resource, armor/plate, ammo modifications, weapon properties/components и ограничения экипировки. Rollover должен корректно обрабатывать отсутствующие optional properties и generated items старого save.

## Will bar

`WillPointsBar.lua` — крупный UI-модуль, реагирующий на `CombatEnd`, `TurnEnd` и runtime updates. Он связан с suppression/damage системой; после удаления/деспавна unit не должны оставаться orphaned controls или stale values.

## AIM hiring UI

Loaded `System_AimHiringFilters.lua` использует specialization и availability. `AimHiringScreen_Template.lua` существует, но unlisted и не активен. При диагностике UI не путать его с фактически зарегистрированным XTemplate.

## Звук

Core содержит 243 `SoundPreset` и 1283 `.opus`; units — ещё 702 `.opus` для voices. `CodeSounds.lua` и семейства `CodeSounds_AK`, `AR`, `AR15`, `BoltR`, `MG`, `Pistols`, `SHOTGUNS`, `SMG`, `SVD`, `WW2Rifles` связывают классы/оружие с sound moments/presets.

Sound IDs потребляются actions и FX. Отсутствующий `.opus` или preset может не остановить загрузку, но оставит действие без ожидаемого звука.

## FX

113 `FX_*.lua` покрывают конкретные модели оружия и общий ammo FX. Они загружаются из metadata индивидуально и образуют реестр moments/particles/sounds для shot, reload, casing, muzzle и других событий. В [покрытии файлов](file-coverage.md) они учитываются одной управляемой группой, но каждое добавление/удаление должно сопровождаться metadata и ресурсами.

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