---
id: JAZZ-COMPAT-001
status: implemented
owner: project-owner
systems:
  - strategy-squads-sectors
  - inventory-items-loot
  - units-progression
repositories:
  - jazz
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-COMPAT-001.md
  - jazz/Code/StandaloneNoMapsFallback.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/docs/technical/compatibility.md
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/technical/systems/file-coverage.md
exclusive_resources:
  - Code:StandaloneNoMapsFallback.lua
  - GameVar:gv_JAZZ_StandaloneNoMaps
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-COMPAT-001: автономный fallback без jazz-maps (phase-1 / one-file in jazz)

> **Phase-1 only — temporary.** Урезанный one-file в core `jazz` уже в main.
> Целевой дизайн: отдельный пакет **`jazz-nomaps`** —
> draft [`JAZZ-COMPAT-002`](JAZZ-COMPAT-002.md).
> При реализации COMPAT-002 этот код **удаляется** из `jazz` и переносится в новый пакет;
> COMPAT-001 → `superseded`. **Не расширять** `StandaloneNoMapsFallback.lua` новыми фичами.

## Проблема

`jazz-maps` (`FhNNYd`) не объявлен зависимостью `jazz`, но без него:

- authored sector lists (`EnemySquadsGarrisonList` и др.) и map-placed loot из maps отсутствуют;
- Legion Global AI покрывает только authored Region `ErnieIsland` / `I7`;
- mainland аванпосты остаются на legacy/vanilla guardpost path.

Нужен урезанный, но играбельный режим `jazz` + `jazz-units` (+ assets/CommonLib) без maps.

## Цели

- Один loaded runtime-файл с gate «maps не загружен».
- Синтетические Legion AI regions по Voronoi-близости к `Guardpost`.
- Wiring role squad lists на аванпостах к `LegionGlobalAI_*` / `LegionJAZZSquad*`, если списки пусты.
- Подмена/усиление vanilla EnemySquad ID на jazz-пресеты при spawn, когда maps нет.
- Инъекция jazz-лута в контейнеры тактической карты (без map authoring).
- При загруженном `FhNNYd` файл полностью no-op.

## Non-goals

- Полный паритет квестов/диалогов/карт/`Maps/**` jazz-maps.
- Новые Region ModItems в editor (только runtime).
- Изменение поведения при активном jazz-maps.
- Обязательный showcase «maps optional» как поддерживаемая конфигурация релиза.

## Требования

- `JAZZ-COMPAT-001-REQ-001` — fallback активируется только если `FhNNYd` не в `ModsLoaded` / `IsModLoaded`.
- `JAZZ-COMPAT-001-REQ-002` — для каждого unmanaged `Guardpost` создаётся Region `JAZZ_Auto_<sector>` с `LegionAIEnabled`, `ManagedOutposts`, урезанными caps.
- `JAZZ-COMPAT-001-REQ-003` — сектора поверхности назначаются ближайшему аванпосту (Chebyshev по координатам ID).
- `JAZZ-COMPAT-001-REQ-004` — пустые role lists аванпоста заполняются существующими jazz EnemySquadDefs (если `jazz-units` их дал).
- `JAZZ-COMPAT-001-REQ-005` — spawn EnemySquad remaps известные vanilla ID → jazz equivalents при наличии defs.
- `JAZZ-COMPAT-001-REQ-006` — при входе на карту контейнеры получают дополнительный jazz loot roll (детерминированный seed).
- `JAZZ-COMPAT-001-REQ-007` — логика в одном `Code/StandaloneNoMapsFallback.lua`, wired в `items.lua` + `metadata.code` после Legion AI.

## Инварианты и ограничения

- Не трогать `jazz-maps/**`.
- Не ломать `ErnieIsland` managed outposts: auto-region не создаётся для уже managed аванпостов.
- Save: `gv_JAZZ_StandaloneNoMaps` только маркеры/флаги; Regions runtime могут пересоздаваться при load.
- Determinism: InteractionRand / BraidRandom с фиксированными context strings.
- Без `jazz-units` squad wiring и remap пропускаются без assert.

## Acceptance criteria

- `JAZZ-COMPAT-001-AC-001` — static: файл loaded; при `IsModLoaded("FhNNYd")` bootstrap не меняет `Regions` / sectors.
- `JAZZ-COMPAT-001-AC-002` — static: без maps bootstrap создаёт ≥1 `JAZZ_Auto_*` Region на кампании с ≥1 unmanaged Guardpost.
- `JAZZ-COMPAT-001-AC-003` — runtime: new game без maps — Legion AI ensure state видит auto-regions; spawn использует jazz lists.
- `JAZZ-COMPAT-001-AC-004` — runtime: container на exploration получает jazz item при inject path.
- `JAZZ-COMPAT-001-AC-005` — с maps включённым: поведение ErnieIsland/I7 без регрессии (no-op fallback).

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: optional incomplete install; полная suite по-прежнему канон.
- Saves: existing save без maps получает auto-regions на LoadGame/InitSatelliteView.
- Network: NetSync не добавляется; только session bootstrap.
- Generated data: ModItemCode + metadata.code.
- Cross-package: читает EnemySquadDefs/UnitData из jazz-units; maps не пишет.
- Rollback: удалить файл и ModItemCode/metadata entries.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: см. frontmatter

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner (запрос на реализацию одного файла + commit/push)
- Дата: 2026-07-30

## Evidence

- `JAZZ-COMPAT-001-AC-001`: `PASS (static)` — gate + load wiring.
- `JAZZ-COMPAT-001-AC-002`: `PASS (static)` — algorithm present; runtime count BLOCKED until playtest.
- `JAZZ-COMPAT-001-AC-003`: `BLOCKED (runtime)` — нужна new game без FhNNYd.
- `JAZZ-COMPAT-001-AC-004`: `BLOCKED (runtime)` — exploration inject.
- `JAZZ-COMPAT-001-AC-005`: `BLOCKED (runtime)` — smoke с maps.

## Documentation delta

- `docs/technical/compatibility.md` — truncated mode без maps.
- `docs/technical/systems/strategy-squads-sectors.md` — StandaloneNoMapsFallback.
- `docs/technical/systems/file-coverage.md` — новый loaded файл.
