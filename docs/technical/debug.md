# Debug и читы для разработки

Developer cheat-sheet по vanilla JA3 и JAZZ. Не игроковая wiki: команды ломают баланс, сейвы и детерминизм. Использовать только для диагностики и проверки контента.

Уровень подтверждения: **static** по `<JA3_ROOT>/ModTools/Src` и загруженному коду JAZZ.

## Предусловия

Читы и консоль доступны, когда `AreCheatsEnabled()` истинно:

- `Platform.cheats`, или
- `Platform.trailer`, или
- `AreModdingToolsActive()` (открыт Mod Editor / modding tools).

| Действие | Хоткей / вызов | Примечание |
|---|---|---|
| Открыть консоль | `Enter` или `Alt-Shift-C` | Также `ShowConsole(true)` |
| Меню Cheats | Esc → Cheats (если читы включены) | Часть читов только отсюда |

Без `Platform.developer` флаг `gv_Cheats.Teleport` по умолчанию **выключен**: хоткей телепорта disabled, пока чит не включат явно.

`Code/Debug.lua` в JAZZ загружается (`metadata.code`), но сейчас **пустой placeholder** — своих helper-функций нет.

## Satellite / глобалка

### Телепорт отряда в сектор

Vanilla уже умеет телепортировать выбранный player squad на сектор под курсором.

1. Включить чит Teleport (раскрывает все сектора):

```lua
CheatEnableTeleport()
-- эквивалент: NetSyncEvent("CheatEnable", "Teleport", true)
```

2. Открыть satellite view, выбрать отряд.
3. Навести курсор на целевой сектор.
4. Нажать **Ctrl-T**.

Цепочка: `CheatTeleportToCursor()` → `NetSyncEvent("CheatSatelliteTeleportSquad", squad_id, sector_id)`.

В JAZZ обработчик — `NetSyncEvents.CheatSatelliteTeleportSquad` в `Code/SatelliteSquad.lua` (override vanilla). При телепорте в неоткрытый сектор без reveal отряд может быть невидим — сначала `RevealAllSectors()` или `CheatEnableTeleport()`.

| Действие | Хоткей / Lua | Примечание |
|---|---|---|
| Включить Teleport + reveal | `CheatEnableTeleport()` | Меню Cheats → Enable Teleport |
| Телепорт к курсору | **Ctrl-T** | Нужны satellite view, выбранный squad, сектор под мышью |
| Телепорт по ID сектора | см. ниже | Консоль |

Телепорт выбранного squad по ID сектора:

```lua
local sat = GetSatelliteDialog()
local sq = sat and sat.selected_squad
if sq then
  NetSyncEvent("CheatSatelliteTeleportSquad", sq.UniqueId, "H12")
end
```

Замените `"H12"` на нужный sector ID. Squad должен иметь окно на карте (`g_SatelliteUI.squad_to_wnd`); иначе handler выходит рано.

### Прочее на глобалке

| Действие | Хоткей / Lua | Примечание |
|---|---|---|
| Reveal all sectors | `RevealAllSectors()` | Также из меню Cheats |
| Show squads power | `NetSyncEvent("CheatEnable", "ShowSquadsPower")` | Toggle |
| Auto-resolve wins | `NetSyncEvent("CheatEnable", "AutoResolve")` | Toggle |
| Disable discovery alert | `NetSyncEvent("CheatEnable", "DisableDiscoveryAlert")` | Toggle |
| Spawn enemy squad | `CheatSpawnEnemySquad("H12", "EmeraldCoast")` | Второй аргумент — `EnemySquadDefs` id |
| Set city loyalty | `CheatSetLoyalty("ErnieVillage", 100)` | Город + целевой loyalty |

## Бой / тактика

| Действие | Хоткей / Lua | Примечание |
|---|---|---|
| God Mode (PoV team) | меню Cheats / `CheatPoVTeam("GodMode")` | Toggle по стороне |
| Infinite AP | `CheatPoVTeam("InfiniteAP")` | Toggle |
| Grant 100 AP | **Ctrl-Alt-J** | Выбранный юнит |
| Grant 10 AP | меню Cheats → Grant 10 AP | |
| Remove 1 AP | меню Cheats | |
| Heal all mercs | меню Cheats → Heal Mercs / `CheatHealAllMercs()` | |
| Add ammo (selected) | меню Cheats / `CheatAddAmmo(SelectedObj)` | |
| +10 merc stats | `NetSyncEvent("CheatAddMercStats")` | |
| Level up selected | меню Cheats / `CheatSelectedObjLevelUp()` | |
| Always Hit | `NetSyncEvent("CheatEnable", "AlwaysHit")` | Взаимоисключает Always Miss |
| Always Miss | `NetSyncEvent("CheatEnable", "AlwaysMiss")` | |
| Skill checks pass | `NetSyncEvent("CheatEnable", "SkillCheck")` | |
| Kill all enemies | меню Cheats / `NetSyncEvent("KillAllEnemies")` | |
| Panic selected | меню Cheats | Нужен `SelectedObj` Unit |
| Select any unit | **Ctrl-Shift-MouseM** (Select) | Developer selection |
| Clear selection | **Ctrl-Shift-MouseM** (Clear) | Тот же бинд в другом action |
| Reveal traps in sight | меню Cheats / `CheatRevealTrapsIG()` | |
| Full visibility | `NetSyncEvent("CheatEnable", "FullVisibility", true)` | Также путь Quick Test Ambient Life (**Alt-Shift-A**) |
| One-HP enemies | `NetSyncEvent("CheatEnable", "OneHpEnemies")` | |
| Free Parts / Free Meds | `NetSyncEvent("CheatEnable", "FreeParts")` / `"FreeMeds"` | |
| Signature no CD | `NetSyncEvent("CheatEnable", "SignatureNoCD")` | |
| AI debug mode | `CheatOpenAIDebug()` | Только в бою, не net-game |

Тактический телепорт юнита (не satellite): при включённом `CheatEnabled("Teleport")` тот же **Ctrl-T** вызывает `CheatTeleportToCursor()` и ставит выбранного юнита на slab под курсором через combat action `Teleport`.

## Стратегия / ресурсы

| Действие | Lua | Примечание |
|---|---|---|
| +$100 000 | `NetSyncEvent("CheatGetMoney")` | Меню Cheats → Get $100 000 |
| Add merc by id | `CheatAddMercIG("Igor")` | В подходящий player squad |
| Remove merc | `CheatRemoveMercIG(merc)` | |
| Hire status | `CheatSetMercHireStatus(merc_id, status)` | |
| Reveal intel (current sector) | меню Cheats → Reveal Intel | |
| Respec perks | меню Cheats / `CheatRespecPerkPoints(unit)` | |
| Restore energy | `CheatRestoreEnergy()` | |

## Консоль и инструменты

| Действие | Вызов | Примечание |
|---|---|---|
| Показать консоль | `ShowConsole(true)` | Нужны cheats / modding tools |
| Очистить debug draw | **F9** (DE_ClearScreen) | |
| Reload Lua | `ReloadLua()` | Опасно: состояние сессии может стать неконсистентным |
| Combat Log | UI Combat Log | При modding/developer виден filter **debug** |
| CTH breakdown (точные %) | — | При `AreModdingToolsActive()` crosshair показывает проценты вместо `+`/`−` (см. accuracy-model) |

Полезные однострочники в консоли:

```lua
-- Текущий сектор и выбран
Inspect(gv_CurrentSectorId)
Inspect(GetSatelliteDialog() and GetSatelliteDialog().selected_squad)

-- Сектор по ID
Inspect(gv_Sectors["H12"])

-- Включить полный fog reveal
RevealAllSectors()
```

## JAZZ-specific

| Действие | Lua | Примечание |
|---|---|---|
| Legion Global AI diagnostics | `Inspect(JAZZ_LegionAIGetDiagnostics())` | Сводка major + regions; `Code/Guardpost_Patrols.lua` |
| Region heat / state | `Inspect(JAZZ_GetLegionAIRegionState("Ernie"))` | Без `create` — только существующее |
| Squad role icon (managed) | `JAZZ_GetLegionAISquadIcon(squad)` | |
| Squad task text | `JAZZ_GetLegionAISquadTaskText(squad)` | |
| CTH debug UI | — | Автоматически при активных modding tools |
| Debug.lua helpers | — | Файл loaded, пустой; helpers пока не добавлены |

## Источники

| Слой | Путь |
|---|---|
| Vanilla cheats | `<JA3_ROOT>/ModTools/Src/Lua/Cheat.lua` |
| Hotkeys / Cheats menu actions | `<JA3_ROOT>/ModTools/Src/Lua/XTemplates/GameShortcuts.lua` |
| Cheats UI list | `<JA3_ROOT>/ModTools/Src/Lua/XTemplates/CheatsList.lua` |
| Satellite teleport (JAZZ) | `Code/SatelliteSquad.lua` → `NetSyncEvents.CheatSatelliteTeleportSquad` |
| Legion AI diagnostics | `Code/Guardpost_Patrols.lua` → `JAZZ_LegionAIGetDiagnostics` |
| Runtime / placeholders | [runtime-editor-integration.md](systems/runtime-editor-integration.md) |
| CTH debug UI | [weapons/accuracy-model.md](weapons/accuracy-model.md) |
