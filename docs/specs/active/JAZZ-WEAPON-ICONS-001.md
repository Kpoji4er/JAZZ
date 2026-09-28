---
id: JAZZ-WEAPON-ICONS-001
status: implemented
owner: project-owner
systems:
  - inventory-ui
  - weapons-ammo-components
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: not-required
write_set:
  - docs/specs/active/JAZZ-WEAPON-ICONS-001.md
  - docs/design/weapon-layer-icons/
  - docs/tools/weapon_layer_icons/
  - docs/tools/README.md
  - .agents/docs/playbooks/assets-and-ui.md
exclusive_resources:
  - none
related_decisions:
  - JAZZ-UI-001
approved_by: project-owner
---

# JAZZ-WEAPON-ICONS-001: isolated arsenal layer prototype

## Проблема

JAZZ-UI-001 implements chips and disables runtime baking. Mosin currently selects complete PNGs by Barrel; InventoryUI's GetItemUIIcon accepts a single path. Neither is a general layered weapon icon system. The arsenal includes old and new hosts with different attachment spots, dependencies and integral geometry.

## Цели

Deliver an executable offline prototype, inspectable images and an arsenal coverage audit. Define the production integration contract without changing loaded runtime.

## Non-goals

Active mod installation, publication, mass generation, registering new ModItemCode, changing shared runtime files, final art acceptance for every weapon, replacing JAZZ-UI-001 in the loaded game.

## Требования

- `JAZZ-WEAPON-ICONS-001-REQ-001` — Audit all local firearm definitions and their component options, including old weapons. Separate catalog coverage from rendered art coverage; unknown data must be reported.
- `JAZZ-WEAPON-ICONS-001-REQ-002` — Pure Lua selector returns a complete layer plan from current components and host profile. Explicit empty slots remain empty; missing components may use defaults. Host changes and parent-dependent layer variants participate in the cache key. Unknown configurations fall back as a whole.
- `JAZZ-WEAPON-ICONS-001-REQ-003` — Offline compositor and interactive review demonstrate transparent layers at fixed camera, framing and lighting. Declare ordering, integral-part limitations and nested attachment transforms; render actual source geometry for a representative host.
- `JAZZ-WEAPON-ICONS-001-REQ-004` — Exercise reversible changes, empty slots, host changes, missing art and ordering. Document integration with existing image binder without wrapping component setter or changing weapon/save state.
- `JAZZ-WEAPON-ICONS-001-REQ-005` — One arsenal-wide art style contract: camera convention, lighting, color treatment, outline, transparency, family scale and acceptance at actual icon size. New game captures and older weapons follow the same contract.
- `JAZZ-WEAPON-ICONS-001-REQ-006` — Isolated display-name prototype uses explicit class/host/structural-component rules. AK74 folding-stock family resolves to AKS-74 in either folded state; sights and minor attachments do not rename weapons. SVD→SVDS is a candidate pending actual model verification, not a blanket StockLight rule. No class replacement, save mutation or loaded localization changes.

## Инварианты и ограничения

All writes stay in the isolated worktree. Active jazz/jazz_assets are read-only. Existing dirty files are preserved. No global Lua installation, no game execution, no asset registration, no changes to Icon or weapon instance identity. Prototype assets and reports are not installed media.

## Acceptance criteria

- `JAZZ-WEAPON-ICONS-001-AC-001` — static/offline: arsenal report enumerates firearm candidates, slots, visual mappings and coverage gaps.
- `JAZZ-WEAPON-ICONS-001-AC-002` — offline Lua tests: A→B→A, default versus explicit empty, nested parent variants, changed host, unsupported fallback, deterministic ordering/key and no weapon mutation.
- `JAZZ-WEAPON-ICONS-001-AC-003` — offline render: actual geometry layers, composed output and interactive review share fixed framing; artifact QA checks dimensions/transparency and image inspected by agent.
- `JAZZ-WEAPON-ICONS-001-AC-004` — static: integration and limitations documented; shared runtime/generated files unchanged by this task.
- `JAZZ-WEAPON-ICONS-001-AC-005` — static: unified style and capture acceptance documented with objective checks and family-scale rules.
- `JAZZ-WEAPON-ICONS-001-AC-006` — offline: name resolver tests base/folding/both states/reversal, irrelevant optics, explicit empty/unknown host/class, localization fallback and unresolved SVD candidate without mutating item data.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: read source/data only; no loaded overrides. Prior chips contract stays active.
- Saves: none.
- Network/determinism: selector is local UI; no game RNG, serialization or network files.
- Generated data: none; future activation needs a separate approved integration phase.
- Cross-package references: source assets read-only, reports use logical IDs and portable relative outputs.
- Rollback/recovery: remove prototype write set; no installed state to restore.

## План и ownership

- Пакет-владелец: jazz tooling/prototype. 3D source ownership remains jazz_assets.
- Исполнитель: this isolated task.
- Reviewer: project-owner; independent human review remains subsequent to prototype delivery.
- Declared write set: frontmatter; README/playbook append only.
- Exclusive resources: none; metadata.lua/items.lua and existing Code files excluded.

## Решение владельца

- Статус: approved for isolated prototype and tests.
- Кто подтвердил: project-owner, task delegation explicitly authorizes implementation and tests in an isolated worktree and requests a verifiable prototype.
- Дата: 2026-09-28.
- Уточнение владельца в ходе работы: реальная M4 использует прямой ванильный магазин на 20 патронов; неверный snapshot layer исключён. Следующая отдельная сессия должна снимать фактическое оружие в игре. Сейчас запуск не запрошен.
- Дополнение владельца: весь арсенал должен иметь единый стиль; дополнительная задача — названия по значимым модулям, примеры АК74→АКС74 и СВД→СВДС. Реализуется как isolated prototype и явные правила, существующий запрет установки в игру сохраняется.

## Evidence

- `JAZZ-WEAPON-ICONS-001-AC-001`: `PASS` — static/offline, `docs/design/weapon-layer-icons/arsenal.json`: 182 local firearm/heavy definitions, 223 component definitions, 1909 slot options, zero extraction errors. Explicit inherited-data/art gaps retained.
- `JAZZ-WEAPON-ICONS-001-AC-002`: `PASS` — offline Lua via lupa, `docs/design/weapon-layer-icons/demo/verification.json`: 63 assertions including selector and same-instance UI binder lifecycle; no game validation claimed.
- `JAZZ-WEAPON-ICONS-001-AC-003`: `PASS` — offline Blender/Pillow, 16 registered transparent layers, five PNG comparisons, 96 exported browser choices (48 supported, 48 whole-icon fallbacks); contact-sheet inspected by agent. Interactive click QA not performed: in-app Browser rejected file URL under its URL policy. This does not assert game or browser runtime acceptance.
- `JAZZ-WEAPON-ICONS-001-AC-004`: `PASS` — static, isolated prototype files plus append-only tooling/playbook references. Existing runtime/generated files were never written by task. Integration boundaries sent to source task; design README covers capture and limitations.
- `JAZZ-WEAPON-ICONS-001-AC-005`: `PASS` — static, `docs/design/weapon-layer-icons/style-and-names.md`: shared art contract, family scale, capture reference sheet and actual-size/alpha/outline acceptance. Artistic approval remains future capture-stage work.
- `JAZZ-WEAPON-ICONS-001-AC-006`: `PASS` — offline Lua/current companion data, `names-verification.json`: 50 checks passed. AK74 structural naming implemented as isolated resolver; SVD candidate explicitly disabled pending model verification. No loaded names/localization changes.

Game runtime validation and independent owner review are subsequent stages before production activation; this spec is implemented, not accepted.

## Documentation delta

Design/prototype documentation only. Loaded runtime has not changed, so technical/wiki/showcase current-state pages must not claim the prototype is active.
