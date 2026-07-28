# Игра, CommonLib и JAZZ

## Как читать матрицу

Загрузка рассматривается как последовательность:

```text
vanilla JA3 → JA3_CommonLib → JAZZ
```

Если каждый слой объявляет одну глобальную функцию или метод под тем же именем, последнее определение заменяет предыдущее. В поддерживаемой конфигурации итоговую функцию предоставляет JAZZ. Однако CommonLib может до этого зарегистрировать обработчики, изменить presets или выполнить мутации данных; такие эффекты не отменяются повторным объявлением функции.

JAZZ поддерживает только последнюю опубликованную CommonLib. Перед каждым анализом сначала проверить официальный `main` и metadata, затем строить эту матрицу по найденной версии. Срез на 25 июля 2026 года: версия 1.11, build 1056, commit `1adf9f232680d3b011248d180fd0ad1e609a8e2c`; это датированный снимок, не pin.

Полная замена любого vanilla-класса в JAZZ всегда сохраняет исходные class name и preset ID и оформляется парой `UndefineClass('<Id>')` непосредственно перед `DefineClass.<Id> = { ... }`. Объявление под новым именем, включая `JAZZ_`-префикс, создаёт параллельный класс и не заменяет vanilla. Это общепроектное правило; каждое такое пересечение отдельно заносится в матрицу и повторно сравнивается после обновления игры.

## Прямые пересечения CommonLib и JAZZ

| Символ | Было в игре | CommonLib | JAZZ, загружается позже | Итог и риск |
| --- | --- | --- | --- | --- |
| `AIChooseSignatureAction` | `Lua/Tactical/CombatAI.lua` | `Code/FixAI.lua` | `Code/CombatAI.lua` | JAZZ; высокий риск потери будущих AI-fix CLib |
| `AIGetAttackTargetingOptions` | `Lua/Tactical/CombatAI.lua` | `Code/FixAI.lua` | `Code/AiActions.lua` | JAZZ; проверить targeting и выбор attack action |
| `AIPolicyIndoorsOutdoors:EvalDest` | `Lua/ClassDefs/ClassDef-AI.generated.lua` | `Code/FixAI.lua` | `Code/AiActions.lua` | JAZZ; проверить оценку indoor/outdoor позиции |
| `AIPolicyProximity:EvalDest` | `Lua/ClassDefs/ClassDef-AI.generated.lua` | `Code/FixAI.lua` | `Code/AIPolicy.lua` | JAZZ; проверить дистанционные веса |
| `AISelectAction` | `Lua/Tactical/CombatAI.lua` | `Code/FixAI.lua` | `Code/CombatAI.lua` | JAZZ; сигнатуры слоёв различаются, высокий риск |
| `GetRandomSquadLogo` | `Lua/Satellite/SatelliteSquad.lua` | `Code/ModItems.lua` | `Code/SatelliteSquad.lua` | JAZZ; проверить пользовательские squad logos |
| `gameOverState` (`MapVar`) | `Lua/Satellite/SatelliteSquad.lua` | — | `Code/SatelliteSquad.lua` использует значение, но не регистрирует его | Владелец registration — vanilla; повторный `MapVar` в JAZZ вызывает cold-load assert |
| `OnMsg.SatelliteTick` | `Lua/Satellite/SatelliteSquad.lua` | — | JAZZ-HOTFIX-002: **не регистрируется** (был identical duplicate; `OnMsg` append) | Один handler — vanilla; global `SatelliteUnitsTick` и др. по-прежнему заменяются по имени |
| `GetMineIncome` | `Lua/Satellite/SatelliteView.lua` | — | `Code/POI Extension.lua` (сумма mine/farm/donations/wood/slon; `nil` при 0) | JAZZ; `SectorsTick` early-out на секторах без дохода |
| `SetupCrocodilePatrolSquad` | `Lua/HotDiamonds.lua` | — | maps `Code/System_JAZZ_CrocodilePatrol.lua` | Дом/маршрут I18–I19–J19 вместо G14/G13–G15 (ремап wetlands) |
| `OnMsg.ReachSectorCenter` (crocodile) | `Lua/HotDiamonds.lua` | — | maps `Code/System_JAZZ_CrocodilePatrol.lua` (upvalue-replace при `debug`, иначе wrap `Msg`) | Vanilla `for i=1,place` падает при place=nil вне G13–G14; shipping часто без `debug` |
| `GetSectorTravelTime` | `Lua/Satellite/SatelliteSquad.lua` | — | core `Code/SatelliteSquad.lua`, затем maps wrapper `Code/System_JAZZ_Vehicles.lua` | Maps ускоряет/блокирует путь для mounted squad; грузить maps после core |
| `GetCombatPath` | `Lua/Tactical/Combat.lua` | — | maps `Code/System_JAZZ_VehicleCombat.lua` | Фильтр reachable для `JAZZ_IsVehicle` (поворот ≤±90°) |
| `Unit:CombatGoto` | `Lua/Tactical/Unit.lua` | — | maps `Code/System_JAZZ_VehicleCombat.lua` | Snap-move без Walk-анимов для боевого транспорта |
| `Unit:GotoSlab` | `Lua/Tactical/Unit.lua` | — | maps `Code/System_JAZZ_VehicleCombat.lua` | Exploration-move для боевого транспорта |
| `Unit:EnumUIActions` | `Lua/UI/UnitCaching.lua` | `Code/TweaksUI.lua` | core `Code/System_OR_Unit.lua`, затем maps `Code/System_JAZZ_VehicleCombat.lua` | Core меняет UI actions; maps добавляет Pivot/Turret для vehicle unit — грузить maps после core |
| `IsLineInSmoke` | Не найдено как глобальный символ в экспортированном source | `Code/_Utils.lua` | `Code/System_OR_Unit.lua` | JAZZ заменяет функцию, введённую CLib |
| `Unit:RunAndGun` | `Lua/Tactical/UnitActions.lua` | `Code/FixAI.lua` | `Code/CombatActions.lua` | JAZZ; проверить AP, движение, очередь и AI |
| `Unit:UpdateMeleeTrainingVisual` | `Lua/Tactical/UnitOverwatch.lua` | `Code/FixesFromFys.lua` | `Code/System_OR_Unit.lua` | JAZZ; проверить очистку визуализации |
| `UpdateSuspicion` | `Lua/Tactical/UnitAwareness.lua` | `Code/FixAI.lua` | `Code/UnitAwareness.lua` | JAZZ; высокий риск для stealth/awareness |

Это реальные коллизии имён, а не автоматически подтверждённые ошибки. Большинство переопределений JAZZ намеренны, поскольку мод меняет соответствующие системы. Риск состоит в том, что обновление CommonLib может исправить исходную реализацию, но JAZZ продолжит заменять её старой или независимой версией.

## Крупные переопределения vanilla-кода JAZZ

Следующие модули имеют прямой смысловой аналог в исходниках игры и содержат существенно изменённые или частичные копии vanilla-логики:

| JAZZ | Vanilla JA3 | Область |
| --- | --- | --- |
| `Code/AiActions.lua` | `Lua/Tactical/AIActions.lua` | AI actions и targeting |
| `Code/CombatActions.lua` | `Lua/CombatActions.lua` | Боевые действия юнита |
| `Code/CombatAI.lua` | `Lua/Tactical/CombatAI.lua` | Выбор AI-действия |
| `Code/CrossHairUI.lua` | `Lua/UI/CrosshairUI.lua` | Crosshair и CTH UI |
| `Code/Deployment.lua` | `Lua/Tactical/Deployment.lua` | Размещение на карте |
| `Code/Guardpost.lua` | `Lua/Guardpost.lua` | Guardposts и патрули |
| `Code/IModeCombatAreaAim.lua` | `Lua/UI/IModeCombatAreaAim.lua` | Режим area aim |
| `Code/Inventory.lua` | `Lua/Inventory.lua` | Инвентарь и предметы |
| `Code/InventoryUI.lua` | `Lua/UI/InventoryUI.lua` | UI инвентаря |
| `Code/SatelliteSquad.lua` | `Lua/Satellite/SatelliteSquad.lua` | Стратегические отряды |
| `Code/UnitAwareness.lua` | `Lua/Tactical/UnitAwareness.lua` | Обнаружение и подозрение |
| `Code/Weather.lua` | `Lua/Weather.lua` | Погода и эффекты |
| `CharacterEffect/DamageReduction.lua` | vanilla-класс `DamageReduction` | Намеренная полная замена CharacterEffect с сохранением исходного class name и preset ID |

### Точечные UI wrappers пилота Legion Global AI

| Символ | Vanilla JA3 | JAZZ | Граница совместимости |
| --- | --- | --- | --- |
| `GetSatelliteIconImages` | `Lua/UI/XSatelliteObjects.lua` | `POI Extension.lua` (load order), затем late re-wrap `JAZZ_LegionAIGetSatelliteIconImages` | После POI Legion AI снова становится итоговым владельцем для managed squad: icon по role PNG; unmanaged/POI делегируется сохранённой base (POI) |
| `GetSatelliteIconImagesSquad` | `Lua/UI/XSatelliteObjects.lua` | `Code/Guardpost_Patrols.lua` | Managed squad: role PNG без `_2`/`_s`; unmanaged → base |
| `TFormat.SquadNameColored` | `Lua/Tactical/Utility.lua` | сохранённая base-реализация | Заголовок managed/unmanaged squad остаётся vanilla; task больше не встраивается в name |
| `SquadWindow:CreateRolloverWindow` | `Lua/UI/XSatelliteObjects.lua` | `JAZZ_LegionAICreateRolloverWindow` в `Guardpost_Patrols.lua` | После vanilla spawn/open добавляет сворачиваемый `idJAZZLegionAITask` под составом; обновляет его при cycle squad, unmanaged скрывает |
| `SquadWindow:GetRolloverText` | `Lua/UI/XSatelliteObjects.lua` | passthrough `self.context` | Не мутирует persistent `Name`; CreateRolloverWindow этот путь для заголовка не использует |

`Guardpost_Patrols.lua` сохраняет base через `rawget(_G, ...)` и переустанавливает icon/rollover wrappers на `ModsReloaded` / `LoadGame` / `InitSatelliteView`. Base `SquadWindow:CreateRolloverWindow` хранится отдельно и не перехватывается повторно, поэтому ReloadLua не строит recursive chain.

CommonLib 1.11 / commit `1adf9f232680d3b011248d180fd0ad1e609a8e2c` эти символы не переопределяет. После обновления игры или CommonLib повторно проверять сигнатуры и rollover template.

При обновлении игры эти файлы требуют трёхстороннего сравнения: старая vanilla-версия, новая vanilla-версия и JAZZ-версия. Простое копирование нового vanilla-файла поверх JAZZ уничтожит механику мода. Слепое сохранение старой копии может вернуть исправленные разработчиками игры ошибки.

`DamageReduction` — отдельный намеренный override, а не новое глобальное имя JAZZ. Его generated companion должен сначала удалить vanilla-определение через `UndefineClass('DamageReduction')`, а затем объявить замену через `DefineClass.DamageReduction`. Имя нельзя менять на `JAZZ_DamageReduction`: совпадение class name и preset ID необходимо, чтобы заменить vanilla-класс и сохранить существующие обращения к `DamageReduction`. Поэтому правило о префиксе `JAZZ_` к этому символу не применяется; предмет аудита здесь — полнота замены и совместимость с обновлениями vanilla, а не отсутствие namespace-префикса.

## Что является собственным кодом JAZZ

К собственным подсистемам относятся расширенная формула CTH и дальности, отдача очередей, новые свойства оружия и брони, специализированные слоты инвентаря, бронеплиты, собственные ранения, дополнительные AI-политики, POI extension, World Flip, специализации и большая часть предметных definitions.

Даже собственный файл может вызывать или заменять vanilla/CLib API. Классификация «собственный» означает происхождение подсистемы, а не отсутствие зависимостей.

## Дубли внутри JAZZ

Найдены повторные определения, где итог зависит от порядка metadata:

- `FirearmBase:GetScrapParts` и связанные методы состояния определяются в оружейных модулях более одного раза;
- `GrenadeLauncher:GetBaseDegradePerShot`, `RocketLauncher:GetBaseDegradePerShot` и `Mortar:GetBaseDegradePerShot` определяются в `System_OR_Grenade.lua`, затем в `WeaponClasses.lua`;
- `PatrollingSquadSetDestination` есть в загружаемом `Guardpost.lua` и незагружаемом `PatrollingFix.lua`.

До рефакторинга необходимо зафиксировать, какая последняя реализация реально работает, и сохранить её без изменения поведения.

## Процедура перед каждой задачей и после обновления CommonLib

1. Запросить текущие HEAD ветки `main` и metadata в официальном GitLab; зафиксировать найденные version/build/commit и сверить локальную или установленную копию.
2. Повторить поиск всех имён из таблицы и найти новые совпадения.
3. Сравнить сигнатуры, возвраты, side effects и сообщения.
4. Для каждого пересечения решить: принять fix CLib, перенести его в JAZZ или осознанно оставить JAZZ override.
5. Выполнить AI, UI, awareness, Run and Gun, smoke и satellite smoke-тесты.
6. Обновить этот документ.