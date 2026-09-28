---
id: JAZZ-WEAPON-CAPTURE-001
status: implemented
owner: project-owner
systems:
  - inventory-ui
  - weapons-ammo-components
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - docs/specs/active/JAZZ-WEAPON-CAPTURE-001.md
  - docs/tools/weapon_layer_icons/
  - docs/design/weapon-layer-icons/
  - docs/tools/README.md
exclusive_resources:
  - live JA3Debug capture camera
related_decisions:
  - JAZZ-WEAPON-ICONS-001
approved_by: project-owner delegated agent self-review
---

# JAZZ-WEAPON-CAPTURE-001: runtime arsenal capture and naming SDD

## Проблема

Offline source scenes can disagree with installed weapons (M4 straight vanilla 20-round magazine). Production art needs actual runtime models, consistent photography, and coverage across the arsenal.

## Цели

Capture the running game's weapon catalog and structural variants; deliver staged icons, names matrix, SDD and reviewed report with honest coverage and defects.

## Non-goals

Installing or publishing artwork/code, altering weapon balance, changing active mod files, savegame replacement, rebuilding mounts. Mounts are a separate future phase.

## Требования

- `JAZZ-WEAPON-CAPTURE-001-REQ-001` — Enumerate live firearm/heavy definitions and actual entity/component/name data; distinguish runtime catalog from earlier static snapshot.
- `JAZZ-WEAPON-CAPTURE-001-REQ-002` — Photograph live temporary weapon visuals under a common camera/light recipe and generate staged transparent icons with traceable source/configuration data. Failed or visually broken assets must be flagged, not silently accepted.
- `JAZZ-WEAPON-CAPTURE-001-REQ-003` — Survey structural modules and names across the catalog; preserve unique names, ignore minor accessories for naming, document unresolved model identities. Mounts remain provisional and independently replaceable.
- `JAZZ-WEAPON-CAPTURE-001-REQ-004` — Restore camera/light/render settings and dispose temporary objects. Never change merc inventories, save progress, install code or reactivate dormant bake hooks. Produce self-reviewed SDD under owner's delegated approval.

## Инварианты и ограничения

Source/mod files read-only; writes restricted to isolated worktree and temporary engine output for capture when required by engine API. Temporary game-thread objects are allowed by explicit capture authorization; restore state. No debugger initialize/pause needed for live eval. No game launch/termination required: owner supplied running game. User approved image collection and self-approval of SDD on 2026-09-28.

## Acceptance criteria

- `JAZZ-WEAPON-CAPTURE-001-AC-001` — runtime: catalog exported with count and per-class actual data.
- `JAZZ-WEAPON-CAPTURE-001-AC-002` — runtime/artifact: every enumerated firearm has an image or explicit recorded failure; structural variants covered or recorded as pending. Alpha/dimensions/cropping validated; contact sheets inspected.
- `JAZZ-WEAPON-CAPTURE-001-AC-003` — static + runtime: naming matrix covers catalog and identifies rules versus candidates; SDD records deferred mounts and replay requirements.
- `JAZZ-WEAPON-CAPTURE-001-AC-004` — runtime + static: cleanup verified, active files not written, SDD self-review and final coverage summary delivered.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: existing loaded definitions used; transient capture helpers only.
- Saves: no changes saved, no inventory changes.
- Network/determinism: no multiplayer use; disposable capture objects created in game thread.
- Generated data: none.
- Cross-package references: actual entity names logged; no sibling writes.
- Rollback/recovery: capture finally cleanup restores camera/render/light, removes temporary visuals; no installation to roll back.

## План и ownership

- Пакет-владелец: jazz tooling and staged art.
- Исполнитель/reviewer: agent, self-review explicitly delegated by owner; not falsely described as independent review.
- Declared write set: frontmatter; temporary capture outputs may use AppData when engine requires virtual path.
- Exclusive resources: live capture camera; coordinate with source task.

## Решение владельца

- Статус: approved, SDD decisions/self-review delegated to agent.
- Кто подтвердил: owner: «запустил игру… ковыряйся, собирай картинки и имена оружки… в конце sdd (сам прочитай и апрувни), иконки и сводку… крепления отдельно… потом».
- Дата: 2026-09-28.

## Evidence

- `JAZZ-WEAPON-CAPTURE-001-AC-001`: `PASS` — runtime, `docs/design/weapon-layer-icons/live/catalog.json`: 183 effective temporary firearm/heavy instances with current names/entities/components. Initial class snapshot retained as `catalog-before-capture.json`; class/preset ID differences for four quest variants explicitly documented and both photographed.
- `JAZZ-WEAPON-CAPTURE-001-AC-002`: `PASS` — runtime + artifact, `live/staged/integrity.json`: 1779 expected unique single-slot configurations covered, 1811 total records including 32 deliberate extra preset/RIS configurations; 1795 PNG icons and 16 recorded stock-configuration RIS refusals. All 183 defaults photographed; 188 structural alternatives catalogued. Oversized Barrett/Gewehr98/M24 families recaptured; no remaining automatic crop/dark/empty-image flags among captured frames. Eight default contact sheets and targeted structural/M4-magazine/SVD variants inspected. Full multi-slot cartesian coverage and manual inspection of every optic are not claimed.
- `JAZZ-WEAPON-CAPTURE-001-AC-003`: `PASS` — static/offline + runtime source evidence, `live/SDD.md`, `live/staged/name-matrix.json`, `names.md`, `weapon-names.csv`: all 183 names; explicit AK74/AKM/VZ58 stock rules, SVDS rejected for photographed thumbhole stock, unique names preserved, mounts provisional. 72 Lua name checks pass. SDD approved by the executing agent under owner's explicit self-review delegation, not independent/human acceptance.
- `JAZZ-WEAPON-CAPTURE-001-AC-004`: `PASS` — runtime + static, final batch receipts show original camera, render flags and light restored and disposable objects released. Separate `live/cleanup.json` confirms zero objects near the capture stage, original camera, Dry_Coastal_Day, time factor 1100; Computer Use confirms normal restored scene. Diagnostic overlay hidden with log retained. All writes are tooling/staged files in this worktree; no active mod/source/icon/localization files installed or changed by this task. `live/REPORT.md` provides coverage, limitations and review queue.

Self-review discovered and corrected a misleading light recipe label: engine table.copy(Preset) yielded empty defaults; explicit-default replay matches the actual captured profile (mean solid-weapon RGB delta 0.88/255). Original receipts remain intact; `live/lighting-consistency.json` and SDD explain this. Declared-vs-vis.parts discrepancies are a review queue, not unverified claims of broken models.

Spec remains implemented in active. Independent review and human production acceptance are subsequent stages; approved SDD does not install the UI feature.

## Documentation delta

Staged design/SDD only; current-state runtime docs unchanged because no production activation is performed.
