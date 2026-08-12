# Покрытие файлов системной документацией

Этот реестр фиксирует статус каждого ручного `Code/*.lua` и указывает страницу-владельца. Статус определяется `metadata.lua`, а не фактом существования файла. Срез обновлён **7 августа 2026**.

Обозначения: **loaded** — загружается; **dormant** — существует, но не указан в metadata; **empty** — нулевая/пустая заготовка; **inert** — загружается, но активная логика отсутствует; **editor** — инструментальная логика.

## `jazz`: бой, оружие, броня и инвентарь

| Файл | Статус | Документация |
|---|---|---|
| `AccuracyRangeCTH.lua` | loaded | [Бой, CTH и действия](combat-cth-actions.md) |
| `CombatActions.lua` | loaded | [Бой, CTH и действия](combat-cth-actions.md) |
| `ExecFirearmAttacks.lua` | loaded | [Бой, CTH и действия](combat-cth-actions.md) |
| `MeleeWeapon.lua` | loaded | [Бой, CTH и действия](combat-cth-actions.md) — thrown knife `ignore_smoke` |
| `IModeCombatAreaAim.lua` | loaded | [Бой, CTH и действия](combat-cth-actions.md) |
| `CrossHairUI.lua` | loaded | [Бой](combat-cth-actions.md), [UI](ui-audio-fx.md) |
| `CombatBadge_DeathRoll.lua` | loaded | [Бой](combat-cth-actions.md), [UI](ui-audio-fx.md) |
| `System_Firearm_AddProperties.lua` | loaded | [Оружие](weapons-ammo-components.md) |
| `System_BobbyRay_ECON004.lua` | loaded | [Bobby Ray](bobby-ray-shop.md) — soft-tail restock / ammo boost / staples flat / tier price |
| `System_OR_Weapons.lua` | loaded | [Оружие](weapons-ammo-components.md) |
| `System_EmplacementAmmo.lua` | loaded | [Оружие](weapons-ammo-components.md) — remap cut `_50BMG_*` emplacement ammo → `JAZZ_AMMO_50BMG_*`; HOTFIX-004 load reseat `ManningEmplacement` |
| `System_WeaponResourceMaintenance.lua` | loaded | [Оружие](weapons-ammo-components.md), [инвентарь](inventory-items-loot-crafting.md) — JAZZ-WEAPONS-002 resource triad / jam wear |
| `WeaponClasses.lua` | loaded | [Оружие](weapons-ammo-components.md) |
| `System_DisposableLaunchers.lua` | loaded | [Оружие](weapons-ammo-components.md), [взрывчатка](explosives-traps-heavy-weapons.md) |
| `Systems_Compontents_FoldingStocks.lua` | loaded | [Оружие](weapons-ammo-components.md) |
| `System_WeaponCompHUD.lua` | loaded | [Оружие](weapons-ammo-components.md), [combat-actions](../weapons/combat-actions.md) — JAZZ-UI-002 Fold/Flash chips у иконки |
| `GetScrapParts.lua` | loaded | [Оружие](weapons-ammo-components.md), [инвентарь](inventory-items-loot-crafting.md) |
| `System_OR_Grenade.lua` | loaded | [Взрывчатка](explosives-traps-heavy-weapons.md) |
| `System_OR_Traps.lua` | loaded | [Взрывчатка](explosives-traps-heavy-weapons.md) |
| `System_GasMask.lua` | loaded | [Взрывчатка](explosives-traps-heavy-weapons.md), [броня](armor-damage-wounds-will.md) |
| `System_ArmorRating.lua` | loaded | [Броня и повреждения](armor-damage-wounds-will.md) |
| `UnitPropertiesStats.lua` | loaded | [Броня и воля](armor-damage-wounds-will.md) |
| `GritOnStart.lua` | loaded | [Броня и воля](armor-damage-wounds-will.md) — grit CombatStart off (MED-001) |
| `Systems_Medicine.lua` | loaded | [Ранения](armor-damage-wounds-will.md) — bleed tiers / Pain / zonal traumas / bandage API (MED-001) |
| `System_JazzStackableMedicine.lua` | loaded | [Ранения](armor-damage-wounds-will.md) — `JazzStackableMedicine` (Bandage/Morphine stacks) + kit charge UI helper |
| `System_JazzTraumaEffect.lua` | loaded | [Ранения](armor-damage-wounds-will.md) — parent `JazzTraumaEffect` for Trauma* tooltips (`ResolveValue("Description")` progress line; `GetDescription` raw for save) |
| `Save_CharacterEffectSerialize.lua` | loaded | [Runtime](runtime-editor-integration.md) — HOTFIX: empty `CharacterEffect` props → `{}`; sanitize `PlaceCharacterEffect('Id', )` on load (mid-combat `suppressionPinned` saves) |
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
| `System_NamedPerks.lua` | loaded | [Юниты и специализации](units-progression-specializations.md) — UNITS-006 named perks runtime (single module) |
| `System_HaveABlast.lua` | loaded | [Юниты и специализации](units-progression-specializations.md) — HaveABlast miss/hit grenade retaliate + inventory pull + −50% blast DR |
| `CombatActions.lua` (`Unit:Nazdarovya`) | loaded | [Юниты и специализации](units-progression-specializations.md) — Igor Nazdarovya every-turn drink |
| `Drunk.lua` (CE override) | loaded | Nazdarovya intoxication stacks ≤5; −15 CTH / +20 melee / stack; 3h sat decay |
| `System_AimHiringFilters.lua` | loaded | [Юниты и специализации](units-progression-specializations.md) |
| `System_HireContractDuration.lua` | loaded | [Юниты и специализации](units-progression-specializations.md) — AIM/AME chat `MaxDuration` 14→30; `GetMercDurationDiscountPercent` maxDay 14→30 |
| `System_AME_Filters.lua` | loaded | [Юниты и специализации](units-progression-specializations.md) — AME PDA filters (UNITS-005) |
| `System_AME_Browser.lua` | loaded | [Юниты и специализации](units-progression-specializations.md) — `PDAAIMEBrowser` + tab/hire wrap (UNITS-005) |
| `System_AME_Market.lua` | loaded | [Юниты и специализации](units-progression-specializations.md) — AME market tick/state (UNITS-005) |
| `System_AME_Mail.lua` | loaded | [Юниты и специализации](units-progression-specializations.md) — AME welcome/listing Email + read analytics; tab всегда открыт (UI-AME-001) |
| `System_RIS_Mail.lua` | loaded | [R.I.S.](ris-intelligence.md) — schema 3 queue/inbox migration, receipt-gated 2h/7h/5h desk (UI-RIS-002; runtime acceptance pending) |
| `System_RIS_Content.lua` | loaded | [R.I.S.](ris-intelligence.md) — generated dossiers, AAR v2, UI and Strategy localization banks |
| `System_RIS_Combat.lua` | loaded | [R.I.S.](ris-intelligence.md) — two-stage dossier counters + per-sector cumulative snapshot v3, baseline WIA, satellite/tactical AAR v2 |
| `System_RIS_Browser.lua` | loaded | [R.I.S.](ris-intelligence.md) — current-language Bulletin / Dossiers / Reports rendering |
| `System_RIS_Strategy.lua` | loaded | [R.I.S.](ris-intelligence.md) — read-only Legion AI observer + one-row Strategy dispatch; loaded after `Guardpost_Patrols.lua` |
| `System_AME_Browser_Template.lua` | source-only | [Юниты и специализации](units-progression-specializations.md) — editable source projected by `_install_ame_xtemplate_moditem.py` into loaded `ModItemXTemplate` `PDAAIMEBrowser` in `items.lua` (UNITS-005) |
| `System_AME_Nationalities.lua` | loaded | [Юниты и специализации](units-progression-specializations.md) — AME MercNationalities + flags (UNITS-005) |
| `System_IMP_StartingGear.lua` | loaded | [Юниты и специализации](units-progression-specializations.md) — IMP hire kit (IMP-001) |
| `System_IMP_Perks.lua` | loaded | [Юниты и специализации](units-progression-specializations.md) — Mimicry/Veteran/Sniper (IMP-001) |
| `AimHiringScreen_Template.lua` | dormant | [Юниты](units-progression-specializations.md), [runtime](runtime-editor-integration.md) |

## `jazz`: стратегия, UI и integration

| Файл | Статус | Документация |
|---|---|---|
| `Deployment.lua` | loaded | [Стратегия](strategy-squads-sectors.md) |
| `EnemySquad.lua` | loaded | [Стратегия](strategy-squads-sectors.md) |
| `Guardpost.lua` | loaded | [Стратегия](strategy-squads-sectors.md) |
| `Guardpost_Patrols.lua` | loaded, Legion Global AI director | [Стратегия](strategy-squads-sectors.md) |
| `FactionOverlay.lua` | loaded, faction matrix + ownership (014) | [Стратегия](strategy-squads-sectors.md) |
| `LegionUnitPrices.lua` | loaded | [Стратегия](strategy-squads-sectors.md), [легион tiers](legion-units-equipment-tiers.md) |
| `LegionSquadComposition.lua` | loaded | [Стратегия](strategy-squads-sectors.md), [легион tiers](legion-units-equipment-tiers.md) |
| `LegionSquadGenerator.lua` | loaded | [Стратегия](strategy-squads-sectors.md) |
| `LegionMilitiaRecruits.lua` | loaded (soft gate; 011 partial) | [Стратегия](strategy-squads-sectors.md) |
| `Regions_Sectors.lua` | loaded | [Стратегия](strategy-squads-sectors.md) |
| `Satellite_RegionBorders.lua` | loaded | [Стратегия](strategy-squads-sectors.md) — sat region edge overlay |
| `SatelliteSquad.lua` | loaded | [Стратегия](strategy-squads-sectors.md), [юниты](units-progression-specializations.md) — IMP hire gear rebuild (IMP-001) |
| `SatelliteSquadFixes.lua` | loaded, empty | [Стратегия](strategy-squads-sectors.md) |
| `POI Extension.lua` | loaded | [Стратегия](strategy-squads-sectors.md) |
| `System_SectorOperations.lua` | loaded | [Стратегия](strategy-squads-sectors.md) |
| `WorldFlipSpawnUnits.lua` | loaded | [Стратегия](strategy-squads-sectors.md) |
| `UtilityFunc.lua` | loaded | [Стратегия](strategy-squads-sectors.md), [runtime](runtime-editor-integration.md) |
| `LegionTierProgression.lua` | loaded | [Легион tiers](legion-units-equipment-tiers.md), [стратегия](strategy-squads-sectors.md) — Maps (time/mainland/mines) + NoMaps (mine/WorldFlip) |
| `VanillaDesyncFixes.lua` | loaded | [Runtime](runtime-editor-integration.md), [development](../development.md) — vanilla ending/statboost/RNG/shot vectors/AI area/buckshot/biases/craft |
| `EmptySquadFix.lua` | dormant | [Стратегия](strategy-squads-sectors.md), [runtime](runtime-editor-integration.md) |
| `PatrollingFix.lua` | dormant | [Стратегия](strategy-squads-sectors.md), [runtime](runtime-editor-integration.md) |
| `Savefix.lua` | dormant | [Стратегия](strategy-squads-sectors.md), [runtime](runtime-editor-integration.md) |
| `ConsoleFont.lua` | loaded | [UI](ui-audio-fx.md) |
| `EditorExtension.lua` | loaded, editor | [Runtime и инструменты](runtime-editor-integration.md) |
| `GameRules_HideAdvanced.lua` | loaded | [Runtime и инструменты](runtime-editor-integration.md) — скрывает все `advanced` GameRule из New Game / Options |
| `Debug.lua` | loaded, empty | [Runtime и инструменты](runtime-editor-integration.md) |

## `jazz`: звук и FX

- `CodeSounds.lua`, `CodeSounds_AK.lua`, `CodeSounds_AR.lua`, `CodeSounds_AR15.lua`, `CodeSounds_BoltR.lua`, `CodeSounds_MG.lua`, `CodeSounds_Pistols.lua`, `CodeSounds_SHOTGUNS.lua`, `CodeSounds_SVD.lua`, `CodeSounds_WW2Rifles.lua` — 10 loaded; `CodeSounds_SMG.lua` — empty stub, **не** в `metadata.code`; владелец [UI, звук и FX](ui-audio-fx.md).
- Все 113 `FX_*.lua` в текущем `Code/` перечислены в metadata и считаются loaded; владелец [UI, звук и FX](ui-audio-fx.md). Добавление/удаление проверять одновременно с metadata, SoundPreset, entity/state/spot и ресурсами.

## `jazz-maps`

| Файл | Статус | Документация |
|---|---|---|
| `Rebels_Loyalty.lua` | loaded | [Карты](maps-quests-dialogue.md), [стратегия](strategy-squads-sectors.md) |
| `System_JAZZ_CrocodilePatrol.lua` | loaded | [Карты](maps-quests-dialogue.md) |
| `System_JAZZ_Vehicles.lua` | loaded | [Автотранспорт](satellite-vehicles.md), [дизайн maps](../../../JAZZ%20Maps/docs/combat-vehicle-design.md), [стратегия](strategy-squads-sectors.md) |
| `System_JAZZ_VehicleCombat.lua` | loaded; tactical spawn dormant (`tactical_enabled=false`); stub устарел vs design | [Автотранспорт](satellite-vehicles.md), [дизайн maps](../../../JAZZ%20Maps/docs/combat-vehicle-design.md) |
| `System_VillaCounterAttack.lua` | loaded | [Каталог карт/квестов](maps-quests-content-catalog.md), JAZZ-QUESTS-003 |
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
| `jazz-nomaps/.github/workflows/discord-player-updates.yml` | GitHub Actions caller only | [Сводки изменений в Discord](discord-player-updates.md) |

## Generated data coverage

Generated ModItems покрываются системами по типу:

- core items/actions/effects/components/recipes/presets — combat, weapon, armor, inventory, UI/audio pages;
- maps sectors/quests/conversations/banters/loot/setpieces — maps и strategy pages;
- units UnitData/appearances/squads/archetypes/loot/voices — units, AI и strategy pages;
- assets EntityData/resources — assets page.

При появлении нового типа ModItem добавить его на профильную страницу и в этот раздел.
