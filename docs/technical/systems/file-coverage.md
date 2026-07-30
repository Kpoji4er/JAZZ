# Покрытие файлов системной документацией

Этот реестр фиксирует статус каждого ручного `Code/*.lua` и указывает страницу-владельца. Статус определяется `metadata.lua`, а не фактом существования файла. Срез обновлён **29 июля 2026**.

Обозначения: **loaded** — загружается; **dormant** — существует, но не указан в metadata; **empty** — нулевая/пустая заготовка; **inert** — загружается, но активная логика отсутствует; **editor** — инструментальная логика.

## `jazz`: бой, оружие, броня и инвентарь

| Файл | Статус | Документация |
|---|---|---|
| `AccuracyRangeCTH.lua` | loaded | [Бой, CTH и действия](combat-cth-actions.md) |
| `CombatActions.lua` | loaded | [Бой, CTH и действия](combat-cth-actions.md) |
| `ExecFirearmAttacks.lua` | loaded | [Бой, CTH и действия](combat-cth-actions.md) |
| `IModeCombatAreaAim.lua` | loaded | [Бой, CTH и действия](combat-cth-actions.md) |
| `CrossHairUI.lua` | loaded | [Бой](combat-cth-actions.md), [UI](ui-audio-fx.md) |
| `CombatBadge_DeathRoll.lua` | loaded | [Бой](combat-cth-actions.md), [UI](ui-audio-fx.md) |
| `System_Firearm_AddProperties.lua` | loaded | [Оружие](weapons-ammo-components.md) |
| `System_OR_Weapons.lua` | loaded | [Оружие](weapons-ammo-components.md) |
| `WeaponClasses.lua` | loaded | [Оружие](weapons-ammo-components.md) |
| `Systems_Compontents_FoldingStocks.lua` | loaded | [Оружие](weapons-ammo-components.md) |
| `GetScrapParts.lua` | loaded | [Оружие](weapons-ammo-components.md), [инвентарь](inventory-items-loot-crafting.md) |
| `System_OR_Grenade.lua` | loaded | [Взрывчатка](explosives-traps-heavy-weapons.md) |
| `System_OR_Traps.lua` | loaded | [Взрывчатка](explosives-traps-heavy-weapons.md) |
| `System_GasMask.lua` | loaded | [Взрывчатка](explosives-traps-heavy-weapons.md), [броня](armor-damage-wounds-will.md) |
| `System_ArmorRating.lua` | loaded | [Броня и повреждения](armor-damage-wounds-will.md) |
| `UnitPropertiesStats.lua` | loaded | [Броня и воля](armor-damage-wounds-will.md) |
| `GritOnStart.lua` | loaded | [Броня и воля](armor-damage-wounds-will.md) |
| `Systems_Wounds_HealWounds.lua` | loaded | [Ранения](armor-damage-wounds-will.md) |
| `System_Wounds_OperationHeal.lua` | loaded | [Ранения](armor-damage-wounds-will.md) |
| `WillPointsBar.lua` | loaded | [Броня и воля](armor-damage-wounds-will.md), [UI](ui-audio-fx.md) |
| `System_OR_Unit.lua` | loaded | [Броня](armor-damage-wounds-will.md), [AI](ai-awareness.md), [видимость](visibility-weather-appearance.md) |
| `Inventory.lua` | loaded | [Инвентарь](inventory-items-loot-crafting.md) |
| `InventoryUI.lua` | loaded | [Инвентарь](inventory-items-loot-crafting.md), [UI](ui-audio-fx.md) |
| `System_UnitInventory.lua` | loaded | [Инвентарь](inventory-items-loot-crafting.md) |
| `System_InventoryStacks.lua` | loaded | [Инвентарь](inventory-items-loot-crafting.md) |
| `System_Vest.lua` | loaded, Vest slot неактивен | [Инвентарь](inventory-items-loot-crafting.md), [броня](armor-damage-wounds-will.md) |
| `System_OR_ItemContainer.lua` | loaded | [Инвентарь](inventory-items-loot-crafting.md) |
| `System_OR_SquadBag.lua` | loaded | [Инвентарь](inventory-items-loot-crafting.md) |
| `System_LootDef.lua` | loaded | [Инвентарь и loot](inventory-items-loot-crafting.md) |
| `System_LootDrops.lua` | loaded | [Инвентарь и loot](inventory-items-loot-crafting.md) |
| `AmmoRolloverHint.lua` | loaded | [Оружие](weapons-ammo-components.md), [UI](ui-audio-fx.md) |
| `WeaponIconBake.lua` | loaded | [Оружие](weapons-ammo-components.md), [UI](ui-audio-fx.md) |

## `jazz`: AI, видимость и юниты

| Файл | Статус | Документация |
|---|---|---|
| `AiActions.lua` | loaded | [AI](ai-awareness.md) |
| `AiAction_ThrowFlare.lua` | loaded | [AI](ai-awareness.md), [взрывчатка](explosives-traps-heavy-weapons.md) |
| `AiFastForward.lua` | loaded | [AI](ai-awareness.md), [UI](ui-audio-fx.md) |
| `AIBehaviours.lua` | loaded | [AI](ai-awareness.md) |
| `AIPolicy.lua` | loaded | [AI](ai-awareness.md) |
| `AIContextProfiles.lua` | loaded | [AI](ai-awareness.md) |
| `CombatAI.lua` | loaded | [AI](ai-awareness.md) |
| `UnitAwareness.lua` | loaded | [AI](ai-awareness.md) |
| `PushUnitAlert.lua` | loaded, empty | [AI](ai-awareness.md) |
| `AIPolicyAttackAP.lua` | dormant, empty | [AI](ai-awareness.md), [runtime](runtime-editor-integration.md) |
| `InfiniteLoopFix.lua` | loaded guard | [AI](ai-awareness.md), [runtime](runtime-editor-integration.md) |
| `Weather.lua` | loaded | [Видимость и погода](visibility-weather-appearance.md) |
| `System_UnitAppearance.lua` | loaded | [Видимость и внешний вид](visibility-weather-appearance.md) |
| `NoSoundsInRooms.lua` | loaded, inert/commented | [Видимость](visibility-weather-appearance.md), [UI/audio](ui-audio-fx.md) |
| `Camera.lua` | loaded | [Видимость](visibility-weather-appearance.md), [бой](combat-cth-actions.md) |
| `SpecializationGiver.lua` | loaded | [Юниты и специализации](units-progression-specializations.md) |
| `System_AimHiringFilters.lua` | loaded | [Юниты и специализации](units-progression-specializations.md) |
| `AimHiringScreen_Template.lua` | dormant | [Юниты](units-progression-specializations.md), [runtime](runtime-editor-integration.md) |

## `jazz`: стратегия, UI и integration

| Файл | Статус | Документация |
|---|---|---|
| `Deployment.lua` | loaded | [Стратегия](strategy-squads-sectors.md) |
| `EnemySquad.lua` | loaded | [Стратегия](strategy-squads-sectors.md) |
| `Guardpost.lua` | loaded | [Стратегия](strategy-squads-sectors.md) |
| `Guardpost_Patrols.lua` | loaded, Legion Global AI director | [Стратегия](strategy-squads-sectors.md) |
| `LegionUnitPrices.lua` | loaded | [Стратегия](strategy-squads-sectors.md), [легион tiers](legion-units-equipment-tiers.md) |
| `LegionSquadComposition.lua` | loaded | [Стратегия](strategy-squads-sectors.md), [легион tiers](legion-units-equipment-tiers.md) |
| `LegionSquadGenerator.lua` | loaded | [Стратегия](strategy-squads-sectors.md) |
| `LegionMilitiaRecruits.lua` | loaded (soft gate; 011 partial) | [Стратегия](strategy-squads-sectors.md) |
| `Regions_Sectors.lua` | loaded | [Стратегия](strategy-squads-sectors.md) |
| `SatelliteSquad.lua` | loaded | [Стратегия](strategy-squads-sectors.md) |
| `SatelliteSquadFixes.lua` | loaded, empty | [Стратегия](strategy-squads-sectors.md) |
| `POI Extension.lua` | loaded | [Стратегия](strategy-squads-sectors.md) |
| `System_SectorOperations.lua` | loaded | [Стратегия](strategy-squads-sectors.md) |
| `WorldFlipSpawnUnits.lua` | loaded | [Стратегия](strategy-squads-sectors.md) |
| `UtilityFunc.lua` | loaded | [Стратегия](strategy-squads-sectors.md), [runtime](runtime-editor-integration.md) |
| `VanillaDesyncFixes.lua` | loaded | [Runtime](runtime-editor-integration.md), [development](../development.md) — vanilla ending/statboost/weighted RNG/shot vectors/AI area |
| `EmptySquadFix.lua` | dormant | [Стратегия](strategy-squads-sectors.md), [runtime](runtime-editor-integration.md) |
| `PatrollingFix.lua` | dormant | [Стратегия](strategy-squads-sectors.md), [runtime](runtime-editor-integration.md) |
| `Savefix.lua` | dormant | [Стратегия](strategy-squads-sectors.md), [runtime](runtime-editor-integration.md) |
| `ConsoleFont.lua` | loaded | [UI](ui-audio-fx.md) |
| `EditorExtension.lua` | loaded, editor | [Runtime и инструменты](runtime-editor-integration.md) |
| `Debug.lua` | loaded, empty | [Runtime и инструменты](runtime-editor-integration.md) |

## `jazz`: звук и FX

- `CodeSounds.lua`, `CodeSounds_AK.lua`, `CodeSounds_AR.lua`, `CodeSounds_AR15.lua`, `CodeSounds_BoltR.lua`, `CodeSounds_MG.lua`, `CodeSounds_Pistols.lua`, `CodeSounds_SHOTGUNS.lua`, `CodeSounds_SMG.lua`, `CodeSounds_SVD.lua`, `CodeSounds_WW2Rifles.lua` — все 11 loaded; владелец [UI, звук и FX](ui-audio-fx.md).
- Все 113 `FX_*.lua` в текущем `Code/` перечислены в metadata и считаются loaded; владелец [UI, звук и FX](ui-audio-fx.md). Добавление/удаление проверять одновременно с metadata, SoundPreset, entity/state/spot и ресурсами.

## `jazz-maps`

| Файл | Статус | Документация |
|---|---|---|
| `Rebels_Loyalty.lua` | loaded | [Карты](maps-quests-dialogue.md), [стратегия](strategy-squads-sectors.md) |
| `System_JAZZ_CrocodilePatrol.lua` | loaded | [Карты](maps-quests-dialogue.md) |
| `System_JAZZ_Vehicles.lua` | loaded | [Автотранспорт](satellite-vehicles.md), [дизайн maps](../../../JAZZ%20Maps/docs/combat-vehicle-design.md), [стратегия](strategy-squads-sectors.md) |
| `System_JAZZ_VehicleCombat.lua` | loaded; tactical spawn dormant (`tactical_enabled=false`); stub устарел vs design | [Автотранспорт](satellite-vehicles.md), [дизайн maps](../../../JAZZ%20Maps/docs/combat-vehicle-design.md) |
| `UnitData/JAZZ_CombatHMMWV.lua` | loaded companion stub (не спавнится) | [Автотранспорт](satellite-vehicles.md) |
| Appearance `JAZZ_HMMWV_Stub` | loaded stub (items) | [Автотранспорт](satellite-vehicles.md); будущий tactical Unit |
| `System_JAZZ_CombatVehicle.lua` | **planned** (ещё нет в metadata) | [дизайн maps](../../../JAZZ%20Maps/docs/combat-vehicle-design.md) |
| `AIMechanism.lua` | dormant | [Карты](maps-quests-dialogue.md), [AI](ai-awareness.md), [runtime](runtime-editor-integration.md) |

## `jazz-units`

| Файл | Статус | Документация |
|---|---|---|
| `AIKeywords.lua` | loaded | [AI](ai-awareness.md), [юниты](units-progression-specializations.md) |
| `AICombatStance.lua` | loaded | [AI](ai-awareness.md) |
| `EliteEnemyNamesFuncs.lua` | loaded | [Юниты](units-progression-specializations.md) |
| `ExperienceSys.lua` | loaded | [Юниты](units-progression-specializations.md) |
| `ExperienceTable.lua` | loaded | [Юниты](units-progression-specializations.md) |
| `Legion.lua` | loaded | [Юниты](units-progression-specializations.md) |
| `Mercenary.lua` | loaded | [Юниты](units-progression-specializations.md) |
| `Rebels.lua` | loaded | [Юниты](units-progression-specializations.md) |
| `StatGainRework.lua` | loaded | [Юниты](units-progression-specializations.md) |

## `jazz_assets`

Пакет не содержит `Code/`. Его generated entity/resource coverage описано в [Entities и ресурсы](assets-entities.md): 490 registered Entity ModItems при 503 entity definitions на диске; 13 файлов требуют индивидуального orphan/reference-аудита, но не автоматического удаления.

## Localization tooling

| Файл | Статус | Документация |
|---|---|---|
| Russian.csv | loaded runtime, Russian mod-only IDs | [Локализация](localization.md) |
| `English.csv` | loaded runtime, English mod-only IDs | [Локализация](localization.md) |
| `Localization/Strings.csv` | development-only catalog | [Локализация](localization.md) |
| Localization/RussianManual.csv | development-only translation memory | [Локализация](localization.md) |
| `Localization/EnglishManual.csv` | development-only English translation memory | [Локализация](localization.md) |
| `Localization/Collisions.csv` | generated audit report | [Локализация](localization.md) |
| `Localization/IdMigration.csv` | development-only applied ID manifest | [Локализация](localization.md) |
| `Localization/IdAmbiguities.csv` | generated ambiguity report | [Локализация](localization.md) |
| `scripts/localization/audit-localization.ps1` | development-only auditor/exporter | [Локализация](localization.md) |
| scripts/localization/migrate-localization-ids.ps1 | development-only clone-aware Plan/Apply | [Локализация](localization.md) |
| `scripts/localization/translate-english-google.ps1` | development-only opt-in draft translator | [Локализация](localization.md) |
| `.agents/skills/manage-jazz-localization/` | agent workflow only | [Локализация](localization.md) |
## GitHub automation

| Файл | Статус | Документация |
|---|---|---|
| `.github/workflows/discord-player-updates.yml` | GitHub Actions only | [Сводки изменений в Discord](discord-player-updates.md) |
| `.github/scripts/discord-player-update.mjs` | CI only; automatic OpenAI fallback | [Сводки изменений в Discord](discord-player-updates.md) |
| `.github/scripts/discord-player-update.test.mjs` | development/test only | [Сводки изменений в Discord](discord-player-updates.md) |
| `jazz_assets/.github/workflows/discord-player-updates.yml` | GitHub Actions caller only | [Сводки изменений в Discord](discord-player-updates.md) |
| `jazz-maps/.github/workflows/discord-player-updates.yml` | GitHub Actions caller only | [Сводки изменений в Discord](discord-player-updates.md) |
| `jazz-units/.github/workflows/discord-player-updates.yml` | GitHub Actions caller only | [Сводки изменений в Discord](discord-player-updates.md) |

## Generated data coverage

Generated ModItems покрываются системами по типу:

- core items/actions/effects/components/recipes/presets — combat, weapon, armor, inventory, UI/audio pages;
- maps sectors/quests/conversations/banters/loot/setpieces — maps и strategy pages;
- units UnitData/appearances/squads/archetypes/loot/voices — units, AI и strategy pages;
- assets EntityData/resources — assets page.

При появлении нового типа ModItem добавить его на профильную страницу и в этот раздел.
