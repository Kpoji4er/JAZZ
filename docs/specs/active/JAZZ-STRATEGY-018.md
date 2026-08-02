---
id: JAZZ-STRATEGY-018
status: implemented
owner: project-owner
systems:
  - legion-global-ai
  - enemy-squads
  - satellite-conflict
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-STRATEGY-018.md
  - jazz/docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md
  - jazz/Code/Guardpost_Patrols.lua
  - jazz/Code/SatelliteSquad.lua
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/showcase/ru/legion-strategy.md
  - jazz/docs/showcase/en/legion-strategy.md
  - jazz/docs/tools/_audit_faction_overlay_static.py
  - jazz/docs/tools/README.md
exclusive_resources:
  - GameVar:gv_JAZZ_LegionAI
related_decisions:
  - none
approved_by: project-owner chat 2026-08-02 — approve STRATEGY-018 (pathing vs player territory)
---

# JAZZ-STRATEGY-018: Legion pathing vs player territory

## Проблема

Playtest / Discord (Sergej 2026-08-02): логистические отряды Легиона нормально идут через сектора, уже занятые игроком — странно «везти алмазы по вражеской территории». [STRATEGY-007](JAZZ-STRATEGY-007.md) явно разрешил patrol в player sectors; для shipment/tax/supply отдельного avoid-player pathing нет.

## Цели

- Роли **recon / scout / patrol** могут ходить по player-controlled секторам.
- **Retribution** — приоритетный вход на player-территорию (карательная миссия).
- Логистика и support роли **обходят** player-controlled сектора, когда путь есть.
- Нет обхода → **не спавнить** новые logistics (кроме особого правила reinforce); уже существующие отряды **не убивать**.
- Уже идущий конвой при перекрытии пути player-сектором — **доезжает** до цели.

## Non-goals

- Блокировка player squad travel.
- Faction overlay / Adonis-Army pathing ([STRATEGY-014](JAZZ-STRATEGY-014.md) — отдельно).
- Полный rewrite satellite pathfinder vanilla.
- Запрет patrol на player sectors (007 для patrol остаётся).
- Despawn / abort существующих отрядов из‑за path policy.

## Locked defaults (owner 2026-08-02)

| Класс ролей | Нет avoid-player пути | Уже существующий / mid-route |
| --- | --- | --- |
| `recon` / scout / `patrol` | можно через player | n/a |
| `retribution` | можно; **приоритет** на player territory | n/a |
| `shipment`, `supply` | **не спавнить** | **оставить**; mid-route → **доехать** |
| `tax`, `manpower`, `recruiter` | **не спавнить** | **оставить** (не despawn) |
| `reinforce` | **спавнить**, но **не идти** (hold / no travel, пока нет обхода) | **оставить**; не форсировать путь через player |

Определение «player-controlled»: сектор под контролем player (и militia, если runtime считает их player side) — уточнить на implementation относительно helpers Legion AI.

Маршрутная политика: boatless / `land_water_boatless` (STRATEGY-007) + avoid-player filter для logistics/support.

## Требования

- `JAZZ-STRATEGY-018-REQ-001` — path filter: для `shipment` / `supply` / `tax` / `manpower` / `recruiter` / `reinforce` маршрут с входом в player-controlled sector **невалиден** для нового travel plan.
- `JAZZ-STRATEGY-018-REQ-002` — spawn gate: `shipment` / `supply` / `tax` / `manpower` / `recruiter` **не создаются**, если нет валидного avoid-player пути origin→destination.
- `JAZZ-STRATEGY-018-REQ-003` — `reinforce`: при отсутствии avoid-player пути **можно спавнить**, но отряд **не начинает travel** (ждёт валидный путь / hold).
- `JAZZ-STRATEGY-018-REQ-004` — уже существующие отряды затронутых ролей **не despawn** из‑за этой политики.
- `JAZZ-STRATEGY-018-REQ-005` — mid-route `shipment` / `supply` (и аналоги с payload в пути): при появлении player на маршруте — **доехать** текущим планом (не abort, не hard reroute-required).
- `JAZZ-STRATEGY-018-REQ-006` — `recon` / scout / `patrol` / `retribution` **не** режутся avoid-player filter; retribution сохраняет приоритет целей на player territory.
- `JAZZ-STRATEGY-018-REQ-007` — Documentation: technical routing + wiki/showcase одна фраза про логистику в обход.

## Инварианты и ограничения

- Не ломать valuables/cargo contract [STRATEGY-017](JAZZ-STRATEGY-017.md).
- Deterministic / NetSync для path choice, spawn skip и reinforce hold.
- Не отменять право patrol заходить в player sectors (007).
- Skip/hold spawn ≠ уничтожение уже существующих отрядов.

## Acceptance criteria

- `JAZZ-STRATEGY-018-AC-001` — runtime/human: player перекрыл единственный путь mine→Major → новый shipment **не** спавнится; уже идущий shipment **доезжает**.
- `JAZZ-STRATEGY-018-AC-002` — runtime/human: при наличии обхода shipment/supply/tax идут **мимо** player-controlled секторов.
- `JAZZ-STRATEGY-018-AC-003` — runtime/human: patrol и retribution **могут** войти в player sector.
- `JAZZ-STRATEGY-018-AC-004` — runtime/human: reinforce без обхода — отряд существует, **не** едет через player; при появлении обхода может начать travel.
- `JAZZ-STRATEGY-018-AC-005` — static/docs: technical + wiki/showcase в том же change set, что runtime.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: sat route planner / Legion spawn gates / reinforce idle hold; medium risk.
- Saves: без новой schema, если только path filter + spawn/hold gates (reinforce hold state — additive flag ok).
- Network/determinism: path + skip/hold must match hosts.
- Generated data: нет.
- Cross-package: `jazz` runtime only (ожидаемо).
- Rollback: feature flag / revert filter.

## План и ownership

- Пакет-владелец: `jazz`.
- Исполнитель: agent after `approved`.
- Reviewer: project-owner.
- Exclusive: `gv_JAZZ_LegionAI` — не параллелить с другой Legion AI волной.

## Решение владельца

- Статус: **implemented** (static wave; runtime/human AC still open)
- Discord Sergej + owner 2026-08-02:
  1. нет обхода → не спавнить (существующие оставить); **reinforce** — спавнить, но не идти;
  2. mid-route → **доехать**.
- `approved_by`: project-owner chat 2026-08-02.

## Evidence

- `JAZZ-STRATEGY-018-AC-001`: `BLOCKED (runtime/human)` — spawn gate wired; needs blocked-path playtest.
- `JAZZ-STRATEGY-018-AC-002`: `BLOCKED (runtime/human)` — avoid-player Dijkstra flag wired; needs route evidence.
- `JAZZ-STRATEGY-018-AC-003`: `PASS (static)` — patrol/retribution not in `lAvoidPlayerRoles`.
- `JAZZ-STRATEGY-018-AC-004`: `PASS (static)` — reinforce hold_for_path on failed assign.
- `JAZZ-STRATEGY-018-AC-005`: `PASS (static)` — technical + wiki + showcase updated.

## Documentation delta

- `docs/technical/systems/strategy-squads-sectors.md`
- `docs/wiki/legion-global-ai.md`, `docs/showcase/ru|en/legion-strategy.md`
- Roadmap §9.
