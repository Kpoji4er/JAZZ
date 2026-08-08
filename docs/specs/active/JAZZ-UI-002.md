---
id: JAZZ-UI-002
status: implemented
owner: project-owner
systems:
  - weapons-ammo-components
  - combat-cth-actions
  - inventory-ui
repositories:
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - items.lua
  - metadata.lua
  - Code/System_WeaponCompHUD.lua
  - docs/specs/active/JAZZ-UI-002.md
  - docs/technical/weapons/combat-actions.md
  - docs/technical/systems/weapons-ammo-components.md
  - docs/technical/systems/combat-cth-actions.md
  - docs/wiki/combat-actions.md
  - docs/showcase/ru/combat-actions.md
  - docs/showcase/en/combat-actions.md
exclusive_resources:
  - items.lua
  - metadata.lua
related_decisions:
  - none
related_specs:
  - JAZZ-HOTFIX-003
  - JAZZ-UI-001
approved_by: project-owner
---

# JAZZ-UI-002: weapon manipulation chips (Fold/Flash) у иконки оружия

## Проблема

`FoldStock` / `UnFoldStock` / `FlashlightOn` / `FlashlightOff` имеют `ShowIn = "SignatureAbilities"` при `group = "Default"`. Они попадают в общий `ui_actions` hotbar, не переезжают в слот 13 (туда смотрит только `group == "SignatureAbilities"`), раздувают первый ряд и сдвигают кнопки на блок оружия.

## Цели

- Component toggles (приклад, фонарь) **не** видны в `CombatActionBar` / `ui_actions` hotbar.
- Surface = **вторая колонка** `UIWeaponDisplay` `idButtons` (`GridX = 2`) рядом со Switch/Reload.
- `GetUIState` для Fold/UnFold работает по любому Stock с валидным `zzFoldingPair`, не только `JAZZ_StockLight*`.
- `Unjam` остаётся на hotbar (`ShowIn = "CombatActions"`) по JAZZ-HOTFIX-003.

## Non-goals

- Перенос `Unjam` / `Reload` / `ChangeWeapon` в новую колонку.
- Чинить placement signature ability в слот 13.
- Новые иконки / AP costs / folding combat effects.
- Overlay-чипы на самой иконке оружия (углы).

## Требования

- `JAZZ-UI-002-REQ-001` — `FoldStock`, `UnFoldStock`, `FlashlightOn`, `FlashlightOff`: `ShowIn = false` (не `"CombatActions"` / не `"SignatureAbilities"`).
- `JAZZ-UI-002-REQ-002` — `UIWeaponDisplay` `idButtons`: колонка 1 = Switch + Reload; колонка 2 (`GridX = 2`) = `idFoldStockButton` + `idFlashlightButton` (стиль `MinWidth = 25`, `FoldWhenHidden`).
- `JAZZ-UI-002-REQ-003` — Fold-кнопка выбирает enabled half (`FoldStock` или `UnFoldStock`); Flash — `FlashlightOn` или `FlashlightOff`; OnPress через штатный CombatAction begin/execute.
- `JAZZ-UI-002-REQ-004` — Fold/UnFold `GetUIState`: Stock slot + non-empty `zzFoldingPair`; Unfolded → Fold, Folded → UnFold (naming: `UnFold`/`Unfold`/`UnFolded` vs `Fold`/`Folded` without Un*).
- `JAZZ-UI-002-REQ-005` — Flash `GetUIState` остаётся на Side + `zzFoldingPair`/известных Off/On id; кнопка скрыта без доступного half.
- `JAZZ-UI-002-REQ-006` — `Unjam` не меняет ShowIn/group относительно HOTFIX-003.
- `JAZZ-UI-002-REQ-007` — technical + wiki + showcase RU/EN описывают surface у иконки оружия (вторая колонка).

## Инварианты и ограничения

- Public IDs `FoldStock` / `UnFoldStock` / `FlashlightOn` / `FlashlightOff` / `Unjam` сохраняются.
- Save/network: только существующий `SetWeaponComponent` path; без новых sync fields.
- Generated: правка CombatAction + XTemplate в `items.lua`; новый Code — пара `items.lua` + `metadata.lua` code list.

## Acceptance criteria

- `JAZZ-UI-002-AC-001` — static: четыре toggles имеют `ShowIn = false`; Unjam остаётся `ShowIn = "CombatActions"`.
- `JAZZ-UI-002-AC-002` — static: `UIWeaponDisplay` содержит `idFoldStockButton` / `idFlashlightButton` с `GridX = 2`.
- `JAZZ-UI-002-AC-003` — static: Fold/UnFold `GetUIState` ссылается на `zzFoldingPair` (не только StockLight hardcode).
- `JAZZ-UI-002-AC-004` — runtime: складной приклад → чип во 2-й колонке; hotbar без сдвига на weapon UI; клик меняет Stock.
- `JAZZ-UI-002-AC-005` — runtime: фонарь → чип col2; клик переключает Side; без Side flashlight — кнопки нет.
- `JAZZ-UI-002-AC-006` — `_validate_items_quick.py` OK; docs sync в том же change set.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: JAZZ-only XTemplate override `UIWeaponDisplay` + CombatAction ShowIn.
- Saves: совместимо.
- Network/determinism: тот же NetStart/UIBegin path, что у других CombatAction.
- Generated data: да (`items.lua` / `metadata.lua`).
- Cross-package: нет.
- Rollback: вернуть ShowIn SignatureAbilities и убрать col2 кнопки.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: `items.lua`, `metadata.lua`

## Решение владельца

- Статус: `approved`
- Кто подтвердил: project-owner (plan attach → implement)
- Дата: 2026-08-08

## Evidence

- `JAZZ-UI-002-AC-001`: `PASS` (static) — `_audit_ui002_weapon_chips.py`: Fold/UnFold/Flash On/Off `ShowIn = false`; Unjam `ShowIn = "CombatActions"`.
- `JAZZ-UI-002-AC-002`: `PASS` (static) — `idFoldStockButton` / `idFlashlightButton` present with `GridX = 2` in `UIWeaponDisplay`.
- `JAZZ-UI-002-AC-003`: `PASS` (static) — FoldStock GetUIState uses `JazzWeaponCompHasFoldingPair` / `JazzWeaponCompIdLooksUnfolded`; helpers in `Code/System_WeaponCompHUD.lua`.
- `JAZZ-UI-002-AC-004`: `BLOCKED` (runtime) — needs in-game foldable stock + hotbar layout check.
- `JAZZ-UI-002-AC-005`: `BLOCKED` (runtime) — needs flashlight Side toggle on weapon chip.
- `JAZZ-UI-002-AC-006`: `PASS` (static) — `_validate_items_quick.py` OK; technical/wiki/showcase RU+EN + file-coverage updated.

## Documentation delta

- `docs/technical/weapons/combat-actions.md`
- `docs/technical/systems/weapons-ammo-components.md`
- `docs/technical/systems/combat-cth-actions.md`
- `docs/technical/systems/file-coverage.md`
- `docs/wiki/combat-actions.md`
- `docs/showcase/ru/combat-actions.md`
- `docs/showcase/en/combat-actions.md`
