# Справочник модулей

Это обзор ручного кода. Полный список загружаемых файлов определяется `metadata.lua`.

## Основной пакет

| Область | Основные модули | Назначение |
| --- | --- | --- |
| Точность | `AccuracyRangeCTH.lua`, `System_OR_Unit.lua`, `CrossHairUI.lua` | Базовый CTH, дистанция, модификаторы и отображение |
| Оружие | `System_OR_Weapons.lua`, `System_Firearm_AddProperties.lua`, `WeaponClasses.lua` | Свойства оружия, износ, классовые способности |
| Атаки | `CombatActions.lua`, `ExecFirearmAttacks.lua`, `IModeCombatAreaAim.lua` | Выполнение выстрелов, очередей и area aim |
| Гранаты | `System_OR_Grenade.lua`, `AiAction_ThrowFlare.lua` | Взрывчатка, осветительные средства и AI |
| Броня | `System_ArmorRating.lua`, `System_Vest.lua` | Типы защиты, ресурс брони и бронеплиты |
| Ранения | `Systems_Wounds_HealWounds.lua`, `System_Wounds_OperationHeal.lua` | Боевые статусы и стратегическое лечение |
| Инвентарь | `System_UnitInventory.lua`, `Inventory.lua`, `InventoryUI.lua` | Слоты, ограничения, перенос и интерфейс |
| Предметы | `System_OR_ItemContainer.lua`, `System_OR_SquadBag.lua`, `System_LootDef.lua`, `System_LootDrops.lua` | Контейнеры, squad bag и loot |
| Видимость | `System_OR_Unit.lua`, `System_GasMask.lua`, `Weather.lua` | Свет, дым, погода, камуфляж и защита |
| AI | `AiActions.lua`, `CombatAI.lua`, `AIPolicy.lua`, `AIBehaviours.lua`, `UnitAwareness.lua` | Выбор действий, позиции и обнаружение |
| Стратегия | `Guardpost.lua`, `EnemySquad.lua`, `SatelliteSquad.lua`, `Regions_Sectors.lua` | Патрули, отряды, регионы и сектора |
| Точки интереса | `POI Extension.lua`, `WorldFlipSpawnUnits.lua` | Доходы, POI и атаки World Flip |
| Наёмники | `System_AimHiringFilters.lua`, `SpecializationGiver.lua`, `Deployment.lua` | Фильтры, роли и размещение |
| UI | `WillPointsBar.lua`, `AmmoRolloverHint.lua`, `CombatBadge_DeathRoll.lua` | Дополнительное отображение состояния |
| Звуки и FX | `CodeSounds*.lua`, `FX_*.lua` | ActionFX и звуковые привязки оружия |

`Camera.lua` задаёт пределы zoom тактической камеры и после `CombatEnd` / `SetpieceDialogClosed` синхронизирует live pitch (`SetupLookAtAngle`) + снимает залипшие enemy-turn `hr` overrides / movement locks (ванильный gap: `AdjustCombatCamera("reset")` не вызывает `SetLookAtAngle`).

## Пакет units

| Модуль | Назначение |
| --- | --- |
| `AIKeywords.lua` | Дополнительные ключевые слова и признаки AI |
| `EliteEnemyNamesFuncs.lua` | Генерация составных имён элитных врагов |
| `Legion.lua`, `Rebels.lua`, `Mercenary.lua` | Пулы имён по фракциям |
| `ExperienceSys.lua`, `ExperienceTable.lua` | Система и таблицы опыта |
| `StatGainRework.lua` | Изменение роста характеристик |

## Пакет maps

| Модуль | Статус |
| --- | --- |
| `Rebels_Loyalty.lua` | Загружается; добавляет эффект изменения лояльности фракции |
| `AIMechanism.lua` | На диске присутствует, но в массив `code` metadata не включён и в runtime не загружается |

## Пакет assets

Пакет преимущественно декларативный. Его Lua-файлы регистрируют `EntityData`; игровая логика должна оставаться в основном пакете или в пакете-владельце данных.

## Незагружаемые и пустые файлы

Во время аудита в основном пакете обнаружены Lua-файлы, отсутствующие в массиве `code`:

- `AimHiringScreen_Template.lua`;
- `AIPolicyAttackAP.lua`;
- `CodeSounds_SMG.lua`;
- `EmptySquadFix.lua`;
- `PatrollingFix.lua`;
- `Savefix.lua`.

Отсутствие в metadata означает, что они не участвуют в обычной загрузке мода. Некоторые из них пусты или содержат legacy-код, но некоторые содержат рабочие реализации. Их нельзя автоматически включать или удалять без проверки намерения и сохранений.

Metadata также загружает ряд пустых FX/debug-заглушек. Они перечислены в [техническом долге](technical-debt.md) как кандидаты на отдельную безопасную чистку.
## Полнота справочника

Этот файл остаётся кратким справочником крупных модулей. Полный реестр ручного кода, включая empty, inert и dormant-файлы, находится в [покрытии файлов](systems/file-coverage.md). Поведение каждого модуля описано в [каталоге систем](systems/README.md).

При добавлении или изменении `Code/*.lua` сначала обновить профильную системную страницу и file coverage. Краткую таблицу здесь обновлять, если меняется назначение крупного модуля или граница ответственности.
