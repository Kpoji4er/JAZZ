---
id: JAZZ-HOTFIX-004
status: approved
owner: project-owner
systems:
  - combat-actions
  - weapons-ammo
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - Code/System_EmplacementAmmo.lua
  - Code/System_OR_Unit.lua
  - docs/specs/active/JAZZ-HOTFIX-004.md
  - docs/tools/_audit_hotfix_004.py
  - docs/tools/_bump_metadata_hotfix004.py
  - docs/tools/README.md
  - docs/technical/systems/weapons-ammo-components.md
  - docs/technical/systems/combat-cth-actions.md
  - docs/technical/systems/file-coverage.md
  - docs/technical/override-matrix.md
  - docs/wiki/combat-actions.md
  - docs/showcase/ru/combat-actions.md
  - docs/showcase/en/combat-actions.md
  - metadata.lua
exclusive_resources:
  - jazz/metadata.lua
related_decisions:
  - none
related_specs:
  - JAZZ-HOTFIX-003
approved_by: project-owner
---

# JAZZ-HOTFIX-004: stationary MG control after load

## Проблема

Игрок теряет управление стационарным пулемётом (`MachineGunEmplacement` / `ManningEmplacement`): кнопки/огонь не отвечают, пока не слезть и сесть снова. Не suppression. Часто после загрузки сейва.

Vanilla `Unit:GameInit` зовёт `EnterEmplacement` до того, как у орудия есть `weapon`/visual (`SetDynamicData` → `Update`). `GetOperatePos()` тогда `nil` → `SetPos(nil)` и `obj.weapon.owner` падает. Статус `ManningEmplacement` уже висит. JAZZ `MachineGunEmplacement:Update` remap ammo пересоздаёт ствол на load и расширяет это окно. `Unit:ResolveDefaultFiringModeAction` вызывает `weapon:HasComponent` без nil-check — `RecalcUIActions` обрывается, HUD пустой. `MGRotate` для emplacement скрыт (`GetAPCost = -1`), поэтому без remount конус не вернуть.

## Цели

- После load/enter sector manning-юнит снова получает ствол орудия, валидную позицию и HUD без leave+enter.
- `EnterEmplacement` не делает `SetPos(nil)` и не падает, если ствол ещё не создан.
- `RecalcUIActions` / `ResolveDefaultFiringModeAction` не падают при отсутствии оружия.

## Non-goals

- Включать `MGRotate` на стационаре (vanilla скрывает его для `ManningEmplacement`).
- Менять CTH, ammo remap, suppression/pinned, portable `MGSetup`/`StationedMachineGun`.
- Переписывать vanilla `InterruptPreparedAttack` или сериализацию `g_Overwatch`.

## Требования

- `JAZZ-HOTFIX-004-REQ-001` — wrap `Unit:EnterEmplacement`: если нет `weapon` — вызвать `Update()`; если нет operate pos/weapon — сохранить `ManningEmplacement` + handle без `SetPos(nil)` / без обращения к `obj.weapon.owner` при nil.
- `JAZZ-HOTFIX-004-REQ-002` — после `LoadGame` и `EnterSector` (отложенный кадр) reseat всех живых `ManningEmplacement`: `Update` при отсутствии ствола, instant `EnterEmplacement`, `FlushCombatCache`, `RecalcUIActions(true)`; если нет `g_Overwatch.permanent` и команда `Idle` — `QueueCommand("MGTarget", "MGSetup", 0, facing)`.
- `JAZZ-HOTFIX-004-REQ-003` — `GetActiveWeapons` при manning: если `obj.weapon` nil, вызвать `obj:Update()` и повторить возврат ствола орудия.
- `JAZZ-HOTFIX-004-REQ-004` — `ResolveDefaultFiringModeAction` вызывает `HasComponent` только при валидном `weapon`; `RecalcUIActions` не индексирует `action.id`, если `GetDefaultAttackAction()` вернул nil.

## Инварианты и ограничения

- Public IDs `ManningEmplacement`, `MGLeave`, `MGRotate`, `MGSetup`, `MachineGunEmplacement` не меняются.
- Ammo remap `_50BMG_*` → `JAZZ_AMMO_50BMG_*` сохраняется.
- Pinned/suppression по-прежнему снимает prepared attacks (HOTFIX-003).
- Save schema не расширяется; reseat — runtime repair после load.
- Новые `_G` имена только top-level wrap flags / `Jazz_ReseatMannedEmplacements`.

## Acceptance criteria

- `JAZZ-HOTFIX-004-AC-001` — static: EnterEmplacement wrap + LoadGame/EnterSector reseat + GetActiveWeapons Update retry присутствуют в `System_EmplacementAmmo.lua` / `System_OR_Unit.lua`.
- `JAZZ-HOTFIX-004-AC-002` — static: `ResolveDefaultFiringModeAction` и `RecalcUIActions` nil-safe по auditor.
- `JAZZ-HOTFIX-004-AC-003` — technical + wiki + showcase RU/EN описывают, что стационарный пулемёт остаётся под контролем после загрузки сейва.
- `JAZZ-HOTFIX-004-AC-004` — runtime: загрузка сейва на occupied emplacement оставляет HUD/огонь без leave+enter.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: wrap vanilla `EnterEmplacement`; CommonLib 1.11 совпадающего override не содержит. JAZZ уже заменяет `GetActiveWeapons` / `RecalcUIActions` / `ResolveDefaultFiringModeAction`.
- Saves: совместимо; старые сейвы чинятся reseat-ом при load.
- Network/determinism: reseat по существующим handle; MGTarget только если конуса нет и Idle.
- Generated data: нет.
- Cross-package references: нет.
- Rollback/recovery: revert коммита `jazz`.

## План и ownership

- Пакет-владелец: `jazz`.
- Исполнитель / Reviewer: project-owner.
- Declared write set: frontmatter.
- Exclusive resources: frontmatter.

## Решение владельца

- Статус: `approved`.
- Кто подтвердил: project-owner — явный запрос «сделай патч и пуш» 2026-08-12.
- Дата: 2026-08-12.

## Evidence

- `JAZZ-HOTFIX-004-AC-001`: `PASS` (static) — `python docs/tools/_audit_hotfix_004.py`.
- `JAZZ-HOTFIX-004-AC-002`: `PASS` (static) — тот же auditor: HasComponent/action.id nil-guards.
- `JAZZ-HOTFIX-004-AC-003`: `PASS` (docs) — weapons-ammo-components, combat-cth-actions, wiki/showcase combat-actions RU/EN.
- `JAZZ-HOTFIX-004-AC-004`: `BLOCKED` (runtime) — load-on-emplacement smoke требует JA3.

## Documentation delta

- Technical: `weapons-ammo-components.md` (emplacement reseat), `combat-cth-actions.md` (HUD guards), `file-coverage.md`, `override-matrix.md` (`Unit:EnterEmplacement` wrap).
- Player wiki + showcase RU/EN: `combat-actions.md` — стационар остаётся под контролем после save/load.
