---
id: JAZZ-UI-001
status: approved
owner: project-owner
systems:
  - weapons-ammo-components
  - inventory-ui
repositories:
  - jazz
risk: high
generated_data: true
runtime_validation: required
write_set:
  - Code/WeaponIconBake.lua
  - Code/InventoryUI.lua
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

# JAZZ-UI-001: side-view weapon icons with attachments

## Проблема

Иконки оружия в инвентаре — статичные template `Icon` PNG. Аттачи видны только в 3D-кабинете `ModifyWeaponDlg` либо как generic badge `UI/Inventory/w_mod`. Игрок не отличает сборки по иконке на тайле, в drag ghost, rollover и stash.

Доказательства текущего контракта:

- `InventoryItem:GetItemUIIcon()` возвращает `self.Icon` (vanilla `Inventory.lua`);
- inventory UI рисует `idItemImg` из `GetItemUIIcon`, опциональный `SubIcon`, и `w_mod` при `CountWeaponUpgrades > 0` (`InventoryUI.lua`);
- `ModifyWeaponDlg` строит живую модель через `CreateVisualObj` / `UpdateVisualObj` с entity аттачей;
- JAZZ property `WeaponIconMod` на `WeaponComponentVisual` объявлено, но runtime не читает;
- MiniMap / `WaitCaptureScreenshot` / `IsolatedObjectScreenshot` — fullscreen framebuffer capture, не готовый inventory RT.

## Цели

- Side-view bake собранного 3D-оружия (аттачи на силуэте) заменяет эффективную иконку экземпляра.
- Одинаковый набор модулей → один shared cache entry (fingerprint), не PNG на каждый instance id.
- Все UI-поверхности, которые резолвят `GetItemUIIcon`, показывают baked path.
- Stock / default config или сбой bake → template `Icon`.
- PNG не сериализуются в save/network; rebuild из component data.
- При активной baked-иконке badge `w_mod` подавляется (моды уже на силуэте).

## Non-goals

- Hand-painted overlay-система через `WeaponIconMod` как primary path (свойство может остаться unused).
- Prebake всех комбинаций аттачей в пакет мода.
- Изменение 3D-preview `ModifyWeaponDlg` (кабинет остаётся showcase; может только триггерить bake).
- Engine offscreen RT / настоящие 3D XImage-виджеты.
- Идеальный style-match с hand-painted `WeaponIcons/*.png` в MVP (принимаем render look; framing итерируется отдельно).
- Полный offline prebake всех комбинаций аттачей.

## Требования

- `JAZZ-UI-001-REQ-001` — для `Firearm` / `FirearmBase` `GetItemUIIcon` возвращает путь baked PNG при cache hit для текущего fingerprint.
- `JAZZ-UI-001-REQ-002` — fingerprint = `weapon.class` + детерминированная карта `slot → component id`; идентичные сборки разделяют один cache file.
- `JAZZ-UI-001-REQ-003` — bake job строит visual через `CreateVisualObj` / `UpdateVisualObj`, фиксированный side framing; аттачи визуально присутствуют на снимке.
- `JAZZ-UI-001-REQ-004` — после успешного изменения компонентов ставится invalidate/rebake; при cache miss первый UI resolve ставит lazy bake в очередь (не блокирует кадр синхронным fullscreen capture дольше согласованного hitch budget из spike).
- `JAZZ-UI-001-REQ-005` — cache miss до завершения bake, ошибка bake, или stock/default component set → template `Icon` без ошибки UI.
- `JAZZ-UI-001-REQ-006` — save/network не содержат PNG blob; только существующая сериализация компонентов оружия определяет возможность rebuild на клиенте.
- `JAZZ-UI-001-REQ-007` — когда `GetItemUIIcon` отдаёт baked path, inventory tile не показывает `w_mod` badge для этого оружия.
- `JAZZ-UI-001-REQ-008` — cache files живут под AppData (или эквивалент, подтверждённый spike); ModifyWeaponDlg может триггерить bake на apply/close, но capture viewport — dedicated bake job, не кабинет игрока.
- `JAZZ-UI-001-REQ-009` — multiplayer: каждый клиент бэйкит локально из synced component state; файлы кэша не синхронизируются по сети.

## Инварианты и ограничения

- Публичные template `Icon` paths в InventoryItem definitions не затираются на диске мода; меняется только runtime resolve.
- Vanilla `ModifyWeaponDlg` 3D pipeline и component apply semantics сохраняются.
- Deterministic fingerprint: одинаковый набор слотов даёт одинаковый ключ на всех клиентах/запусках.
- Не смешивать bake hitch с критическими combat/net ticks; bake в real-time queue.
- Generated data: регистрация нового `ModItemCode` и любых UI overrides — одна транзакция `items.lua` + `metadata.lua` + companion.
- Owner go-ahead («Давай», 2026-07-29) разрешает implementation при provisional spike acceptance ниже; human AC-005..008 остаются обязательными до `implemented`/`accepted`.

### Spike gates (provisional → human confirm)

1. **Path load** — provisional PASS: MiniMap pattern `AppData/Editor/<modId>/…png` + `UIL.MeasureImage` / `UIL.DrawXImage`; inventory binds via `JazzWeaponIcon_ApplyToXImage` (src_rect from MeasureImage when ResourceManager miss).
2. **Side capture** — provisional: dedicated bake job + `WaitCaptureScreenshot` (MiniMap) / IsolatedObject hide pattern; human confirm framing.
3. **Background** — MVP: black sky (`RenderSky=0`); accept for MVP, iterate chroma later if needed.
4. **Hitch budget** — strategy locked: async real-time queue, one bake at a time, lazy on UI miss + trigger on `SetWeaponComponent` / `WeaponModifiedSuccess`; no sync capture inside `GetItemUIIcon`.

## Acceptance criteria

- `JAZZ-UI-001-AC-001` — static: override `GetItemUIIcon` для firearm; fingerprint helper детерминирован; нет записи PNG в save helpers.
- `JAZZ-UI-001-AC-002` — static: bake использует `CreateVisualObj`/`UpdateVisualObj`; trigger на component change + lazy queue на miss.
- `JAZZ-UI-001-AC-003` — static: `w_mod` suppressed when baked icon active.
- `JAZZ-UI-001-AC-004` — sync-audit: `WeaponIconBake.lua` (и UI hook files) согласованы в `items.lua` + `metadata.lua`.
- `JAZZ-UI-001-AC-005` — runtime: два экземпляра одного class с одинаковыми компонентами показывают один и тот же baked path/файл.
- `JAZZ-UI-001-AC-006` — runtime: смена scope/muzzle/stock в ModifyWeapon → после bake иконка в инвентаре отражает аттачи; stock config или bake fail → template `Icon`.
- `JAZZ-UI-001-AC-007` — runtime/human: drag ghost, rollover и inventory tile используют baked icon (не расходятся).
- `JAZZ-UI-001-AC-008` — human: spike gates 1–4 закрыты evidence до approve; после implement — playtest framing приемлем как MVP.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: last-writer override `GetItemUIIcon` и тонкий InventoryUI hook для `w_mod`; capture API — vanilla CommonLua. Нет зависимости от мода MiniMap (только reference pattern).
- Saves: schema без PNG; после load иконки появляются после cache hit или lazy bake. Старые сейвы совместимы.
- Network/determinism: component sync без изменений; bake локальный, non-hashed visual cache.
- Generated data: да — `ModItemCode` (+ optional XTemplate/InventoryUI companion registration).
- Cross-package: нет (`jazz` only). Assets package не требует prebaked icons.
- Rollback/recovery: revert write set; удалить AppData cache dir вручную при необходимости.
- Risks: style clash с painted icons; capture hitch/queue; dynamic path registration; framing pistol vs MG; multiplayer local cache divergence until bake completes (fallback Icon).

## План и ownership

- Пакет-владелец: jazz
- Исполнитель: agent (после approved)
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: `items.lua`, `metadata.lua`
- Порядок работ после approve:
  1. Закрыть spike gates evidence в разделе Evidence / owner notes.
  2. Реализовать `Code/WeaponIconBake.lua` + hooks.
  3. Sync generated data.
  4. Runtime AC + technical docs.
  5. DoD validator.

## Решение владельца

- Статус: approved (код в ветке; `implemented`/`accepted` после runtime AC-005..008)
- Кто подтвердил: project-owner («Давай»)
- Дата: 2026-07-29
- Продуктовые решения:
  - fidelity = side-view 3D silhouette with attachments;
  - replace icon everywhere via `GetItemUIIcon`;
  - cache by module fingerprint (shared across instances).
- Spike gates: provisional accept on MiniMap AppData/UIL pattern + async queue; human playtest closes AC-005..008.

## Evidence

- `JAZZ-UI-001-AC-001`: `PASS` — static: `FirearmBase:GetItemUIIcon` + fingerprint/`xxhash` cache; no PNG save helpers in `WeaponIconBake.lua`.
- `JAZZ-UI-001-AC-002`: `PASS` — static: bake uses `CreateVisualObj`/`UpdateVisualObj`; queue on `SetWeaponComponent` / `WeaponModifiedSuccess` / resolve miss.
- `JAZZ-UI-001-AC-003`: `PASS` — static: `XInventoryItem:OnContextUpdate` hides `idItemModImg` when `JazzWeaponIcon_HasBakedIcon`.
- `JAZZ-UI-001-AC-004`: `PASS` — sync: `Code/WeaponIconBake.lua` in `items.lua` ModItemCode + `metadata.code` before `InventoryUI.lua`; audit WARNINGS only (pre-existing orphans).
- `JAZZ-UI-001-AC-005`: `BLOCKED` — runtime playtest (two instances same fingerprint).
- `JAZZ-UI-001-AC-006`: `BLOCKED` — runtime playtest (modify → bake → inventory).
- `JAZZ-UI-001-AC-007`: `BLOCKED` — runtime/human (tile / drag / rollover).
- `JAZZ-UI-001-AC-008`: `BLOCKED` — human framing / spike confirm on capture quality.

### Spike evidence

- Gate 1 Path load: `PASS (provisional)` — MiniMap `AppData/Editor` + `JazzWeaponIcon_ApplyToXImage`.
- Gate 2 Side capture: `BLOCKED` — needs human bake screenshot in-game.
- Gate 3 Background: `PASS (provisional)` — black sky MVP.
- Gate 4 Hitch budget: `PASS (provisional)` — async single-flight queue in code.

## Documentation delta

- `docs/technical/systems/weapons-ammo-components.md` — секция Inventory icons (JAZZ-UI-001).
- Player wiki: follow-up после accept.
