---
id: JAZZ-UI-001
status: implemented
owner: project-owner
systems:
  - weapons-ammo-components
  - inventory-ui
repositories:
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - Code/WeaponAttachChips.lua
  - Code/InventoryUI.lua
  - Code/WeaponIconBake.lua
  - Icons/Upgrades/
  - items.lua
  - metadata.lua
  - docs/specs/active/JAZZ-UI-001.md
  - docs/technical/systems/weapons-ammo-components.md
exclusive_resources:
  - items.lua
  - metadata.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-UI-001: inventory attachment chips (path B)

## Изменение scope 2026-10-02: отключение overlay-чипов

Решение владельца в текущем запросе: отключить чипы, рисовавшиеся поверх иконок оружия, поскольку сами иконки теперь показывают сборку. Этот раздел заменяет требования path B ниже; прежние требования сохранены как история.

- `JAZZ-UI-001-REQ-007`: `JazzAttachChips_Apply` больше не создаёт overlay; очищает и скрывает существующий `idJazzAttachChips` при обновлении HUD/inventory/stash.
- `JAZZ-UI-001-REQ-008`: изображения компонентов и их `ChipIcon` сохраняются; кнопки Fold/Flash UI-002 не отключаются. Generic `w_mod` на firearm остаётся скрытым.
- `JAZZ-UI-001-AC-007`: native UI probe — новый host не получает overlay, старый overlay очищается и скрывается; native weapon layers и кнопки управления сохраняются.
- Write set дополнен профильными wiki/showcase RU+EN и диагностическим Lua в `docs/tools/`; ownership/load order не меняются.

## Проблема

Иконки оружия в инвентаре — статичные template `Icon` PNG. Аттачи видны только в 3D-кабинете `ModifyWeaponDlg` либо как generic badge `UI/Inventory/w_mod`. Игрок не отличает сборки по иконке на тайле, в HUD и stash.

Runtime side-view bake (path E) оказался нестабилен по framing/chroma/пропорциям; owner выбрал path **B** (чипы слотов/компонентов рядом с template-иконкой).

## Цели

- Template `Icon` оружия не подменяется baked PNG.
- На тайле/HUD — **VWrap** chips top-left (3 в левом столбце, 4-й справа; 24px): `ChipIcon` / convention PNG / slot-fallback. Non-default **или** removable default с effects.
- `Icon` кабинета моддинга не заменяется миниатюрой; новый компонент = пара `Icon` + `ChipIcon`.
- Generic `w_mod` скрывается, когда показан хотя бы один chip.
- Save/network без PNG blob; UI rebuild из component data.
- Side-view bake path **выключен** (код может остаться dormant, без queue/`GetItemUIIcon` override).

## Non-goals

- Hand-painted overlay на силуэт ствола (`WeaponIconMod`) как primary path.
- Prebake комбинаций аттачей / runtime 3D capture в inventory icon.
- Подмена `Icon` файлом Chip-миниатюры.
- Изменение 3D-preview `ModifyWeaponDlg`.

## Требования

- `JAZZ-UI-001-REQ-001` — `Firearm` / `FirearmBase` `GetItemUIIcon` возвращает vanilla template `Icon` (bake override off).
- `JAZZ-UI-001-REQ-002` — helper собирает non-default `slot → component` с путём chip-картинки (`ChipIcon` → `Icon` → `Icons/Upgrades/slot_<family>.png`).
- `JAZZ-UI-001-REQ-003` — `XInventoryItem` / `UIWeaponDisplay` показывают chip row (до N иконок) для non-stock сборок.
- `JAZZ-UI-001-REQ-004` — при chip row > 0 badge `w_mod` / `idModIcon` скрыт.
- `JAZZ-UI-001-REQ-005` — stock/default config → без chips, vanilla `w_mod` behaviour (обычно скрыт т.к. CountWeaponUpgrades=0).
- `JAZZ-UI-001-REQ-006` — Chip-миниатюры живут в `Icons/Upgrades/Chips/<ComponentId>.png`; property `ChipIcon`; бэкап по слотам с ревью до wire.
- `JAZZ-UI-001-REQ-007` — multiplayer: только synced components; chips локальный UI, без сетевых файлов.
- `JAZZ-UI-001-REQ-008` — новый WeaponComponent: пара через **два** skill — `$create-jazz-component-icons` (`Icon`) и `$create-jazz-chip-icons` (`ChipIcon`); генерация не смешивается в одном skill.

## Инварианты и ограничения

- Публичные template `Icon` paths оружия на диске не затираются.
- Deterministic chip set от component map.
- Generated data: новые `ModItemCode` / Icon path на WeaponComponent — транзакция `items.lua` + `metadata.lua` (+ companion если есть).
- Owner go-ahead path B: 2026-07-30 («а дальше идем на B»).

## Acceptance criteria

- `JAZZ-UI-001-AC-001` — static: bake `GetItemUIIcon` override disabled / no bake queue from inventory resolve.
- `JAZZ-UI-001-AC-002` — static: chip helper + InventoryUI/HUD bind; `w_mod` suppressed when chips visible.
- `JAZZ-UI-001-AC-003` — sync-audit: `WeaponAttachChips.lua` (+ related) согласованы в `items.lua` + `metadata.lua`.
- `JAZZ-UI-001-AC-004` — runtime: оружие с scope/muzzle/stock ≠ default показывает соответствующие chips на тайле.
- `JAZZ-UI-001-AC-005` — runtime: stock config без chips; `w_mod` не остаётся «ложным» индикатором при chips.
- `JAZZ-UI-001-AC-006` — human: chips читаемы на inventory tile и UIWeaponDisplay.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: InventoryUI hook; no `GetItemUIIcon` replace for bake.
- Saves: без изменений schema.
- Generated data: да — code registration; Icon fills on empty components; upgrade PNG under `Icons/Upgrades/`.
- Cross-package: нет.
- Rollback: revert write set; bake можно вернуть отдельной spec.
- Risks: мелкий размер chips; нехватка уникального арта → slot-fallback.

## План и ownership

- Пакет-владелец: jazz
- Исполнитель: agent
- Reviewer: project-owner
- Порядок:
  1. Skill/prompt attachment icons + slot-fallback PNG.
  2. Wire empty component Icons → fallback/specific.
  3. `WeaponAttachChips.lua` + InventoryUI; disable bake.
  4. Sync + technical docs + runtime AC.

## Решение владельца

- Статус: approved (scope pivot bake → chips)
- Кто подтвердил: project-owner
- Дата: 2026-07-30
- Продуктовые решения:
  - fidelity = chip badges, not baked silhouette;
  - reuse `WeaponComponent.Icon` / generate slot fallbacks;
  - bake dormant.

## Evidence

- `JAZZ-UI-001-AC-001`: `PASS` (static) — bake unloaded: `WeaponIconBake.lua` not in `metadata.code` / `ModItemCode`; `GetItemUIIcon` not overridden; chips path B.
- `JAZZ-UI-001-AC-002`: `PASS` (static) — `WeaponAttachChips.lua` + InventoryUI/HUD bind; `w_mod` скрывается при chips.
- `JAZZ-UI-001-AC-003`: `PASS` (static) — `WeaponAttachChips` в `items.lua` / `metadata.lua`.
- `JAZZ-UI-001-AC-004`: `PASS` (runtime/human) — owner playtest 2026-07-31: non-default scope/muzzle/stock показывают chips на тайле.
- `JAZZ-UI-001-AC-005`: `PASS` (runtime/human) — owner playtest 2026-07-31: stock без chips; `w_mod` не ложный индикатор при chips.
- `JAZZ-UI-001-AC-006`: `PASS` (human) — owner: chips читаемы на inventory tile и UIWeaponDisplay.

## Documentation delta

- `docs/technical/systems/weapons-ammo-components.md` — Inventory icons → chips.
- Skill `$create-jazz-attachment-icons`; playbook assets-and-ui.

Evidence 2026-10-02: offline Lua regression PASS; Lua compilation PASS; generated sync 0 errors, 12 existing warnings. Native pre-fix fixture confirmed correct internal Grid layout. Post-fix editor round-trip / combat visual acceptance BLOCKED: game and editor closed before dispatch; manual scoped transaction used while closed. `_repair_ui002_stock_layout.lua` retained for subsequent official round-trip.

`JAZZ-UI-001-AC-007`: BLOCKED (native/editor acceptance); offline subset PASS в `_test_weapon_hud_overlays.py`. Spec Done gate не пройден: требуется новая проверка в движке; для UI-002 остаются ранее открытые AC-004/005. Коммит сохраняет локальную реализацию без заявления о runtime/human acceptance.
