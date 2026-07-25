# Игра, CommonLib и JAZZ

## Как читать матрицу

Загрузка рассматривается как последовательность:

```text
vanilla JA3 → JA3_CommonLib → JAZZ
```

Если каждый слой объявляет одну глобальную функцию или метод под тем же именем, последнее определение заменяет предыдущее. В поддерживаемой конфигурации итоговую функцию предоставляет JAZZ. Однако CommonLib может до этого зарегистрировать обработчики, изменить presets или выполнить мутации данных; такие эффекты не отменяются повторным объявлением функции.

JAZZ поддерживает только последнюю опубликованную CommonLib. Перед каждым анализом сначала проверить официальный `main` и metadata, затем строить эту матрицу по найденной версии. Срез на 25 июля 2026 года: версия 1.11, build 1056, commit `1adf9f232680d3b011248d180fd0ad1e609a8e2c`; это датированный снимок, не pin.

## Прямые пересечения CommonLib и JAZZ

| Символ | Было в игре | CommonLib | JAZZ, загружается позже | Итог и риск |
| --- | --- | --- | --- | --- |
| `AIChooseSignatureAction` | `Lua/Tactical/CombatAI.lua` | `Code/FixAI.lua` | `Code/CombatAI.lua` | JAZZ; высокий риск потери будущих AI-fix CLib |
| `AIGetAttackTargetingOptions` | `Lua/Tactical/CombatAI.lua` | `Code/FixAI.lua` | `Code/AiActions.lua` | JAZZ; проверить targeting и выбор attack action |
| `AIPolicyIndoorsOutdoors:EvalDest` | `Lua/ClassDefs/ClassDef-AI.generated.lua` | `Code/FixAI.lua` | `Code/AiActions.lua` | JAZZ; проверить оценку indoor/outdoor позиции |
| `AIPolicyProximity:EvalDest` | `Lua/ClassDefs/ClassDef-AI.generated.lua` | `Code/FixAI.lua` | `Code/AIPolicy.lua` | JAZZ; проверить дистанционные веса |
| `AISelectAction` | `Lua/Tactical/CombatAI.lua` | `Code/FixAI.lua` | `Code/CombatAI.lua` | JAZZ; сигнатуры слоёв различаются, высокий риск |
| `GetRandomSquadLogo` | `Lua/Satellite/SatelliteSquad.lua` | `Code/ModItems.lua` | `Code/SatelliteSquad.lua` | JAZZ; проверить пользовательские squad logos |
| `IsLineInSmoke` | Не найдено как глобальный символ в экспортированном source | `Code/_Utils.lua` | `Code/System_OR_Unit.lua` | JAZZ заменяет функцию, введённую CLib |
| `Unit:EnumUIActions` | `Lua/UI/UnitCaching.lua` | `Code/TweaksUI.lua` | `Code/System_OR_Unit.lua` | JAZZ; проверить кеш UI actions и действия CLib |
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

При обновлении игры эти файлы требуют трёхстороннего сравнения: старая vanilla-версия, новая vanilla-версия и JAZZ-версия. Простое копирование нового vanilla-файла поверх JAZZ уничтожит механику мода. Слепое сохранение старой копии может вернуть исправленные разработчиками игры ошибки.

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